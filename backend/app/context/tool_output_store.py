class ToolOutputStore:
    def extract(self, trace: list[dict]) -> list[dict]:
        records = []
        pending_call = None

        for step in trace:
            if step["kind"] == "tool_call":
                if pending_call is not None:
                    records.append({**pending_call, "result": None})
                pending_call = {
                    "tool_name": step["content"].get("name"),
                    "arguments": step["content"].get("arguments", {}),
                }
            elif step["kind"] == "tool_result" and pending_call is not None:
                records.append({**pending_call, "result": step["content"].get("result")})
                pending_call = None

        if pending_call is not None:
            records.append({**pending_call, "result": None})

        return records
