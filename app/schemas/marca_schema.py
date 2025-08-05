from pydantic import BaseModel

class MarcaCreate(BaseModel):
    nombre: str

class MarcaResponse(BaseModel):
    id_marca: int
    nombre: str

    model_config = {
        "from_attributes": True
    }