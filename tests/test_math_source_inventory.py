#!/usr/bin/env python3
"""Focused tests for locus-sensitive publication inline-code classification."""
import copy
import importlib.util
import pathlib
import unittest
import unicodedata

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_math_source_inventory", ROOT / "scripts" / "validate_math_source.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

APPROVED_DIAGNOSTIC_PATH = "theory/orthemic-core-formalization.md"
APPROVED_DIAGNOSTIC_LOCUS = {"line": 477, "column": 38}
APPROVED_DIAGNOSTIC_OCCURRENCE = 13
APPROVED_DIAGNOSTIC_TEXT = (
    "μ̄_2: stale calibration; μ̄_3: wrong\n  claim scope"
)


def inventory_issues(inventory, source_texts, registry_ids=()):
    """Call the production inventory contract once it exists."""
    validate = getattr(VALIDATOR, "validate_inventory_data", None)
    return (
        []
        if validate is None
        else validate(inventory, source_texts, registry_ids=set(registry_ids))
    )


def migration_issues(migration, inventory):
    validate = getattr(VALIDATOR, "validate_migration_data", None)
    return [] if validate is None else validate(migration, inventory)


def gallery_issues(gallery_text, render_map):
    validate = getattr(VALIDATOR, "validate_gallery_data", None)
    return [] if validate is None else validate(gallery_text, render_map)


def build_source_issues(build_sources, declared_sources):
    validate = getattr(VALIDATOR, "validate_build_source_parity", None)
    return (
        []
        if validate is None
        else validate(set(build_sources), set(declared_sources))
    )


def extract_occurrences(source):
    return VALIDATOR.extract_inline_code_occurrences(source)


def literal_inventory(path, source):
    """Build an exact minimal literal-code inventory from *source*."""
    extracted = extract_occurrences(source)
    rows = [
        {
            "file": path,
            "locus": copy.deepcopy(occurrence["locus"]),
            "occurrence": occurrence["occurrence"],
            "text": occurrence["text"],
            "classification": "literal-code",
        }
        for occurrence in extracted
    ]
    return {
        "schema": "orthemology-math-source-inventory-v2",
        "classes": ["literal-code", "semantic-registry-id", "mathematics"],
        "sources": [
            {
                "file": path,
                "occurrence_count": len(rows),
                "classification_counts": {
                    "literal-code": len(rows),
                    "semantic-registry-id": 0,
                    "mathematics": 0,
                },
            }
        ],
        "occurrences": rows,
    }, {path: source}


def diagnostic_inventory(
    status=APPROVED_DIAGNOSTIC_TEXT,
    path=APPROVED_DIAGNOSTIC_PATH,
    copied_status=None,
):
    """Build a source whose diagnostic has the exact reviewed locus/ordinal."""
    lines = ["`token_%d`" % index for index in range(1, 13)]
    lines.extend([""] * (476 - len(lines)))
    lines.append(" " * 37 + "`%s`" % status)
    if copied_status is not None:
        lines.append(" " * 37 + "`%s`" % copied_status)
    return literal_inventory(path, "\n".join(lines))


def valid_inventory():
    source = "A classified occurrence: `V1(e)`.\n"
    inventory = {
        "schema": "orthemology-math-source-inventory-v2",
        "classes": ["literal-code", "semantic-registry-id", "mathematics"],
        "sources": [
            {
                "file": "publication/example.md",
                "occurrence_count": 1,
                "classification_counts": {
                    "literal-code": 0,
                    "semantic-registry-id": 0,
                    "mathematics": 1,
                },
            }
        ],
        "occurrences": [
            {
                "file": "publication/example.md",
                "locus": {"line": 1, "column": 26},
                "occurrence": 1,
                "text": "V1(e)",
                "classification": "mathematics",
            }
        ],
    }
    return inventory, {"publication/example.md": source}


class OccurrenceIdentityTests(unittest.TestCase):
    def assertIssue(self, issues, fragment):
        self.assertTrue(any(fragment in issue for issue in issues), issues)

    def assertLiteralControl(self, span):
        self.assertFalse(VALIDATOR._formula_like(span), span)
        source = "Literal: `%s`.\n" % span
        inventory, source_texts = literal_inventory(
            "publication/example.md",
            source,
        )
        self.assertEqual(inventory_issues(inventory, source_texts), [])

    def assertFormulaControl(self, span):
        self.assertTrue(VALIDATOR._formula_like(span), span)
        source = "Formula: `%s`.\n" % span
        inventory, source_texts = literal_inventory(
            "publication/example.md",
            source,
        )
        self.assertIssue(
            inventory_issues(inventory, source_texts),
            "formula-like literal classification",
        )

    def test_rejects_duplicate_file_locus_occurrence_key(self):
        inventory, source_texts = valid_inventory()
        inventory["occurrences"].append(copy.deepcopy(inventory["occurrences"][0]))

        issues = inventory_issues(inventory, source_texts)

        self.assertIssue(issues, "duplicate occurrence key")

    def test_rejects_new_and_copied_occurrences(self):
        inventory, source_texts = valid_inventory()
        for addition in ("Another formula: `x = y`.\n", "Copy: `V1(e)`.\n"):
            with self.subTest(addition=addition):
                mutated = dict(source_texts)
                mutated["publication/example.md"] += addition
                self.assertIssue(
                    inventory_issues(inventory, mutated),
                    "unclassified source occurrence",
                )

    def test_rejects_moved_occurrence_and_orphan_row(self):
        inventory, source_texts = valid_inventory()
        source_texts["publication/example.md"] = (
            "A preceding line moves the classified occurrence.\n"
            + source_texts["publication/example.md"]
        )

        issues = inventory_issues(inventory, source_texts)

        self.assertIssue(issues, "unclassified source occurrence")
        self.assertIssue(issues, "orphan inventory row")

    def test_rejects_missing_row_and_orphan_row(self):
        inventory, source_texts = valid_inventory()
        missing = copy.deepcopy(inventory)
        missing["occurrences"].clear()
        orphan = copy.deepcopy(inventory)
        orphan["occurrences"][0]["locus"]["column"] += 1

        self.assertIssue(
            inventory_issues(missing, source_texts), "unclassified source occurrence"
        )
        self.assertIssue(
            inventory_issues(orphan, source_texts), "orphan inventory row"
        )

    def test_multiline_single_backtick_span_has_exact_source_identity(self):
        source = "Formula: `x = y\n+ z`; then `V1`.\n"
        occurrences = extract_occurrences(source)

        self.assertEqual(
            occurrences,
            [
                {
                    "locus": {"line": 1, "column": 10},
                    "occurrence": 1,
                    "text": "x = y\n+ z",
                },
                {
                    "locus": {"line": 2, "column": 12},
                    "occurrence": 2,
                    "text": "V1",
                },
            ],
        )

    def test_multiline_span_copy_move_and_orphan_are_rejected(self):
        source = "Formula: `x = y\n+ z`.\n"
        inventory = {
            "schema": "orthemology-math-source-inventory-v2",
            "classes": ["literal-code", "semantic-registry-id", "mathematics"],
            "sources": [
                {
                    "file": "publication/example.md",
                    "occurrence_count": 1,
                    "classification_counts": {
                        "literal-code": 0,
                        "semantic-registry-id": 0,
                        "mathematics": 1,
                    },
                }
            ],
            "occurrences": [
                {
                    "file": "publication/example.md",
                    "locus": {"line": 1, "column": 10},
                    "occurrence": 1,
                    "text": "x = y\n+ z",
                    "classification": "mathematics",
                }
            ],
        }
        self.assertEqual(
            inventory_issues(inventory, {"publication/example.md": source}),
            [],
        )

        copied = {"publication/example.md": source + source}
        self.assertIssue(
            inventory_issues(inventory, copied),
            "unclassified source occurrence",
        )

        moved = {"publication/example.md": "Prefix.\n" + source}
        moved_issues = inventory_issues(inventory, moved)
        self.assertIssue(moved_issues, "unclassified source occurrence")
        self.assertIssue(moved_issues, "orphan inventory row")

        orphan = copy.deepcopy(inventory)
        orphan["occurrences"][0]["locus"]["column"] += 1
        self.assertIssue(
            inventory_issues(orphan, {"publication/example.md": source}),
            "orphan inventory row",
        )

    def test_multiline_scanner_masks_fences_and_rejects_unclosed_delimiter(self):
        source = (
            "```text\n"
            "not an occurrence: `x = y\n"
            "+ z`\n"
            "```\n"
            "Real: `a = b\n"
            "+ c`.\n"
        )
        occurrences = extract_occurrences(source)
        self.assertEqual(len(occurrences), 1)
        self.assertEqual(occurrences[0]["text"], "a = b\n+ c")

        inventory, source_texts = valid_inventory()
        source_texts["publication/example.md"] = "Unclosed `x = y.\n"
        self.assertIssue(
            inventory_issues(inventory, source_texts),
            "malformed single-backtick delimiter",
        )

    def test_commonmark_fence_masking_preserves_loci_for_tildes_and_long_runs(self):
        source = (
            "~~~text\n"
            "hidden: `x = y`\n"
            "~~~\n"
            "````text\n"
            "hidden: `f(x)`\n"
            "```\n"
            "still hidden: `p → q`\n"
            "`````\n"
            "~~~~text\n"
            "hidden: `x ∈ S`\n"
            "~~~\n"
            "still hidden: `a = b`\n"
            "~~~~\n"
            "Real: `V1`.\n"
        )

        self.assertEqual(
            extract_occurrences(source),
            [
                {
                    "locus": {"line": 14, "column": 7},
                    "occurrence": 1,
                    "text": "V1",
                }
            ],
        )
        self.assertEqual(
            extract_occurrences("~~~text\nhidden: `x = y`\n"),
            [],
        )

    def test_rejects_formula_as_registry_id_including_bare_operator_call(self):
        inventory, source_texts = valid_inventory()
        inventory["occurrences"][0]["classification"] = "semantic-registry-id"
        inventory["sources"][0]["classification_counts"] = {
            "literal-code": 0,
            "semantic-registry-id": 1,
            "mathematics": 0,
        }

        issues = inventory_issues(inventory, source_texts, registry_ids={"V1"})

        self.assertIssue(issues, "formula-like registry classification")

    def test_rejects_combining_accent_as_nonmathematics(self):
        inventory, source_texts = valid_inventory()
        accented = unicodedata.normalize("NFD", "x̂")
        source_texts["publication/example.md"] = f"Accent: `{accented}`.\n"
        inventory["occurrences"][0].update(
            {
                "locus": {"line": 1, "column": 9},
                "text": accented,
                "classification": "literal-code",
            }
        )
        inventory["sources"][0]["classification_counts"] = {
            "literal-code": 1,
            "semantic-registry-id": 0,
            "mathematics": 0,
        }

        self.assertIssue(
            inventory_issues(inventory, source_texts),
            "combining accent classified as nonmathematics",
        )

    def test_approved_multiline_token_status_example_remains_literal_code(self):
        inventory, source_texts = diagnostic_inventory()
        self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_diagnostic_literal_requires_exact_inventory_identity_and_text(self):
        occurrence_key = (
            APPROVED_DIAGNOSTIC_PATH,
            APPROVED_DIAGNOSTIC_LOCUS["line"],
            APPROVED_DIAGNOSTIC_LOCUS["column"],
            APPROVED_DIAGNOSTIC_OCCURRENCE,
        )
        generic_statuses = (
            "μ̄_2: stale calibration; μ̄_3: wrong\nclaim scope",
            "μ̄_17: stale calibration; μ̄_204: wrong\nclaim scope",
            "token_17: stale calibration; agent_4: wrong\nclaim scope",
        )
        rejected = (
            "V1(e): stale calibration; token_3: wrong\nclaim scope",
            "RelSpec_q(e): stale calibration; token_3: wrong\nclaim scope",
            "x∈S: stale calibration; token_3: wrong\nclaim scope",
            "x=y: stale calibration; token_3: wrong\nclaim scope",
            "p→q: stale calibration; token_3: wrong\nclaim scope",
            "{x|P(x)}: stale calibration; token_3: wrong\nclaim scope",
            "x̂: stale calibration; token_3: wrong\nclaim scope",
            "μ⃗: stale calibration; token_3: wrong\nclaim scope",
            "x̄_2: stale calibration; token_3: wrong\nclaim scope",
            "μ̂_2: stale calibration; token_3: wrong\nclaim scope",
            "μ⃗_2: stale calibration; token_3: wrong\nclaim scope",
            "q̄_17: stale calibration; token_3: wrong\nclaim scope",
            "μ̄₂: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_₂: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_x: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_2a: stale calibration; token_3: wrong\nclaim scope",
            "V₁: stale calibration; token_3: wrong\nclaim scope",
            "x₂: stale calibration; token_3: wrong\nclaim scope",
            "x²: stale calibration; token_3: wrong\nclaim scope",
            "xᵢ: stale calibration; token_3: wrong\nclaim scope",
            "xⁿ: stale calibration; token_3: wrong\nclaim scope",
            "xₐ: stale calibration; token_3: wrong\nclaim scope",
            "𝑥: stale calibration; token_3: wrong\nclaim scope",
            "𝐕1: stale calibration; token_3: wrong\nclaim scope",
            "Ｖ1: stale calibration; token_3: wrong\nclaim scope",
            "V１: stale calibration; token_3: wrong\nclaim scope",
            "Ⓥ1: stale calibration; token_3: wrong\nclaim scope",
            "Ⅴ1: stale calibration; token_3: wrong\nclaim scope",
            "α_2: stale calibration; token_3: wrong\nclaim scope",
            "é_2: stale calibration; token_3: wrong\nclaim scope",
            "+: stale calibration; token_3: wrong\nclaim scope",
            "/: stale calibration; token_3: wrong\nclaim scope",
            "⋅: stale calibration; token_3: wrong\nclaim scope",
            "−: stale calibration; token_3: wrong\nclaim scope",
            "·: stale calibration; token_3: wrong\nclaim scope",
            "^: stale calibration; token_3: wrong\nclaim scope",
            "≈: stale calibration; token_3: wrong\nclaim scope",
            "≃: stale calibration; token_3: wrong\nclaim scope",
        )

        self.assertTrue(
            VALIDATOR.is_approved_diagnostic_literal(
                occurrence_key,
                APPROVED_DIAGNOSTIC_TEXT,
            )
        )
        for status in generic_statuses:
            with self.subTest(status=status):
                self.assertFalse(
                    VALIDATOR.is_approved_diagnostic_literal(
                        occurrence_key,
                        status,
                    ),
                    status,
                )
        for status in rejected:
            with self.subTest(status=status):
                self.assertFalse(
                    VALIDATOR.is_approved_diagnostic_literal(
                        occurrence_key,
                        status,
                    ),
                    status,
                )

    def test_only_exact_approved_diagnostic_occurrence_is_exempt(self):
        self.assertTrue(VALIDATOR._formula_like(APPROVED_DIAGNOSTIC_TEXT))
        inventory, source_texts = diagnostic_inventory()
        self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_nonformula_status_near_misses_remain_literal_code(self):
        malformed = (
            ": pass;\nagent_2: fail",
            "agent_1: pass;\n: fail",
            "pass;\nagent_2: fail",
            "agent_1: pass;\nfail",
            "agent_1: pass;\nagent_2: fail;",
            "agent_1: pass;;\nagent_2: fail",
            "agent 1: pass;\nagent_2: fail",
            "agent_1 : pass;\nagent_2: fail",
            "agent_1:: pass;\nagent_2: fail",
            "agent_1: PASS;\nagent_2: FAIL!",
            "PASS;\nFAIL",
        )
        for status in malformed:
            with self.subTest(status=status):
                self.assertFalse(VALIDATOR._formula_like(status), status)
                inventory, source_texts = diagnostic_inventory(
                    status=status,
                    path="publication/example.md",
                )
                self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_nonformula_missing_separator_status_remains_literal_code(self):
        status = "agent_1: pass\nagent_2: fail"
        self.assertFalse(VALIDATOR._formula_like(status), status)
        inventory, source_texts = diagnostic_inventory(
            status=status,
            path="publication/example.md",
        )
        self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_nonformula_missing_colon_statuses_remain_literal_code(self):
        malformed = (
            "agent_1 pass;\nagent_2 fail",
            "agent_1: pass\nagent_2 fail",
        )
        for status in malformed:
            with self.subTest(status=status):
                self.assertFalse(VALIDATOR._formula_like(status), status)
                inventory, source_texts = diagnostic_inventory(
                    status=status,
                    path="publication/example.md",
                )
                self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_formula_bearing_approved_diagnostic_mutations_are_rejected(self):
        mutated = (
            "μ̄_3: wrong\n  claim scope; μ̄_2: stale calibration",
            "μ̄_2: stale calibration; μ̄_2: wrong\n  claim scope",
            "μ̄_2: fresh calibration; μ̄_3: wrong\n  claim scope",
            "μ̄_2: stale calibration; μ̄_3: incorrect\n  claim scope",
            "μ̄_2: stale calibration ; μ̄_3: wrong\n  claim scope",
            "μ̄_2: stale calibration; μ̄_3: wrong\n claim scope",
        )
        for status in mutated:
            with self.subTest(status=status):
                self.assertTrue(VALIDATOR._formula_like(status), status)
                inventory, source_texts = diagnostic_inventory(status=status)
                self.assertIssue(
                    inventory_issues(inventory, source_texts),
                    "formula-like literal classification",
                )

    def test_approved_diagnostic_cannot_be_moved(self):
        moved_inventory, moved_sources = diagnostic_inventory(
            path="publication/example.md",
        )
        self.assertIssue(
            inventory_issues(moved_inventory, moved_sources),
            "formula-like literal classification",
        )

    def test_approved_diagnostic_cannot_be_copied(self):
        copied_inventory, copied_sources = diagnostic_inventory(
            copied_status=APPROVED_DIAGNOSTIC_TEXT,
        )
        copied_issues = inventory_issues(copied_inventory, copied_sources)
        self.assertEqual(
            sum(
                "formula-like literal classification" in issue
                for issue in copied_issues
            ),
            1,
            copied_issues,
        )

    def test_unrelated_multiline_literal_code_remains_valid(self):
        controls = (
            "printf first;\nprintf second",
            "first: value\nsecond: value",
            "line one\nline two",
        )
        for control in controls:
            with self.subTest(control=control):
                source = "Control: `%s`.\n" % control
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_status_punctuation_does_not_make_unrelated_multiline_code_diagnostic(self):
        controls = (
            "color: red;\nbackground: blue;",
            "if ready:\n  break; continue",
            "owner: editor;\nnotes continue here",
            "heading:\nplain text; continuation",
            "owner: editor;\nreviewers:\n  - alice\n  - bob",
            "endpoint: https://example.test/a;\nretry: disabled",
            "started: 12:30;\nended: 13:45",
            "Note: preserve the first clause;\ncontinue with the second sentence.",
            "items:\n  alpha; beta\nnotes: retained",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertFalse(VALIDATOR._formula_like(control), control)
                source = "Control: `%s`.\n" % control
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_inventory_corpus_has_one_reviewed_multiline_literal(self):
        inventory = yaml.safe_load(
            (ROOT / "docs" / "math-source-inventory.yaml").read_text(
                encoding="utf-8"
            )
        )
        multiline_literals = [
            {
                "file": row.get("file"),
                "locus": row.get("locus"),
                "occurrence": row.get("occurrence"),
                "text": row.get("text"),
            }
            for row in inventory["occurrences"]
            if row.get("classification") == "literal-code"
            and isinstance(row.get("text"), str)
            and "\n" in row["text"]
        ]
        self.assertEqual(
            multiline_literals,
            [
                {
                    "file": APPROVED_DIAGNOSTIC_PATH,
                    "locus": APPROVED_DIAGNOSTIC_LOCUS,
                    "occurrence": APPROVED_DIAGNOSTIC_OCCURRENCE,
                    "text": APPROVED_DIAGNOSTIC_TEXT,
                }
            ],
        )

    def test_formula_bearing_literals_are_classified_independently_of_status_shape(self):
        formula_statuses = (
            "V1(e): stale calibration; token_3: wrong\nclaim scope",
            "RelSpec_q(e): stale calibration; token_3: wrong\nclaim scope",
            "x+y: PASS;\nagent_2: FAIL!",
            "x/y — pass?\nagent_2 says FAIL.",
            "x⋅y: status unknown\nplain continuation",
            "x·y, status unknown\nplain continuation",
            "x-y: status unknown\nplain continuation",
            "x−y: status unknown\nplain continuation",
            "x^y, status unknown\nplain continuation",
            "x<y: status unknown\nplain continuation",
            "x>y, status unknown\nplain continuation",
            "x≈y: status unknown\nplain continuation",
            "x≃y, status unknown\nplain continuation",
            "x∈S: stale calibration; token_3: wrong\nclaim scope",
            "x=y: stale calibration; token_3: wrong\nclaim scope",
            "p→q: stale calibration; token_3: wrong\nclaim scope",
            "x̂: stale calibration; token_3: wrong\nclaim scope",
            "μ⃗: stale calibration; token_3: wrong\nclaim scope",
            "x̄_2: stale calibration; token_3: wrong\nclaim scope",
            "μ̂_2: stale calibration; token_3: wrong\nclaim scope",
            "μ⃗_2: stale calibration; token_3: wrong\nclaim scope",
            "q̄_17: stale calibration; token_3: wrong\nclaim scope",
            "μ̄₂: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_₂: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_x: stale calibration; token_3: wrong\nclaim scope",
            "μ̄_2a: stale calibration; token_3: wrong\nclaim scope",
            "V₁: stale calibration; token_3: wrong\nclaim scope",
            "x₂: stale calibration; token_3: wrong\nclaim scope",
            "x²: stale calibration; token_3: wrong\nclaim scope",
            "xᵢ: stale calibration; token_3: wrong\nclaim scope",
            "xⁿ: stale calibration; token_3: wrong\nclaim scope",
            "xₐ: stale calibration; token_3: wrong\nclaim scope",
            "𝑥: stale calibration; token_3: wrong\nclaim scope",
            "𝐕1: stale calibration; token_3: wrong\nclaim scope",
            "Ｖ1: stale calibration; token_3: wrong\nclaim scope",
            "V１: stale calibration; token_3: wrong\nclaim scope",
            "Ⓥ1: stale calibration; token_3: wrong\nclaim scope",
            "Ⅴ1: stale calibration; token_3: wrong\nclaim scope",
            "α_2: stale calibration; token_3: wrong\nclaim scope",
            "é_2: stale calibration; token_3: wrong\nclaim scope",
            "+: stale calibration; token_3: wrong\nclaim scope",
            "/: stale calibration; token_3: wrong\nclaim scope",
            "⋅: stale calibration; token_3: wrong\nclaim scope",
            "−: stale calibration; token_3: wrong\nclaim scope",
            "·: stale calibration; token_3: wrong\nclaim scope",
            "^: stale calibration; token_3: wrong\nclaim scope",
            "≈: stale calibration; token_3: wrong\nclaim scope",
            "≃: stale calibration; token_3: wrong\nclaim scope",
        )
        for status in formula_statuses:
            with self.subTest(status=status):
                self.assertTrue(VALIDATOR._formula_like(status), status)
                source = "Diagnostic: `%s`.\n" % status
                inventory = {
                    "schema": "orthemology-math-source-inventory-v2",
                    "classes": [
                        "literal-code",
                        "semantic-registry-id",
                        "mathematics",
                    ],
                    "sources": [
                        {
                            "file": "publication/example.md",
                            "occurrence_count": 1,
                            "classification_counts": {
                                "literal-code": 1,
                                "semantic-registry-id": 0,
                                "mathematics": 0,
                            },
                        }
                    ],
                    "occurrences": [
                        {
                            "file": "publication/example.md",
                            "locus": {"line": 1, "column": 13},
                            "occurrence": 1,
                            "text": status,
                            "classification": "literal-code",
                        }
                    ],
                }

                issues = inventory_issues(
                    inventory,
                    {"publication/example.md": source},
                )
                self.assertIssue(issues, "formula-like literal classification")

    def test_operator_and_binary_formulae_are_detected_directly(self):
        formulae = (
            "/",
            "⋅",
            "−",
            "·",
            "^",
            "≈",
            "≃",
            "x+y",
            "x/y",
            "x⋅y",
            "x·y",
            "x-y",
            "x−y",
            "x^y",
            "x<y",
            "x>y",
            "x≈y",
            "x≃y",
            "A-B",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertTrue(VALIDATOR._formula_like(formula), formula)

    def test_structural_formula_operands_cover_numbers_spacing_and_unicode(self):
        formulae = (
            "x^2",
            "x+2",
            "2+x",
            "x/2",
            "2/x",
            "x<2",
            "2>x",
            "x*y",
            "x + 2",
            "2 / x",
            "alpha / beta",
            "-2+x",
            "x+-2",
            "x + -2",
            "x + −2",
            "−2+x",
            "2.5*x",
            ".5 + x",
            "x / -3.25",
            "2.0/−.5",
            "φ + 2",
            "2×𝑥",
            "𝑥^2",
            "α≤3.5",
            "3.5≥β",
            "A∩B",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertTrue(
                    VALIDATOR._binary_formula_structure(formula),
                    formula,
                )
                self.assertTrue(VALIDATOR._formula_like(formula), formula)
                source = "Formula: `%s`.\n" % formula
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertIssue(
                    inventory_issues(inventory, source_texts),
                    "formula-like literal classification",
                )

    def test_callable_identifiers_cover_spacing_and_unicode(self):
        formulae = (
            "f (x)",
            "φ(x)",
            "𝑓 (x)",
            "RelSpec_q (e)",
            "V1(e)",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertFormulaControl(formula)

    def test_every_unicode_mark_category_is_formula_like(self):
        mark_codepoints = (
            0x20DD,
            0x0903,
            0xFE0F,
            0x05B0,
            0x064B,
            0x20E1,
        )
        observed_categories = set()
        for codepoint in mark_codepoints:
            mark = chr(codepoint)
            category = unicodedata.category(mark)
            observed_categories.add(category)
            with self.subTest(codepoint=hex(codepoint), category=category):
                self.assertTrue(category.startswith("M"), category)
                self.assertTrue(VALIDATOR._formula_like("x" + mark), hex(codepoint))
                source = "Mark: `x%s`.\n" % mark
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertIssue(
                    inventory_issues(inventory, source_texts),
                    "formula-like literal classification",
                )
        self.assertEqual(observed_categories, {"Mn", "Mc", "Me"})

    def test_syntactic_urls_are_removed_before_formula_heuristics(self):
        urls = (
            "https://example.test/search?x=1",
            "https://example.test/search?q=a+b",
            "https://example.test/search?q=a%2Bb",
            "https://example.test/path#x=1",
            "http://example.test/a/b?ratio=x%2Fy#section-2",
            "https://example.test/f(x)?q=φ(x)",
            "curl https://example.test/search?x=1&q=a+b#result",
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertFalse(VALIDATOR._formula_like(url), url)
                source = "Endpoint: `%s`.\n" % url
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertEqual(inventory_issues(inventory, source_texts), [])

    def test_formula_outside_a_url_remains_formula_like(self):
        spans = (
            "x=1 https://example.test/search?q=a+b",
            "https://example.test/search?q=a+b then x+2",
            "φ(x) at https://example.test/path#x=1",
        )
        for span in spans:
            with self.subTest(span=span):
                self.assertTrue(VALIDATOR._formula_like(span), span)
                source = "Mixed: `%s`.\n" % span
                inventory, source_texts = literal_inventory(
                    "publication/example.md",
                    source,
                )
                self.assertIssue(
                    inventory_issues(inventory, source_texts),
                    "formula-like literal classification",
                )

    def test_commands_paths_and_versions_remain_nonformula_controls(self):
        controls = (
            "python --version",
            "git show HEAD:path",
            "docs/notation-gallery.md",
            "docs/verdict-registry.yaml",
            "../docs/notation-gallery.md",
            "theislampill/orthemology",
            "applications/daee-epistemics/",
            "C:\\Python311",
            "orthemic-multi-actor-conflict-note.md",
            "SCAN-CLEAN",
            "v1.2.3",
            "Python 3.11.9",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertFalse(VALIDATOR._formula_like(control), control)

    def test_cli_commands_and_complete_flag_tokens_remain_literal(self):
        controls = (
            "pytest -q --disable-warnings",
            "pytest --maxfail=1",
            "python -m pytest -q",
            "validator --count=2 --verbose",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_cli_masking_preserves_formulae_after_complete_option_tokens(self):
        formulae = (
            "pytest -q then x+2",
            "validator --count=2 then φ(x)",
            "python -m pytest then 2.5*x",
            "validator --verbose then RelSpec_q (e)",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertFormulaControl(formula)

    def test_filenames_paths_and_archive_names_precede_callable_detection(self):
        controls = (
            "report(v1)" + ".md",
            "task-12-report" + ".md",
            "release(v2).tar" + ".gz",
            "notes(archived)" + ".txt",
            "artifact-v1.2.3" + ".zip",
            "docs/notation-gallery.md",
            "scripts/validate_math_source.py",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_semver_tokens_precede_operator_detection(self):
        controls = (
            "1.2.3-alpha+001",
            "v2.0.0-rc.1+build.7",
            "0.0.1",
            "10.20.30-beta.2",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_uppercase_status_ids_precede_binary_hyphen_detection(self):
        controls = (
            "TASK-12",
            "R7E-12",
            "TASK-12-REVIEW",
            "R7E-12A",
            "SCAN-CLEAN",
            "M-1",
            "E-T1-USED",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_non_status_single_letter_hyphens_remain_formulae(self):
        formulae = (
            "X-2",
            "Y-17",
            "A-B",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertFormulaControl(formula)

    def test_line_leading_asterisks_are_list_markers_not_multiplication(self):
        controls = (
            "*",
            "* item",
            "  * item",
            "items:\n  * first\n  * second",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_commonmark_unordered_list_markers_are_masked_line_by_line(self):
        controls = (
            "+",
            "-",
            "+ item",
            " + item",
            "  + item",
            "   + item",
            "- item",
            "  * item",
            "items:\n+ first\n  * second\n   - third",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

        formulae = (
            "x+y",
            "2.5*x",
            "+ x+y",
            "  * 2.5*x",
        )
        for formula in formulae:
            with self.subTest(formula=formula):
                self.assertFormulaControl(formula)

    def test_multiword_parenthetical_prose_is_not_a_callable(self):
        controls = (
            "plain prose (aside)",
            "release notes (draft)",
            "two words (context only)",
            "Plain Notes (Draft)",
            "release Notes (draft)",
            "Title (Draft)",
            "Release (Candidate)",
            "Title(Draft)",
            "Release(Candidate)",
        )
        for control in controls:
            with self.subTest(control=control):
                self.assertLiteralControl(control)

    def test_unicode_formula_style_keys_are_detected_without_diagnostic_context(self):
        formula_style_keys = (
            "V₁",
            "x₂",
            "x²",
            "xᵢ",
            "xⁿ",
            "xₐ",
            "𝑥",
            "𝐕1",
            "Ｖ1",
            "V１",
            "Ⓥ1",
            "Ⅴ1",
            "α_2",
            "é_2",
        )
        for key in formula_style_keys:
            with self.subTest(key=key):
                self.assertTrue(VALIDATOR._formula_like(key), key)

    def test_preserves_literal_command_and_true_registry_id(self):
        source = "Run `python --version`; inspect `V1`.\n"
        inventory = {
            "schema": "orthemology-math-source-inventory-v2",
            "classes": ["literal-code", "semantic-registry-id", "mathematics"],
            "sources": [
                {
                    "file": "publication/example.md",
                    "occurrence_count": 2,
                    "classification_counts": {
                        "literal-code": 1,
                        "semantic-registry-id": 1,
                        "mathematics": 0,
                    },
                }
            ],
            "occurrences": [
                {
                    "file": "publication/example.md",
                    "locus": {"line": 1, "column": 5},
                    "occurrence": 1,
                    "text": "python --version",
                    "classification": "literal-code",
                },
                {
                    "file": "publication/example.md",
                    "locus": {"line": 1, "column": 33},
                    "occurrence": 2,
                    "text": "V1",
                    "classification": "semantic-registry-id",
                },
            ],
        }

        self.assertEqual(
            inventory_issues(
                inventory,
                {"publication/example.md": source},
                registry_ids={"V1"},
            ),
            [],
        )

    def test_rejects_removed_publication_source(self):
        inventory, _source_texts = valid_inventory()

        self.assertIssue(
            inventory_issues(inventory, {}),
            "missing publication source",
        )

    def test_rejects_removed_gallery_symbol(self):
        render_map = [
            {"registry_symbol": "A", "latex": r"\mathcal{A}"},
            {"registry_symbol": "B", "latex": r"\mathcal{B}"},
        ]

        self.assertIssue(
            gallery_issues(r"Gallery contains $\mathcal{A}$.", render_map),
            "gallery missing registry symbol",
        )

    def test_rejects_removed_build_source(self):
        declared = {"publication/one.md", "publication/two.md"}

        self.assertIssue(
            build_source_issues({"publication/one.md"}, declared),
            "build source parity",
        )


class MigrationTruthTests(unittest.TestCase):
    def test_current_status_fails_split_migration_contract(self):
        inventory, _source_texts = valid_inventory()
        migration = {
            "schema": "orthemology-math-migration-status-v1",
            "documents": [
                {
                    "pdf": "example-artifact",
                    "sources": ["publication/example.md"],
                    "migrated": True,
                    "expected_notdef": 0,
                }
            ],
        }

        issues = migration_issues(migration, inventory)

        self.assertTrue(issues, "legacy migrated status must fail the v2 contract")

    def test_rejects_migrated_source_with_math_backtick_and_completed_visual_qa(self):
        inventory, _source_texts = valid_inventory()
        migration = {
            "schema": "orthemology-math-migration-status-v2",
            "documents": [
                {
                    "artifact_id": "example-artifact",
                    "sources": ["publication/example.md"],
                    "glyph_defect_repaired": True,
                    "full_math_source_migrated": True,
                    "expected_notdef": 0,
                    "visual_qa_state": "complete",
                }
            ],
        }

        issues = migration_issues(migration, inventory)

        self.assertTrue(
            any("full_math_source_migrated" in issue for issue in issues), issues
        )
        self.assertTrue(any("visual QA" in issue for issue in issues), issues)


if __name__ == "__main__":
    unittest.main()
