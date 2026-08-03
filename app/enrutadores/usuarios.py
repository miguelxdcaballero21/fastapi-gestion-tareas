from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.conexion_db import SesionDependencia
from app.modelos.usuarios import (
    Usuario,
    UsuarioCrear,
    UsuarioActualizar,
    UsuarioRespuesta
)
from app.modelos.tareas import Tarea

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioRespuesta)
def crear_usuario(
    usuario: UsuarioCrear,
    sesion: SesionDependencia
):

    usuario_existente = sesion.exec(
        select(Usuario).where(
            Usuario.correo == usuario.correo
        )
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo
    )

    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)

    return nuevo_usuario


@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios(
    sesion: SesionDependencia
):

    usuarios = sesion.exec(
        select(Usuario)
    ).all()

    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def listar_usuario(
    usuario_id: int,
    sesion: SesionDependencia
):

    usuario = sesion.get(
        Usuario,
        usuario_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioActualizar,
    sesion: SesionDependencia
):

    usuario = sesion.get(
        Usuario,
        usuario_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario_existente = sesion.exec(
        select(Usuario).where(
            Usuario.correo == datos.correo,
            Usuario.id != usuario_id
        )
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    usuario.nombre = datos.nombre
    usuario.correo = datos.correo

    sesion.add(usuario)
    sesion.commit()
    sesion.refresh(usuario)

    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    sesion: SesionDependencia
):

    usuario = sesion.get(
        Usuario,
        usuario_id
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    tarea = sesion.exec(
        select(Tarea).where(
            Tarea.usuario_id == usuario_id
        )
    ).first()

    if tarea:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el usuario porque tiene tareas asociadas"
        )

    sesion.delete(usuario)
    sesion.commit()

    return {
        "mensaje": "Usuario eliminado correctamente"
    }