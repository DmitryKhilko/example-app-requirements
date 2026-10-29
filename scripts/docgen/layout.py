"""Раскладка спецификаций по папкам и разделам: общее для проверки, индексов и меню."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .config import FOLDER_TITLES, INDEX_MARKER
from .models import Feature


def folder_title(folder: Path, folder_features: list[Feature], docs_dir: Path) -> str:
    """Название папки для меню: служебные папки — из FOLDER_TITLES, папки модулей — из поля `module`."""
    if folder.name in FOLDER_TITLES:
        return FOLDER_TITLES[folder.name]
    rel = folder.relative_to(docs_dir).as_posix()
    modules = [f.module for f in folder_features if f.path.startswith(rel + "/")]
    direct = [m for m, f in zip(modules, folder_features) if Path(f.path).parent == Path(rel)]
    pool = direct or modules
    return max(set(pool), key=pool.count) if pool else folder.name


def section_tabs(features: list[Feature]) -> dict[str, list[Feature]]:
    """Спецификации по разделам: первая папка пути (specifications, archive)."""
    tabs: dict[str, list[Feature]] = defaultdict(list)
    for f in features:
        parts = Path(f.path).parts
        if len(parts) > 1:
            tabs[parts[0]].append(f)
    return tabs


def spec_folders(docs_dir: Path, features: list[Feature]) -> set[Path]:
    """Папки, в которых спецификации лежат непосредственно."""
    return {(docs_dir / f.path).parent for f in features}


def is_manual_index(path: Path) -> bool:
    """index.md, созданный вручную (без маркера генератора): скрипт его не перезаписывает."""
    return path.exists() and INDEX_MARKER not in path.read_text(encoding="utf-8")
