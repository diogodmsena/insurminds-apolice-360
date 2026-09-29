from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.app.models.comparison_schema import ComparisonResult
from backend.app.services.storage_service import StorageService
from backend.app.agents.comparison_agent import ComparisonAgent
from backend.app.services.llm_service import LLMService

router = APIRouter(prefix="/api/compare", tags=["Comparison"])

storage_service = StorageService()
llm_service = LLMService()
comparison_agent = ComparisonAgent(llm_service)

class CompareRequest(BaseModel):
    policy_ids: List[str]

@router.post("", response_model=ComparisonResult)
def compare_policies(req: CompareRequest):
    """
    Compara 2 ou mais apólices através do Agente Comparador Especialista.
    Gera matriz de cobertura, gap analysis, scorecards e veredito executivo.
    """
    if len(req.policy_ids) < 2:
        raise HTTPException(status_code=400, detail="Selecione pelo menos 2 apólices para efetuar a comparação.")

    policies = []
    for pid in req.policy_ids:
        pol = storage_service.get_policy(pid)
        if not pol:
            raise HTTPException(status_code=404, detail=f"Apólice '{pid}' não encontrada no banco.")
        policies.append(pol)

    try:
        comparison_res = comparison_agent.run(policies)
        storage_service.save_comparison(comparison_res)
        return comparison_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a comparação: {str(e)}")

@router.get("/history", response_model=List[ComparisonResult])
def list_comparison_history():
    """Lista o histórico de comparações realizadas."""
    return storage_service.list_comparisons()

@router.get("/{comparison_id}", response_model=ComparisonResult)
def get_comparison_result(comparison_id: str):
    res = storage_service.get_comparison(comparison_id)
    if not res:
        raise HTTPException(status_code=404, detail="Comparação não localizada.")
    return res
