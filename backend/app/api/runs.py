import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from app.store.db import get_engine, get_sessionmaker, init_db
from app.store.models import EvalRun
from app.eval.orchestrator import EvalOrchestrator
from app.agent_adapter.client import AgentAdapterClient
from app.judge.scorer import JudgeScorer
from app.llm.registry import get_adapter
from app.scenarios.loader import load_scenarios
from app.config import settings

router = APIRouter()

_engine = get_engine(f"sqlite:///{settings.db_path}")
init_db(_engine)
_SessionLocal = get_sessionmaker(_engine)

def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateRunRequest(BaseModel):
    agent_endpoint_url: str
    worker_count: int
    scenarios_json: str

class RunResponse(BaseModel):
    run_id: int
    status: str

@router.post("/runs", response_model=RunResponse)
async def create_run(req: CreateRunRequest, db: DBSession = Depends(get_db)):
    run = EvalRun(agent_endpoint_url=req.agent_endpoint_url, worker_count=req.worker_count, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        scenarios = load_scenarios(req.scenarios_json)
        llm = get_adapter("claude", api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        orchestrator = EvalOrchestrator(agent_client=AgentAdapterClient(), judge=JudgeScorer(llm=llm))
        await orchestrator.run(scenarios, req.agent_endpoint_url, req.worker_count)
        run.status = "done"
    except Exception:
        run.status = "failed"
    db.commit()

    return RunResponse(run_id=run.id, status=run.status)

@router.get("/runs/{run_id}")
def get_run(run_id: int, db: DBSession = Depends(get_db)):
    run = db.query(EvalRun).get(run_id)
    return {"run_id": run.id, "status": run.status, "agent_endpoint_url": run.agent_endpoint_url}
