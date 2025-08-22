from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class DetalleCompra(Base):
    __tablename__ = "detalle_compra"

    id_detalle_compra = Column(Integer, primary_key=True, index=True)
    id_compra   = Column(Integer, ForeignKey("compra.id_compra"), nullable=False)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)

    cantidad       = Column(Integer, nullable=False)
    precio_unitario= Column(Numeric(10, 4), nullable=False)
    subtotal       = Column(Numeric(10, 4), nullable=False)

    compra   = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto") 
