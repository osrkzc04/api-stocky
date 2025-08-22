from sqlalchemy import Column, DateTime, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(100), nullable=False)
    rol = Column(String(10), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    kardex = relationship("Kardex", back_populates="usuario")