# Agent Bench — LLM Agent Evaluation Harness

Self-hosted webapp that runs a JSON-defined scenario set concurrently against your own agent HTTP endpoint, scoring each scenario's trace and output with an LLM judge — while minimizing judge token spend via a shared rubric context cache, trace compression, structured tool-output capture, and selective reasoning capture.

## Prerequisites

- Python 3.11+
- Node 18+ / npm
- An API key for at least one LLM provider (Anthropic and/or OpenAI), used as the judge
- Your own agent exposed over HTTP as `POST <endpoint> {"task": str} -> {"trace": [{"kind": "reasoning"|"tool_call"|"tool_result", "content": ...}], "final_output": str}`

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

| Variable | Default | Purpose |
|---|---|---|
| `AGENTBENCH_DB_PATH` | `agentbench.db` | SQLite file path |
| `AGENTBENCH_WORKER_COUNT` | `4` | Default scenario concurrency |
| `AGENTBENCH_SCENARIO_TIMEOUT` | `60` | Per-scenario agent adapter timeout (seconds) |
| `ANTHROPIC_API_KEY` | — | Required to use the Claude judge |
| `OPENAI_API_KEY` | — | Required to use the OpenAI judge |

Run tests:

```bash
pytest tests/unit -v
pytest tests/integration -v -m integration
pytest tests/e2e -v -m e2e
```

No Docker is required for this harness — the agent under test lives entirely on the user's own infrastructure.

## Scenario file format

A JSON list of `{"task": string, "success_criteria": string}` objects, e.g.:

```json
[
  {"task": "book a flight from NYC to LA", "success_criteria": "flight is booked and confirmation shown"},
  {"task": "cancel booking #1234", "success_criteria": "booking is cancelled"}
]
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE_URL` if the backend isn't on `http://localhost:8000`.
