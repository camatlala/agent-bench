import { useState } from "react";
import { RunConfigForm } from "./components/RunConfigForm";
import { ResultsDashboard } from "./components/ResultsDashboard";
import { createRun } from "./api/client";

export function App() {
  const [runId, setRunId] = useState<number | null>(null);

  const handleSubmit = async (agentEndpointUrl: string, workerCount: number, scenariosJson: string) => {
    const { run_id } = await createRun(agentEndpointUrl, workerCount, scenariosJson);
    setRunId(run_id);
  };

  return (
    <div>
      <h1>Agent Bench</h1>
      {runId === null ? <RunConfigForm onSubmit={handleSubmit} /> : <ResultsDashboard runId={runId} />}
    </div>
  );
}
