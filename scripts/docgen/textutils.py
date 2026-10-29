"""Мелкие текстовые помощники, общие для всех этапов."""

from __future__ import annotations


def clean(value: object) -> str:
    """Приводит значение метаданных к аккуратной строке."""
    return " ".join(str(value).split()) if value is not None else ""


def sort_key(text: str) -> str:
    return text.casefold()


def escape_md(text: str) -> str:
    return text.replace("[", r"\[").replace("]", r"\]")


def toml_str(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
