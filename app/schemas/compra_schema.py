from pydantic import BaseModel, condecimal, Field
from datetime import datetime
from typing import List, Optional

Decimal10_4 = condecimal(max_digits=10, decimal_places=4)

# -------- Detalles --------
class ProductoMini(BaseModel):
    id_producto: int
    codigo: str
    nombre: str
    class Config: from_attributes = True

class DetalleCompraOut(BaseModel):
    id_detalle_compra: int
    cantidad: int
    precio_unitario: Decimal10_4
    subtotal: Decimal10_4
    producto: ProductoMini | None = None
    class Config: from_attributes = True

class DetalleCompraCreate(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal10_4
    subtotal: Optional[Decimal10_4] = None 

# -------- Cabecera --------
class CompraBase(BaseModel):
    subtotal: Decimal10_4
    iva_15:  Decimal10_4
    iva_0:   Decimal10_4
    total:   Decimal10_4
    id_proveedor: int
    id_usuario: int

class CompraCreate(BaseModel):
    id_proveedor: int
    id_usuario: int
    detalles: List[DetalleCompraCreate]  
    subtotal: Optional[Decimal10_4] = None
    iva_15:   Optional[Decimal10_4] = None
    iva_0:    Optional[Decimal10_4] = None
    total:    Optional[Decimal10_4] = None

class CompraUpdate(BaseModel):
    subtotal: Optional[Decimal10_4] = None
    iva_15:   Optional[Decimal10_4] = None
    iva_0:    Optional[Decimal10_4] = None
    total:    Optional[Decimal10_4] = None
    id_proveedor: Optional[int] = None
    id_usuario: Optional[int] = None

class CompraResponse(CompraBase):
    id_compra: int
    numero_compra: int
    fecha: datetime
    class Config: from_attributes = True

class ProveedorMini(BaseModel):
    id_proveedor: int
    nombre: str
    dni: str
    telefono: str
    correo_electronico: str
    class Config: from_attributes = True

class UsuarioMini(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
    class Config: from_attributes = True

class CompraDetalleResponse(CompraResponse):
    proveedor: ProveedorMini
    usuario: UsuarioMini
    detalles: List[DetalleCompraOut]