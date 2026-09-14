from app.context.trace_compressor import compress_trace

def test_passes_through_distinct_steps():
    trace = [
        {"kind": "reasoning", "content": "thinking about the task"},
        {"kind": "tool_call", "content": {"name": "search", "arguments": {}}},
    ]
    assert compress_trace(trace) == trace

def test_collapses_repeated_identical_steps():
    trace = [
        {"kind": "tool_call", "content": {"name": "ping", "arguments": {}}},
        {"kind": "tool_call", "content": {"name": "ping", "arguments": {}}},
        {"kind": "tool_call", "content": {"name": "ping", "arguments": {}}},
    ]
    result = compress_trace(trace)
    assert len(result) == 1
    assert result[0]["repeated"] == 3
