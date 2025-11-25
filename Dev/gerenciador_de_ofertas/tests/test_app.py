from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_preco_endpoint_responde():
    resp = client.get("/preco")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)


def test_alerta_endpoint_responde():
    resp = client.get("/alerta")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    assert "status" in body or "erro" in body