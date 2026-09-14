import pytest
from app.scenarios.loader import load_scenarios

def test_loads_valid_scenario_list():
    raw = '[{"task": "book a flight", "success_criteria": "flight is booked"}]'
    result = load_scenarios(raw)
    assert result == [{"task": "book a flight", "success_criteria": "flight is booked"}]

def test_raises_on_malformed_json():
    with pytest.raises(ValueError):
        load_scenarios("not json")

def test_raises_on_non_list_json():
    with pytest.raises(ValueError):
        load_scenarios('{"task": "x"}')

def test_raises_on_missing_field():
    with pytest.raises(ValueError):
        load_scenarios('[{"task": "book a flight"}]')
