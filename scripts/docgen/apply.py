"""Этап 4. Применение: записать план на диск или (check=True) только сверить с тем, что уже лежит на диске."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import Plan


@dataclass
class ApplyResult:
    """Что изменилось (при check=True — что устарело)."""
    map_changed: bool
    indexes_changed: int      # изменённые и удалённые лишние индексы
    indexes_total: int
    stale_removed: int
    nav_changed: bool
    icons_changed: int
    relations_changed: int

    @property
    def outdated(self) -> bool:
        return bool(self.map_changed or self.indexes_changed or self.nav_changed
                    or self.icons_changed or self.relations_changed)


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def apply_plan(plan: Plan, check: bool) -> ApplyResult:
    """Записывает изменившиеся файлы и удаляет лишние индексы; при check=True ничего на диске не меняет."""
    map_changed = _read(plan.map_path) != plan.map_content
    if map_changed and not check:
        _write(plan.map_path, plan.map_content)

    indexes_changed = len(plan.stale_indexes)
    if not check:
        for path in plan.stale_indexes:
            path.unlink()
    for path, content in plan.indexes.items():
        if _read(path) != content:
            indexes_changed += 1
            if not check:
                _write(path, content)

    nav_changed = False
    if plan.nav_path is not None and plan.nav_content is not None:
        nav_changed = _read(plan.nav_path) != plan.nav_content
        if nav_changed and not check:
            _write(plan.nav_path, plan.nav_content)

    if not check:
        for path in sorted(set(plan.icons) | set(plan.relations)):
            _write(path, plan.relations.get(path) or plan.icons[path])

    return ApplyResult(map_changed, indexes_changed, len(plan.indexes), len(plan.stale_indexes), nav_changed,
                       len(plan.icons), len(plan.relations))
