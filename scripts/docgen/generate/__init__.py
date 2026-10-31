"""Этап 3. Генерация: «Обзор» реестра, индексы, меню, значки статуса, «Релизы» и разделы «Взаимосвязи».

Генерация ничего не пишет на диск: она возвращает план (models.Plan) — какое содержимое должно получиться.
Записывает или сверяет с диском этап 4 (apply.py).
"""

from __future__ import annotations

import posixpath

from ..config import OVERVIEW_PAGE, RELEASES_PAGE
from ..models import BuildContext, Feature, Plan, Spec
from .icons import plan_icons
from .nav import plan_nav, render_nav
from .pages import build_indexes, render_overview, stale_indexes
from .relations import plan_relations
from .releases import render_releases


def build_plan(ctx: BuildContext, specs: list[Spec], features: list[Feature]) -> Plan:
    """Строит план записи по проверенным данным."""
    docs_dir = ctx.docs_dir
    indexes = build_indexes(ctx, features)
    releases_path = docs_dir / RELEASES_PAGE
    # страница «Обзор» лежит там, куда указывает ctx.output (по умолчанию docs/registry/overview.md)
    try:
        overview_rel = ctx.output.relative_to(docs_dir).as_posix()
    except ValueError:
        overview_rel = OVERVIEW_PAGE
    nav = render_nav(docs_dir, features, indexes, ctx.module_order, generated=frozenset({ctx.output, releases_path}),
                     overview_page=overview_rel)

    # Значки и разделы «Взаимосвязи» меняют одни и те же файлы: связи считаются по тексту уже со значком.
    texts = {s.rel: s.text for s in specs}
    icons = plan_icons(features, texts)
    relations = plan_relations(features, {**texts, **icons})

    return Plan(
        map_path=ctx.output,
        map_content=render_overview(features, ctx.module_order, posixpath.dirname(overview_rel) or "."),
        indexes=indexes,
        stale_indexes=stale_indexes(docs_dir, indexes),
        nav_path=ctx.config if ctx.config.exists() else None,
        nav_content=plan_nav(ctx.config, nav),
        icons={docs_dir / rel: text for rel, text in icons.items()},
        relations={docs_dir / rel: text for rel, text in relations.items()},
        releases_path=releases_path,
        releases_content=render_releases(features, ctx.module_order),
        features_total=len(features),
    )
