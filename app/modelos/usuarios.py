from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    correo: str


class UsuarioCrear(SQLModel):
    nombre: str
    correo: str


class UsuarioRespuesta(SQLModel):
    id: int
    nombre: str
    correo: str