import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["system"] == "InsurMinds Apólice 360"

def test_seed_and_list_policies():
    seed_res = client.post("/api/policies/seed-samples")
    assert seed_res.status_code == 200
    policies = seed_res.json()
    assert len(policies) >= 2

    list_res = client.get("/api/policies")
    assert list_res.status_code == 200
    all_pols = list_res.json()
    assert len(all_pols) >= len(policies)

def test_comparison_api():
    list_res = client.get("/api/policies")
    policies = list_res.json()
    assert len(policies) >= 2
    
    pids = [policies[0]["id"], policies[1]["id"]]
    comp_res = client.post("/api/compare", json={"policy_ids": pids})
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert len(comp_data["scorecards"]) == 2
    assert "executive_verdict" in comp_data

def test_chat_api():
    chat_res = client.post("/api/chat", json={
        "question": "Qual apólice oferece a melhor proteção para penhora online e custos de defesa?"
    })
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert "answer" in chat_data
    assert len(chat_data["answer"]) > 20

def test_upload_policy_api():
    import os
    from backend.app.config import SAMPLES_DIR
    sample_file = os.path.join(SAMPLES_DIR, "apolice_alpha_dno_standard.pdf")
    with open(sample_file, "rb") as f:
        response = client.post(
            "/api/policies/upload",
            files={"file": ("test_upload_alpha.pdf", f, "application/pdf")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["insurer_name"] != ""
    # Clean up uploaded test policy
    client.delete(f"/api/policies/{data['id']}")
