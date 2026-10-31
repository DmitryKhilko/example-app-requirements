"""Проверка структуры текста спецификаций по шаблону: заголовки, якоря, обязательные разделы."""

from __future__ import annotations

import re
from pathlib import Path

from ..config import INDEX_NAME
from ..layout import section_of
from ..markdown import parse_headings
from ..models import BuildContext, Spec
from ..problems import Problems
from ..template import TemplateRules

# Идентификатор якоря: латиница, цифры, дефис и подчёркивание; начинается с буквы
_ANCHOR_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def check_headings(spec: Spec, rules: TemplateRules, problems: Problems) -> None:
    """Правила заголовков (они же записаны в комментарии в конце шаблона):

    1. у каждого заголовка есть явный якорь в конце строки: `## Текст {#latin-id}`;
    2. идентификатор — латиница, цифры, дефис и подчёркивание, начинается с буквы, уникален в файле;
    3. заголовок первого уровня один, его якорь совпадает с именем файла без расширения;
    4. все заголовки шаблона (уровня 2 и глубже) присутствуют с тем же названием, уровнем и якорем.
       Порядок разделов, отличающийся от шаблона, — предупреждение.

    Раздел «Взаимосвязи» (`{#relations}`) формирует скрипт; в шаблоне его нет, поэтому он не требуется, а повторный
    заголовок с таким якорем отклоняется правилом уникальности.
    """
    path = spec.path
    headings = parse_headings(spec.text)

    seen: dict[str, int] = {}
    for h in headings:
        mark = "#" * h.level
        if h.anchor is None:
            problems.error(path, f"у заголовка «{h.title}» нет явного якоря; ожидается `{mark} {h.title} {{#latin-id}}`",
                           h.line)
        elif not _ANCHOR_ID_RE.match(h.anchor):
            problems.error(path, f"недопустимый якорь `{h.anchor}`: латиница, цифры, дефис и подчёркивание, "
                                 f"первая — буква", h.line)
        elif h.anchor in seen:
            problems.error(path, f"якорь `{h.anchor}` уже использован в строке {seen[h.anchor]}", h.line)
        else:
            seen[h.anchor] = h.line

    titles = [h for h in headings if h.level == 1]
    if not titles:
        problems.error(path, f"нет заголовка первого уровня: ожидается `# Название фичи {{#{path.stem}}}`")
    elif len(titles) > 1:
        problems.error(path, "заголовок первого уровня должен быть один (лишние — в строках "
                             + ", ".join(str(h.line) for h in titles[1:]) + ")", titles[1].line)
    elif titles[0].anchor is not None and titles[0].anchor != path.stem:
        problems.error(path, f"якорь заголовка первого уровня `{titles[0].anchor}` должен совпадать с именем "
                             f"файла: `{path.stem}`", titles[0].line)

    by_anchor: dict[str, object] = {}
    for h in headings:
        if h.anchor is not None:
            by_anchor.setdefault(h.anchor, h)
    found_order: list[str] = []
    for section in rules.sections:
        mark = "#" * section.level
        expected = f"`{mark} {section.title} {{#{section.anchor}}}`"
        h = by_anchor.get(section.anchor)
        if h is None:
            same_title = next((x for x in headings if x.level == section.level
                               and " ".join(x.title.split()) == section.title), None)
            if same_title is not None and (same_title.anchor is None or not _ANCHOR_ID_RE.match(same_title.anchor)):
                continue   # заголовок есть, но с плохим якорем: об этом уже сообщено выше
            hint = f" (заголовок «{section.title}» есть, но с якорем `{same_title.anchor}`)" if same_title else ""
            problems.error(path, f"нет обязательного раздела: {expected}{hint}")
            continue
        found_order.append(section.anchor)
        if h.level != section.level or " ".join(h.title.split()) != section.title:
            problems.error(path, f"раздел `{{#{section.anchor}}}` должен выглядеть как в шаблоне: {expected}", h.line)

    actual_order = [h.anchor for h in headings if h.anchor in found_order]
    actual_order = [a for i, a in enumerate(actual_order) if a not in actual_order[:i]]
    if actual_order != found_order:
        problems.warning(path, "разделы идут не в порядке шаблона; ожидается: "
                                + " → ".join(f"«{by_anchor[a].title}»" for a in found_order))


def check_structure(specs: list[Spec], rules: TemplateRules, ctx: BuildContext, problems: Problems) -> None:
    """Проверяет структуру всех спецификаций (включая архив) и ищет в папках реестра файлы без метаданных."""
    for spec in specs:
        if spec.is_spec:
            check_headings(spec, rules, problems)

    # в `docs/registry/active/` и `docs/registry/archive/` лежат только спецификации (и сформированные index.md)
    for spec in specs:
        if spec.is_spec or spec.broken or section_of(spec.rel) is None:
            continue
        if spec.path.name == INDEX_NAME:
            continue  # сформированные index.md — не спецификации; созданные вручную отмечает validate/project.py
        problems.error(spec.path, "нет метаданных спецификации (`module`, `feature_name`): файл не попадёт в обзор и меню")
