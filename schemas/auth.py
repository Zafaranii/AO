from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class WhatsAppLinkResponse(BaseModel):
    whatsapp_url: str
    admin_phone: str
    message: str
