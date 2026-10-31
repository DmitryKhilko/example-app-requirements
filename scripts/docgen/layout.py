"""Раскладка спецификаций по папкам и подразделам реестра: общее для проверки, индексов и меню."""

from __future__ import annotations

from pathlib import Path

from .config import INDEX_MARKER, REGISTRY_DIR, SECTION_TITLES
from .models import Feature


def section_of(rel_path: str) -> str | None:
    """Подраздел реестра, в котором лежит файл или папка: `registry/active` или `registry/archive` (путь относительно docs).

    None — путь вне подразделов (например, спецификация, которую забыли положить в `registry/active/<модуль>/`).
    """
    parts = Path(rel_path).parts
    if len(parts) >= 2 and parts[0] == REGISTRY_DIR and parts[1] in SECTION_TITLES:
        return f"{parts[0]}/{parts[1]}"
    return None


def folder_title(folder: Path, folder_features: list[Feature], docs_dir: Path) -> str:
    """Название папки для меню: подразделы реестра — из SECTION_TITLES, папки модулей — из поля `module`."""
    rel = folder.relative_to(docs_dir)
    if len(rel.parts) == 2 and section_of(rel.as_posix()) == rel.as_posix():
        return SECTION_TITLES[rel.parts[1]]
    rel_posix = rel.as_posix()
    modules = [f.module for f in folder_features if f.path.startswith(rel_posix + "/")]
    direct = [m for m, f in zip(modules, folder_features) if Path(f.path).parent == Path(rel_posix)]
    pool = direct or modules
    return max(set(pool), key=pool.count) if pool else folder.name


def registry_sections(features: list[Feature]) -> dict[str, list[Feature]]:
    """Спецификации по подразделам реестра (`registry/active`, `registry/archive`).

    Оба подраздела есть всегда, даже пустые: у каждого должен быть свой индекс и пункт в левом меню. Спецификации вне
    подразделов сюда не попадают (об этом сообщает проверка, validate/project.py).
    """
    sections: dict[str, list[Feature]] = {f"{REGISTRY_DIR}/{name}": [] for name in SECTION_TITLES}
    for f in features:
        section = section_of(f.path)
        if section is not None:
            sections[section].append(f)
    return sections


def spec_folders(docs_dir: Path, features: list[Feature]) -> set[Path]:
    """Папки, в которых спецификации лежат непосредственно."""
    return {(docs_dir / f.path).parent for f in features}


def is_manual_index(path: Path) -> bool:
    """index.md, созданный вручную (без маркера генератора): скрипт его не перезаписывает."""
    return path.exists() and INDEX_MARKER not in path.read_text(encoding="utf-8")
