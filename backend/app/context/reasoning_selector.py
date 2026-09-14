import re

_WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

def _tokens(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text)}

def select_relevant_reasoning(trace: list[dict], success_criteria: str, max_steps: int = 3) -> list[dict]:
    criteria_tokens = _tokens(success_criteria)
    reasoning_steps = [(i, step) for i, step in enumerate(trace) if step["kind"] == "reasoning"]

    scored = [
        (i, step, len(criteria_tokens & _tokens(step["content"])))
        for i, step in reasoning_steps
    ]
    scored.sort(key=lambda item: item[2], reverse=True)
    top = scored[:max_steps]
    top_by_original_index = sorted(top, key=lambda item: item[0])

    return [step for _, step, _ in top_by_original_index]
