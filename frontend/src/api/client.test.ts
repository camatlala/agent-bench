import { describe, it, expect, vi, afterEach } from "vitest";
import { createRun, getRun } from "./client";

describe("api client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("createRun posts to /runs", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ run_id: 1, status: "running" }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await createRun("https://agent.local/run", 4, "[]");

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/runs"),
      expect.objectContaining({ method: "POST" })
    );
    expect(result).toEqual({ run_id: 1, status: "running" });
  });

  it("getRun fetches run detail by id", async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ run_id: 1, status: "done", agent_endpoint_url: "https://agent.local/run" }),
    });
    vi.stubGlobal("fetch", mockFetch);

    const result = await getRun(1);
    expect(result.status).toBe("done");
  });
});
