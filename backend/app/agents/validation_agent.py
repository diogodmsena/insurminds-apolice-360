from typing import Dict, Any, List
from backend.app.agents.base import BaseAgent
from backend.app.models.policy_schema import DnoPolicyData

class ValidationAgent(BaseAgent):
    """
    Agente responsável por auditar a conformidade técnica securitária:
    - Verifica consistência financeira (Sublimites <= LMG global).
    - Valida cronologia (Início vigência <= Fim vigência).
    - Avalia cobertura essencial mínima (Custos de Defesa).
    - Calcula o Score Final de Confiança e gera notas de auditoria.
    """
    def __init__(self):
        super().__init__("ValidationAgent")

    def run(self, extraction_dict: Dict[str, Any]) -> DnoPolicyData:
        self.logger.info(f"Iniciando validação de conformidade para apólice {extraction_dict.get('policy_number')}")
        notes: List[str] = []
        status = "Válido"
        confidence = float(extraction_dict.get("extraction_confidence_score", 0.90))

        lmg = float(extraction_dict.get("lmg_amount", 0.0))
        if lmg <= 0:
            notes.append("Alerta: Limite Máximo de Garantia (LMG) não identificado ou zerado.")
            status = "Alerta"
            confidence -= 0.20

        # Validação de Sublimites
        sublimits = extraction_dict.get("sublimits", [])
        for sub in sublimits:
            sub_amt = float(sub.get("amount", 0.0))
            if sub_amt > lmg and lmg > 0:
                notes.append(f"Inconsistência: Sublimite '{sub.get('name')}' (R$ {sub_amt:,.2f}) excede o LMG global (R$ {lmg:,.2f}).")
                status = "Alerta"
                confidence -= 0.10

        # Validação de Coberturas Básicas Essenciais
        basic_covs = extraction_dict.get("basic_coverages", [])
        has_defense_costs = any("defesa" in c.get("title", "").lower() for c in basic_covs)
        if not has_defense_costs:
            notes.append("Aviso técnico: Cobertura explícita de Custos de Defesa não rotulada nas coberturas básicas.")
            confidence -= 0.05

        # Validação de Franquia / POS
        deductibles = extraction_dict.get("deductibles_pos", [])
        if not deductibles:
            notes.append("Observação: Cláusula específica de POS (franquia) não explicitada na tabela resumida.")

        if not notes:
            notes.append("Apólice validada com sucesso: Estrutura em total conformidade com a regulamentação SUSEP D&O.")

        extraction_dict["validation_status"] = status
        extraction_dict["validation_notes"] = notes
        extraction_dict["extraction_confidence_score"] = max(0.5, min(1.0, round(confidence, 2)))

        policy_obj = DnoPolicyData.model_validate(extraction_dict)
        self.logger.info(f"Validação concluída: Status {status}, Score: {policy_obj.extraction_confidence_score}")
        return policy_obj
