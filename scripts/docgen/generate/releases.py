"""Страница «Релизы» (docs/releases.md): сворачиваемый блок на каждый релиз со списком вошедших спецификаций."""

from __future__ import annotations

import re
from collections import defaultdict

from ..config import GENERATED_COMMENT, LINK_ATTRS_TEMPLATE, NO_RELEASES_TEXT, PAGE_FRONT_MATTER, RELEASES_ANCHOR
from ..models import Feature
from ..ordering import feature_key, module_key
from ..textutils import escape_md


def release_key(release: str) -> tuple[int, ...]:
    """Ключ сортировки номера релиза: числа через точку сравниваются как числа (1.10.0 новее 1.9.0)."""
    return tuple(int(part) for part in re.findall(r"\d+", release))


def _plural_specs(n: int) -> str:
    """«1 спецификация», «2 спецификации», «5 спецификаций»."""
    if n % 10 == 1 and n % 100 != 11:
        word = "спецификация"
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        word = "спецификации"
    else:
        word = "спецификаций"
    return f"{n} {word}"


def _indent(text: str) -> list[str]:
    """Описание как продолжение элемента списка: каждая строка со сдвигом на 4 пробела."""
    return [("    " + line) if line.strip() else "" for line in text.split("\n")]


def _spec_item(f: Feature) -> list[str]:
    """Элемент списка: значок статуса и ссылка на спецификацию (название), под ней описание из раздела «Описание»."""
    attrs = LINK_ATTRS_TEMPLATE.format(status=f.shown_status)
    if f.spec_id:
        attrs = attrs[:-1] + f' data-id="{f.spec_id}"}}'      # код спецификации попадает в текстовый файл
    lines = [f"- {f.icon} [{escape_md(f.name)}]({f.link})" + attrs, ""]
    if f.description:
        lines += _indent(f.description) + [""]
    return lines


def _block(release: str, items: list[Feature], module_order: list[str]) -> list[str]:
    """Сворачиваемый блок релиза (те же классы, что у блоков модулей на карте функциональностей).

    В панели: кнопка «Скачать в текстовый файл» (её обрабатывает releases.js; текст файла он собирает из самой панели)
    и список спецификаций релиза.
    """
    body = ['<div class="release-actions" markdown>', "",
            f'[:lucide-download: Скачать в текстовый файл](#){{ .md-button data-release-download="{release}" }}',
            "", "</div>", ""]
    for f in sorted(items, key=lambda f: (module_key(f.module, module_order), feature_key(f))):
        body += _spec_item(f)
    return [f'<details class="feature-block feature-module release-block" data-release="{release}" markdown="block">',
            f'<summary markdown="span"><span class="feature-title">**Релиз {release}**</span>'
            f'<span class="feature-counts">{_plural_specs(len(items))}</span></summary>', "", *body, "</details>", ""]


def render_releases(features: list[Feature], module_order: list[str]) -> str:
    """Содержимое docs/releases.md: релизы от новых к старым; в релиз входят спецификации с заполненным `relise_id`.

    Внутри релиза спецификации идут по модулям (порядок nav-order.yml), затем по полю `order` и названию."""
    by_release: dict[str, list[Feature]] = defaultdict(list)
    for f in features:
        if f.release:
            by_release[f.release].append(f)

    out: list[str] = [
        *PAGE_FRONT_MATTER,
        f"# Релизы продукта {{#{RELEASES_ANCHOR}}}",
        "",
        GENERATED_COMMENT,
        "",
        "## Список релизов {#release-list}",
        "",
    ]
    if by_release:
        out += ["Релизы идут от новых к старым. Откройте релиз, чтобы увидеть вошедшие в него спецификации; "
                "список релиза можно скачать в текстовый файл.", ""]
        for release in sorted(by_release, key=release_key, reverse=True):
            out += _block(release, by_release[release], module_order)
    else:
        out += [NO_RELEASES_TEXT, ""]
    return "\n".join(out).rstrip() + "\n"
