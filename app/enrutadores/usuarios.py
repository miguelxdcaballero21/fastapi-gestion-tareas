from fastapi import APIRouter, HTTPException

from app.listas import usuarios
from app.modelos.usuarios import Usuario, UsuarioRespuesta

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioRespuesta)
def crear_usuario(usuario: Usuario):

    # Validar que el correo no exista
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