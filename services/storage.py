import os
from typing import List, Tuple
from uuid import uuid4


class StorageBackend:
    def save_files(self, entity_type: str, entity_id: int, filenames_and_bytes: List[Tuple[str, bytes]]) -> List[Tuple[str, str]]:
        """
        Save multiple files.

        Returns list of (key, url) for each saved file.
        """
        raise NotImplementedError


class LocalStorage(StorageBackend):
    def __init__(self, base_dir: str = "uploads", public_base_path: str = "/uploads"):
        self.base_dir = base_dir
        self.public_base_path = public_base_path.rstrip("/")

    def _ensure_dir(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def _safe_name(self, original: str) -> str:
        _, ext = os.path.splitext(original)
        return f"{uuid4().hex}{ext.lower()}"

    def save_files(self, entity_type: str, entity_id: int, filenames_and_bytes: List[Tuple[str, bytes]]) -> List[Tuple[str, str]]:
        target_dir = os.path.join(self.base_dir, entity_type, str(entity_id))
        self._ensure_dir(target_dir)

        results: List[Tuple[str, str]] = []
        for original_name, content in filenames_and_bytes:
            safe_name = self._safe_name(original_name or "file")
            disk_path = os.path.join(target_dir, safe_name)
            with open(disk_path, "wb") as f:
                f.write(content)
            key = f"{entity_type}/{entity_id}/{safe_name}"
            url = f"{self.public_base_path}/{key}"
            results.append((key, url))
        return results


class S3Storage(StorageBackend):
    def __init__(self, bucket: str, region: str | None = None, public_base_url: str | None = None):
        try:
            import boto3  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError("boto3 is required for S3Storage. Please install boto3.") from e
        self._boto3 = boto3
        self.bucket = bucket
        self.region = region
        self.public_base_url = public_base_url.rstrip("/") if public_base_url else None
        self.client = boto3.client("s3", region_name=region) if region else boto3.client("s3")

    def _safe_name(self, original: str) -> str:
        _, ext = os.path.splitext(original)
        return f"{uuid4().hex}{ext.lower()}"

    def save_files(self, entity_type: str, entity_id: int, filenames_and_bytes: List[Tuple[str, bytes]]) -> List[Tuple[str, str]]:
        results: List[Tuple[str, str]] = []
        for original_name, content in filenames_and_bytes:
            key_name = self._safe_name(original_name or "file")
            key = f"{entity_type}/{entity_id}/{key_name}"
            self.client.put_object(Bucket=self.bucket, Key=key, Body=content, ContentType=_guess_mime_from_name(original_name))
            if self.public_base_url:
                url = f"{self.public_base_url}/{key}"
            else:
                url = f"s3://{self.bucket}/{key}"
            results.append((key, url))
        return results


def _guess_mime_from_name(filename: str | None) -> str:
    if not filename:
        return "application/octet-stream"
    name = filename.lower()
    if name.endswith(".jpg") or name.endswith(".jpeg"):
        return "image/jpeg"
    if name.endswith(".png"):
        return "image/png"
    if name.endswith(".webp"):
        return "image/webp"
    if name.endswith(".gif"):
        return "image/gif"
    return "application/octet-stream"


def get_storage_from_env() -> StorageBackend:
    backend = os.getenv("STORAGE_BACKEND", "local").strip().lower()
    if backend == "s3":
        bucket = os.getenv("S3_BUCKET")
        if not bucket:
            raise RuntimeError("S3_BUCKET env var is required when STORAGE_BACKEND=s3")
        region = os.getenv("S3_REGION")
        public_base = os.getenv("S3_PUBLIC_BASE_URL")
        return S3Storage(bucket=bucket, region=region, public_base_url=public_base)
    # default local
    base_dir = os.getenv("UPLOADS_DIR", "uploads")
    public_path = os.getenv("UPLOADS_PUBLIC_BASE_PATH", "/uploads")
    return LocalStorage(base_dir=base_dir, public_base_path=public_path)


