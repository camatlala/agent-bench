from app.context.reasoning_selector import select_relevant_reasoning

def test_filters_to_reasoning_steps_only():
    trace = [
        {"kind": "reasoning", "content": "need to check the flight booking system"},
        {"kind": "tool_call", "content": {"name": "search"}},
        {"kind": "reasoning", "content": "unrelated thought about the weather"},
    ]
    result = select_relevant_reasoning(trace, "flight is booked", max_steps=5)
    assert all(step["kind"] == "reasoning" for step in result)

def test_keeps_top_scoring_steps_in_original_order():
    trace = [
        {"kind": "reasoning", "content": "thinking about the weather today"},
        {"kind": "reasoning", "content": "the flight booking is confirmed"},
        {"kind": "reasoning", "content": "unrelated musings"},
    ]
    result = select_relevant_reasoning(trace, "flight booking confirmed", max_steps=1)
    assert len(result) == 1
    assert "flight booking" in result[0]["content"]
