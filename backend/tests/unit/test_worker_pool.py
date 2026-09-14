import asyncio
import pytest
from app.eval.worker_pool import run_with_worker_pool

@pytest.mark.asyncio
async def test_runs_all_items_and_preserves_order():
    async def double(x):
        await asyncio.sleep(0)
        return x * 2

    results = await run_with_worker_pool([1, 2, 3], double, worker_count=2)
    assert results == [2, 4, 6]

@pytest.mark.asyncio
async def test_bounds_concurrency():
    active = {"count": 0, "max_seen": 0}

    async def track(x):
        active["count"] += 1
        active["max_seen"] = max(active["max_seen"], active["count"])
        await asyncio.sleep(0.01)
        active["count"] -= 1
        return x

    await run_with_worker_pool(list(range(10)), track, worker_count=3)
    assert active["max_seen"] <= 3

@pytest.mark.asyncio
async def test_one_failure_does_not_block_others():
    async def maybe_fail(x):
        if x == 2:
            raise ValueError("boom")
        return x

    results = await run_with_worker_pool([1, 2, 3], maybe_fail, worker_count=2)
    assert results[0] == 1
    assert isinstance(results[1], ValueError)
    assert results[2] == 3
