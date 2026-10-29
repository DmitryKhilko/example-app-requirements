"""Значок статуса в левом меню: поле `icon` метаданных ведётся по `status`, вручную его не заполняют."""

from __future__ import annotations

import re

from ..config import FRONT_MATTER_RE, ICON_KEY, STATUS_ICONS
from ..models import Feature


def status_icon(feature: Feature) -> str:
    """Значок статуса для поля `icon`: `:lucide-file-check:` -> `lucide/file-check` (тот же рисунок, что в карте)."""
    return "lucide/" + STATUS_ICONS[feature.shown_status].strip(":").removeprefix("lucide-")


def set_icon(text: str, icon: str) -> str | None:
    """Ставит поле `icon` в метаданные: заменяет имеющееся или вставляет после `status`. None — метаданных нет."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    block, line = match.group(1), f"{ICON_KEY}: {icon}"
    if re.search(rf"(?m)^{ICON_KEY}:.*$", block):
        block = re.sub(rf"(?m)^{ICON_KEY}:.*$", lambda _: line, block, count=1)
    elif re.search(r"(?m)^status:.*$", block):
        block = re.sub(r"(?m)^(status:.*)$", lambda m: f"{m.group(1)}\n{line}", block, count=1)
    else:
        block = f"{block}\n{line}"
    return text[:match.start(1)] + block + text[match.end(1):]


def plan_icons(features: list[Feature], texts: dict[str, str]) -> dict[str, str]:
    """Спецификации (путь относительно docs -> новый текст), у которых поле `icon` не соответствует статусу."""
    changed: dict[str, str] = {}
    for f in features:
        text = texts[f.path]
        new = set_icon(text, status_icon(f))
        if new is not None and new != text:
            changed[f.path] = new
    return changed
