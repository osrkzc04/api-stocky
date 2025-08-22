from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Venta(Base):
    __tablename__ = "venta"

    id_venta = Column(Integer, primary_key=True, index=True)
    numero_venta = Column(Integer, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    subtotal = Column(Numeric(10, 4), nullable=False)
    iva_15   = Column(Numeric(10, 4), nullable=False)
    iva_0    = Column(Numeric(10, 4), nullable=False)
    total    = Column(Numeric(10, 4), nullable=False)

    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_usuario   = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    cliente = relationship("Cliente", back_populates="ventas", lazy="joined")
    usuario   = relationship("Usuario", lazy="joined")
    detalles  = relationship("DetalleVenta", back_populates="venta", lazy="selectin")