"""Страницы-перечни: «Обзор» реестра (registry/overview.md), индексы подразделов «Действующие» и «Архив» и индексы модулей."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path
from urllib.parse import quote

from ..config import (DEFAULT_ARCHIVE_DIR_NAME, DESCRIPTION_ANCHOR, GENERATED_COMMENT, INDEX_MARKER,
                      INDEX_NAME, OVERVIEW_ANCHOR, OVERVIEW_TITLE, PAGE_FRONT_MATTER, PLACEHOLDER_MODULE,
                      PLACEHOLDER_PRODUCT, SECTION_PAGE_TITLES)
from ..layout import folder_title, is_manual_index, registry_sections, spec_folders
from ..models import BuildContext, Feature
from ..textutils import escape_md
from .widgets import controls_block, render_tree, statistics_section, status_keys


def link_from(base_dir: str):
    """Функция «адрес спецификации относительно страницы, лежащей в папке base_dir» (base_dir — путь от docs, `.` — корень).

    Ссылка ведёт на раздел «Описание» спецификации.
    """
    return lambda f: quote(posixpath.relpath(f.path, base_dir)) + f"#{DESCRIPTION_ANCHOR}"


def render_overview(features: list[Feature], module_order: list[str], base_dir: str) -> str:
    """Страница «Обзор» (registry/overview.md): итоги по всем спецификациям и два списка — действующие и архивные.

    Структура: заголовок первого уровня, инфо-блок «Статусы спецификаций», плитки статусов с общим итогом, строка отбора,
    затем разделы «Действующие спецификации» и «Архивные спецификации» — вложенные сворачиваемые блоки
    «Модуль» → «Субмодуль» → спецификации. Плитки и отбор действуют сразу на оба списка.
    """
    active = [f for f in features if not f.archived]
    archived = [f for f in features if f.archived]
    link = link_from(base_dir)

    out: list[str] = [
        *PAGE_FRONT_MATTER,
        f"# {OVERVIEW_TITLE} {{#{OVERVIEW_ANCHOR}}}",
        "",
        GENERATED_COMMENT,
        "",
        *controls_block(features, status_keys(), PLACEHOLDER_PRODUCT),
        "## Действующие спецификации {#active-features}",
        "",
    ]
    out += render_tree(active, module_order, link) if active else ["*Нет действующих спецификаций*", ""]
    out += ["## Архивные спецификации {#archived-features}", ""]
    out += render_tree(archived, module_order, link) if archived else ["*Нет архивных спецификаций*", ""]
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


def render_section_index(section: str, section_features: list[Feature], module_order: list[str]) -> str:
    """Содержимое index.md подраздела («Действующие» или «Архив»): тот же вид, что у «Обзора», но по одному списку.

    Структура: заголовок первого уровня («Действующие спецификации» / «Архивные спецификации»), инфо-блок «Статусы
    спецификаций», плитки статусов с общим итогом, строка отбора и сразу за ними — сворачиваемые блоки
    «Модуль» → «Субмодуль» → спецификации. В «Действующих» нет статуса «архив», в «Архиве» — только он.
    `section` — путь подраздела от docs (`registry/active`).
    """
    name = posixpath.basename(section)
    archive = name == DEFAULT_ARCHIVE_DIR_NAME
    title = SECTION_PAGE_TITLES.get(name, name)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "section"
    empty = "*Нет архивных спецификаций*" if archive else "*Нет действующих спецификаций*"
    tree = render_tree(section_features, module_order, link_from(section)) if section_features else [empty, ""]
    lines = [
        *PAGE_FRONT_MATTER,
        f"# {escape_md(title)} {{#{slug}}}", "", GENERATED_COMMENT, "",
        *controls_block(section_features, _page_statuses(archive), PLACEHOLDER_PRODUCT),
        *tree,
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_indexes(ctx: BuildContext, features: list[Feature]) -> dict[Path, str]:
    """index.md для папок модулей (где спецификации лежат непосредственно) и для подразделов (registry/active, registry/archive).

    Индексы обоих подразделов создаются всегда, даже если спецификаций в них нет: у каждого есть пункт в левом меню.
    Вручную созданные index.md не перезаписываются (предупреждения о них выдаёт проверка, validate/project.py).
    """
    docs_dir = ctx.docs_dir
    result: dict[Path, str] = {}
    for folder in sorted(spec_folders(docs_dir, features)):
        target = folder / INDEX_NAME
        if is_manual_index(target):
            continue
        result[target] = render_index(folder, docs_dir, features, ctx.module_order)

    for section, section_features in registry_sections(features).items():
        target = docs_dir / section / INDEX_NAME
        if target in result or is_manual_index(target):
            continue
        result[target] = render_section_index(section, section_features, ctx.module_order)
    return result


def stale_indexes(docs_dir: Path, wanted: dict[Path, str]) -> list[Path]:
    """Ранее сгенерированные index.md, которые больше не нужны (например, после переноса модуля или смены структуры)."""
    return [p for p in sorted(docs_dir.rglob(INDEX_NAME))
            if p not in wanted and p.parent != docs_dir and INDEX_MARKER in p.read_text(encoding="utf-8")]
