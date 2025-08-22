from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Base ---
class KardexBase(BaseModel):
    id_producto: int
    tipo_movimiento: str = Field(..., pattern="^(entrada|salida)$")
    cantidad: int
    id_usuario: int


# --- Crear ---
class KardexCreate(KardexBase):
    pass


# --- Actualizar ---
class KardexUpdate(BaseModel):
    id_producto: Optional[int] = None
    tipo_movimiento: Optional[str] = Field(None, pattern="^(entrada|salida)$")
    cantidad: Optional[int] = None
    id_usuario: Optional[int] = None


# --- Respuesta ---
class KardexResponse(KardexBase):
    id_kardex: int
    fecha: datetime

    class Config:
        from_attributes = True


# --- Mini Schemas para anidar ---
class ProductoMini(BaseModel):
    id_producto: int
    codigo: str
    nombre: str

    class Config:
        from_attributes = True


class UsuarioMini(BaseModel):
    id_usuario: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True


# --- Respuesta con relaciones ---
class KardexDetalleResponse(KardexResponse):
    producto: ProductoMini
    usuario: UsuarioMini