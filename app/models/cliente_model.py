from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    dni = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), unique=True, nullable=False)
    direccion = Column(Text, nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())