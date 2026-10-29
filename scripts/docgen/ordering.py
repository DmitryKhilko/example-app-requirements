"""Порядок модулей (nav-order.yml) и спецификаций (поле `order`)."""

from __future__ import annotations

from pathlib import Path

import yaml

from .config import NAV_ORDER_KEY
from .models import Feature
from .problems import Problems
from .textutils import clean, sort_key


def load_module_order(path: Path, problems: Problems) -> list[str]:
    """Список модулей из nav-order.yml (необязательный файл). Пустой список — порядок по алфавиту."""
    if not path.exists():
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        problems.error(path, f"не удалось разобрать YAML: {exc}")
        return []
    modules = data.get(NAV_ORDER_KEY) if isinstance(data, dict) else None
    if not isinstance(modules, list) or not all(isinstance(m, str) for m in modules):
        problems.error(path, f"ожидается список названий модулей в ключе `{NAV_ORDER_KEY}`")
        return []
    return [clean(m) for m in modules]


def module_key(module: str, module_order: list[str]) -> tuple[int, str]:
    """Модули из nav-order.yml — в заданном порядке, остальные — после них по алфавиту."""
    name = clean(module)
    pos = module_order.index(name) if name in module_order else len(module_order)
    return pos, sort_key(name)


def feature_key(feature: Feature) -> tuple[bool, int, str]:
    """Спецификации с `order` — по возрастанию номера, остальные — после них по алфавиту."""
    return feature.order is None, feature.order or 0, sort_key(feature.name)
