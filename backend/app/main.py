import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.routes.policies import router as policies_router, seed_sample_policies
from backend.app.routes.comparison import router as comparison_router
from backend.app.routes.chat import router as chat_router
from backend.app.services.storage_service import StorageService
from backend.app.config import UPLOADS_DIR, ARTEFATOS_DIR, FRONTEND_DIST

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage = StorageService()
    policies = storage.list_policies()
    if len(policies) == 0:
        seed_sample_policies()
    yield

app = FastAPI(
    title="InsurMinds Apólice 360",
    description="Plataforma Inteligente para Análise, Extração e Comparação de Apólices D&O com IA Generativa",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(policies_router)
app.include_router(comparison_router)
app.include_router(chat_router)

# Estáticos
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")
app.mount("/artefatos", StaticFiles(directory=str(ARTEFATOS_DIR)), name="artefatos")

if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")

@app.get("/health")
def health_check():
    storage = StorageService()
    policies_count = len(storage.list_policies())
    comparisons_count = len(storage.list_comparisons())
    return {
        "status": "online",
        "system": "InsurMinds Apólice 360",
        "policies_stored": policies_count,
        "comparisons_stored": comparisons_count,
        "version": "1.0.0"
    }
