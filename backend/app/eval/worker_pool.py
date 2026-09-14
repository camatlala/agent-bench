import asyncio
from typing import Any, Awaitable, Callable

async def run_with_worker_pool(items: list, worker_fn: Callable[[Any], Awaitable[Any]], worker_count: int) -> list:
    semaphore = asyncio.Semaphore(worker_count)

    async def guarded(item):
        async with semaphore:
            try:
                return await worker_fn(item)
            except Exception as exc:
                return exc

    return await asyncio.gather(*(guarded(item) for item in items))
