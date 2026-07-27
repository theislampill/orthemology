#!/usr/bin/env python3
"""Generate deterministic LaTeX derivatives from publication Markdown owners."""

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

import yaml
from markdown_it import MarkdownIt

from latex_to_typst_math import MathConvertError, translate_display, translate_inline


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILE_PATH = pathlib.Path("docs/publication-profile.yaml")
OUTPUT_PATH = pathlib.Path("publication/latex")
LONG_TABLE_ROW_THRESHOLD = 10
LONG_TABLE_TOTAL_CONTENT_THRESHOLD = 1500
LONG_TABLE_MAX_ROW_CONTENT_THRESHOLD = 800
BREAKABLE_TABLE_COLUMN_THRESHOLD = 5
DISPLAY_MATH_MULTLINE_THRESHOLD = 180
DISPLAY_MATH_TARGET_WIDTH = 72
DISPLAY_MATH_LAYOUT_BREAK = "\\\\\n"
REVIEWED_DISPLAY_MATH_BREAK_COMMANDS = frozenset(
    {
        r"\iff",
        r"\implies",
        r"\Leftrightarrow",
        r"\Longrightarrow",
        r"\Rightarrow",
        r"\vee",
        r"\wedge",
    }
)
INLINE_CODE_PATH_LAYOUT_BREAK = r"\allowbreak{}"
INLINE_CODE_PATH_BREAK_CHARACTERS = frozenset("/-._")
INLINE_CODE_PATH_SEGMENT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
DECLARED_REPOSITORY_INLINE_CODE_ROOTS = frozenset(
    {
        "applications",
        "artifacts",
        "companion",
        "docs",
        "examples",
        "experiments",
        "references",
        "schemas",
        "scripts",
        "terminology",
        "tests",
        "theory",
    }
)
DECLARED_EXTERNAL_REPOSITORY_SLUGS = frozenset(
    {
        "theislampill/daee-epistemics",
    }
)
DECLARED_SOURCE_RELATIVE_INLINE_CODE_PATHS = frozenset(
    {
        "sourcing/R3-COMPANION-SOURCING-LEDGER.md",
    }
)
PLACEHOLDER_OPEN = "\ue000"
PLACEHOLDER_CLOSE = "\ue001"
PLACEHOLDER_RE = re.compile(
    re.escape(PLACEHOLDER_OPEN) + r"(\d+)" + re.escape(PLACEHOLDER_CLOSE)
)
PURE_COMMENT_RE = re.compile(r"\s*(?:<!--.*?-->\s*)+", re.S)


class GenerationError(ValueError):
    """Raised when Markdown cannot be represented by the bounded LaTeX writer."""


def _is_escaped(text, index):
    slash_count = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        slash_count += 1
        index -= 1
    return slash_count % 2 == 1


def _find_closing_dollar(text, start, delimiter):
    index = start
    while True:
        index = text.find(delimiter, index)
        if index < 0:
            return -1
        if not _is_escaped(text, index):
            if delimiter == "$" and "\n" in text[start:index]:
                return -1
            return index
        index += len(delimiter)


def _fence_end(text, start, marker):
    line_end = text.find("\n", start)
    if line_end < 0:
        return len(text)
    pattern = re.compile(
        r"(?m)^ {0,3}" + re.escape(marker[0]) + "{%d,}\\s*$" % len(marker)
    )
    match = pattern.search(text, line_end + 1)
    if match is None:
        raise GenerationError("unclosed fenced code block")
    close_end = text.find("\n", match.end())
    return len(text) if close_end < 0 else close_end + 1


def _find_closing_backtick_run(text, start, run_length):
    cursor = start
    while True:
        closing = text.find("`", cursor)
        if closing < 0:
            return -1
        closing_end = closing + 1
        while closing_end < len(text) and text[closing_end] == "`":
            closing_end += 1
        if closing_end - closing == run_length:
            return closing_end
        cursor = closing_end


def _protect_math(markdown):
    if PLACEHOLDER_OPEN in markdown or PLACEHOLDER_CLOSE in markdown:
        raise GenerationError("source contains reserved math placeholder")
    protected = []
    math = []
    index = 0
    line_start = True
    while index < len(markdown):
        if line_start:
            fence_match = re.match(r" {0,3}(`{3,}|~{3,})[^\n]*(?:\n|$)", markdown[index:])
            if fence_match:
                marker = fence_match.group(1)
                end = _fence_end(markdown, index, marker)
                protected.append(markdown[index:end])
                index = end
                line_start = index == 0 or markdown[index - 1] == "\n"
                continue
        char = markdown[index]
        if char == "`":
            run = 1
            while index + run < len(markdown) and markdown[index + run] == "`":
                run += 1
            end = _find_closing_backtick_run(markdown, index + run, run)
            if end < 0:
                raise GenerationError("unclosed inline-code delimiter")
            protected.append(markdown[index:end])
            index = end
            line_start = False
            continue
        if char == "\\" and index + 1 < len(markdown):
            protected.append(markdown[index : index + 2])
            line_start = markdown[index + 1] == "\n"
            index += 2
            continue
        if char == "$":
            delimiter = "$$" if markdown.startswith("$$", index) else "$"
            body_start = index + len(delimiter)
            end = _find_closing_dollar(markdown, body_start, delimiter)
            if end < 0:
                raise GenerationError(
                    "unclosed %s math delimiter" % ("display" if delimiter == "$$" else "inline")
                )
            body = markdown[body_start:end]
            if not body.strip():
                raise GenerationError("empty math delimiter")
            kind = "display" if delimiter == "$$" else "inline"
            try:
                if kind == "display":
                    translate_display(body)
                else:
                    translate_inline(body)
            except MathConvertError as exc:
                raise GenerationError("math translation failed: %s" % exc) from exc
            math.append((kind, body))
            protected.append(
                PLACEHOLDER_OPEN + str(len(math) - 1) + PLACEHOLDER_CLOSE
            )
            index = end + len(delimiter)
            line_start = False
            continue
        protected.append(char)
        line_start = char == "\n"
        index += 1
    return "".join(protected), math


TEXT_ESCAPES = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def _escape_text(text):
    return "".join(TEXT_ESCAPES.get(char, char) for char in text)


def _escape_code(text):
    escaped = _escape_text(text)
    return escaped.replace(r"\$", r"\char36{}")


def _inline_code_path_segments(text):
    if (
        "/" not in text
        or any(character.isspace() for character in text)
        or "://" in text
        or text.startswith("--")
        or "//" in text
    ):
        return None
    body = text[:-1] if text.endswith("/") else text
    if not body:
        return None
    segments = tuple(body.split("/"))
    if not all(INLINE_CODE_PATH_SEGMENT_RE.fullmatch(item) for item in segments):
        return None
    return segments


def is_path_like_inline_code(text):
    """Accept only closed repository paths and exact declared exceptions."""
    segments = _inline_code_path_segments(text)
    if segments is None:
        return False
    return (
        segments[0] in DECLARED_REPOSITORY_INLINE_CODE_ROOTS
        or text in DECLARED_EXTERNAL_REPOSITORY_SLUGS
        or text in DECLARED_SOURCE_RELATIVE_INLINE_CODE_PATHS
    )


def _tracked_repository_paths(root):
    try:
        result = subprocess.run(
            ["git", "-C", str(pathlib.Path(root)), "ls-files", "-z"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GenerationError("cannot enumerate tracked repository paths") from exc
    return {
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    }


def tracked_repository_root_segments(root=ROOT):
    """Return first path segments backed by at least one tracked nested file."""
    roots = set()
    for tracked_path in _tracked_repository_paths(root):
        parts = pathlib.PurePosixPath(tracked_path).parts
        if len(parts) > 1:
            roots.add(parts[0])
    return roots


def validate_inline_code_path_declarations(root=ROOT):
    """Validate closed local and source-relative path declarations."""
    tracked_paths = _tracked_repository_paths(root)
    tracked_roots = {
        pathlib.PurePosixPath(path).parts[0]
        for path in tracked_paths
        if len(pathlib.PurePosixPath(path).parts) > 1
    }
    missing_roots = DECLARED_REPOSITORY_INLINE_CODE_ROOTS - tracked_roots
    if missing_roots:
        raise GenerationError(
            "declared inline-code path roots are not tracked: %s"
            % sorted(missing_roots)
        )
    for relative in DECLARED_SOURCE_RELATIVE_INLINE_CODE_PATHS:
        matches = [
            path
            for path in tracked_paths
            if path == relative or path.endswith("/" + relative)
        ]
        if len(matches) != 1:
            raise GenerationError(
                "source-relative inline-code path must resolve uniquely: %s"
                % relative
            )
    if DECLARED_REPOSITORY_INLINE_CODE_ROOTS & {
        _inline_code_path_segments(path)[0]
        for path in DECLARED_EXTERNAL_REPOSITORY_SLUGS
    }:
        raise GenerationError(
            "external repository slugs overlap declared local roots"
        )


def remove_inline_code_path_layout_breaks(body):
    """Remove only discretionary breaks inserted in a validated inline path."""
    return body.replace(INLINE_CODE_PATH_LAYOUT_BREAK, "")


def _render_inline_code(text):
    escaped = _escape_code(text)
    if not is_path_like_inline_code(text):
        return escaped
    output = []
    for character in text:
        output.append(_escape_code(character))
        if character in INLINE_CODE_PATH_BREAK_CHARACTERS:
            output.append(INLINE_CODE_PATH_LAYOUT_BREAK)
    layout_body = "".join(output)
    if remove_inline_code_path_layout_breaks(layout_body) != escaped:
        raise GenerationError("inline-code path layout changed the source token stream")
    return layout_body


def reviewed_display_math_break_positions(body):
    """Return reviewed top-level token boundaries that can take a layout break."""
    positions = []
    brace_depth = 0
    parenthesis_depth = 0
    bracket_depth = 0
    index = 0
    while index < len(body):
        character = body[index]
        if character == "\\":
            command_end = index + 1
            if command_end < len(body) and body[command_end].isalpha():
                while command_end < len(body) and body[command_end].isalpha():
                    command_end += 1
            elif command_end < len(body):
                command_end += 1
            command = body[index:command_end]
            if (
                brace_depth == 0
                and parenthesis_depth == 0
                and bracket_depth == 0
                and command in REVIEWED_DISPLAY_MATH_BREAK_COMMANDS
            ):
                positions.append(command_end)
            index = command_end
            continue
        if character == "{":
            brace_depth += 1
        elif character == "}":
            brace_depth = max(0, brace_depth - 1)
        elif brace_depth == 0:
            if character == "(":
                parenthesis_depth += 1
            elif character == ")":
                parenthesis_depth = max(0, parenthesis_depth - 1)
            elif character == "[":
                bracket_depth += 1
            elif character == "]":
                bracket_depth = max(0, bracket_depth - 1)
            elif (
                character in ",;"
                and parenthesis_depth == 0
                and bracket_depth == 0
            ):
                positions.append(index + 1)
        index += 1
    return positions


def remove_display_math_layout_breaks(body):
    """Remove only layout breaks inserted by the long-display renderer."""
    return body.replace(DISPLAY_MATH_LAYOUT_BREAK, "")


def _multline_break_positions(body):
    candidates = reviewed_display_math_break_positions(body)
    selected = []
    line_start = 0
    while len(body) - line_start > DISPLAY_MATH_TARGET_WIDTH:
        remaining = [
            position
            for position in candidates
            if line_start < position < len(body)
        ]
        if not remaining:
            break
        target = line_start + DISPLAY_MATH_TARGET_WIDTH
        before_target = [position for position in remaining if position <= target]
        position = max(before_target) if before_target else min(remaining)
        selected.append(position)
        line_start = position
    return selected


def _render_display_math(body):
    source = body.strip()
    if (
        len(source) < DISPLAY_MATH_MULTLINE_THRESHOLD
        or r"\begin{" in source
        or r"\end{" in source
        or "\\\\\n" in source
    ):
        return "\n\\[\n%s\n\\]\n" % source
    break_positions = _multline_break_positions(source)
    if not break_positions:
        return "\n\\[\n%s\n\\]\n" % source
    output = []
    cursor = 0
    for position in break_positions:
        output.append(source[cursor:position])
        output.append(DISPLAY_MATH_LAYOUT_BREAK)
        cursor = position
    output.append(source[cursor:])
    layout_body = "".join(output)
    if remove_display_math_layout_breaks(layout_body) != source:
        raise GenerationError("display-math layout changed the source token stream")
    return "\n\\begin{multline*}\n%s\n\\end{multline*}\n" % layout_body


def _render_text(text, math):
    output = []
    cursor = 0
    for match in PLACEHOLDER_RE.finditer(text):
        output.append(_escape_text(text[cursor : match.start()]))
        kind, body = math[int(match.group(1))]
        if kind == "display":
            output.append(_render_display_math(body))
        else:
            output.append("$%s$" % body)
        cursor = match.end()
    output.append(_escape_text(text[cursor:]))
    return "".join(output)


def _escape_url(url):
    if "}" in url:
        raise GenerationError("link target contains an unsupported closing brace")
    return r"\detokenize{%s}" % url


def _render_inline(tokens, math):
    output = []
    for token in tokens:
        kind = token.type
        if kind == "text":
            output.append(_render_text(token.content, math))
        elif kind == "code_inline":
            output.append(r"\texttt{%s}" % _render_inline_code(token.content))
        elif kind == "strong_open":
            output.append(r"\textbf{")
        elif kind == "strong_close":
            output.append("}")
        elif kind == "em_open":
            output.append(r"\emph{")
        elif kind == "em_close":
            output.append("}")
        elif kind == "s_open":
            output.append(r"\textcolor{gray}{")
        elif kind == "s_close":
            output.append("}")
        elif kind == "link_open":
            output.append(r"\href{%s}{" % _escape_url(token.attrGet("href") or ""))
        elif kind == "link_close":
            output.append("}")
        elif kind == "softbreak":
            output.append(" ")
        elif kind == "hardbreak":
            output.append("\\\\\n")
        elif kind == "image":
            raise GenerationError("images are not supported")
        elif kind == "html_inline":
            if not PURE_COMMENT_RE.fullmatch(token.content):
                raise GenerationError("raw inline HTML is not supported")
            if output:
                output[-1] = output[-1].rstrip(" \t")
        else:
            raise GenerationError("unhandled inline token: %s" % kind)
    return "".join(output)


def _column_spec(count):
    width = max(0.06, min(0.47, 0.94 / max(count, 1)))
    return "@{}" + "".join("p{%.3f\\linewidth}" % width for _ in range(count)) + "@{}"


def table_requires_breakable_rows(
    data_rows,
    total_rendered_characters,
    max_row_rendered_characters,
    columns,
):
    """Return whether a table needs normal-flow, page-breakable row blocks."""
    return data_rows > 0 and (
        data_rows >= LONG_TABLE_ROW_THRESHOLD
        or total_rendered_characters >= LONG_TABLE_TOTAL_CONTENT_THRESHOLD
        or max_row_rendered_characters >= LONG_TABLE_MAX_ROW_CONTENT_THRESHOLD
        or columns >= BREAKABLE_TABLE_COLUMN_THRESHOLD
    )


def _table_shape(table):
    row_lengths = [len(table["header"])] + [
        len(row) for row in table["rows"]
    ]
    columns = max(row_lengths or [1])
    rows = [
        row + [""] * (columns - len(row))
        for row in table["rows"]
    ]
    row_rendered_characters = [
        sum(len(cell) for cell in row)
        for row in rows
    ]
    total_rendered_characters = sum(
        len(cell)
        for row in [table["header"], *rows]
        for cell in row
    )
    return (
        columns,
        rows,
        total_rendered_characters,
        max(row_rendered_characters, default=0),
    )


def _render_standard_table(table, columns, rows):
    output = [
        "\n\\begin{center}\n\\begin{tabular}{%s}\n\\toprule\n"
        % _column_spec(columns)
    ]
    if table["header"]:
        output.append(
            " & ".join(r"\textbf{%s}" % cell for cell in table["header"])
            + " \\\\\n\\midrule\n"
        )
    for row in rows:
        output.append(" & ".join(row) + " \\\\\n")
    output.append("\\bottomrule\n\\end{tabular}\n\\end{center}\n")
    return "".join(output)


def _normal_flow_header_label(header, column_index):
    label = header if header else "Column %d" % (column_index + 1)
    if label.startswith(r"\textbf{") and label.endswith("}"):
        label = label[len(r"\textbf{") : -1]
    return r"\textbf{%s}:" % label


def _render_breakable_table(
    table,
    columns,
    rows,
    total_rendered_characters,
    max_row_rendered_characters,
):
    headers = table["header"] + [""] * (columns - len(table["header"]))
    output = [
        (
            "\n%% breakable-row-table: data-rows=%d "
            "total-rendered-characters=%d max-row-rendered-characters=%d\n"
        )
        % (
            len(rows),
            total_rendered_characters,
            max_row_rendered_characters,
        ),
        "\\par\\medskip\n",
        "\\hrule height 0.8pt\n",
        "\\smallskip\n",
    ]
    for row_index, row in enumerate(rows):
        output.append(
            "%% breakable-row: %d/%d\n" % (row_index + 1, len(rows))
        )
        for column_index, cell in enumerate(row):
            output.append(
                "\\noindent%s %s\\par\n"
                % (
                    _normal_flow_header_label(
                        headers[column_index],
                        column_index,
                    ),
                    cell,
                )
            )
        if row_index != len(rows) - 1:
            output.extend(
                [
                    "\\smallskip\n",
                    "\\hrule height 0.4pt\n",
                    "\\smallskip\n",
                ]
            )
    output.extend(
        [
            "\\smallskip\n",
            "\\hrule height 0.8pt\n",
            "\\par\\medskip\n",
        ]
    )
    return "".join(output)


def _render_table(table):
    (
        columns,
        rows,
        total_rendered_characters,
        max_row_rendered_characters,
    ) = _table_shape(table)
    if table_requires_breakable_rows(
        len(rows),
        total_rendered_characters,
        max_row_rendered_characters,
        columns,
    ):
        return _render_breakable_table(
            table,
            columns,
            rows,
            total_rendered_characters,
            max_row_rendered_characters,
        )
    return _render_standard_table(table, columns, rows)


def render_markdown(markdown, source_name="<memory>"):
    """Render bounded CommonMark, tables, code, links, and canonical math."""
    try:
        protected, math = _protect_math(markdown)
        tokens = MarkdownIt("commonmark").enable("table").enable("strikethrough").parse(
            protected
        )
    except GenerationError:
        raise
    except Exception as exc:
        raise GenerationError("%s: Markdown parse failed: %s" % (source_name, exc)) from exc

    output = []
    index = 0
    list_stack = []
    table = None
    appendix_active = False
    while index < len(tokens):
        token = tokens[index]
        kind = token.type
        if kind == "heading_open":
            inline = tokens[index + 1]
            heading_text = inline.content.strip()
            level = int(token.tag[1])
            if level == 2 and "appendix" in heading_text.casefold() and not appendix_active:
                output.append("\n\\onecolumn\n\\appendix\n")
                appendix_active = True
            if level == 2 and re.search(r"\breferences\b", heading_text, re.I) and appendix_active:
                output.append("\n\\twocolumn\n")
                appendix_active = False
            command = {
                1: "part*",
                2: "section",
                3: "subsection",
                4: "subsubsection",
                5: "paragraph",
                6: "subparagraph",
            }[level]
            output.append(
                "\n\\%s{%s}\n"
                % (command, _render_inline(inline.children or [], math))
            )
            index += 3
            continue
        if kind == "paragraph_open":
            inline = tokens[index + 1]
            body = _render_inline(inline.children or [], math)
            output.append(body + ("\n" if list_stack else "\n\n"))
            index += 3
            continue
        if kind == "blockquote_open":
            output.append("\n\\begin{quote}\n")
            index += 1
            continue
        if kind == "blockquote_close":
            output.append("\\end{quote}\n")
            index += 1
            continue
        if kind in ("bullet_list_open", "ordered_list_open"):
            environment = "itemize" if kind == "bullet_list_open" else "enumerate"
            list_stack.append(environment)
            output.append("\n\\begin{%s}\n" % environment)
            index += 1
            continue
        if kind in ("bullet_list_close", "ordered_list_close"):
            environment = list_stack.pop()
            output.append("\\end{%s}\n" % environment)
            index += 1
            continue
        if kind == "list_item_open":
            output.append("\\item ")
            index += 1
            continue
        if kind == "list_item_close":
            output.append("\n")
            index += 1
            continue
        if kind in ("fence", "code_block"):
            info = (getattr(token, "info", "") or "").strip()
            content = token.content.rstrip("\n")
            if info == "math":
                try:
                    translate_display(content)
                except MathConvertError as exc:
                    raise GenerationError(
                        "%s: math fence translation failed: %s" % (source_name, exc)
                    ) from exc
                output.append(_render_display_math(content))
            else:
                if r"\end{verbatim}" in content:
                    raise GenerationError("code block contains an unsafe verbatim terminator")
                output.append("\n\\begin{verbatim}\n%s\n\\end{verbatim}\n" % content)
            index += 1
            continue
        if kind == "hr":
            output.append("\n\\bigskip\\hrule\\bigskip\n")
            index += 1
            continue
        if kind == "table_open":
            table = {"header": [], "rows": []}
            index += 1
            continue
        if kind in ("thead_open", "tbody_open"):
            index += 1
            continue
        if kind == "tr_open":
            table["current"] = []
            index += 1
            continue
        if kind in ("th_open", "td_open"):
            inline = tokens[index + 1]
            cell = (
                _render_inline(inline.children or [], math)
                if inline.type == "inline"
                else ""
            )
            table["current"].append((kind == "th_open", cell))
            index += 3
            continue
        if kind == "tr_close":
            row = table.pop("current")
            if row and all(is_header for is_header, _ in row):
                table["header"] = [cell for _, cell in row]
            else:
                table["rows"].append([cell for _, cell in row])
            index += 1
            continue
        if kind in ("thead_close", "tbody_close"):
            index += 1
            continue
        if kind == "table_close":
            output.append(_render_table(table))
            table = None
            index += 1
            continue
        if kind == "html_block":
            if not PURE_COMMENT_RE.fullmatch(token.content):
                raise GenerationError("raw HTML block is not supported")
            index += 1
            continue
        raise GenerationError("%s: unhandled block token: %s" % (source_name, kind))
    return "".join(output)


def _split_primary_source(markdown):
    lines = markdown.splitlines(keepends=True)
    title_index = next(
        (index for index, line in enumerate(lines) if line.startswith("# ")),
        None,
    )
    if title_index is None:
        raise GenerationError("publication source lacks a level-one title")
    title = lines[title_index][2:].strip()
    remainder = lines[title_index + 1 :]
    h2_indices = [
        index for index, line in enumerate(remainder) if line.startswith("## ")
    ]
    if not h2_indices:
        return title, "".join(remainder), ""
    first_h2 = h2_indices[0]
    if remainder[first_h2].strip().casefold() == "## abstract":
        next_h2 = next(
            (index for index in h2_indices if index > first_h2),
            len(remainder),
        )
        return title, "".join(remainder[:next_h2]), "".join(remainder[next_h2:])
    return title, "".join(remainder[:first_h2]), "".join(remainder[first_h2:])


def _source_comment(path, text):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return "%% source: %s\n%% source-sha256: %s\n" % (path, digest)


def render_artifact(profile, artifact, source_texts):
    """Render one profile artifact from its declared Markdown source owners."""
    source_paths = artifact.get("sources", [])
    if not source_paths:
        raise GenerationError("artifact has no source owner")
    if artifact.get("bibliography_owner") != profile.get("source_ownership", {}).get(
        "bibliography_owner"
    ):
        raise GenerationError("artifact bibliography owner conflicts with profile")
    missing = [path for path in source_paths if path not in source_texts]
    if missing:
        raise GenerationError("missing source owner: %s" % missing)
    title, front_matter, body = _split_primary_source(source_texts[source_paths[0]])
    layout = profile.get("layout", {})
    if layout != {
        "document_class": "article",
        "font_size_pt": 10,
        "paper_size": "us-letter",
        "body_columns": 2,
        "references_columns": 2,
        "front_matter": "full-width-title-and-abstract",
        "technical_appendices": "single-column",
    }:
        raise GenerationError("publication layout diverges from the approved profile")

    comments = ["% GENERATED FILE — DO NOT EDIT; authoritative prose is Markdown.\n"]
    for path in source_paths:
        comments.append(_source_comment(path, source_texts[path]))
    for qualification in artifact.get("source_qualifications", []):
        comments.append("%% source-qualification: %s\n" % qualification)

    packages = profile.get("package_policy", {}).get("supported_packages", [])
    package_lines = ["\\usepackage{%s}\n" % package for package in packages]
    preamble = [
        *comments,
        "\\documentclass[10pt,letterpaper,twocolumn]{article}\n",
        *package_lines,
        "\\geometry{letterpaper,margin=0.75in}\n",
        "\\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue,citecolor=blue}\n",
        "\\setlength{\\emergencystretch}{3em}\n",
        "\\title{%s}\n" % _escape_text(title),
        "\\author{}\n",
        "\\date{}\n",
        "\\begin{document}\n",
        "\\twocolumn[\n",
        "\\maketitle\n",
        render_markdown(front_matter, source_name=source_paths[0]),
        "\\vspace{1em}\n",
        "]\n",
        render_markdown(body, source_name=source_paths[0]),
    ]
    for path in source_paths[1:]:
        preamble.append(render_markdown(source_texts[path], source_name=path))

    bibliography = artifact["bibliography_owner"]
    if pathlib.PurePosixPath(bibliography).is_absolute() or re.match(
        r"^[A-Za-z]:", bibliography
    ):
        raise GenerationError("absolute bibliography path is prohibited")
    bibliography_stem = "../../../" + bibliography.removesuffix(".bib")
    preamble.extend(
        [
            "\n\\twocolumn\n",
            "\\bibliographystyle{plainnat}\n",
            "\\bibliography{%s}\n" % bibliography_stem,
            "\\end{document}\n",
        ]
    )
    return "".join(preamble).replace("\r\n", "\n")


def expected_latex_tree(root, profile=None, artifacts=None):
    root = pathlib.Path(root)
    if (root / ".git").exists():
        validate_inline_code_path_declarations(root)
    if profile is None:
        profile = yaml.safe_load((root / PROFILE_PATH).read_text(encoding="utf-8"))
    if artifacts is None:
        artifacts = profile.get("artifacts", [])
    source_paths = {
        source
        for artifact in artifacts
        for source in artifact.get("sources", [])
    }
    source_texts = {
        source: (root / source).read_text(encoding="utf-8")
        for source in sorted(source_paths)
    }
    tree = {}
    for artifact in artifacts:
        artifact_id = artifact["artifact_id"]
        tree["%s/main.tex" % artifact_id] = render_artifact(
            profile,
            artifact,
            source_texts,
        )
    return tree


def write_latex_tree(output, tree):
    output = pathlib.Path(output)
    for relative, content in sorted(tree.items()):
        target = output / pathlib.PurePosixPath(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def tree_drift(output, tree):
    output = pathlib.Path(output)
    issues = []
    expected_paths = set(tree)
    actual_paths = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    } if output.is_dir() else set()
    for relative in sorted(expected_paths - actual_paths):
        issues.append("missing generated LaTeX: %s" % relative)
    for relative in sorted(actual_paths - expected_paths):
        issues.append("unexpected generated file: %s" % relative)
    for relative in sorted(expected_paths & actual_paths):
        actual = (output / pathlib.PurePosixPath(relative)).read_text(encoding="utf-8")
        if actual != tree[relative]:
            issues.append("generated LaTeX drift: %s" % relative)
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    profile = yaml.safe_load((args.root / PROFILE_PATH).read_text(encoding="utf-8"))
    tree = expected_latex_tree(args.root, profile)
    output = args.root / OUTPUT_PATH
    if args.check:
        issues = tree_drift(output, tree)
        for issue in issues:
            print("[FAIL] %s" % issue)
        if not issues:
            print("[PASS] generated LaTeX tree matches authoritative sources")
        print("TOTAL: %d failures" % len(issues))
        return 1 if issues else 0
    write_latex_tree(output, tree)
    for relative, content in sorted(tree.items()):
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        print("[WRITE] %s %s" % (relative, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
