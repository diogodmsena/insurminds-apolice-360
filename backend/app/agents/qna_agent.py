from typing import List, Dict, Any
from backend.app.agents.base import BaseAgent
from backend.app.models.policy_schema import DnoPolicyData
from backend.app.services.llm_service import LLMService

class QnAAgent(BaseAgent):
    """
    Agente Consultor Securitário D&O (RAG & Q&A).
    Responde a dúvidas sobre coberturas, franquias, prazos de prescrição,
    exclusões e diferenças entre apólices, citando cláusulas específicas.
    """
    def __init__(self, llm_service: LLMService = None):
        super().__init__("QnAAgent")
        self.llm_service = llm_service or LLMService()

    def run(self, question: str, policies: List[DnoPolicyData]) -> Dict[str, Any]:
        self.logger.info(f"Processando pergunta consultiva: '{question}' sobre {len(policies)} apólices.")

        # Montagem do contexto securitário das apólices
        context_snippets = []
        for p in policies:
            snippet = (
                f"=== APÓLICE: {p.policy_number} | SEGURADORA: {p.insurer_name} ===\n"
                f"Tomador: {p.policyholder} | LMG: R$ {p.lmg_amount:,.2f} | Vigência: {p.start_date} a {p.end_date}\n"
                f"Retroatividade: {p.retroactive_date} | Prazo Complementar: {p.discovery_period_months} meses\n"
                f"Franquias (POS): {[d.category + ': R$ ' + str(d.amount) for d in p.deductibles_pos]}\n"
                f"Coberturas Básicas: {[c.title + ' (' + (c.clause_reference or 'Contratual') + ')' for c in p.basic_coverages]}\n"
                f"Coberturas Adicionais: {[c.title + ' (' + (c.clause_reference or 'Extensão') + ')' for c in p.additional_coverages]}\n"
                f"Exclusões: {[e.title + ' (' + (e.clause_reference or 'Exclusão') + ')' for e in p.key_exclusions]}\n"
            )
            context_snippets.append(snippet)

        context_str = "\n".join(context_snippets)

        system_prompt = (
            "Você é o consultor sênior de seguros D&O da plataforma InsurMinds Apólice 360. "
            "Responda à pergunta do usuário de forma clara, técnica e fundamentada nas apólices fornecidas no contexto. "
            "Cite sempre a seguradora, o número da apólice e a cláusula ou extensão correspondente. "
            "Se a pergunta indagar sobre qual apólice é mais vantajosa, aponte os prós e contras objetivos."
        )

        prompt = f"""
CONTEXTO DAS APÓLICES CADASTRADAS:
{context_str}

PERGUNTA DO USUÁRIO:
{question}

Responda em formato Markdown profissional e amigável:
"""

        answer = self.llm_service.generate_text_response(prompt, system_prompt)

        # Identificação de apólices referenciadas
        mentioned_policies = [p.insurer_name for p in policies if p.insurer_name.lower() in answer.lower()]
        if not mentioned_policies and policies:
            mentioned_policies = [policies[0].insurer_name]

        return {
            "question": question,
            "answer": answer,
            "policies_referenced": mentioned_policies,
            "policy_count": len(policies)
        }
