from app.api import auth
from app.core.database import Base, engine
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)
app = FastAPI(title="E-commerce Backend Api", version="1.0.0")

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {
        "message": "Koneksi Berhasil! Backend E-commerce terhubung ke Superbase.",
    }