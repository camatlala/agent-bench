from app.context.tool_output_store import ToolOutputStore

def test_extract_pairs_tool_call_and_result():
    trace = [
        {"kind": "reasoning", "content": "need to search"},
        {"kind": "tool_call", "content": {"name": "search", "arguments": {"q": "flights"}}},
        {"kind": "tool_result", "content": {"result": "found 3 flights"}},
    ]
    store = ToolOutputStore()
    result = store.extract(trace)

    assert result == [
        {"tool_name": "search", "arguments": {"q": "flights"}, "result": "found 3 flights"},
    ]

def test_extract_returns_empty_when_no_tool_steps():
    store = ToolOutputStore()
    assert store.extract([{"kind": "reasoning", "content": "just thinking"}]) == []
