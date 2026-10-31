"""Этап 2. Проверка: структура и метаданные ВСЕХ спецификаций (включая архив) и настройки проекта.

Правила для метаданных и заголовков берутся из шаблона `templates/feature-spec-template.md` (см. template.py).
Проверка ничего не пишет на диск и собирает все замечания сразу, а не по первому. Ошибки останавливают сборку,
предупреждения — нет. Результат — список прочитанных файлов и проверенных фич для следующего этапа (generate).
"""

from __future__ import annotations

from ..models import BuildContext, Feature, Spec
from ..ordering import load_module_order
from ..problems import Problems
from ..reader import read_specs
from ..template import load_template
from .meta import build_features, check_release_dates, check_template_meta
from .project import check_manual_indexes, check_nav_markers, check_order
from .relations import check_relations
from .structure import check_structure


def validate_all(ctx: BuildContext, problems: Problems) -> tuple[list[Spec], list[Feature]]:
    """Читает спецификации и выполняет все проверки. Ошибки и предупреждения накапливаются в problems."""
    rules = load_template(ctx.template, problems)
    specs = read_specs(ctx.docs_dir, ctx.output, problems)
    features = build_features(specs, ctx, problems, rules)
    check_template_meta(specs, rules, problems)
    check_release_dates(features, problems, ctx.docs_dir)
    check_relations(ctx.docs_dir, features, problems)
    ctx.module_order[:] = load_module_order(ctx.nav_order, problems)
    check_order(features, ctx.module_order, ctx.docs_dir, ctx.nav_order, problems)
    check_nav_markers(ctx.config, problems)
    check_manual_indexes(ctx.docs_dir, features, problems)
    check_structure(specs, rules, ctx, problems)
    return specs, features
