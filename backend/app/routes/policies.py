import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any

from backend.app.models.policy_schema import DnoPolicyData
from backend.app.services.ocr_service import OCRService
from backend.app.services.llm_service import LLMService
from backend.app.services.storage_service import StorageService
from backend.app.agents.ingestion_agent import IngestionAgent
from backend.app.agents.extraction_agent import ExtractionAgent
from backend.app.agents.validation_agent import ValidationAgent
from backend.app.config import UPLOADS_DIR, SAMPLES_DIR

router = APIRouter(prefix="/api/policies", tags=["Policies"])

storage_service = StorageService()
ocr_service = OCRService()
llm_service = LLMService()

ingestion_agent = IngestionAgent(ocr_service)
extraction_agent = ExtractionAgent(llm_service)
validation_agent = ValidationAgent()

@router.get("", response_model=List[DnoPolicyData])
def list_policies():
    """Retorna todas as apólices cadastradas e estruturadas."""
    return storage_service.list_policies()

@router.get("/{policy_id}", response_model=DnoPolicyData)
def get_policy(policy_id: str):
    policy = storage_service.get_policy(policy_id)
    if not policy:
        raise HTTPException(status_code=404, detail="Apólice não encontrada.")
    return policy

@router.delete("/{policy_id}")
def delete_policy(policy_id: str):
    success = storage_service.delete_policy(policy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Apólice não encontrada para exclusão.")
    return {"status": "removido", "policy_id": policy_id}

@router.post("/upload", response_model=DnoPolicyData)
async def upload_policy(file: UploadFile = File(...)):
    """
    Recebe um arquivo PDF ou imagem de apólice,
    executa o pipeline completo multiagente (Ingestão -> Extração -> Validação)
    e persiste o resultado estruturado.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]:
        raise HTTPException(status_code=400, detail="Formato não suportado. Envie um arquivo PDF ou Imagem.")

    unique_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Pipeline Multiagente
        ingestion_res = ingestion_agent.run(file_path)
        extraction_dict = extraction_agent.run(ingestion_res)
        validated_policy = validation_agent.run(extraction_dict)
        
        # Persistência
        storage_service.save_policy(validated_policy)
        return validated_policy
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento da apólice: {str(e)}")

@router.post("/seed-samples", response_model=List[DnoPolicyData])
def seed_sample_policies():
    """
    Carrega e processa automaticamente as 3 apólices D&O de demonstração
    para viabilizar testes instantâneos.
    """
    sample_files = [
        "apolice_alpha_dno_standard.pdf",
        "apolice_beta_dno_corporate.pdf",
        "apolice_gamma_dno_premium.pdf"
    ]
    processed = []
    existing = {p.filename: p for p in storage_service.list_policies()}

    for sample_name in sample_files:
        sample_path = os.path.join(SAMPLES_DIR, sample_name)
        if not os.path.exists(sample_path):
            continue
        
        if sample_name in existing:
            processed.append(existing[sample_name])
            continue

        ingestion_res = ingestion_agent.run(sample_path)
        extraction_dict = extraction_agent.run(ingestion_res)
        validated_policy = validation_agent.run(extraction_dict)
        storage_service.save_policy(validated_policy)
        processed.append(validated_policy)

    return processed
