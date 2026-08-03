from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from app.modelos.usuarios import UsuarioRespuesta
from app.modelos.actividades import ActividadRespuesta

if TYPE_CHECKING:
    from app.modelos.usuarios import Usuario
    from app.modelos.actividades import Actividad


class Tarea(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str
    descripcion: str
    estado: str
    avance: int

    fecha_inicio: date
    fecha_final: date

    usuario_id: int = Field(foreign_key="usuario.id")

    usuario: "Usuario" = Relationship(back_populates="tareas")
    actividades: list["Actividad"] = Relationship(back_populates="tarea")


class TareaCrear(SQLModel):
    nombre: str
    descripcion: str
    estado: str
    avance: int

    fecha_inicio: date
    fecha_final: date

    usuario_id: int


class TareaActualizar(SQLModel):
    nombre: str
    descripcion: str
    estado: str
    avance: int

    fecha_inicio: date
    fecha_final: date


class TareaRespuesta(SQLModel):
    id: int

    nombre: str
    descripcion: str
    estado: str
    avance: int

    fecha_inicio: date
    fecha_final: date

    usuario_id: int


class TareaLista(SQLModel):
    id: int

    nombre: str
    descripcion: str
    estado: str
    avance: int

    fecha_inicio: date
    fecha_final: date

    usuario: UsuarioRespuesta
    actividades: list[ActividadRespuesta]