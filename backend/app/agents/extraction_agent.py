import uuid
from typing import Dict, Any
from backend.app.agents.base import BaseAgent
from backend.app.services.llm_service import LLMService

class ExtractionAgent(BaseAgent):
    """
    Agente especialista em Seguro D&O (Directors and Officers).
    Responsável por:
    - Identificação de Seguradora, Tomador, Segurados e Vigência.
    - Extração do LMG (Limite Máximo de Garantia) e sublimites.
    - Extração de franquias e POS (Participação Obrigatória do Segurado).
    - Mapeamento das Coberturas Básicas e Adicionais.
    - Mapeamento das Exclusões Críticas e Cláusulas Restritivas.
    """
    def __init__(self, llm_service: LLMService = None):
        super().__init__("ExtractionAgent")
        self.llm_service = llm_service or LLMService()

    def run(self, ingestion_result: Dict[str, Any]) -> Dict[str, Any]:
        file_name = ingestion_result.get("file_name", "apolice_desconhecida.pdf")
        full_text = ingestion_result.get("full_text", "")
        self.logger.info(f"Extraindo dados securitários D&O para: {file_name}")

        system_prompt = (
            "Você é um perito atuário e especialista jurídico em apólices de seguro D&O (Directors and Officers) no Brasil. "
            "Sua tarefa é analisar o texto do contrato de seguro/apólice e extrair os dados técnicos com precisão rigorosa, "
            "conforme as normas da SUSEP (Circular SUSEP 553/2017 e afins)."
        )

        prompt = f"""
Analise o texto integral da apólice D&O abaixo e retorne um objeto JSON contendo:
- policy_number: string (número da apólice)
- insurer_name: string (nome da seguradora)
- policyholder: string (tomador / empresa contratante)
- insured_persons_scope: string (definição dos segurados protegidos)
- start_date: string (formato YYYY-MM-DD)
- end_date: string (formato YYYY-MM-DD)
- retroactive_date: string (data ou 'Ilimitada')
- territorial_scope: string (âmbito territorial, ex: Brasil, Global, etc.)
- jurisdiction: string (jurisdição competente)
- lmg_amount: number (valor do Limite Máximo de Garantia em reais/moeda indicada)
- lmg_currency: string (ex: BRL)
- sublimits: lista de objetos [{{"name": string, "amount": number, "currency": string, "percentage_lmg": number, "details": string}}]
- deductibles_pos: lista de objetos [{{"category": string, "amount": number, "currency": string, "description": string}}]
- basic_coverages: lista de objetos [{{"title": string, "status": string, "limit_value": number, "description": string, "clause_reference": string, "page_number": number}}]
- additional_coverages: lista de objetos [{{"title": string, "status": string, "limit_value": number, "description": string, "clause_reference": string, "page_number": number}}]
- key_exclusions: lista de objetos [{{"title": string, "description": string, "clause_reference": string, "severity": string}}]
- discovery_period_months: number (prazo complementar/suplementar em meses)
- extraction_confidence_score: number entre 0.8 e 1.0
- executive_summary: string (resumo executivo do perfil da apólice e pontos de destaque)

TEXTO DO DOCUMENTO:
{full_text[:28000]}
"""

        raw_extracted = self.llm_service.generate_json_response(prompt, system_prompt)

        # Normalizações e preenchimento de campos auxiliares
        raw_extracted["id"] = f"pol-{uuid.uuid4().hex[:8]}"
        raw_extracted["filename"] = file_name
        raw_extracted["file_path"] = ingestion_result.get("file_path", "")

        self.logger.info(f"Extração concluída para {file_name}. Apólice: {raw_extracted.get('policy_number')}")
        return raw_extracted
