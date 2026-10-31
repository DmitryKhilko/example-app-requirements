"""Проверка метаданных спецификаций: обязательные поля, статус, порядок, формат блока `relations`."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote

from ..config import (DEFAULT_STATUS, DEFAULT_SUBMODULE, DESCRIPTION_ANCHOR, ID_KEY, ID_RE, ORDER_KEY, RELATION_TYPES,
                      RELATIONS_KEY, RELEASE_KEY, RELEASE_RE, STATUS_ALIASES, STATUS_ICONS, TEMPLATE_PLACEHOLDER_FIELDS)
from ..markdown import description_of
from ..models import BuildContext, Feature, Relation, Spec
from ..problems import Problems
from ..template import ALWAYS_REQUIRED, TemplateRules
from ..textutils import clean


def normalize_status(raw: object, path: Path, problems: Problems, required: bool = False) -> str:
    """Статус по жизненному циклу. Пустой — предупреждение (если поле не обязательное; обязательное проверяет
    check_template_meta), неизвестное значение — ошибка. В обоих случаях дальше работа идёт со статусом по умолчанию."""
    key = clean(raw).lower()
    if not key:
        if not required:
            problems.warning(path, f"не указан `status`, принято значение `{DEFAULT_STATUS}`")
        return DEFAULT_STATUS
    key = STATUS_ALIASES.get(key, key)
    if key not in STATUS_ICONS:
        problems.error(path, f"неизвестный `status: {raw}` (допустимо: {', '.join(STATUS_ICONS)})")
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


def build_features(specs: list[Spec], ctx: BuildContext, problems: Problems, rules: TemplateRules) -> list[Feature]:
    """Проверяет метаданные каждой спецификации и собирает из них фичи.

    Спецификацией считается файл с одним из полей SPEC_KEYS; остальные статьи (глоссарий, главная и т. п.)
    пропускаются. Ошибки (нет `module` или `feature_name`, неверный `order` и `relations`) попадают в problems;
    такая спецификация в список не попадает.
    """
    features: list[Feature] = []
    status_required = any(rule.path == ("status",) and rule.required for rule in rules.meta)
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
        status = normalize_status(meta.get("status"), path, problems, status_required)
        archived = in_archive_dir or status == "archived"

        order = parse_order(meta.get(ORDER_KEY), path, problems)
        release = clean(meta.get(RELEASE_KEY))
        if release and not RELEASE_RE.match(release):
            problems.error(path, f"недопустимый `{RELEASE_KEY}: {release}`: номер релиза — числа через точку "
                                 f"(например, 1.2.1; в кавычках)")
            release = ""

        link = quote(os.path.relpath(path, ctx.output.parent).replace(os.sep, "/")) + f"#{DESCRIPTION_ANCHOR}"
        features.append(Feature(module, submodule, name, link, status, archived,
                                spec.rel, path.stem, parse_relations(meta, path, problems), order,
                                clean(meta.get(ID_KEY)), release, description_of(spec.text)))
    return features


def _is_empty(value: object) -> bool:
    """Поле не задано или пусто (пустая строка)."""
    return value is None or (isinstance(value, str) and not clean(value))


def _lookup(meta: dict, path: tuple[str, ...]) -> tuple[bool, object]:
    """Значение поля по пути (`("relations", "depends_on")`): (есть ли поле, значение)."""
    value: object = meta
    for key in path:
        if not isinstance(value, dict) or key not in value:
            return False, None
        value = value[key]
    return True, value


def check_template_meta(specs: list[Spec], rules: TemplateRules, problems: Problems) -> None:
    """Метаданные по шаблону:

    * обязательные поля заполнены. Обязательность берётся из комментариев шаблона; у списков и наборов
      (`relations`, `relations.depends_on`) «обязательное» значит, что поле есть, пустой список `[]` допустим;
    * значения-подсказки из шаблона («Название модуля», «Фамилия Имя») заменены;
    * `id` — латиница и цифры, группы через дефис; уникален среди всех спецификаций (включая архив);
    * неизвестные шаблону поля — предупреждение (чаще всего опечатка).

    `module` и `feature_name` проверяет build_features, поэтому здесь они пропускаются.
    """
    ids: dict[str, Spec] = {}
    for spec in specs:
        if not spec.is_spec:
            continue
        path, meta = spec.path, spec.meta

        missing_top: set[str] = set()
        for rule in rules.meta:
            if not rule.required or (len(rule.path) == 1 and rule.path[0] in ALWAYS_REQUIRED):
                continue
            if len(rule.path) > 1:
                parent_found, parent = _lookup(meta, rule.path[:1])
                if rule.path[0] in missing_top or (parent_found and parent is not None and not isinstance(parent, dict)):
                    continue   # о родителе уже сообщено (нет поля или неверный формат)
            found, value = _lookup(meta, rule.path)
            if found if rule.container else (found and not _is_empty(value)):
                continue
            if len(rule.path) == 1:
                missing_top.add(rule.path[0])
            if rule.container:
                hint = " (если значений нет, укажите пустой список `[]`)" if isinstance(rule.placeholder, list) else ""
                problems.error(path, f"нет обязательного поля `{rule.name}`{hint}")
            else:
                problems.error(path, f"не заполнено обязательное поле `{rule.name}`")

        for rule in rules.meta:
            if (len(rule.path) == 1 and rule.path[0] in TEMPLATE_PLACEHOLDER_FIELDS
                    and isinstance(rule.placeholder, str) and clean(rule.placeholder)):
                found, value = _lookup(meta, rule.path)
                if found and clean(value) == clean(rule.placeholder):
                    report = problems.error if rule.required else problems.warning
                    report(path, f"поле `{rule.name}` не заполнено: значение «{clean(value)}» взято из шаблона")

        code = clean(meta.get(ID_KEY))
        if code:
            if not ID_RE.match(code):
                problems.error(path, f"недопустимый `{ID_KEY}: {code}`: латиница и цифры, группы через дефис "
                                     f"(например, SHOP-CAT-SF-005)")
            elif code in ids:
                problems.error(path, f"`{ID_KEY}: {code}` уже используется в спецификации {ids[code].rel}")
            else:
                ids[code] = spec

        if rules.known_fields:
            unknown = [str(key) for key in meta if str(key) not in rules.known_fields]
            if unknown:
                problems.warning(path, f"неизвестные поля метаданных: {', '.join(unknown)} "
                                       f"(в шаблоне: {', '.join(rules.known_fields)})")
