#!/usr/bin/env python3
"""Task 12 contracts for deterministic LaTeX source generation and migration."""

import importlib.util
import pathlib
import sys
import tempfile
import unittest
from collections import Counter

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from latex_to_typst_math import translate_display, translate_inline
from unicode_math_to_latex import convert


def load_generator():
    path = SCRIPTS / "generate_latex_sources.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("generate_latex_sources", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AthariSourceBatchTests(unittest.TestCase):
    def test_reviewed_orthable_expression_translates_and_is_migrated(self):
        latex = r"\operatorname{Orthable}(m; A)"
        self.assertEqual(
            translate_inline(latex),
            'op("Orthable")(m; A)',
        )
        source = (
            ROOT
            / "companion"
            / "orthability-divine-attributes-and-speech-athari.md"
        ).read_text(encoding="utf-8")
        self.assertIn("$%s$" % latex, source)
        self.assertNotIn("`Orthable(m; A)`", source)


REVIEWED_SOURCE_BATCHES = {
    "companion/orthability-and-the-ground-of-intelligibility.md": {
        "Orthable(m; A)": r"\operatorname{Orthable}(m; A)",
        "m": "m",
        "A": "A",
        "p̂": r"\hat p",
        "O*(m; A)": r"O^*(m; A)",
        "PlacementCorrect(p̂, m, A)": (
            r"\operatorname{PlacementCorrect}(\hat p, m, A)"
        ),
        "AdequateMetaType(μ_rep; A)": (
            r"\operatorname{AdequateMetaType}(\mu_{\mathrm{rep}}; A)"
        ),
        "PathwayAdequate(e)": r"\operatorname{PathwayAdequate}(e)",
        (
            "StrictlySoundReasoning_q(e) := ReasoningPathAdequate_q(e) "
            "∧ TOKEN_TRUTH_LINKED_q(e)"
        ): (
            r"\operatorname{StrictlySoundReasoning}_q(e) := "
            r"\operatorname{ReasoningPathAdequate}_q(e) \wedge "
            r"\operatorname{TokenTruthLinked}_q(e)"
        ),
        "ReasoningPathAdequate_q(e)": (
            r"\operatorname{ReasoningPathAdequate}_q(e)"
        ),
        "ReqReason_q(e) ⊆ ReqPath(e)": (
            r"\operatorname{ReqReason}_q(e) \subseteq "
            r"\operatorname{ReqPath}(e)"
        ),
        "q": "q",
        "Inst_A(m, o)": r"\operatorname{Inst}_A(m, o)",
        "F_O": "F_O",
        "F_M": "F_M",
        "RelSpec": r"\operatorname{RelSpec}",
    },
    "theory/orthemic-multi-actor-conflict-note.md": {
        "A_α": r"A_\alpha",
        "T_α = task(A_α)": (
            r"T_\alpha = \operatorname{task}(A_\alpha)"
        ),
        "Π_{A_α}": r"\Pi_{A_\alpha}",
        "A": "A",
        "α, β": r"\alpha, \beta",
        "O*(m; A_α)": r"O^*(m; A_\alpha)",
        "𝒢_{α,A_α} ⊆ Π_{A_α}": (
            r"\mathcal{G}_{\alpha,A_\alpha} \subseteq \Pi_{A_\alpha}"
        ),
        "GoalSchema(·)": r"\operatorname{GoalSchema}(\cdot)",
        "GoalSchema(α)": r"\operatorname{GoalSchema}(\alpha)",
        "GoalSchema(β)": r"\operatorname{GoalSchema}(\beta)",
        "𝒢_α ∩ 𝒢_β": r"\mathcal{G}_\alpha \cap \mathcal{G}_\beta",
    },
}


class ReviewedSmallSourceBatchTests(unittest.TestCase):
    def test_reviewed_unique_expressions_translate_and_are_migrated(self):
        for relative, expressions in REVIEWED_SOURCE_BATCHES.items():
            source = (ROOT / relative).read_text(encoding="utf-8")
            for original, latex in expressions.items():
                with self.subTest(source=relative, original=original):
                    translate_inline(latex)
                    self.assertNotIn("`%s`" % original, source)
                    self.assertIn("$%s$" % latex, source)


class MigrationLedgerTests(unittest.TestCase):
    def test_reviewed_occurrence_records_are_translatable_and_migrated(self):
        inventory = yaml.safe_load(
            (ROOT / "docs" / "math-source-inventory.yaml").read_text(
                encoding="utf-8"
            )
        )
        migration = inventory.get("migration", {})
        records = migration.get("records", [])
        self.assertTrue(records, "reviewed Task 12 migration records are missing")
        keys = [
            (
                record["file"],
                record["original_locus"]["line"],
                record["original_locus"]["column"],
                record["original_occurrence"],
            )
            for record in records
        ]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(
            migration.get("mathematics_occurrences_migrated"),
            len(records),
        )
        sources = {}
        expected_replacements = Counter()
        for record in records:
            relative = record["file"]
            sources.setdefault(
                relative,
                (ROOT / relative).read_text(encoding="utf-8"),
            )
            with self.subTest(source=relative, occurrence=record["original_occurrence"]):
                self.assertEqual(record.get("state"), "migrated")
                translate_inline(record["replacement"])
                expected_replacements[(relative, record["replacement"])] += 1
        for (relative, replacement), expected_count in expected_replacements.items():
            with self.subTest(source=relative, replacement=replacement):
                self.assertGreaterEqual(
                    sources[relative].count("$%s$" % replacement),
                    expected_count,
                )

    def test_reviewed_replacements_do_not_nest_math_style_commands(self):
        inventory = yaml.safe_load(
            (ROOT / "docs" / "math-source-inventory.yaml").read_text(
                encoding="utf-8"
            )
        )
        forbidden = (
            r"\operatorname{\operatorname{",
            r"\mathrm{\mathrm{",
            r"\mathcal{\mathcal{",
        )
        for record in inventory.get("migration", {}).get("records", []):
            for fragment in forbidden:
                with self.subTest(
                    source=record["file"],
                    occurrence=record["original_occurrence"],
                    fragment=fragment,
                ):
                    self.assertNotIn(fragment, record["replacement"])

    def test_apply_event_restriction_preserves_the_legacy_single_bar(self):
        inventory = yaml.safe_load(
            (ROOT / "docs" / "math-source-inventory.yaml").read_text(
                encoding="utf-8"
            )
        )
        records = [
            record
            for record in inventory.get("migration", {}).get("records", [])
            if record.get("original_text", "").startswith("ApplyEvent(")
        ]
        self.assertEqual(len(records), 1)
        record = records[0]
        legacy = "ApplyEvent(μ̄, e) = ⟨μ̄, Trace_e\\|_μ̄⟩"
        expected = (
            r"\operatorname{ApplyEvent}(\bar{\mu}, e) = "
            r"\langle\bar{\mu}, \operatorname{Trace}_e |_{\bar{\mu}}\rangle"
        )
        rejected = r"\operatorname{Trace}_e \|_"
        source = (
            ROOT / "theory" / "orthemic-core-formalization.md"
        ).read_text(encoding="utf-8")
        generated = (
            ROOT
            / "publication"
            / "latex"
            / "orthemic-core-reference-draft"
            / "main.tex"
        ).read_text(encoding="utf-8")

        translate_inline(expected)
        self.assertEqual(record["original_text"], legacy)
        self.assertEqual(record["replacement"], expected)
        self.assertEqual(source.count("$%s$" % expected), 1)
        self.assertEqual(generated.count(expected), 1)
        for surface in (record["replacement"], source, generated):
            self.assertNotIn(rejected, surface)

    def test_completed_inventory_and_migration_status_are_exact(self):
        inventory = yaml.safe_load(
            (ROOT / "docs" / "math-source-inventory.yaml").read_text(
                encoding="utf-8"
            )
        )
        migration = inventory["migration"]
        self.assertEqual(migration["authoritative_mathematics_occurrences"], 673)
        self.assertEqual(migration["preserved_literal_code_occurrences"], 113)
        self.assertEqual(
            migration["preserved_semantic_registry_id_occurrences"],
            94,
        )
        self.assertEqual(migration["mathematics_occurrences_migrated"], 673)
        self.assertEqual(migration["mathematics_occurrences_remaining"], 0)
        self.assertEqual(
            inventory["totals"],
            {
                "sources": 7,
                "occurrences": 207,
                "literal-code": 113,
                "semantic-registry-id": 94,
                "mathematics": 0,
            },
        )

        status = yaml.safe_load(
            (ROOT / "docs" / "math-migration-status.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(status["documents"])
        for document in status["documents"]:
            with self.subTest(artifact=document["artifact_id"]):
                self.assertIs(document["full_math_source_migrated"], True)
                self.assertEqual(document["expected_notdef"], 0)


MULTILINE_COVERAGE_MIGRATIONS = (
    (
        "prov(μ) = ⟨authority, warrant,\n  scope, ver(μ)⟩",
        (
            r"\operatorname{prov}(\mu) = \langle "
            r"\mathrm{authority}, \mathrm{warrant}, \mathrm{scope}, "
            r"\operatorname{ver}(\mu) \rangle"
        ),
        "inline",
    ),
    (
        (
            "RelSpec_q(e) = ⟨declared reference class; relevant case/risk stratum;\n"
            "  reliability metric; threshold or tolerance; perturbation or comparison\n"
            "  family where applicable; evaluation protocol; evidence used to\n"
            "  establish reliability; version and validity conditions⟩"
        ),
        (
            r"\operatorname{RelSpec}_q(e) = \langle "
            r"\text{declared reference class}; "
            r"\text{relevant case/risk stratum}; "
            r"\text{reliability metric}; \text{threshold or tolerance}; "
            r"\text{perturbation or comparison family where applicable}; "
            r"\text{evaluation protocol}; "
            r"\text{evidence used to establish reliability}; "
            r"\text{version and validity conditions} \rangle"
        ),
        "inline",
    ),
    (
        (
            "TokenAdequate(μ̄, e) ⟺ MetaInst(μ̄, μ) ∧ Compatible(μ̄, A(e)) ∧\n"
            "  Anchored(μ̄, κ(e), v(e)) ∧ ScopeCorrect(μ̄, 𝒬(e)) ∧ Current(μ̄, t(e)) ∧\n"
            "  Provenanced(μ̄) ∧ AuthorizedBinding(μ̄)"
        ),
        (
            r"\operatorname{TokenAdequate}(\bar{\mu}, e) "
            r"\Leftrightarrow \operatorname{MetaInst}(\bar{\mu}, \mu) "
            r"\wedge \operatorname{Compatible}(\bar{\mu}, A(e)) "
            r"\wedge \operatorname{Anchored}(\bar{\mu}, \kappa(e), v(e)) "
            r"\wedge \operatorname{ScopeCorrect}(\bar{\mu}, \mathcal{Q}(e)) "
            r"\wedge \operatorname{Current}(\bar{\mu}, t(e)) "
            r"\wedge \operatorname{Provenanced}(\bar{\mu}) "
            r"\wedge \operatorname{AuthorizedBinding}(\bar{\mu})"
        ),
        "inline",
    ),
    (
        (
            "PerturbSpec(e) = ⟨varied fields; invariant fields; generator or\n"
            "  enumeration; size or measure; tolerance⟩"
        ),
        (
            r"\operatorname{PerturbSpec}(e) = \langle "
            r"\text{varied fields}; \text{invariant fields}; "
            r"\text{generator or enumeration}; \text{size or measure}; "
            r"\text{tolerance} \rangle"
        ),
        "inline",
    ),
)


class MultilineCoverageMigrationTests(unittest.TestCase):
    def test_reviewed_formulas_translate_and_replace_multiline_code_spans(self):
        source = (
            ROOT / "theory" / "orthemic-core-formalization.md"
        ).read_text(encoding="utf-8")
        for original, replacement, form in MULTILINE_COVERAGE_MIGRATIONS:
            with self.subTest(original=original.splitlines()[0], form=form):
                if form == "display":
                    translate_display(replacement)
                    expected = "$$\n%s\n$$" % replacement
                else:
                    translate_inline(replacement)
                    expected = "$%s$" % replacement
                self.assertNotIn("`%s`" % original, source)
                self.assertIn(expected, source)


class MarkdownRenderingTests(unittest.TestCase):
    def test_math_and_literal_dollars_remain_distinct(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "# Sample title\n\n"
            "## Abstract\n\n"
            "Code `cost $5`, currency \\$7, and "
            "math $\\operatorname{Orthable}(m; A)$.\n"
        )

        rendered = generator.render_markdown(markdown, source_name="sample.md")

        self.assertIn(r"\texttt{cost \char36{}5}", rendered)
        self.assertIn(r"currency \$7", rendered)
        self.assertIn(r"$\operatorname{Orthable}(m; A)$", rendered)

    def test_table_link_and_multiline_aligned_math_are_rendered(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = r"""# Sample title

| Quantity | Meaning |
|---|---|
| $x$ | [profile $O^*(m; A)$](docs/publication-profile.yaml) |

$$
\begin{aligned}
x &\to y \\
y &\to z
\end{aligned}
$$
"""

        rendered = generator.render_markdown(markdown, source_name="sample.md")

        self.assertIn(r"\begin{tabular}", rendered)
        self.assertIn(r"$O^*(m; A)$", rendered)
        self.assertIn(
            r"\href{\detokenize{docs/publication-profile.yaml}}{",
            rendered,
        )
        self.assertIn(r"\begin{aligned}", rendered)
        self.assertIn(r"\[", rendered)

    def test_commonmark_multiline_code_span_is_preserved_as_literal_code(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "Diagnostic `token_2: stale calibration; "
            "token_3: wrong\nclaim scope` remains literal.\n"
        )

        rendered = generator.render_markdown(
            markdown,
            source_name="multiline-code.md",
        )

        self.assertIn(
            r"\texttt{token\_2: stale calibration; "
            r"token\_3: wrong claim scope}",
            rendered,
        )

    def test_removed_reference_comments_leave_no_trailing_whitespace(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = "- Citation. <!-- ref:citation-key -->\n"

        rendered = generator.render_markdown(
            markdown,
            source_name="reference-list.md",
        )

        self.assertIn("\\item Citation.\n", rendered)
        self.assertFalse(
            any(
                line.endswith((" ", "\t"))
                for line in rendered.splitlines()
            ),
            repr(rendered),
        )

    def test_malformed_math_raw_html_and_images_are_hard_failures(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        bad_inputs = (
            "Unclosed $x.\n",
            "<div>unsupported</div>\n",
            "![unsupported](figure.png)\n",
        )
        for markdown in bad_inputs:
            with self.subTest(markdown=markdown):
                with self.assertRaises(generator.GenerationError):
                    generator.render_markdown(markdown, source_name="bad.md")


class ReviewedConverterSyntaxTests(unittest.TestCase):
    def test_reviewed_corpus_relations_and_direct_sum_have_bounded_latex(self):
        cases = {
            "x ≠ y": r"x \neq y",
            "x ∉ S": r"x \notin S",
            "x ≢_A y": r"x ≢_A y",
            "x ≉_{ε_A} y": r"x ≉_{\epsilon_A} y",
            "r_1 ⊕ r_2": r"r_1 ⊕ r_2",
            "λ, 1−λ": r"\lambda, 1-\lambda",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(convert(source), expected)
                translate_inline(expected)


class ArtifactGenerationTests(unittest.TestCase):
    def setUp(self):
        self.generator = load_generator()
        self.assertIsNotNone(
            self.generator,
            "Task 12 LaTeX generator is missing",
        )
        self.profile = {
            "layout": {
                "document_class": "article",
                "font_size_pt": 10,
                "paper_size": "us-letter",
                "body_columns": 2,
                "references_columns": 2,
                "front_matter": "full-width-title-and-abstract",
                "technical_appendices": "single-column",
            },
            "source_ownership": {
                "bibliography_owner": "references/orthemology.bib",
            },
            "package_policy": {
                "supported_packages": [
                    "amsmath",
                    "amssymb",
                    "booktabs",
                    "geometry",
                    "hyperref",
                    "microtype",
                    "natbib",
                    "xcolor",
                ],
            },
        }
        self.artifact = {
            "artifact_id": "sample-artifact",
            "sources": ["docs/notation-gallery.md"],
            "bibliography_owner": "references/orthemology.bib",
            "source_qualifications": [
                "research-stage-draft",
                "not-peer-reviewed",
            ],
        }
        self.source_texts = {
            "docs/notation-gallery.md": (
                "# Sample title\n\n"
                "## Abstract\n\n"
                "Abstract body with $x$.\n\n"
                "## 1. Body\n\n"
                "Body prose.\n\n"
                "## Appendix A. Check\n\n"
                "Technical details.\n\n"
                "## References\n\n"
                "Reference note.\n"
            )
        }

    def test_profile_layout_bibliography_and_qualifications_are_owned(self):
        latex = self.generator.render_artifact(
            self.profile,
            self.artifact,
            self.source_texts,
        )

        self.assertIn(
            r"\documentclass[10pt,letterpaper,twocolumn]{article}",
            latex,
        )
        self.assertIn(r"\twocolumn[", latex)
        self.assertIn(r"\onecolumn", latex)
        self.assertIn(r"\appendix", latex)
        self.assertEqual(latex.count(r"\bibliography{"), 1)
        self.assertIn(
            r"\bibliography{../../../references/orthemology}",
            latex,
        )
        self.assertIn("% source-qualification: research-stage-draft", latex)
        self.assertIn("% source-qualification: not-peer-reviewed", latex)

    def test_expected_tree_is_deterministic_and_validator_catches_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "docs").mkdir()
            (root / "references").mkdir()
            (root / "docs" / "notation-gallery.md").write_text(
                self.source_texts["docs/notation-gallery.md"],
                encoding="utf-8",
                newline="\n",
            )
            (root / "references" / "orthemology.bib").write_text(
                "",
                encoding="utf-8",
                newline="\n",
            )
            first = self.generator.expected_latex_tree(
                root,
                self.profile,
                [self.artifact],
            )
            second = self.generator.expected_latex_tree(
                root,
                self.profile,
                [self.artifact],
            )
            self.assertEqual(first, second)

            output = root / "publication" / "latex"
            self.generator.write_latex_tree(output, first)
            validator = load_validator()
            self.assertIsNotNone(validator, "Task 12 LaTeX validator is missing")
            self.assertEqual(
                validator.validate_latex_tree(
                    root,
                    self.profile,
                    [self.artifact],
                ),
                [],
            )

            main = output / "sample-artifact" / "main.tex"
            original = main.read_text(encoding="utf-8")
            mutations = (
                original.replace("Body prose.", "Changed claim."),
                original + "\n\\immediate\\write18{whoami}\n",
                original + "\n\\input{C:/private/source.tex}\n",
                original + "\n\\conferenceinfo{Invented venue}\n",
            )
            expected_fragments = (
                "semantic divergence",
                "shell escape",
                "absolute path",
                "venue metadata",
            )
            for mutation, fragment in zip(mutations, expected_fragments):
                with self.subTest(fragment=fragment):
                    main.write_text(
                        mutation,
                        encoding="utf-8",
                        newline="\n",
                    )
                    issues = validator.validate_latex_tree(
                        root,
                        self.profile,
                        [self.artifact],
                    )
                    self.assertTrue(
                        any(fragment in issue for issue in issues),
                        issues,
                    )
            main.write_text(original, encoding="utf-8", newline="\n")
            stale_auxiliary = output / "sample-artifact" / "stale.aux"
            stale_auxiliary.write_text("stale", encoding="utf-8", newline="\n")
            self.assertTrue(
                any(
                    "unexpected generated file" in issue
                    for issue in self.generator.tree_drift(output, first)
                )
            )
            self.assertTrue(
                any(
                    "unexpected generated file" in issue
                    for issue in validator.validate_latex_tree(
                        root,
                        self.profile,
                        [self.artifact],
                    )
                )
            )


def load_validator():
    path = SCRIPTS / "validate_latex_sources.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("validate_latex_sources", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    unittest.main()
