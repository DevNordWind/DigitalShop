from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from fluent.syntax import FluentParser
from fluent.syntax.ast import Attribute, Junk, Message

_ROOT_MARKERS = ("pyproject.toml", "setup.cfg", ".git")


def _find_project_root(start: Path) -> Path:
    for directory in (start, *start.parents):
        if any((directory / marker).exists() for marker in _ROOT_MARKERS):
            return directory

    raise RuntimeError(
        f"Could not locate project root above {start} "
        f"(looked for one of {_ROOT_MARKERS})"
    )


BASE_DIR = _find_project_root(Path(__file__).resolve()) / "texts"
SOURCE_LANG = "ru"
TARGET_LANGS = ("en", "uk")

_parser = FluentParser()


@dataclass(frozen=True, slots=True)
class ParsedFtl:
    keys_by_file: dict[str, frozenset[str]]
    errors_by_file: dict[str, tuple[str, ...]]


def _extract_keys_and_errors(path: Path) -> tuple[frozenset[str], tuple[str, ...]]:
    resource = _parser.parse(path.read_text(encoding="utf-8"))

    keys: set[str] = set()
    errors: list[str] = []

    for entry in resource.body:
        if isinstance(entry, Junk):
            reasons = ", ".join(ann.message for ann in entry.annotations)
            errors.append(f"{path}: {reasons or 'invalid syntax'}")
            continue

        if not isinstance(entry, Message):
            continue

        keys.add(entry.id.name)
        for attr in entry.attributes:
            if isinstance(attr, Attribute):
                keys.add(f"{entry.id.name}.{attr.id.name}")

    return frozenset(keys), tuple(errors)


def _parse_locale_dir(lang_dir: Path) -> ParsedFtl:
    keys_by_file: dict[str, frozenset[str]] = {}
    errors_by_file: dict[str, tuple[str, ...]] = {}

    for file in sorted(lang_dir.rglob("*.ftl")):
        rel = str(file.relative_to(lang_dir))
        keys, errors = _extract_keys_and_errors(file)
        keys_by_file[rel] = keys
        if errors:
            errors_by_file[rel] = errors

    return ParsedFtl(keys_by_file=keys_by_file, errors_by_file=errors_by_file)


def _all_keys(parsed: ParsedFtl) -> frozenset[str]:
    if not parsed.keys_by_file:
        return frozenset()
    return frozenset.union(*parsed.keys_by_file.values())


@pytest.fixture(scope="module")
def source_ftl() -> ParsedFtl:
    return _parse_locale_dir(BASE_DIR / SOURCE_LANG)


@pytest.mark.parametrize("lang", TARGET_LANGS)
def test_no_syntax_errors_in_locale(lang: str) -> None:
    parsed = _parse_locale_dir(BASE_DIR / lang)
    all_errors = [err for errs in parsed.errors_by_file.values() for err in errs]
    assert not all_errors, "Syntax errors found in .ftl files:\n" + "\n".join(
        all_errors
    )


def test_no_syntax_errors_in_source(source_ftl: ParsedFtl) -> None:
    all_errors = [err for errs in source_ftl.errors_by_file.values() for err in errs]
    assert not all_errors, "Syntax errors found in .ftl files:\n" + "\n".join(
        all_errors
    )


@pytest.mark.parametrize("lang", TARGET_LANGS)
def test_all_source_keys_present_in_target_lang(
    lang: str, source_ftl: ParsedFtl
) -> None:
    target_dir = BASE_DIR / lang
    assert target_dir.exists(), (
        f"Locale directory '{lang}' does not exist: {target_dir}"
    )

    target_ftl = _parse_locale_dir(target_dir)

    source_keys = _all_keys(source_ftl)
    target_keys = _all_keys(target_ftl)

    missing = sorted(source_keys - target_keys)
    assert not missing, (
        f"Locale '{lang}' is missing keys present in '{SOURCE_LANG}': {missing}"
    )


@pytest.mark.parametrize("lang", TARGET_LANGS)
def test_no_orphan_keys_in_target_lang(lang: str, source_ftl: ParsedFtl) -> None:
    target_ftl = _parse_locale_dir(BASE_DIR / lang)

    source_keys = _all_keys(source_ftl)
    target_keys = _all_keys(target_ftl)

    orphans = sorted(target_keys - source_keys)
    assert not orphans, (
        f"Locale '{lang}' has keys missing from '{SOURCE_LANG}' "
        f"(possibly leftover from a refactor): {orphans}"
    )
