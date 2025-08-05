from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class ClienteBase(BaseModel):
    dni: str = Field(..., example="0102030405")
    nombre: str = Field(..., example="Juan Pérez")
    telefono: str = Field(..., example="0987654321")
    direccion: str = Field(..., example="Av. Siempre Viva 123")
    correo_electronico: EmailStr = Field(..., example="juan.perez@example.com")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    correo_electronico: EmailStr | None = None


class ClienteResponse(ClienteBase):
    id_cliente: int
    creado_en: datetime

    class Config:
        from_attributes = True  # Pydantic v2