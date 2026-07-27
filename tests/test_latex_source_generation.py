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
    def test_matching_outline_prefixes_are_not_repeated_in_latex_headings(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "## 1. First section\n\n"
            "### 1.1 First subsection\n\n"
            "### 1.2 Second subsection\n\n"
            "## 2. Second section\n"
        )

        rendered = generator.render_markdown(
            markdown,
            source_name="matching-outline-prefixes.md",
        )

        self.assertIn(r"\section{First section}", rendered)
        self.assertIn(r"\subsection{First subsection}", rendered)
        self.assertIn(r"\subsection{Second subsection}", rendered)
        self.assertIn(r"\section{Second section}", rendered)
        for repeated in (
            r"\section{1. First section}",
            r"\subsection{1.1 First subsection}",
            r"\subsection{1.2 Second subsection}",
            r"\section{2. Second section}",
        ):
            self.assertNotIn(repeated, rendered)

    def test_nonmatching_and_nonnumeric_heading_prefixes_are_preserved(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "## 9. Nonmatching section\n\n"
            "### 9.1 Nonmatching subsection\n\n"
            "## Descriptive section\n\n"
            "### Qualitative subsection\n\n"
            "## 3.2 Numeric text at section level\n\n"
            "## 3D geometry remains descriptive\n"
        )

        rendered = generator.render_markdown(
            markdown,
            source_name="preserved-heading-prefixes.md",
        )

        for preserved in (
            r"\section{9. Nonmatching section}",
            r"\subsection{9.1 Nonmatching subsection}",
            r"\section{Descriptive section}",
            r"\subsection{Qualitative subsection}",
            r"\section{3.2 Numeric text at section level}",
            r"\section{3D geometry remains descriptive}",
        ):
            self.assertIn(preserved, rendered)

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

    def test_overlong_aligned_conjunction_uses_reconstructable_continuation(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        aligned = r"""\begin{aligned}
\operatorname{TokenAdequate}(\bar\mu, e) &\Leftrightarrow \operatorname{MetaInst}(\bar\mu, \mu) \wedge \operatorname{Compatible}(\bar\mu, A(e)) \\
\operatorname{V3c}(e) &\Leftrightarrow \forall \bar\mu \in \operatorname{MetaTok}(e): \operatorname{TokenAdequate}(\bar\mu, e)
\end{aligned}"""
        markdown = "$$\n%s\n$$\n" % aligned

        first = generator.render_markdown(
            markdown,
            source_name="exact-notation-gallery-aligned-control.md",
        )
        second = generator.render_markdown(
            markdown,
            source_name="exact-notation-gallery-aligned-control.md",
        )

        self.assertEqual(first, second)
        layout_break = "\\\\\n&\\quad{} "
        self.assertIn(
            r"\operatorname{MetaInst}(\bar\mu, \mu) "
            + layout_break
            + r"\wedge \operatorname{Compatible}(\bar\mu, A(e))",
            first,
        )
        relation_break = "\\\\\n&\\quad"
        self.assertIn(
            r"\operatorname{V3c}(e) &\Leftrightarrow"
            + relation_break
            + r" \forall \bar\mu \in \operatorname{MetaTok}(e):"
            + relation_break
            + r" "
            + r"\operatorname{TokenAdequate}(\bar\mu, e)",
            first,
        )
        self.assertEqual(first.count("\n&\\quad"), 3)
        begin = first.index(r"\begin{aligned}")
        end = first.index(r"\end{aligned}", begin) + len(r"\end{aligned}")
        layout_body = first[begin:end]
        self.assertEqual(
            generator.remove_aligned_math_layout_breaks(layout_body),
            aligned,
        )
        for token in (
            r"\operatorname{TokenAdequate}",
            r"\operatorname{MetaInst}",
            r"\operatorname{Compatible}",
            r"\operatorname{V3c}",
            r"\Leftrightarrow",
            r"\wedge",
        ):
            self.assertEqual(layout_body.count(token), aligned.count(token))
        for prohibited in (
            r"\resizebox",
            r"\scalebox",
            r"\small",
            r"\footnotesize",
            r"\hfuzz",
            r"\sloppy",
        ):
            self.assertNotIn(prohibited, first)

    def test_long_table_threshold_is_explicitly_row_or_content_based(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")

        self.assertEqual(generator.LONG_TABLE_ROW_THRESHOLD, 10)
        self.assertEqual(generator.LONG_TABLE_TOTAL_CONTENT_THRESHOLD, 1500)
        self.assertEqual(generator.LONG_TABLE_MAX_ROW_CONTENT_THRESHOLD, 800)
        self.assertEqual(generator.BREAKABLE_TABLE_COLUMN_THRESHOLD, 5)
        self.assertFalse(
            generator.table_requires_breakable_rows(
                data_rows=generator.LONG_TABLE_ROW_THRESHOLD - 1,
                total_rendered_characters=(
                    generator.LONG_TABLE_TOTAL_CONTENT_THRESHOLD - 1
                ),
                max_row_rendered_characters=(
                    generator.LONG_TABLE_MAX_ROW_CONTENT_THRESHOLD - 1
                ),
                columns=generator.BREAKABLE_TABLE_COLUMN_THRESHOLD - 1,
            )
        )
        self.assertTrue(
            generator.table_requires_breakable_rows(
                data_rows=generator.LONG_TABLE_ROW_THRESHOLD,
                total_rendered_characters=0,
                max_row_rendered_characters=0,
                columns=1,
            )
        )
        self.assertTrue(
            generator.table_requires_breakable_rows(
                data_rows=1,
                total_rendered_characters=(
                    generator.LONG_TABLE_TOTAL_CONTENT_THRESHOLD
                ),
                max_row_rendered_characters=0,
                columns=1,
            )
        )
        self.assertTrue(
            generator.table_requires_breakable_rows(
                data_rows=1,
                total_rendered_characters=0,
                max_row_rendered_characters=(
                    generator.LONG_TABLE_MAX_ROW_CONTENT_THRESHOLD
                ),
                columns=1,
            )
        )
        self.assertTrue(
            generator.table_requires_breakable_rows(
                data_rows=1,
                total_rendered_characters=1,
                max_row_rendered_characters=1,
                columns=generator.BREAKABLE_TABLE_COLUMN_THRESHOLD,
            )
        )

    def test_exact_fifteen_line_verdict_table_uses_breakable_row_blocks(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        source = (
            ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"
        ).read_text(encoding="utf-8")
        start = source.index("| Verdict | Question it answers |")
        end = source.index("\n\n", start)
        verdict_table = source[start:end] + "\n"
        self.assertEqual(len(verdict_table.strip().splitlines()), 15)

        rendered = generator.render_markdown(
            verdict_table,
            source_name="exact-verdict-table.md",
        )

        self.assertIn("% breakable-row-table:", rendered)
        self.assertEqual(rendered.count("% breakable-row:"), 13)
        self.assertNotIn(r"\begin{tabular}", rendered)
        self.assertNotIn(r"\begin{minipage}", rendered)
        self.assertNotIn(r"\parbox", rendered)
        self.assertEqual(rendered.count(r"\hrule height 0.8pt"), 2)
        self.assertEqual(rendered.count(r"\hrule height 0.4pt"), 12)
        self.assertEqual(rendered.count(r"\textbf{Verdict}:"), 13)
        self.assertEqual(
            rendered.count(r"\textbf{Question it answers}:"),
            13,
        )
        self.assertNotIn(r"\small", rendered.splitlines())
        for prohibited in (
            r"\footnotesize",
            r"\resizebox",
            r"\scalebox",
        ):
            self.assertNotIn(prohibited, rendered)

        row_labels = (
            "V1 — result correctness",
            "V2a — evidential support",
            "V2b-P — configured-procedure truth-conduciveness",
            "V2b-T — token-level truth linkage",
            "V2c — evidence currentness",
            "V3a — configuration adequacy",
            "V3b — policy adequacy",
            "V3c — governing-token adequacy",
            "V3d — executor fidelity",
            "V3e — ex-ante justification",
            "V4a — route safety",
            "V5 — closure truthfulness",
            "V6 — robustness",
        )
        positions = [rendered.index(label) for label in row_labels]
        self.assertEqual(positions, sorted(positions))

    def test_two_row_result_pathway_matrix_uses_normal_flow_for_tall_row(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        source = (
            ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"
        ).read_text(encoding="utf-8")
        start = source.index("| | **PathwayAdequate** | **PathwayDefective** |")
        end = source.index("\n\n", start)
        matrix = source[start:end] + "\n"

        rendered = generator.render_markdown(
            matrix,
            source_name="exact-result-pathway-matrix.md",
        )

        self.assertIn("% breakable-row-table:", rendered)
        self.assertEqual(rendered.count("% breakable-row:"), 2)
        self.assertNotIn(r"\begin{tabular}", rendered)
        self.assertNotIn(r"\begin{minipage}", rendered)
        self.assertIn(r"\textbf{PathwayAdequate}:", rendered)
        self.assertIn(r"\textbf{PathwayDefective}:", rendered)
        self.assertLess(
            rendered.index("Result correct (V1)"),
            rendered.index("Result incorrect (¬V1)"),
        )

    def test_short_table_remains_one_existing_tabular(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "| Key | Meaning |\n"
            "|---|---|\n"
            "| A | Alpha |\n"
            "| B | Beta |\n"
        )

        rendered = generator.render_markdown(
            markdown,
            source_name="short-table.md",
        )

        self.assertNotIn("% breakable-row-table:", rendered)
        self.assertEqual(rendered.count(r"\begin{tabular}"), 1)
        self.assertEqual(rendered.count(r"\end{tabular}"), 1)
        self.assertIn(r"\toprule", rendered)
        self.assertIn(r"\midrule", rendered)
        self.assertIn(r"\bottomrule", rendered)

    def test_exact_five_column_configuration_table_uses_normal_flow(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        source = (
            ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"
        ).read_text(encoding="utf-8")
        start = source.index(
            "| Configuration | $g$ | $S_\\mu$ | "
            "$\\operatorname{select}_\\mu$ | Meta-policy examples |"
        )
        end = source.index("\n\n", start)
        configuration_table = source[start:end] + "\n"
        self.assertEqual(len(configuration_table.strip().splitlines()), 7)

        rendered = generator.render_markdown(
            configuration_table,
            source_name="exact-five-column-configuration-table.md",
        )

        self.assertIn("% breakable-row-table:", rendered)
        self.assertEqual(rendered.count("% breakable-row:"), 5)
        self.assertNotIn(r"\begin{tabular}", rendered)
        self.assertEqual(rendered.count(r"\textbf{Configuration}:"), 5)
        self.assertEqual(rendered.count(r"\textbf{Meta-policy examples}:"), 5)
        row_labels = (
            "Evidence grade",
            "Version currency",
            "Depth of resolution",
            "Closure standard",
            "Warrant state",
        )
        positions = [rendered.index(label) for label in row_labels]
        self.assertEqual(positions, sorted(positions))

    def test_short_four_column_table_retains_exact_standard_rendering(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        markdown = (
            "| A | B | C | D |\n"
            "|---|---|---|---|\n"
            "| a | b | c | d |\n"
        )
        expected = (
            "\n\\begin{center}\n"
            "\\begin{tabular}{@{}p{0.235\\linewidth}p{0.235\\linewidth}"
            "p{0.235\\linewidth}p{0.235\\linewidth}@{}}\n"
            "\\toprule\n"
            "\\textbf{A} & \\textbf{B} & \\textbf{C} & \\textbf{D} \\\\\n"
            "\\midrule\n"
            "a & b & c & d \\\\\n"
            "\\bottomrule\n"
            "\\end{tabular}\n"
            "\\end{center}\n"
        )

        rendered = generator.render_markdown(
            markdown,
            source_name="short-four-column-table.md",
        )

        self.assertEqual(rendered, expected)

    def test_breakable_table_preserves_escaped_pipe_math_citation_and_order(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        rows = [
            (
                "R1",
                r"escaped \| pipe; math $x \mid y$; citation [@source-one]",
            )
        ] + [("R%d" % number, "Meaning %d" % number) for number in range(2, 11)]
        markdown = (
            "| Label | Meaning |\n"
            "|---|---|\n"
            + "".join("| %s | %s |\n" % row for row in rows)
        )

        first = generator.render_markdown(
            markdown,
            source_name="semantic-table.md",
        )
        second = generator.render_markdown(
            markdown,
            source_name="semantic-table.md",
        )

        self.assertEqual(first, second)
        self.assertIn("% breakable-row-table:", first)
        self.assertNotIn(r"\begin{tabular}", first)
        self.assertNotIn(r"\begin{minipage}", first)
        self.assertEqual(first.count("% breakable-row:"), 10)
        self.assertEqual(first.count(r"\textbf{Label}:"), 10)
        self.assertEqual(first.count(r"\textbf{Meaning}:"), 10)
        self.assertIn("escaped | pipe", first)
        self.assertIn(r"math $x \mid y$", first)
        self.assertIn("citation [@source-one]", first)
        expected_cells = ["R1", "escaped | pipe"] + [
            "R%d" % number for number in range(2, 11)
        ]
        positions = [first.index(cell) for cell in expected_cells]
        self.assertEqual(positions, sorted(positions))

    def test_exact_episode_signature_uses_reconstructable_multline_layout(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        source = (
            ROOT / "manuscript" / "orthemma-ortheme-systems-revised-draft.md"
        ).read_text(encoding="utf-8")
        _, math = generator._protect_math(source)
        displays = [body.strip() for kind, body in math if kind == "display"]
        self.assertEqual(len(displays), 1)
        signature = displays[0]
        self.assertEqual(len(signature), 257)
        markdown = "$$\n%s\n$$\n" % signature

        first = generator.render_markdown(
            markdown,
            source_name="exact-episode-signature.md",
        )
        second = generator.render_markdown(
            markdown,
            source_name="exact-episode-signature.md",
        )

        self.assertEqual(first, second)
        self.assertIn("\\begin{multline*}\n", first)
        self.assertNotIn(r"\[", first)
        begin = first.index("\\begin{multline*}\n") + len("\\begin{multline*}\n")
        end = first.index("\n\\end{multline*}", begin)
        layout_body = first[begin:end]
        self.assertGreaterEqual(
            layout_body.count(generator.DISPLAY_MATH_LAYOUT_BREAK),
            2,
        )
        self.assertEqual(
            generator.remove_display_math_layout_breaks(layout_body),
            signature,
        )
        self.assertEqual(layout_body.count(";"), signature.count(";"))
        self.assertEqual(layout_body.count(","), signature.count(","))
        for prohibited in (
            r"\resizebox",
            r"\scalebox",
            r"\small",
            r"\footnotesize",
        ):
            self.assertNotIn(prohibited, first)

    def test_long_tuple_conjunction_and_implication_preserve_math_tokens(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        examples = {
            "tuple": (
                r"\langle a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, "
                r"a_9, a_{10}, a_{11}, a_{12}, a_{13}, a_{14}, a_{15}, "
                r"a_{16}, a_{17}, a_{18}, a_{19}, a_{20}, a_{21}, a_{22}, "
                r"a_{23}, a_{24}, a_{25} \rangle"
            ),
            "conjunction": (
                r"\forall x,\ \operatorname{Eligible}(x) "
                r"\wedge \operatorname{Grounded}(x) "
                r"\wedge \operatorname{Authorized}(x) "
                r"\wedge \operatorname{Current}(x) "
                r"\wedge \operatorname{Traceable}(x) "
                r"\wedge \operatorname{Robust}(x)"
            ),
            "implication": (
                r"\operatorname{Configured}(e) "
                r"\wedge \operatorname{Executed}(e) "
                r"\Rightarrow \operatorname{Traceable}(e) "
                r"\wedge \operatorname{Current}(e) "
                r"\Rightarrow \operatorname{Reviewable}(e) "
                r"\Leftrightarrow \operatorname{Auditable}(e)"
            ),
        }

        for name, original in examples.items():
            with self.subTest(name=name):
                rendered = generator.render_markdown(
                    "$$\n%s\n$$\n" % original,
                    source_name="%s-control.md" % name,
                )
                begin = rendered.index("\\begin{multline*}\n") + len(
                    "\\begin{multline*}\n"
                )
                end = rendered.index("\n\\end{multline*}", begin)
                layout_body = rendered[begin:end]
                reconstructed = generator.remove_display_math_layout_breaks(
                    layout_body
                )
                self.assertEqual(reconstructed, original)
                for token in (
                    ",",
                    r"\forall",
                    r"\wedge",
                    r"\Rightarrow",
                    r"\Leftrightarrow",
                ):
                    self.assertEqual(
                        layout_body.count(token),
                        original.count(token),
                    )

    def test_display_break_candidates_exclude_nested_punctuation(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        body = (
            r"\operatorname{Pair}(a,b) "
            r"\wedge \operatorname{Tagged}{x,y} "
            r"\Rightarrow z,w"
        )
        positions = generator.reviewed_display_math_break_positions(body)

        nested_commas = [
            index + 1
            for index, character in enumerate(body)
            if character == "," and index + 1 != body.rindex(",") + 1
        ]
        for position in nested_commas:
            self.assertNotIn(position, positions)
        self.assertIn(body.rindex(",") + 1, positions)
        self.assertIn(body.index(r"\wedge") + len(r"\wedge"), positions)
        self.assertIn(
            body.index(r"\Rightarrow") + len(r"\Rightarrow"),
            positions,
        )

    def test_exact_124_character_display_uses_reconstructable_multline_layout(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        exact_display = (
            r"e \models_{\mu} (m : \hat{o}) \iff \hat{o} \in \hat{O}(e) "
            r"\ \text{and}\ \mu \in \vec{\mu}(e)"
            r"\ \text{governed that placement}"
        )
        self.assertEqual(len(exact_display), 124)
        self.assertGreaterEqual(
            len(exact_display),
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD,
        )
        first = generator.render_markdown(
            "$$\n%s\n$$\n" % exact_display,
            source_name="exact-124-character-display.md",
        )
        second = generator.render_markdown(
            "$$\n%s\n$$\n" % exact_display,
            source_name="exact-124-character-display.md",
        )

        self.assertEqual(first, second)
        begin = first.index("\\begin{multline*}\n") + len(
            "\\begin{multline*}\n"
        )
        end = first.index("\n\\end{multline*}", begin)
        layout_body = first[begin:end]
        self.assertEqual(
            layout_body.count(generator.DISPLAY_MATH_LAYOUT_BREAK),
            1,
        )
        self.assertIn(
            r"\iff" + generator.DISPLAY_MATH_LAYOUT_BREAK,
            layout_body,
        )
        self.assertEqual(
            generator.remove_display_math_layout_breaks(layout_body),
            exact_display,
        )
        self.assertIn(r"\text{and}", layout_body)
        self.assertIn(r"\text{governed that placement}", layout_body)

    def test_display_multline_threshold_is_exact_and_reconstructable(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")

        def formula_of_length(length):
            connective = r" \iff "
            payload = length - len(connective)
            left = payload // 2
            return ("x" * left) + connective + ("y" * (payload - left))

        below = formula_of_length(
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD - 1
        )
        at_boundary = formula_of_length(
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD
        )
        self.assertEqual(
            len(below),
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD - 1,
        )
        self.assertEqual(
            len(at_boundary),
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD,
        )

        rendered_below = generator._render_display_math(below)
        self.assertEqual(rendered_below, "\n\\[\n%s\n\\]\n" % below)

        rendered_boundary = generator._render_display_math(at_boundary)
        begin = rendered_boundary.index("\\begin{multline*}\n") + len(
            "\\begin{multline*}\n"
        )
        end = rendered_boundary.index("\n\\end{multline*}", begin)
        layout_body = rendered_boundary[begin:end]
        self.assertEqual(
            generator.remove_display_math_layout_breaks(layout_body),
            at_boundary,
        )

    def test_exact_long_inline_tuples_get_reconstructable_safe_breaks(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        examples = {
            "relspec": (
                r"\operatorname{RelSpec}_q(e) = \langle "
                r"\text{declared reference class}; "
                r"\text{relevant case/risk stratum}; "
                r"\text{reliability metric}; "
                r"\text{threshold or tolerance}; "
                r"\text{perturbation or comparison family where applicable}; "
                r"\text{evaluation protocol}; "
                r"\text{evidence used to establish reliability}; "
                r"\text{version and validity conditions} \rangle"
            ),
            "perturbspec": (
                r"\operatorname{PerturbSpec}(e) = \langle "
                r"\text{varied fields}; "
                r"\text{invariant fields}; "
                r"\text{generator or enumeration}; "
                r"\text{size or measure}; "
                r"\text{tolerance} \rangle"
            ),
        }
        self.assertEqual(len(examples["relspec"]), 344)
        self.assertEqual(len(examples["perturbspec"]), 168)

        for name, original in examples.items():
            with self.subTest(name=name):
                rendered = generator.render_markdown(
                    "Inline $%s$ remains inline.\n" % original,
                    source_name="%s-inline.md" % name,
                )
                prefix = "Inline $"
                suffix = "$ remains inline."
                begin = rendered.index(prefix) + len(prefix)
                end = rendered.index(suffix, begin)
                layout_body = rendered[begin:end]
                self.assertGreaterEqual(
                    layout_body.count(r"\allowbreak{}"),
                    5,
                )
                self.assertEqual(
                    generator.normalize_inline_math_layout(layout_body),
                    original,
                )
                self.assertIn(r"\operatorname{", layout_body)
                self.assertIn(r"\text{", layout_body)
                self.assertNotIn(r"\operatorname\allowbreak{}", layout_body)
                self.assertNotIn(r"\text\allowbreak{}", layout_body)
                self.assertNotIn(r"\begin{multline*}", rendered)

    def test_exact_overlong_text_phrase_splits_at_reviewed_word_space(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        original = (
            r"\operatorname{RelSpec}_q(e) = \langle "
            r"\text{declared reference class}; "
            r"\text{relevant case/risk stratum}; "
            r"\text{reliability metric}; "
            r"\text{threshold or tolerance}; "
            r"\text{perturbation or comparison family where applicable}; "
            r"\text{evaluation protocol}; "
            r"\text{evidence used to establish reliability}; "
            r"\text{version and validity conditions} \rangle"
        )
        rendered = generator._render_inline_math(original)
        expected_split = (
            r"\text{perturbation or comparison }"
            r"\allowbreak{}"
            r"\text{family where applicable}"
        )

        self.assertIn(expected_split, rendered)
        self.assertNotEqual(
            generator.remove_inline_math_layout_breaks(rendered),
            original,
        )
        self.assertEqual(
            generator.normalize_inline_math_layout(rendered),
            original,
        )

    def test_inline_text_split_threshold_and_escaped_content_are_bounded(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        below = "one two three four five six seven eight"
        at_boundary = below + "x"
        escaped = r"alpha beta gamma \{delta\} epsilon zeta eta theta"
        self.assertEqual(
            len(below),
            generator.INLINE_MATH_TEXT_GROUP_BREAK_THRESHOLD - 1,
        )
        self.assertEqual(
            len(at_boundary),
            generator.INLINE_MATH_TEXT_GROUP_BREAK_THRESHOLD,
        )

        def qualifying_formula(content):
            return (
                r"\operatorname{TextSpec}(e) = \langle \text{"
                + content
                + r"}; \text{padding words keep this structured formula "
                r"above the inline threshold} \rangle"
            )

        below_formula = qualifying_formula(below)
        below_layout = generator._render_inline_math(below_formula)
        self.assertIn(r"\text{%s}" % below, below_layout)
        self.assertEqual(
            generator.normalize_inline_math_layout(below_layout),
            below_formula,
        )

        boundary_formula = qualifying_formula(at_boundary)
        boundary_layout = generator._render_inline_math(boundary_formula)
        self.assertNotIn(r"\text{%s}" % at_boundary, boundary_layout)
        self.assertIn(
            r"}\allowbreak{}\text{",
            boundary_layout,
        )
        self.assertEqual(
            generator.normalize_inline_math_layout(boundary_layout),
            boundary_formula,
        )

        escaped_formula = qualifying_formula(escaped)
        escaped_layout = generator._render_inline_math(escaped_formula)
        self.assertIn(r"\text{%s}" % escaped, escaped_layout)
        self.assertEqual(
            generator.normalize_inline_math_layout(escaped_layout),
            escaped_formula,
        )

        short_formula = r"\text{%s}" % at_boundary
        self.assertLess(
            len(short_formula),
            generator.INLINE_MATH_BREAK_THRESHOLD,
        )
        self.assertEqual(
            generator._render_inline_math(short_formula),
            short_formula,
        )

    def test_inline_break_candidates_exclude_nested_math_syntax(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        body = (
            r"\operatorname{Pair}(a,b) = \text{left,right}; "
            r"x_{i,j} \wedge y,z"
        )
        positions = generator.reviewed_inline_math_break_positions(body)

        excluded_commas = [
            body.index(",", body.index("(a,b)")) + 1,
            body.index(",", body.index(r"\text{left,right}")) + 1,
            body.index(",", body.index(r"_{i,j}")) + 1,
        ]
        for position in excluded_commas:
            self.assertNotIn(position, positions)
        self.assertIn(body.index("=") + 1, positions)
        self.assertIn(body.index(";") + 1, positions)
        self.assertIn(
            body.index(r"\wedge") + len(r"\wedge"),
            positions,
        )
        self.assertIn(body.rindex(",") + 1, positions)

    def test_inline_break_candidates_preserve_subscript_and_superscript_attachment(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        scripted_boundaries = (
            (r"left =_{q} right", "="),
            (r"left =   ^{q} right", "="),
            (r"left \sim_{q} right", r"\sim"),
            (r"left \sim   ^{q} right", r"\sim"),
            (r"left \wedge_{\mu} right", r"\wedge"),
            (r"left \iff  ^{q} right", r"\iff"),
        )

        for body, boundary in scripted_boundaries:
            with self.subTest(body=body):
                positions = generator.reviewed_inline_math_break_positions(body)
                boundary_end = body.index(boundary) + len(boundary)
                self.assertNotIn(boundary_end, positions)

        ordinary = r"left = right \sim other \wedge final"
        ordinary_positions = generator.reviewed_inline_math_break_positions(
            ordinary
        )
        for boundary in ("=", r"\sim", r"\wedge"):
            with self.subTest(ordinary_boundary=boundary):
                self.assertIn(
                    ordinary.index(boundary) + len(boundary),
                    ordinary_positions,
                )

    def test_long_inline_renderer_never_separates_scripted_math_bases(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        original = (
            r"\operatorname{Guarded}(e) =_{q} "
            r"\operatorname{Left}(e) \wedge_{\mu} "
            r"\operatorname{RightWithLongPayloadForLayoutQualification}"
            r"(e, q, \mu)"
        )
        self.assertGreaterEqual(
            len(original),
            generator.INLINE_MATH_BREAK_THRESHOLD,
        )

        rendered = generator._render_inline_math(original)

        self.assertEqual(rendered, original)
        self.assertNotIn(
            generator.INLINE_MATH_LAYOUT_BREAK + "_",
            rendered,
        )
        self.assertNotIn(
            generator.INLINE_MATH_LAYOUT_BREAK + "^",
            rendered,
        )

    def test_short_math_controls_stay_unchanged_and_long_inline_is_breakable(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        short_display = r"x \iff y"
        rendered_display = generator.render_markdown(
            "$$\n%s\n$$\n" % short_display,
            source_name="short-display.md",
        )
        self.assertIn("\n\\[\n%s\n\\]\n" % short_display, rendered_display)
        self.assertNotIn(r"\begin{multline*}", rendered_display)

        short_inline = r"\operatorname{Pair}(x,y) = z"
        rendered_short_inline = generator.render_markdown(
            "Inline $%s$ remains inline.\n" % short_inline,
            source_name="short-inline.md",
        )
        self.assertIn("$%s$" % short_inline, rendered_short_inline)
        self.assertNotIn(r"\allowbreak{}", rendered_short_inline)

        unstructured_inline = (
            r"\operatorname{Unbroken}{"
            + ("x" * generator.INLINE_MATH_BREAK_THRESHOLD)
            + "}"
        )
        rendered_unstructured = generator.render_markdown(
            "Inline $%s$ remains inline.\n" % unstructured_inline,
            source_name="unstructured-long-inline.md",
        )
        self.assertIn("$%s$" % unstructured_inline, rendered_unstructured)
        self.assertNotIn(r"\allowbreak{}", rendered_unstructured)

        long_inline = (
            r"\operatorname{Configured}(e) "
            r"\wedge \operatorname{Executed}(e) "
            r"\Rightarrow \operatorname{Traceable}(e) "
            r"\wedge \operatorname{Current}(e) "
            r"\Rightarrow \operatorname{Reviewable}(e) "
            r"\Leftrightarrow \operatorname{Auditable}(e)"
        )
        self.assertGreaterEqual(
            len(long_inline),
            generator.DISPLAY_MATH_MULTLINE_THRESHOLD,
        )
        rendered_inline = generator.render_markdown(
            "Inline $%s$ remains inline.\n" % long_inline,
            source_name="long-inline.md",
        )
        prefix = "Inline $"
        suffix = "$ remains inline."
        begin = rendered_inline.index(prefix) + len(prefix)
        end = rendered_inline.index(suffix, begin)
        layout_body = rendered_inline[begin:end]
        self.assertGreaterEqual(
            layout_body.count(r"\allowbreak{}"),
            5,
        )
        self.assertEqual(
            generator.normalize_inline_math_layout(layout_body),
            long_inline,
        )
        self.assertNotIn(r"\begin{multline*}", rendered_inline)

    def test_exact_long_inline_code_path_gets_reconstructable_breaks(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        path = "experiments/false-closure-selective-prediction-v2/"
        markdown = "Packet `%s` is frozen.\n" % path

        first = generator.render_markdown(
            markdown,
            source_name="exact-inline-code-path.md",
        )
        second = generator.render_markdown(
            markdown,
            source_name="exact-inline-code-path.md",
        )

        self.assertEqual(first, second)
        self.assertTrue(generator.is_path_like_inline_code(path))
        texttt_open = first.index(r"\texttt{") + len(r"\texttt{")
        texttt_close = first.index("} is frozen.", texttt_open)
        layout_body = first[texttt_open:texttt_close]
        self.assertGreaterEqual(
            layout_body.count(generator.INLINE_CODE_PATH_LAYOUT_BREAK),
            4,
        )
        self.assertEqual(
            generator.remove_inline_code_path_layout_breaks(layout_body),
            generator._escape_code(path),
        )

    def test_unique_tracked_source_filenames_get_reconstructable_breaks(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        expected = {
            "orthability-and-the-ground-of-intelligibility.md": (
                "companion/orthability-and-the-ground-of-intelligibility.md"
            ),
            "orthability-divine-attributes-and-speech-athari.md": (
                "companion/orthability-divine-attributes-and-speech-athari.md"
            ),
        }
        resolutions = (
            generator.tracked_unique_inline_code_basename_resolutions(ROOT)
        )

        for filename, relative in expected.items():
            with self.subTest(filename=filename):
                self.assertEqual(resolutions.get(filename), relative)
                self.assertTrue(
                    generator.is_path_like_inline_code(filename)
                )
                rendered = generator.render_markdown(
                    "Companion `%s` remains exact.\n" % filename,
                    source_name="unique-source-filename.md",
                )
                texttt_open = rendered.index(r"\texttt{") + len(r"\texttt{")
                texttt_close = rendered.index("} remains exact.", texttt_open)
                layout_body = rendered[texttt_open:texttt_close]
                self.assertGreaterEqual(
                    layout_body.count(
                        generator.INLINE_CODE_PATH_LAYOUT_BREAK
                    ),
                    4,
                )
                self.assertEqual(
                    generator.remove_inline_code_path_layout_breaks(
                        layout_body
                    ),
                    generator._escape_code(filename),
                )

    def test_ambiguous_nonexistent_and_nonfilename_controls_stay_literal(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        resolutions = (
            generator.tracked_unique_inline_code_basename_resolutions(ROOT)
        )
        tracked_paths = generator._tracked_repository_paths(ROOT)
        controls = (
            "README.md",
            "report(v1).md",
            "v1.2",
            "2026-07-27",
            "STATUS_A",
            "RESULT_CORRECT",
        )

        self.assertEqual(
            generator.ALLOWED_INLINE_CODE_BASENAME_EXTENSIONS,
            {".bib", ".json", ".md", ".py", ".tex", ".yaml", ".yml"},
        )
        self.assertGreater(
            sum(
                pathlib.PurePosixPath(path).name == "README.md"
                for path in tracked_paths
            ),
            1,
        )
        self.assertNotIn("README.md", resolutions)
        self.assertNotIn("report(v1).md", resolutions)
        for basename, path in resolutions.items():
            with self.subTest(resolution=basename):
                self.assertEqual(
                    sorted(
                        tracked
                        for tracked in tracked_paths
                        if pathlib.PurePosixPath(tracked).name == basename
                    ),
                    [path],
                )
        for control in controls:
            with self.subTest(control=control):
                self.assertFalse(generator.is_path_like_inline_code(control))
                rendered = generator.render_markdown(
                    "Control `%s` remains literal.\n" % control,
                    source_name="inline-code-basename-control.md",
                )
                self.assertIn(
                    r"\texttt{%s}" % generator._escape_code(control),
                    rendered,
                )
                self.assertNotIn(
                    generator.INLINE_CODE_PATH_LAYOUT_BREAK,
                    rendered,
                )

    def test_inline_code_registry_command_url_and_nonpath_controls_are_unchanged(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        controls = (
            "RESULT_CORRECT",
            "python scripts/generate_latex_sources.py --check",
            "https://example.test/a-b",
            "and/or",
            "x/y",
            "--root/path",
            "V2b-P/V2b-T",
            "ARG-01/ARG-02",
            "v1.2/v2.0",
            "2026-07-27/2026-08-01",
            "STATUS_A/STATUS_B",
        )

        for control in controls:
            with self.subTest(control=control):
                self.assertFalse(generator.is_path_like_inline_code(control))
                rendered = generator.render_markdown(
                    "Control `%s` remains literal.\n" % control,
                    source_name="inline-code-control.md",
                )
                self.assertIn(
                    r"\texttt{%s}" % generator._escape_code(control),
                    rendered,
                )
                self.assertNotIn(
                    generator.INLINE_CODE_PATH_LAYOUT_BREAK,
                    rendered,
                )

    def test_inline_code_path_roots_are_closed_and_tracked(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        expected_roots = {
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
        self.assertEqual(
            generator.DECLARED_REPOSITORY_INLINE_CODE_ROOTS,
            expected_roots,
        )
        tracked_roots = generator.tracked_repository_root_segments(ROOT)
        self.assertTrue(expected_roots <= tracked_roots)
        self.assertNotIn("sourcing", tracked_roots)
        self.assertNotIn("theislampill", tracked_roots)
        generator.validate_inline_code_path_declarations(ROOT)

        self.assertEqual(
            generator.DECLARED_EXTERNAL_REPOSITORY_SLUGS,
            {"theislampill/daee-epistemics"},
        )
        self.assertTrue(
            generator.is_path_like_inline_code(
                "theislampill/daee-epistemics"
            )
        )
        self.assertFalse(
            generator.is_path_like_inline_code("theislampill/other")
        )
        self.assertFalse(
            generator.is_path_like_inline_code(
                "another-owner/daee-epistemics"
            )
        )

        self.assertEqual(
            generator.DECLARED_SOURCE_RELATIVE_INLINE_CODE_PATHS,
            {"sourcing/R3-COMPANION-SOURCING-LEDGER.md"},
        )
        self.assertTrue(
            generator.is_path_like_inline_code(
                "sourcing/R3-COMPANION-SOURCING-LEDGER.md"
            )
        )
        self.assertFalse(
            generator.is_path_like_inline_code(
                "sourcing/COPIED-NONPATH.md"
            )
        )

    def test_repository_path_grammar_accepts_valid_nested_forms_only(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        valid = (
            "applications/daee-epistemics/",
            "docs/architecture/ORTHEMOLOGY-LAYER-MAP.md",
            "docs/project-closure/r7b/R7B-PDF-MATH-BASELINE.md",
            "scripts/generate_latex_sources.py",
            "scripts/latex_to_typst_math.py",
            "tests/reqpath-fixtures.json",
            "references/source-status.yaml",
        )
        copied_nonpaths = (
            "V2b-P/V2b-T",
            "ARG-01/ARG-02",
            "v1.2/v2.0",
            "2026-07-27/2026-08-01",
            "STATUS_A/STATUS_B",
            "unknown/docs/current-state.yaml",
            "scripts//generate_latex_sources.py",
            "/docs/current-state.yaml",
            "../docs/current-state.yaml",
        )

        for path in valid:
            with self.subTest(valid=path):
                self.assertTrue(generator.is_path_like_inline_code(path))
        for text in copied_nonpaths:
            with self.subTest(copied_nonpath=text):
                self.assertFalse(generator.is_path_like_inline_code(text))

    def test_current_path_and_inline_math_layout_inventories_remain_exact(self):
        generator = load_generator()
        self.assertIsNotNone(generator, "Task 12 LaTeX generator is missing")
        profile = yaml.safe_load(
            (ROOT / "docs" / "publication-profile.yaml").read_text(
                encoding="utf-8"
            )
        )

        def walk(tokens):
            for token in tokens:
                yield token
                if token.children:
                    yield from walk(token.children)

        path_values = []
        basename_values = []
        for artifact in profile["artifacts"]:
            for relative in artifact["sources"]:
                source = (ROOT / relative).read_text(encoding="utf-8")
                protected, _ = generator._protect_math(source)
                tokens = (
                    generator.MarkdownIt("commonmark")
                    .enable("table")
                    .enable("strikethrough")
                    .parse(protected)
                )
                for token in walk(tokens):
                    if token.type != "code_inline":
                        continue
                    if generator._inline_code_path_segments(token.content):
                        if generator.is_path_like_inline_code(token.content):
                            path_values.append(token.content)
                    elif generator.is_uniquely_tracked_inline_code_basename(
                        token.content,
                        ROOT,
                    ):
                        basename_values.append(token.content)

        tree = generator.expected_latex_tree(ROOT, profile)
        total_marker_count = sum(
            content.count(generator.INLINE_CODE_PATH_LAYOUT_BREAK)
            for content in tree.values()
        )
        path_marker_count = sum(
            generator._render_inline_code(path).count(
                generator.INLINE_CODE_PATH_LAYOUT_BREAK
            )
            for path in path_values
        )
        basename_marker_count = sum(
            generator._render_inline_code(filename).count(
                generator.INLINE_CODE_PATH_LAYOUT_BREAK
            )
            for filename in basename_values
        )
        self.assertEqual(len(path_values), 65)
        self.assertEqual(len(set(path_values)), 39)
        self.assertEqual(path_marker_count, 241)
        self.assertEqual(len(basename_values), 16)
        self.assertEqual(len(set(basename_values)), 10)
        self.assertEqual(basename_marker_count, 70)
        for filename in set(basename_values):
            with self.subTest(reconstructable_basename=filename):
                layout_body = generator._render_inline_code(filename)
                self.assertEqual(
                    generator.remove_inline_code_path_layout_breaks(
                        layout_body
                    ),
                    generator._escape_code(filename),
                )
        self.assertEqual(
            total_marker_count - path_marker_count - basename_marker_count,
            44,
        )
        for path, content in tree.items():
            with self.subTest(generated_path=path):
                self.assertNotIn(
                    generator.INLINE_MATH_LAYOUT_BREAK + "_",
                    content,
                )
                self.assertNotIn(
                    generator.INLINE_MATH_LAYOUT_BREAK + "^",
                    content,
                )

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

    def test_outline_number_matching_spans_front_matter_and_body(self):
        source_texts = {
            "docs/notation-gallery.md": (
                "# Sample title\n\n"
                "## Abstract\n\n"
                "Abstract body.\n\n"
                "## 2. Body\n\n"
                "### 2.1 Detail\n\n"
                "Body prose.\n"
            )
        }

        latex = self.generator.render_artifact(
            self.profile,
            self.artifact,
            source_texts,
        )

        self.assertIn(r"\section{Abstract}", latex)
        self.assertIn(r"\section{Body}", latex)
        self.assertIn(r"\subsection{Detail}", latex)
        self.assertNotIn(r"\section{2. Body}", latex)
        self.assertNotIn(r"\subsection{2.1 Detail}", latex)

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
