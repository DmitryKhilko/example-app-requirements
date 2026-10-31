"""Точка входа: аргументы командной строки и последовательность этапов «чтение и проверка -> генерация -> применение»."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .apply import apply_plan
from .config import (DEFAULT_ARCHIVE_DIR_NAME, DEFAULT_CONFIG, DEFAULT_DOCS_DIR, DEFAULT_NAV_ORDER, DEFAULT_OUTPUT,
                     DEFAULT_TEMPLATE, ICON_KEY, RELATIONS_TITLE)
from .generate import build_plan
from .models import BuildContext
from .problems import Problems, display_path
from .validate import validate_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Сборка карты фичей из спецификаций")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_DIR, help="папка со спецификациями")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="файл карты фичей")
    parser.add_argument("--archive-dir", default=DEFAULT_ARCHIVE_DIR_NAME, help="имя папки архива")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="zensical.toml с блоком меню (nav)")
    parser.add_argument("--nav-order", type=Path, default=DEFAULT_NAV_ORDER, help="nav-order.yml с порядком модулей в меню")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE,
                        help="шаблон спецификации: из него берутся правила проверки метаданных и заголовков")
    parser.add_argument("--check", action="store_true", help="не писать файл, а проверить его актуальность")
    parser.add_argument("--validate", action="store_true",
                        help="только проверить спецификации (метаданные, связи, структура); ничего не писать")
    args = parser.parse_args(argv)
    if args.validate and args.check:
        parser.error("--validate и --check взаимоисключающие")

    docs_dir = args.docs.resolve()
    if not docs_dir.is_dir():
        print(f"Папка не найдена: {docs_dir}", file=sys.stderr)
        return 1

    ctx = BuildContext(docs_dir, args.output.resolve(), args.archive_dir, args.config, args.nav_order, args.template)
    problems = Problems()

    # Этап 1-2. Чтение и проверка
    specs, features = validate_all(ctx, problems)
    if problems.errors:
        if args.validate:
            print(f"Проверка не пройдена: ошибок — {len(problems.errors)}, предупреждений — {len(problems.warnings)}.",
                  file=sys.stderr)
        else:
            print(f"Карта не обновлена: ошибок — {len(problems.errors)}.", file=sys.stderr)
        return 1
    if args.validate:
        print(f"Проверка пройдена: спецификаций — {len(features)}, предупреждений — {len(problems.warnings)}.")
        return 0

    # Этап 3-4. Генерация и применение (или сверка при --check)
    plan = build_plan(ctx, specs, features)
    result = apply_plan(plan, check=args.check)

    if args.check:
        if result.outdated:
            print("Карта фичей, страница «Релизы», индексы папок, меню или разделы «Взаимосвязи» устарели: запустите "
                  "scripts/generate_docs.py "
                  f"(карта: {'устарела' if result.map_changed else 'ок'}, "
                  f"релизы: {'устарели' if result.releases_changed else 'ок'}, индексов: {result.indexes_changed}, "
                  f"меню: {'устарело' if result.nav_changed else 'ок'}, "
                  f"взаимосвязей в спецификациях: {result.relations_changed}, "
                  f"значков статуса в метаданных: {result.icons_changed}).",
                  file=sys.stderr)
            return 1
        print("Карта фичей, страница «Релизы», индексы папок, меню и разделы «Взаимосвязи» актуальны.")
        return 0

    if not result.map_changed:
        print(f"Карта фичей без изменений ({len(features)} спецификаций).")
    else:
        print(f"Карта фичей обновлена: {display_path(args.output)} ({len(features)} спецификаций).")
    print("Страница «Релизы» обновлена." if result.releases_changed else "Страница «Релизы» без изменений.")
    print(f"Индексы папок: изменено {result.indexes_changed} (всего {result.indexes_total}, "
          f"удалено лишних {result.stale_removed}).")
    print("Меню (nav) обновлено." if result.nav_changed else "Меню (nav) без изменений.")
    print(f"Значки статуса (`{ICON_KEY}`) в метаданных спецификаций: изменено {result.icons_changed}.")
    print(f"Разделы «{RELATIONS_TITLE}» в спецификациях: изменено {result.relations_changed} (всего {len(features)}).")
    return 0
