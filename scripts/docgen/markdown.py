"""Разбор заголовков Markdown: уровень, текст и явный якорь `{#id}` в конце строки."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .config import DESCRIPTION_RE, FRONT_MATTER_RE, RELATIONS_BEGIN_PREFIX

_HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*$")
# Явный якорь в конце строки заголовка: `Текст {#latin-id}` (после идентификатора допустимы другие атрибуты attr_list)
_ANCHOR_RE = re.compile(r"^(.*?)[ \t]*\{#([^\s{}]*)(?:[ \t][^{}]*)?\}$")


@dataclass(frozen=True)
class Heading:
    level: int
    title: str            # текст заголовка без якоря
    anchor: str | None    # идентификатор из `{#id}`; None — якоря нет
    line: int             # номер строки в файле (с 1)


def parse_headings(text: str) -> list[Heading]:
    """Заголовки вида `## Текст {#id}` вне блока метаданных, блоков кода (``` и ~~~) и HTML-комментариев."""
    match = FRONT_MATTER_RE.match(text)
    offset = text[:match.end()].count("\n") if match else 0
    body = text[match.end():] if match else text

    headings: list[Heading] = []
    in_fence = in_comment = False
    for number, line in enumerate(body.split("\n"), start=offset + 1):
        stripped = line.strip()
        if in_comment:
            in_comment = "-->" not in line
            continue
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("<!--"):
            in_comment = "-->" not in stripped
            continue
        found = _HEADING_RE.match(line)
        if not found:
            continue
        raw = found.group(2)
        anchored = _ANCHOR_RE.match(raw)
        if anchored:
            headings.append(Heading(len(found.group(1)), anchored.group(1), anchored.group(2), number))
        else:
            headings.append(Heading(len(found.group(1)), raw, None, number))
    return headings


def description_of(text: str) -> str:
    """Текст раздела «Описание» (от заголовка с якорем `article-overview` до следующего заголовка или раздела «Взаимосвязи»).

    Блок метаданных, блоки кода и HTML-комментарии не учитываются при поиске заголовков; сам текст раздела возвращается
    как есть (Markdown), без лишних пустых строк по краям. Нет раздела — пустая строка.
    """
    match = FRONT_MATTER_RE.match(text)
    body = text[match.end():] if match else text
    lines: list[str] = []
    found = in_fence = False
    for line in body.split("\n"):
        stripped = line.strip()
        if not found:
            if DESCRIPTION_RE.match(line):
                found = True
            continue
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and (_HEADING_RE.match(line) or stripped.startswith(RELATIONS_BEGIN_PREFIX)):
            break
        lines.append(line.rstrip())
    return "\n".join(lines).strip("\n")
