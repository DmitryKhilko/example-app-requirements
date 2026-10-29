"""Этап 2. Проверка: структура и метаданные ВСЕХ спецификаций (включая архив) и настройки проекта.

Проверка ничего не пишет на диск и собирает все замечания сразу, а не по первому. Ошибки останавливают сборку,
предупреждения — нет. Результат — список прочитанных файлов и проверенных фич для следующего этапа (generate).
"""

from __future__ import annotations

from ..models import BuildContext, Feature, Spec
from ..ordering import load_module_order
from ..problems import Problems
from ..reader import read_specs
from .meta import build_features
from .project import check_manual_indexes, check_nav_markers, check_order
from .relations import check_relations
from .structure import check_structure


def validate_all(ctx: BuildContext, problems: Problems) -> tuple[list[Spec], list[Feature]]:
    """Читает спецификации и выполняет все проверки. Ошибки и предупреждения накапливаются в problems."""
    specs = read_specs(ctx.docs_dir, ctx.output, problems)
    features = build_features(specs, ctx, problems)
    check_relations(ctx.docs_dir, features, problems)
    ctx.module_order[:] = load_module_order(ctx.nav_order, problems)
    check_order(features, ctx.module_order, ctx.docs_dir, ctx.nav_order, problems)
    check_nav_markers(ctx.config, problems)
    check_manual_indexes(ctx.docs_dir, features, problems)
    check_structure(specs, features, ctx, problems)
    return specs, features
