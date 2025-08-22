from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id_detalle_venta = Column(Integer, primary_key=True, index=True)
    id_venta   = Column(Integer, ForeignKey("venta.id_venta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)

    cantidad       = Column(Integer, nullable=False)
    precio_unitario= Column(Numeric(10, 4), nullable=False)
    subtotal       = Column(Numeric(10, 4), nullable=False)

    venta   = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto") 