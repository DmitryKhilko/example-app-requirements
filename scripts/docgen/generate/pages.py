"""Страницы-перечни: карта фичей (feature-map.md) и индексы папок и разделов (index.md)."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path
from urllib.parse import quote

from ..config import (DEFAULT_ARCHIVE_DIR_NAME, DESCRIPTION_ANCHOR, FOLDER_TITLES, GENERATED_COMMENT, INDEX_MARKER,
                      INDEX_NAME, PAGE_FRONT_MATTER, PLACEHOLDER_MODULE, PLACEHOLDER_PRODUCT)
from ..layout import folder_title, is_manual_index, section_tabs, spec_folders
from ..models import BuildContext, Feature
from ..textutils import escape_md
from .widgets import render_tree, statistics_section, status_keys


def render_map(features: list[Feature], module_order: list[str]) -> str:
    active = [f for f in features if not f.archived]
    archived = [f for f in features if f.archived]

    out: list[str] = [
        *PAGE_FRONT_MATTER,
        "# Карта функциональностей продукта {#feature-map}",
        "",
        GENERATED_COMMENT,
        "",
        *statistics_section(features, status_keys(), PLACEHOLDER_PRODUCT),
        "## Действующие спецификации {#active-features}",
        "",
    ]
    out += render_tree(active, module_order) if active else ["*Нет действующих спецификаций*", ""]
    out += ["## Архив спецификаций {#archived-features}", ""]
    out += render_tree(archived, module_order) if archived else ["*Архив пуст*", ""]
    return "\n".join(out).rstrip() + "\n"


def _page_statuses(archive: bool) -> list[str]:
    """Статусы плиток страницы: в архиве — только «архив», в действующих спецификациях — все, кроме «архив»."""
    return ["archived"] if archive else status_keys(exclude=("archived",))


def render_index(folder: Path, docs_dir: Path, features: list[Feature], module_order: list[str]) -> str:
    """Содержимое index.md папки модуля: статистика (плитки, отбор) и иерархия субмодулей только по этому модулю."""
    direct = [f for f in features if (docs_dir / f.path).parent == folder]
    title = folder_title(folder, features, docs_dir)
    slug = re.sub(r"[^a-z0-9]+", "-", folder.name.lower()).strip("-") or "folder"
    archive = DEFAULT_ARCHIVE_DIR_NAME in folder.relative_to(docs_dir).parts

    lines = [
        *PAGE_FRONT_MATTER,
        f"# {escape_md(title)} {{#{slug}}}", "", GENERATED_COMMENT, "",
        *statistics_section(direct, _page_statuses(archive), PLACEHOLDER_MODULE),
        "## Спецификации {#specs}", "",
        *render_tree(direct, module_order, lambda f: f"{Path(f.path).name}#{DESCRIPTION_ANCHOR}", with_modules=False),
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_section_index(tab: str, tab_features: list[Feature], module_order: list[str]) -> str:
    """Содержимое index.md раздела (вкладки меню): как карта, но только по спецификациям этого раздела."""
    title = FOLDER_TITLES.get(tab, tab)
    slug = re.sub(r"[^a-z0-9]+", "-", tab.lower()).strip("-") or "section"
    archive = tab == DEFAULT_ARCHIVE_DIR_NAME
    to_spec = lambda f: quote(posixpath.relpath(f.path, tab)) + f"#{DESCRIPTION_ANCHOR}"
    lines = [
        *PAGE_FRONT_MATTER,
        f"# {escape_md(title)} {{#{slug}}}", "", GENERATED_COMMENT, "",
        *statistics_section(tab_features, _page_statuses(archive), PLACEHOLDER_PRODUCT),
        "## Спецификации {#specs}", "",
        *render_tree(tab_features, module_order, to_spec),
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_indexes(ctx: BuildContext, features: list[Feature]) -> dict[Path, str]:
    """index.md для папок модулей (где спецификации лежат непосредственно) и для разделов (specifications, archive).

    Промежуточная папка archive/specifications индекса не получает: она избыточна. Вручную созданные index.md
    не перезаписываются (предупреждения о них выдаёт проверка, validate/project.py).
    """
    docs_dir = ctx.docs_dir
    result: dict[Path, str] = {}
    for folder in sorted(spec_folders(docs_dir, features)):
        target = folder / INDEX_NAME
        if is_manual_index(target):
            continue
        result[target] = render_index(folder, docs_dir, features, ctx.module_order)

    for tab, tab_features in sorted(section_tabs(features).items()):
        target = docs_dir / tab / INDEX_NAME
        if target in result or is_manual_index(target):
            continue
        result[target] = render_section_index(tab, tab_features, ctx.module_order)
    return result


def stale_indexes(docs_dir: Path, wanted: dict[Path, str]) -> list[Path]:
    """Ранее сгенерированные index.md, которые больше не нужны (например, в корневых папках)."""
    return [p for p in sorted(docs_dir.rglob(INDEX_NAME))
            if p not in wanted and p.parent != docs_dir and INDEX_MARKER in p.read_text(encoding="utf-8")]
