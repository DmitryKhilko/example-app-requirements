"""Меню сайта: блок `nav` в zensical.toml между маркерами (Zensical берёт названия папок из имён папок).

Горизонтальное меню (вкладки): «Проект», «Реестр требований», «Релизы». Левое меню — содержимое выбранной вкладки.
"""

from __future__ import annotations

from pathlib import Path

from ..config import (INDEX_NAME, NAV_BEGIN, NAV_END, NAV_RE, OVERVIEW_MENU_TITLE, OVERVIEW_PAGE, PROJECT_MENU_TITLE,
                      PROJECT_PAGES, REGISTRY_MENU_TITLE, RELEASES_MENU_TITLE, RELEASES_PAGE, SECTION_TITLES)
from ..layout import folder_title, registry_sections
from ..models import Feature
from ..ordering import feature_key, module_key
from ..textutils import toml_str


def _page(indent: int, title: str, page: str) -> str:
    return f"{' ' * indent}{{ {toml_str(title)} = {toml_str(page)} }},"


def _group(indent: int, title: str, body: list[str]) -> str:
    pad = " " * indent
    return f"{pad}{{ {toml_str(title)} = [\n" + "\n".join(body) + f"\n{pad}] }},"


def render_nav(docs_dir: Path, features: list[Feature], wanted_indexes: dict[Path, str],
               module_order: list[str], generated: frozenset[Path] = frozenset(),
               overview_page: str = OVERVIEW_PAGE) -> str:
    """Блок `nav = [...]` для zensical.toml.

    * «Проект» — страницы PROJECT_PAGES («О продукте», «Глоссарий», «Roadmap»); первая открывается при щелчке на вкладке.
    * «Реестр требований» — «Обзор» (первая страница вкладки), затем подразделы «Действующие» и «Архив». Подраздел
      открывает свой индекс, а внутри него идут модули (папки со спецификациями) с их индексами и спецификациями.
      Названия подразделов — SECTION_TITLES, модулей — поле `module`; промежуточные папки пропускаются.
    * «Релизы» — страница releases.md.

    generated — файлы, которых ещё нет на диске, но которые будут созданы этой же сборкой (обзор, релизы): страница
    с таким файлом попадает в меню уже при первом запуске, а не при втором. Отсутствующие страницы пропускаются.
    """
    def exists(rel: str) -> bool:
        return (docs_dir / rel).exists() or docs_dir / rel in generated

    items: list[str] = []

    project = [_page(8, title, page) for title, page in PROJECT_PAGES if exists(page)]
    if project:
        items.append(_group(4, PROJECT_MENU_TITLE, project))

    registry: list[str] = []
    if exists(overview_page):
        registry.append(_page(8, OVERVIEW_MENU_TITLE, overview_page))

    for section, section_features in registry_sections(features).items():
        folders = sorted({(docs_dir / f.path).parent for f in section_features})
        # модули в меню — в порядке nav-order.yml (а не по именам папок); тот же порядок в «Действующих» и в «Архиве»
        folders.sort(key=lambda fo: module_key(folder_title(fo, features, docs_dir), module_order))
        body: list[str] = []
        section_index = docs_dir / section / INDEX_NAME     # индекс подраздела: пункт открывает его, модули свёрнуты
        if section_index in wanted_indexes or section_index.exists():
            body.append(f"            {toml_str(f'{section}/{INDEX_NAME}')},")
        for folder in folders:
            if folder == docs_dir / section:      # спецификации прямо в папке подраздела: отдельной группы нет
                body += [f"            {toml_str(f.path)}," for f in sorted(section_features, key=feature_key)
                         if (docs_dir / f.path).parent == folder]
                continue
            rel = folder.relative_to(docs_dir).as_posix()
            pages = [f for f in section_features if (docs_dir / f.path).parent == folder]
            paths = ([f"{rel}/{INDEX_NAME}"] if (folder / INDEX_NAME) in wanted_indexes or (folder / INDEX_NAME).exists() else [])
            paths += [f.path for f in sorted(pages, key=feature_key)]
            body.append(_group(12, folder_title(folder, features, docs_dir),
                               [f"                {toml_str(p)}," for p in paths]))
        title = SECTION_TITLES[section.rsplit("/", 1)[-1]]
        if body:
            registry.append(_group(8, title, body))
    if registry:
        items.append(_group(4, REGISTRY_MENU_TITLE, registry))

    if exists(RELEASES_PAGE):
        items.append(_page(4, RELEASES_MENU_TITLE, RELEASES_PAGE))

    return "nav = [\n" + "\n".join(items) + "\n]"


def plan_nav(config: Path, nav: str) -> str | None:
    """Новое содержимое zensical.toml: блок меню между маркерами заменён на `nav`.

    None — файла нет (или в нём нет маркеров: об этом сообщает проверка, validate/project.py).
    """
    if not config.exists():
        return None
    text = config.read_text(encoding="utf-8")
    block = f"{NAV_BEGIN}\n{nav}\n{NAV_END}"
    if not NAV_RE.search(text):
        return None
    return NAV_RE.sub(lambda _: block, text, count=1)
