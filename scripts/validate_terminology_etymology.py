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


def _claim_clauses(text: str) -> list[str]:
    return [
        clause.strip()
        for clause in re.split(r"(?<=[.!?;])\s+|\n+", text)
        if clause.strip()
    ]


def _positive_claim_role(
    clause: str,
    subject_pattern: str,
    predicate_pattern: str,
    object_pattern: str,
    *,
    complement_pattern: str = r"\s*",
    max_span: int = 220,
) -> bool:
    """Match a bounded positive subject-predicate-object claim in one clause."""
    subjects = list(re.finditer(subject_pattern, clause))
    predicates = list(re.finditer(predicate_pattern, clause))
    objects = list(re.finditer(object_pattern, clause))
    for subject in subjects:
        for predicate in predicates:
            if predicate.start() < subject.end():
                continue
            for claimed_object in objects:
                if claimed_object.start() < predicate.end():
                    continue
                if claimed_object.end() - subject.start() > max_span:
                    continue
                complement = clause[predicate.end():claimed_object.start()]
                if not re.fullmatch(complement_pattern, complement):
                    continue
                predicate_prefix = clause[subject.end():predicate.start()]
                predicate_negation = re.search(
                    r"\b(?P<negator>not|never|neither|without)"
                    r"(?P<modifiers>(?:\s+[a-z]+(?:-[a-z]+)*ly){0,2})\s*$",
                    predicate_prefix,
                )
                contrastive_not = (
                    predicate_negation
                    and predicate_negation.group("negator") == "not"
                    and re.search(
                        r"\b(?:only|merely)\b",
                        predicate_negation.group("modifiers"),
                    )
                )
                predicate_is_negated = predicate_negation and not contrastive_not
                object_is_negated = re.match(
                    r"(?:no|none|neither)\b",
                    claimed_object.group(0),
                )
                if predicate_is_negated or object_is_negated:
                    continue
                return True
    return False


def claim_failures(text: str) -> set[str]:
    n = normalize(text)
    clauses = _claim_clauses(n)
    failures: set[str] = set()
    if re.search(r"\b(inherited|productive) english suffix -?emma\b", n):
        failures.add("E_EMMA_ENGLISH_SUFFIX")
    if re.search(r"greek (?:ema|ἐμά).{0,45}(?:deriv(?:es|ation)|origin).{0,35}(?:-?ma|-?emma)", n):
        failures.add("E_EMA_DERIVATION")
    if "greek-derived terms" in n and not (
        "constructed" in n and ("analog" in n or "morphologically grounded" in n)
    ):
        failures.add("E_UNQUALIFIED_GREEK_DERIVATION")
    if (
        re.search(r"(?:first coined|original coinage|uniquely coined).{0,35}\bortheme\b", n)
        or re.search(
            r"\b(?:this project|the project|we|the authors?)\b.{0,35}"
            r"(?:introduced|created|originated).{0,20}\bortheme\b.{0,35}"
            r"(?:before any prior use|before all prior use|first|earliest)",
            n,
        )
    ):
        failures.add("E_ORTHEME_ORIGINALITY")
    if (
        re.search(r"(?:1999|orthographic-unit use).{0,70}(?:establishes|proves).{0,45}project", n)
        or re.search(r"(?:smyth|merriam-webster).{0,45}(?:establishes|proves).{0,45}(?:complete )?project definition", n)
        or re.search(
            r"(?:smyth|lsj|merriam-webster|constable|burridge|blaxter|unicode|"
            r"dictionary|grammar|lexicon).{0,45}(?:defines?|gives?|supplies?|fixes?|"
            r"determines?).{0,35}(?:ortheme|orthemma).{0,30}"
            r"(?:project-specific|project's).{0,15}(?:meaning|definition|sense)",
            n,
        )
        or any(
            _positive_claim_role(
                clause,
                r"\b(?:smyth|lsj|merriam-webster|constable|burridge|blaxter|"
                r"unicode|dictionary|grammar|lexicon)\b",
                r"\b(?:shows?|defines?|gives?|supplies?|fixes?|determines?|"
                r"establishes?|proves?)\b",
                r"(?:\b(?:ortheme|orthemma)\b.{0,45}\b(?:correct |complete )?"
                r"(?:project(?:'s|-specific)? )?(?:definition|meaning|sense)\b|"
                r"\b(?:correct |complete )?project(?:'s|-specific)? "
                r"(?:definition|meaning|sense)\b.{0,30}\b(?:ortheme|orthemma)\b)",
                complement_pattern=r"\s*(?:that\s+)?",
            )
            for clause in clauses
        )
    ):
        failures.add("E_SOURCE_SCOPE")
    if (
        re.search(r"historical attestation.{0,25}(?:means|therefore|so).{0,25}(?:adopts|adoption)", n)
        or re.search(r"(?:earlier spelling collision|prior attestation).{0,55}(?:retire|rename)", n)
    ):
        failures.add("E_ATTESTATION_ADOPTION")
    if (
        re.search(r"(?:project vocabulary|project terms|terminology).{0,25}(?:is|are) adopted", n)
        or re.search(
            r"(?:candidate vocabulary|project vocabulary|coined vocabulary|project terms|"
            r"candidate terms|the terminology|these terms).{0,40}"
            r"(?:has|have) been accepted.{0,35}(?:official|project|terminology|vocabulary)",
            n,
        )
        or any(
            _positive_claim_role(
                clause,
                r"\bproject\b",
                r"\b(?:adopts?|adopted|accepts?|accepted|approves?|approved)\b",
                r"\b(?:all |any |the |no )?(?:candidate |coined |project )?"
                r"(?:terms|terminology|vocabulary)\b",
                complement_pattern=r"\s*",
            )
            for clause in clauses
        )
    ):
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
        or any(
            _positive_claim_role(
                clause,
                r"\b(?:a |the )?bounded(?: negative)? search\b",
                r"\b(?:proves?|establishes?|shows?|demonstrates?|confirms?)\b",
                r"\b(?:the )?(?:first coinage|first use|novelty|originality|"
                r"priority|earliest use|uniqueness)\b",
                complement_pattern=r"\s*(?:(?:that\s+)?(?:this|it)\s+is\s+)?",
            )
            for clause in clauses
        )
    ):
        failures.add("E_NEGATIVE_SEARCH_NOVELTY")
    if re.search(r"(?:examples|morphology).{0,35}(?:establish|prove).{0,35}cross-domain utility", n):
        failures.add("E_UTILITY_OVERCLAIM")
    if re.search(
        r"o\*_t\(m\).{0,35}(?:is|as).{0,20}(?:the )?primitive.{0,45}(?:every|multiple|all) analys",
        n,
    ):
        failures.add("E_TASK_RELATIVE_PRIMITIVE")
    if re.search(
        r"o\*_t\(m\).{0,55}(?:supplies?|defines?|gives?|is).{0,35}"
        r"(?:task-wide )?ground truth.{0,55}(?:all|every|any|multiple) analys",
        n,
    ):
        failures.add("E_TASK_RELATIVE_PRIMITIVE")
    if (
        "ready_to_run" in n
        and (
            "ready_for_human_matching_review" in n
            or re.search(r"human matching review.{0,20}pending", n)
        )
    ):
        failures.add("E_READINESS_STATE")
    if re.search(
        r"(?:repeated repository use|historical attestation|morphology|examples).{0,55}"
        r"(?:establish|prove).{0,35}(?:terminology )?utility.{0,45}"
        r"(?:without|bypass).{0,30}(?:matched )?benchmark",
        n,
    ):
        failures.add("E_BENCHMARK_BYPASS")
    return failures


def _duplicates(values: list) -> list:
    duplicates: list = []
    for value in values:
        if values.count(value) > 1 and not any(value == item for item in duplicates):
            duplicates.append(value)
    return sorted(duplicates, key=lambda value: str(value))


def _split_bibtex_fields(body: str, key: str) -> tuple[dict[str, str], list[str]]:
    parts: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(body):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"' and depth == 0:
            quoted = not quoted
        elif not quoted:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth < 0:
                    return {}, ["bibliography entry %s has an unmatched closing brace" % key]
            elif char == "," and depth == 0:
                parts.append(body[start:index])
                start = index + 1
    if depth != 0 or quoted:
        return {}, ["bibliography entry %s has an unclosed field value" % key]
    parts.append(body[start:])

    fields: dict[str, str] = {}
    errors: list[str] = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            errors.append("bibliography entry %s has malformed field %r" % (key, part))
            continue
        name, value = part.split("=", 1)
        name = name.strip().casefold()
        value = value.strip()
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", name) or not value:
            errors.append("bibliography entry %s has malformed field assignment" % key)
            continue
        if name in fields:
            errors.append("bibliography entry %s has duplicate field %s" % (key, name))
            continue
        if value.startswith("{"):
            if not value.endswith("}"):
                errors.append("bibliography entry %s field %s is unclosed" % (key, name))
                continue
        elif value.startswith('"'):
            if not value.endswith('"'):
                errors.append("bibliography entry %s field %s is unclosed" % (key, name))
                continue
        fields[name] = value
    return fields, errors


def parse_bibtex(text: str) -> tuple[list[dict], list[str]]:
    """Parse entry boundaries and fields without accepting unclosed structures."""
    entries: list[dict] = []
    errors: list[str] = []
    index = 0
    length = len(text)
    while index < length:
        if text[index].isspace():
            index += 1
            continue
        if text[index] == "%":
            newline = text.find("\n", index)
            index = length if newline < 0 else newline + 1
            continue
        if text[index] != "@":
            line_end = text.find("\n", index)
            excerpt = text[index:(length if line_end < 0 else line_end)].strip()
            errors.append("unexpected bibliography content outside an entry: %r" % excerpt[:60])
            index = length if line_end < 0 else line_end + 1
            continue

        entry_start = index
        index += 1
        type_match = re.match(r"[A-Za-z]+", text[index:])
        if not type_match:
            errors.append("bibliography entry at offset %d lacks an entry type" % entry_start)
            index += 1
            continue
        entry_type = type_match.group(0).casefold()
        index += len(type_match.group(0))
        while index < length and text[index].isspace():
            index += 1
        if index >= length or text[index] not in "{(":
            errors.append("bibliography entry at offset %d lacks an opening delimiter" % entry_start)
            continue
        opening = text[index]
        closing = "}" if opening == "{" else ")"
        index += 1
        key_start = index
        while index < length and text[index] not in "," + closing:
            index += 1
        key = text[key_start:index].strip()
        if not key or index >= length or text[index] != ",":
            errors.append("bibliography entry at offset %d lacks a key and field separator" % entry_start)
            if index < length:
                index += 1
            continue
        index += 1
        body_start = index
        brace_depth = 0
        quoted = False
        escaped = False
        while index < length:
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"' and brace_depth == 0:
                quoted = not quoted
            elif not quoted:
                if char == "{":
                    brace_depth += 1
                elif char == "}":
                    if opening == "{" and brace_depth == 0:
                        break
                    brace_depth -= 1
                    if brace_depth < 0:
                        break
                elif char == closing and opening == "(" and brace_depth == 0:
                    break
            index += 1
        if index >= length:
            errors.append("unclosed bibliography entry %s" % key)
            break
        body = text[body_start:index]
        index += 1
        fields, field_errors = _split_bibtex_fields(body, key)
        errors.extend(field_errors)
        entries.append({
            "type": entry_type,
            "key": key,
            "fields": fields,
            "raw": text[entry_start:index],
            "start": entry_start,
            "end": index,
        })
    return entries, errors


def _bibtex_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and (
        (value[0] == "{" and value[-1] == "}")
        or (value[0] == '"' and value[-1] == '"')
    ):
        value = value[1:-1]
    return value.replace(r"\%", "%").strip()


def validate_fixture_document(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or data.get("schema") != "terminology-etymology-fixtures-v1":
        return ["fixture schema must be terminology-etymology-fixtures-v1"]
    rules = data.get("rules")
    invalid = data.get("invalid_cases")
    valid = data.get("valid_controls")
    if not all(isinstance(value, list) for value in (rules, invalid, valid)):
        return ["rules, invalid_cases, and valid_controls must be lists"]
    for label, value in (
        ("rules", rules),
        ("invalid_cases", invalid),
        ("valid_controls", valid),
    ):
        if not value:
            errors.append("%s must be nonempty" % label)
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
    missing_rules = sorted(FAILURE_CODES - set(string_codes))
    if missing_rules:
        errors.append("rules omit failure codes: %s" % missing_rules)
    cases = invalid + valid
    case_ids = [row.get("id") for row in cases if isinstance(row, dict)]
    if len(case_ids) != len(cases) or any(not value for value in case_ids):
        errors.append("every fixture case requires an id")
    if _duplicates(case_ids):
        errors.append("duplicate fixture case ids: %s" % _duplicates(case_ids))
    covered_codes: set[str] = set()
    for row in invalid:
        if not isinstance(row, dict) or not isinstance(row.get("prose"), str):
            errors.append("fixture cases require one prose string")
            continue
        declared = row.get("expected_failure_codes")
        if not isinstance(declared, list) or not declared:
            errors.append("%s expected_failure_codes must be a list" % row.get("id"))
            continue
        unknown = sorted(set(declared) - FAILURE_CODES)
        if unknown:
            errors.append("%s declares unknown failures: %s" % (row.get("id"), unknown))
        covered_codes.update(code for code in declared if isinstance(code, str))
        actual = claim_failures(row["prose"])
        if actual != set(declared):
            errors.append("%s expected %s but produced %s" % (
                row.get("id"), sorted(declared), sorted(actual)))
    uncovered_codes = sorted(set(string_codes) - covered_codes)
    if uncovered_codes:
        errors.append("rules lack invalid-case coverage: %s" % uncovered_codes)
    for row in valid:
        if not isinstance(row, dict) or not isinstance(row.get("prose"), str):
            errors.append("fixture cases require one prose string")
            continue
        declared = row.get("expected_failure_codes")
        if declared != []:
            errors.append("%s valid control must declare no failures" % row.get("id"))
            continue
        actual = claim_failures(row["prose"])
        if actual:
            errors.append("%s valid control produced %s" % (
                row.get("id"), sorted(actual)))

    source_rows = data.get("required_source_rows")
    if not isinstance(source_rows, list) or not source_rows:
        errors.append("required_source_rows must be a nonempty list")
    else:
        required_source_fields = {
            "id", "bibliography_key", "claim_level", "claim", "source_type",
            "status", "direct_support", "exclusions", "exclusion_statement",
            "locator", "identifier",
        }
        source_ids: list[str] = []
        bibliography_keys: list[str] = []
        for position, row in enumerate(source_rows, 1):
            if not isinstance(row, dict):
                errors.append("required source rows must be mappings")
                continue
            missing = sorted(required_source_fields - set(row))
            if missing:
                errors.append("required source row %d source expectation lacks fields: %s" % (
                    position, missing))
            if not isinstance(row.get("exclusions"), list) or not row.get("exclusions"):
                errors.append("%s exclusions must be a nonempty list" % row.get("id"))
            identifier = row.get("identifier")
            if (
                not isinstance(identifier, dict)
                or identifier.get("field") not in {"doi", "url"}
                or not isinstance(identifier.get("value"), str)
                or not identifier.get("value")
            ):
                errors.append("%s identifier expectation is malformed" % row.get("id"))
            if isinstance(row.get("id"), str) and row.get("id"):
                source_ids.append(row["id"])
            else:
                errors.append("required source row %d requires a string id" % position)
            if isinstance(row.get("bibliography_key"), str) and row.get("bibliography_key"):
                bibliography_keys.append(row["bibliography_key"])
            else:
                errors.append("required source row %d requires a bibliography key" % position)
        if _duplicates(source_ids):
            errors.append("duplicate required source ids: %s" % _duplicates(source_ids))
        if _duplicates(bibliography_keys):
            errors.append("duplicate required bibliography keys: %s" % _duplicates(bibliography_keys))

    live_claims = data.get("required_live_claims")
    if not isinstance(live_claims, list) or not live_claims:
        errors.append("required_live_claims must be a nonempty list")
    else:
        live_fields = {"document", "start_marker", "end_marker", "required_assertion_ids"}
        for position, owner in enumerate(live_claims, 1):
            if not isinstance(owner, dict):
                errors.append("live claim expectations must be mappings")
                continue
            missing = sorted(live_fields - set(owner))
            if missing:
                errors.append("required live claim row %d live claim expectation lacks fields: %s" % (
                    position, missing))
                continue
            assertion_ids = owner.get("required_assertion_ids")
            if not isinstance(assertion_ids, list) or not assertion_ids:
                errors.append("required live claim row %d requires assertion ids" % position)
            else:
                unknown = sorted(set(assertion_ids) - set(ASSERTIONS))
                if unknown:
                    errors.append("required live claim row %d has unknown assertions: %s" % (
                        position, unknown))

    document_assertions = data.get("required_document_assertions")
    if not isinstance(document_assertions, list) or not document_assertions:
        errors.append("required_document_assertions must be a nonempty list")
    else:
        for position, requirement in enumerate(document_assertions, 1):
            if (
                not isinstance(requirement, dict)
                or not isinstance(requirement.get("document"), str)
                or requirement.get("assertion_id") not in ASSERTIONS
            ):
                errors.append("document assertion row %d is malformed" % position)

    readiness = data.get("required_readiness")
    if (
        not isinstance(readiness, dict)
        or not isinstance(readiness.get("document"), str)
        or not isinstance(readiness.get("exact_state"), str)
        or not readiness.get("exact_state")
    ):
        errors.append("required_readiness is malformed")

    frozen_packets = data.get("frozen_packets")
    if not isinstance(frozen_packets, list) or not frozen_packets:
        errors.append("frozen_packets must be a nonempty list")
    else:
        for position, packet in enumerate(frozen_packets, 1):
            if (
                not isinstance(packet, dict)
                or not isinstance(packet.get("path"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", str(packet.get("sha256", "")))
            ):
                errors.append("frozen packet row %d is malformed" % position)

    for collection in (
        "complete_claim_surfaces",
        "fixture_mutation_cases",
        "source_record_mutation_cases",
        "bibliography_mutation_cases",
    ):
        value = data.get(collection)
        if not isinstance(value, list) or not value:
            errors.append("%s must be a nonempty list" % collection)
    complete_surfaces = data.get("complete_claim_surfaces")
    if isinstance(complete_surfaces, list):
        if any(not isinstance(value, str) or not value for value in complete_surfaces):
            errors.append("complete_claim_surfaces must contain paths")
        if _duplicates(complete_surfaces):
            errors.append("duplicate complete claim surfaces: %s" % _duplicates(complete_surfaces))
    return errors


def validate_mutation_controls(data: dict, root: Path = ROOT) -> list[str]:
    """Prove tracked malformed, duplicate, and provenance mutations are rejected."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["mutation controls require a fixture mapping"]
    for collection in ("rules", "invalid_cases", "valid_controls"):
        if not isinstance(data.get(collection), list) or not data[collection]:
            return ["mutation controls require nonempty %s" % collection]
    fixture_errors = validate_fixture_document(data)
    if fixture_errors:
        return ["mutation controls require a valid fixture document: %s" % fixture_errors]

    fixture_cases = data.get("fixture_mutation_cases")
    if not isinstance(fixture_cases, list) or not fixture_cases:
        return ["fixture_mutation_cases must be a nonempty list"]
    for case in fixture_cases:
        label = str(case.get("id"))
        target = case.get("target")
        operation = case.get("operation")
        diagnostic = str(case.get("expected_diagnostic"))
        mutation = copy.deepcopy(data)
        if target not in (
            "rules", "invalid_cases", "valid_controls", "required_source_rows",
            "required_live_claims",
        ):
            errors.append("%s names an unknown fixture mutation target" % label)
            continue
        if operation == "empty_collection":
            mutation[target] = []
        elif operation == "duplicate_first":
            mutation[target].append(copy.deepcopy(mutation[target][0]))
        elif operation == "remove_first_field" and mutation[target]:
            mutation[target][0].pop(case.get("field"), None)
        elif operation == "set_first_field" and mutation[target]:
            mutation[target][0][case.get("field")] = case.get("value")
        else:
            errors.append("%s names an unknown fixture mutation operation" % label)
            continue
        actual = validate_fixture_document(mutation)
        if not any(diagnostic in item for item in actual):
            errors.append("%s was not rejected with %s" % (label, diagnostic))

    for label, mutation, diagnostic in (
        (
            "malformed fixture collection",
            {**copy.deepcopy(data), "valid_controls": {}},
            "must be lists",
        ),
        (
            "unknown failure code",
            copy.deepcopy(data),
            "unknown failures",
        ),
        (
            "missing rule failure code",
            copy.deepcopy(data),
            "string failure_code",
        ),
    ):
        if label == "unknown failure code":
            mutation["invalid_cases"][0]["expected_failure_codes"] = ["E_UNKNOWN"]
        elif label == "missing rule failure code":
            del mutation["rules"][0]["failure_code"]
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

    source_path = root / "references" / "source-status.yaml"
    bib_path = root / "references" / "orthemology.bib"
    try:
        registry = yaml.safe_load(source_path.read_text(encoding="utf-8"))
        bib = bib_path.read_text(encoding="utf-8")
    except Exception as exc:
        return errors + ["mutation controls could not load source owners: %s" % exc]
    base_errors = validate_source_records_data(registry, bib, data)
    if base_errors:
        return errors + ["source mutation valid control failed: %s" % base_errors]

    source_cases = data.get("source_record_mutation_cases")
    if not isinstance(source_cases, list) or not source_cases:
        errors.append("source_record_mutation_cases must be a nonempty list")
    else:
        for case in source_cases:
            label = str(case.get("id"))
            mutation = copy.deepcopy(registry)
            rows = mutation.get("claims", [])
            matching = [row for row in rows if row.get("id") == case.get("row_id")]
            operation = case.get("operation")
            if operation == "malform_family":
                mutation["covered_claim_families"]["terminology_provenance"] = []
            elif operation == "remove" and matching:
                rows.remove(matching[0])
            elif operation == "duplicate" and matching:
                rows.append(copy.deepcopy(matching[0]))
            elif isinstance(case.get("set_fields"), dict) and matching:
                matching[0].update(case["set_fields"])
            else:
                errors.append("%s could not apply its source mutation" % label)
                continue
            actual = validate_source_records_data(mutation, bib, data)
            for diagnostic in case.get("expected_diagnostics", []):
                if not any(str(diagnostic) in item for item in actual):
                    errors.append("%s lacked diagnostic %s" % (label, diagnostic))

    entries, parse_errors = parse_bibtex(bib)
    if parse_errors:
        errors.append("bibliography mutation valid control failed: %s" % parse_errors)
    bib_cases = data.get("bibliography_mutation_cases")
    if not isinstance(bib_cases, list) or not bib_cases:
        errors.append("bibliography_mutation_cases must be a nonempty list")
    elif not parse_errors:
        for case in bib_cases:
            label = str(case.get("id"))
            matching = [entry for entry in entries if entry["key"] == case.get("bibliography_key")]
            if len(matching) != 1:
                errors.append("%s could not identify one bibliography entry" % label)
                continue
            entry = matching[0]
            operation = case.get("operation")
            if operation == "remove_entry_close":
                mutation = bib[:entry["end"] - 1] + bib[entry["end"]:]
            elif operation == "remove":
                mutation = bib[:entry["start"]] + bib[entry["end"]:]
            elif operation == "duplicate":
                mutation = bib + "\n" + entry["raw"] + "\n"
            else:
                errors.append("%s names an unknown bibliography mutation operation" % label)
                continue
            actual = validate_source_records_data(registry, mutation, data)
            diagnostic = str(case.get("expected_diagnostic"))
            if not any(diagnostic in item for item in actual):
                errors.append("%s lacked diagnostic %s" % (label, diagnostic))
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
    for document in data.get("complete_claim_surfaces", []):
        path = root / document
        if not path.exists():
            errors.append("%s complete claim surface is missing" % document)
            continue
        unsafe = claim_failures(path.read_text(encoding="utf-8"))
        if unsafe:
            errors.append("%s complete claim surface has unsafe claims: %s" % (
                document, sorted(unsafe)))
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
        ready_tokens = re.findall(r"\bREADY_[A-Z_]+\b", text)
        contradictory = sorted(set(token for token in ready_tokens if token != exact))
        if contradictory:
            errors.append("readiness owner has contradictory readiness states: %s" % contradictory)
        if re.search(r"\bREADY(?: TO |-)RUN\b", text):
            errors.append("readiness owner retains contradictory READY TO RUN wording")
    for packet in data.get("frozen_packets", []):
        actual = _packet_digest(root / packet["path"])
        if actual != packet["sha256"]:
            errors.append("%s packet hash drift: %s" % (packet["path"], actual))
    return errors


def validate_source_records_data(registry: object, bib: str, data: dict) -> list[str]:
    errors: list[str] = []
    claims = registry.get("claims") if isinstance(registry, dict) else None
    if not isinstance(claims, list):
        return ["source-status claims must be a list"]
    if any(not isinstance(row, dict) for row in claims):
        return ["source-status claim rows must be mappings"]
    ids = [row.get("id") for row in claims]
    if any(not isinstance(row_id, str) or not row_id for row_id in ids) or _duplicates(ids):
        errors.append("source-status rows must have unique ids")
    families = registry.get("covered_claim_families")
    if not isinstance(families, dict):
        errors.append("covered_claim_families must be a mapping")
    else:
        terminology_family = families.get("terminology_provenance")
        if not isinstance(terminology_family, dict):
            errors.append("terminology_provenance family must be a mapping")
        elif terminology_family.get("prefix") != "ETY":
            errors.append("terminology_provenance family with ETY prefix is missing")
    entries, bib_errors = parse_bibtex(bib)
    errors.extend(bib_errors)
    bib_keys = [entry["key"] for entry in entries]
    for required in data.get("required_source_rows", []):
        row_id = required["id"]
        key = required["bibliography_key"]
        matching = [row for row in claims if row.get("id") == row_id]
        if len(matching) != 1:
            errors.append("%s must occur exactly once in source status" % row_id)
        else:
            row = matching[0]
            if row.get("claim") != required.get("claim"):
                errors.append("%s claim differs from its required provenance role" % row_id)
            for fixture_field, source_field in (
                ("claim_level", "claim_level"),
                ("source_type", "source_type"),
                ("status", "status"),
            ):
                if row.get(source_field) != required.get(fixture_field):
                    errors.append("%s %s differs from its required provenance role" % (
                        row_id, fixture_field))
            if row.get("support") != required.get("direct_support"):
                errors.append("%s direct support differs from its required provenance role" % row_id)
            if row.get("locus_exact") != required.get("locator"):
                errors.append("%s locator differs from its required provenance role" % row_id)
            notes = normalize(str(row.get("notes", "")))
            if row.get("notes") != required.get("exclusion_statement"):
                errors.append("%s exclusions differ from the required provenance boundary" % row_id)
            missing_exclusions = [
                exclusion for exclusion in required.get("exclusions", [])
                if normalize(str(exclusion)) not in notes
            ]
            if missing_exclusions:
                errors.append("%s exclusions are missing: %s" % (
                    row_id, missing_exclusions))
            if row.get("bibliography_key") != key:
                errors.append("%s bibliography association must be %s" % (row_id, key))
        if bib_keys.count(key) != 1:
            errors.append("%s must occur exactly once in bibliography" % key)
            continue
        entry = next(entry for entry in entries if entry["key"] == key)
        identifier = required.get("identifier") or {}
        identifier_field = str(identifier.get("field", "")).casefold()
        expected_identifier = str(identifier.get("value", ""))
        actual_identifier = _bibtex_scalar(entry["fields"].get(identifier_field, ""))
        if actual_identifier != expected_identifier:
            errors.append("%s bibliography identifier %s differs from %s" % (
                key, identifier_field, expected_identifier))
        if identifier_field == "doi" and len(matching) == 1:
            if str(matching[0].get("doi", "")) != expected_identifier:
                errors.append("%s source-status identifier differs from its bibliography DOI" % row_id)
    return errors


def validate_source_records(root: Path, data: dict) -> list[str]:
    source_path = root / "references" / "source-status.yaml"
    bib_path = root / "references" / "orthemology.bib"
    try:
        registry = yaml.safe_load(source_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return ["source-status YAML parse failed: %s" % exc]
    try:
        bib = bib_path.read_text(encoding="utf-8")
    except Exception as exc:
        return ["bibliography read failed: %s" % exc]
    return validate_source_records_data(registry, bib, data)


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
    fixture_errors = validate_fixture_document(data)
    failures += _print_result("fixture structure and semantic cases", fixture_errors)
    if fixture_errors:
        print("[FAIL] dependent checks — skipped because the fixture document is invalid")
        failures += 1
        print("TOTAL: %d failures" % failures)
        return 1
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
