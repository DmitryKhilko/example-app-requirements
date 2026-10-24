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
  `archived`. В карте такие фичи выводятся в отдельном разделе со значком 📦.
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

# Статусы в терминах репозитория (см. [project.extra.status] в zensical.toml).
# Порядок важен: в таком порядке статусы идут в легенде и статистике.
STATUS_ICONS = {
    "published": "🟢",
    "review": "⏳",
    "draft": "📋",
    "archived": "📦",
}
STATUS_TITLES = {
    "published": "опубликовано",
    "review": "на проверке",
    "draft": "черновик",
    "archived": "архив",
}
# Синонимы: допускаются русские статусы из исходной концепции Feature Map.
STATUS_ALIASES = {
    "готово": "published",
    "в разработке": "review",
    "бэклог": "draft",
    "архив": "archived",
}
DEFAULT_STATUS = "draft"
DEFAULT_SUBMODULE = "Общее"

# Блок метаданных обязан стоять в самом начале файла между строками `---`.
FRONT_MATTER_RE = re.compile(
    r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
SPEC_KEYS = ("module", "submodule", "feature_name")


# ---------------------------------------------------------------------------
# Модель данных
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Feature:
    module: str
    submodule: str
    name: str
    link: str          # ссылка на спецификацию относительно файла карты
    status: str        # ключ из STATUS_ICONS
    archived: bool

    @property
    def icon(self) -> str:
        return STATUS_ICONS["archived"] if self.archived else STATUS_ICONS[self.status]


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

        link = quote(os.path.relpath(path, output.parent).replace(os.sep, "/"))
        features.append(Feature(module, submodule, name, link, status, archived))

    return features


# ---------------------------------------------------------------------------
# Формирование Markdown
# ---------------------------------------------------------------------------

def _sort_key(text: str) -> str:
    return text.casefold()


def _escape(text: str) -> str:
    return text.replace("[", r"\[").replace("]", r"\]")


def render_tree(features: list[Feature]) -> list[str]:
    """Дерево «модуль -> субмодуль -> фича». Отступ 4 пробела (требование Python-Markdown)."""
    tree: dict[str, dict[str, list[Feature]]] = defaultdict(lambda: defaultdict(list))
    for feature in features:
        tree[feature.module][feature.submodule].append(feature)

    lines: list[str] = []
    for module in sorted(tree, key=_sort_key):
        lines.append(f"- **{_escape(module)}**")
        for submodule in sorted(tree[module], key=_sort_key):
            lines.append(f"    - *{_escape(submodule)}*")
            for feature in sorted(tree[module][submodule], key=lambda f: _sort_key(f.name)):
                lines.append(f"        - {feature.icon} [{_escape(feature.name)}]({feature.link})")
    return lines


def render_map(features: list[Feature], archive_dir_name: str) -> str:
    active = [f for f in features if not f.archived]
    archived = [f for f in features if f.archived]

    counts = [f"{STATUS_ICONS[s]} {sum(1 for f in active if f.status == s)}"
              for s in ("published", "review", "draft")]
    counts.append(f"{STATUS_ICONS['archived']} {len(archived)}")
    legend = " · ".join(f"{STATUS_ICONS[s]} {STATUS_TITLES[s]}" for s in STATUS_ICONS)

    out: list[str] = [
        "# 🗺️ Карта фичей продукта",
        "",
        "> Файл формируется автоматически скриптом `scripts/build_feature_map.py` "
        "при слиянии изменений в ветку `main`. Не редактируйте его вручную: "
        "правки будут перезаписаны.",
        "",
        f"Всего спецификаций: **{len(features)}** · " + " · ".join(counts),
        "",
        f"Обозначения: {legend}",
        "",
        "## 🚀 Активные фичи",
        "",
    ]
    out += render_tree(active) if active else ["*Нет активных фичей*"]
    out += [
        "",
        "## 📦 Архив фичей",
        "",
        f"> Спецификации из папки `docs/{archive_dir_name}/` или со статусом `archived`.",
        "",
    ]
    out += render_tree(archived) if archived else ["*Архив пуст*"]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

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

    if args.check:
        if current != content:
            print(f"Карта фичей устарела: запустите scripts/build_feature_map.py ({_display(args.output)}).",
                  file=sys.stderr)
            return 1
        print("Карта фичей актуальна.")
        return 0

    if current == content:
        print(f"Карта фичей без изменений ({len(features)} спецификаций).")
    else:
        args.output.write_text(content, encoding="utf-8", newline="\n")
        print(f"Карта фичей обновлена: {_display(args.output)} ({len(features)} спецификаций).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
