import json

_REQUIRED_FIELDS = ["task", "success_criteria"]

def load_scenarios(raw_json: str) -> list[dict]:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Scenario file is not valid JSON: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Scenario file must contain a JSON list of scenario objects")

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValueError(f"Scenario at index {i} is not an object")
        missing = [f for f in _REQUIRED_FIELDS if f not in entry]
        if missing:
            raise ValueError(f"Scenario at index {i} is missing required field(s): {missing}")

    return data
