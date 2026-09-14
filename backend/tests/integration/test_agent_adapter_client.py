import pytest
import httpx
import respx
from app.agent_adapter.client import AgentAdapterClient

pytestmark = pytest.mark.integration

@respx.mock
def test_run_scenario_returns_normalized_response():
    respx.post("https://agent.local/run").mock(
        return_value=httpx.Response(200, json={
            "trace": [{"kind": "reasoning", "content": "thinking"}],
            "final_output": "done",
        })
    )
    client = AgentAdapterClient()
    result = client.run_scenario("https://agent.local/run", "book a flight")
    assert result == {"trace": [{"kind": "reasoning", "content": "thinking"}], "final_output": "done"}

@respx.mock
def test_run_scenario_raises_on_http_error():
    respx.post("https://agent.local/run").mock(return_value=httpx.Response(500))
    client = AgentAdapterClient()
    with pytest.raises(httpx.HTTPStatusError):
        client.run_scenario("https://agent.local/run", "book a flight")
