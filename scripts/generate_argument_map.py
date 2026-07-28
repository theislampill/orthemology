#!/usr/bin/env python3
"""Deterministically render the Task 9 argument-map summary."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "companion" / "DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml"
COMPANION_PATH = ROOT / "companion" / "dynamic-orthing-noetic-learning-and-orthability.md"
SOURCE_STATUS_PATH = ROOT / "references" / "source-status.yaml"
BEGIN_MARKER = "<!-- BEGIN GENERATED ARGUMENT MAP -->"
END_MARKER = "<!-- END GENERATED ARGUMENT MAP -->"


def _mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def collect_issues(data: Any, source_registry: Any = None) -> list[str]:
    """Return bounded generator-side structural issues without touching files."""
    issues: list[str] = []
    model = _mapping(data)
    if model is None:
        return ["argument map must be a mapping"]
    nodes = model.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return ["nodes must be a non-empty list"]
    seen: set[str] = set()
    for index, raw in enumerate(nodes, start=1):
        if not isinstance(raw, dict):
            issues.append(f"node {index} must be a mapping")
            continue
        node_id = raw.get("id")
        if not isinstance(node_id, str) or not node_id:
            issues.append(f"node {index} missing stable id")
        elif node_id in seen:
            issues.append(f"duplicate node id {node_id}")
        else:
            seen.add(node_id)
        if raw.get("order") != index:
            issues.append(f"node {node_id or index} order must be {index}")
    if source_registry is not None:
        module_name = "_task9_argument_validator_for_generator"
        validator = sys.modules.get(module_name)
        if validator is None:
            validator_path = ROOT / "scripts" / "validate_argument_map.py"
            spec = importlib.util.spec_from_file_location(module_name, validator_path)
            if spec is None or spec.loader is None:
                issues.append("could not load independent semantic validator")
            else:
                validator = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = validator
                spec.loader.exec_module(validator)
        if validator is not None:
            for issue in validator.validate_mapping(data, source_registry):
                if issue not in issues:
                    issues.append(issue)
    return issues[:100]


def render_argument_map(data: Any, source_registry: Any = None) -> str:
    """Render the canonical ordered summary using LF only."""
    registry = source_registry
    if registry is None:
        registry = yaml.safe_load(SOURCE_STATUS_PATH.read_text(encoding="utf-8"))
    issues = collect_issues(data, registry)
    if issues:
        raise ValueError("; ".join(issues))
    model = copy.deepcopy(data)
    nodes = model["nodes"]
    lines = [
        "### Generated typed argument-node summary",
        "",
        f"Argument nodes: **{len(nodes)}**.",
        "",
        "| Order | Stable ID | Node | Scope | Inference / bridge | Claim role | Dependency | Rival exit |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for node in nodes:
        deps = ", ".join(node["dependencies"]) if node["dependencies"] else "none"
        inference = f"{node['inference_type']} / {node['bridge_status']}"
        rival = node["rival_exit"]["id"]
        cells = (
            str(node["order"]),
            f"`{node['id']}`",
            node["label"],
            node["scope"],
            inference,
            node["claim_role"],
            deps,
            rival,
        )
        lines.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in cells) + " |")
    lines.extend(
        [
            "",
            "The table is generated from the structured map. Cross-framework scope means",
            "dialectical accessibility and rival routing, not a neutral or coequal tribunal.",
            "The Atharī/Taymiyyan frame is the declared operative frame. The common-premise",
            "fittingness-to-Wisdom bridge remains held; actual divine Speech remains",
            "revelational and school-internal; OSM and DAEE validate neither metaphysics nor",
            "theology.",
            "",
        ]
    )
    return "\n".join(lines)


def replace_generated_section(document: str, rendered: str) -> str:
    """Replace exactly one non-nested marker pair and normalize LF."""
    normalized = document.replace("\r\n", "\n").replace("\r", "\n")
    rendered_normalized = rendered.replace("\r\n", "\n").replace("\r", "\n")
    if BEGIN_MARKER in rendered_normalized or END_MARKER in rendered_normalized:
        raise ValueError("rendered payload must not contain generated markers")
    if normalized.count(BEGIN_MARKER) != 1 or normalized.count(END_MARKER) != 1:
        raise ValueError("document must contain exactly one generated marker pair")
    begin = normalized.index(BEGIN_MARKER)
    end = normalized.index(END_MARKER)
    if begin >= end:
        raise ValueError("generated markers are reversed")
    interior = normalized[begin + len(BEGIN_MARKER) : end]
    if BEGIN_MARKER in interior or END_MARKER in interior:
        raise ValueError("generated markers are nested")
    replacement = f"{BEGIN_MARKER}\n{rendered_normalized.rstrip()}\n{END_MARKER}"
    return normalized[:begin] + replacement + normalized[end + len(END_MARKER) :]


def build() -> tuple[Path, str]:
    """Return the companion path and canonical expected LF text."""
    data = yaml.safe_load(MAP_PATH.read_text(encoding="utf-8"))
    registry = yaml.safe_load(SOURCE_STATUS_PATH.read_text(encoding="utf-8"))
    issues = collect_issues(data, registry)
    if issues:
        raise ValueError("; ".join(issues))
    current = COMPANION_PATH.read_text(encoding="utf-8")
    return COMPANION_PATH, replace_generated_section(
        current, render_argument_map(data, registry)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        path, expected = build()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"[FAIL] argument-map generation: {exc}")
        return 1
    current = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if args.check:
        if current != expected:
            print(f"[FAIL] generated argument map drift: {path.relative_to(ROOT)}")
            return 1
        print(f"[PASS] generated argument map current: {path.relative_to(ROOT)}")
        return 0
    path.write_text(expected, encoding="utf-8", newline="\n")
    print(f"[PASS] generated argument map updated: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
