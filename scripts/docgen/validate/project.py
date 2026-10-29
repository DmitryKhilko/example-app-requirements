"""Проверка настроек проекта: nav-order.yml, маркеры меню в zensical.toml, вручную созданные index.md."""

from __future__ import annotations

from pathlib import Path

from ..config import INDEX_NAME, NAV_BEGIN, NAV_END, NAV_RE, ORDER_KEY
from ..layout import is_manual_index, section_tabs, spec_folders
from ..models import Feature
from ..problems import Problems
from ..textutils import clean


def check_order(features: list[Feature], modules: list[str], docs_dir: Path, nav_order: Path, problems: Problems) -> None:
    """Предупреждения: модуль из nav-order.yml не найден; повторяется модуль; два одинаковых `order` в одной папке."""
    known = {clean(f.module) for f in features}
    for name in dict.fromkeys(modules):
        if name not in known:
            problems.warning(nav_order, f"модуль «{name}» не найден ни в одной спецификации (опечатка?)")
    for name in sorted({m for m in modules if modules.count(m) > 1}):
        problems.warning(nav_order, f"модуль «{name}» указан в списке несколько раз")
    seen: dict[tuple[Path, int], Feature] = {}
    for f in features:
        if f.order is None:
            continue
        key = ((docs_dir / f.path).parent, f.order)
        if key in seen:
            problems.warning(docs_dir / f.path, f"`{ORDER_KEY}: {f.order}` уже задан у `{seen[key].path}`: порядок этих страниц определит алфавит")
        else:
            seen[key] = f


def check_nav_markers(config: Path, problems: Problems) -> None:
    """В zensical.toml должны стоять маркеры блока меню: иначе сайт молча публиковался бы с устаревшим меню."""
    if config.exists() and not NAV_RE.search(config.read_text(encoding="utf-8")):
        problems.error(config, f"нет маркеров `{NAV_BEGIN}` … `{NAV_END}`: меню не обновлено")


def check_manual_indexes(docs_dir: Path, features: list[Feature], problems: Problems) -> None:
    """Предупреждения о вручную созданных index.md и о папке раздела, в которой спецификации лежат прямо в корне.

    Те же решения принимает генерация индексов (generate/pages.py): такие файлы она не перезаписывает.
    """
    generated: set[Path] = set()
    for folder in sorted(spec_folders(docs_dir, features)):
        target = folder / INDEX_NAME
        if is_manual_index(target):
            problems.warning(target, "файл создан вручную и не перезаписывается; удалите его, чтобы сформировать автоматически")
        else:
            generated.add(target)

    for tab in sorted(section_tabs(features)):
        target = docs_dir / tab / INDEX_NAME
        if target in generated:
            problems.warning(target, f"спецификации лежат прямо в папке раздела `{tab}`: индекс раздела не создан")
        elif is_manual_index(target):
            problems.warning(target, "файл создан вручную и не перезаписывается; удалите его, чтобы сформировать автоматически")
