"""Раздел «Взаимосвязи» в каждой спецификации: схема Mermaid и таблица прямых связей фичи."""

from __future__ import annotations

import posixpath
import re
from collections import defaultdict
from urllib.parse import quote

from ..config import (DESCRIPTION_ANCHOR, DESCRIPTION_RE, DIRECTORY_URLS, MERMAID_FONT_SIZE, NO_RELATIONS_TEXT,
                      RELATION_EDGES, RELATION_LABELS, RELATION_ORDER, RELATIONS_ANCHOR, RELATIONS_BEGIN,
                      RELATIONS_BEGIN_PREFIX, RELATIONS_END, RELATIONS_TITLE, STATUS_TITLES)
from ..models import Feature, Link, Relation
from ..textutils import escape_md, sort_key


def relation_index(features: list[Feature]) -> tuple[dict[str, Feature], dict[str, list[tuple[Relation, Feature]]]]:
    """Фичи по имени файла и обратные связи: для каждой фичи — кто и как на неё ссылается."""
    by_slug = {f.slug: f for f in features}
    incoming: dict[str, list[tuple[Relation, Feature]]] = defaultdict(list)
    for f in features:
        for r in f.relations:
            if r.target in by_slug and r.target != f.slug:
                incoming[r.target].append((r, f))
    return by_slug, incoming


def feature_links(f: Feature, by_slug: dict[str, Feature],
                  incoming: dict[str, list[tuple[Relation, Feature]]]) -> list[Link]:
    """Все прямые связи фичи (объявленные ею и обратные), без повторов, в порядке RELATION_ORDER."""
    found: dict[tuple[str, str, str], Link] = {}

    def add(kind: str, direction: str, other: Feature, note: str) -> None:
        if kind == "related":           # связь симметрична: «in» и «out» сливаются в одну строку
            direction = "out"
        key = (kind, direction, other.slug)
        if key not in found or (note and not found[key].note):
            found[key] = Link(kind, direction, other, note or (found[key].note if key in found else ""))

    for r in f.relations:
        if r.target in by_slug and r.target != f.slug:
            add(r.kind, "out", by_slug[r.target], r.note)
    for r, source in incoming.get(f.slug, []):
        add(r.kind, "in", source, r.note)

    order = {key: i for i, key in enumerate(RELATION_ORDER)}
    return sorted(found.values(), key=lambda l: (order[(l.kind, l.direction)], sort_key(l.other.name)))


def _mermaid_text(text: str) -> str:
    """Экранирует текст подписи узла Mermaid (внутри двойных кавычек)."""
    return text.replace("&", "#amp;").replace('"', "#quot;").replace("<", "#lt;").replace(">", "#gt;")


def _table_cell(text: str) -> str:
    return text.replace("|", r"\|")


def _site_url(from_path: str, to_path: str) -> str:
    """Относительный адрес страницы на собранном сайте (для кликов по узлам схемы, которые Markdown не обрабатывает)."""
    if DIRECTORY_URLS:
        return posixpath.relpath(to_path[:-3], from_path[:-3]) + "/"
    return posixpath.relpath(to_path[:-3] + ".html", posixpath.dirname(from_path) or ".")


def render_diagram(f: Feature, links: list[Link]) -> list[str]:
    """Схема Mermaid: текущая фича и её прямые соседи.

    Стрелка идёт от субъекта связи к объекту («A зависит от B» -> A --> B), поэтому слева стоят те, кто зависит
    от текущей фичи / расширяет её / заменяет её, справа — то, от чего зависит она сама. Текущая фича выделена
    толщиной рамки, архивные — пунктирной рамкой (цвета не заданы: схема сама подстраивается под светлую и тёмную тему).
    """
    ids: dict[str, str] = {f.slug: "n0"}
    for link in links:
        ids.setdefault(link.other.slug, f"n{len(ids)}")

    def node(feature: Feature, current: bool = False) -> str:
        title = _mermaid_text(feature.name)
        title = f"<b>{title}</b>" if current else title
        return f'    {ids[feature.slug]}["{title}<br/><i>[{STATUS_TITLES[feature.shown_status]}]</i>"]'

    out = [f'%%{{init: {{"themeVariables": {{"fontSize": "{MERMAID_FONT_SIZE}"}}}}}}%%', "flowchart LR",
           node(f, current=True)]
    seen: set[str] = set()
    for link in links:
        if link.other.slug not in seen:
            seen.add(link.other.slug)
            out.append(node(link.other))
    for link in links:
        arrow, label = RELATION_EDGES[link.kind]
        a, b = ids[f.slug], ids[link.other.slug]
        if link.direction == "in":
            a, b = b, a
        out.append(f'    {a} {arrow}|"{label}"| {b}')

    archived = [ids[f.slug]] if f.archived else []
    archived += [ids[s] for s in seen if _find(links, s).archived]
    out += ["", "    classDef current stroke-width:3px", "    classDef archived stroke-dasharray:5 4",
            "    class n0 current"]
    if archived:
        out.append(f"    class {','.join(archived)} archived")
    out.append("")
    for link in links:
        if link.other.slug in seen:
            seen.discard(link.other.slug)       # одна ссылка на узел
            out.append(f'    click {ids[link.other.slug]} "{_site_url(f.path, link.other.path)}"')
    return out


def _find(links: list[Link], slug: str) -> Feature:
    return next(l.other for l in links if l.other.slug == slug)


def render_table(f: Feature, links: list[Link]) -> list[str]:
    """Таблица связей: тип связи, ссылка на фичу (с окном предпросмотра), статус (текстом, без значка), пояснение."""
    rows = ["| Связь | Функциональность | Статус | Комментарий |", "|---|---|---|---|"]
    for link in links:
        other = link.other
        href = quote(posixpath.relpath(other.path, posixpath.dirname(f.path) or "."))
        rows.append(
            f"| {RELATION_LABELS[(link.kind, link.direction)]} "
            f"| [{_table_cell(escape_md(other.name))}]({href}#{DESCRIPTION_ANCHOR}){{data-preview}} "
            f"| {STATUS_TITLES[other.shown_status]} "
            f"| {_table_cell(link.note)} |"
        )
    return rows


def render_relations_block(f: Feature, links: list[Link]) -> str:
    """Раздел «Взаимосвязи» целиком (вместе с маркерами)."""
    lines = [RELATIONS_BEGIN, "", f"## {RELATIONS_TITLE} {{#{RELATIONS_ANCHOR}}}", ""]
    if links:
        lines += ["Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.", "",
                  "```mermaid", *render_diagram(f, links), "```", "", *render_table(f, links)]
    else:
        lines.append(NO_RELATIONS_TEXT)
    lines += ["", RELATIONS_END]
    return "\n".join(lines)


_HEADING_RE = re.compile(r"^#{1,6}\s+\S")
_BLOCK_RE = re.compile(re.escape(RELATIONS_BEGIN_PREFIX) + r".*?" + re.escape(RELATIONS_END), re.DOTALL)


def place_relations_block(text: str, block: str) -> str | None:
    """Заменяет раздел между маркерами или вставляет его после раздела «Описание». None — нет раздела «Описание»."""
    if _BLOCK_RE.search(text):
        return _BLOCK_RE.sub(lambda _: block, text, count=1)

    lines = text.split("\n")
    in_fence, description, position = False, None, None
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif in_fence:
            continue
        elif description is None:
            if DESCRIPTION_RE.match(line):
                description = i
        elif _HEADING_RE.match(line):
            position = i
            break
    if description is None:
        return None
    if position is None:
        return text.rstrip("\n") + "\n\n" + block + "\n"
    head = "\n".join(lines[:position]).rstrip("\n")
    return head + "\n\n" + block + "\n\n" + "\n".join(lines[position:])


def plan_relations(features: list[Feature], texts: dict[str, str]) -> dict[str, str]:
    """Спецификации (путь относительно docs -> новый текст), у которых раздел «Взаимосвязи» нужно создать или обновить.

    Спецификации без раздела «Описание» пропускаются (предупреждение выдаёт проверка, validate/structure.py).
    """
    by_slug, incoming = relation_index(features)
    changed: dict[str, str] = {}
    for f in features:
        text = texts[f.path]
        new = place_relations_block(text, render_relations_block(f, feature_links(f, by_slug, incoming)))
        if new is not None and new != text:
            changed[f.path] = new
    return changed
