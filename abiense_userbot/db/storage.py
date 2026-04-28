from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any


class JsonStorage:
    def __init__(self, path: str = "abiense_data.json") -> None:
        self.path = Path(path)
        self._lock = Lock()
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict[str, Any]:
        raw = self.path.read_text(encoding="utf-8")
        return json.loads(raw or "{}")

    def _write(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            data = self._read()
            return data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            data = self._read()
            data[key] = value
            self._write(data)

    def delete(self, key: str) -> bool:
        with self._lock:
            data = self._read()
            existed = key in data
            if existed:
                del data[key]
                self._write(data)
            return existed
