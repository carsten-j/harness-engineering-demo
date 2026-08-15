"""Happy-path tests for the demo service."""

from fastapi.testclient import TestClient

from api.invoices import app
from web.views import format_total

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_total_empty_invoice() -> None:
    resp = client.post("/invoices/total", json={"customer": "ACME", "items": []})
    assert resp.status_code == 200
    assert resp.json() == {"customer": "ACME", "total_cents": 0}


def test_format_total() -> None:
    assert format_total(12345) == "123.45 kr"
