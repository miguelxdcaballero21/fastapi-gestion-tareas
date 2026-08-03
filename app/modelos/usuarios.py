from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modelos.tareas import Tarea


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nombre: str
    correo: str

    tareas: list["Tarea"] = Relationship(back_populates="usuario")


class UsuarioCrear(SQLModel):
    nombre: str
    correo: str


class UsuarioActualizar(SQLModel):
    nombre: str
    correo: str


class UsuarioRespuesta(SQLModel):
    id: int
    nombre: str
    correo: str