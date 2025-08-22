from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey, func, Computed
from sqlalchemy.orm import relationship
from app.core.database import Base

class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    iva = Column(Boolean, nullable=False, default=True)
    precio_total = Column(Numeric(10, 4), nullable=False) 
    precio_unitario = Column(
        Numeric(10, 4),
        Computed("CASE WHEN iva THEN precio_total / 1.15 ELSE precio_total END", persisted=True),
        nullable=False
    )
    cantidad_en_stock = Column(Integer, nullable=False, default=0)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    id_marca = Column(Integer, ForeignKey("marca.id_marca"), nullable=False)
    marca = relationship("Marca", lazy="joined")

    kardex = relationship("Kardex", back_populates="producto",cascade="all, delete-orphan")
    