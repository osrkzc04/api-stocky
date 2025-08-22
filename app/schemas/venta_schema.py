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

class DetalleVentaOut(BaseModel):
    id_detalle_venta: int
    cantidad: int
    precio_unitario: Decimal10_4
    subtotal: Decimal10_4
    producto: ProductoMini | None = None
    class Config: from_attributes = True

class DetalleVentaCreate(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: Decimal10_4
    subtotal: Optional[Decimal10_4] = None 

# -------- Cabecera --------
class VentaBase(BaseModel):
    subtotal: Decimal10_4
    iva_15:  Decimal10_4
    iva_0:   Decimal10_4
    total:   Decimal10_4
    id_cliente: int
    id_usuario: int

class VentaCreate(BaseModel):
    id_cliente: int
    id_usuario: int
    detalles: List[DetalleVentaCreate]  
    subtotal: Optional[Decimal10_4] = None
    iva_15:   Optional[Decimal10_4] = None
    iva_0:    Optional[Decimal10_4] = None
    total:    Optional[Decimal10_4] = None

class VentaUpdate(BaseModel):
    subtotal: Optional[Decimal10_4] = None
    iva_15:   Optional[Decimal10_4] = None
    iva_0:    Optional[Decimal10_4] = None
    total:    Optional[Decimal10_4] = None
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None

class VentaResponse(VentaBase):
    id_venta: int
    numero_venta: int
    fecha: datetime
    class Config: from_attributes = True

class ClienteMini(BaseModel):
    id_cliente: int
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

class VentaDetalleResponse(VentaResponse):
    cliente: ClienteMini
    usuario: UsuarioMini
    detalles: List[DetalleVentaOut]