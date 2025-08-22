from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Marca(Base):
    __tablename__ = "marca"

    id_marca = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)