const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface RunDetail {
  run_id: number;
  status: string;
  agent_endpoint_url: string;
}

export async function createRun(agentEndpointUrl: string, workerCount: number, scenariosJson: string): Promise<{ run_id: number; status: string }> {
  const res = await fetch(`${BASE_URL}/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_endpoint_url: agentEndpointUrl, worker_count: workerCount, scenarios_json: scenariosJson }),
  });
  return res.json();
}

export async function getRun(id: number): Promise<RunDetail> {
  const res = await fetch(`${BASE_URL}/runs/${id}`);
  return res.json();
}

export function openRunStream(id: number, onEvent: (event: any) => void): WebSocket {
  const wsUrl = BASE_URL.replace(/^http/, "ws") + `/runs/${id}/stream`;
  const ws = new WebSocket(wsUrl);
  ws.onmessage = (msg) => onEvent(JSON.parse(msg.data));
  return ws;
}
