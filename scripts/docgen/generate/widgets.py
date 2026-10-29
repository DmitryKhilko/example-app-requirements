"""Элементы страниц-перечней: счётчики статусов, плитки-фильтры, строка отбора, сворачиваемые блоки, дерево."""

from __future__ import annotations

from collections import defaultdict

from ..config import (EMPTY_MESSAGE, LINK_ATTRS_TEMPLATE, STATUS_DESCRIPTIONS, STATUS_ICONS, STATUS_TITLES)
from ..models import Feature
from ..ordering import feature_key, module_key
from ..textutils import escape_md, sort_key


def status_keys(only: list[str] | None = None, exclude: tuple[str, ...] = ()) -> list[str]:
    """Статусы в порядке STATUS_ICONS: only — оставить только эти, exclude — убрать указанные."""
    return [s for s in STATUS_ICONS if (only is None or s in only) and s not in exclude]


def status_counts(features: list[Feature]) -> str:
    """Счётчики фич по значкам статусов, например `:lucide-inbox:: 3, :lucide-rocket:: 6`.

    Порядок — как в STATUS_ICONS; статусы без фич не выводятся. Каждый счётчик — `<span data-count-item>` с числом
    в `<span data-count>`: при отборе их пересчитывает status-filter.js (запятые между счётчиками рисует
    extra.css, раздел 9; без JavaScript страница показывает итоги без отбора).
    """
    parts = []
    for status, icon in STATUS_ICONS.items():
        count = sum(1 for f in features if f.shown_status == status)
        if count:
            parts.append(f'<span data-count-item="{status}">{icon}: <span data-count>{count}</span></span>')
    return " ".join(parts)


def _tree(features: list[Feature]) -> dict[str, dict[str, list[Feature]]]:
    tree: dict[str, dict[str, list[Feature]]] = defaultdict(lambda: defaultdict(list))
    for feature in features:
        tree[feature.module][feature.submodule].append(feature)
    return tree


def _block(kind: str, title_md: str, counts: str, body: list[str]) -> list[str]:
    """Сворачиваемый блок `<details>` (kind — `module` или `submodule`).

    Заголовок и счётчики статусов — в `<summary>`: название на первой строке, статистика (значки и числа) на второй. Атрибуты `markdown="block"` / `"span"` (md_in_html) нужны, чтобы
    Markdown внутри блока обрабатывался: список функциональностей и значки статусов (:lucide-…:). Блок закрыт по умолчанию;
    открывать и закрывать его, а также раскрывать совпадения при отборе будет status-filter.js.
    """
    return [f'<details class="feature-block feature-{kind}" markdown="block">',
            f'<summary markdown="span"><span class="feature-title">{title_md}</span>'
            f'<span class="feature-counts">{counts}</span></summary>', "", *body, "", "</details>", ""]


def _feature_lines(features: list[Feature], link) -> list[str]:
    return [f"- {f.icon} [{escape_md(f.name)}]({link(f)})" + LINK_ATTRS_TEMPLATE.format(status=f.shown_status)
            for f in sorted(features, key=feature_key)]


def render_tree(features: list[Feature], module_order: list[str], link=lambda f: f.link,
                with_modules: bool = True) -> list[str]:
    """Иерархия «модуль -> субмодуль -> функциональность» в виде вложенных сворачиваемых блоков.

    Заголовки модуля и субмодуля содержат счётчики статусов. with_modules=False — для страницы одного модуля:
    блоки только по субмодулям. module_order — порядок модулей из nav-order.yml. link — как получить адрес спецификации: по умолчанию относительно файла карты,
    для индексов — относительно индекса.
    """
    lines: list[str] = []
    for module in sorted(_tree(features), key=lambda m: module_key(m, module_order)):
        subs = _tree(features)[module]
        sub_blocks: list[str] = []
        for submodule in sorted(subs, key=sort_key):
            sub_blocks += _block("submodule", f"*{escape_md(submodule)}*", status_counts(subs[submodule]),
                                 _feature_lines(subs[submodule], link))
        if with_modules:
            module_features = [f for items in subs.values() for f in items]
            lines += _block("module", f"**{escape_md(module)}**", status_counts(module_features), sub_blocks)
        else:
            lines += sub_blocks
    return lines


def tiles_block(features: list[Feature], statuses: list[str]) -> list[str]:
    """Плитки статистики: сверху на всю ширину плитка «Всего спецификаций» (общий итог, не кнопка), ниже сетка плиток
    статусов одной высоты и ширины: значок и число, под ними название статуса.

    Плитка — кнопка фильтра по статусу (атрибут data-filter; выбор нескольких, выбранные подсвечиваются). Подсказок
    (tooltip) у плиток нет: статусы поясняет инфо-блок «Статусы спецификаций». Число в `<span data-stat>` пересчитывает
    status-filter.js при отборе. Вид плиток — extra.css, раздел 4.
    """
    tiles = [f'[<span class="status-top">{STATUS_ICONS[s]} '
             f'<span data-stat="{s}">{sum(1 for f in features if f.shown_status == s)}</span></span>'
             f'<span class="status-name">{STATUS_TITLES[s]}</span>](#)'
             f'{{ .status-tile data-filter="{s}" aria-label="{STATUS_TITLES[s]}" }}' for s in statuses]
    # Общий итог — обычный элемент (не ссылка), поэтому фильтром не является; число пересчитывает status-filter.js.
    total = (f'<div class="status-total" markdown="span">:lucide-files: <span class="status-name">Всего спецификаций</span> '
             f'<span data-stat-total>{len(features)}</span></div>')
    # data-n — число плиток статусов: по нему extra.css выбирает число колонок сетки (раздел 4)
    return [total, "", f'<div class="status-tiles" data-n="{len(statuses)}" markdown>', "", *tiles, "", "</div>", ""]


def filter_block(placeholder: str) -> list[str]:
    """Строка отбора по названию с кнопкой «Сбросить» (под плитками) и сообщение при пустом результате.

    Поле — обычный HTML-элемент `input` (Markdown пропускает его без изменений), кнопка — ссылка с классом `.md-button`
    (оформляет тема, см. документацию Zensical «Buttons»). Ввод и клики обрабатывает status-filter.js.
    «Сбросить» снимает выбор плиток и очищает поле. Сообщение «Нет данных…» скрыто атрибутом `hidden`, показывает его
    status-filter.js; своей кнопки у него нет: достаточно «Сбросить» рядом с полем.
    """
    field = (f'<input type="search" class="feature-search" data-feature-search="" autocomplete="off" '
             f'placeholder="{placeholder}" aria-label="{placeholder}">')
    empty = f'<div class="feature-empty" data-feature-empty="" hidden><p>{EMPTY_MESSAGE}</p></div>'
    return ['<div class="feature-filter" markdown>', "", field, "",
            '[Сбросить](#){ .md-button data-filter-reset="" }', "", "</div>", "", empty, ""]


def statuses_info(statuses: list[str]) -> list[str]:
    """Свёрнутый инфо-блок «Статусы спецификаций»: каждый статус в строке «значок название: пояснение».

    Выводятся статусы, плитки которых есть на странице (на странице архива — только «архив»). Блок `??? info` свёрнут
    по умолчанию (расширение pymdownx.details). Тексты — STATUS_TITLES и STATUS_DESCRIPTIONS.
    """
    rows = [f"    - {STATUS_ICONS[s]} {STATUS_TITLES[s]}: {STATUS_DESCRIPTIONS[s]}" for s in statuses]
    return ['??? info "Статусы спецификаций"', "", *rows, ""]


def statistics_section(features: list[Feature], statuses: list[str], placeholder: str) -> list[str]:
    """Раздел «Статистика»: инфо-блок «Статусы спецификаций», плитки-фильтры, строка отбора и «Сбросить»."""
    return ["## Статистика {#statistics}", "", *statuses_info(statuses), *tiles_block(features, statuses),
            *filter_block(placeholder)]
