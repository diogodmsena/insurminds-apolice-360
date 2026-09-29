import os
import pytest
from backend.app.agents.ingestion_agent import IngestionAgent
from backend.app.agents.extraction_agent import ExtractionAgent
from backend.app.agents.validation_agent import ValidationAgent
from backend.app.models.policy_schema import DnoPolicyData

def test_ingestion_and_extraction_pipeline():
    sample_pdf = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data", "samples", "apolice_alpha_dno_standard.pdf"
    )
    assert os.path.exists(sample_pdf), "PDF de amostra deve existir"

    ingestion_agent = IngestionAgent()
    ingest_res = ingestion_agent.run(sample_pdf)
    assert ingest_res["status"] == "sucesso"
    assert ingest_res["total_pages"] >= 1
    assert "Porto Seguro" in ingest_res["full_text"]

    extraction_agent = ExtractionAgent()
    extract_res = extraction_agent.run(ingest_res)
    assert "policy_number" in extract_res
    assert extract_res["lmg_amount"] > 0
    assert len(extract_res["basic_coverages"]) > 0

    validation_agent = ValidationAgent()
    validated = validation_agent.run(extract_res)
    assert isinstance(validated, DnoPolicyData)
    assert validated.validation_status in ["Válido", "Alerta"]
    assert validated.extraction_confidence_score >= 0.8
