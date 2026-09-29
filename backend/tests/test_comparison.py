import os
import pytest
from backend.app.agents.ingestion_agent import IngestionAgent
from backend.app.agents.extraction_agent import ExtractionAgent
from backend.app.agents.validation_agent import ValidationAgent
from backend.app.agents.comparison_agent import ComparisonAgent
from backend.app.models.comparison_schema import ComparisonResult

def test_comparison_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pdf1 = os.path.join(base_dir, "data", "samples", "apolice_alpha_dno_standard.pdf")
    pdf2 = os.path.join(base_dir, "data", "samples", "apolice_beta_dno_corporate.pdf")

    ingestion_agent = IngestionAgent()
    extraction_agent = ExtractionAgent()
    validation_agent = ValidationAgent()

    # Processar apólice 1
    p1_data = validation_agent.run(extraction_agent.run(ingestion_agent.run(pdf1)))
    # Processar apólice 2
    p2_data = validation_agent.run(extraction_agent.run(ingestion_agent.run(pdf2)))

    comparison_agent = ComparisonAgent()
    result = comparison_agent.run([p1_data, p2_data])

    assert isinstance(result, ComparisonResult)
    assert len(result.policy_ids) == 2
    assert len(result.scorecards) == 2
    assert len(result.coverage_matrix) > 0
    assert result.executive_verdict is not None
    assert len(result.strategic_recommendations) >= 3
