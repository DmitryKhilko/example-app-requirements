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

    def error(self, path: Path, message: str) -> None:
        self.errors.append(message)
        self._print("error", path, message)

    def warning(self, path: Path, message: str) -> None:
        self.warnings.append(message)
        self._print("warning", path, message)

    @staticmethod
    def _print(level: str, path: Path, message: str) -> None:
        rel = display_path(path)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::{level} file={rel}::{message}", file=sys.stderr)
        else:
            label = "ОШИБКА" if level == "error" else "Предупреждение"
            print(f"{label}: {rel}: {message}", file=sys.stderr)


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
