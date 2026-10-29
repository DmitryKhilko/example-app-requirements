"""Проверка связей между спецификациями: цели, самоссылки, неизвестные типы, повторы, циклы, архив."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ..models import Feature
from ..problems import Problems


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