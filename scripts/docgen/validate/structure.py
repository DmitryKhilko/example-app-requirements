"""Проверка структуры текста спецификаций (только предупреждения)."""

from __future__ import annotations

from ..config import DESCRIPTION_ANCHOR, DESCRIPTION_RE, FOLDER_TITLES, INDEX_NAME
from ..models import BuildContext, Feature, Spec
from ..problems import Problems
from pathlib import Path


def has_description(text: str) -> bool:
    """Есть ли заголовок «Описание» с якорем `{#article-overview}` (вне блоков кода)."""
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        elif not in_fence and DESCRIPTION_RE.match(line):
            return True
    return False


def check_structure(specs: list[Spec], features: list[Feature], ctx: BuildContext, problems: Problems) -> None:
    """Предупреждения по структуре (ничего не пишет):

    * в спецификации есть раздел «Описание» с якорем `{#article-overview}` (на него ведут ссылки карты и окна
      предпросмотра, после него вставляется раздел «Взаимосвязи»);
    * в папках разделов (specifications, archive) нет .md-файлов без метаданных спецификации: такой файл
      молча не попал бы в карту. Файлы index.md пропускаются (вручную созданные отмечает validate/project.py).
    """
    texts = {s.rel: s.text for s in specs}
    for f in features:
        if not has_description(texts[f.path]):
            problems.warning(ctx.docs_dir / f.path, f"нет раздела «Описание» с якорем `{{#{DESCRIPTION_ANCHOR}}}`")

    sections = {ctx.archive_dir_name, *FOLDER_TITLES}
    for spec in specs:
        parts = Path(spec.rel).parts
        if spec.is_spec or spec.broken or len(parts) < 2 or parts[0] not in sections:
            continue
        if spec.path.name == INDEX_NAME:
            continue  # сформированные index.md — не спецификации; созданные вручную отмечает validate/project.py
        problems.warning(spec.path, "файл в папке спецификаций без метаданных спецификации "
                                    "(`module`, `feature_name`): в карту он не попадёт")
