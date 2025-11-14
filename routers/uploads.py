from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import json

from database import get_db
from dependencies import get_current_admin_or_super_admin
from models import Admin
from services.storage import get_storage_from_env
from models.apartment_rent import ApartmentRent
from models.apartment_sale import ApartmentSale
from models.apartment_part import ApartmentPart
from models.rental_contract import RentalContract


router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/photos")
async def upload_photos(
    entity_id: int = Form(..., description="ID of the target entity (apartment, part, or contract ID)"),
    entity_type: str = Form(..., description="Type: one of 'part', 'rent', 'sale', 'rental_contract'"),
    document_type: Optional[str] = Form(None, description="For rental_contract: 'contract' or 'customer_id'. Optional for other types."),
    files: List[UploadFile] = File(..., description="One or more image/document files"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin_or_super_admin),
):
    entity_type_normalized = entity_type.strip().lower()
    allowed_types = {"part", "rent", "sale", "rental_contract"}
    if entity_type_normalized not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"entity_type must be one of: {', '.join(sorted(allowed_types))}"
        )

    # Validate document_type for rental_contract
    if entity_type_normalized == "rental_contract":
        if not document_type:
            raise HTTPException(
                status_code=400,
                detail="document_type is required for rental_contract. Must be 'contract' or 'customer_id'"
            )
        document_type_normalized = document_type.strip().lower()
        if document_type_normalized not in {"contract", "customer_id"}:
            raise HTTPException(
                status_code=400,
                detail="document_type must be 'contract' or 'customer_id' for rental_contract"
            )
    else:
        document_type_normalized = None

    storage = get_storage_from_env()

    # Read all files
    payload: List[tuple[str, bytes]] = []
    for file in files:
        if not file.filename:
            continue
        content = await file.read()
        payload.append((file.filename, content))

    if not payload:
        raise HTTPException(status_code=400, detail="No valid files provided")

    # Save files to storage
    try:
        saved = storage.save_files(entity_type_normalized, entity_id, payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded files: {str(e)}")

    if not saved:
        raise HTTPException(status_code=500, detail="No files were saved")

    new_urls = [url for _, url in saved]

    # Handle different entity types
    if entity_type_normalized == "rental_contract":
        # For rental contracts, update contract_url or customer_id_url with first file's URL
        instance = db.query(RentalContract).filter(RentalContract.id == entity_id).first()
        if not instance:
            raise HTTPException(status_code=404, detail="Rental contract not found")
        
        # Use first file's URL for the single URL field
        first_url = new_urls[0]
        if document_type_normalized == "contract":
            instance.contract_url = first_url
        elif document_type_normalized == "customer_id":
            instance.customer_id_url = first_url
        
        db.add(instance)
        db.commit()
        db.refresh(instance)

        return JSONResponse(
            {
                "entity_id": entity_id,
                "entity_type": entity_type_normalized,
                "document_type": document_type_normalized,
                "count": len(saved),
                "files": [
                    {"key": key, "url": url}
                    for key, url in saved
                ],
                "folder_key": f"{entity_type_normalized}/{entity_id}/",
                "saved_to_db": True,
                "url_field_updated": document_type_normalized,
                "url_saved": first_url,
            }
        )
    else:
        # For apartments and parts, update photos_url (JSON array)
        model_map = {
            "rent": ApartmentRent,
            "sale": ApartmentSale,
            "part": ApartmentPart,
        }
        Model = model_map[entity_type_normalized]

        instance = db.query(Model).filter(Model.id == entity_id).first()
        if not instance:
            raise HTTPException(status_code=404, detail="Target entity not found")

        # Get existing URLs
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

        # Combine and deduplicate
        combined = existing_urls + new_urls
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


