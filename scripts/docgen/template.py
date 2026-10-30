"""Правила проверки спецификаций, взятые из шаблона `templates/feature-spec-template.md`.

Шаблон — единственный источник правил, поэтому они не расходятся с тем, что видит автор:

* поле метаданных обязательно, если в комментарии к нему сказано «обязательное» (а не «необязательное»); так же
  читаются вложенные поля (`relations.depends_on`). Поля без пометки не обязательны. Допустимы только поля шаблона
  (и `icon`, которое ведёт сам скрипт);
* обязательны все заголовки второго и более глубоких уровней шаблона: с тем же названием, уровнем и якорем.
  Заголовок первого уровня в шаблоне — заготовка: его якорь должен совпадать с именем файла спецификации.

Если шаблона нет, проверяются только `module`, `feature_name` и раздел «Описание» (без них не работают карта и
раздел «Взаимосвязи»).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import DESCRIPTION_ANCHOR, FRONT_MATTER_RE, ICON_KEY
from .markdown import Heading, parse_headings
from .problems import Problems

_KEY_RE = re.compile(r"^(\s*)([A-Za-z_][\w-]*):(.*)$")
_REQUIRED_RE = re.compile(r"(?<!не)обязательн", re.IGNORECASE)
# Поля, без которых запись не считается спецификацией: обязательны всегда, даже если шаблона нет.
ALWAYS_REQUIRED = ("module", "feature_name")


@dataclass(frozen=True)
class MetaRule:
    """Поле метаданных шаблона: путь (`("module",)` или `("relations", "depends_on")`), обязательность, значение."""
    path: tuple[str, ...]
    required: bool
    placeholder: object              # значение поля в шаблоне («Название модуля», [] и т. п.)

    @property
    def name(self) -> str:
        return ".".join(self.path)

    @property
    def container(self) -> bool:
        """Список или набор в шаблоне: «обязательное» означает, что поле есть (пустой список допустим)."""
        return isinstance(self.placeholder, (list, dict))


@dataclass(frozen=True)
class TemplateRules:
    meta: tuple[MetaRule, ...]
    sections: tuple[Heading, ...]    # обязательные заголовки уровня 2 и глубже, в порядке шаблона
    known_fields: tuple[str, ...]    # допустимые поля верхнего уровня (пусто — не проверять)


# Правила на случай, если шаблона нет: только то, без чего карта и «Взаимосвязи» не работают.
FALLBACK_RULES = TemplateRules(
    meta=tuple(MetaRule((key,), True, "") for key in ALWAYS_REQUIRED),
    sections=(Heading(2, "Описание", DESCRIPTION_ANCHOR, 0),),
    known_fields=(),
)


def _comment(rest: str) -> str:
    """Комментарий в конце строки метаданных (после `#`); значение в кавычках может содержать `#`."""
    rest = rest.strip()
    if rest[:1] in ('"', "'"):
        closing = rest.find(rest[0], 1)
        rest = rest[closing + 1:] if closing != -1 else ""
    index = rest.find("#")
    return rest[index + 1:].strip() if index != -1 else ""


def _meta_rules(block: str, values: dict) -> list[MetaRule]:
    """Поля метаданных шаблона (верхний уровень и один уровень вложенности) с признаком обязательности."""
    rules: list[MetaRule] = []
    parent: str | None = None
    for line in block.split("\n"):
        found = _KEY_RE.match(line)
        if not found or line.lstrip().startswith("#"):
            continue
        indent, key, rest = found.groups()
        required = bool(_REQUIRED_RE.search(_comment(rest)))
        if not indent:
            parent = key
            rules.append(MetaRule((key,), required, values.get(key)))
        elif parent is not None:
            nested = values.get(parent)
            rules.append(MetaRule((parent, key), required, nested.get(key) if isinstance(nested, dict) else None))
    return rules


def load_template(path: Path, problems: Problems) -> TemplateRules:
    """Читает шаблон и возвращает правила; если шаблона нет или он испорчен — предупреждение и минимальные правила."""
    fallback = "проверяются только `module`, `feature_name` и раздел «Описание»"
    if not path.exists():
        problems.warning(path, f"шаблон спецификации не найден: {fallback}")
        return FALLBACK_RULES
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        problems.warning(path, f"в шаблоне нет блока метаданных: {fallback}")
        return FALLBACK_RULES
    try:
        values = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        problems.warning(path, f"в шаблоне некорректный YAML ({str(exc).splitlines()[0]}): {fallback}")
        return FALLBACK_RULES

    rules = _meta_rules(match.group(1), values)
    for key in ALWAYS_REQUIRED:
        index = next((i for i, r in enumerate(rules) if r.path == (key,)), None)
        if index is None:
            rules.append(MetaRule((key,), True, ""))
        elif not rules[index].required:
            rules[index] = MetaRule((key,), True, rules[index].placeholder)

    sections: list[Heading] = []
    for heading in parse_headings(text):
        if heading.level < 2:
            continue   # заголовок первого уровня — заготовка названия фичи
        if heading.anchor is None:
            problems.warning(path, f"у заголовка шаблона «{heading.title}» нет якоря, он не проверяется",
                             line=heading.line)
            continue
        sections.append(heading)

    known = tuple(dict.fromkeys([*(r.path[0] for r in rules), ICON_KEY]))
    return TemplateRules(tuple(rules), tuple(sections), known)
