from dataclasses import dataclass
import os

@dataclass
class Settings:
    db_path: str = os.environ.get("AGENTBENCH_DB_PATH", "agentbench.db")
    default_worker_count: int = int(os.environ.get("AGENTBENCH_WORKER_COUNT", "4"))
    scenario_timeout_seconds: int = int(os.environ.get("AGENTBENCH_SCENARIO_TIMEOUT", "60"))

settings = Settings()
