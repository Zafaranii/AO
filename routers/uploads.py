from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os

from database import get_db
from dependencies import get_current_admin_or_super_admin
from models import Admin, AdminRoleEnum
from models.apartment_rent import ApartmentRent
from models.apartment_sale import ApartmentSale
from models.apartment_part import ApartmentPart
from models.rental_contract import RentalContract
from services.media import parse_urls
from services.storage import get_storage_from_env, delete_urls_quietly

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf"}
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
ENTITY_TYPES = {"part", "rent", "sale", "rental_contract"}
DOCUMENT_FIELDS = {"contract": "contract_url", "customer_id": "customer_id_url"}
MODEL_MAP = {"rent": ApartmentRent, "sale": ApartmentSale, "part": ApartmentPart, "rental_contract": RentalContract}


def _normalize_entity_type(entity_type: str) -> str:
    normalized = entity_type.strip().lower()
    if normalized not in ENTITY_TYPES:
        raise HTTPException(status_code=400, detail=f"entity_type must be one of: {', '.join(sorted(ENTITY_TYPES))}")
    return normalized


def _normalize_document_type(entity_type: str, document_type: Optional[str]) -> Optional[str]:
    if entity_type != "rental_contract":
        return None
    normalized = (document_type or "").strip().lower()
    if normalized not in DOCUMENT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail="document_type is required for rental_contract and must be 'contract' or 'customer_id'",
        )
    return normalized


def _load_entity(db: Session, entity_type: str, entity_id: int, admin: Admin):
    """Fetch the target row and make sure this admin may modify it (owner or super admin)."""
    instance = db.query(MODEL_MAP[entity_type]).filter(MODEL_MAP[entity_type].id == entity_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Target entity not found")
    if admin.role == AdminRoleEnum.super_admin:
        return instance

    if entity_type in ("rent", "sale"):
        owner_id = instance.listed_by_admin_id
    else:  # part, rental_contract
        owner_id = instance.created_by_admin_id
    if owner_id != admin.id:
        raise HTTPException(status_code=403, detail="You can only modify files of items you created")
    return instance


@router.post("/photos")
async def upload_photos(
    entity_id: int = Form(..., description="ID of the target entity (apartment, part, or contract ID)"),
    entity_type: str = Form(..., description="Type: one of 'part', 'rent', 'sale', 'rental_contract'"),
    document_type: Optional[str] = Form(None, description="For rental_contract: 'contract' or 'customer_id'."),
    files: List[UploadFile] = File(..., description="One or more image/document files"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin),
):
    entity_type = _normalize_entity_type(entity_type)
    document_type = _normalize_document_type(entity_type, document_type)
    instance = _load_entity(db, entity_type, entity_id, current_admin)

    payload: List[tuple[str, bytes]] = []
    for file in files:
        if not file.filename:
            continue
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            )
        content = await file.read()
        if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"{file.filename} exceeds {MAX_UPLOAD_MB}MB limit")
        payload.append((file.filename, content))

    if not payload:
        raise HTTPException(status_code=400, detail="No valid files provided")

    storage = get_storage_from_env()
    try:
        saved = storage.save_files(entity_type, entity_id, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded files: {str(e)}")
    if not saved:
        raise HTTPException(status_code=500, detail="No files were saved")

    new_urls = [url for _, url in saved]
    response = {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "count": len(saved),
        "files": [{"key": key, "url": url} for key, url in saved],
        "folder_key": f"{entity_type}/{entity_id}/",
        "saved_to_db": True,
    }

    try:
        if entity_type == "rental_contract":
            # single-URL field: the first file wins and the file it replaces is removed from storage
            field = DOCUMENT_FIELDS[document_type]
            previous = getattr(instance, field)
            setattr(instance, field, new_urls[0])
            db.commit()
            if previous and previous != new_urls[0]:
                delete_urls_quietly([previous])
            response.update({"document_type": document_type, "url_field_updated": document_type, "url_saved": new_urls[0]})
        else:
            combined = parse_urls(instance.photos_url) + new_urls
            instance.photos_url = json.dumps(list(dict.fromkeys(combined)))
            db.commit()
    except Exception:
        db.rollback()
        delete_urls_quietly(new_urls)  # don't leave orphan files behind a failed DB write
        raise HTTPException(status_code=500, detail="Failed to save file references")

    return response


@router.delete("/photos")
async def delete_photo(
    entity_type: str = Query(..., description="'part', 'rent', 'sale' or 'rental_contract'"),
    entity_id: int = Query(...),
    url: Optional[str] = Query(None, description="URL of the photo to remove (not used for rental_contract)"),
    document_type: Optional[str] = Query(None, description="For rental_contract: 'contract' or 'customer_id'"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin),
):
    """Remove one photo (or one contract document) from the entity and delete the file from storage."""
    entity_type = _normalize_entity_type(entity_type)
    document_type = _normalize_document_type(entity_type, document_type)
    instance = _load_entity(db, entity_type, entity_id, current_admin)

    if entity_type == "rental_contract":
        field = DOCUMENT_FIELDS[document_type]
        removed = getattr(instance, field)
        if not removed:
            raise HTTPException(status_code=404, detail="No document stored for this field")
        setattr(instance, field, None)
    else:
        if not url:
            raise HTTPException(status_code=400, detail="url is required")
        current = parse_urls(instance.photos_url)
        if url not in current:
            raise HTTPException(status_code=404, detail="Photo not found on this item")
        removed = url
        instance.photos_url = json.dumps([u for u in current if u != url])

    db.commit()
    delete_urls_quietly([removed])
    return {"entity_id": entity_id, "entity_type": entity_type, "deleted": removed}


@router.get("/signed-url")
async def get_signed_url(
    url: str = Query(..., description="A file URL previously returned by the API"),
    expires_in: int = Query(900, ge=60, le=86400),
    current_admin: Admin = Depends(get_current_admin_or_super_admin),
):
    """Time-limited link for reading a private file (contract / customer ID scans)."""
    return {"url": get_storage_from_env().signed_url(url, expires_in), "expires_in": expires_in}
