from pydantic import BaseModel, Field

class MarcaBase(BaseModel):
    nombre: str = Field(..., max_length=100)

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100)

class MarcaResponse(MarcaBase):
    id_marca: int

    class Config:
        from_attributes = True