"""Меню сайта: блок `nav` в zensical.toml между маркерами (Zensical берёт названия папок из имён папок)."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ..config import FOLDER_TITLES, INDEX_NAME, NAV_BEGIN, NAV_END, NAV_RE, ROOT_PAGES
from ..layout import folder_title
from ..models import Feature
from ..ordering import feature_key, module_key
from ..textutils import toml_str


def render_nav(docs_dir: Path, features: list[Feature], wanted_indexes: dict[Path, str],
               module_order: list[str], generated: frozenset[Path] = frozenset()) -> str:
    """Блок `nav = [...]` для zensical.toml: служебные страницы, затем вкладки по корневым папкам.

    Вкладка — первая папка пути (specifications, archive), раздел меню — модуль (папка со спецификациями),
    промежуточные папки пропускаются. Названия берутся из FOLDER_TITLES и поля `module`.
    generated — файлы, которых ещё нет на диске, но которые будут созданы этой же сборкой (карта фичей): служебная
    страница с таким файлом попадает в меню уже при первом запуске, а не при втором.
    """
    items = [f"    {{ {toml_str(title)} = {toml_str(page)} }},"
             for title, page in ROOT_PAGES if (docs_dir / page).exists() or docs_dir / page in generated]

    folders = sorted({(docs_dir / f.path).parent for f in features})
    # модули в меню — в порядке nav-order.yml (а не по именам папок); тот же порядок в «Спецификациях» и в архиве
    folders.sort(key=lambda fo: module_key(folder_title(fo, features, docs_dir), module_order))
    tabs: dict[str, list[Path]] = defaultdict(list)
    for folder in folders:
        tabs[folder.relative_to(docs_dir).parts[0]].append(folder)
    order = [k for k in FOLDER_TITLES if k in tabs] + sorted(k for k in tabs if k not in FOLDER_TITLES)

    for tab in order:
        sections = []
        tab_index = docs_dir / tab / INDEX_NAME        # индекс раздела: вкладка открывает его, группы меню свёрнуты
        if tab_index in wanted_indexes or tab_index.exists():
            sections.append(f"        {toml_str(f'{tab}/{INDEX_NAME}')},")
        for folder in tabs[tab]:
            rel = folder.relative_to(docs_dir).as_posix()
            pages = [f for f in features if (docs_dir / f.path).parent == folder]
            title = folder_title(folder, features, docs_dir)
            paths = ([f"{rel}/{INDEX_NAME}"] if (folder / INDEX_NAME) in wanted_indexes or (folder / INDEX_NAME).exists() else [])
            paths += [f.path for f in sorted(pages, key=feature_key)]
            body = ",\n".join(f"            {toml_str(p)}" for p in paths)
            sections.append(f"        {{ {toml_str(title)} = [\n{body},\n        ] }},")
        items.append(f"    {{ {toml_str(FOLDER_TITLES.get(tab, tab))} = [\n" + "\n".join(sections) + "\n    ] },")
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
