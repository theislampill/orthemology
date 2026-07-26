#!/usr/bin/env python3
"""Validate Task 10 terminology formation and provenance boundaries.

Offline only. This validator checks fixture behavior, record shape, bounded
live-prose agreement, readiness ownership, and frozen packet bytes. It does not
verify external scholarly truth.
"""
from __future__ import annotations

import copy
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "terminology-etymology-fixtures.yaml"

FAILURE_CODES = {
    "E_EMMA_ENGLISH_SUFFIX",
    "E_EMA_DERIVATION",
    "E_UNQUALIFIED_GREEK_DERIVATION",
    "E_ORTHEME_ORIGINALITY",
    "E_SOURCE_SCOPE",
    "E_ATTESTATION_ADOPTION",
    "E_TERMINOLOGY_ADOPTION",
    "E_OBJECT_WORD_COLLAPSE",
    "E_UNIVERSALITY",
    "E_PROVEN_ISOMORPHISM",
    "E_NEGATIVE_SEARCH_NOVELTY",
    "E_UTILITY_OVERCLAIM",
    "E_TASK_RELATIVE_PRIMITIVE",
    "E_READINESS_STATE",
    "E_BENCHMARK_BYPASS",
}

ASSERTIONS = {
    "CONSTRUCTED_GROUNDED": ("constructed", "morphologically grounded"),
    "ORTH_SCOPE": ("orth-", "correct or corrective"),
    "EME_SCOPE": ("-eme", "analogy"),
    "MA_MAT_SCOPE": ("-ma", "-mat-", "result or effect"),
    "EMA_RESONANCE": ("ἐμά", "possessive resonance", "not a derivation"),
    "PRIOR_DIFFERENT_SENSE": ("ortheme", "orthographic-unit sense"),
    "NON_ADOPTION": ("does not adopt",),
    "BENCHMARK_GATE": ("benchmark-gated", "mnemonic or meta-schema hypothesis"),
    "ANALYSIS_RELATIVE_GLOSSARY": (
        "relative to a declared, versioned analysis",
        "task-relative wording is shorthand only after one analysis",
    ),
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.translate(str.maketrans({
        "–": "-", "—": "-", "−": "-", "‑": "-",
        "’": "'", "‘": "'", "ʼ": "'", "`": "'",
    }))
    return " ".join(text.split())


def claim_failures(text: str) -> set[str]:
    n = normalize(text)
    failures: set[str] = set()
    if re.search(r"\b(inherited|productive) english suffix -?emma\b", n):
        failures.add("E_EMMA_ENGLISH_SUFFIX")
    if re.search(r"greek (?:ema|ἐμά).{0,45}(?:deriv(?:es|ation)|origin).{0,35}(?:-?ma|-?emma)", n):
        failures.add("E_EMA_DERIVATION")
    if "greek-derived terms" in n and not (
        "constructed" in n and ("analog" in n or "morphologically grounded" in n)
    ):
        failures.add("E_UNQUALIFIED_GREEK_DERIVATION")
    if re.search(r"(?:first coined|original coinage|uniquely coined).{0,35}\bortheme\b", n):
        failures.add("E_ORTHEME_ORIGINALITY")
    if (
        re.search(r"(?:1999|orthographic-unit use).{0,70}(?:establishes|proves).{0,45}project", n)
        or re.search(r"(?:smyth|merriam-webster).{0,45}(?:establishes|proves).{0,45}(?:complete )?project definition", n)
    ):
        failures.add("E_SOURCE_SCOPE")
    if (
        re.search(r"historical attestation.{0,25}(?:means|therefore|so).{0,25}(?:adopts|adoption)", n)
        or re.search(r"(?:earlier spelling collision|prior attestation).{0,55}(?:retire|rename)", n)
    ):
        failures.add("E_ATTESTATION_ADOPTION")
    if re.search(r"(?:project vocabulary|project terms|terminology).{0,25}(?:is|are) adopted", n):
        failures.add("E_TERMINOLOGY_ADOPTION")
    if re.search(r"decision 0002 adopts the word metaorthemma", n):
        failures.add("E_OBJECT_WORD_COLLAPSE")
    if "universal primitives" in n and not re.search(
        r"(?:not|never|no).{0,15}universal primitives", n
    ):
        failures.add("E_UNIVERSALITY")
    if re.search(r"(?:proves?|proven).{0,40}cross-domain isomorphism", n):
        failures.add("E_PROVEN_ISOMORPHISM")
    if (
        re.search(r"bounded search found no hit.{0,55}(?:unique|original|novel|first)", n)
        or re.search(r"no (?:authoritative )?hit.{0,55}(?:proves?|establishes)(?! no).{0,30}(?:novel|unique|original|first)", n)
    ):
        failures.add("E_NEGATIVE_SEARCH_NOVELTY")
    if re.search(r"(?:examples|morphology).{0,35}(?:establish|prove).{0,35}cross-domain utility", n):
        failures.add("E_UTILITY_OVERCLAIM")
    if re.search(
        r"o\*_t\(m\).{0,35}(?:is|as).{0,20}(?:the )?primitive.{0,45}(?:every|multiple|all) analys",
        n,
    ):
        failures.add("E_TASK_RELATIVE_PRIMITIVE")
    if "ready_to_run" in n and re.search(r"human matching review.{0,20}pending", n):
        failures.add("E_READINESS_STATE")
    if re.search(
        r"(?:repeated repository use|historical attestation|morphology|examples).{0,55}"
        r"(?:establish|prove).{0,35}(?:terminology )?utility.{0,45}"
        r"(?:without|bypass).{0,30}(?:matched )?benchmark",
        n,
    ):
        failures.add("E_BENCHMARK_BYPASS")
    return failures


def _duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def validate_fixture_document(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema") != "terminology-etymology-fixtures-v1":
        return ["fixture schema must be terminology-etymology-fixtures-v1"]
    rules = data.get("rules")
    invalid = data.get("invalid_cases")
    valid = data.get("valid_controls")
    if not all(isinstance(value, list) for value in (rules, invalid, valid)):
        return ["rules, invalid_cases, and valid_controls must be lists"]
    rule_ids = [row.get("id") for row in rules if isinstance(row, dict)]
    codes = [row.get("failure_code") for row in rules if isinstance(row, dict)]
    if len(rule_ids) != len(rules) or any(not value for value in rule_ids):
        errors.append("every rule requires an id")
    if _duplicates(rule_ids):
        errors.append("duplicate rule ids: %s" % _duplicates(rule_ids))
    string_codes = [code for code in codes if isinstance(code, str) and code]
    if len(string_codes) != len(rules):
        errors.append("every rule requires a string failure_code")
    if _duplicates(string_codes):
        errors.append("duplicate rule failure codes: %s" % _duplicates(string_codes))
    unknown_rules = sorted(set(string_codes) - FAILURE_CODES)
    if unknown_rules:
        errors.append("unknown rule failure codes: %s" % unknown_rules)
    cases = invalid + valid
    case_ids = [row.get("id") for row in cases if isinstance(row, dict)]
    if len(case_ids) != len(cases) or any(not value for value in case_ids):
        errors.append("every fixture case requires an id")
    if _duplicates(case_ids):
        errors.append("duplicate fixture case ids: %s" % _duplicates(case_ids))
    for row in cases:
        if not isinstance(row, dict) or not isinstance(row.get("prose"), str):
            errors.append("fixture cases require one prose string")
            continue
        declared = row.get("expected_failure_codes")
        if not isinstance(declared, list):
            errors.append("%s expected_failure_codes must be a list" % row.get("id"))
            continue
        unknown = sorted(set(declared) - FAILURE_CODES)
        if unknown:
            errors.append("%s declares unknown failures: %s" % (row.get("id"), unknown))
        actual = claim_failures(row["prose"])
        if actual != set(declared):
            errors.append("%s expected %s but produced %s" % (
                row.get("id"), sorted(declared), sorted(actual)))
    return errors


def validate_mutation_controls(data: dict) -> list[str]:
    """Prove representative malformed and duplicate fixtures are rejected."""
    errors: list[str] = []
    mutations: list[tuple[str, dict, str]] = []

    malformed = copy.deepcopy(data)
    malformed["valid_controls"] = {}
    mutations.append(("malformed fixture collection", malformed, "must be lists"))

    duplicate = copy.deepcopy(data)
    duplicate["invalid_cases"][1]["id"] = duplicate["invalid_cases"][0]["id"]
    mutations.append(("duplicate fixture id", duplicate, "duplicate fixture case ids"))

    unknown = copy.deepcopy(data)
    unknown["invalid_cases"][0]["expected_failure_codes"] = ["E_UNKNOWN"]
    mutations.append(("unknown failure code", unknown, "unknown failures"))

    missing_code = copy.deepcopy(data)
    del missing_code["rules"][0]["failure_code"]
    mutations.append(("missing rule failure code", missing_code, "string failure_code"))

    for label, mutation, diagnostic in mutations:
        actual = validate_fixture_document(mutation)
        if not any(diagnostic in item for item in actual):
            errors.append("%s was not rejected with %s" % (label, diagnostic))

    for text, diagnostic in (
        ("START x END START y END", "exactly once"),
        ("END x START", "reversed"),
    ):
        try:
            extract_region(text, "START", "END")
        except ValueError as exc:
            if diagnostic not in str(exc):
                errors.append("region mutation lacked diagnostic %s" % diagnostic)
        else:
            errors.append("region mutation was accepted: %s" % diagnostic)
    return errors


def extract_region(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError("bounded region markers must each occur exactly once")
    start_at = text.index(start) + len(start)
    end_at = text.index(end)
    if end_at <= start_at:
        raise ValueError("bounded region markers are reversed or empty")
    return text[start_at:end_at]


def _packet_digest(packet: Path) -> str:
    digest = hashlib.sha256()
    paths = sorted(
        (path for path in packet.rglob("*")
         if path.is_file() and path.name != "FREEZE-HASH.txt"),
        key=lambda path: path.relative_to(packet).as_posix(),
    )
    for path in paths:
        digest.update(path.relative_to(packet).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def validate_live_documents(root: Path, data: dict) -> list[str]:
    errors: list[str] = []
    for owner in data.get("required_live_claims", []):
        path = root / owner["document"]
        if not path.exists():
            errors.append("%s is missing" % owner["document"])
            continue
        text = path.read_text(encoding="utf-8")
        try:
            region = extract_region(text, owner["start_marker"], owner["end_marker"])
        except ValueError as exc:
            errors.append("%s: %s" % (owner["document"], exc))
            continue
        unsafe = claim_failures(region)
        if unsafe:
            errors.append("%s has unsafe claims: %s" % (owner["document"], sorted(unsafe)))
        normalized_region = normalize(region)
        for assertion_id in owner.get("required_assertion_ids", []):
            needles = ASSERTIONS.get(assertion_id)
            if not needles:
                errors.append("unknown assertion id %s" % assertion_id)
            elif not all(normalize(needle) in normalized_region for needle in needles):
                errors.append("%s lacks assertion %s" % (owner["document"], assertion_id))
    for requirement in data.get("required_document_assertions", []):
        path = root / requirement["document"]
        assertion_id = requirement["assertion_id"]
        needles = ASSERTIONS.get(assertion_id)
        if not path.exists() or not needles:
            errors.append("%s document assertion is malformed" % assertion_id)
            continue
        normalized_text = normalize(path.read_text(encoding="utf-8"))
        if not all(normalize(needle) in normalized_text for needle in needles):
            errors.append("%s lacks assertion %s" % (
                requirement["document"], assertion_id))
    readiness = data.get("required_readiness") or {}
    readiness_path = root / str(readiness.get("document", ""))
    if not readiness_path.exists():
        errors.append("readiness owner is missing")
    else:
        text = readiness_path.read_text(encoding="utf-8")
        exact = str(readiness.get("exact_state", ""))
        if exact not in text:
            errors.append("readiness owner lacks exact state %s" % exact)
        if "READY TO RUN" in text:
            errors.append("readiness owner retains contradictory READY TO RUN wording")
    for packet in data.get("frozen_packets", []):
        actual = _packet_digest(root / packet["path"])
        if actual != packet["sha256"]:
            errors.append("%s packet hash drift: %s" % (packet["path"], actual))
    return errors


def validate_source_records(root: Path, data: dict) -> list[str]:
    errors: list[str] = []
    source_path = root / "references" / "source-status.yaml"
    bib_path = root / "references" / "orthemology.bib"
    try:
        registry = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return ["source-status YAML parse failed: %s" % exc]
    claims = registry.get("claims") if isinstance(registry, dict) else None
    if not isinstance(claims, list):
        return ["source-status claims must be a list"]
    if any(not isinstance(row, dict) for row in claims):
        return ["source-status claim rows must be mappings"]
    ids = [row.get("id") for row in claims]
    if any(not isinstance(row_id, str) or not row_id for row_id in ids) or _duplicates(ids):
        errors.append("source-status rows must have unique ids")
    families = registry.get("covered_claim_families") or {}
    if (families.get("terminology_provenance") or {}).get("prefix") != "ETY":
        errors.append("terminology_provenance family with ETY prefix is missing")
    bib = bib_path.read_text(encoding="utf-8")
    bib_keys = re.findall(r"@\w+\{([^,\s]+),", bib)
    for required in data.get("required_source_rows", []):
        row_id = required["id"]
        key = required["bibliography_key"]
        matching = [row for row in claims if row.get("id") == row_id]
        if len(matching) != 1:
            errors.append("%s must occur exactly once in source status" % row_id)
        if bib_keys.count(key) != 1:
            errors.append("%s must occur exactly once in bibliography" % key)
    return errors


def _print_result(label: str, errors: list[str]) -> int:
    if errors:
        for error in errors:
            print("[FAIL] %s — %s" % (label, error))
        return len(errors)
    print("[PASS] %s" % label)
    return 0


def main() -> int:
    try:
        data = yaml.safe_load(FIXTURES.read_text(encoding="utf-8"))
    except Exception as exc:
        print("[FAIL] fixture YAML parse — %s" % exc)
        print("TOTAL: 1 failures")
        return 1
    failures = 0
    failures += _print_result("fixture structure and semantic cases",
                              validate_fixture_document(data))
    failures += _print_result("malformed and duplicate fixture mutations",
                              validate_mutation_controls(data))
    failures += _print_result("bounded live terminology claims",
                              validate_live_documents(ROOT, data))
    failures += _print_result("terminology source and bibliography records",
                              validate_source_records(ROOT, data))
    print("TOTAL: %d failures" % failures)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
