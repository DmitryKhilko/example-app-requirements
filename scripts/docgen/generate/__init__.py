"""Этап 3. Генерация: карта фичей, индексы, меню, значки статуса и разделы «Взаимосвязи».

Генерация ничего не пишет на диск: она возвращает план (models.Plan) — какое содержимое должно получиться.
Записывает или сверяет с диском этап 4 (apply.py).
"""

from __future__ import annotations

from ..models import BuildContext, Feature, Plan, Spec
from .icons import plan_icons
from .nav import plan_nav, render_nav
from .pages import build_indexes, render_map, stale_indexes
from .relations import plan_relations


def build_plan(ctx: BuildContext, specs: list[Spec], features: list[Feature]) -> Plan:
    """Строит план записи по проверенным данным."""
    docs_dir = ctx.docs_dir
    indexes = build_indexes(ctx, features)
    nav = render_nav(docs_dir, features, indexes, ctx.module_order)

    # Значки и разделы «Взаимосвязи» меняют одни и те же файлы: связи считаются по тексту уже со значком.
    texts = {s.rel: s.text for s in specs}
    icons = plan_icons(features, texts)
    relations = plan_relations(features, {**texts, **icons})

    return Plan(
        map_path=ctx.output,
        map_content=render_map(features, ctx.module_order),
        indexes=indexes,
        stale_indexes=stale_indexes(docs_dir, indexes),
        nav_path=ctx.config if ctx.config.exists() else None,
        nav_content=plan_nav(ctx.config, nav),
        icons={docs_dir / rel: text for rel, text in icons.items()},
        relations={docs_dir / rel: text for rel, text in relations.items()},
        features_total=len(features),
    )
