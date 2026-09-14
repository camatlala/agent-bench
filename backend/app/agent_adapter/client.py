import httpx

class AgentAdapterClient:
    def run_scenario(self, endpoint_url: str, task: str, timeout_seconds: int = 60) -> dict:
        response = httpx.post(endpoint_url, json={"task": task}, timeout=timeout_seconds)
        response.raise_for_status()
        body = response.json()
        return {"trace": body.get("trace", []), "final_output": body.get("final_output", "")}
