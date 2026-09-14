<h1 align="center">🕹️ Agent Bench</h1>
<p align="center"><b>LLM Agent Evaluation Harness</b></p>

<p align="center">
  <a href="https://github.com/DenverCoder1/readme-typing-svg">
    <img src="https://readme-typing-svg.demolab.com/?lines=Concurrent+scenario+eval;Shared+rubric+context+cache;Trace+compression+%2B+structured+tool+capture;Bounded+worker+pool%2C+one+failure+never+blocks&font=Fira%20Code&center=true&width=520&height=45&color=ffb454&vCenter=true&pause=1000&size=20" /></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-14354C.svg?logo=python&logoColor=white">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white">
  <img alt="asyncio" src="https://custom-icon-badges.demolab.com/badge/-asyncio-3776AB?style=flat&logoColor=white&logo=python">
  <img alt="React" src="https://img.shields.io/badge/React-20232a.svg?logo=react&logoColor=%2361DAFB">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-07405e.svg?logo=sqlite&logoColor=white">
  <img alt="pytest" src="https://img.shields.io/badge/Pytest-0A9EDC.svg?logo=pytest&logoColor=white">
  <img alt="No Docker required" src="https://custom-icon-badges.demolab.com/badge/-No%20Docker%20required-1F222E?style=flat&logoColor=white&logo=check-circle">
</p>

<p align="center">
  Run a JSON-defined scenario set concurrently against your own agent HTTP endpoint, scoring each run with an LLM judge — maximizing evaluations per token, not just per dollar.
</p>

<br/>

<details open>
<summary><h2>🧩 Architecture</h2></summary>

FastAPI backend runs a configurable-size worker pool against your agent's HTTP endpoint. The harness never runs the agent itself, and never injects a model choice into it — it only uses an LLM for judging.

| Piece | Role |
|---|---|
| `app/agent_adapter/` | HTTP client for your agent endpoint |
| `app/eval/worker_pool.py` | Bounded-concurrency dispatcher — one scenario's failure never blocks the rest |
| `app/context/` | Shared rubric cache · trace compressor · structured tool-output store · reasoning selector |
| `app/judge/` | Rubric-based LLM-judge scorer |
| `app/eval/orchestrator.py` | Wires worker pool → adapter → judge → aggregate |

</details>

<details open>
<summary><h2>🚀 Quickstart</h2></summary>

**Prerequisites:** Python 3.11+, Node 18+, an API key for Claude and/or OpenAI, and your own agent exposed as `POST <endpoint> {"task": str} -> {"trace": [...], "final_output": str}`.

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

No Docker needed — the agent under test lives entirely on your own infrastructure.

</details>

<details>
<summary><h2>📄 Scenario File Format</h2></summary>

```json
[
  {"task": "book a flight from NYC to LA", "success_criteria": "flight is booked and confirmation shown"},
  {"task": "cancel booking #1234", "success_criteria": "booking is cancelled"}
]
```

</details>

<details>
<summary><h2>⚙️ Environment Variables</h2></summary>

| Variable | Default | Purpose |
|---|---|---|
| `AGENTBENCH_DB_PATH` | `agentbench.db` | SQLite file path |
| `AGENTBENCH_WORKER_COUNT` | `4` | Default scenario concurrency |
| `AGENTBENCH_SCENARIO_TIMEOUT` | `60` | Per-scenario agent adapter timeout (seconds) |
| `ANTHROPIC_API_KEY` | — | Required to use the Claude judge |
| `OPENAI_API_KEY` | — | Required to use the OpenAI judge |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Frontend → backend URL |

</details>

<details>
<summary><h2>🧪 Testing</h2></summary>

```bash
pytest tests/unit -v
pytest tests/integration -v -m integration
pytest tests/e2e -v -m e2e
```

</details>

<details>
<summary><h2>📌 Status</h2></summary>

✅ 27/27 tests passing — fully verified, no Docker dependency in this harness.

</details>
