from typing import Callable

class SharedContextCache:
    def __init__(self):
        self._store: dict[str, str] = {}

    def get_or_set(self, key: str, builder: Callable[[], str]) -> str:
        if key not in self._store:
            self._store[key] = builder()
        return self._store[key]
