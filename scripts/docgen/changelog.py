"""Версии и журнал изменений активных спецификаций, формируемые по истории git.

Авторы не меняют `doc_version` и раздел «Журнал изменений» вручную. Скрипт (`generate_docs.py --versioning`, в CI после
слияния в main) для каждой активной спецификации:

1. берёт историю коммитов файла (`git log --follow`, от старых к новым; коммиты со `[skip ci]` — автоматические — не учитываются);
2. считает версию X.Y.Z по сообщениям коммитов (Conventional Commits): первый коммит — 0.1.0; `feat!:` или «BREAKING CHANGE» —
   X+1, Y=0, Z=0; `feat:` — Y+1, Z=0; всё остальное (`fix:`, `docs:`, …) — Z+1;
3. записывает итоговую версию в `doc_version` и целиком перезаписывает «Журнал изменений»: по строке на каждый коммит,
   новые сверху — «Версия 0.2.0. Ответственный: Автор», где версия — ссылка на коммит (адрес — `repo_url` из zensical.toml).

Полная перезапись выбрана намеренно: журнал всегда повторяет историю git, без дублей и сбоев порядка. Для этого в CI нужна
полная история (`fetch-depth: 0`). Без git, без коммитов у файла и для архивных спецификаций этап пропускается.

Хуки: pre-commit (`--staged`) запрещает менять `doc_version` и журнал вручную, commit-msg (`--commit-msg`) требует
префикс Conventional Commits, если в коммит попала активная спецификация.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import (CHANGELOG_ANCHOR, CHANGELOG_TITLE, COMMIT_TYPES, COMMIT_URL_PATH, DOC_VERSION_KEY,
                     FRONT_MATTER_RE, GENERATED_COMMIT_MARK, INITIAL_VERSION, RELATIONS_BEGIN_PREFIX, RELATIONS_END,
                     SPEC_KEYS)
from .problems import Problems

_CHANGELOG_START_RE = re.compile(r'^\?\?\?\+?[ \t]+\w+[^\n]*id="' + CHANGELOG_ANCHOR + '"')
_H1_RE = re.compile(r"^ {0,3}#[ \t]+(.+?)[ \t]*$")
_VERSION_LINE_RE = re.compile(rf"^({DOC_VERSION_KEY}:[ \t]*)(\"[^\"\n]*\"|'[^'\n]*'|[^\s#\n]*)", re.MULTILINE)
_REPO_URL_RE = re.compile(r'^repo_url\s*=\s*"([^"]+)"', re.MULTILINE)
_CONVENTIONAL_RE = re.compile(r"^(?P<type>[A-Za-z]+)(\([^)\n]*\))?(?P<bang>!)?:[ \t]*\S")
_SEP = "\x1f"


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def _git(root: Path, *args: str) -> str | None:
    """Вывод команды git (UTF-8) или None, если git недоступен, репозитория нет или команда завершилась ошибкой."""
    try:
        done = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=root, capture_output=True, check=False)
    except (OSError, ValueError):
        return None
    return done.stdout.decode("utf-8", errors="replace") if done.returncode == 0 else None


def repo_root(start: Path) -> Path | None:
    out = _git(start, "rev-parse", "--show-toplevel")
    return Path(out.strip()) if out and out.strip() else None


def _has_commits(root: Path) -> bool:
    return _git(root, "rev-parse", "--verify", "-q", "HEAD") is not None


def _md_names(root: Path, *args: str) -> list[str]:
    return [l for l in (_git(root, *args) or "").split("\n") if l.strip().endswith(".md")]


def repo_url(config: Path) -> str:
    """Адрес репозитория из zensical.toml (`repo_url`); пустая строка, если не задан."""
    try:
        found = _REPO_URL_RE.search(config.read_text(encoding="utf-8"))
    except OSError:
        return ""
    return found.group(1).rstrip("/") if found else ""


# ---------------------------------------------------------------------------
# Разбор файла
# ---------------------------------------------------------------------------

def _front_matter(text: str) -> dict | None:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None
    return meta if isinstance(meta, dict) else None


def _is_spec(text: str) -> bool:
    meta = _front_matter(text)
    return bool(meta) and any(key in meta for key in SPEC_KEYS)


def is_active(rel_to_docs: str, archive_dir_name: str) -> bool:
    """Активная спецификация: лежит в docs/registry/, но не в папке архива."""
    parts = rel_to_docs.split("/")
    return len(parts) > 2 and parts[0] == "registry" and parts[1] != archive_dir_name


def _changelog_span(lines: list[str]) -> tuple[int, int] | None:
    """(первая, последняя) строки блока «Журнал изменений»: строка `??? note … id="change-history"` и весь отступ под ней."""
    for start, line in enumerate(lines):
        if _CHANGELOG_START_RE.match(line):
            last = start
            for j in range(start + 1, len(lines)):
                if not lines[j].strip():
                    continue
                if lines[j].startswith(("    ", "\t")):
                    last = j
                    continue
                break
            return start, last
    return None


def _doc_version_of(text: str | None) -> str:
    return str((_front_matter(text or "") or {}).get(DOC_VERSION_KEY) or "").strip()


def _journal_of(text: str | None) -> list[str]:
    lines = (text or "").replace("\r\n", "\n").split("\n")
    span = _changelog_span(lines)
    return [l.rstrip() for l in lines[span[0]:span[1] + 1] if l.strip()] if span else []


# ---------------------------------------------------------------------------
# Версии по истории коммитов
# ---------------------------------------------------------------------------

@dataclass
class VersionEntry:
    version: str
    commit: str
    author: str


def next_version(version: tuple[int, int, int], message: str) -> tuple[int, int, int]:
    """Следующая версия по сообщению коммита (Conventional Commits)."""
    major, minor, patch = version
    subject = message.strip().split("\n", 1)[0]
    found = _CONVENTIONAL_RE.match(subject)
    if (found and found.group("bang")) or "BREAKING CHANGE" in message:
        return major + 1, 0, 0
    if found and found.group("type").lower() == "feat":
        return major, minor + 1, 0
    return major, minor, patch + 1


def version_history(root: Path, rel: str) -> list[VersionEntry]:
    """Записи журнала от старых к новым: версия после каждого коммита, затронувшего файл."""
    out = _git(root, "log", "--follow", "--reverse", "--no-merges", f"--format=%x00%H{_SEP}%an{_SEP}%B", "--", rel)
    if not out:
        return []
    version = tuple(int(p) for p in INITIAL_VERSION.split("."))
    entries: list[VersionEntry] = []
    for chunk in out.split("\x00")[1:]:
        commit, _, rest = chunk.partition(_SEP)
        author, _, message = rest.partition(_SEP)
        if GENERATED_COMMIT_MARK in message:
            continue
        if entries:
            version = next_version(version, message)
        entries.append(VersionEntry(".".join(map(str, version)), commit.strip(), author.strip()))
    return entries


def build_journal(entries: list[VersionEntry], url: str) -> list[str]:
    """Блок «Журнал изменений» (аккордеон `??? note no-icon`) со списком версий, новые сверху."""
    lines = [f'??? note no-icon "<h2 id="{CHANGELOG_ANCHOR}" style="display: inline;">{CHANGELOG_TITLE}</h2>"', ""]
    for item in reversed(entries):
        label = f"Версия {item.version}"
        link = f"[{label}]({url}{COMMIT_URL_PATH}{item.commit})" if url else label
        lines.append(f"    - {link}. Ответственный: {item.author}")
    return lines


def apply_versioning(text: str, entries: list[VersionEntry], url: str) -> str:
    """Текст спецификации с актуальными `doc_version` и журналом изменений."""
    eol = "\r\n" if "\r\n" in text else "\n"
    match = FRONT_MATTER_RE.match(text)
    head, tail = (text[:match.end()], text[match.end():]) if match else ("", text)
    version = entries[-1].version
    new_head, count = _VERSION_LINE_RE.subn(lambda m: f'{m.group(1)}"{version}"', head, count=1)
    if not count and match:   # поля нет — добавляем перед закрывающим ---
        new_head = re.sub(r"(\r?\n---[ \t]*\r?\n?)$", lambda m: f'{eol}{DOC_VERSION_KEY}: "{version}"{m.group(1)}', head, count=1)
    lines = (new_head + tail).replace("\r\n", "\n").split("\n")
    journal = build_journal(entries, url)
    span = _changelog_span(lines)
    if span:
        lines[span[0]:span[1] + 1] = journal
    else:
        offset = new_head.replace("\r\n", "\n").count("\n")
        h1 = next((i for i in range(offset, len(lines)) if _H1_RE.match(lines[i])), None)
        at = (h1 + 1) if h1 is not None else offset
        block = ["", *journal]
        lines[at:at] = block
        if at + len(block) < len(lines) and lines[at + len(block)].strip():
            lines.insert(at + len(block), "")
    return eol.join(lines)


def sync_versions(docs_dir: Path, archive_dir_name: str, config: Path) -> list[Path]:
    """Обновляет `doc_version` и журнал изменений у активных спецификаций по истории git. Возвращает изменённые файлы."""
    root = repo_root(docs_dir)
    if root is None or not _has_commits(root):
        return []
    url = repo_url(config)
    changed: list[Path] = []
    for rel in _md_names(root, "ls-files", "--", docs_dir.as_posix()):
        path = root / rel
        if not path.is_file() or not is_active(path.relative_to(docs_dir).as_posix(), archive_dir_name):
            continue
        text = path.read_text(encoding="utf-8")
        if not _is_spec(text):
            continue
        entries = version_history(root, rel)
        if not entries:
            continue
        updated = apply_versioning(text, entries, url)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="")
            changed.append(path)
    return changed


# ---------------------------------------------------------------------------
# Проверки для хуков
# ---------------------------------------------------------------------------

def check_staged_edits(docs_dir: Path, archive_dir_name: str, problems: Problems) -> None:
    """pre-commit: в изменённых активных спецификациях запрещено править `doc_version` и «Журнал изменений» вручную."""
    root = repo_root(docs_dir)
    if root is None or not _has_commits(root):
        return
    for rel in _md_names(root, "diff", "--cached", "--name-only", "--diff-filter=M", "--", docs_dir.as_posix()):
        path = root / rel
        if not is_active(path.relative_to(docs_dir).as_posix(), archive_dir_name):
            continue
        old, new = _git(root, "show", f"HEAD:{rel}"), _git(root, "show", f":{rel}")
        if old is None or new is None or not _is_spec(new):
            continue
        if _doc_version_of(old) != _doc_version_of(new):
            problems.error(path, f"`{DOC_VERSION_KEY}` менять вручную нельзя: версию считает скрипт по сообщениям коммитов "
                                 f"(feat: / fix: / feat!:)")
        if _journal_of(old) != _journal_of(new):
            problems.error(path, f"раздел «{CHANGELOG_TITLE}» менять вручную нельзя: его формирует скрипт по истории git")


def check_commit_message(message_file: Path, docs_dir: Path, archive_dir_name: str, problems: Problems) -> None:
    """commit-msg: если в коммит попала активная спецификация, сообщение должно начинаться с префикса Conventional Commits."""
    root = repo_root(docs_dir)
    if root is None:
        return
    try:
        raw = message_file.read_text(encoding="utf-8")
    except OSError:
        return
    lines = [l for l in raw.split("\n") if l.strip() and not l.startswith("#")]
    subject = lines[0].strip() if lines else ""
    if subject.startswith(("Merge ", "Revert ", "fixup!", "squash!")):
        return
    staged = _md_names(root, "diff", "--cached", "--name-only", "--diff-filter=AM", "--", docs_dir.as_posix())
    if not any(is_active((root / r).relative_to(docs_dir).as_posix(), archive_dir_name) for r in staged):
        return
    found = _CONVENTIONAL_RE.match(subject)
    if not found or found.group("type").lower() not in COMMIT_TYPES:
        problems.error(message_file, "сообщение коммита должно начинаться с префикса: "
                                     + ", ".join(f"`{t}:`" for t in COMMIT_TYPES)
                                     + " (feat: — новая функциональность, fix: — исправление, feat!: — несовместимое изменение), "
                                     "например: `feat: добавил шаг подтверждения по SMS`")
