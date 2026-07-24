from datetime import date
from pydantic import BaseModel


class Tarea(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    avance: int
    fecha_inicio: date
    fecha_final: date
    usuario_id: int


class TareaRespuesta(Tarea):
    id: int