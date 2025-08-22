from pydantic import BaseModel, Field, condecimal
from typing import Optional

Decimal10_4 = condecimal(max_digits=10, decimal_places=4)

class MarcaMini(BaseModel):
    id_marca: int
    nombre: str
    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    codigo: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=100)
    descripcion: str
    iva: bool = True
    precio_total: Decimal10_4
    cantidad_en_stock: int = Field(0, ge=0)
    id_marca: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    iva: Optional[bool] = None
    precio_total: Optional[Decimal10_4] = None
    cantidad_en_stock: Optional[int] = Field(None, ge=0)
    id_marca: Optional[int] = None

class ProductoResponse(BaseModel):
    id_producto: int
    codigo: str
    nombre: str
    descripcion: str
    iva: bool
    precio_total: Decimal10_4
    precio_unitario: Decimal10_4
    cantidad_en_stock: int
    id_marca: int
    marca: MarcaMini | None = None

    class Config:
        from_attributes = True
