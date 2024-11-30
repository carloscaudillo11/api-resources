from fastapi import FastAPI
from app.routes.resources_srv import router as router

app = FastAPI()

# Registrar las rutas
app.include_router(router)

@app.get("/")
def root():
    return {"message": "API de monitoreo de servidores"}
