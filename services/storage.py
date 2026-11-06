import logging
import mimetypes
import os
import shutil
from functools import lru_cache
from typing import Iterable, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)

# Entity types whose files must never be publicly readable (ID scans, signed contracts).
# They are served through short-lived signed URLs (see GET /uploads/signed-url).
PRIVATE_ENTITY_TYPES = {"rental_contract"}


def _safe_name(original: str) -> str:
    _, ext = os.path.splitext(original or "")
    return f"{uuid4().hex}{ext.lower()}"


class StorageBackend:
    def save_files(self, entity_type: str, entity_id: int, filenames_and_bytes: List[Tuple[str, bytes]]) -> List[Tuple[str, str]]:
        """Save files. Returns a list of (key, url) per saved file."""
        raise NotImplementedError

    def key_from_url(self, url: str) -> Optional[str]:
        """Return the storage key for a URL this backend produced, or None for foreign URLs."""
        raise NotImplementedError

    def delete_keys(self, keys: Iterable[str]) -> None:
        raise NotImplementedError

    def delete_prefix(self, prefix: str) -> None:
        """Delete every object whose key starts with prefix (e.g. 'part/12/')."""
        raise NotImplementedError

    def signed_url(self, url: str, expires_in: int = 900) -> str:
        """Time-limited URL for reading a private file. Backends without signing return the URL."""
        return url

    def check(self) -> None:
        """Raise if the backend is unusable. Called once at startup."""

    # ---- helpers shared by all backends ----
    def delete_urls(self, urls: Iterable[str]) -> None:
        keys = [k for k in (self.key_from_url(u) for u in urls if u) if k]
        if keys:
            self.delete_keys(keys)

    def delete_entity_files(self, entity_type: str, entity_id: int, urls: Iterable[str] = ()) -> None:
        """Best-effort removal of everything stored for one entity. Never raises."""
        try:
            self.delete_urls(urls)
        except Exception:
            logger.exception("Failed deleting files by URL for %s/%s", entity_type, entity_id)
        try:
            self.delete_prefix(f"{entity_type}/{entity_id}/")
        except Exception:
            logger.exception("Failed deleting file prefix for %s/%s", entity_type, entity_id)


class LocalStorage(StorageBackend):
    def __init__(self, base_dir: str = "uploads", public_base_path: str = "/uploads"):
        self.base_dir = os.path.abspath(base_dir)
        self.public_base_path = public_base_path.rstrip("/")

    def _path(self, key: str) -> Optional[str]:
        path = os.path.abspath(os.path.join(self.base_dir, key))
        # never let a crafted key escape the uploads directory
        if not path.startswith(self.base_dir + os.sep):
            return None
        return path

    def save_files(self, entity_type, entity_id, filenames_and_bytes):
        target_dir = os.path.join(self.base_dir, entity_type, str(entity_id))
        os.makedirs(target_dir, exist_ok=True)
        results = []
        for original_name, content in filenames_and_bytes:
            name = _safe_name(original_name)
            with open(os.path.join(target_dir, name), "wb") as f:
                f.write(content)
            key = f"{entity_type}/{entity_id}/{name}"
            results.append((key, f"{self.public_base_path}/{key}"))
        return results

    def key_from_url(self, url):
        prefix = self.public_base_path + "/"
        if url and url.startswith(prefix):
            return url[len(prefix):]
        return None

    def delete_keys(self, keys):
        for key in keys:
            path = self._path(key)
            if path and os.path.isfile(path):
                os.remove(path)

    def delete_prefix(self, prefix):
        path = self._path(prefix.rstrip("/"))
        if path and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)


class S3Storage(StorageBackend):
    """Any S3-compatible bucket: AWS S3, DigitalOcean Spaces, Cloudflare R2, Wasabi, Backblaze B2, MinIO, ..."""

    def __init__(
        self,
        bucket: str,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        public_base_url: Optional[str] = None,
        key_prefix: str = "",
        addressing_style: Optional[str] = None,
    ):
        try:
            import boto3
            from botocore.config import Config
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("boto3 is required when STORAGE_BACKEND=s3") from e

        self.bucket = bucket
        self.key_prefix = key_prefix.strip("/")
        endpoint_url = (endpoint_url or "").rstrip("/") or None
        style = addressing_style or ("path" if endpoint_url else "auto")

        self.client = boto3.client(
            "s3",
            region_name=region or "us-east-1",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id or None,
            aws_secret_access_key=secret_access_key or None,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": style},
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )

        if public_base_url:
            self.public_base_url = public_base_url.rstrip("/")
        elif endpoint_url:
            self.public_base_url = f"{endpoint_url}/{bucket}"
        elif region:
            self.public_base_url = f"https://{bucket}.s3.{region}.amazonaws.com"
        else:
            self.public_base_url = f"https://{bucket}.s3.amazonaws.com"

    def _full_key(self, key: str) -> str:
        return f"{self.key_prefix}/{key}" if self.key_prefix else key

    def check(self) -> None:
        self.client.head_bucket(Bucket=self.bucket)

    def save_files(self, entity_type, entity_id, filenames_and_bytes):
        results = []
        for original_name, content in filenames_and_bytes:
            key = f"{entity_type}/{entity_id}/{_safe_name(original_name)}"
            content_type = mimetypes.guess_type(original_name or "")[0] or "application/octet-stream"
            extra = {}
            if entity_type not in PRIVATE_ENTITY_TYPES:
                extra["CacheControl"] = "public, max-age=31536000, immutable"
            # No ACL is set on purpose: many providers reject ACLs. Public read is controlled by the bucket policy.
            self.client.put_object(
                Bucket=self.bucket,
                Key=self._full_key(key),
                Body=content,
                ContentType=content_type,
                **extra,
            )
            results.append((key, f"{self.public_base_url}/{self._full_key(key)}"))
        return results

    def key_from_url(self, url):
        if not url:
            return None
        bases = [self.public_base_url + "/", f"s3://{self.bucket}/"]
        for base in bases:
            if url.startswith(base):
                full = url[len(base):]
                if self.key_prefix:
                    if not full.startswith(self.key_prefix + "/"):
                        return None
                    return full[len(self.key_prefix) + 1:]
                return full
        return None

    def delete_keys(self, keys):
        keys = [self._full_key(k) for k in keys]
        for i in range(0, len(keys), 1000):  # S3 limit per request
            batch = keys[i:i + 1000]
            resp = self.client.delete_objects(
                Bucket=self.bucket,
                Delete={"Objects": [{"Key": k} for k in batch], "Quiet": True},
            )
            for err in resp.get("Errors", []):
                logger.error("Failed to delete %s: %s", err.get("Key"), err.get("Message"))

    def delete_prefix(self, prefix):
        full_prefix = self._full_key(prefix)
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=full_prefix):
            keys = [obj["Key"] for obj in page.get("Contents", [])]
            if keys:
                self.client.delete_objects(
                    Bucket=self.bucket,
                    Delete={"Objects": [{"Key": k} for k in keys], "Quiet": True},
                )

    def signed_url(self, url, expires_in=900):
        key = self.key_from_url(url)
        if not key:
            return url
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": self._full_key(key)},
            ExpiresIn=expires_in,
        )


@lru_cache(maxsize=1)
def get_storage_from_env() -> StorageBackend:
    backend = os.getenv("STORAGE_BACKEND", "local").strip().lower()
    if backend == "s3":
        bucket = os.getenv("S3_BUCKET")
        if not bucket:
            raise RuntimeError("S3_BUCKET env var is required when STORAGE_BACKEND=s3")
        return S3Storage(
            bucket=bucket,
            region=os.getenv("S3_REGION"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
            secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
            public_base_url=os.getenv("S3_PUBLIC_BASE_URL"),
            key_prefix=os.getenv("S3_KEY_PREFIX", ""),
            addressing_style=os.getenv("S3_ADDRESSING_STYLE"),
        )
    return LocalStorage(
        base_dir=os.getenv("UPLOADS_DIR", "uploads"),
        public_base_path=os.getenv("UPLOADS_PUBLIC_BASE_PATH", "/uploads"),
    )


def delete_urls_quietly(urls: Iterable[str]) -> None:
    """Delete files after the DB no longer references them. A storage outage must not fail the request."""
    try:
        get_storage_from_env().delete_urls(urls)
    except Exception:
        logger.exception("Failed to delete files from storage")
