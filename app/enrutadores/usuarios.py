from fastapi import APIRouter, HTTPException

from app.listas import usuarios
from app.modelos.usuarios import (
    Usuario,
    UsuarioActualizar,
    UsuarioRespuesta
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioRespuesta)
def crear_usuario(usuario: Usuario):

    for u in usuarios:
        if u["correo"] == usuario.correo:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }

    usuarios.append(nuevo_usuario)

    return nuevo_usuario


@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios():
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(usuario_id: int):

    usuario = next(
        (u for u in usuarios if u["id"] == usuario_id),
        None
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioActualizar
):

    usuario = next(
        (u for u in usuarios if u["id"] == usuario_id),
        None
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    for u in usuarios:
        if (
            u["correo"] == datos.correo
            and u["id"] != usuario_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya está registrado"
            )

    usuario["nombre"] = datos.nombre
    usuario["correo"] = datos.correo

    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):

    usuario = next(
        (u for u in usuarios if u["id"] == usuario_id),
        None
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    usuarios.remove(usuario)

    return {
        "mensaje": "Usuario eliminado correctamente"
    }