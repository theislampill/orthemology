#!/usr/bin/env python3
"""Byte custody and bounded relational checks only; not source authentication."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
AUTHOR = BASE / "intrinsic-representation-dependency-20261010"


def load(path):
    return json.loads(path.read_bytes())


def text(path):
    return path.read_bytes().decode("utf-8")


def check_record(root, row):
    data = (root / row["path"]).read_bytes()
    assert len(data) == row["bytes"], row["path"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]


bindings = load(HERE / "REVIEW_BINDINGS.json")
for row in bindings["records"]:
    check_record(BASE, row)

manifest = load(AUTHOR / "MANIFEST.json")
for row in manifest["files"]:
    check_record(AUTHOR, row)
inputs = load(AUTHOR / "INPUT_BINDINGS.json")
for row in inputs["records"]:
    check_record(BASE, row)

appendix = text(AUTHOR / "SOURCE_APPENDIX.md")
verses = []
for name in ["QURAN18_60_64_CONNECTOR.json", "QURAN18_65_82_CONNECTOR.json"]:
    for item in load(AUTHOR / name):
        assert not item["result"].get("isError")
        body = json.loads(item["result"]["content"][0]["text"])
        assert body["surah"] == 18 and body["ayah"] == item["ayah"]
        assert body["text"] in appendix
        verses.append(body["ayah"])
assert verses == list(range(60, 83))

parts = []
commentary_count = 0
for name, ayah in [("IBN_KATHIR18_79_CONNECTOR.json", 79),
                   ("IBN_KATHIR18_82_CONNECTOR.json", 82)]:
    raw = load(AUTHOR / name)
    for response in raw if isinstance(raw, list) else [raw]:
        assert not response.get("isError")
        body = json.loads(response["content"][0]["text"])
        assert body["surah"] == 18 and body["ayah"] == ayah
        for tafsir in body["tafsirs"]:
            assert tafsir["source"] == "katheer"
            assert tafsir["attribution"] in appendix
            assert tafsir["text"] in appendix
            commentary_count += 1
            if ayah == 82:
                assert tafsir["total_parts"] == 4
                parts.append(tafsir["part"])
assert parts == [1, 2, 3, 4]

parent16 = text(BASE / "particular-determination-semantics-20261010/sources/majmu16-context.txt")
assert text(AUTHOR / "MAJMU16_297_309.txt") in parent16
assert text(AUTHOR / "MAJMU16_310_312.txt") in parent16
assert text(AUTHOR / "MAJMU10_473_479.txt") in text(AUTHOR / "MAJMU10_fatwa154.txt")

logical = load(AUTHOR / "LOGICAL_CHECK.json")
assert logical["guidance"] == [["r", "w"]]
assert logical["production"] == [["u", "r"], ["w", "q"]]
adjacency = {}
for origin, destination in logical["production"]:
    adjacency.setdefault(origin, []).append(destination)


def visit(node, stack):
    assert node not in stack, "productive cycle"
    for child in adjacency.get(node, []):
        visit(child, stack | {node})


for node in adjacency:
    visit(node, set())
assert logical["metaphysical_possibility_claim"] is False
assert logical["adequacy_claim"] is False

print(json.dumps({
    "status": "PASS",
    "review_bound_files": len(bindings["records"]),
    "author_manifest_entries": len(manifest["files"]),
    "author_input_records": len(inputs["records"]),
    "consecutive_verse_responses": len(verses),
    "commentary_parts": commentary_count,
    "literal_excerpt_checks": 3,
    "displayed_productive_relation_acyclic": True,
    "source_authentication_or_metaphysical_validation": False,
    "review_bindings_sha256": hashlib.sha256((HERE / "REVIEW_BINDINGS.json").read_bytes()).hexdigest(),
    "review_sha256": hashlib.sha256((HERE / "REVIEW.md").read_bytes()).hexdigest()
}, indent=2))
