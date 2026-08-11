from pydantic import BaseModel, EmailStr


class Usuario(BaseModel):
    nombre: str
    correo: EmailStr


class UsuarioActualizar(BaseModel):
    nombre: str
    correo: EmailStr


class UsuarioRespuesta(Usuario):
    id: int