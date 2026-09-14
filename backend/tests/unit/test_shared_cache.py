from app.context.shared_cache import SharedContextCache

def test_builder_called_once_for_repeated_key():
    cache = SharedContextCache()
    call_count = {"n": 0}

    def build():
        call_count["n"] += 1
        return "expensive preamble"

    first = cache.get_or_set("rubric", build)
    second = cache.get_or_set("rubric", build)

    assert first == second == "expensive preamble"
    assert call_count["n"] == 1

def test_different_keys_call_builder_separately():
    cache = SharedContextCache()
    assert cache.get_or_set("a", lambda: "A") == "A"
    assert cache.get_or_set("b", lambda: "B") == "B"
