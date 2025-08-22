from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class ProveedorBase(BaseModel):
    dni: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    telefono: str = Field(..., max_length=20)
    direccion: str
    correo_electronico: EmailStr

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    dni: str | None = None
    nombre: str | None = None
    telefono: str | None = None
    direccion: str | None = None
    correo_electronico: EmailStr | None = None

class ProveedorResponse(ProveedorBase):
    id_proveedor: int
    creado_en: datetime | None = None

    class Config:
        from_attributes = True
