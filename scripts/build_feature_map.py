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

Запуск
------
    python scripts/build_feature_map.py           # пересобрать карту
    python scripts/build_feature_map.py --check   # только проверить, что карта актуальна

Код возврата 1 — ошибка в метаданных (нет `module` или `feature_name`, битый YAML)
либо, в режиме --check, карта устарела.
"""

from __future__ import annotations

import argparse
import os
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
    "Перечень функциональностей — иерархическое оглавление спецификаций продукта: "
    "**модуль → субмодуль → функциональность**. Название каждой функциональности — ссылка на раздел "
    "«Описание» её спецификации (при наведении курсора показывается предпросмотр). Перед названием стоит "
    "значок статуса, а в заголовках модулей и субмодулей указано число функциональностей по статусам. "
    "Актуальные и архивные функциональности выведены отдельными разделами; нужные статусы можно выбрать "
    "кнопками фильтра в разделе «Статистика»."
)

# Блок метаданных обязан стоять в самом начале файла между строками `---`.
FRONT_MATTER_RE = re.compile(
    r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
SPEC_KEYS = ("module", "submodule", "feature_name")


# Индексы папок (index.md): названия служебных папок для меню. Названия папок модулей берутся из поля `module`.
FOLDER_TITLES = {"specifications": "Спецификации", "archive": "Архив"}
INDEX_NAME = "index.md"
# Блок «Внимание» в разделе «Описание» каждого индекса (admonition, тело — отступ 4 пробела).
INDEX_WARNING = [
    '!!! warning "Внимание"',
    "",
    "    Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку "
    "`main`. Не редактируйте его вручную: правки будут перезаписаны.",
    "",
]

# ---------------------------------------------------------------------------
# Модель данных
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Feature:
    module: str
    submodule: str
    name: str
    link: str          # ссылка на раздел «Описание» относительно файла карты (с якорем)
    status: str        # ключ из STATUS_ICONS
    archived: bool
    path: str = ""    # путь файла относительно папки docs (posix)

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
                                rel_to_docs.as_posix()))

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


def render_tree(features: list[Feature]) -> list[str]:
    """Дерево «модуль -> субмодуль -> фича» со счётчиками статусов в заголовках модуля и субмодуля.

    Отступ 4 пробела (требование Python-Markdown).
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
                    f"        - {feature.icon} [{_escape(feature.name)}]({feature.link})"
                    + LINK_ATTRS_TEMPLATE.format(status=feature.shown_status)
                )
    return lines


def render_map(features: list[Feature], archive_dir_name: str) -> str:
    active = [f for f in features if not f.archived]
    archived = [f for f in features if f.archived]

    # Сводка выводится двумя обычными блоками admonition (`!!! info`): «Обозначения» — в разделе
    # «Описание», «Всего спецификаций» — в разделе «Статистика». Тело блока — отступ 4 пробела.
    # Модификатор `inline` не используется: такие блоки «плавают» сбоку и сужают страницу.
    # «Обозначения» — одна колонка с пояснениями. «Всего спецификаций» — две колонки по 3 статуса: класс
    # `status-cols` (после типа блока) включает их правилом из theme-custom/stylesheets/extra.css, раздел 4.
    legend = [f"    - {STATUS_ICONS[s]} {STATUS_TITLES[s]}: {STATUS_DESCRIPTIONS[s]}" for s in STATUS_ICONS]
    # Кнопки фильтра по статусам: ссылки с классом `.md-button` (оформляет тема, см. документацию
    # Zensical «Buttons»). Клики обрабатывает theme-custom/javascripts/status-filter.js.
    filter_buttons = [f'[{STATUS_ICONS[s]} {STATUS_TITLES[s]}](#){{ .md-button data-filter="{s}" }}'
                      for s in STATUS_ICONS]
    filter_buttons.append('[Сбросить](#){ .md-button data-filter-reset="" }')
    counts = [f"    - {STATUS_ICONS[s]} {STATUS_TITLES[s]}: {sum(1 for f in active if f.status == s)}"
              for s in STATUS_ICONS if s != "archived"]
    counts.append(f"    - {STATUS_ICONS['archived']} {STATUS_TITLES['archived']}: {len(archived)}")

    out: list[str] = [
        "# Перечень функциональностей продукта {#feature-map}",
        "",
        f"## Описание {{#{DESCRIPTION_ANCHOR}}}",
        "",
        PAGE_DESCRIPTION,
        "",
        "> Файл формируется автоматически скриптом `scripts/build_feature_map.py` "
        "при слиянии изменений в ветку `main`. Не редактируйте его вручную: "
        "правки будут перезаписаны.",
        "",
        '!!! info "Обозначения"',
        "",
        *legend,
        "",
        "## Статистика {#statistics}",
        "",
        f'!!! info status-cols "Всего спецификаций: {len(features)}"',
        "",
        *counts,
        "",
        "**Фильтр по статусу:**",
        "",
        *filter_buttons,
        "",
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
    """Содержимое index.md папки: описание и список вложенных папок либо спецификаций."""
    rel = folder.relative_to(docs_dir).as_posix()
    inside = [f for f in features if f.path.startswith(rel + "/")]
    title = _folder_title(folder, inside, docs_dir)
    slug = re.sub(r"[^a-z0-9]+", "-", folder.name.lower()).strip("-") or "folder"

    direct = [f for f in inside if Path(f.path).parent == Path(rel)]
    subfolders = sorted({Path(f.path).relative_to(rel).parts[0] for f in inside if f not in direct})

    lines = [f"# {_escape(title)} {{#{slug}}}", "", f"## Описание {{#{DESCRIPTION_ANCHOR}}}", ""]
    if subfolders:
        lines += [f"Раздел «{title}» содержит вложенные разделы. Счётчики показывают число спецификаций "
                  "по статусам.", "", *INDEX_WARNING, f"## Разделы {{#sections}}", ""]
        for name in subfolders:
            sub = folder / name
            sub_features = [f for f in inside if f.path.startswith(f"{rel}/{name}/")]
            sub_title = _folder_title(sub, features, docs_dir)
            lines.append(f"- [{_escape(sub_title)}]({name}/{INDEX_NAME}#{DESCRIPTION_ANCHOR})"
                         f"{{data-preview}}: {status_counts(sub_features)}")
    if direct:
        lines += [f"Спецификации раздела «{title}»: всего {len(direct)}.", "", *INDEX_WARNING,
                  "## Спецификации {#specs}", ""]
        by_sub: dict[str, list[Feature]] = defaultdict(list)
        for f in direct:
            by_sub[f.submodule].append(f)
        for sub in sorted(by_sub, key=_sort_key):
            lines.append(f"- *{_escape(sub)}*: {status_counts(by_sub[sub])}")
            for f in sorted(by_sub[sub], key=lambda x: _sort_key(x.name)):
                lines.append(f"    - {f.icon} [{_escape(f.name)}]({Path(f.path).name}#{DESCRIPTION_ANCHOR})"
                             + LINK_ATTRS_TEMPLATE.format(status=f.shown_status))
    return "\n".join(lines).rstrip() + "\n"


def build_indexes(docs_dir: Path, features: list[Feature], problems: Problems) -> dict[Path, str]:
    """index.md для каждой папки со спецификациями и для всех её родителей внутри docs (кроме самой docs)."""
    folders: set[Path] = set()
    for f in features:
        parent = (docs_dir / f.path).parent
        while parent != docs_dir:
            folders.add(parent)
            parent = parent.parent

    result: dict[Path, str] = {}
    for folder in sorted(folders):
        target = folder / INDEX_NAME
        if target.exists() and "scripts/build_feature_map.py" not in target.read_text(encoding="utf-8"):
            problems.warning(target, "файл создан вручную и не перезаписывается; удалите его, чтобы сформировать автоматически")
            continue
        result[target] = render_index(folder, docs_dir, features)
    return result


def sync_indexes(indexes: dict[Path, str], check: bool) -> tuple[int, int]:
    """Записывает индексы (или проверяет их). Возвращает (изменено, всего)."""
    changed = 0
    for path, content in indexes.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        changed += 1
        if not check:
            path.write_text(content, encoding="utf-8", newline="\n")
    return changed, len(indexes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Сборка карты фичей из спецификаций")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_DIR, help="папка со спецификациями")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="файл карты фичей")
    parser.add_argument("--archive-dir", default=DEFAULT_ARCHIVE_DIR_NAME, help="имя папки архива")
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

    if args.check:
        stale_idx, _ = sync_indexes(indexes, check=True)
        if current != content or stale_idx:
            print("Карта фичей или индексы папок устарели: запустите scripts/build_feature_map.py "
                  f"({_display(args.output)}, индексов: {stale_idx}).", file=sys.stderr)
            return 1
        print("Карта фичей и индексы папок актуальны.")
        return 0

    if current == content:
        print(f"Карта фичей без изменений ({len(features)} спецификаций).")
    else:
        args.output.write_text(content, encoding="utf-8", newline="\n")
        print(f"Карта фичей обновлена: {_display(args.output)} ({len(features)} спецификаций).")
    changed, total = sync_indexes(indexes, check=False)
    print(f"Индексы папок: обновлено {changed} из {total}.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
