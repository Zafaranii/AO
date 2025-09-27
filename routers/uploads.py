from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os
import json

from database import get_db
from dependencies import get_current_admin_or_super_admin
from models import Admin
from services.storage import get_storage_from_env
from models.apartment_rent import ApartmentRent
from models.apartment_sale import ApartmentSale
from models.apartment_part import ApartmentPart


router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/photos")
async def upload_photos(
    entity_id: int = Form(..., description="ID of the target entity"),
    entity_type: str = Form(..., description="Type: one of 'part', 'rent', 'sale'"),
    files: List[UploadFile] = File(..., description="One or more image files"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin),
):
    entity_type_normalized = entity_type.strip().lower()
    if entity_type_normalized not in {"part", "rent", "sale"}:
        raise HTTPException(status_code=400, detail="entity_type must be one of: part, rent, sale")

    storage = get_storage_from_env()

    payload: List[tuple[str, bytes]] = []
    for file in files:
        if not file.filename:
            continue
        content = await file.read()
        payload.append((file.filename, content))

    try:
        saved = storage.save_files(entity_type_normalized, entity_id, payload)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded files")

    # Persist URLs to the corresponding entity photos_url
    new_urls = [url for _, url in saved]
    model_map = {
        "rent": ApartmentRent,
        "sale": ApartmentSale,
        "part": ApartmentPart,
    }
    Model = model_map[entity_type_normalized]

    instance = db.query(Model).filter(Model.id == entity_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Target entity not found")

    existing_urls: List[str] = []
    if getattr(instance, "photos_url", None):
        try:
            parsed = json.loads(instance.photos_url)
            if isinstance(parsed, list):
                existing_urls = [str(u) for u in parsed]
            elif isinstance(parsed, str):
                existing_urls = [parsed]
        except Exception:
            existing_urls = []

    combined = existing_urls + new_urls
    # Deduplicate while preserving order
    seen = set()
    deduped: List[str] = []
    for u in combined:
        if u not in seen:
            seen.add(u)
            deduped.append(u)

    instance.photos_url = json.dumps(deduped)
    db.add(instance)
    db.commit()
    db.refresh(instance)

    return JSONResponse(
        {
            "entity_id": entity_id,
            "entity_type": entity_type_normalized,
            "count": len(saved),
            "files": [
                {"key": key, "url": url}
                for key, url in saved
            ],
            "folder_key": f"{entity_type_normalized}/{entity_id}/",
            "saved_to_db": True,
        }
    )


