from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modelos.tareas import Tarea


class Actividad(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str
    descripcion: str
    estado: str

    fecha: date
    completada: bool

    tarea_id: int = Field(foreign_key="tarea.id")

    tarea: "Tarea" = Relationship(back_populates="actividades")


class ActividadCrear(SQLModel):
    nombre: str
    descripcion: str
    estado: str

    fecha: date
    completada: bool


class ActividadActualizar(SQLModel):
    completada: bool


class ActividadRespuesta(SQLModel):
    id: int

    nombre: str
    descripcion: str
    estado: str

    fecha: date
    completada: bool

    tarea_id: int