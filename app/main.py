from fastapi import FastAPI
from app.routes.resources_srv import router as router

app = FastAPI()

# Registrar las rutas
app.include_router(router, prefix="/api/v1", tags=["Server Info"])

@app.get("/")
def root():
    return {"message": "API de monitoreo de servidores"}
