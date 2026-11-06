"""Persistencia de partidas y récords en JSON."""

import json
import os
from typing import Optional

from config import SAVE_FILE

DEFAULT_DATA = {
    "record": 0,
    "saved_game": None,
}


def _load_raw() -> dict:
    if not os.path.exists(SAVE_FILE):
        return DEFAULT_DATA.copy()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_DATA.copy()
        data.setdefault("record", 0)
        data.setdefault("saved_game", None)
        return data
    except (json.JSONDecodeError, OSError):
        return DEFAULT_DATA.copy()


def _save_raw(data: dict) -> None:
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(f"[save] No se pudo guardar: {exc}")


def load_record() -> int:
    return int(_load_raw().get("record", 0))


def save_record(score: int) -> None:
    data = _load_raw()
    if score > int(data.get("record", 0)):
        data["record"] = score
        _save_raw(data)


def has_saved_game() -> bool:
    return _load_raw().get("saved_game") is not None


def load_game() -> Optional[dict]:
    return _load_raw().get("saved_game")


def save_game(snake_body: list, direction: tuple, score: int, level: int) -> None:
    data = _load_raw()
    data["saved_game"] = {
        "snake": [list(seg) for seg in snake_body],
        "direction": list(direction),
        "score": score,
        "level": level,
    }
    _save_raw(data)


def clear_saved_game() -> None:
    data = _load_raw()
    data["saved_game"] = None
    _save_raw(data)