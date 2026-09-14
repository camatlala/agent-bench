import { useState } from "react";

export function RunConfigForm({ onSubmit }: { onSubmit: (agentEndpointUrl: string, workerCount: number, scenariosJson: string) => void }) {
  const [agentEndpointUrl, setAgentEndpointUrl] = useState("");
  const [workerCount, setWorkerCount] = useState(4);
  const [scenariosJson, setScenariosJson] = useState("[]");

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(agentEndpointUrl, workerCount, scenariosJson); }}>
      <input placeholder="agent endpoint URL" value={agentEndpointUrl} onChange={(e) => setAgentEndpointUrl(e.target.value)} />
      <input type="number" placeholder="worker count" value={workerCount} onChange={(e) => setWorkerCount(Number(e.target.value))} />
      <textarea placeholder="scenarios JSON" value={scenariosJson} onChange={(e) => setScenariosJson(e.target.value)} />
      <button type="submit">Start run</button>
    </form>
  );
}
