#!/usr/bin/env python3
"""Build and verify the six governed PDFLaTeX publication artifacts.

The canonical inputs are the Task 12 Markdown and generated LaTeX blobs at the
sidecar's source commit. Each source package uses repository-relative paths,
builds twice in independent clean directories, and runs in the digest-pinned
TeX Live container with networking and shell escape disabled.
"""
import argparse
import datetime
import gzip
import hashlib
import io
import json
import os
import pathlib
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unicodedata
import urllib.parse

import yaml
from pypdf import PdfReader


ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
PROFILE_PATH = pathlib.Path("docs/publication-profile.yaml")
LOCK_PATH = pathlib.Path("publication/toolchain-lock.yaml")
CANDIDATE_PATH = pathlib.Path("docs/current-candidate-state.yaml")
BIB_PATH = pathlib.Path("references/orthemology.bib")
LATEXMKRC_PATH = pathlib.Path("publication/latexmkrc")
PDFTEX_COMPAT_PATH = pathlib.Path("publication/pdftex-unicode-compat.tex")
COMPATIBILITY_REPORT_PATH = pathlib.Path(
    "docs/project-closure/r7e-sol/R7E-SOL-ARXIV-COMPATIBILITY.md"
)
BIBTEX_STATUS_NAME = "main.bibtex.rc"
EXPECTED_BIBLIOGRAPHY_DATABASE = "../../../references/orthemology.bib"
EXPECTED_BIBLIOGRAPHY_AUX_DATABASE = "../../../references/orthemology"
EXPECTED_BIBLIOGRAPHY_STYLE = "plainnat"
EMPTY_BIBLIOGRAPHY_DISPOSITION = "EMPTY_BIBLIOGRAPHY_NO_CITATIONS"
NONEMPTY_BIBLIOGRAPHY_DISPOSITION = "NONEMPTY_BIBLIOGRAPHY"
CANONICAL_EMPTY_BBL = (
    "\\begin{thebibliography}{0}\n"
    "\\providecommand{\\natexlab}[1]{#1}\n"
    "\\providecommand{\\url}[1]{\\texttt{#1}}\n"
    "\\expandafter\\ifx\\csname urlstyle\\endcsname\\relax\n"
    "  \\providecommand{\\doi}[1]{doi: #1}\\else\n"
    "  \\providecommand{\\doi}{doi: \\begingroup \\urlstyle{rm}\\Url}\\fi\n"
    "\n"
    "\\end{thebibliography}\n"
).encode("utf-8")
EXPECTED_TEX_PACKAGES = {
    "fvextra": {
        "tex_live_package": "fvextra",
        "revision": 78177,
        "version": "1.14.0",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "fvextra/fvextra.sty"
        ),
        "role": "compatibility-direct",
    },
    "fancyvrb": {
        "tex_live_package": "fancyvrb",
        "revision": 77677,
        "version": "4.6",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "fancyvrb/fancyvrb.sty"
        ),
        "role": "fvextra-required",
    },
    "etoolbox": {
        "tex_live_package": "etoolbox",
        "revision": 77677,
        "version": "2.5m",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "etoolbox/etoolbox.sty"
        ),
        "role": "fvextra-required",
    },
    "upquote": {
        "tex_live_package": "upquote",
        "revision": 77677,
        "version": "1.3",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "upquote/upquote.sty"
        ),
        "role": "fvextra-required",
    },
    "textcomp": {
        "tex_live_package": "latex",
        "revision": 76924,
        "version": "2.1b",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "base/textcomp.sty"
        ),
        "role": "fvextra-required",
    },
    "lineno": {
        "tex_live_package": "lineno",
        "revision": 77890,
        "version": "5.7",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "lineno/lineno.sty"
        ),
        "role": "fvextra-required",
    },
    "keyval": {
        "tex_live_package": "graphics",
        "revision": 75374,
        "version": "1.15",
        "path": (
            "/usr/local/texlive/2025/texmf-dist/tex/latex/"
            "graphics/keyval.sty"
        ),
        "role": "fancyvrb-required",
    },
}

# Compatibility surface for the Task 11 parity validator. Runtime ownership is
# the typed publication profile loaded by artifact_specs().
DOCS = [
    (
        "orthemma-ortheme-systems-draft",
        ["manuscript/orthemma-ortheme-systems-revised-draft.md"],
    ),
    (
        "orthemic-core-reference-draft",
        [
            "theory/orthemic-core-formalization.md",
            "theory/orthemic-multi-actor-conflict-note.md",
        ],
    ),
    (
        "orthability-ground-of-intelligibility-draft",
        ["companion/orthability-and-the-ground-of-intelligibility.md"],
    ),
    (
        "orthability-divine-speech-athari-draft",
        ["companion/orthability-divine-attributes-and-speech-athari.md"],
    ),
    (
        "dynamic-orthing-noetic-learning-orthability-draft",
        ["companion/dynamic-orthing-noetic-learning-and-orthability.md"],
    ),
    ("notation-gallery", ["docs/notation-gallery.md"]),
]

RAW_MD_PATTERNS = [
    (r"\|\s*-{3,}\s*\|", "pipe table delimiter row"),
    (r"^\s*>\s+\w", "literal blockquote marker"),
    (r"\[[^\]\n]{2,}\]\(https?://", "raw Markdown link syntax"),
    (r"^---\s*$", "standalone Markdown rule"),
]


class PipelineError(RuntimeError):
    pass


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(pathlib.Path(path).read_bytes())


def json_bytes(value):
    return (
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    ).encode("utf-8")


def compatibility_artifact_rows(root):
    """Derive the compatibility evidence table from committed artifact owners."""
    root = pathlib.Path(root)
    rows = []
    for artifact_id, _sources in DOCS:
        pdf_path = root / "artifacts" / (artifact_id + ".pdf")
        archive_path = root / "artifacts" / (artifact_id + ".source.tar.gz")
        manifest_path = root / "artifacts" / (
            artifact_id + ".source-manifest.json"
        )
        for path in (pdf_path, archive_path, manifest_path):
            if not path.is_file():
                raise PipelineError(
                    "compatibility report owner is missing: %s"
                    % path.relative_to(root).as_posix()
                )
        rows.append(
            {
                "artifact_id": artifact_id,
                "pages": len(PdfReader(str(pdf_path)).pages),
                "pdf_sha256": sha256_file(pdf_path),
                "source_archive_sha256": sha256_file(archive_path),
                "source_manifest_sha256": sha256_file(manifest_path),
            }
        )
    return rows


def render_compatibility_artifact_table(root):
    lines = [
        "| Artifact | Pages | PDF SHA-256 | Source archive SHA-256 | "
        "Source manifest SHA-256 |",
        "|---|---:|---|---|---|",
    ]
    for row in compatibility_artifact_rows(root):
        lines.append(
            "| `%s` | %d | `%s` | `%s` | `%s` |"
            % (
                row["artifact_id"],
                row["pages"],
                row["pdf_sha256"],
                row["source_archive_sha256"],
                row["source_manifest_sha256"],
            )
        )
    return "\n".join(lines)


def is_total_page_record_candidate(line):
    """Recognize semantic total markers despite Unicode punctuation variants."""
    normalized = unicodedata.normalize("NFKD", line).casefold()
    marker = ["total", "final", "page", "count"]
    token_text = []
    collapsed = []
    for character in normalized:
        category = unicodedata.category(character)
        if category.startswith("M"):
            continue
        if character.isalnum():
            token_text.append(character)
            collapsed.append(character)
        else:
            token_text.append(" ")
    tokens = "".join(token_text).split()
    return any(
        tokens[index : index + len(marker)] == marker
        for index in range(len(tokens) - len(marker) + 1)
    ) or "".join(marker) in "".join(collapsed)


def compatibility_report_table_issues(root):
    """Return field-specific drift between the report table and artifact owners."""
    root = pathlib.Path(root)
    report_path = root / COMPATIBILITY_REPORT_PATH
    if not report_path.is_file():
        return ["compatibility report is missing"]
    text = report_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    expected_table_lines = render_compatibility_artifact_table(root).splitlines()
    table_header = expected_table_lines[0]
    header_indexes = [
        index for index, line in enumerate(lines) if line == table_header
    ]
    issues = []
    if len(header_indexes) != 1:
        issues.append(
            "compatibility report must contain exactly one artifact table region"
        )
    else:
        start = header_indexes[0]
        end = start
        while end < len(lines) and lines[end].strip():
            end += 1
        if lines[start:end] != expected_table_lines:
            issues.append(
                "compatibility report artifact table region is not exact"
            )
    row_pattern = re.compile(
        r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \| "
        r"`([0-9a-f]{64})` \| `([0-9a-f]{64})` \|$",
        re.M,
    )
    row_matches = list(row_pattern.finditer(text))
    row_ids = [match.group(1) for match in row_matches]
    duplicate_ids = sorted(
        artifact_id
        for artifact_id in set(row_ids)
        if row_ids.count(artifact_id) > 1
    )
    if duplicate_ids:
        issues.append(
            "compatibility report has duplicate artifact rows: %r"
            % duplicate_ids
        )
    reported = {
        match.group(1): {
            "pages": int(match.group(2)),
            "pdf_sha256": match.group(3),
            "source_archive_sha256": match.group(4),
            "source_manifest_sha256": match.group(5),
        }
        for match in row_matches
    }
    expected_rows = compatibility_artifact_rows(root)
    expected_ids = [row["artifact_id"] for row in expected_rows]
    if row_ids != expected_ids:
        issues.append(
            "compatibility report artifact order differs: expected %r, got %r"
            % (expected_ids, row_ids)
        )
    labels = {
        "pages": "page count",
        "pdf_sha256": "PDF SHA-256",
        "source_archive_sha256": "source archive SHA-256",
        "source_manifest_sha256": "source manifest SHA-256",
    }
    for expected in expected_rows:
        artifact_id = expected["artifact_id"]
        actual = reported.get(artifact_id)
        if actual is None:
            issues.append(
                "%s compatibility report row is missing" % artifact_id
            )
            continue
        for field, label in labels.items():
            if actual.get(field) != expected[field]:
                issues.append(
                    "%s %s differs from owner" % (artifact_id, label)
                )
    expected_total = sum(row["pages"] for row in expected_rows)
    total_record_indexes = [
        index
        for index, line in enumerate(lines)
        if is_total_page_record_candidate(line)
    ]
    total_match = (
        re.fullmatch(
            r"Total final page count: `(0|[1-9][0-9]{0,5})`\.",
            lines[total_record_indexes[0]],
        )
        if len(total_record_indexes) == 1
        else None
    )
    if total_match is None:
        issues.append(
            "compatibility report must contain exactly one total page count"
        )
    elif int(total_match.group(1)) != expected_total:
        issues.append("compatibility report total page count differs from owners")
    elif (
        len(header_indexes) != 1
        or total_record_indexes[0]
        != header_indexes[0] + len(expected_table_lines) + 1
    ):
        issues.append(
            "compatibility report total page count is not in canonical table position"
        )
    return issues


def rewrite_compatibility_artifact_table(root):
    root = pathlib.Path(root)
    report_path = root / COMPATIBILITY_REPORT_PATH
    text = report_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"^\| Artifact \| Pages \| PDF SHA-256 \| Source archive SHA-256 \| "
        r"Source manifest SHA-256 \|\n"
        r"^\|---\|---:\|---\|---\|---\|\n"
        r"(?:^\| `[^`]+` \| \d+ \| `[0-9a-f]{64}` \| `[0-9a-f]{64}` "
        r"\| `[0-9a-f]{64}` \|\n?)+",
        re.M,
    )
    replacement = render_compatibility_artifact_table(root) + "\n"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise PipelineError("compatibility report artifact table is malformed")
    expected_total = sum(
        row["pages"] for row in compatibility_artifact_rows(root)
    )
    updated_lines = updated.splitlines()
    total_record_indexes = [
        index
        for index, line in enumerate(updated_lines)
        if is_total_page_record_candidate(line)
    ]
    if (
        len(total_record_indexes) != 1
        or re.fullmatch(
            r"Total final page count: `(?:0|[1-9][0-9]{0,5})`\.",
            updated_lines[total_record_indexes[0]],
        )
        is None
    ):
        raise PipelineError(
            "compatibility report must contain exactly one total page count"
        )
    header_indexes = [
        index
        for index, line in enumerate(updated_lines)
        if line == render_compatibility_artifact_table(root).splitlines()[0]
    ]
    expected_table_line_count = len(
        render_compatibility_artifact_table(root).splitlines()
    )
    if (
        len(header_indexes) != 1
        or total_record_indexes[0]
        != header_indexes[0] + expected_table_line_count + 1
    ):
        raise PipelineError(
            "compatibility report total page count is not in canonical table position"
        )
    updated, total_count = re.subn(
        r"^Total final page count: `(?:0|[1-9][0-9]{0,5})`\.$",
        "Total final page count: `%d`." % expected_total,
        updated,
        count=1,
        flags=re.M,
    )
    if total_count != 1:
        raise PipelineError("compatibility report total page count is missing")
    report_path.write_text(updated, encoding="utf-8", newline="\n")


def run(command, *, cwd=ROOT, timeout=300, env=None):
    return subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )


def configure_utf8_diagnostics():
    """Keep Unicode validation failures printable on every supported console."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="backslashreplace")


def git(*args, text=True, root=ROOT):
    result = subprocess.run(
        ["git", *args],
        cwd=str(pathlib.Path(root)),
        capture_output=True,
        text=text,
        check=False,
    )
    if result.returncode:
        detail = result.stderr if text else result.stderr.decode(errors="replace")
        raise PipelineError("git %s failed: %s" % (" ".join(args), detail.strip()))
    return result.stdout


def git_head(*, root=ROOT):
    return git("rev-parse", "HEAD", root=root).strip()


def validate_commit(commit, *, root=ROOT):
    if not re.fullmatch(r"[0-9a-f]{40}", commit or ""):
        raise PipelineError("source commit must be a full lowercase SHA-1")
    result = run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=root,
    )
    if result.returncode:
        raise PipelineError("source commit is unavailable: %s" % commit)


def git_blob(commit, relative_path, *, root=ROOT):
    relative = pathlib.PurePosixPath(str(relative_path).replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise PipelineError("unsafe repository path: %s" % relative_path)
    return git(
        "show",
        "%s:%s" % (commit, relative.as_posix()),
        text=False,
        root=root,
    )


def git_commit_epoch(commit, *, root=ROOT):
    value = git(
        "show",
        "-s",
        "--format=%ct",
        commit,
        root=root,
    ).strip()
    if not value.isdigit():
        raise PipelineError("source commit has no numeric committer epoch")
    return int(value)


def git_tree(commit, *, root=ROOT):
    return git("rev-parse", commit + "^{tree}", root=root).strip()


def load_profile(root=ROOT):
    path = pathlib.Path(root) / PROFILE_PATH
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_toolchain_lock(root=ROOT):
    path = pathlib.Path(root) / LOCK_PATH
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_source_provenance(
    profile,
    lock,
    requested_commit=None,
    *,
    root=ROOT,
):
    """Return the pinned active source ancestor after exact tree validation."""
    profile_record = profile.get("source_provenance")
    lock_record = lock.get("source_provenance")
    if not isinstance(profile_record, dict) or profile_record != lock_record:
        raise PipelineError("profile and toolchain source provenance differ")
    required = {
        "source_commit",
        "source_tree",
        "source_date_epoch",
        "independently_reviewed_equivalent_source_commit",
        "independently_reviewed_equivalent_source_tree",
        "source_tree_equivalence",
    }
    if set(profile_record) != required:
        raise PipelineError("source provenance fields are incomplete")
    source_commit = profile_record["source_commit"]
    reviewed_commit = profile_record[
        "independently_reviewed_equivalent_source_commit"
    ]
    validate_commit(source_commit, root=root)
    validate_commit(reviewed_commit, root=root)
    if requested_commit is not None and requested_commit != source_commit:
        raise PipelineError(
            "requested source commit differs from the pinned active ancestor"
        )
    source_tree = git_tree(source_commit, root=root)
    reviewed_tree = git_tree(reviewed_commit, root=root)
    if source_tree != profile_record["source_tree"]:
        raise PipelineError("active source tree differs from provenance")
    if reviewed_tree != profile_record[
        "independently_reviewed_equivalent_source_tree"
    ]:
        raise PipelineError("reviewed source tree differs from provenance")
    if source_tree != reviewed_tree:
        raise PipelineError("active and independently reviewed source trees differ")
    if profile_record["source_tree_equivalence"] != "verified-identical":
        raise PipelineError("source tree equivalence is not verified")
    if (
        git_commit_epoch(source_commit, root=root)
        != profile_record["source_date_epoch"]
    ):
        raise PipelineError("source date epoch differs from active source commit")
    ancestry = run(
        ["git", "merge-base", "--is-ancestor", source_commit, "HEAD"],
        cwd=root,
    )
    if ancestry.returncode:
        raise PipelineError("pinned active source commit is not an ancestor of HEAD")
    return dict(profile_record)


def load_candidate_status(root=ROOT):
    root = pathlib.Path(root)
    path = root / CANDIDATE_PATH
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {
        "source": CANDIDATE_PATH.as_posix(),
        "sha256": sha256_file(path),
        "label": data["label"],
        "observed_at_utc": data["observed_at_utc"],
        "timeless_state": data["timeless_state"],
        "status_claims": data["status_claims"],
    }


def artifact_specs(root=ROOT):
    profile = load_profile(root)
    return [dict(row) for row in profile["artifacts"]]


def compatibility_input_bytes(root=ROOT):
    root = pathlib.Path(root)
    return {
        LATEXMKRC_PATH.as_posix(): (root / LATEXMKRC_PATH).read_bytes(),
        PDFTEX_COMPAT_PATH.as_posix(): (root / PDFTEX_COMPAT_PATH).read_bytes(),
    }


def unicode_mapping_issues(latex_inputs, compatibility_bytes):
    """Return all unmapped literal Unicode points in generated LaTeX inputs."""
    issues = []
    declared_matches = re.findall(
        rb"\\DeclareUnicodeCharacter\{([0-9A-Fa-f]{4,6})\}",
        bytes(compatibility_bytes),
    )
    declared = {int(value, 16) for value in declared_matches}
    if len(declared) != len(declared_matches):
        issues.append("duplicate Unicode compatibility declaration")
    observed = set()
    for path, payload in sorted(latex_inputs.items()):
        try:
            text = bytes(payload).decode("utf-8")
        except UnicodeDecodeError as exc:
            issues.append("%s is not UTF-8: %s" % (path, exc))
            continue
        observed.update(ord(character) for character in text if ord(character) > 127)
    for codepoint in sorted(observed - declared):
        issues.append(
            "unmapped generated LaTeX Unicode code point U+%04X" % codepoint
        )
    return issues


def toolchain_lock_issues(lock, *, root=ROOT):
    issues = []
    root = pathlib.Path(root)
    container = lock.get("container", {})
    tools = lock.get("tools", {})
    image = container.get("image", "")
    digest = container.get("manifest_digest")
    if image != "texlive/texlive@" + str(digest):
        issues.append("container image must use the declared manifest digest")
    if container.get("platform") != "linux/amd64":
        issues.append("container platform must be linux/amd64")
    if container.get("network") != "none":
        issues.append("container network must be none")
    if container.get("locale") != "C.UTF-8":
        issues.append("container locale must be C.UTF-8")
    if lock.get("build", {}).get("shell_escape") != "disabled":
        issues.append("shell escape must be disabled")
    expected = {
        "latexmk": "4.87",
        "pdftex": "1.40.28",
        "bibtex": "0.99d",
        "kpathsea": "6.4.1",
    }
    if tools != expected:
        issues.append("TeX tool versions differ from the approved lock")
    if lock.get("tex_packages") != EXPECTED_TEX_PACKAGES:
        issues.append("TeX package identities differ from the approved lock")
    if container.get("config_digest") != (
        "sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1"
    ):
        issues.append("container configuration digest differs from the approved lock")
    python_lock = lock.get("python", {})
    requirements_path = python_lock.get("requirements_lock")
    if requirements_path != "requirements-ci.lock.txt":
        issues.append("Python requirements lock path differs from the approved lock")
    else:
        path = root / requirements_path
        if (
            not path.is_file()
            or python_lock.get("requirements_lock_sha256")
            != sha256_file(path)
        ):
            issues.append("Python requirements lock hash differs from owner")
    if python_lock.get("version") != "3.11.9":
        issues.append("Python version differs from the approved lock")
    if python_lock.get("pypdf") != "6.14.2":
        issues.append("pypdf version differs from the approved lock")
    if lock.get("qa", {}).get("poppler") != "25.07.0":
        issues.append("Poppler version differs from the approved lock")
    timeout = lock.get("build", {}).get("timeout_seconds")
    if timeout != 120:
        issues.append("latexmk execution timeout must be exactly 120 seconds")
    if lock.get("build", {}).get("runaway_page_guard") != 500:
        issues.append("runaway page guard must be exactly 500 pages")
    return issues


def runtime_toolchain_issues(lock, evidence):
    """Compare independently probed runtime evidence to the complete lock."""
    expected = {
        "container_manifest_digest": lock["container"]["manifest_digest"],
        "container_config_digest": lock["container"]["config_digest"],
        "container_os": "linux",
        "container_architecture": "amd64",
        "python": lock["python"]["version"],
        "requirements_lock_sha256": lock["python"][
            "requirements_lock_sha256"
        ],
        "pypdf": lock["python"]["pypdf"],
        "poppler": lock["qa"]["poppler"],
        "latexmk": lock["tools"]["latexmk"],
        "pdftex": lock["tools"]["pdftex"],
        "bibtex": lock["tools"]["bibtex"],
        "kpathsea": lock["tools"]["kpathsea"],
    }
    issues = []
    if set(evidence) != set(expected):
        issues.append("runtime toolchain evidence fields are incomplete")
    for field, value in expected.items():
        if evidence.get(field) != value:
            issues.append(
                "runtime toolchain evidence differs for %s: expected %s, got %s"
                % (field, value, evidence.get(field))
            )
    return issues


def latexmk_timeout_seconds(lock):
    timeout = lock.get("build", {}).get("timeout_seconds")
    if timeout != 120:
        raise PipelineError("latexmk execution timeout differs from the lock")
    return timeout


def latex_page_guard_pages(lock):
    pages = lock.get("build", {}).get("runaway_page_guard")
    if pages != 500:
        raise PipelineError("runaway page guard differs from the lock")
    return pages


def docker_build_command(
    lock, *, host_package_root, artifact_id, source_date_epoch
):
    container = lock["container"]
    tex_bin = container["tex_bin"]
    host = pathlib.Path(host_package_root).resolve().as_posix()
    workdir = "/work/publication/latex/%s" % artifact_id
    latexmk = "%s/latexmk main.tex" % tex_bin
    return [
        "docker",
        "run",
        "--rm",
        "--network=none",
        "--platform=%s" % container["platform"],
        "-e",
        "LANG=C.UTF-8",
        "-e",
        "LC_ALL=C.UTF-8",
        "-e",
        "TZ=UTC",
        "-e",
        "SOURCE_DATE_EPOCH=%d" % source_date_epoch,
        "-e",
        "FORCE_SOURCE_DATE=1",
        "-e",
        "TEXMFHOME=/nonexistent",
        "-e",
        "TEXMFCONFIG=/tmp/texmf-config",
        "-e",
        "TEXMFVAR=/tmp/texmf-var",
        "-e",
        (
            "PATH=%s:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:"
            "/sbin:/bin" % tex_bin
        ),
        "-v",
        "%s:/work" % host,
        "-w",
        workdir,
        container["image"],
        "/bin/sh",
        "-c",
        latexmk,
    ]


def build_log_issues(log_text, *, tolerance_pt):
    issues = []
    if (
        "Invalid UTF-8 byte sequence" in log_text
        or "FancyVerbBreakAnywhereBreak" in log_text
    ):
        issues.append("UTF-8 verbatim break corruption")
    if re.search(
        r"Maximum runs of .* reached without getting stable files",
        log_text,
        re.I,
    ):
        issues.append("latexmk pass limit reached")
    if "Task 13 runaway page guard exceeded" in log_text:
        issues.append("runaway page guard exceeded")
    if "Empty `thebibliography' environment" in log_text:
        issues.append("empty bibliography environment reached PDF layout")
    undefined_patterns = [
        r"(?:LaTeX|Package \S+) Warning:.*Reference.*undefined",
        r"(?:LaTeX|Package \S+) Warning:.*Citation.*undefined",
        r"There were undefined references",
        r"There were undefined citations",
    ]
    for pattern in undefined_patterns:
        if re.search(pattern, log_text, re.I):
            issues.append("unresolved reference or citation: %s" % pattern)
    for match in re.finditer(
        r"Overfull \\[hv]box \(([0-9]+(?:\.[0-9]+)?)pt too "
        r"(?:wide|high)\)",
        log_text,
        re.I,
    ):
        width = float(match.group(1))
        if width > float(tolerance_pt):
            issues.append(
                "overfull box %.3fpt exceeds %.3fpt tolerance"
                % (width, float(tolerance_pt))
            )
    if re.search(r"Emergency stop|Fatal error occurred|^!", log_text, re.M):
        issues.append("TeX log contains a fatal error")
    return issues


def _tex_citation_commands(main_tex):
    try:
        text = bytes(main_tex).decode("utf-8")
    except UnicodeDecodeError:
        return []
    uncommented = "\n".join(
        re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines()
    )
    return re.findall(
        r"\\(?:[Cc]ite[A-Za-z]*|nocite)\s*"
        r"(?:\[[^\]\n]*\]\s*){0,2}\{",
        uncommented,
    )


def _normalized_blg_lines(blg_text):
    return [
        line.rstrip()
        for line in str(blg_text).replace("\r\n", "\n").replace("\r", "\n").splitlines()
    ]


def _canonical_empty_blg_issues(lines):
    issues = []
    required = {
        "This is BibTeX, Version 0.99d (TeX Live 2025)",
        "Capacity: max_strings=200000, hash_size=200000, hash_prime=170003",
        "The top-level auxiliary file: main.aux",
        "The style file: plainnat.bst",
        "I found no \\citation commands---while reading file main.aux",
        "Database file #1: ../../../references/orthemology.bib",
        "You've used 0 entries,",
        "(There was 1 error message)",
    }
    missing = sorted(required - set(lines))
    if missing:
        issues.append("canonical empty BibTeX log evidence is missing: %r" % missing)
    if lines.count("I found no \\citation commands---while reading file main.aux") != 1:
        issues.append("canonical no-citation error must occur exactly once")
    if lines.count("(There was 1 error message)") != 1:
        issues.append("canonical empty BibTeX error summary must occur exactly once")
    allowed_patterns = [
        r"^$",
        r"^This is BibTeX, Version 0\.99d \(TeX Live 2025\)$",
        r"^Capacity: max_strings=200000, hash_size=200000, hash_prime=170003$",
        r"^The top-level auxiliary file: main\.aux$",
        r"^The style file: plainnat\.bst$",
        r"^I found no \\citation commands---while reading file main\.aux$",
        r"^Database file #1: \.\./\.\./\.\./references/orthemology\.bib$",
        r"^You've used 0 entries,$",
        r"^\s+\d+ wiz_defined-function locations,$",
        r"^\s+\d+ strings with \d+ characters,$",
        r"^and the built_in function-call counts, \d+ in all, are:$",
        r"^[A-Za-z0-9$:=+*<>.-]+ -- \d+$",
        r"^\(There was 1 error message\)$",
    ]
    unexpected = [
        line
        for line in lines
        if not any(re.fullmatch(pattern, line) for pattern in allowed_patterns)
    ]
    if unexpected:
        issues.append("unexpected empty BibTeX log content: %r" % unexpected)
    return issues


def _clean_nonempty_blg_issues(lines):
    issues = []
    required = {
        "This is BibTeX, Version 0.99d (TeX Live 2025)",
        "Capacity: max_strings=200000, hash_size=200000, hash_prime=170003",
        "The top-level auxiliary file: main.aux",
        "The style file: plainnat.bst",
        "Database file #1: ../../../references/orthemology.bib",
    }
    missing = sorted(required - set(lines))
    if missing:
        issues.append("nonempty BibTeX log evidence is missing: %r" % missing)
    if not any(re.fullmatch(r"You've used [1-9]\d* entr(?:y|ies),", line) for line in lines):
        issues.append("nonempty BibTeX log does not report a used entry")
    forbidden = [
        line
        for line in lines
        if "Warning--" in line
        or "error message" in line.lower()
        or line.startswith("I found ")
        or line.startswith("I couldn't ")
    ]
    if forbidden:
        issues.append("nonempty BibTeX log contains warning/error: %r" % forbidden)
    return issues


def classify_bibliography_run(
    *,
    main_tex,
    aux_text,
    bbl_bytes,
    blg_text,
    bibtex_rc,
    fls_text,
    bibliography,
    expected_bibliography_sha256,
):
    """Classify one clean BibTeX run and return fail-closed QA evidence."""
    issues = []
    citation_commands = _tex_citation_commands(main_tex)
    aux_citations = re.findall(r"^\\citation\{[^}]*\}\s*$", aux_text, re.M)
    aux_styles = re.findall(r"^\\bibstyle\{([^}]*)\}\s*$", aux_text, re.M)
    aux_databases = re.findall(r"^\\bibdata\{([^}]*)\}\s*$", aux_text, re.M)
    if aux_styles != [EXPECTED_BIBLIOGRAPHY_STYLE]:
        issues.append("aux bibliography style must be exactly plainnat")
    if aux_databases != [EXPECTED_BIBLIOGRAPHY_AUX_DATABASE]:
        issues.append("aux bibliography database must be the packaged owner")
    if not re.search(r"^INPUT (?:\./)?main\.bbl\s*$", fls_text, re.M):
        issues.append("pdflatex recorder did not observe generated main.bbl")
    bibliography_sha256 = sha256_bytes(bibliography)
    if bibliography_sha256 != expected_bibliography_sha256:
        issues.append("packaged bibliography hash differs from its owner")

    bbl_bytes = bytes(bbl_bytes)
    bbl_text = bbl_bytes.decode("utf-8", errors="replace")
    blg_lines = _normalized_blg_lines(blg_text)
    empty_bbl = bbl_bytes == CANONICAL_EMPTY_BBL
    has_bibitem = bool(re.search(r"\\bibitem(?:\[|\{)", bbl_text))

    if empty_bbl:
        disposition = EMPTY_BIBLIOGRAPHY_DISPOSITION
        if citation_commands:
            issues.append("empty bibliography source contains cite/nocite commands")
        if aux_citations:
            issues.append("empty bibliography aux contains citation commands")
        if bibtex_rc != 2:
            issues.append("canonical empty bibliography requires BibTeX return code 2")
        if has_bibitem:
            issues.append("canonical empty bibliography contains an entry")
        issues.extend(_canonical_empty_blg_issues(blg_lines))
    else:
        disposition = NONEMPTY_BIBLIOGRAPHY_DISPOSITION
        if not citation_commands:
            issues.append("nonempty bibliography source has no cite/nocite command")
        if not aux_citations:
            issues.append("nonempty bibliography aux has no citation command")
        if bibtex_rc != 0:
            issues.append("nonempty bibliography requires BibTeX return code 0")
        if not has_bibitem:
            issues.append("nonempty bibliography has no bibitem")
        issues.extend(_clean_nonempty_blg_issues(blg_lines))

    record = {
        "disposition": disposition,
        "bibtex_return_code": bibtex_rc,
        "bibtex_version": "0.99d",
        "database_path": EXPECTED_BIBLIOGRAPHY_DATABASE,
        "bibliography_style": EXPECTED_BIBLIOGRAPHY_STYLE,
        "citation_commands": len(citation_commands),
        "aux_citations": len(aux_citations),
        "bbl_sha256": sha256_bytes(bbl_bytes),
        "blg_sha256": sha256_bytes(
            ("\n".join(blg_lines) + "\n").encode("utf-8")
        ),
        "bibliography_sha256": bibliography_sha256,
        "stale_bbl_preexisting": False,
    }
    return issues, record


def probe_utf8_verbatim_compatibility(lock, *, root=ROOT):
    """Compile and extract a multibyte verbatim line under the pinned engine."""
    root = pathlib.Path(root)
    parent = root / "tmp" / "pdf-builds"
    parent.mkdir(parents=True, exist_ok=True)
    artifact_id = "utf8-verbatim-probe"
    with tempfile.TemporaryDirectory(dir=str(parent)) as temporary:
        package_root = pathlib.Path(temporary)
        workdir = (
            package_root / "publication" / "latex" / artifact_id
        )
        workdir.mkdir(parents=True)
        compatibility = compatibility_input_bytes(root)
        (workdir / ".latexmkrc").write_bytes(
            compatibility[LATEXMKRC_PATH.as_posix()]
        )
        (workdir / "pdftex-unicode-compat.tex").write_bytes(
            compatibility[PDFTEX_COMPAT_PATH.as_posix()]
        )
        main_bytes = (
            "\\documentclass{article}\n"
            "\\usepackage{amssymb}\n"
            "\\begin{document}\n"
            "\\begin{verbatim}\n"
            "m --Omega--> x --placement--> a_t --creates--> Succ ⊆ M\n"
            "                                                       "
            "|______________________|\n"
            "claim_status_ref: decision-0034#claim-status\n"
            "\\end{verbatim}\n"
            "\\end{document}\n"
        ).encode("utf-8")
        if b"Succ \xe2\x8a\x86 M" not in main_bytes:
            raise PipelineError("UTF-8 verbatim probe source bytes are corrupt")
        (workdir / "main.tex").write_bytes(main_bytes)
        command = docker_build_command(
            lock,
            host_package_root=package_root,
            artifact_id=artifact_id,
            source_date_epoch=0,
        )
        try:
            result = run(command, timeout=latexmk_timeout_seconds(lock))
        except subprocess.TimeoutExpired as exc:
            raise PipelineError(
                "UTF-8 verbatim compatibility probe exceeded the locked timeout"
            ) from exc
        log_path = workdir / "main.log"
        pdf_path = workdir / "main.pdf"
        combined = result.stdout + "\n" + result.stderr
        log_text = (
            log_path.read_text(encoding="utf-8", errors="replace")
            if log_path.is_file()
            else combined
        )
        log_issues = build_log_issues(log_text, tolerance_pt=5)
        if result.returncode or not pdf_path.is_file() or log_issues:
            raise PipelineError(
                "UTF-8 verbatim compatibility probe failed: %s\n%s"
                % ("; ".join(log_issues), combined[-3000:])
            )
        reader = PdfReader(str(pdf_path))
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        normalized = re.sub(r"\s+", "", extracted)
        if "Succ⊆M" not in normalized:
            raise PipelineError(
                "UTF-8 verbatim compatibility probe lost `Succ ⊆ M`: %r"
                % extracted
            )
        if "|______________________|" not in normalized:
            raise PipelineError(
                "verbatim compatibility probe changed the diagram run: %r"
                % extracted
            )
        if len(reader.pages) > latex_page_guard_pages(lock):
            raise PipelineError("UTF-8 verbatim probe exceeded the page guard")
        return {
            "source_utf8_hex": "5375636320e28a86204d",
            "extracted_semantic_text": "Succ ⊆ M",
            "page_count": len(reader.pages),
        }


def _probe_bibliography_case(lock, package_root, *, cited, root=ROOT):
    artifact_id = (
        "nonempty-bibliography-probe"
        if cited
        else "empty-bibliography-probe"
    )
    workdir = package_root / "publication" / "latex" / artifact_id
    bibliography_path = package_root / BIB_PATH
    workdir.mkdir(parents=True)
    bibliography_path.parent.mkdir(parents=True, exist_ok=True)
    compatibility = compatibility_input_bytes(root)
    (workdir / ".latexmkrc").write_bytes(
        compatibility[LATEXMKRC_PATH.as_posix()]
    )
    (workdir / "pdftex-unicode-compat.tex").write_bytes(
        compatibility[PDFTEX_COMPAT_PATH.as_posix()]
    )
    citation = "Body sentinel \\cite{example}.\n" if cited else "Body sentinel.\n"
    main_bytes = (
        "\\documentclass[10pt,letterpaper,twocolumn]{article}\n"
        "\\usepackage{natbib}\n"
        "\\begin{document}\n"
        "\\twocolumn[\\begin{center}\\textbf{Front matter sentinel}"
        "\\end{center}]\n"
        + citation
        + "\\twocolumn\n"
        "\\bibliographystyle{plainnat}\n"
        "\\bibliography{../../../references/orthemology}\n"
        "\\end{document}\n"
    ).encode("utf-8")
    bibliography = (
        "@book{example,\n"
        "  author = {Author, Example},\n"
        "  title = {Example Title},\n"
        "  year = {2026},\n"
        "  publisher = {Example Press}\n"
        "}\n"
    ).encode("utf-8")
    (workdir / "main.tex").write_bytes(main_bytes)
    bibliography_path.write_bytes(bibliography)
    command = docker_build_command(
        lock,
        host_package_root=package_root,
        artifact_id=artifact_id,
        source_date_epoch=0,
    )
    result = run(command, timeout=latexmk_timeout_seconds(lock))
    required = {
        name: workdir / name
        for name in (
            "main.aux",
            "main.bbl",
            "main.blg",
            BIBTEX_STATUS_NAME,
            "main.fls",
            "main.log",
            "main.pdf",
        )
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    if result.returncode or missing:
        raise PipelineError(
            "%s failed or omitted outputs %r:\n%s"
            % (artifact_id, missing, (result.stdout + result.stderr)[-3000:])
        )
    status_text = required[BIBTEX_STATUS_NAME].read_text(
        encoding="ascii", errors="strict"
    ).strip()
    if not status_text.isdigit():
        raise PipelineError("%s BibTeX status is malformed" % artifact_id)
    log_text = required["main.log"].read_text(
        encoding="utf-8", errors="replace"
    )
    log_issues = build_log_issues(log_text, tolerance_pt=5)
    fls_text = required["main.fls"].read_text(
        encoding="utf-8", errors="replace"
    )
    log_issues.extend(fls_issues(fls_text, artifact_id))
    bibliography_issues, bibliography_qa = classify_bibliography_run(
        main_tex=main_bytes,
        aux_text=required["main.aux"].read_text(
            encoding="utf-8", errors="replace"
        ),
        bbl_bytes=required["main.bbl"].read_bytes(),
        blg_text=required["main.blg"].read_text(
            encoding="utf-8", errors="replace"
        ),
        bibtex_rc=int(status_text),
        fls_text=fls_text,
        bibliography=bibliography,
        expected_bibliography_sha256=sha256_bytes(bibliography),
    )
    if log_issues or bibliography_issues:
        raise PipelineError(
            "%s bibliography compatibility: %s"
            % (
                artifact_id,
                "; ".join(log_issues + bibliography_issues),
            )
        )
    reader = PdfReader(str(required["main.pdf"]))
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    normalized = re.sub(r"\s+", "", extracted)
    if len(reader.pages) != 1:
        raise PipelineError("%s must render exactly one probe page" % artifact_id)
    if "Frontmattersentinel" not in normalized or "Bodysentinel" not in normalized:
        raise PipelineError("%s lost front matter or body text" % artifact_id)
    if cited:
        if (
            bibliography_qa["disposition"]
            != NONEMPTY_BIBLIOGRAPHY_DISPOSITION
            or "References" not in normalized
            or "ExampleTitle" not in normalized
        ):
            raise PipelineError(
                "nonempty bibliography heading or entry did not render"
            )
    elif (
        bibliography_qa["disposition"] != EMPTY_BIBLIOGRAPHY_DISPOSITION
        or "References" in normalized
    ):
        raise PipelineError("empty bibliography produced a heading or page")
    return bibliography_qa


def probe_bibliography_compatibility(lock, *, root=ROOT):
    """Compile exact empty and nonempty bibliography layout controls."""
    root = pathlib.Path(root)
    parent = root / "tmp" / "pdf-builds"
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(parent)) as temporary:
        package_root = pathlib.Path(temporary)
        empty = _probe_bibliography_case(
            lock,
            package_root,
            cited=False,
            root=root,
        )
        nonempty = _probe_bibliography_case(
            lock,
            package_root,
            cited=True,
            root=root,
        )
        return {"empty": empty, "nonempty": nonempty}


def create_source_package(
    *,
    artifact_id,
    main_tex,
    bibliography,
    source_commit,
    source_tree,
    independently_reviewed_equivalent_source_commit,
    independently_reviewed_equivalent_source_tree,
    source_date_epoch,
    profile_sha256,
    toolchain_lock_sha256,
    latexmkrc,
    pdftex_compat,
    tex_live_dependencies,
):
    members = {
        "publication/latex/%s/main.tex" % artifact_id: (
            bytes(main_tex),
            "entry-point",
        ),
        "publication/latex/%s/.latexmkrc" % artifact_id: (
            bytes(latexmkrc),
            "build-driver",
        ),
        "publication/latex/%s/pdftex-unicode-compat.tex" % artifact_id: (
            bytes(pdftex_compat),
            "compatibility-input",
        ),
        BIB_PATH.as_posix(): (bytes(bibliography), "bibliography-owner"),
    }
    raw = io.BytesIO()
    with gzip.GzipFile(
        fileobj=raw,
        mode="wb",
        filename="",
        compresslevel=9,
        mtime=source_date_epoch,
    ) as gz:
        with tarfile.open(
            fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT
        ) as archive:
            for name in sorted(members):
                payload, _role = members[name]
                info = tarfile.TarInfo(name)
                info.size = len(payload)
                info.mtime = source_date_epoch
                info.mode = 0o644
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                archive.addfile(info, io.BytesIO(payload))
    archive_bytes = raw.getvalue()
    manifest = {
        "schema": "orthemology-source-manifest-v1",
        "artifact_id": artifact_id,
        "source_commit": source_commit,
        "source_tree": source_tree,
        "independently_reviewed_equivalent_source_commit": (
            independently_reviewed_equivalent_source_commit
        ),
        "independently_reviewed_equivalent_source_tree": (
            independently_reviewed_equivalent_source_tree
        ),
        "source_tree_equivalence": "verified-identical",
        "source_date_epoch": source_date_epoch,
        "archive": {
            "path": "artifacts/%s.source.tar.gz" % artifact_id,
            "sha256": sha256_bytes(archive_bytes),
            "format": "tar-gzip-ustar",
        },
        "entry_point": "publication/latex/%s/main.tex" % artifact_id,
        "build_workdir": "publication/latex/%s" % artifact_id,
        "publication_profile_sha256": profile_sha256,
        "toolchain_lock_sha256": toolchain_lock_sha256,
        "tex_live_dependencies": tex_live_dependencies,
        "compatibility_inputs": {
            LATEXMKRC_PATH.as_posix(): sha256_bytes(latexmkrc),
            PDFTEX_COMPAT_PATH.as_posix(): sha256_bytes(pdftex_compat),
        },
        "members": [
            {
                "path": name,
                "sha256": sha256_bytes(members[name][0]),
                "bytes": len(members[name][0]),
                "mode": "0644",
                "role": members[name][1],
            }
            for name in sorted(members)
        ],
    }
    return archive_bytes, manifest


def build_sidecar_record(
    *,
    artifact_id,
    pdf_sha256,
    page_count,
    source_commit,
    source_tree,
    independently_reviewed_equivalent_source_commit,
    independently_reviewed_equivalent_source_tree,
    source_date_epoch,
    markdown_sha256,
    latex_sha256,
    bibliography_sha256,
    profile_sha256,
    toolchain_lock_sha256,
    candidate_status,
    source_package_sha256,
    source_manifest_sha256,
    tool_versions,
    compatibility_sha256=None,
    bibliography_qa=None,
):
    timestamp = datetime.datetime.fromtimestamp(
        source_date_epoch, tz=datetime.timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    workdir = "publication/latex/%s" % artifact_id
    return {
        "schema": "orthemology-pdf-sources-v2",
        "artifact_id": artifact_id,
        "pdf": artifact_id + ".pdf",
        "pdf_sha256": pdf_sha256,
        "page_count": page_count,
        "source_commit": source_commit,
        "source_tree": source_tree,
        "independently_reviewed_equivalent_source_commit": (
            independently_reviewed_equivalent_source_commit
        ),
        "independently_reviewed_equivalent_source_tree": (
            independently_reviewed_equivalent_source_tree
        ),
        "source_tree_equivalence": "verified-identical",
        "source_date_epoch": source_date_epoch,
        "build_time_utc": timestamp,
        "source_hashes": {
            "markdown": dict(sorted(markdown_sha256.items())),
            "latex": dict(sorted(latex_sha256.items())),
            "bibliography": {
                "path": BIB_PATH.as_posix(),
                "sha256": bibliography_sha256,
            },
            "compatibility": dict(sorted((compatibility_sha256 or {}).items())),
        },
        "publication_profile": {
            "path": PROFILE_PATH.as_posix(),
            "sha256": profile_sha256,
        },
        "toolchain_lock": {
            "path": LOCK_PATH.as_posix(),
            "sha256": toolchain_lock_sha256,
        },
        "candidate_status": candidate_status,
        "entry_point": workdir + "/main.tex",
        "build_workdir": workdir,
        "build_command": (
            "/usr/local/texlive/2025/bin/x86_64-linux/latexmk main.tex"
        ),
        "source_package": {
            "path": "artifacts/%s.source.tar.gz" % artifact_id,
            "sha256": source_package_sha256,
        },
        "source_manifest": {
            "path": "artifacts/%s.source-manifest.json" % artifact_id,
            "sha256": source_manifest_sha256,
        },
        "tools": dict(sorted(tool_versions.items())),
        "bibliography_qa": dict(bibliography_qa or {}),
        "generation_status": (
            "complete; PDFLaTeX through latexmk; independent double build "
            "byte-identical; clean source-package rebuild verified"
        ),
    }


def prepare_render_directory(path):
    target = pathlib.Path(path).resolve()
    if target == pathlib.Path(target.anchor):
        raise ValueError("refusing to clear a filesystem root")
    target.mkdir(parents=True, exist_ok=True)
    for child in target.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    return target


def extract_source_package(archive_bytes, destination):
    destination = pathlib.Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
        for member in archive.getmembers():
            pure = pathlib.PurePosixPath(member.name)
            if (
                not member.isfile()
                or pure.is_absolute()
                or ".." in pure.parts
                or "\\" in member.name
            ):
                raise PipelineError("unsafe source-package member: %s" % member.name)
            target = destination.joinpath(*pure.parts).resolve()
            if destination not in target.parents:
                raise PipelineError("source-package member escapes root")
            target.parent.mkdir(parents=True, exist_ok=True)
            stream = archive.extractfile(member)
            if stream is None:
                raise PipelineError("source-package member is unreadable")
            target.write_bytes(stream.read())


def _find_poppler_binary():
    candidates = []
    if os.name == "nt":
        result = subprocess.run(
            ["where.exe", "pdftoppm"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0:
            candidates.extend(
                pathlib.Path(line.strip())
                for line in result.stdout.splitlines()
                if line.strip()
            )
    found = shutil.which("pdftoppm")
    if found:
        candidates.append(pathlib.Path(found))
    for candidate in candidates:
        if candidate.is_file() and (
            os.name != "nt" or candidate.suffix.casefold() == ".exe"
        ):
            return candidate
    raise PipelineError("a runnable pdftoppm binary is required")


def probe_toolchain(lock, *, root=ROOT, runner=run):
    root = pathlib.Path(root)
    issues = toolchain_lock_issues(lock, root=root)
    if issues:
        raise PipelineError("; ".join(issues))
    image = lock["container"]["image"]
    inspect = runner(
        [
            "docker",
            "image",
            "inspect",
            image,
            "--format",
            "{{.Id}}|{{.Os}}|{{.Architecture}}",
        ],
        timeout=60,
    )
    if inspect.returncode:
        raise PipelineError(
            "pinned TeX image is not locally available; pull it before the "
            "offline build: %s" % inspect.stderr.strip()
        )
    inspect_parts = inspect.stdout.strip().split("|")
    if len(inspect_parts) != 3:
        raise PipelineError(
            "local image identity probe is malformed: %s"
            % inspect.stdout.strip()
        )
    manifest_digest, container_os, container_architecture = inspect_parts
    raw_manifest = runner(
        ["docker", "buildx", "imagetools", "inspect", "--raw", image],
        timeout=60,
    )
    if raw_manifest.returncode:
        raise PipelineError(
            "container configuration probe failed: %s"
            % raw_manifest.stderr.strip()
        )
    try:
        config_digest = json.loads(raw_manifest.stdout)["config"]["digest"]
    except (KeyError, TypeError, ValueError) as exc:
        raise PipelineError(
            "container configuration probe returned malformed manifest JSON"
        ) from exc
    tex_bin = lock["container"]["tex_bin"]
    version_command = [
        "docker",
        "run",
        "--rm",
        "--network=none",
        "--platform=%s" % lock["container"]["platform"],
        "-e",
        "LANG=C.UTF-8",
        "-e",
        "LC_ALL=C.UTF-8",
        image,
        "/bin/sh",
        "-lc",
        (
            "%s/latexmk -v; %s/pdflatex --version; %s/bibtex --version; "
            "%s/kpsewhich --version"
        )
        % (tex_bin, tex_bin, tex_bin, tex_bin),
    ]
    probe = runner(version_command, timeout=60)
    if probe.returncode:
        raise PipelineError("TeX toolchain probe failed: %s" % probe.stderr.strip())
    version_patterns = {
        "latexmk": r"Latexmk,.*?Version\s+([0-9.]+)",
        "pdftex": r"pdfTeX[^\n]*?-([0-9]+\.[0-9]+\.[0-9]+)",
        "bibtex": r"BibTeX\s+([0-9.]+[a-z]?)",
        "kpathsea": r"kpathsea version\s+([0-9.]+)",
    }
    tex_versions = {}
    for name, pattern in version_patterns.items():
        match = re.search(pattern, probe.stdout, re.I | re.S)
        if match is None:
            raise PipelineError(
                "TeX toolchain version probe omitted %s" % name
            )
        tex_versions[name] = match.group(1)
    probe_utf8_verbatim_compatibility(lock, root=root)
    probe_bibliography_compatibility(lock, root=root)
    import pypdf

    poppler_binary = _find_poppler_binary()
    poppler_probe = runner([str(poppler_binary), "-v"], timeout=30)
    poppler_output = poppler_probe.stdout + "\n" + poppler_probe.stderr
    poppler_match = re.search(
        r"pdftoppm version\s+([0-9.]+)",
        poppler_output,
        re.I,
    )
    if poppler_probe.returncode not in (0, 99) or poppler_match is None:
        raise PipelineError(
            "Poppler version probe failed: %s" % poppler_output.strip()
        )
    evidence = {
        **tex_versions,
        "container_manifest_digest": manifest_digest,
        "container_config_digest": config_digest,
        "container_os": container_os,
        "container_architecture": container_architecture,
        "python": sys.version.split()[0],
        "requirements_lock_sha256": sha256_file(
            root / lock["python"]["requirements_lock"]
        ),
        "pypdf": pypdf.__version__,
        "poppler": poppler_match.group(1),
    }
    runtime_issues = runtime_toolchain_issues(lock, evidence)
    if runtime_issues:
        raise PipelineError("; ".join(runtime_issues))
    return {
        name: evidence[name]
        for name in (
            "latexmk",
            "pdftex",
            "bibtex",
            "kpathsea",
            "python",
            "pypdf",
            "poppler",
        )
    }


def fls_issues(
    fls_text,
    artifact_id,
    *,
    declared_package_inputs=None,
):
    issues = []
    workdir = "/work/publication/latex/%s" % artifact_id
    declared = (
        {str(path).replace("\\", "/") for path in declared_package_inputs}
        if declared_package_inputs is not None
        else None
    )
    generated = {
        "publication/latex/%s/main.aux" % artifact_id,
        "publication/latex/%s/main.bbl" % artifact_id,
        "publication/latex/%s/main.out" % artifact_id,
        "publication/latex/%s/main.toc" % artifact_id,
    }
    seen_main = False
    seen_bbl = False
    for line in fls_text.splitlines():
        if not line.startswith("INPUT "):
            continue
        raw = line[6:].strip().replace("\\", "/")
        if raw.endswith("/main.tex") or raw == "main.tex":
            seen_main = True
        if raw.endswith("/main.bbl") or raw == "main.bbl":
            seen_bbl = True
        repository_input = None
        if re.match(r"^[A-Za-z]:", raw):
            issues.append("recorder input uses an absolute drive path: %s" % raw)
            continue
        if raw.startswith("/"):
            allowed = (
                raw.startswith("/usr/local/texlive/2025/")
                or raw.startswith("/tmp/texmf-")
                or raw == "/dev/null"
            )
            if raw.startswith("/work/"):
                repository_input = posixpath.normpath(raw)[len("/work/") :]
            elif not allowed:
                issues.append("undeclared absolute build input: %s" % raw)
        else:
            resolved = posixpath.normpath(posixpath.join(workdir, raw))
            if not resolved.startswith("/work/"):
                issues.append("recorder input escapes package: %s" % raw)
            else:
                repository_input = resolved[len("/work/") :]
        if (
            declared is not None
            and repository_input is not None
            and repository_input not in declared
            and repository_input not in generated
        ):
            issues.append(
                "recorder input is outside the declared source boundary: %s"
                % raw
            )
    if not seen_main:
        issues.append("recorder did not observe main.tex")
    if not seen_bbl:
        issues.append("recorder did not observe generated main.bbl")
    return issues


def _object(value):
    return value.get_object() if hasattr(value, "get_object") else value


def _font_issues(reader):
    issues = []
    seen = set()

    def inspect_font(font, label):
        font = _object(font)
        marker = getattr(font, "indirect_reference", None)
        key = repr(marker) if marker is not None else id(font)
        if key in seen:
            return
        seen.add(key)
        subtype = str(font.get("/Subtype", ""))
        if subtype == "/Type3":
            issues.append("%s uses a Type 3 font" % label)
        descendants = font.get("/DescendantFonts")
        if descendants:
            for index, descendant in enumerate(_object(descendants)):
                inspect_font(descendant, "%s descendant %d" % (label, index))
            return
        descriptor = font.get("/FontDescriptor")
        if descriptor is None:
            issues.append("%s is not embedded (missing FontDescriptor)" % label)
            return
        descriptor = _object(descriptor)
        if not any(
            descriptor.get(name) is not None
            for name in ("/FontFile", "/FontFile2", "/FontFile3")
        ):
            issues.append("%s is not embedded (missing font program)" % label)

    for page_number, page in enumerate(reader.pages, 1):
        resources = _object(page.get("/Resources") or {})
        fonts = _object(resources.get("/Font") or {})
        for name, font in fonts.items():
            inspect_font(font, "page %d font %s" % (page_number, name))
    return issues


def _javascript_issues(reader):
    issues = []
    root = reader.root_object
    names = _object(root.get("/Names") or {})
    if names.get("/JavaScript") is not None:
        issues.append("PDF contains a JavaScript name tree")
    open_action = _object(root.get("/OpenAction") or {})
    if isinstance(open_action, dict) and str(open_action.get("/S")) == "/JavaScript":
        issues.append("PDF contains a JavaScript open action")
    for page_number, page in enumerate(reader.pages, 1):
        for annotation in _object(page.get("/Annots") or []):
            annotation = _object(annotation)
            action = _object(annotation.get("/A") or {})
            if isinstance(action, dict) and str(action.get("/S")) == "/JavaScript":
                issues.append("page %d contains a JavaScript action" % page_number)
    return issues


def _image_count(reader):
    count = 0
    for page in reader.pages:
        resources = _object(page.get("/Resources") or {})
        xobjects = _object(resources.get("/XObject") or {})
        for value in xobjects.values():
            value = _object(value)
            if str(value.get("/Subtype", "")) == "/Image":
                count += 1
    return count


def local_pdf_uri_issues(uri, *, artifact_id, root=ROOT):
    """Validate one PDF URI from artifacts/<artifact_id>.pdf."""
    root = pathlib.Path(root).resolve()
    uri = str(uri).strip()
    parsed = urllib.parse.urlsplit(uri)
    if parsed.scheme:
        if parsed.scheme.lower() in {"http", "https"} and parsed.netloc:
            return []
        return [
            "%s has a prohibited URI scheme: %s"
            % (artifact_id, parsed.scheme)
        ]
    if parsed.netloc:
        return ["%s has a network-relative URI" % artifact_id]
    target = urllib.parse.unquote(parsed.path)
    if (
        not target
        or "\\" in target
        or target.startswith("/")
        or re.match(r"^[A-Za-z]:", target)
    ):
        return ["%s has an absolute or malformed local URI: %s" % (artifact_id, uri)]
    resolved = (root / "artifacts" / target).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return ["%s local URI escapes the repository: %s" % (artifact_id, uri)]
    if not resolved.is_file():
        return ["%s local URI target is missing: %s" % (artifact_id, uri)]
    return []


def _link_issues(reader, *, artifact_id=None, root=ROOT):
    issues = []
    count = 0
    for page_number, page in enumerate(reader.pages, 1):
        for annotation in _object(page.get("/Annots") or []):
            annotation = _object(annotation)
            if str(annotation.get("/Subtype")) != "/Link":
                continue
            count += 1
            action = _object(annotation.get("/A") or {})
            if action:
                action_type = str(action.get("/S", ""))
                if action_type == "/URI" and not str(action.get("/URI", "")).strip():
                    issues.append("page %d has an empty URI link" % page_number)
                elif action_type == "/URI" and artifact_id is not None:
                    issues.extend(
                        "page %d %s" % (page_number, issue)
                        for issue in local_pdf_uri_issues(
                            action.get("/URI", ""),
                            artifact_id=artifact_id,
                            root=root,
                        )
                    )
                elif action_type not in ("/URI", "/GoTo", ""):
                    issues.append(
                        "page %d has an unsupported link action %s"
                        % (page_number, action_type)
                    )
    return issues, count


def _markdown_headings(markdown_bytes):
    headings = []
    for payload in markdown_bytes.values():
        text = payload.decode("utf-8")
        fence_marker = None
        fence_length = 0
        for line in text.splitlines():
            fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if fence:
                marker = fence.group(1)[0]
                length = len(fence.group(1))
                if fence_marker is None:
                    fence_marker = marker
                    fence_length = length
                elif marker == fence_marker and length >= fence_length:
                    fence_marker = None
                    fence_length = 0
                continue
            if fence_marker is not None:
                continue
            match = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
            if match:
                headings.append(match.group(2))
    return headings


def normalize_heading_text(text):
    """Return a case-insensitive Unicode letter/number heading key."""
    text = str(text)
    # pdfTeX's OT1 mapping can extract ī either as a detached spacing macron
    # before dotless i (pypdf) or as dotless i plus a combining macron
    # (Poppler). Repair only those marked sequences; a genuine unmarked
    # dotless i remains a distinct retained Unicode letter.
    text = re.sub("\u00af\\s*\u0131", "i", text)
    text = text.replace("\u0131\u0304", "i")
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(
        character
        for character in decomposed
        if (
            character not in {"\u02bf", "\u02be"}
            and unicodedata.category(character)[0] in {"L", "N"}
        )
    )


def heading_sequence_issues(extracted_text, headings):
    """Validate normalized source headings against extracted PDF text in order."""
    issues = []
    normalized = normalize_heading_text(extracted_text)
    cursor = 0
    for heading in headings:
        key = normalize_heading_text(heading)[:40]
        if not key:
            issues.append(
                "heading normalizes to empty Unicode letter/number key: %s"
                % heading[:60]
            )
            continue
        position = normalized.find(key, cursor)
        if position < 0:
            if key in normalized:
                issues.append("heading appears out of order: %s" % heading[:60])
            else:
                issues.append("heading missing from PDF text: %s" % heading[:60])
        else:
            cursor = position + len(key)
    return issues


def pdf_structure_issues(
    pdf_bytes,
    markdown_bytes,
    *,
    artifact_id=None,
    root=ROOT,
):
    issues = []
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
    except Exception as exc:
        return ["PDF parse failed: %s" % exc], {}
    if reader.is_encrypted:
        issues.append("PDF must not be encrypted")
    page_text = [page.extract_text() or "" for page in reader.pages]
    for page_number, text in enumerate(page_text, 1):
        if len(re.sub(r"\s+", "", text)) < 20:
            issues.append("page %d is blank or has no extractable text" % page_number)
    text = "\n".join(page_text)
    for pattern, label in RAW_MD_PATTERNS:
        if re.search(pattern, text, re.M):
            issues.append("rendered text contains %s" % label)
    if "\x00" in text:
        issues.append("PDF text contains a notdef/NUL glyph")
    if "�" in text:
        issues.append("PDF text contains U+FFFD")

    issues.extend(
        heading_sequence_issues(text, _markdown_headings(markdown_bytes))
    )

    issues.extend(_font_issues(reader))
    issues.extend(_javascript_issues(reader))
    image_count = _image_count(reader)
    if image_count:
        issues.append(
            "PDF contains %d image XObjects; rasterized text is prohibited"
            % image_count
        )
    link_issues, link_count = _link_issues(
        reader,
        artifact_id=artifact_id,
        root=root,
    )
    issues.extend(link_issues)
    return issues, {
        "page_count": len(reader.pages),
        "text": text,
        "link_count": link_count,
        "image_count": image_count,
    }


def source_inputs(spec, source_commit, *, root=ROOT):
    artifact_id = spec["artifact_id"]
    markdown = {
        rel: git_blob(source_commit, rel, root=root)
        for rel in spec.get("sources", [])
    }
    latex_path = "publication/latex/%s/main.tex" % artifact_id
    latex = {
        latex_path: git_blob(source_commit, latex_path, root=root)
    }
    bibliography = git_blob(
        source_commit,
        BIB_PATH.as_posix(),
        root=root,
    )
    return markdown, latex, bibliography


def verify_worktree_source_inputs(
    markdown,
    latex,
    bibliography,
    *,
    root=ROOT,
):
    root = pathlib.Path(root)
    issues = []
    for rel, expected in {**markdown, **latex}.items():
        path = root / rel
        if not path.is_file() or path.read_bytes() != expected:
            issues.append("%s differs from the pinned source commit" % rel)
    bib_path = root / BIB_PATH
    if not bib_path.is_file() or bib_path.read_bytes() != bibliography:
        issues.append("%s differs from the pinned source commit" % BIB_PATH.as_posix())
    return issues


def build_archive_once(
    archive_bytes,
    manifest,
    profile,
    lock,
    *,
    temporary_parent=None,
    root=ROOT,
):
    from validate_arxiv_source_package import validate_source_package_bytes

    package_issues = validate_source_package_bytes(
        archive_bytes,
        manifest,
        profile,
        root=root,
    )
    if package_issues:
        raise PipelineError("source package invalid: %s" % "; ".join(package_issues))
    root = pathlib.Path(root)
    parent = pathlib.Path(temporary_parent or root / "tmp" / "pdf-builds")
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(parent)) as temporary:
        package_root = pathlib.Path(temporary)
        extract_source_package(archive_bytes, package_root)
        workdir = (
            package_root
            / "publication"
            / "latex"
            / manifest["artifact_id"]
        )
        generated_names = (
            "main.aux",
            "main.bbl",
            "main.blg",
            BIBTEX_STATUS_NAME,
            "main.fdb_latexmk",
            "main.fls",
            "main.log",
            "main.pdf",
        )
        stale = [name for name in generated_names if (workdir / name).exists()]
        if stale:
            raise PipelineError(
                "source package contains stale build outputs: %s"
                % ", ".join(stale)
            )
        command = docker_build_command(
            lock,
            host_package_root=package_root,
            artifact_id=manifest["artifact_id"],
            source_date_epoch=manifest["source_date_epoch"],
        )
        try:
            result = run(command, timeout=latexmk_timeout_seconds(lock))
        except subprocess.TimeoutExpired as exc:
            raise PipelineError(
                "latexmk exceeded the locked %d-second timeout for %s"
                % (
                    latexmk_timeout_seconds(lock),
                    manifest["artifact_id"],
                )
            ) from exc
        log_path = workdir / "main.log"
        fls_path = workdir / "main.fls"
        pdf_path = workdir / "main.pdf"
        aux_path = workdir / "main.aux"
        bbl_path = workdir / "main.bbl"
        blg_path = workdir / "main.blg"
        bibtex_status_path = workdir / BIBTEX_STATUS_NAME
        combined = result.stdout + "\n" + result.stderr
        log_text = (
            log_path.read_text(encoding="utf-8", errors="replace")
            if log_path.is_file()
            else combined
        )
        if result.returncode or not pdf_path.is_file():
            raise PipelineError(
                "latexmk failed for %s:\n%s"
                % (manifest["artifact_id"], combined[-6000:])
            )
        log_issues = build_log_issues(
            log_text,
            tolerance_pt=profile["hard_limits"]["overfull_box_tolerance_pt"],
        )
        if log_issues:
            raise PipelineError(
                "%s build log: %s"
                % (manifest["artifact_id"], "; ".join(log_issues))
            )
        if not fls_path.is_file():
            raise PipelineError("latexmk recorder output main.fls is missing")
        fls_text = fls_path.read_text(encoding="utf-8", errors="replace")
        recorded_issues = fls_issues(
            fls_text,
            manifest["artifact_id"],
            declared_package_inputs={
                row["path"] for row in manifest["members"]
            },
        )
        if recorded_issues:
            raise PipelineError(
                "%s recorder: %s"
                % (manifest["artifact_id"], "; ".join(recorded_issues))
            )
        missing_bibliography_outputs = [
            path.name
            for path in (aux_path, bbl_path, blg_path, bibtex_status_path)
            if not path.is_file()
        ]
        if missing_bibliography_outputs:
            raise PipelineError(
                "%s bibliography outputs missing: %s"
                % (
                    manifest["artifact_id"],
                    ", ".join(missing_bibliography_outputs),
                )
            )
        bibtex_status_text = bibtex_status_path.read_text(
            encoding="ascii", errors="strict"
        ).strip()
        if not re.fullmatch(r"\d+", bibtex_status_text):
            raise PipelineError("BibTeX return-code record is malformed")
        expected_bibliography_sha256 = next(
            (
                row["sha256"]
                for row in manifest["members"]
                if row["path"] == BIB_PATH.as_posix()
            ),
            None,
        )
        if expected_bibliography_sha256 is None:
            raise PipelineError("source manifest omits bibliography owner hash")
        bibliography_path = package_root / BIB_PATH
        bibliography_issues, bibliography_qa = classify_bibliography_run(
            main_tex=(workdir / "main.tex").read_bytes(),
            aux_text=aux_path.read_text(encoding="utf-8", errors="replace"),
            bbl_bytes=bbl_path.read_bytes(),
            blg_text=blg_path.read_text(encoding="utf-8", errors="replace"),
            bibtex_rc=int(bibtex_status_text),
            fls_text=fls_text,
            bibliography=bibliography_path.read_bytes(),
            expected_bibliography_sha256=expected_bibliography_sha256,
        )
        if bibliography_issues:
            raise PipelineError(
                "%s bibliography QA: %s"
                % (
                    manifest["artifact_id"],
                    "; ".join(bibliography_issues),
                )
            )
        return {
            "pdf": pdf_path.read_bytes(),
            "log": log_text,
            "fls": fls_text,
            "bibliography_qa": bibliography_qa,
            "command": command,
        }


def build_artifact(
    spec,
    source_provenance,
    profile,
    lock,
    tool_versions,
    candidate_status,
    *,
    check_only,
    root=ROOT,
):
    root = pathlib.Path(root)
    artifacts_root = root / "artifacts"
    artifact_id = spec["artifact_id"]
    source_commit = source_provenance["source_commit"]
    source_tree = source_provenance["source_tree"]
    reviewed_commit = source_provenance[
        "independently_reviewed_equivalent_source_commit"
    ]
    reviewed_tree = source_provenance[
        "independently_reviewed_equivalent_source_tree"
    ]
    epoch = git_commit_epoch(source_commit, root=root)
    markdown, latex, bibliography = source_inputs(
        spec,
        source_commit,
        root=root,
    )
    source_drift = verify_worktree_source_inputs(
        markdown,
        latex,
        bibliography,
        root=root,
    )
    if source_drift:
        raise PipelineError("; ".join(source_drift))
    profile_hash = sha256_file(root / PROFILE_PATH)
    lock_hash = sha256_file(root / LOCK_PATH)
    compatibility = compatibility_input_bytes(root)
    unicode_issues = unicode_mapping_issues(
        latex, compatibility[PDFTEX_COMPAT_PATH.as_posix()]
    )
    if unicode_issues:
        raise PipelineError("; ".join(unicode_issues))
    archive_bytes, manifest = create_source_package(
        artifact_id=artifact_id,
        main_tex=latex["publication/latex/%s/main.tex" % artifact_id],
        bibliography=bibliography,
        source_commit=source_commit,
        source_tree=source_tree,
        independently_reviewed_equivalent_source_commit=reviewed_commit,
        independently_reviewed_equivalent_source_tree=reviewed_tree,
        source_date_epoch=epoch,
        profile_sha256=profile_hash,
        toolchain_lock_sha256=lock_hash,
        latexmkrc=compatibility[LATEXMKRC_PATH.as_posix()],
        pdftex_compat=compatibility[PDFTEX_COMPAT_PATH.as_posix()],
        tex_live_dependencies=lock["tex_packages"],
    )
    manifest_payload = json_bytes(manifest)
    first = build_archive_once(
        archive_bytes,
        manifest,
        profile,
        lock,
        root=root,
    )
    second = build_archive_once(
        archive_bytes,
        manifest,
        profile,
        lock,
        root=root,
    )
    if first["pdf"] != second["pdf"]:
        raise PipelineError("%s independent builds are not byte-identical" % artifact_id)
    if first["bibliography_qa"] != second["bibliography_qa"]:
        raise PipelineError(
            "%s independent bibliography QA records differ" % artifact_id
        )
    structure_issues, structure = pdf_structure_issues(
        first["pdf"],
        markdown,
        artifact_id=artifact_id,
        root=root,
    )
    if structure_issues:
        raise PipelineError(
            "%s PDF structure: %s"
            % (artifact_id, "; ".join(structure_issues[:20]))
        )
    sidecar = build_sidecar_record(
        artifact_id=artifact_id,
        pdf_sha256=sha256_bytes(first["pdf"]),
        page_count=structure["page_count"],
        source_commit=source_commit,
        source_tree=source_tree,
        independently_reviewed_equivalent_source_commit=reviewed_commit,
        independently_reviewed_equivalent_source_tree=reviewed_tree,
        source_date_epoch=epoch,
        markdown_sha256={
            rel: sha256_bytes(payload) for rel, payload in markdown.items()
        },
        latex_sha256={
            rel: sha256_bytes(payload) for rel, payload in latex.items()
        },
        bibliography_sha256=sha256_bytes(bibliography),
        profile_sha256=profile_hash,
        toolchain_lock_sha256=lock_hash,
        candidate_status=candidate_status,
        source_package_sha256=sha256_bytes(archive_bytes),
        source_manifest_sha256=sha256_bytes(manifest_payload),
        tool_versions=tool_versions,
        compatibility_sha256={
            rel: sha256_bytes(payload)
            for rel, payload in compatibility.items()
        },
        bibliography_qa=first["bibliography_qa"],
    )
    sidecar_payload = json_bytes(sidecar)
    expected = {
        artifacts_root / (artifact_id + ".pdf"): first["pdf"],
        artifacts_root / (artifact_id + ".source.tar.gz"): archive_bytes,
        artifacts_root / (artifact_id + ".source-manifest.json"): manifest_payload,
        artifacts_root / (artifact_id + ".sources.json"): sidecar_payload,
    }
    if check_only:
        mismatches = [
            path.name
            for path, payload in expected.items()
            if not path.is_file() or path.read_bytes() != payload
        ]
        if mismatches:
            raise PipelineError(
                "%s committed artifact drift: %s"
                % (artifact_id, ", ".join(mismatches))
            )
    else:
        artifacts_root.mkdir(parents=True, exist_ok=True)
        for path, payload in expected.items():
            path.write_bytes(payload)
    return {
        "artifact_id": artifact_id,
        "pdf_sha256": sidecar["pdf_sha256"],
        "package_sha256": sidecar["source_package"]["sha256"],
        "manifest_sha256": sidecar["source_manifest"]["sha256"],
        "page_count": sidecar["page_count"],
        "link_count": structure["link_count"],
        "image_count": structure["image_count"],
        "bibliography_disposition": first["bibliography_qa"]["disposition"],
    }


def execute_pipeline(*, check_only, source_commit=None, root=ROOT):
    root = pathlib.Path(root)
    profile = load_profile(root)
    lock = load_toolchain_lock(root)
    source_provenance = validate_source_provenance(
        profile,
        lock,
        requested_commit=source_commit,
        root=root,
    )
    tool_versions = probe_toolchain(lock, root=root)
    candidate_status = load_candidate_status(root)
    results = []
    for spec in artifact_specs(root):
        result = build_artifact(
            spec,
            source_provenance,
            profile,
            lock,
            tool_versions,
            candidate_status,
            check_only=check_only,
            root=root,
        )
        results.append(result)
        print(
            "[PASS] %s: %d pages, PDF %s..., package %s..."
            % (
                result["artifact_id"],
                result["page_count"],
                result["pdf_sha256"][:16],
                result["package_sha256"][:16],
            )
        )
    if check_only:
        report_issues = compatibility_report_table_issues(root)
        if report_issues:
            raise PipelineError("; ".join(report_issues))
    else:
        rewrite_compatibility_artifact_table(root)
    return results


def find_pdftoppm(explicit=None):
    if explicit:
        path = pathlib.Path(explicit)
        if path.is_file():
            return path
        raise PipelineError("pdftoppm is missing: %s" % explicit)
    found = shutil.which("pdftoppm")
    if found:
        return pathlib.Path(found)
    raise PipelineError("pdftoppm is required for committed-PDF rasterization")


def render_committed_pdf(
    artifact_id,
    *,
    output_dir=None,
    pdftoppm=None,
    root=ROOT,
):
    root = pathlib.Path(root)
    valid = {row["artifact_id"] for row in artifact_specs(root)}
    if artifact_id not in valid:
        raise PipelineError("unknown artifact identity: %s" % artifact_id)
    pdf_path = root / "artifacts" / (artifact_id + ".pdf")
    if not pdf_path.is_file():
        raise PipelineError("committed PDF is missing: %s" % pdf_path)
    output = pathlib.Path(
        output_dir or root / "tmp" / "pdfs" / artifact_id
    )
    prepare_render_directory(output)
    renderer = find_pdftoppm(pdftoppm)
    prefix = output / "page"
    command = [
        str(renderer),
        "-png",
        "-r",
        "150",
        str(pdf_path),
        str(prefix),
    ]
    result = run(command, timeout=600)
    if result.returncode:
        raise PipelineError("pdftoppm failed: %s" % result.stderr.strip())
    pages = sorted(output.glob("page-*.png"))
    expected = len(PdfReader(str(pdf_path)).pages)
    if len(pages) != expected:
        raise PipelineError(
            "rendered page count mismatch: expected %d, got %d"
            % (expected, len(pages))
        )
    normalized = []
    for index, page in enumerate(pages, 1):
        target = output / ("page-%03d.png" % index)
        if page != target:
            page.replace(target)
        normalized.append(target)
    return normalized


def main(argv=None):
    configure_utf8_diagnostics()
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--render-committed", metavar="ARTIFACT_ID")
    parser.add_argument("--output-dir")
    parser.add_argument("--pdftoppm")
    args = parser.parse_args(argv)
    try:
        if args.render_committed:
            pages = render_committed_pdf(
                args.render_committed,
                output_dir=args.output_dir,
                pdftoppm=args.pdftoppm,
                root=args.root,
            )
            print(
                "[PASS] rendered %d committed pages to %s"
                % (len(pages), pages[0].parent if pages else args.output_dir)
            )
            return 0
        execute_pipeline(
            check_only=args.check,
            source_commit=args.source_commit,
            root=args.root,
        )
        print("TOTAL: 0 failures")
        return 0
    except (PipelineError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print("[FAIL] %s" % exc)
        print("TOTAL: 1 failures")
        return 1


if __name__ == "__main__":
    sys.exit(main())
