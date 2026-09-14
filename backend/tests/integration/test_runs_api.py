import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

pytestmark = pytest.mark.integration

@patch("app.api.runs.EvalOrchestrator")
def test_create_run_returns_id_and_status(mock_orchestrator_cls, tmp_path, monkeypatch):
    monkeypatch.setenv("AGENTBENCH_DB_PATH", f"sqlite:///{tmp_path}/test.db")
    mock_orchestrator_cls.return_value.run = AsyncMock(return_value={
        "total_scenarios": 1, "scored": 1, "failed": 0, "average_score": 0.9,
    })

    from app.main import create_app
    app = create_app()
    client = TestClient(app)

    response = client.post("/runs", json={
        "agent_endpoint_url": "https://agent.local/run",
        "worker_count": 2,
        "scenarios_json": '[{"task": "book a flight", "success_criteria": "flight is booked"}]',
    })
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in ("pending", "running", "done")

    get_response = client.get(f"/runs/{body['run_id']}")
    assert get_response.status_code == 200
