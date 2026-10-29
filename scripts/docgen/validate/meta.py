"""Проверка метаданных спецификаций: обязательные поля, статус, порядок, формат блока `relations`."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

from ..config import (DEFAULT_STATUS, DEFAULT_SUBMODULE, DESCRIPTION_ANCHOR, ORDER_KEY, RELATION_TYPES,
                      RELATIONS_KEY, STATUS_ALIASES, STATUS_ICONS)
from ..models import BuildContext, Feature, Relation, Spec
from ..problems import Problems
from ..textutils import clean


def normalize_status(raw: object, path: Path, problems: Problems) -> str:
    key = clean(raw).lower()
    if not key:
        problems.warning(path, f"не указан `status`, принято значение `{DEFAULT_STATUS}`")
        return DEFAULT_STATUS
    key = STATUS_ALIASES.get(key, key)
    if key not in STATUS_ICONS:
        allowed = ", ".join(STATUS_ICONS)
        problems.warning(
            path,
            f"неизвестный `status: {raw}` (допустимо: {allowed}), "
            f"принято значение `{DEFAULT_STATUS}`",
        )
        return DEFAULT_STATUS
    return key


def parse_relations(meta: dict, path: Path, problems: Problems) -> tuple[Relation, ...]:
    """Разбирает поле `relations` метаданных; ошибки формата попадают в problems."""
    raw = meta.get(RELATIONS_KEY)
    if raw is None:
        return ()
    if not isinstance(raw, dict):
        problems.error(path, f"`{RELATIONS_KEY}` должно быть набором «тип связи: список фичей»")
        return ()
    result: list[Relation] = []
    for kind, items in raw.items():
        if kind not in RELATION_TYPES:
            problems.error(path, f"неизвестный тип связи `{kind}` (допустимо: {', '.join(RELATION_TYPES)})")
            continue
        if items is None:
            continue
        if isinstance(items, (str, dict)):
            items = [items]
        if not isinstance(items, list):
            problems.error(path, f"`{RELATIONS_KEY}.{kind}` должно быть списком")
            continue
        for item in items:
            note = ""
            if isinstance(item, dict):
                unknown = set(item) - {"feature", "note"}
                if unknown or not item.get("feature"):
                    problems.error(path, f"элемент `{RELATIONS_KEY}.{kind}`: нужны поле `feature` и, по желанию, "
                                         f"`note` (лишние поля: {', '.join(sorted(map(str, unknown))) or 'нет'})")
                    continue
                note, item = clean(item.get("note")), item["feature"]
            target = clean(item)
            if not target:
                problems.error(path, f"пустое значение в `{RELATIONS_KEY}.{kind}`")
                continue
            result.append(Relation(kind, target.removesuffix(".md"), note))
    return tuple(result)


def parse_order(raw: object, path: Path, problems: Problems) -> int | None:
    """Поле `order`: целое число (лучше с шагом 10). Не задано — спецификация идёт после пронумерованных."""
    if raw is None or raw == "":
        return None
    if isinstance(raw, bool) or not isinstance(raw, int):
        problems.error(path, f"`{ORDER_KEY}` должно быть целым числом, например 10 (указано: {raw!r})")
        return None
    return raw


def build_features(specs: list[Spec], ctx: BuildContext, problems: Problems) -> list[Feature]:
    """Проверяет метаданные каждой спецификации и собирает из них фичи.

    Спецификацией считается файл с одним из полей SPEC_KEYS; остальные статьи (глоссарий, главная и т. п.)
    пропускаются. Ошибки (нет `module` или `feature_name`, неверный `order` и `relations`) попадают в problems;
    такая спецификация в список не попадает.
    """
    features: list[Feature] = []
    for spec in specs:
        if not spec.is_spec:
            continue  # не спецификация фичи (глоссарий, главная и т. п.)

        path, meta = spec.path, spec.meta
        module = clean(meta.get("module"))
        name = clean(meta.get("feature_name"))
        submodule = clean(meta.get("submodule")) or DEFAULT_SUBMODULE
        if not module:
            problems.error(path, "не заполнено обязательное поле `module`")
        if not name:
            problems.error(path, "не заполнено обязательное поле `feature_name`")
        if not module or not name:
            continue

        rel_to_docs = Path(spec.rel)
        in_archive_dir = ctx.archive_dir_name in rel_to_docs.parts[:-1]
        status = normalize_status(meta.get("status"), path, problems)
        archived = in_archive_dir or status == "archived"

        order = parse_order(meta.get(ORDER_KEY), path, problems)

        link = quote(os.path.relpath(path, ctx.output.parent).replace(os.sep, "/")) + f"#{DESCRIPTION_ANCHOR}"
        features.append(Feature(module, submodule, name, link, status, archived,
                                spec.rel, path.stem, parse_relations(meta, path, problems), order))
    return features
