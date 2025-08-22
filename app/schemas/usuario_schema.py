from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: str

class UsuarioCreate(UsuarioBase):
    pass
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: EmailStr | None = None
    contrasena: str | None = None
    rol: str | None = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    creado_en: datetime | None = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"