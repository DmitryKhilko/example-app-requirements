"""Этап 1. Чтение: обход docs/, разбор блока метаданных (YAML Front Matter) каждого файла."""

from __future__ import annotations

from pathlib import Path

import yaml

from .config import FRONT_MATTER_RE
from .models import Spec
from .problems import Problems


def read_front_matter(path: Path, text: str, problems: Problems) -> dict | None:
    """Возвращает метаданные файла или None, если блока метаданных нет (или он не разобран: ошибка уже сообщена)."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        problems.error(path, f"некорректный YAML в метаданных: {exc}".replace("\n", " "))
        return None
    if data is None:
        return {}
    if not isinstance(data, dict):
        problems.error(path, "метаданные должны быть набором «ключ: значение»")
        return None
    return data


def read_specs(docs_dir: Path, output: Path, problems: Problems) -> list[Spec]:
    """Читает все .md-файлы папки docs/ (кроме файла карты): текст и метаданные. Решений о корректности не принимает."""
    specs: list[Spec] = []
    for path in sorted(docs_dir.rglob("*.md")):
        if path.resolve() == output:
            continue
        text = path.read_text(encoding="utf-8")
        errors_before = len(problems.errors)
        meta = read_front_matter(path, text, problems)
        specs.append(Spec(path, path.relative_to(docs_dir).as_posix(), text, meta,
                          broken=len(problems.errors) > errors_before))
    return specs