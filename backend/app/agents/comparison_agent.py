import uuid
from typing import List, Dict, Any
from backend.app.agents.base import BaseAgent
from backend.app.models.policy_schema import DnoPolicyData
from backend.app.models.comparison_schema import (
    ComparisonResult,
    CoverageMatrixRow,
    ExclusionComparisonRow,
    PolicyScorecard
)
from backend.app.services.llm_service import LLMService

class ComparisonAgent(BaseAgent):
    """
    Agente especialista em Comparação Multidimensional de Apólices D&O.
    Compara 2 ou mais apólices identificando:
    - Assimetrias em LMG e Sublimites
    - Gaps de Cobertura (coberturas ausentes em uma e presentes em outra)
    - Diferenças na severidade de Exclusões e Franquias
    - Scorecards de Proteção Global (0 a 100)
    - Recomendações Estratégicas para a Diretoria / Tomador
    """
    def __init__(self, llm_service: LLMService = None):
        super().__init__("ComparisonAgent")
        self.llm_service = llm_service or LLMService()

    def run(self, policies: List[DnoPolicyData]) -> ComparisonResult:
        if len(policies) < 2:
            raise ValueError("A comparação exige pelo menos 2 apólices D&O.")

        self.logger.info(f"Iniciando comparação entre {len(policies)} apólices: {[p.policy_number for p in policies]}")
        comp_id = f"cmp-{uuid.uuid4().hex[:8]}"

        # 1. Informações básicas resumidas
        policies_meta = []
        for p in policies:
            policies_meta.append({
                "id": p.id,
                "policy_number": p.policy_number,
                "insurer_name": p.insurer_name,
                "policyholder": p.policyholder,
                "lmg_amount": p.lmg_amount,
                "lmg_currency": p.lmg_currency,
                "start_date": p.start_date,
                "end_date": p.end_date,
                "discovery_period_months": p.discovery_period_months
            })

        # 2. Construção da Matriz de Coberturas Uniformizada
        all_coverages_dict = {}
        for p in policies:
            for c in p.basic_coverages:
                cat = "Básica"
                if c.title not in all_coverages_dict:
                    all_coverages_dict[c.title] = {"category": cat, "items": {}}
                all_coverages_dict[c.title]["items"][p.id] = c

            for c in p.additional_coverages:
                cat = "Adicional"
                if c.title not in all_coverages_dict:
                    all_coverages_dict[c.title] = {"category": cat, "items": {}}
                all_coverages_dict[c.title]["items"][p.id] = c

        coverage_matrix_rows: List[CoverageMatrixRow] = []
        gaps_identified = []

        for cov_title, data in all_coverages_dict.items():
            policy_values = {}
            included_count = 0
            best_policy_id = None
            max_limit = -1.0

            for p in policies:
                item = data["items"].get(p.id)
                if item:
                    included_count += 1
                    val_str = item.status
                    if item.limit_value and item.limit_value > 0:
                        val_str += f" (até R$ {item.limit_value:,.0f})"
                        if item.limit_value > max_limit:
                            max_limit = item.limit_value
                            best_policy_id = p.id
                    else:
                        val_str += f" (LMG Global)"
                        if p.lmg_amount > max_limit:
                            max_limit = p.lmg_amount
                            best_policy_id = p.id
                    policy_values[p.id] = val_str
                else:
                    policy_values[p.id] = "Não Contemplado / Excluído"

            is_gap = (included_count > 0 and included_count < len(policies))
            if is_gap:
                gaps_identified.append({
                    "coverage": cov_title,
                    "covered_by": [p.insurer_name for p in policies if p.id in data["items"]],
                    "missing_in": [p.insurer_name for p in policies if p.id not in data["items"]]
                })

            coverage_matrix_rows.append(CoverageMatrixRow(
                coverage_name=cov_title,
                category=data["category"],
                policy_values=policy_values,
                is_gap=is_gap,
                advantage_policy_id=best_policy_id,
                note="Diferencial competitivo" if is_gap else "Padrão presente em ambas"
            ))

        # 3. Matriz de Exclusões
        all_exclusions = {}
        for p in policies:
            for exc in p.key_exclusions:
                if exc.title not in all_exclusions:
                    all_exclusions[exc.title] = {"severity": exc.severity, "impact": exc.description, "policies": {}}
                all_exclusions[exc.title]["policies"][p.id] = "Excluído com Cláusula Estrita"

        exclusion_matrix_rows: List[ExclusionComparisonRow] = []
        for exc_title, exc_info in all_exclusions.items():
            status_map = {}
            for p in policies:
                status_map[p.id] = exc_info["policies"].get(p.id, "Cláusula Padrão")
            exclusion_matrix_rows.append(ExclusionComparisonRow(
                exclusion_name=exc_title,
                policy_status=status_map,
                severity_rank=exc_info["severity"],
                critical_impact=exc_info["impact"]
            ))

        # 4. Geração de Scorecards Individuais
        scorecards: Dict[str, PolicyScorecard] = {}
        max_lmg = max(p.lmg_amount for p in policies)

        for p in policies:
            # Score financeiro (0 a 100) baseado no LMG relativo
            fin_score = round(min(100.0, (p.lmg_amount / max_lmg) * 100.0), 1) if max_lmg > 0 else 70.0
            
            # Amplitude de coberturas
            total_covs = len(p.basic_coverages) + len(p.additional_coverages)
            breadth_score = min(100.0, round(50.0 + (total_covs * 8.0), 1))
            
            # Acessibilidade de sinistros (Franquia Zero para PF = +20)
            has_zero_pos = any(d.amount == 0 for d in p.deductibles_pos)
            claims_score = 90.0 if has_zero_pos else 75.0

            # Score global ponderado
            protection_score = round((fin_score * 0.40) + (breadth_score * 0.35) + (claims_score * 0.25), 1)

            pros = []
            cons = []
            if p.lmg_amount == max_lmg:
                pros.append(f"Maior Limite Máximo de Garantia (R$ {p.lmg_amount:,.2f})")
            else:
                cons.append(f"LMG inferior em relação ao concorrente (R$ {p.lmg_amount:,.2f})")

            has_penhora = any("penhora" in c.title.lower() for c in p.additional_coverages)
            if has_penhora:
                pros.append("Proteção ativa contra Penhora Online de bens de executivos")
            else:
                cons.append("Sem cobertura explícita para bloqueios judiciais e penhora online")

            has_reg = any("investiga" in c.title.lower() or "cvm" in c.title.lower() for c in p.additional_coverages)
            if has_reg:
                pros.append("Amparo para custos prévios em investigações CVM/CADE")

            scorecards[p.id] = PolicyScorecard(
                policy_id=p.id,
                insurer_name=p.insurer_name,
                protection_score=protection_score,
                financial_adequacy_score=fin_score,
                coverage_breadth_score=breadth_score,
                claims_accessibility_score=claims_score,
                pros=pros,
                cons=cons
            )

        # 5. Análise Comparativa Executiva e Recomendações
        best_policy = max(policies, key=lambda pol: scorecards[pol.id].protection_score)
        
        exec_verdict = (
            f"Conclusão da Avaliação Técnica: A apólice emitida por '{best_policy.insurer_name}' "
            f"(Score de Proteção {scorecards[best_policy.id].protection_score}/100) apresenta o arranjo contratual mais equilibrado "
            f"e vantajoso para o corpo diretivo da '{best_policy.policyholder}'. Ela se destaca pela maior solidez de LMG "
            f"(R$ {best_policy.lmg_amount:,.2f}) e inclusão de cláusulas vitais de salvaguarda patrimonial imediata, "
            f"tais como custos em investigações de órgãos reguladores e mitigação de constrição de ativos particulares."
        )

        recommendations = [
            f"Adotar preferencialmente a apólice da '{best_policy.insurer_name}' caso a prioridade seja a blindagem integral dos administradores.",
            "Requerer endosso para equiparação das cláusulas de Gestão de Crise e Penhora Online nas cotações concorrentes.",
            "Certificar a manutenção da data de retroatividade 'Ilimitada' em caso de portabilidade entre seguradoras, evitando perda de direito adquirido.",
            "Assegurar que as franquias para reclamações com litisconsórcio corporativo sejam suportadas integralmente pelo Tomador (Pessoa Jurídica)."
        ]

        financial_summary = {
            "max_lmg": max_lmg,
            "min_lmg": min(p.lmg_amount for p in policies),
            "difference_lmg": max_lmg - min(p.lmg_amount for p in policies),
            "best_policy_id": best_policy.id,
            "best_insurer": best_policy.insurer_name
        }

        return ComparisonResult(
            id=comp_id,
            policy_ids=[p.id for p in policies],
            policies_meta=policies_meta,
            scorecards=scorecards,
            coverage_matrix=coverage_matrix_rows,
            exclusion_matrix=exclusion_matrix_rows,
            financial_summary=financial_summary,
            gaps_identified=gaps_identified,
            executive_verdict=exec_verdict,
            strategic_recommendations=recommendations
        )
