from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Compra(Base):
    __tablename__ = "compra"

    id_compra = Column(Integer, primary_key=True, index=True)
    numero_compra = Column(Integer, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    subtotal = Column(Numeric(10, 4), nullable=False)
    iva_15   = Column(Numeric(10, 4), nullable=False)
    iva_0    = Column(Numeric(10, 4), nullable=False)
    total    = Column(Numeric(10, 4), nullable=False)

    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor"), nullable=False)
    id_usuario   = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    proveedor = relationship("Proveedor", back_populates="compras", lazy="joined")
    usuario   = relationship("Usuario", lazy="joined")
    detalles  = relationship("DetalleCompra", back_populates="compra", lazy="selectin")