#!/usr/bin/env python3
"""Regression checks for the independently reviewed source transcription.

These checks preserve reviewed notation and graph coverage, not theorem truth.
The original PDF remains private and is not required to run the tests.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "research/source-fidelity/epistemic-tuples"
RECORD = json.loads((DIRECTORY / "FIDELITY.json").read_text(encoding="utf-8"))
README = (DIRECTORY / "README.md").read_text(encoding="utf-8")
SVG = (DIRECTORY / "architecture.svg").read_text(encoding="utf-8")


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def issues(markdown, svg_text, record):
    errors = []
    sections = re.findall(
        r"^### (F\d\d)\. ([\s\S]*?)(?=^### F\d\d\.|^## |\Z)",
        markdown, re.M,
    )
    if [key for key, _ in sections] != [f"F{i:02d}" for i in range(1, 31)]:
        errors.append("formula inventory")
    expected = {row["id"]: row for row in record["formula_groups"]}
    for key, body in sections:
        row = expected[key]
        if re.findall(r"^\$\$\n(.*?)\n\$\$", body, re.M | re.S) != row["tex"]:
            errors.append(key + " notation")
        coordinates = f"Physical p. {row['physical_page']} / printed p. {row['printed_page']}"
        if coordinates not in body:
            errors.append(key + " page binding")
    svg = ET.fromstring(svg_text)
    labels = {
        element.attrib["id"].removeprefix("node-"): " ".join("".join(element.itertext()).split())
        for element in svg.iter() if element.attrib.get("id", "").startswith("node-")
    }
    if labels != record["diagram"]["labels"]:
        errors.append("diagram labels")
    edges = [[e.attrib["data-from"], e.attrib["data-to"]]
             for e in svg.iter() if "data-from" in e.attrib]
    if edges != record["diagram"]["directed_edges"]:
        errors.append("directed edges")
    edge_group = next(e for e in svg if e.attrib.get("marker-end") == "url(#arrow)")
    if len(edge_group) != 11 or any(e.attrib.get("marker-start") for e in edge_group):
        errors.append("visible arrowheads")
    for i, (start, end) in enumerate(record["diagram"]["directed_edges"], 1):
        line = f"{i}. {labels[start]} → {labels[end]}"
        if line not in markdown.splitlines():
            errors.append(f"accessible edge {i}")
    table = [[c.strip() for c in line.strip("|").split("|")]
             for line in markdown.splitlines() if re.match(r"^\| L[0-7] \|", line)]
    if table != record["hierarchy"]["rows"]:
        errors.append("hierarchy table")
    for name, text in [("README.md", markdown), ("architecture.svg", svg_text)]:
        if digest(text.encode("utf-8")) != record["reviewed_artifacts"][name]:
            errors.append(name + " reviewed identity")
    return errors


class FidelityTests(unittest.TestCase):
    def test_reviewed_document(self):
        self.assertEqual(issues(README, SVG, RECORD), [])
        self.assertEqual(RECORD["fidelity_review"]["status"], "PASS_BOUNDED_SOURCE_FIDELITY")

    def test_immutable_sources_and_publication_boundary(self):
        for row in RECORD["immutable_sources"]:
            self.assertEqual(digest((ROOT / row["path"]).read_bytes()), row["sha256"])
        projection = json.loads((ROOT / RECORD["publication_eligibility"]["projection_manifest"]).read_text())
        objects = {row["source_sha256"]: row for row in projection["objects"]}
        pdf = objects[RECORD["original_pdf"]["sha256"]]
        self.assertEqual(pdf["declared_eligibility_basis"], "reviewed_owner_authored")
        self.assertEqual(pdf["disposition"], "NOT_PUBLISHED")
        self.assertEqual(pdf["reason"], "HOLD_UNQUALIFIED_BINARY_RENDER_VARIANT")
        self.assertFalse(list(DIRECTORY.rglob("*.pdf")))
        self.assertFalse(projection["scientific_acceptance"])
        self.assertFalse(projection["t21_started"])

    def test_inherited_coverage_dispositions(self):
        coverage = RECORD["inherited_binary_coverage"]
        rows = coverage["documents"]
        self.assertEqual([r["index"] for r in rows], list(range(1, 26)))
        self.assertEqual(len({r["original_binary_sha256"] for r in rows}), 25)
        self.assertEqual([r["index"] for r in rows if r["disposition"] == "DISTINCT_HISTORICAL_EXPRESSION_SUBSTANTIVELY_COVERED"], [1, 5, 7, 9, 12, 22])
        self.assertEqual([r["index"] for r in rows if r["disposition"] == "SOURCE_READING_FIDELITY_REPAIR"], [23])
        self.assertEqual(sum(r["disposition"] == "DUPLICATE_OR_RENDER_EQUIVALENT" for r in rows), 18)
        self.assertEqual(rows[22]["original_binary_sha256"], RECORD["original_pdf"]["sha256"])
        self.assertTrue(coverage["current_repair"]["original_disposition_retained"])
        self.assertEqual(coverage["summary"]["unique_unpublished_scientific_results_found"], 0)
        projection = json.loads((ROOT / RECORD["publication_eligibility"]["projection_manifest"]).read_text())
        held = {r["source_sha256"] for r in projection["objects"] if r["disposition"] == "NOT_PUBLISHED"}
        self.assertTrue({r["original_binary_sha256"] for r in rows}.issubset(held))

    def test_navigation_and_privacy(self):
        references = re.findall(r"^\[[^\]]+\]: (\S+)$", README, re.M)
        self.assertEqual(len(references), 20)
        for reference in references + ["architecture.svg", "FIDELITY.json"]:
            path, _, anchor = reference.partition("#")
            target = (DIRECTORY / path).resolve()
            self.assertTrue(target.is_relative_to(ROOT))
            self.assertTrue(target.is_file(), path)
            if anchor.startswith("L") and anchor[1:].isdigit():
                self.assertLessEqual(int(anchor[1:]), len(target.read_text().split("\n")))
        for path in DIRECTORY.iterdir():
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"(?i)(?:(?<![a-z])[a-z]:[\\/]|/mnt/[a-z]/|/home/|/Users/|file://|owner_private_handoff)", text), path.name)
        self.assertNotIn("<script", SVG.lower())
        self.assertNotIn("href=", SVG.lower())
        self.assertIn("not a claim about a uniquely correct psychology", README)
        self.assertIn("Separate mathematical correction", README)
        self.assertIn("#5-et05-strict-cone-repair-and-vector-equilibrium", README)

    def test_lost_mathematical_glyph_is_detected(self):
        for old, new, group in [
            (r"\mathcal E", "E", "F01"),
            (r"\setminus\{0\}", r"^\circ", "F16"),
            (r"\sigma_{-i}^*", r"\sigma_{-i}", "F13"),
            (r"\sum_{j=1}^k", r"\sum_j", "F06"),
        ]:
            with self.subTest(group=group):
                self.assertIn(group + " notation", issues(README.replace(old, new), SVG, RECORD))

    def test_missing_feedback_arrow_is_detected(self):
        changed = re.sub(r'^    <path id="edge-11"[^\n]+\n', "", SVG, flags=re.M)
        self.assertIn("directed edges", issues(README, changed, RECORD))

    def test_reversed_edge_is_detected(self):
        changed = SVG.replace('data-from="defeater" data-to="perception"', 'data-from="perception" data-to="defeater"')
        self.assertIn("directed edges", issues(README, changed, RECORD))

    def test_missing_accessible_edge_is_detected(self):
        changed = README.replace("11. action / judgment policy → memory / retention", "")
        self.assertIn("accessible edge 11", issues(changed, SVG, RECORD))

    def test_changed_hierarchy_qualification_is_detected(self):
        changed = README.replace("total ranking is not assumed.", "total ranking is assumed.")
        self.assertIn("hierarchy table", issues(changed, SVG, RECORD))


if __name__ == "__main__":
    unittest.main()
