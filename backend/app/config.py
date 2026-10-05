from pathlib import Path
import os

# Root do projeto: "Projeto Final"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# Carregar variáveis de ambiente do .env
try:
    from dotenv import load_dotenv
    if ENV_FILE.exists():
        load_dotenv(dotenv_path=ENV_FILE)
except ImportError:
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v

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
