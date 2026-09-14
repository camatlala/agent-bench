from app.store.db import get_engine, get_sessionmaker, init_db
from app.store.models import EvalRun, Scenario, ScenarioResult, TraceStep, TokenUsage

def test_create_and_query_run(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    run = EvalRun(agent_endpoint_url="https://agent.local/run", worker_count=4, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)

    assert run.id is not None

    scenario = Scenario(run_id=run.id, task="book a flight", success_criteria="flight is booked")
    db.add(scenario)
    db.commit()
    db.refresh(scenario)

    result = ScenarioResult(scenario_id=scenario.id, final_output="Flight booked.", score=0.9, rationale="matches", status="scored")
    db.add(result)
    db.commit()
    db.refresh(result)

    db.add(TraceStep(result_id=result.id, step_index=0, kind="tool_call", content_json='{"tool": "search_flights"}'))
    db.add(TokenUsage(run_id=run.id, scenario_index=0, prompt_tokens=100, completion_tokens=20))
    db.commit()

    assert db.query(Scenario).count() == 1
    assert db.query(ScenarioResult).count() == 1
    assert db.query(TraceStep).count() == 1
    assert db.query(TokenUsage).count() == 1
