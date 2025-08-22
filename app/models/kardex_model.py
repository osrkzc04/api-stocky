from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.core.database import Base

TIPO_MOVIMIENTO = Enum("entrada", "salida", name="tipo_mov_kardex_enum")

class Kardex(Base):
    __tablename__ = "kardex"

    id_kardex = Column(Integer, primary_key=True, index=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False, index=True)
    tipo_movimiento = Column(TIPO_MOVIMIENTO, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False, index=True)

    # Relaciones
    id_producto = Column(Integer, ForeignKey("producto.id_producto"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    producto = relationship("Producto", back_populates="kardex", lazy="joined")
    usuario = relationship("Usuario", back_populates="kardex", lazy="joined")

    def __repr__(self) -> str:
        return (f"<Kardex id={self.id_kardex} prod={self.id_producto} "
                f"tipo={self.tipo_movimiento} cant={self.cantidad} fecha={self.fecha}>")