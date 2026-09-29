from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CoverageMatrixRow(BaseModel):
    coverage_name: str
    category: str = "Básica"  # Básica, Adicional, Extensão Especial
    policy_values: Dict[str, str]  # policy_id -> status ou valor ("Incluso até R$ 5M", "Não Contratado", etc.)
    is_gap: bool = False
    advantage_policy_id: Optional[str] = None
    note: Optional[str] = None

class ExclusionComparisonRow(BaseModel):
    exclusion_name: str
    policy_status: Dict[str, str]  # policy_id -> "Excluído", "Exceção Coberta", "Cláusula Estrita"
    severity_rank: str  # Alta, Moderada, Padrão
    critical_impact: str

class PolicyScorecard(BaseModel):
    policy_id: str
    insurer_name: str
    protection_score: float = Field(..., ge=0, le=100, description="Nota global de proteção de 0 a 100")
    financial_adequacy_score: float = Field(..., ge=0, le=100)
    coverage_breadth_score: float = Field(..., ge=0, le=100)
    claims_accessibility_score: float = Field(..., ge=0, le=100)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)

class ComparisonResult(BaseModel):
    id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    policy_ids: List[str]
    policies_meta: List[Dict[str, Any]]
    
    scorecards: Dict[str, PolicyScorecard]
    coverage_matrix: List[CoverageMatrixRow]
    exclusion_matrix: List[ExclusionComparisonRow]
    financial_summary: Dict[str, Any]
    
    gaps_identified: List[Dict[str, Any]]
    executive_verdict: str
    strategic_recommendations: List[str]
