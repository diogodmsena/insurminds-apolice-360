from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SublimitItem(BaseModel):
    name: str = Field(..., description="Nome da cobertura ou extensão com sublimite")
    amount: float = Field(..., description="Valor monetário do sublimite")
    currency: str = Field(default="BRL", description="Moeda (BRL, USD, etc.)")
    percentage_lmg: Optional[float] = Field(None, description="Percentual do LMG correspondente")
    details: Optional[str] = Field(None, description="Condições ou restrições do sublimite")

class DeductibleItem(BaseModel):
    category: str = Field(..., description="Categoria de aplicação (Geral, Reclamações nos EUA, CVM, etc.)")
    amount: float = Field(..., description="Valor da franquia/POS")
    currency: str = Field(default="BRL", description="Moeda")
    description: Optional[str] = Field(None, description="Observações de aplicação da franquia")

class CoverageItem(BaseModel):
    title: str = Field(..., description="Título da cobertura")
    status: str = Field(default="Incluso", description="Status: Incluso, Excluído, Sublimitado, Opcional")
    limit_value: Optional[float] = Field(None, description="Valor específico caso aplicável")
    description: str = Field(..., description="Resumo explicativo da cobertura")
    clause_reference: Optional[str] = Field(None, description="Referência da cláusula no contrato (ex: Cláusula 4.2)")
    page_number: Optional[int] = Field(None, description="Página do documento de origem")

class ExclusionItem(BaseModel):
    title: str = Field(..., description="Título da exclusão")
    description: str = Field(..., description="Descrição detalhada do risco excluído")
    clause_reference: Optional[str] = Field(None, description="Referência da cláusula")
    severity: str = Field(default="Alta", description="Gravidade/Impacto: Alta, Média, Padrão de Mercado")

class DnoPolicyData(BaseModel):
    id: str = Field(..., description="Identificador único no sistema")
    filename: str = Field(..., description="Nome do arquivo original")
    policy_number: str = Field(..., description="Número da apólice ou proposta")
    insurer_name: str = Field(..., description="Nome da Seguradora emitente")
    policyholder: str = Field(..., description="Tomador (Empresa contratante)")
    insured_persons_scope: str = Field(..., description="Definição de Segurados protegidos")
    start_date: str = Field(..., description="Início da vigência (YYYY-MM-DD)")
    end_date: str = Field(..., description="Fim da vigência (YYYY-MM-DD)")
    retroactive_date: str = Field(default="Ilimitada", description="Data de retroatividade")
    territorial_scope: str = Field(default="Brasil", description="Âmbito geográfico")
    jurisdiction: str = Field(default="Brasil", description="Jurisdição competente")
    
    lmg_amount: float = Field(..., description="Limite Máximo de Garantia global")
    lmg_currency: str = Field(default="BRL", description="Moeda do LMG")
    premium_amount: Optional[float] = Field(None, description="Prêmio total (se especificado)")
    
    sublimits: List[SublimitItem] = Field(default_factory=list, description="Sublimites específicos")
    deductibles_pos: List[DeductibleItem] = Field(default_factory=list, description="Participação Obrigatória do Segurado")
    basic_coverages: List[CoverageItem] = Field(default_factory=list, description="Coberturas básicas")
    additional_coverages: List[CoverageItem] = Field(default_factory=list, description="Coberturas adicionais e extensões")
    key_exclusions: List[ExclusionItem] = Field(default_factory=list, description="Principais exclusões")
    
    discovery_period_months: Optional[int] = Field(default=36, description="Prazo complementar/suplementar em meses")
    extraction_confidence_score: float = Field(default=0.95, description="Score de confiança da extração (0.0 a 1.0)")
    validation_status: str = Field(default="Válido", description="Status da validação: Válido, Alerta, Incompleto")
    validation_notes: List[str] = Field(default_factory=list, description="Notas e alertas de validação")
    executive_summary: str = Field(..., description="Resumo executivo do perfil da apólice")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    file_path: Optional[str] = None
