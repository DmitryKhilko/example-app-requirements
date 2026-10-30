"""Накопитель ошибок и предупреждений."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .config import REPO_ROOT


class Problems:
    """Накопитель ошибок и предупреждений (выводятся в формате GitHub Actions)."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path, message: str, line: int | None = None) -> None:
        self.errors.append(message)
        self._print("error", path, message, line)

    def warning(self, path: Path, message: str, line: int | None = None) -> None:
        self.warnings.append(message)
        self._print("warning", path, message, line)

    @staticmethod
    def _print(level: str, path: Path, message: str, line: int | None) -> None:
        rel = display_path(path)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            where = f"file={rel},line={line}" if line else f"file={rel}"
            print(f"::{level} {where}::{message}", file=sys.stderr)
        else:
            label = "ОШИБКА" if level == "error" else "Предупреждение"
            print(f"{label}: {rel}{f':{line}' if line else ''}: {message}", file=sys.stderr)


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
