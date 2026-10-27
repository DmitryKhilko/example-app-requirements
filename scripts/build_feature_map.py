#!/usr/bin/env python3
"""Генератор карты фичей (Feature Map) по метаданным спецификаций.

Скрипт обходит папку docs/, читает YAML Front Matter у каждого .md-файла и
собирает иерархическое оглавление «Модуль -> Субмодуль -> Фича» со ссылками на
спецификации. Результат записывается в docs/feature-map.md.

Принципы работы
---------------
* Карта каждый раз собирается с нуля (идемпотентно): новая спецификация
  появляется в карте, удалённая исчезает, изменённый статус обновляется.
* Спецификацией считается файл, в метаданных которого есть хотя бы одно из полей
  `module`, `submodule`, `feature_name`. Остальные статьи (глоссарий, главная и
  т. п.) в карту не попадают.
* Архивная спецификация — файл внутри docs/archive/ ИЛИ файл со статусом
  `archived`. В карте такие фичи выводятся в отдельном разделе со значком коробки.
* Страница карты состоит из разделов: «Описание» (краткое пояснение, служебная заметка и блок
  «Обозначения»), «Статистика» (блок «Всего спецификаций» и кнопки фильтра по статусам),
  «Актуальные функциональности» и «Архивные функциональности». Текст описания — в константе
  PAGE_DESCRIPTION. У всех заголовков страницы заданы явные якоря, как в спецификациях:
  `{#feature-map}`, `{#article-overview}`, `{#statistics}`, `{#active-features}`, `{#archived-features}`.
* Каждая ссылка ведёт на раздел «Описание» (`#article-overview`) и снабжена атрибутами
  `data-preview` (окно предпросмотра) и `data-status` (код статуса для фильтра на странице).
* В файле карты нет даты и времени, поэтому без реальных изменений в
  спецификациях файл не меняется и автокоммит не создаётся.
* Взаимосвязи фичей. В метаданных спецификации можно задать блок `relations` (типы связей —
  в RELATION_TYPES). На него ссылаются по имени файла без расширения (оно же — якорь заголовка
  первого уровня), поэтому при переносе файла в архив связи не ломаются. Скрипт описывает связь
  один раз (в спецификации-источнике), а обратные связи («используется в», «расширяется…»)
  вычисляет сам. В каждой спецификации сразу после раздела «Описание» он создаёт и обновляет раздел
  «Взаимосвязи» (`{#relations}`) — схему Mermaid и таблицу только для ЭТОЙ фичи и её прямых
  соседей (полная карта связей не строится). Раздел заключён в маркеры RELATIONS_BEGIN/RELATIONS_END:
  всё между ними пересобирается с нуля, вручную править не нужно. Если маркеров нет, раздел
  вставляется перед первым заголовком, следующим за «Описанием».
* Проверки связей (ошибка — сборка падает): неизвестная фича, связь на себя, неизвестный тип связи
  или поле, повторяющееся имя файла у двух спецификаций, цикл в `depends_on`. Предупреждение:
  действующая фича зависит от архивной или расширяет её, одна и та же связь указана дважды.
  Без реальных изменений метаданных разделы «Взаимосвязи» не меняются, автокоммит не создаётся.

Запуск
------
    python scripts/build_feature_map.py           # пересобрать карту, индексы, меню и разделы «Взаимосвязи»
    python scripts/build_feature_map.py --check   # только проверить, что всё актуально

Код возврата 1 — ошибка в метаданных (нет `module` или `feature_name`, битый YAML, ошибки в `relations`)
либо, в режиме --check, что-то из сформированного устарело.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

import yaml

# ---------------------------------------------------------------------------
# Настройки
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUTPUT = DEFAULT_DOCS_DIR / "feature-map.md"
DEFAULT_ARCHIVE_DIR_NAME = "archive"

# Статусы фичи по жизненному циклу (SDLC); те же подписи заданы в [project.extra.status]
# файла zensical.toml. Порядок важен: в таком порядке статусы идут в легенде и статистике.
#   backlog     — фича заведена, к работе не приступали
#   analysis    — анализ: аналитик собирает и пишет требования, спецификацию согласуют («три амиго»)
#   ready       — спецификация утверждена, фича готова к разработке
#   development — идёт разработка
#   released    — реализовано, работает в эксплуатации
#   archived    — выведена из эксплуатации (ставится автоматически для файлов из docs/archive/)
STATUS_ICONS = {
    "backlog": ":lucide-file:",
    "analysis": ":lucide-file-pen-line:",
    "ready": ":lucide-file-check:",
    "development": ":lucide-file-braces:",
    "released": ":lucide-file-text:",
    "archived": ":lucide-file-archive:",
}
STATUS_TITLES = {
    "backlog": "бэклог",
    "analysis": "анализ",
    "ready": "готово к разработке",
    "development": "разработка",
    "released": "реализовано",
    "archived": "архив",
}
# Пояснения к статусам — выводятся в блоке «Обозначения» на странице перечня.
STATUS_DESCRIPTIONS = {
    "backlog": "зафиксированное сырое требование или идея",
    "analysis": "детализация и согласование требования",
    "ready": "утверждённое требование, готовое к реализации",
    "development": "требование в работе у команды разработки и тестирования",
    "released": "код, связанный с требованием, успешно развёрнут на проде",
    "archived": "отклонённое или устаревшее требование",
}
# Синонимы: допускаются русские названия статусов (регистр не важен).
STATUS_ALIASES = {
    "бэклог": "backlog",
    "анализ": "analysis",
    "готово к разработке": "ready",
    "разработка": "development",
    "реализовано": "released",
    "архив": "archived",
}
DEFAULT_STATUS = "backlog"
DEFAULT_SUBMODULE = "Общее"

# Каждая ссылка карты ведёт на раздел «Описание» спецификации: в спецификации заголовок
# должен иметь явный якорь `## Описание {#article-overview}`. Атрибут `data-preview`
# включает окно предпросмотра этого раздела при наведении (расширение attr_list).
# Пробела между `)` и `{` быть не должно: иначе attr_list атрибут не применит.
DESCRIPTION_ANCHOR = "article-overview"
# `data-status` — код статуса фичи: по нему скрипт theme-custom/javascripts/status-filter.js
# фильтрует перечень на странице (кнопки фильтра `data-filter` выводятся над перечнем).
LINK_ATTRS_TEMPLATE = '{{data-preview data-status="{status}"}}'

# Краткое описание страницы — первый абзац раздела «Описание» (поддерживается Markdown).
PAGE_DESCRIPTION = (
    "Карта функциональностей - иерархическое оглавление спецификаций продукта: "
    "**модуль -> субмодуль -> функциональность**. Название каждой функциональности - ссылка на раздел "
    "«Описание» её спецификации (при наведении курсора показывается предпросмотр). Перед названием стоит "
    "значок статуса, а в заголовках модулей и субмодулей указано число функциональностей по статусам. "
    "Актуальные и архивные функциональности выведены отдельными разделами; нужные статусы можно выбрать "
    "кнопками фильтра в разделе «Отбор функциональностей продукта»."
)
# Текст раздела «Отбор функциональностей продукта» и подсказка в поле отбора.
SELECTION_DESCRIPTION = (
    "Отбор (фильтрация) функциональностей {scope} как по текущему статусу функциональности, так и по названию "
    "{names}. При одновременном использовании отбора по статусу и названию "
    "отображается то, что подходит под оба условия."
)
# Страница карты: отбор по продукту целиком; страница модуля (index.md): отбор внутри модуля.
# Сообщение при пустом результате отбора: скрыто атрибутом `hidden`, показывает его status-filter.js.
# Кнопка «Сбросить» внутри (атрибут data-filter-reset) снимает фильтр по статусам и очищает поле поиска.
EMPTY_MESSAGE = "Нет данных, соответствующих условиям отбора"
SELECTION_PRODUCT = dict(scope="продукта", names="модуля, субмодуля, функциональности",
                         placeholder="Отбор по названию модуля или субмодуля или функциональности")
# Индекс архивного модуля: только отбор по названию, без кнопок статусов и «Сбросить»; свой текст раздела.
SELECTION_ARCHIVE = dict(description="Отбор (фильтрация) функциональностей модуля по названию субмодуля, функциональности.",
                         placeholder="Отбор по названию субмодуля или функциональности", reset=False)
SELECTION_MODULE = dict(scope="модуля", names="субмодуля, функциональности",
                        placeholder="Отбор по названию субмодуля или функциональности")

# Блок метаданных обязан стоять в самом начале файла между строками `---`.
FRONT_MATTER_RE = re.compile(
    r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
SPEC_KEYS = ("module", "submodule", "feature_name")

# ---------------------------------------------------------------------------
# Взаимосвязи фичей
# ---------------------------------------------------------------------------
# Метаданные спецификации:
#   relations:
#     depends_on: [auth-sms]                  # без неё эта фича не работает
#     extends:    [filter-categories]         # добавляет возможности уже работающей фиче
#     replaces:   [search-old]                # заменяет (обычно архивную) фичу
#     related:    [{feature: payment-sbp, note: "Соседний шаг оформления заказа"}]   # просто связана
# Элемент списка — имя файла спецификации без расширения либо набор `feature` + `note` (пояснение для таблицы).
RELATIONS_KEY = "relations"
RELATION_TYPES = ("depends_on", "extends", "replaces", "related")
RELATIONS_ANCHOR = "relations"
RELATIONS_TITLE = "Взаимосвязи"
# Маркеры раздела: всё между ними скрипт пересобирает при каждом запуске.
RELATIONS_BEGIN_PREFIX = "<!-- relations:start"
RELATIONS_BEGIN = ("<!-- relations:start — раздел формируется скриптом scripts/build_feature_map.py "
                   "по полю `relations` метаданных, не редактируйте его вручную -->")
RELATIONS_END = "<!-- relations:end -->"
# Подписи строк таблицы: (тип связи, направление) -> текст. «out» — связь объявлена в этой спецификации,
# «in» — её объявила другая спецификация (обратная связь, вычисляется).
RELATION_LABELS = {
    ("depends_on", "out"): "Зависит от",
    ("depends_on", "in"): "Используется в",
    ("extends", "out"): "Расширяет",
    ("extends", "in"): "Расширяется функциональностью",
    ("replaces", "out"): "Заменяет",
    ("replaces", "in"): "Заменена функциональностью",
    ("related", "out"): "Связана с",
    ("related", "in"): "Связана с",
}
# Порядок групп строк в таблице.
RELATION_ORDER = [("depends_on", "out"), ("depends_on", "in"), ("extends", "out"), ("extends", "in"),
                  ("replaces", "out"), ("replaces", "in"), ("related", "out")]
# Стрелка и подпись ребра на схеме Mermaid: стрелка идёт от субъекта связи к объекту
# («A зависит от B» -> A --> B), поэтому слева на схеме те, кто зависит от текущей фичи, справа — те, от кого зависит она.
RELATION_EDGES = {
    "depends_on": ("-->", "зависит от"),
    "extends": ("-.->", "расширяет"),
    "replaces": ("==>", "заменяет"),
    "related": ("-.-", "связана с"),
}
NO_RELATIONS_TEXT = "Связи с другими функциональностями в метаданных не заявлены."
# Размер шрифта на схеме Mermaid. Равен размеру шрифта таблиц темы (`.64rem` при корневом шрифте 20px = 12.8px),
# чтобы схема и таблица связей читались одинаково. Если в вашей теме шрифт таблиц другой, поменяйте значение здесь.
MERMAID_FONT_SIZE = "12.8px"
# Адреса страниц сайта: при use_directory_urls (по умолчанию) `a/b.md` публикуется как `a/b/`.
DIRECTORY_URLS = True


# Индексы папок (index.md): названия служебных папок для меню. Названия папок модулей берутся из поля `module`.
FOLDER_TITLES = {"specifications": "Спецификации", "archive": "Архив спецификаций"}
# Индекс раздела (вкладки верхнего меню): `docs/specifications/index.md` и `docs/archive/index.md`. Страница устроена как
# карта фичей, но показывает только спецификации своего раздела (по первой папке пути).
FOLDER_DESCRIPTIONS = {
    "specifications": "Действующие спецификации функциональностей продукта по модулям и субмодулям.",
    "archive": "Архивные спецификации: отклонённые и устаревшие функциональности продукта по модулям и субмодулям.",
}
SELECTION_SECTION = dict(scope="раздела", names="модуля, субмодуля, функциональности",
                         placeholder=SELECTION_PRODUCT["placeholder"])
SELECTION_SECTION_ARCHIVE = dict(
    description="Отбор (фильтрация) функциональностей раздела по названию модуля, субмодуля, функциональности.",
    placeholder=SELECTION_PRODUCT["placeholder"], reset=False)
INDEX_NAME = "index.md"
INDEX_MARKER = "scripts/build_feature_map.py"   # по этой строке скрипт узнаёт свои (сгенерированные) файлы
# Навигация (меню сайта): Zensical берёт названия папок из имён папок, поэтому меню собирается скриптом
# и записывается в zensical.toml между маркерами NAV_BEGIN и NAV_END.
DEFAULT_CONFIG = REPO_ROOT / "zensical.toml"
NAV_BEGIN = "# BEGIN GENERATED NAV (scripts/build_feature_map.py) — не редактируйте вручную"
NAV_END = "# END GENERATED NAV"
# Служебные страницы в начале меню: (название, файл относительно docs). Отсутствующие файлы пропускаются.
ROOT_PAGES = [
    ("О программном продукте", "index.md"),
    ("Карта функциональностей", "feature-map.md"),
    ("Глоссарий", "glossary.md"),
]
# ---------------------------------------------------------------------------
# Модель данных
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Relation:
    """Связь, объявленная в метаданных спецификации-источника."""
    kind: str          # ключ из RELATION_TYPES
    target: str        # имя файла (slug) целевой спецификации
    note: str = ""     # пояснение для таблицы (необязательно)


@dataclass(frozen=True)
class Feature:
    module: str
    submodule: str
    name: str
    link: str          # ссылка на раздел «Описание» относительно файла карты (с якорем)
    status: str        # ключ из STATUS_ICONS
    archived: bool
    path: str = ""    # путь файла относительно папки docs (posix)
    slug: str = ""    # имя файла без расширения: по нему фичи ссылаются друг на друга
    relations: tuple[Relation, ...] = ()

    @property
    def shown_status(self) -> str:
        """Статус, под которым фича показана в карте (архивные всегда `archived`)."""
        return "archived" if self.archived else self.status

    @property
    def icon(self) -> str:
        return STATUS_ICONS[self.shown_status]


class Problems:
    """Накопитель ошибок и предупреждений (выводятся в формате GitHub Actions)."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str) -> None:
        self.errors.append(message)
        self._print("error", path, message)

    def warning(self, path: Path, message: str) -> None:
        self.warnings.append(message)
        self._print("warning", path, message)

    @staticmethod
    def _print(level: str, path: Path, message: str) -> None:
        rel = _display(path)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::{level} file={rel}::{message}", file=sys.stderr)
        else:
            label = "ОШИБКА" if level == "error" else "Предупреждение"
            print(f"{label}: {rel}: {message}", file=sys.stderr)


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


# ---------------------------------------------------------------------------
# Чтение спецификаций
# ---------------------------------------------------------------------------

def read_front_matter(path: Path, problems: Problems) -> dict | None:
    """Возвращает метаданные файла или None, если блока метаданных нет."""
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        problems.error(path, f"некорректный YAML в метаданных: {exc}".replace("\n", " "))
        return None
    if data is None:
        return {}
    if not isinstance(data, dict):
        problems.error(path, "метаданные должны быть набором «ключ: значение»")
        return None
    return data


def clean(value: object) -> str:
    """Приводит значение метаданных к аккуратной строке."""
    return " ".join(str(value).split()) if value is not None else ""


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


def collect_features(
    docs_dir: Path, output: Path, archive_dir_name: str, problems: Problems
) -> list[Feature]:
    features: list[Feature] = []
    output = output.resolve()

    for path in sorted(docs_dir.rglob("*.md")):
        if path.resolve() == output:
            continue

        meta = read_front_matter(path, problems)
        if not meta or not any(key in meta for key in SPEC_KEYS):
            continue  # не спецификация фичи (глоссарий, главная и т. п.)

        module = clean(meta.get("module"))
        name = clean(meta.get("feature_name"))
        submodule = clean(meta.get("submodule")) or DEFAULT_SUBMODULE
        if not module:
            problems.error(path, "не заполнено обязательное поле `module`")
        if not name:
            problems.error(path, "не заполнено обязательное поле `feature_name`")
        if not module or not name:
            continue

        rel_to_docs = path.relative_to(docs_dir)
        in_archive_dir = archive_dir_name in rel_to_docs.parts[:-1]
        status = normalize_status(meta.get("status"), path, problems)
        archived = in_archive_dir or status == "archived"

        link = quote(os.path.relpath(path, output.parent).replace(os.sep, "/")) + f"#{DESCRIPTION_ANCHOR}"
        features.append(Feature(module, submodule, name, link, status, archived,
                                rel_to_docs.as_posix(), path.stem, parse_relations(meta, path, problems)))

    check_relations(docs_dir, features, problems)
    return features


# ---------------------------------------------------------------------------
# Формирование Markdown
# ---------------------------------------------------------------------------

def _sort_key(text: str) -> str:
    return text.casefold()


def _escape(text: str) -> str:
    return text.replace("[", r"\[").replace("]", r"\]")


def status_counts(features: list[Feature]) -> str:
    """Счётчики фич по значкам статусов, например `:lucide-inbox:: 3, :lucide-rocket:: 6`.

    Порядок — как в STATUS_ICONS; статусы без фич не выводятся.
    """
    parts = []
    for status, icon in STATUS_ICONS.items():
        count = sum(1 for f in features if f.shown_status == status)
        if count:
            parts.append(f"{icon}: {count}")
    return ", ".join(parts)


def render_tree(features: list[Feature], link=lambda f: f.link) -> list[str]:
    """Дерево «модуль -> субмодуль -> фича» со счётчиками статусов в заголовках модуля и субмодуля.

    Отступ 4 пробела (требование Python-Markdown). link — как получить адрес спецификации: по умолчанию относительно
    файла карты, для индексов разделов — относительно индекса.
    """
    tree: dict[str, dict[str, list[Feature]]] = defaultdict(lambda: defaultdict(list))
    for feature in features:
        tree[feature.module][feature.submodule].append(feature)

    lines: list[str] = []
    for module in sorted(tree, key=_sort_key):
        module_features = [f for subs in tree[module].values() for f in subs]
        lines.append(f"- **{_escape(module)}**: {status_counts(module_features)}")
        for submodule in sorted(tree[module], key=_sort_key):
            lines.append(f"    - *{_escape(submodule)}*: {status_counts(tree[module][submodule])}")
            for feature in sorted(tree[module][submodule], key=lambda f: _sort_key(f.name)):
                lines.append(
                    f"        - {feature.icon} [{_escape(feature.name)}]({link(feature)})"
                    + LINK_ATTRS_TEMPLATE.format(status=feature.shown_status)
                )
    return lines


def _statuses(only: list[str] | None = None, exclude: tuple[str, ...] = ()) -> list[str]:
    """Статусы для легенды, статистики и кнопок в порядке STATUS_ICONS.

    only — оставить только эти статусы, exclude — убрать указанные (в индексах модулей лишние статусы не выводятся).
    """
    return [s for s in STATUS_ICONS if (only is None or s in only) and s not in exclude]


def legend_block(statuses: list[str] | None = None) -> list[str]:
    """Инфо-блок «Статусы требований» (одна колонка с пояснениями), общий для карты и индексов модулей."""
    legend = [f"    - {STATUS_ICONS[s]} {STATUS_TITLES[s]}: {STATUS_DESCRIPTIONS[s]}" for s in _statuses(statuses)]
    return ['!!! info "Статусы требований"', "", *legend, ""]


def warning_block(page_file: str) -> list[str]:
    """Блок «Внимание»: какой файл показан на странице и что он формируется автоматически.

    page_file — путь к файлу относительно корня репозитория, например `docs/feature-map.md`.
    """
    name = page_file.rsplit("/", 1)[-1]
    return ['!!! warning "Внимание"', "",
            f"    На странице отображается содержимое файла `{page_file}`. Файл `{name}` формируется "
            "автоматически скриптом `scripts/build_feature_map.py` при каждом внесении изменений в ветку `main`. "
            f"Не редактируйте файл `{name}` вручную: правки будут перезаписаны.", ""]


def statistics_block(features: list[Feature], statuses: list[str] | None = None) -> list[str]:
    """Блок «Всего спецификаций: N» — две колонки по 3 статуса (класс `status-cols`, см. extra.css, раздел 4)."""
    counts = [f"    - {STATUS_ICONS[s]} {STATUS_TITLES[s]}: {sum(1 for f in features if f.shown_status == s)}"
              for s in _statuses(statuses)]
    return [f'!!! info status-cols "Всего спецификаций: {len(features)}"', "", *counts, ""]


def selection_block(texts: dict = SELECTION_PRODUCT, statuses: list[str] | None = None) -> list[str]:
    """Текст раздела «Отбор функциональностей продукта», кнопки статусов и поле отбора по названию.

    Кнопки — ссылки с классом `.md-button` (оформляет тема, см. документацию Zensical «Buttons»), поле — обычный
    HTML-элемент `input` (Markdown пропускает его без изменений). Клики и ввод обрабатывает
    theme-custom/javascripts/status-filter.js, вид поля задаёт extra.css, раздел 6.
    """
    buttons = [f'[{STATUS_ICONS[s]} {STATUS_TITLES[s]}](#){{ .md-button data-filter="{s}" }}' for s in _statuses(statuses)]
    if texts.get("reset", True):
        buttons.append('[Сбросить](#){ .md-button data-filter-reset="" }')
    search_field = (f'<input type="search" class="feature-search" data-feature-search="" autocomplete="off" '
                    f'placeholder="{texts["placeholder"]}" aria-label="{texts["placeholder"]}">')
    description = texts.get("description") or SELECTION_DESCRIPTION.format(**texts)
    # Одной строкой: так Markdown передаёт HTML-блок без изменений.
    empty = (f'<div class="feature-empty" data-feature-empty="" hidden><p>{EMPTY_MESSAGE}</p>'
             f'<p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>')
    return [description, "", *([*buttons, ""] if buttons else []), search_field, "", empty, ""]


def render_map(features: list[Feature], archive_dir_name: str) -> str:
    active = [f for f in features if not f.archived]
    archived = [f for f in features if f.archived]

    out: list[str] = [
        "# Карта функциональностей {#feature-map}",
        "",
        f"## Описание {{#{DESCRIPTION_ANCHOR}}}",
        "",
        PAGE_DESCRIPTION,
        "",
        *warning_block(f"docs/{DEFAULT_OUTPUT.name}"),
        *legend_block(),
        "## Статистика функциональностей продукта в разрезе статусов {#statistics}",
        "",
        *statistics_block(features),
        "## Отбор функциональностей продукта {#feature-selection}",
        "",
        *selection_block(),
        "## Актуальные функциональности {#active-features}",
        "",
    ]
    out += render_tree(active) if active else ["*Нет активных фичей*"]
    out += [
        "",
        "## Архивные функциональности {#archived-features}",
        "",
        f"> Спецификации из папки `docs/{archive_dir_name}/` или со статусом `archived`.",
        "",
    ]
    out += render_tree(archived) if archived else ["*Архив пуст*"]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Индексы папок
# ---------------------------------------------------------------------------

def _folder_title(folder: Path, folder_features: list[Feature], docs_dir: Path) -> str:
    """Название папки для меню: служебные папки — из FOLDER_TITLES, папки модулей — из поля `module`."""
    if folder.name in FOLDER_TITLES:
        return FOLDER_TITLES[folder.name]
    rel = folder.relative_to(docs_dir).as_posix()
    modules = [f.module for f in folder_features if f.path.startswith(rel + "/")]
    direct = [m for m, f in zip(modules, folder_features) if Path(f.path).parent == Path(rel)]
    pool = direct or modules
    return max(set(pool), key=pool.count) if pool else folder.name


def render_index(folder: Path, docs_dir: Path, features: list[Feature]) -> str:
    """Содержимое index.md папки модуля: описание, статусы, статистика и отбор (только по этому модулю) и список спецификаций."""
    direct = [f for f in features if (docs_dir / f.path).parent == folder]
    title = _folder_title(folder, features, docs_dir)
    slug = re.sub(r"[^a-z0-9]+", "-", folder.name.lower()).strip("-") or "folder"
    # Индекс модуля в архиве: только статус «архив» и без кнопок статусов; в действующих спецификациях статус «архив» не выводится.
    if DEFAULT_ARCHIVE_DIR_NAME in folder.relative_to(docs_dir).parts:
        legend_statuses, button_statuses, selection = ["archived"], [], SELECTION_ARCHIVE
    else:
        legend_statuses = button_statuses = _statuses(exclude=("archived",))
        selection = SELECTION_MODULE

    lines = [
        f"# {_escape(title)} {{#{slug}}}", "",
        f"## Описание {{#{DESCRIPTION_ANCHOR}}}", "",
        f"Спецификации модуля «{title}».", "",
        *warning_block(f"docs/{(folder / INDEX_NAME).relative_to(docs_dir).as_posix()}"),
        *legend_block(legend_statuses),
        "## Статистика функциональностей модуля в разрезе статусов {#statistics}", "",
        *statistics_block(direct, legend_statuses),
        "## Отбор функциональностей модуля {#feature-selection}", "",
        *selection_block(selection, button_statuses),
        "## Спецификации модуля {#specs}", "",
    ]
    by_sub: dict[str, list[Feature]] = defaultdict(list)
    for f in direct:
        by_sub[f.submodule].append(f)
    for sub in sorted(by_sub, key=_sort_key):
        lines.append(f"- *{_escape(sub)}*: {status_counts(by_sub[sub])}")
        for f in sorted(by_sub[sub], key=lambda x: _sort_key(x.name)):
            lines.append(f"    - {f.icon} [{_escape(f.name)}]({Path(f.path).name}#{DESCRIPTION_ANCHOR})"
                         + LINK_ATTRS_TEMPLATE.format(status=f.shown_status))
    return "\n".join(lines).rstrip() + "\n"


def render_section_index(tab: str, tab_features: list[Feature]) -> str:
    """Содержимое index.md раздела (вкладки меню): как карта фичей, но только по спецификациям этого раздела."""
    title = FOLDER_TITLES.get(tab, tab)
    slug = re.sub(r"[^a-z0-9]+", "-", tab.lower()).strip("-") or "section"
    if tab == DEFAULT_ARCHIVE_DIR_NAME:      # в архиве только статус «архив» и поиск по названию, без кнопок статусов
        legend_statuses, button_statuses, selection = ["archived"], [], SELECTION_SECTION_ARCHIVE
    else:
        legend_statuses = button_statuses = _statuses(exclude=("archived",))
        selection = SELECTION_SECTION
    to_spec = lambda f: quote(posixpath.relpath(f.path, tab)) + f"#{DESCRIPTION_ANCHOR}"
    lines = [
        f"# {_escape(title)} {{#{slug}}}", "",
        f"## Описание {{#{DESCRIPTION_ANCHOR}}}", "",
        FOLDER_DESCRIPTIONS.get(tab, f"Спецификации раздела «{title}»."), "",
        *warning_block(f"docs/{tab}/{INDEX_NAME}"),
        *legend_block(legend_statuses),
        "## Статистика функциональностей раздела в разрезе статусов {#statistics}", "",
        *statistics_block(tab_features, legend_statuses),
        "## Отбор функциональностей раздела {#feature-selection}", "",
        *selection_block(selection, button_statuses),
        "## Спецификации раздела {#specs}", "",
        *render_tree(tab_features, to_spec),
    ]
    return "\n".join(lines).rstrip() + "\n"


def section_tabs(features: list[Feature]) -> dict[str, list[Feature]]:
    """Спецификации по разделам: первая папка пути (specifications, archive)."""
    tabs: dict[str, list[Feature]] = defaultdict(list)
    for f in features:
        parts = Path(f.path).parts
        if len(parts) > 1:
            tabs[parts[0]].append(f)
    return tabs


def build_indexes(docs_dir: Path, features: list[Feature], problems: Problems) -> dict[Path, str]:
    """index.md для папок модулей (где спецификации лежат непосредственно) и для разделов (specifications, archive).

    Промежуточная папка archive/specifications индекса не получает: она избыточна.
    """
    folders = {(docs_dir / f.path).parent for f in features}
    result: dict[Path, str] = {}
    for folder in sorted(folders):
        target = folder / INDEX_NAME
        if target.exists() and INDEX_MARKER not in target.read_text(encoding="utf-8"):
            problems.warning(target, "файл создан вручную и не перезаписывается; удалите его, чтобы сформировать автоматически")
            continue
        result[target] = render_index(folder, docs_dir, features)

    for tab, tab_features in sorted(section_tabs(features).items()):
        target = docs_dir / tab / INDEX_NAME
        if target in result:
            problems.warning(target, f"спецификации лежат прямо в папке раздела `{tab}`: индекс раздела не создан")
        elif target.exists() and INDEX_MARKER not in target.read_text(encoding="utf-8"):
            problems.warning(target, "файл создан вручную и не перезаписывается; удалите его, чтобы сформировать автоматически")
        else:
            result[target] = render_section_index(tab, tab_features)
    return result


def stale_indexes(docs_dir: Path, wanted: dict[Path, str]) -> list[Path]:
    """Ранее сгенерированные index.md, которые больше не нужны (например, в корневых папках)."""
    return [p for p in sorted(docs_dir.rglob(INDEX_NAME))
            if p not in wanted and p.parent != docs_dir and INDEX_MARKER in p.read_text(encoding="utf-8")]


def _toml(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_nav(docs_dir: Path, features: list[Feature], wanted_indexes: dict[Path, str]) -> str:
    """Блок `nav = [...]` для zensical.toml: служебные страницы, затем вкладки по корневым папкам.

    Вкладка — первая папка пути (specifications, archive), раздел меню — модуль (папка со спецификациями),
    промежуточные папки пропускаются. Названия берутся из FOLDER_TITLES и поля `module`.
    """
    items = [f"    {{ {_toml(title)} = {_toml(page)} }}," for title, page in ROOT_PAGES if (docs_dir / page).exists()]

    folders = sorted({(docs_dir / f.path).parent for f in features})
    tabs: dict[str, list[Path]] = defaultdict(list)
    for folder in folders:
        tabs[folder.relative_to(docs_dir).parts[0]].append(folder)
    order = [k for k in FOLDER_TITLES if k in tabs] + sorted(k for k in tabs if k not in FOLDER_TITLES)

    for tab in order:
        sections = []
        tab_index = docs_dir / tab / INDEX_NAME        # индекс раздела: вкладка открывает его, группы меню свёрнуты
        if tab_index in wanted_indexes or tab_index.exists():
            sections.append(f"        {_toml(f'{tab}/{INDEX_NAME}')},")
        for folder in tabs[tab]:
            rel = folder.relative_to(docs_dir).as_posix()
            pages = [f for f in features if (docs_dir / f.path).parent == folder]
            title = _folder_title(folder, features, docs_dir)
            paths = ([f"{rel}/{INDEX_NAME}"] if (folder / INDEX_NAME) in wanted_indexes or (folder / INDEX_NAME).exists() else [])
            paths += [f.path for f in sorted(pages, key=lambda x: _sort_key(x.name))]
            body = ",\n".join(f"            {_toml(p)}" for p in paths)
            sections.append(f"        {{ {_toml(title)} = [\n{body},\n        ] }},")
        items.append(f"    {{ {_toml(FOLDER_TITLES.get(tab, tab))} = [\n" + "\n".join(sections) + "\n    ] },")
    return "nav = [\n" + "\n".join(items) + "\n]"


def sync_nav(config: Path, nav: str, check: bool, problems: Problems) -> bool:
    """Записывает nav между маркерами в zensical.toml. Возвращает True, если файл изменился (или устарел)."""
    if not config.exists():
        return False
    text = config.read_text(encoding="utf-8")
    block = f"{NAV_BEGIN}\n{nav}\n{NAV_END}"
    pattern = re.compile(re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END), re.DOTALL)
    if not pattern.search(text):
        problems.warning(config, f"нет маркеров `{NAV_BEGIN}` … `{NAV_END}`: меню не обновлено")
        return False
    new = pattern.sub(lambda _: block, text, count=1)
    if new == text:
        return False
    if not check:
        config.write_text(new, encoding="utf-8", newline="\n")
    return True


def sync_indexes(indexes: dict[Path, str], check: bool, stale: list[Path] = ()) -> tuple[int, int]:
    """Записывает индексы, удаляет лишние (или только проверяет). Возвращает (изменено, всего)."""
    changed = 0
    for path in stale:
        changed += 1
        if not check:
            path.unlink()
    for path, content in indexes.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        changed += 1
        if not check:
            path.write_text(content, encoding="utf-8", newline="\n")
    return changed, len(indexes)


# ---------------------------------------------------------------------------
# Взаимосвязи фичей: проверка, схема, таблица, раздел в спецификации
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Link:
    """Связь, показанная с точки зрения одной фичи: что за фича и в какую сторону направлена связь."""
    kind: str          # ключ из RELATION_TYPES
    direction: str     # out — объявлена в этой спецификации, in — в спецификации `other`
    other: Feature
    note: str = ""


def check_relations(docs_dir: Path, features: list[Feature], problems: Problems) -> None:
    """Проверяет связи: уникальность имён файлов, существование целей, связь на себя, циклы, архив."""
    by_slug: dict[str, Feature] = {}
    for f in features:
        if f.slug in by_slug:
            problems.error(docs_dir / f.path, f"имя файла `{f.slug}` уже занято спецификацией "
                                              f"{by_slug[f.slug].path}: ссылки на неё были бы неоднозначны")
        else:
            by_slug[f.slug] = f

    depends: dict[str, list[str]] = defaultdict(list)
    for f in features:
        path = docs_dir / f.path
        seen: set[tuple[str, str]] = set()
        for r in f.relations:
            if r.target == f.slug:
                problems.error(path, f"`{r.kind}`: фича не может ссылаться на саму себя")
                continue
            target = by_slug.get(r.target)
            if target is None:
                problems.error(path, f"`{r.kind}`: нет спецификации с именем файла `{r.target}`")
                continue
            if (r.kind, r.target) in seen:
                problems.warning(path, f"`{r.kind}`: связь с `{r.target}` указана дважды")
                continue
            seen.add((r.kind, r.target))
            if r.kind == "depends_on":
                depends[f.slug].append(r.target)
            if r.kind in ("depends_on", "extends") and target.archived and not f.archived:
                problems.warning(path, f"`{r.kind}`: действующая фича ссылается на архивную `{r.target}`")

    # Цикл в зависимостях (A зависит от B, B зависит от A): поиск в глубину.
    state: dict[str, int] = {}   # 1 — в обработке, 2 — готово

    def visit(slug: str, trail: list[str]) -> None:
        state[slug] = 1
        for nxt in depends.get(slug, []):
            if state.get(nxt) == 1:
                cycle = trail[trail.index(nxt):] + [nxt] if nxt in trail else [slug, nxt]
                problems.error(docs_dir / by_slug[slug].path,
                               "циклическая зависимость `depends_on`: " + " -> ".join(cycle))
            elif nxt not in state:
                visit(nxt, trail + [nxt])
        state[slug] = 2

    for slug in list(depends):
        if slug not in state:
            visit(slug, [slug])


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
    return sorted(found.values(), key=lambda l: (order[(l.kind, l.direction)], _sort_key(l.other.name)))


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
            f"| [{_table_cell(_escape(other.name))}]({href}#{DESCRIPTION_ANCHOR}){{data-preview}} "
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
_DESCRIPTION_RE = re.compile(r"^##\s+.*\{#" + re.escape(DESCRIPTION_ANCHOR) + r"\}\s*$")
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
            if _DESCRIPTION_RE.match(line):
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


def sync_relations(docs_dir: Path, features: list[Feature], check: bool, problems: Problems) -> int:
    """Обновляет раздел «Взаимосвязи» во всех спецификациях (или только проверяет). Возвращает число изменённых файлов."""
    by_slug, incoming = relation_index(features)
    changed = 0
    for f in features:
        path = docs_dir / f.path
        text = path.read_text(encoding="utf-8")
        new = place_relations_block(text, render_relations_block(f, feature_links(f, by_slug, incoming)))
        if new is None:
            problems.warning(path, f"нет раздела «Описание» с якорем `{{#{DESCRIPTION_ANCHOR}}}`: "
                                   f"раздел «{RELATIONS_TITLE}» не добавлен")
            continue
        if new != text:
            changed += 1
            if not check:
                path.write_text(new, encoding="utf-8", newline="\n")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Сборка карты фичей из спецификаций")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_DIR, help="папка со спецификациями")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="файл карты фичей")
    parser.add_argument("--archive-dir", default=DEFAULT_ARCHIVE_DIR_NAME, help="имя папки архива")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="zensical.toml с блоком меню (nav)")
    parser.add_argument("--check", action="store_true", help="не писать файл, а проверить его актуальность")
    args = parser.parse_args(argv)

    docs_dir = args.docs.resolve()
    if not docs_dir.is_dir():
        print(f"Папка не найдена: {docs_dir}", file=sys.stderr)
        return 1

    problems = Problems()
    features = collect_features(docs_dir, args.output, args.archive_dir, problems)
    if problems.errors:
        print(f"Карта не обновлена: ошибок в метаданных — {len(problems.errors)}.", file=sys.stderr)
        return 1

    content = render_map(features, args.archive_dir)
    current = args.output.read_text(encoding="utf-8") if args.output.exists() else None
    indexes = build_indexes(docs_dir, features, problems)
    stale = stale_indexes(docs_dir, indexes)
    nav = render_nav(docs_dir, features, indexes)

    if args.check:
        stale_idx, _ = sync_indexes(indexes, check=True, stale=stale)
        nav_stale = sync_nav(args.config, nav, True, problems)
        rel_stale = sync_relations(docs_dir, features, True, problems)
        if current != content or stale_idx or nav_stale or rel_stale:
            print("Карта фичей, индексы папок, меню или разделы «Взаимосвязи» устарели: запустите "
                  "scripts/build_feature_map.py "
                  f"(карта: {'устарела' if current != content else 'ок'}, индексов: {stale_idx}, "
                  f"меню: {'устарело' if nav_stale else 'ок'}, взаимосвязей в спецификациях: {rel_stale}).",
                  file=sys.stderr)
            return 1
        print("Карта фичей, индексы папок, меню и разделы «Взаимосвязи» актуальны.")
        return 0

    if current == content:
        print(f"Карта фичей без изменений ({len(features)} спецификаций).")
    else:
        args.output.write_text(content, encoding="utf-8", newline="\n")
        print(f"Карта фичей обновлена: {_display(args.output)} ({len(features)} спецификаций).")
    changed, total = sync_indexes(indexes, check=False, stale=stale)
    print(f"Индексы папок: изменено {changed} (всего {total}, удалено лишних {len(stale)}).")
    print("Меню (nav) обновлено." if sync_nav(args.config, nav, False, problems) else "Меню (nav) без изменений.")
    rel_changed = sync_relations(docs_dir, features, False, problems)
    print(f"Разделы «{RELATIONS_TITLE}» в спецификациях: изменено {rel_changed} (всего {len(features)}).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
