from fastapi import APIRouter
from app.controllers.resources_srv import get_server_info

router = APIRouter()

@router.get("/ubuntu")
def server_info(host: str, username: str, password: str):
    """
    Ruta para obtener información del servidor.
    """
    return get_server_info(host, username, password)
