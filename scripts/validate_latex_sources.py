#!/usr/bin/env python3
"""Validate generated LaTeX ownership, policy, and deterministic source parity."""

import argparse
import pathlib
import re
import sys

import yaml

from generate_latex_sources import (
    OUTPUT_PATH,
    PROFILE_PATH,
    ROOT,
    expected_latex_tree,
)


SHELL_ESCAPE_RE = re.compile(
    r"\\(?:immediate\s*)?write18\b|--shell-escape|\\ShellEscape\b",
    re.I,
)
ABSOLUTE_PATH_RE = re.compile(
    r"\\(?:input|include|bibliography)\{(?:[A-Za-z]:[/\\]|[/\\]{2})",
    re.I,
)
VENUE_METADATA_RE = re.compile(
    r"\\(?:conferenceinfo|acm[A-Za-z]*|IEEE[A-Za-z]*)\b",
    re.I,
)
PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}")
EXPECTED_DIRECT_PACKAGES = [
    "amsmath",
    "amssymb",
    "booktabs",
    "geometry",
    "hyperref",
    "microtype",
    "natbib",
    "needspace",
    "xcolor",
]


def validate_latex_tree(root=ROOT, profile=None, artifacts=None):
    root = pathlib.Path(root)
    if profile is None:
        profile = yaml.safe_load((root / PROFILE_PATH).read_text(encoding="utf-8"))
    if artifacts is None:
        artifacts = profile.get("artifacts", [])
    expected = expected_latex_tree(root, profile, artifacts)
    output = root / OUTPUT_PATH
    issues = []
    expected_paths = set(expected)
    actual_paths = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    } if output.is_dir() else set()
    for relative in sorted(expected_paths - actual_paths):
        issues.append("missing generated LaTeX: %s" % relative)
    for relative in sorted(actual_paths - expected_paths):
        issues.append("unexpected generated file: %s" % relative)

    direct_packages = profile.get("package_policy", {}).get("direct_packages")
    bibliography_owner = profile.get("source_ownership", {}).get(
        "bibliography_owner", ""
    )
    expected_bibliography = "../../../" + bibliography_owner.removesuffix(".bib")
    artifacts_by_id = {
        artifact.get("artifact_id"): artifact for artifact in artifacts
    }
    for relative in sorted(actual_paths & expected_paths):
        path = output / pathlib.PurePosixPath(relative)
        content = path.read_text(encoding="utf-8")
        if relative in expected and content != expected[relative]:
            issues.append("semantic divergence from Markdown owner: %s" % relative)
        if SHELL_ESCAPE_RE.search(content):
            issues.append("shell escape is prohibited: %s" % relative)
        if ABSOLUTE_PATH_RE.search(content):
            issues.append("absolute path is prohibited: %s" % relative)
        if VENUE_METADATA_RE.search(content):
            issues.append("venue metadata is prohibited: %s" % relative)
        packages = [
            package.strip()
            for match in PACKAGE_RE.finditer(content)
            for package in match.group(1).split(",")
        ]
        if direct_packages != EXPECTED_DIRECT_PACKAGES:
            issues.append("profile direct package policy is not exact")
        if packages != EXPECTED_DIRECT_PACKAGES:
            issues.append(
                "generated main package set is not exact in %s: %r"
                % (relative, packages)
            )
        if content.count(r"\bibliography{") != 1:
            issues.append("one bibliography owner required: %s" % relative)
        if r"\bibliography{%s}" % expected_bibliography not in content:
            issues.append("bibliography owner mismatch: %s" % relative)
        if (
            r"\documentclass[10pt,letterpaper,twocolumn]{article}"
            not in content
            or r"\twocolumn[" not in content
        ):
            issues.append("profile layout mismatch: %s" % relative)
        artifact_id = pathlib.PurePosixPath(relative).parts[0]
        artifact = artifacts_by_id.get(artifact_id, {})
        for qualification in artifact.get("source_qualifications", []):
            marker = "%% source-qualification: %s" % qualification
            if marker not in content:
                issues.append(
                    "source qualification missing in %s: %s"
                    % (relative, qualification)
                )
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args(argv)
    issues = validate_latex_tree(args.root)
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] generated LaTeX source ownership and policy")
    print("TOTAL: %d failures" % len(issues))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
