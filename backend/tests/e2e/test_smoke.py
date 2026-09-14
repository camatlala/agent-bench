from unittest.mock import MagicMock
import pytest
from app.eval.orchestrator import EvalOrchestrator

pytestmark = pytest.mark.e2e

@pytest.mark.asyncio
async def test_full_eval_run_computes_correct_aggregate_metrics_with_concurrency():
    scenarios = [
        {"task": "book a flight", "success_criteria": "flight is booked"},
        {"task": "cancel a flight", "success_criteria": "flight is cancelled"},
        {"task": "check flight status", "success_criteria": "status is reported"},
    ]

    agent_client = MagicMock()
    agent_client.run_scenario.side_effect = [
        {"trace": [{"kind": "reasoning", "content": "booking now"}], "final_output": "Flight booked."},
        {"trace": [{"kind": "reasoning", "content": "cancelling now"}], "final_output": "Flight cancelled."},
        {"trace": [{"kind": "reasoning", "content": "checking status"}], "final_output": "Status: on time."},
    ]

    judge = MagicMock()
    judge.score.side_effect = [
        {"score": 1.0, "rationale": "booked"},
        {"score": 1.0, "rationale": "cancelled"},
        {"score": 0.8, "rationale": "reported"},
    ]

    orchestrator = EvalOrchestrator(agent_client=agent_client, judge=judge)
    result = await orchestrator.run(scenarios, "https://agent.local/run", worker_count=2)

    assert result["total_scenarios"] == 3
    assert result["scored"] == 3
    assert result["failed"] == 0
    assert result["average_score"] == pytest.approx(0.9333, rel=1e-3)
