def compress_trace(trace: list[dict]) -> list[dict]:
    if not trace:
        return []

    compressed = []
    i = 0
    while i < len(trace):
        current = trace[i]
        run_length = 1
        while (
            i + run_length < len(trace)
            and trace[i + run_length]["kind"] == current["kind"]
            and trace[i + run_length]["content"] == current["content"]
        ):
            run_length += 1

        if run_length > 1:
            compressed.append({**current, "repeated": run_length})
        else:
            compressed.append(current)

        i += run_length

    return compressed
