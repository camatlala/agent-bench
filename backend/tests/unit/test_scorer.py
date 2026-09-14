from unittest.mock import MagicMock
import pytest
from app.judge.scorer import JudgeScorer
from app.llm.base import LLMResponse
from app.context.shared_cache import SharedContextCache

def test_score_parses_valid_response_and_uses_shared_cache():
    llm = MagicMock()
    llm.complete.return_value = LLMResponse(text="SCORE: 0.75\nRATIONALE: mostly correct", prompt_tokens=50, completion_tokens=10)
    cache = SharedContextCache()

    scorer = JudgeScorer(llm=llm)
    result = scorer.score("book a flight", "flight is booked", "Flight booked.", [], cache)

    assert result["score"] == 0.75
    assert "mostly correct" in result["rationale"]
    assert "rubric_preamble" in cache._store

def test_score_raises_on_unparseable_response():
    llm = MagicMock()
    llm.complete.return_value = LLMResponse(text="looks fine", prompt_tokens=50, completion_tokens=10)
    cache = SharedContextCache()

    scorer = JudgeScorer(llm=llm)
    with pytest.raises(ValueError):
        scorer.score("book a flight", "flight is booked", "Flight booked.", [], cache)
