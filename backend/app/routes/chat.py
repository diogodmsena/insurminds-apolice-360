from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from backend.app.services.storage_service import StorageService
from backend.app.agents.qna_agent import QnAAgent
from backend.app.services.llm_service import LLMService

router = APIRouter(prefix="/api/chat", tags=["Chat"])

storage_service = StorageService()
llm_service = LLMService()
qna_agent = QnAAgent(llm_service)

class ChatRequest(BaseModel):
    session_id: Optional[str] = "default-session"
    question: str
    policy_ids: Optional[List[str]] = None

@router.post("")
def chat_with_policies(req: ChatRequest):
    """
    Realiza perguntas livres ao Agente Consultor Securitário
    com base nas apólices selecionadas (ou todas se nenhuma for informada).
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")

    # Se policy_ids não forem fornecidos, utiliza todas as apólices cadastradas
    if req.policy_ids and len(req.policy_ids) > 0:
        policies = [p for p in [storage_service.get_policy(pid) for pid in req.policy_ids] if p is not None]
    else:
        policies = storage_service.list_policies()

    if not policies:
        raise HTTPException(status_code=400, detail="Nenhuma apólice disponível para consulta. Carregue ao menos uma apólice primeiro.")

    answer_data = qna_agent.run(req.question, policies)

    # Persiste a mensagem no histórico do chat
    storage_service.save_chat_message(
        session_id=req.session_id,
        role="user",
        content=req.question,
        policy_ids=[p.id for p in policies]
    )
    storage_service.save_chat_message(
        session_id=req.session_id,
        role="assistant",
        content=answer_data["answer"],
        policy_ids=[p.id for p in policies]
    )

    return answer_data

@router.get("/history/{session_id}")
def get_chat_history(session_id: str):
    return storage_service.get_chat_history(session_id)
