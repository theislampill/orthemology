#!/usr/bin/env python3
"""Mathematical-source validator (R7B, Decision 0023).

Deterministic, offline. Guards the math-source discipline the audit requires:

  1. render_map <-> registry bijection: every non-retired notation symbol has
     exactly one render_map entry and vice versa (no symbol goes un-rendered,
     no orphan render entry drifts in);
  2. every render_map `latex` translates through scripts/latex_to_typst_math.py
     with no MathConvertError (the strict subset actually covers the corpus);
  3. notation-gallery drift: every render_map `latex` appears verbatim in
     docs/notation-gallery.md, so the gallery renders every registered symbol;
  4. NO precomposed combining accent (U+0300-U+036F, U+20D7) inside publication
     math source ($...$, $$...$$, ```math) anywhere in the corpus — publication
     math must use \\hat / \\bar / \\vec (this is the exact source antipattern
     behind the reproduced notdef defect, R7B-PDF-MATH-BASELINE.md);
  5. build, migration, inventory, and publication-profile source ownership is
     exact and bidirectional;
  6. every inline-code occurrence in the seven publication sources has one
     file/locus/occurrence classification; and
  7. the deferred publication profile is schema-valid and venue-neutral.

This is a typography/consistency gate. It establishes no empirical or
theological claim, and it does not change any symbol's meaning (Decision 0005).
"""
import ast
import io
import json
import os
import re
import sys
import unicodedata
from collections import Counter

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from latex_to_typst_math import translate_inline, translate_display, MathConvertError
from validate_publication_profile import validate_profile

FAILS = []
GALLERY = "docs/notation-gallery.md"
# combining diacritics that must never appear in publication math source
COMBINING = re.compile(r"[̀-ͯ⃗]")
DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE_RE = re.compile(r"\$([^\$\n]+?)\$")
CODE_FENCE_RE = re.compile(r"```(\w*)\n(.*?)```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})([^\r\n]*)$")
FORMULA_SIGNAL_RE = re.compile(
    r"[=∈⊆⊂⟺⇔→↦∧∨≼≠≤≥∀∃∅⊥⊨⊭±×÷∩∪⟨⟩⋅·−≈≃]"
    r"|\{[^}]*\|[^}]*\}"
)
URL_RE = re.compile(
    r"(?<![A-Za-z0-9+.-])https?://[^\s<>`\"']+",
    re.IGNORECASE,
)
FILE_TOKEN_RE = re.compile(
    r"(?<![\w.])"
    r"(?:\.{1,2}[\\/])?"
    r"(?:[\w()\-]+[\\/])*"
    r"[\w()\-]+(?:\.[A-Za-z0-9]+)+"
    r"(?![\w.])"
)
SEMVER_TOKEN_RE = re.compile(
    r"(?<![0-9A-Za-z])"
    r"v?(?:0|[1-9][0-9]*)"
    r"\.(?:0|[1-9][0-9]*)"
    r"\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?![0-9A-Za-z])"
)
CLOSED_SINGLE_LETTER_STATUS_PREFIXES = "ABCDEFGHIKMNOPRSV"
STATUS_ID_TOKEN_RE = re.compile(
    r"(?<![A-Z0-9])"
    r"(?:"
    r"[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+"
    r"|"
    rf"[{CLOSED_SINGLE_LETTER_STATUS_PREFIXES}]"
    r"(?=[A-Z0-9-]*[0-9])(?:-[A-Z0-9]+)+"
    r")"
    r"(?![A-Z0-9])"
)
FILE_SUFFIX_RE = re.compile(r"\.[A-Za-z0-9]+/?$")
CALLABLE_FORMULA_CANDIDATE_RE = re.compile(
    r"(?<![\w./?=&-])(?P<name>[^\W\d_]\w*)\s*\([^)]*\)"
)
CLI_COMMAND_TOKEN_RE = re.compile(r"[A-Za-z_.][A-Za-z0-9_.\\/:-]+")
CLI_FLAG_TOKEN_RE = re.compile(
    r"-{1,2}[A-Za-z][A-Za-z0-9_-]*(?:=[^\s]+)?"
)
CLI_TOKEN_RE = re.compile(r"\S+")
COMMONMARK_LIST_MARKER_RE = re.compile(
    r"(?m)^(?P<indent> {0,3})[+*-](?=[ \t]+|\r?$)"
)
FORMULA_OPERAND_PATTERN = (
    r"(?:[+\-\u2212]?(?:\d+(?:\.\d+)?|\.\d+)|[^\W\d_]\w*)"
)
FORMULA_IDENTIFIER_RE = re.compile(r"[^\W\d_]\w*$")
FORMULA_OPERAND_AT_END_RE = re.compile(FORMULA_OPERAND_PATTERN + r"$")
FORMULA_OPERAND_AT_START_RE = re.compile(FORMULA_OPERAND_PATTERN)
OPERAND_BOUNDARY_CHARS = frozenset("./\\?&=#@")
PUNCTUATION_FORMULA_OPERATORS = frozenset("*/^-·")
ISOLATED_FORMULA_OPERATOR_RE = re.compile(r"(?<![\w/])(?:[+/^])(?![\w/])")
UNICODE_INDEXED_IDENTIFIER_RE = re.compile(
    r"(?<!\w)([^\W\d_]\w*_[A-Za-z0-9]+)(?!\w)"
)
APPROVED_DIAGNOSTIC_OCCURRENCE_KEY = (
    "theory/orthemic-core-formalization.md",
    477,
    38,
    13,
)
APPROVED_DIAGNOSTIC_TEXT = (
    "\u03bc\u0304_2: stale calibration; \u03bc\u0304_3: wrong\n"
    "  claim scope"
)
MACHINE_ASSIGNMENT_RE = re.compile(
    r"(?:(?:export )?[A-Z_][A-Z0-9_]*|\$env:[A-Za-z_][A-Za-z0-9_]*)=(.*)",
    re.S,
)
MATH_OR_CONTROL_IN_VALUE_RE = re.compile(
    r"[=∈⊆⊂⟺⇔→↦∧∨≼≠≤≥∀∃⃗{}|;&<>`]"
)


def _without_syntactic_urls(span):
    """Replace complete HTTP(S) URL tokens before formula classification."""
    return URL_RE.sub(lambda match: " " * len(match.group(0)), span)


def _is_cli_command(span):
    """Return whether *span* is a complete command containing CLI flag tokens."""
    if "\n" in span or "\r" in span:
        return False
    tokens = span.strip().split()
    if len(tokens) < 2 or not CLI_COMMAND_TOKEN_RE.fullmatch(tokens[0]):
        return False
    return any(
        CLI_FLAG_TOKEN_RE.fullmatch(token.strip("'\""))
        for token in tokens[1:]
    )


def _without_cli_syntax(span):
    """Mask only the command and complete option tokens in a CLI-shaped span."""
    if not _is_cli_command(span):
        return span
    characters = list(span)
    for index, match in enumerate(CLI_TOKEN_RE.finditer(span)):
        token = match.group(0)
        if (
            index == 0
            or CLI_FLAG_TOKEN_RE.fullmatch(token.strip("'\""))
        ):
            characters[match.start():match.end()] = " " * len(token)
    return "".join(characters)


def is_machine_assignment(span):
    """Return whether *span* is one complete shell environment assignment.

    Bare shell names use the conventional uppercase environment-name grammar;
    PowerShell's explicit ``$env:`` namespace also permits mixed-case names.
    The value may be one wholly quoted scalar or one whitespace-free unquoted
    scalar, but may not contain formula or command-control syntax.
    """
    match = MACHINE_ASSIGNMENT_RE.fullmatch(span)
    if not match:
        return False
    value = match.group(1)
    powershell_env = span.startswith("$env:")
    control_value = value
    if powershell_env and value.startswith('"') and value.endswith('"'):
        control_value = value.replace("`$", "")
    control_value = _without_syntactic_urls(control_value)
    if not value or MATH_OR_CONTROL_IN_VALUE_RE.search(control_value):
        return False
    if value[0] in "'\"":
        quote = value[0]
        structurally_complete = (
            len(value) >= 2
            and value[-1] == quote
            and quote not in value[1:-1]
            and "\n" not in value
        )
        if not structurally_complete or quote == "'":
            return structurally_complete
        interior = value[1:-1]
        if "$" not in interior:
            return True
        unescaped = interior.replace("`$", "")
        return powershell_env and "$" not in unescaped and "`" not in unescaped
    return (
        "$" not in value
        and "(" not in value
        and ")" not in value
        and not any(ch.isspace() or ch in "'\"" for ch in value)
    )


def real_math_spans(text):
    """Extract genuine math spans, ignoring $ that appears inside code fences or
    inline `code` (e.g. prose describing the $...$ syntax). Returns (kind, body)
    with kind 'i' (inline) or 'd' (display/fence)."""
    spans = []

    def fence_sub(m):
        if m.group(1).strip() == "math":
            spans.append(("d", m.group(2)))
        return "\n"

    t = CODE_FENCE_RE.sub(fence_sub, text)
    t = INLINE_CODE_RE.sub(" ", t)
    for m in DISPLAY_RE.finditer(t):
        spans.append(("d", m.group(1)))
    t = DISPLAY_RE.sub(" ", t)
    for m in INLINE_RE.finditer(t):
        spans.append(("i", m.group(1)))
    return spans


def _mask_fences(text):
    """Mask CommonMark fenced code while retaining every source offset.

    Backtick and tilde fences may use any run of three or more markers. A
    closing run must use the same marker and be at least as long as the opener;
    shorter interior runs remain code. An unclosed fence extends to end of
    input, as it does under CommonMark.
    """
    masked = list(text)
    fence = None
    fence_start = None
    offset = 0
    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        if fence is None:
            match = FENCE_OPEN_RE.fullmatch(content)
            if match is not None:
                marker = match.group(1)
                info = match.group(2)
                if marker[0] == "`" and "`" in info:
                    match = None
            if match is not None:
                fence = (marker[0], len(marker))
                fence_start = offset
        else:
            marker, minimum_length = fence
            close = re.fullmatch(
                r" {0,3}%s{%d,}[ \t]*"
                % (re.escape(marker), minimum_length),
                content,
            )
            if close is not None:
                end = offset + len(line)
                for index in range(fence_start, end):
                    if masked[index] != "\n":
                        masked[index] = " "
                fence = None
                fence_start = None
        offset += len(line)
    if fence is not None:
        for index in range(fence_start, len(masked)):
            if masked[index] != "\n":
                masked[index] = " "
    return "".join(masked)


class InlineCodeParseError(ValueError):
    """Raised when a single-backtick code span has no closing delimiter."""


def _single_backtick_spans(masked):
    """Return source offsets for CommonMark code spans delimited by one backtick.

    A code span may cross line boundaries. Runs of two or more backticks are
    paired and skipped as separate CommonMark code spans, so a single backtick
    inside one is never misclassified. Fenced blocks must be masked first.
    """
    spans = []
    cursor = 0
    length = len(masked)
    while cursor < length:
        opening = masked.find("`", cursor)
        if opening < 0:
            break
        run_end = opening + 1
        while run_end < length and masked[run_end] == "`":
            run_end += 1
        run_length = run_end - opening

        closing = run_end
        while True:
            closing = masked.find("`", closing)
            if closing < 0:
                if run_length == 1:
                    line = masked.count("\n", 0, opening) + 1
                    last_newline = masked.rfind("\n", 0, opening)
                    column = opening - last_newline
                    raise InlineCodeParseError(
                        "malformed single-backtick delimiter at line %d, column %d"
                        % (line, column)
                    )
                cursor = run_end
                break
            closing_end = closing + 1
            while closing_end < length and masked[closing_end] == "`":
                closing_end += 1
            if closing_end - closing == run_length:
                if run_length == 1:
                    spans.append(
                        {
                            "start": opening,
                            "end": closing_end,
                            "content_start": run_end,
                            "content_end": closing,
                        }
                    )
                cursor = closing_end
                break
            closing = closing_end
    return spans


def extract_inline_code_occurrences(text):
    """Return source-ordered inline-code occurrences with stable source loci."""
    masked = _mask_fences(text)
    occurrences = []
    for ordinal, span in enumerate(_single_backtick_spans(masked), 1):
        start = span["start"]
        line = masked.count("\n", 0, start) + 1
        last_newline = masked.rfind("\n", 0, start)
        column = start - last_newline
        occurrences.append(
            {
                "locus": {"line": line, "column": column},
                "occurrence": ordinal,
                "text": text[span["content_start"]:span["content_end"]],
            }
        )
    return occurrences


def _without_syntactic_file_paths(span):
    """Replace unambiguous filenames and relative paths before classification."""
    def replace(match):
        token = match.group(0)
        if any(char.isalpha() or char in "_()" for char in token):
            return " " * len(token)
        return token

    return FILE_TOKEN_RE.sub(replace, span)


def _without_semver_tokens(span):
    """Replace complete semantic-version tokens before operator classification."""
    return SEMVER_TOKEN_RE.sub(lambda match: " " * len(match.group(0)), span)


def _without_status_ids(span):
    """Replace uppercase hyphenated status identifiers before classification."""
    return STATUS_ID_TOKEN_RE.sub(lambda match: " " * len(match.group(0)), span)


def _without_commonmark_list_markers(span):
    """Mask 0–3-space CommonMark unordered-list markers line by line."""
    return COMMONMARK_LIST_MARKER_RE.sub(
        lambda match: match.group("indent") + " ",
        span,
    )


def _contains_unicode_mark(span):
    """Return whether *span* contains any Unicode Mark category."""
    return any(unicodedata.category(char).startswith("M") for char in span)


def _is_formula_operator(char):
    """Recognize Unicode math symbols and reviewed ASCII punctuation operators."""
    return (
        unicodedata.category(char) == "Sm"
        or char in PUNCTUATION_FORMULA_OPERATORS
    )


def _operand_before(span, operator_start):
    prefix = span[:operator_start].rstrip()
    match = FORMULA_OPERAND_AT_END_RE.search(prefix)
    if not match:
        return None
    if (
        match.start()
        and (
            prefix[match.start() - 1] in OPERAND_BOUNDARY_CHARS
            or prefix[match.start() - 1].isalnum()
            or prefix[match.start() - 1] == "_"
        )
    ):
        return None
    return match.group(0)


def _operand_after(span, operator_end):
    suffix = span[operator_end:].lstrip()
    match = FORMULA_OPERAND_AT_START_RE.match(suffix)
    if not match:
        return None
    if (
        match.end() < len(suffix)
        and (
            suffix[match.end()] in OPERAND_BOUNDARY_CHARS
            or suffix[match.end()].isalnum()
            or suffix[match.end()] == "_"
        )
    ):
        return None
    return match.group(0)


def _binary_formula_structure(span):
    """Return whether operands surround a Unicode-category math operator run."""
    index = 0
    while index < len(span):
        if not _is_formula_operator(span[index]):
            index += 1
            continue
        operator_start = index
        while index < len(span) and _is_formula_operator(span[index]):
            index += 1
        operator_text = span[operator_start:index]
        line_start = span.rfind("\n", 0, operator_start) + 1
        line_prefix = span[line_start:operator_start]
        if (
            operator_text == "--"
            or (
                operator_text in {"-", "*"}
                and not line_prefix.strip()
            )
        ):
            continue
        left_operand = _operand_before(span, operator_start)
        right_operand = _operand_after(span, index)
        if not left_operand or not right_operand:
            continue
        if (
            operator_text == "-"
            and operator_start
            and index < len(span)
            and not span[operator_start - 1].isspace()
            and not span[index].isspace()
            and FORMULA_IDENTIFIER_RE.fullmatch(left_operand)
            and FORMULA_IDENTIFIER_RE.fullmatch(right_operand)
            and (
                "/" in span
                or "\\" in span
                or FILE_SUFFIX_RE.search(span)
            )
        ):
            continue
        if (
            operator_text == "/"
            and operator_start
            and index < len(span)
            and not span[operator_start - 1].isspace()
            and not span[index].isspace()
            and FORMULA_IDENTIFIER_RE.fullmatch(left_operand)
            and FORMULA_IDENTIFIER_RE.fullmatch(right_operand)
            and (len(left_operand) > 1 or len(right_operand) > 1)
        ):
            continue
        return True
    return False


def _unicode_formula_style(span):
    """Return whether *span* uses Unicode mathematical presentation forms."""
    for char in span:
        name = unicodedata.name(char, "")
        if (
            name.startswith("MATHEMATICAL ")
            or "SUBSCRIPT" in name
            or "SUPERSCRIPT" in name
            or (
                unicodedata.normalize("NFKC", char) != char
                and unicodedata.category(char)[0] in {"L", "N", "S"}
            )
        ):
            return True
    return False


def _callable_formula_structure(span):
    """Detect reviewed callable math names without treating prose as a call."""
    for match in CALLABLE_FORMULA_CANDIDATE_RE.finditer(span):
        name = match.group("name")
        if (
            len(name) == 1
            or any(char.isdigit() for char in name)
            or "_" in name
            or _unicode_formula_style(name)
        ):
            return True
    return False


def _unicode_indexed_identifier(span):
    """Return whether an indexed identifier contains a non-ASCII letter."""
    return any(
        any(ord(char) > 127 for char in match.group(1))
        for match in UNICODE_INDEXED_IDENTIFIER_RE.finditer(span)
    )


def _formula_like(span):
    candidate = _without_cli_syntax(span)
    candidate = _without_syntactic_urls(candidate)
    candidate = _without_semver_tokens(candidate)
    candidate = _without_syntactic_file_paths(candidate)
    candidate = _without_status_ids(candidate)
    candidate = _without_commonmark_list_markers(candidate)
    return bool(
        _contains_unicode_mark(candidate)
        or FORMULA_SIGNAL_RE.search(candidate)
        or _binary_formula_structure(candidate)
        or _callable_formula_structure(candidate)
        or ISOLATED_FORMULA_OPERATOR_RE.search(candidate)
        or _unicode_formula_style(candidate)
        or _unicode_indexed_identifier(candidate)
    )


def is_approved_diagnostic_literal(key, span):
    """Return whether *span* is the one reviewed diagnostic occurrence."""
    return key == APPROVED_DIAGNOSTIC_OCCURRENCE_KEY and span == APPROVED_DIAGNOSTIC_TEXT


def validate_inventory_data(inventory, source_texts, registry_ids=None):
    """Validate exact source occurrence <-> inventory row parity."""
    registry_ids = set(registry_ids or ())
    issues = []
    if not isinstance(inventory, dict):
        return ["inventory must be a mapping"]
    if inventory.get("schema") != "orthemology-math-source-inventory-v2":
        issues.append("inventory schema must be orthemology-math-source-inventory-v2")
    if inventory.get("classes") != [
        "literal-code",
        "semantic-registry-id",
        "mathematics",
    ]:
        issues.append("inventory classes must preserve the closed classification enum")

    source_rows = inventory.get("sources")
    occurrence_rows = inventory.get("occurrences")
    if not isinstance(source_rows, list):
        source_rows = []
        issues.append("inventory sources must be a list")
    if not isinstance(occurrence_rows, list):
        occurrence_rows = []
        issues.append("inventory occurrences must be a list")

    source_files = []
    for source_row in source_rows:
        if not isinstance(source_row, dict) or not isinstance(source_row.get("file"), str):
            issues.append("inventory source row must contain a file")
            continue
        source_files.append(source_row["file"])
    duplicates = sorted(
        path for path, count in Counter(source_files).items() if count > 1
    )
    if duplicates:
        issues.append("duplicate publication source row: %s" % duplicates)

    actual = {}
    actual_by_file = {}
    for path in source_files:
        if path not in source_texts:
            issues.append("missing publication source: %s" % path)
            continue
        try:
            extracted = extract_inline_code_occurrences(source_texts[path])
        except InlineCodeParseError as exc:
            issues.append("%s: %s" % (path, exc))
            extracted = []
        actual_by_file[path] = extracted
        for occurrence in extracted:
            key = (
                path,
                occurrence["locus"]["line"],
                occurrence["locus"]["column"],
                occurrence["occurrence"],
            )
            actual[key] = occurrence

    inventoried = {}
    rows_by_file = {}
    for row in occurrence_rows:
        if not isinstance(row, dict):
            issues.append("inventory occurrence row must be a mapping")
            continue
        locus = row.get("locus")
        if not isinstance(locus, dict):
            issues.append("inventory occurrence row lacks locus")
            continue
        key = (
            row.get("file"),
            locus.get("line"),
            locus.get("column"),
            row.get("occurrence"),
        )
        if key in inventoried:
            issues.append("duplicate occurrence key: %r" % (key,))
        else:
            inventoried[key] = row
        rows_by_file.setdefault(row.get("file"), []).append(row)

        classification = row.get("classification")
        span = row.get("text")
        if classification not in {
            "literal-code",
            "semantic-registry-id",
            "mathematics",
        }:
            issues.append("invalid occurrence classification at %r" % (key,))
            continue
        if not isinstance(span, str):
            issues.append("inventory occurrence text must be a string at %r" % (key,))
            continue
        approved_diagnostic_literal = (
            classification == "literal-code"
            and is_approved_diagnostic_literal(key, span)
        )
        if (
            COMBINING.search(span)
            and classification != "mathematics"
            and not approved_diagnostic_literal
        ):
            issues.append(
                "combining accent classified as nonmathematics at %r" % (key,)
            )
        if classification == "semantic-registry-id":
            if _formula_like(span) and span not in registry_ids:
                issues.append("formula-like registry classification at %r" % (key,))
            elif span not in registry_ids:
                issues.append("false registry-ID classification at %r" % (key,))
        if (
            classification == "literal-code"
            and _formula_like(span)
            and not is_machine_assignment(span)
            and not approved_diagnostic_literal
        ):
            issues.append("formula-like literal classification at %r" % (key,))

    for key, occurrence in actual.items():
        row = inventoried.get(key)
        if row is None:
            issues.append("unclassified source occurrence: %r" % (key,))
        elif row.get("text") != occurrence["text"]:
            issues.append("inventory text mismatch at %r" % (key,))
    for key in inventoried:
        if key not in actual:
            issues.append("orphan inventory row: %r" % (key,))

    if APPROVED_DIAGNOSTIC_OCCURRENCE_KEY[0] in source_files:
        approved_row = inventoried.get(APPROVED_DIAGNOSTIC_OCCURRENCE_KEY)
        approved_source_occurrence = actual.get(APPROVED_DIAGNOSTIC_OCCURRENCE_KEY)
        if (
            approved_row is None
            or approved_source_occurrence is None
            or approved_row.get("classification") != "literal-code"
            or approved_row.get("text") != APPROVED_DIAGNOSTIC_TEXT
            or approved_source_occurrence.get("text") != APPROVED_DIAGNOSTIC_TEXT
        ):
            issues.append(
                "approved diagnostic occurrence must match its exact "
                "inventory identity and extracted source text"
            )

    for source_row in source_rows:
        if not isinstance(source_row, dict) or "file" not in source_row:
            continue
        path = source_row["file"]
        rows = rows_by_file.get(path, [])
        if source_row.get("occurrence_count") != len(rows):
            issues.append("source occurrence count mismatch: %s" % path)
        counts = Counter(
            row.get("classification") for row in rows if isinstance(row, dict)
        )
        declared = source_row.get("classification_counts")
        expected = {
            "literal-code": counts["literal-code"],
            "semantic-registry-id": counts["semantic-registry-id"],
            "mathematics": counts["mathematics"],
        }
        if declared != expected:
            issues.append("source classification counts mismatch: %s" % path)
    totals = inventory.get("totals")
    if isinstance(totals, dict):
        counts = Counter(
            row.get("classification") for row in occurrence_rows if isinstance(row, dict)
        )
        expected_totals = {
            "sources": len(source_rows),
            "occurrences": len(occurrence_rows),
            "literal-code": counts["literal-code"],
            "semantic-registry-id": counts["semantic-registry-id"],
            "mathematics": counts["mathematics"],
        }
        if totals != expected_totals:
            issues.append("inventory totals mismatch")
    return issues


def validate_gallery_data(gallery_text, render_map):
    issues = []
    for entry in render_map:
        latex = entry.get("latex")
        symbol = entry.get("registry_symbol")
        if not isinstance(latex, str) or (
            "$" + latex + "$" not in gallery_text and latex not in gallery_text
        ):
            issues.append("gallery missing registry symbol: %s" % symbol)
    return issues


def validate_build_source_parity(build_sources, declared_sources):
    build_sources = set(build_sources)
    declared_sources = set(declared_sources)
    if build_sources == declared_sources:
        return []
    return [
        "build source parity mismatch: missing from build %s; undeclared in profile %s"
        % (
            sorted(declared_sources - build_sources),
            sorted(build_sources - declared_sources),
        )
    ]


def extract_build_sources(build_text):
    """Extract source paths only from build_pdfs.py's explicit DOCS owner."""
    tree = ast.parse(build_text)
    owners = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(target, ast.Name) and target.id == "DOCS" for target in targets):
            continue
        owners.append(ast.literal_eval(node.value))
    if len(owners) != 1:
        raise ValueError("build_pdfs.py must declare exactly one literal DOCS owner")
    sources = set()
    for row in owners[0]:
        if (
            not isinstance(row, (list, tuple))
            or len(row) != 2
            or not isinstance(row[1], (list, tuple))
        ):
            raise ValueError("DOCS rows must be (artifact_id, source_paths)")
        for source in row[1]:
            if not isinstance(source, str):
                raise ValueError("DOCS source paths must be strings")
            sources.add(source)
    return sources


def validate_migration_data(migration, inventory):
    issues = []
    if not isinstance(migration, dict):
        return ["migration status must be a mapping"]
    if migration.get("schema") != "orthemology-math-migration-status-v2":
        issues.append("migration schema must split glyph and full-source state")
    documents = migration.get("documents")
    if not isinstance(documents, list):
        return issues + ["migration documents must be a list"]
    math_sources = {
        row.get("file")
        for row in inventory.get("occurrences", [])
        if isinstance(row, dict) and row.get("classification") == "mathematics"
    }
    covered = []
    for document in documents:
        if not isinstance(document, dict):
            issues.append("migration document must be a mapping")
            continue
        for field in (
            "artifact_id",
            "sources",
            "glyph_defect_repaired",
            "full_math_source_migrated",
            "expected_notdef",
            "visual_qa_state",
        ):
            if field not in document:
                issues.append("migration document missing %s" % field)
        sources = document.get("sources", [])
        if isinstance(sources, list):
            covered.extend(sources)
        if document.get("full_math_source_migrated") is True:
            blocked = sorted(set(sources) & math_sources)
            if blocked:
                issues.append(
                    "full_math_source_migrated conflicts with math backticks: %s"
                    % blocked
                )
        if document.get("visual_qa_state") != "deferred-task-13":
            issues.append("visual QA must remain deferred to Task 13")
    inventory_sources = [
        row.get("file")
        for row in inventory.get("sources", [])
        if isinstance(row, dict)
    ]
    if Counter(covered) != Counter(inventory_sources):
        issues.append("migration status must cover every publication source exactly once")
    return issues


def _registry_ids(root):
    ids = set()
    semantic_key = re.compile(
        r"(?:^id$|_id$|^alias$|^symbol$|^registry_symbol$|"
        r"status|vocabulary|enum)"
    )
    semantic_token = re.compile(
        r"^(?:(?:ARG|ATH|FCSP|ER)-[A-Z0-9]+|"
        r"[A-Z][A-Z0-9]*(?:[-_][A-Za-z0-9]+)+)$"
    )

    def collect(value, owner_key=""):
        if isinstance(value, dict):
            for key, child in value.items():
                if owner_key == "legacy_aliases":
                    if isinstance(key, str):
                        ids.add(key)
                    if isinstance(child, str):
                        ids.add(child)
                if isinstance(key, str) and semantic_token.fullmatch(key):
                    ids.add(key)
                if (
                    isinstance(key, str)
                    and semantic_key.search(key)
                    and isinstance(child, str)
                ):
                    ids.add(child)
                collect(child, key if isinstance(key, str) else "")
        elif isinstance(value, list):
            for child in value:
                if (
                    isinstance(child, str)
                    and (
                        semantic_key.search(owner_key)
                        or semantic_token.fullmatch(child)
                    )
                ):
                    ids.add(child)
                collect(child, owner_key)

    for rel in (
        "docs/verdict-registry.yaml",
        "docs/notation-registry.yaml",
        "experiments/experiment-status.yaml",
        "references/source-status.yaml",
        "companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml",
    ):
        path = os.path.join(root, rel)
        if os.path.exists(path):
            collect(yaml.safe_load(io.open(path, encoding="utf-8")))
    schema_path = os.path.join(root, "schemas/handoff.schema.json")
    if os.path.exists(schema_path):
        collect(json.load(io.open(schema_path, encoding="utf-8")))
    return ids


def validate_inventory(root=ROOT):
    root = os.fspath(root)
    inventory_path = os.path.join(root, "docs/math-source-inventory.yaml")
    migration_path = os.path.join(root, "docs/math-migration-status.yaml")
    try:
        inventory = yaml.safe_load(io.open(inventory_path, encoding="utf-8"))
        migration = yaml.safe_load(io.open(migration_path, encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return ["inventory load: %s" % exc]
    source_texts = {}
    if isinstance(inventory, dict):
        for source in inventory.get("sources", []):
            if not isinstance(source, dict) or not isinstance(source.get("file"), str):
                continue
            path = os.path.join(root, source["file"])
            if os.path.exists(path):
                source_texts[source["file"]] = io.open(path, encoding="utf-8").read()
    issues = validate_inventory_data(inventory, source_texts, _registry_ids(root))
    issues.extend(validate_migration_data(migration, inventory))
    return issues


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def main():
    reg = yaml.safe_load(read("docs/notation-registry.yaml"))
    symbols = [s["symbol"] for s in reg["symbols"]]
    rmap = reg.get("render_map", [])
    rm_syms = [e["registry_symbol"] for e in rmap]

    # 1. bijection
    missing = [s for s in symbols if s not in rm_syms]
    orphan = [s for s in rm_syms if s not in symbols]
    check("render_map covers every normative symbol", not missing, "missing: %s" % missing)
    check("render_map has no orphan (all map to a live symbol)", not orphan, "orphan: %s" % orphan)
    check("render_map has no duplicate registry_symbol",
          len(rm_syms) == len(set(rm_syms)),
          "dupes: %s" % [s for s in rm_syms if rm_syms.count(s) > 1])

    # 2. every latex translates
    gallery_text = read(GALLERY)
    for e in rmap:
        try:
            translate_inline(e["latex"])
            ok = True
            detail = ""
        except MathConvertError as ex:
            ok = False
            detail = str(ex)
        check("render_map latex translates: %s" % e["registry_symbol"], ok, detail)
        # 3. gallery drift
        check("gallery renders symbol %s" % e["registry_symbol"],
              ("$" + e["latex"] + "$") in gallery_text or e["latex"] in gallery_text,
              "latex not found verbatim in %s" % GALLERY)

    # 4. every math source span across the corpus (a) carries no precomposed
    #    combining accent and (b) translates cleanly through the strict subset —
    #    so no shipped math source can render broken or use the notdef antipattern.
    scan_roots = ["manuscript", "theory", "companion", "docs", "applications"]
    bad_accents = []
    bad_translate = []
    for r in scan_roots:
        base = os.path.join(ROOT, r)
        if not os.path.isdir(base):
            continue
        for dp, dirs, fns in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace("\\", "/")
                text = io.open(os.path.join(dp, fn), encoding="utf-8").read()
                for kind, sp in real_math_spans(text):
                    if COMBINING.search(sp):
                        bad_accents.append("%s: %r" % (rel, sp[:40]))
                    try:
                        translate_inline(sp) if kind == "i" else translate_display(sp)
                    except MathConvertError as ex:
                        bad_translate.append("%s: %r -> %s" % (rel, sp[:30], ex))
    check("no precomposed combining accents in publication math source",
          not bad_accents, "; ".join(bad_accents[:5]))
    check("every math source span translates through the strict subset",
          not bad_translate, "; ".join(bad_translate[:5]))

    # 5. migration manifest covers every build source doc
    mig = yaml.safe_load(read("docs/math-migration-status.yaml"))
    listed = set()
    for d in mig["documents"]:
        for s in d.get("sources", []):
            listed.add(s)
    profile = yaml.safe_load(read("docs/publication-profile.yaml"))
    profile_sources = {
        source
        for artifact in profile.get("artifacts", [])
        for source in artifact.get("sources", [])
    }
    # Derive build sources from the literal DOCS compatibility owner only.
    # Other repository paths in the builder are not publication source inputs.
    bp = read("scripts/build_pdfs.py")
    build_sources = extract_build_sources(bp)
    build_source_issues = validate_build_source_parity(
        build_sources, profile_sources
    )
    check("math-migration-status has exact build-source parity",
          not build_source_issues, "; ".join(build_source_issues))
    migration_profile_issues = validate_build_source_parity(
        listed, profile_sources
    )
    check("math-migration-status has exact publication-profile source parity",
          not migration_profile_issues, "; ".join(migration_profile_issues))

    # 6. Task 11 replaces the global text allowlist with exact, bidirectional
    #    file/locus/occurrence ownership for all seven publication sources.
    inventory_issues = validate_inventory(ROOT)
    check("publication inline-code inventory has exact bidirectional parity",
          not inventory_issues, "; ".join(inventory_issues[:5]))

    # 7. The existing CI entry point also owns the deferred publication profile.
    profile_issues = validate_profile(ROOT)
    check("publication profile is schema-valid and preserves deferred ownership",
          not profile_issues, "; ".join(profile_issues[:5]))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
