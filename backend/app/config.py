from pathlib import Path
import os

# Root do projeto: "Projeto Final"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
UPLOADS_DIR = DATA_DIR / "uploads"
DB_DIR = DATA_DIR / "db"
ARTEFATOS_DIR = PROJECT_ROOT / "Projeto_Final_Artefatos"
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

DB_PATH = str(DB_DIR / "insurminds.db")

# Garantir criação dos diretórios essenciais
for d in [DATA_DIR, SAMPLES_DIR, UPLOADS_DIR, DB_DIR, ARTEFATOS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
