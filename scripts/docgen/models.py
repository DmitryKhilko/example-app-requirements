"""Модель данных: связи, фичи, прочитанные файлы, параметры запуска и план записи."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import SPEC_KEYS, STATUS_ICONS


@dataclass(frozen=True)
class Relation:
    """Связь, объявленная в метаданных спецификации-источника."""
    kind: str          # ключ из RELATION_TYPES
    target: str        # имя файла (slug) целевой спецификации
    note: str = ""     # пояснение для таблицы (необязательно)


@dataclass(frozen=True)
class Feature:
    module: str
    submodule: str
    name: str
    link: str          # ссылка на раздел «Описание» относительно файла карты (с якорем)
    status: str        # ключ из STATUS_ICONS
    archived: bool
    path: str = ""    # путь файла относительно папки docs (posix)
    slug: str = ""    # имя файла без расширения: по нему фичи ссылаются друг на друга
    relations: tuple[Relation, ...] = ()
    order: int | None = None   # необязательное поле `order`: порядок в меню и картах (меньше — выше)

    @property
    def shown_status(self) -> str:
        """Статус, под которым фича показана в карте (архивные всегда `archived`)."""
        return "archived" if self.archived else self.status

    @property
    def icon(self) -> str:
        return STATUS_ICONS[self.shown_status]


@dataclass(frozen=True)
class Link:
    """Связь, показанная с точки зрения одной фичи: что за фича и в какую сторону направлена связь."""
    kind: str          # ключ из RELATION_TYPES
    direction: str     # out — объявлена в этой спецификации, in — в спецификации `other`
    other: Feature
    note: str = ""


@dataclass(frozen=True)
class Spec:
    """Прочитанный .md-файл из docs/: путь, текст и метаданные как есть (без проверок)."""
    path: Path
    rel: str                      # путь относительно папки docs (posix)
    text: str
    meta: dict | None             # None — метаданных нет или они не разобраны
    broken: bool = False          # метаданные есть, но разобрать их не удалось (ошибка уже сообщена)

    @property
    def is_spec(self) -> bool:
        """Спецификацией считается файл, в метаданных которого есть хотя бы одно из полей SPEC_KEYS."""
        return bool(self.meta) and any(key in self.meta for key in SPEC_KEYS)


@dataclass
class BuildContext:
    """Параметры запуска, общие для всех этапов (вместо глобальных переменных)."""
    docs_dir: Path
    output: Path                  # файл карты фичей (resolved)
    archive_dir_name: str
    config: Path                  # zensical.toml
    nav_order: Path               # nav-order.yml
    template: Path                # шаблон спецификации: источник правил проверки
    module_order: list[str] = field(default_factory=list)   # заполняется при проверке (из nav-order.yml)


@dataclass
class Plan:
    """Результат генерации: что должно оказаться на диске. Сама генерация ничего не пишет."""
    map_path: Path
    map_content: str
    indexes: dict[Path, str]
    stale_indexes: list[Path]
    nav_path: Path | None = None              # zensical.toml (None — файла нет)
    nav_content: str | None = None
    icons: dict[Path, str] = field(default_factory=dict)       # спецификации с обновлённым `icon` (новый текст)
    relations: dict[Path, str] = field(default_factory=dict)   # спецификации с обновлённым разделом «Взаимосвязи»
    features_total: int = 0
