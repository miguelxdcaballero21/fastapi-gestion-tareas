from fastapi import FastAPI

from app.enrutadores.usuarios import router as router_usuarios

app = FastAPI(
    title="Gestión de Tareas",
    version="1.0.0"
)

app.include_router(router_usuarios)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API Gestión de Tareas"
    }