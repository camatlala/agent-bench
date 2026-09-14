import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from app.store.db import Base

class EvalRun(Base):
    __tablename__ = "eval_runs"
    id = Column(Integer, primary_key=True)
    agent_endpoint_url = Column(String, nullable=False)
    worker_count = Column(Integer, nullable=False, default=4)
    status = Column(String, nullable=False, default="pending")  # pending|running|failed|done
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("eval_runs.id"), nullable=False)
    task = Column(Text, nullable=False)
    success_criteria = Column(Text, nullable=False)

class ScenarioResult(Base):
    __tablename__ = "scenario_results"
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    final_output = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    rationale = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending|scored|failed|unscored

class TraceStep(Base):
    __tablename__ = "trace_steps"
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey("scenario_results.id"), nullable=False)
    step_index = Column(Integer, nullable=False)
    kind = Column(String, nullable=False)  # reasoning|tool_call|tool_result
    content_json = Column(Text, nullable=False)

class TokenUsage(Base):
    __tablename__ = "token_usage"
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("eval_runs.id"), nullable=False)
    scenario_index = Column(Integer, nullable=False)
    prompt_tokens = Column(Integer, nullable=False)
    completion_tokens = Column(Integer, nullable=False)
