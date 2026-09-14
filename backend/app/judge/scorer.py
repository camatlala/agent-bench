import re
import json
from app.llm.base import LLMAdapter
from app.context.shared_cache import SharedContextCache

_SCORE_RE = re.compile(r"score\s*:\s*([0-9]*\.?[0-9]+)", re.IGNORECASE)
_RATIONALE_RE = re.compile(r"rationale\s*:\s*(.+)", re.IGNORECASE | re.DOTALL)

_RUBRIC_PREAMBLE = (
    "You are grading whether an AI agent completed a task successfully. "
    "Score from 0 (complete failure) to 1 (fully successful) based on the "
    "agent's final output and its trace of reasoning and tool calls."
)

class JudgeScorer:
    def __init__(self, llm: LLMAdapter):
        self._llm = llm

    def score(self, task: str, success_criteria: str, final_output: str, compressed_trace: list[dict], shared_cache: SharedContextCache) -> dict:
        preamble = shared_cache.get_or_set("rubric_preamble", lambda: _RUBRIC_PREAMBLE)
        trace_text = json.dumps(compressed_trace) if compressed_trace else "(no trace)"

        prompt = (
            f"{preamble}\n\n"
            f"Task: {task}\n"
            f"Success criteria: {success_criteria}\n"
            f"Agent's final output: {final_output}\n"
            f"Agent's trace: {trace_text}\n\n"
            "Respond with exactly:\nSCORE: <a number between 0 and 1>\nRATIONALE: <one sentence>"
        )
        response = self._llm.complete([{"role": "user", "content": prompt}], tools=[])

        score_match = _SCORE_RE.search(response.text)
        rationale_match = _RATIONALE_RE.search(response.text)
        if not score_match:
            raise ValueError(f"Judge response did not contain a parseable SCORE: {response.text!r}")

        return {
            "score": float(score_match.group(1)),
            "rationale": rationale_match.group(1).strip() if rationale_match else "",
        }
