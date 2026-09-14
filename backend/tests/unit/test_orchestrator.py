from unittest.mock import MagicMock
import httpx
import pytest
from app.eval.orchestrator import EvalOrchestrator

def _scenarios():
    return [
        {"task": "book a flight", "success_criteria": "flight is booked"},
        {"task": "cancel a flight", "success_criteria": "flight is cancelled"},
    ]

@pytest.mark.asyncio
async def test_run_scores_all_scenarios_successfully():
    agent_client = MagicMock()
    agent_client.run_scenario.return_value = {"trace": [], "final_output": "done"}

    judge = MagicMock()
    judge.score.return_value = {"score": 0.8, "rationale": "ok"}

    orchestrator = EvalOrchestrator(agent_client=agent_client, judge=judge)
    result = await orchestrator.run(_scenarios(), "https://agent.local/run", worker_count=2)

    assert result["total_scenarios"] == 2
    assert result["scored"] == 2
    assert result["failed"] == 0
    assert result["average_score"] == 0.8

@pytest.mark.asyncio
async def test_run_counts_agent_failures_without_stopping():
    agent_client = MagicMock()
    agent_client.run_scenario.side_effect = [
        httpx.HTTPStatusError("boom", request=MagicMock(), response=MagicMock()),
        {"trace": [], "final_output": "cancelled"},
    ]

    judge = MagicMock()
    judge.score.return_value = {"score": 0.9, "rationale": "ok"}

    orchestrator = EvalOrchestrator(agent_client=agent_client, judge=judge)
    result = await orchestrator.run(_scenarios(), "https://agent.local/run", worker_count=2)

    assert result["total_scenarios"] == 2
    assert result["scored"] == 1
    assert result["failed"] == 1
