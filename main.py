from typing import Union
from fastapi import FastAPI
from app.routes import auth_route, cliente_route, marca_route, usuario_route

app = FastAPI(
    title="Sistema de Gestión de Bodega",
    version="1.0.0",
    docs_url="/docs",  # opcional, puedes cambiarlo a otra ruta
    redoc_url="/redoc",  # también puedes personalizar o quitarlo
)

app.include_router(usuario_route.router)
app.include_router(auth_route.router)
app.include_router(marca_route.router)
app.include_router(cliente_route.router)

@app.get("/")
def read_root():
    return {"message": "API Bodega con FastAPI"}