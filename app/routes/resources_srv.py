from fastapi import APIRouter, Depends
from app.controllers.resources_srv import get_server_info

router = APIRouter()

@router.get("/")
def server_info(host: str, username: str, password: str):
    """
    Ruta para obtener información del servidor.
    """
    return get_server_info(host, username, password)
