#!/usr/bin/env python3
"""Генератор документации по метаданным спецификаций: карта фичей, индексы модулей и разделов, меню, взаимосвязи..

Тонкая точка входа: вся логика находится в пакете `scripts/docgen/` (описание структуры — в его __init__.py).

Запуск
------
    python scripts/generate_docs.py           # пересобрать карту, индексы, меню и разделы «Взаимосвязи»
    python scripts/generate_docs.py --check   # только проверить, что всё актуально
    python scripts/generate_docs.py --validate  # только проверить спецификации (метаданные, связи, структуру), ничего не писать

Код возврата 1 — ошибка в метаданных (нет `module` или `feature_name`, битый YAML, ошибки в `relations`)
либо, в режиме --check, что-то из сформированного устарело.
"""

import sys
from pathlib import Path

# Пакет docgen лежит рядом со скриптом; путь добавляем явно, чтобы запуск не зависел от режима интерпретатора.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from docgen.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
