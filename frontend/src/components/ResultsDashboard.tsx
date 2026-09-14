import { useEffect, useState } from "react";
import { getRun, openRunStream, RunDetail } from "../api/client";

export function ResultsDashboard({ runId }: { runId: number }) {
  const [run, setRun] = useState<RunDetail | null>(null);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    getRun(runId).then(setRun);
    const ws = openRunStream(runId, (event) => setEvents((prev) => [...prev, event]));
    return () => ws.close();
  }, [runId]);

  return (
    <div>
      <h3>Run {runId}: {run?.status}</h3>
      <ul>
        {events.map((e, i) => <li key={i}>{JSON.stringify(e)}</li>)}
      </ul>
    </div>
  );
}
