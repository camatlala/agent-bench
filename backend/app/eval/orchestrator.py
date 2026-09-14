from app.eval.worker_pool import run_with_worker_pool
from app.context.trace_compressor import compress_trace
from app.context.reasoning_selector import select_relevant_reasoning
from app.context.shared_cache import SharedContextCache

class EvalOrchestrator:
    def __init__(self, agent_client, judge):
        self._agent_client = agent_client
        self._judge = judge

    async def run(self, scenarios: list[dict], agent_endpoint_url: str, worker_count: int) -> dict:
        shared_cache = SharedContextCache()

        async def run_one(scenario: dict):
            agent_result = self._agent_client.run_scenario(agent_endpoint_url, scenario["task"])
            trace = agent_result["trace"]
            final_output = agent_result["final_output"]

            compressed = compress_trace(trace)
            relevant_reasoning = select_relevant_reasoning(compressed, scenario["success_criteria"])

            return self._judge.score(
                scenario["task"], scenario["success_criteria"], final_output, relevant_reasoning, shared_cache
            )

        results = await run_with_worker_pool(scenarios, run_one, worker_count)

        scored = 0
        failed = 0
        total_score = 0.0
        for result in results:
            if isinstance(result, Exception):
                failed += 1
            else:
                scored += 1
                total_score += result["score"]

        return {
            "total_scenarios": len(scenarios),
            "scored": scored,
            "failed": failed,
            "average_score": (total_score / scored) if scored else 0.0,
        }
