#!/usr/bin/env python3
"""Focused tests for planned-output internal-reference handling.

The synthetic cases run an unchanged copy of the production validator inside
an isolated temporary Git repository.  No test depends on a future output in
the live implementation plan, so completing a later task cannot stale this
suite again.
"""
import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_internal_references.py"
DOCS = "do" + "cs"
SENTINEL = DOCS + "/future/SYNTHETIC-PLANNED-OUTPUT.json"
PLAN = Path(DOCS) / "superpowers/plans/synthetic-internal-reference-plan.md"


def run_command(command, cwd, *, check=True, env=None):
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=check,
        env=env,
    )


def run_git(root, *args):
    return run_command(["git", *args], root)


def write(root, relative_path, content):
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")
    return target


def commit_all(root, message="synthetic fixture"):
    run_git(root, "add", "--all")
    run_git(root, "commit", "--quiet", "-m", message)


@contextlib.contextmanager
def temporary_corpus():
    """Yield a minimal committed corpus and always remove it afterward."""
    with tempfile.TemporaryDirectory(prefix="orthemology-internal-refs-") as temp:
        root = Path(temp)
        run_git(root, "init", "--quiet")
        run_git(root, "config", "user.name", "Internal Reference Fixture")
        run_git(root, "config", "user.email", "fixture@example.invalid")

        validator = root / "scripts" / "validate_internal_references.py"
        validator.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(VALIDATOR, validator)
        shutil.copy2(ROOT / "scripts" / "validate_repo.py", validator.parent / "validate_repo.py")
        write(
            root,
            "docs/reference-exemptions.yaml",
            "external_paths:\n"
            "  owner_repository: synthetic-fixture\n"
            "  paths: []\n"
            "retired_paths:\n"
            "  paths: []\n",
        )
        # These are historical examples named in the validator's own docstring.
        write(root, "examples/shared-upstream-corroboration-failure.json", "{}\n")
        write(root, "scripts/validate_claim_reasoning_paths.py", "# fixture\n")
        # Literal owner paths named by the production selector contracts also
        # need reference targets in this miniature corpus. These empty fixtures
        # confer no source identity: its source map has no registered rows.
        for target in (
            "docs/provenance/v5-successors/EVIDENCE_BINDINGS.json",
            "docs/provenance/v5-successors/fragments/D04.json",
            "experiments/orthemology-v5-successors/groups/t16-successor/REPLAY_INPUTS.json",
            "scripts/replay_v5_successors.py",
            "scripts/v5_d04_assets/covering_recipe.py",
            "scripts/v5_d04_assets/v5_d04_normalizers_translated.py",
            "scripts/v5_d04_recipes.json",
            "experiments/orthemology-v5-successors/source-store/0748d78e938b178963f833decf2cafba3584b4262c534b6083168d59a0a1b3d6/FINAL_EXECUTION_RECORD.json",
            "experiments/orthemology-v5-successors/source-store/61b23329c0dc24c8533a922204769a2128e7574bcbf96ba52424bda2a6614fbb/PUBLIC_PROJECTION.json",
        ):
            write(root, target, "{}\n" if target.endswith('.json') else '# fixture\n')
        write(root, ".gitignore", ".superpowers/sdd/\n")
        write(root, "docs/provenance/v5-consolidation/SOURCE_MAP.json", '{"sources": []}\n')
        commit_all(root, "initialize synthetic corpus")
        yield root


def run_validator(root=ROOT):
    validator = root / "scripts" / "validate_internal_references.py"
    return run_command(
        [sys.executable, str(validator)],
        root,
        check=False,
        # Supply the unchanged production resolver as an import dependency.
        # The fixture-local validator and validate_repo remain first on sys.path;
        # dependency source files are not added to the miniature citation corpus.
        env={**os.environ, "PYTHONPATH": str(ROOT / "scripts")},
    )


def assert_failure(test, result, cited, source=None):
    output = result.stdout + result.stderr
    test.assertEqual(1, result.returncode, output)
    test.assertIn(cited, output)
    if source is not None:
        test.assertIn(str(source).replace("\\", "/"), output)


class HistoricalProjectionReferenceTests(unittest.TestCase):
    """Original-coordinate resolution is finite, exact and owner-specific."""
    @classmethod
    def setUpClass(cls):
        from test_ar8r_v11_reconciliation import Pmr007DuplicateAliasTests
        cls.fixture_type = Pmr007DuplicateAliasTests
        cls.fixture_type.setUpClass()
        cls.addClassCleanup(cls.fixture_type.doClassCleanups)

    def setUp(self):
        import importlib.util
        from unittest import mock
        import hashlib
        import json
        self.fixture = self.fixture_type('test_exact_canonical_copies_admit_the_entire_finite_batch')
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        spec = importlib.util.spec_from_file_location('projection_reference_fixture', VALIDATOR)
        self.refs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.refs)
        patch = mock.patch.multiple(self.refs, ROOT=str(self.fixture.repo),
                                    HISTORICAL_PROSE_REVISION=self.fixture.baseline)
        patch.start(); self.addCleanup(patch.stop)
        self.alias = self.fixture.selection[0]['alias']
        self.canonical = self.fixture.repo / self.fixture.selection[0]['canonical']
        self.body = self.canonical.read_bytes()
        identity = hashlib.sha256(self.body).hexdigest()
        self.row = {'repository_path':self.alias, 'disposition':'REUSE',
            'repository_revision':self.fixture.baseline, 'source_sha256':identity,
            'public_sha256':identity, 'source_bytes':len(self.body), 'public_bytes':len(self.body),
            'git_blob':hashlib.sha1(b'blob '+str(len(self.body)).encode()+b'\0'+self.body).hexdigest(),
            'publication_basis':'exact_existing_public_git_blob; retained_counterpart_qualified_by_snapshot_validator'}
        self.manifest = self.fixture.repo / self.refs.PROJECTION_MANIFEST
        self.manifest.parent.mkdir(parents=True)
        self.write_row(self.row)
        (self.fixture.repo / self.alias).unlink()

    def write_row(self, row):
        import json
        self.manifest.write_text(json.dumps({'objects':[row]}))

    def resolves(self):
        return self.refs._resolves(self.refs.PROJECTION_MANIFEST,self.alias)

    def test_exact_original_route_and_metadata_changes_do_not_leak_to_other_owners(self):
        self.assertTrue(self.resolves())
        self.assertFalse(self.refs._resolves('README.md',self.alias))
        for field,value in (('source_sha256','0'*64),('public_sha256','0'*64),
                ('source_bytes',1),('public_bytes',1),('git_blob','0'*40),
                ('repository_revision','HEAD'),('disposition','PROJECT'),
                ('publication_basis','unreviewed')):
            with self.subTest(field=field):
                self.write_row(dict(self.row,**{field:value}))
                self.assertFalse(self.resolves())
                self.write_row(self.row)
                self.assertTrue(self.resolves())
        selected={r['alias'] for r in self.fixture.selection}
        excluded=next(p for p in self.fixture.bodies if p.startswith(self.fixture.prefix+'/') and p not in selected)
        (self.fixture.repo/excluded).unlink()
        self.assertFalse(self.refs._resolves(self.refs.PROJECTION_MANIFEST,excluded))

    def test_current_copy_and_present_alias_cannot_fall_through_to_exists(self):
        self.assertTrue(self.resolves())
        for target in (self.canonical,self.fixture.repo/self.alias):
            with self.subTest(path=str(target.relative_to(self.fixture.repo))):
                target.write_bytes(self.body+b'changed')
                self.assertFalse(self.resolves())
                target.write_bytes(self.body);target.chmod(0o755)
                self.assertFalse(self.resolves())
                target.chmod(0o644);target.unlink();target.symlink_to(self.manifest)
                self.assertFalse(self.resolves())
                target.unlink();target.write_bytes(self.body)
                self.assertTrue(self.resolves())

    def test_same_size_corrupt_original_git_object_cannot_borrow_current_copy(self):
        import zlib
        self.assertTrue(self.resolves())
        oid=self.row['git_blob']
        target=self.fixture.repo/'.git/objects'/oid[:2]/oid[2:]
        original=target.read_bytes();mode=target.stat().st_mode&0o777
        corrupt=b'x'*len(self.body)
        try:
            target.unlink();target.write_bytes(zlib.compress(b'blob '+str(len(corrupt)).encode()+b'\0'+corrupt))
            self.assertFalse(self.resolves())
        finally:
            target.unlink();target.write_bytes(original);target.chmod(mode)
        self.assertTrue(self.resolves())


class InternalReferenceTests(unittest.TestCase):
    def test_jsonl_path_is_not_truncated_and_missing_jsonl_stays_red(self):
        with temporary_corpus() as corpus:
            target = DOCS + "/records.jsonl"
            write(corpus, target, "{}\n")
            write(corpus, DOCS + "/reader.md", "Read `" + target + "`.\n")
            result = run_validator(corpus)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            (corpus / target).unlink()
            result = run_validator(corpus)
            assert_failure(self, result, target)

    def test_original_selector_field_does_not_exempt_native_destination(self):
        import json
        with temporary_corpus() as corpus:
            source_map = DOCS + "/provenance/v5-consolidation/SOURCE_MAP.json"
            row = {"source_artifact": "V4", "source_path": "examples/" + "packet-only.json",
                   "source_sha256": "a" * 64, "operation": "EXTERNAL_CUSTODY",
                   "transformation": "NO_REPOSITORY_EFFECT", "destination_repository_path": None,
                   "public_safety_tier": "HISTORICAL_EVIDENCE"}
            write(corpus, source_map, json.dumps({"sources": [row]}, indent=2))
            result = run_validator(corpus)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            row["destination_repository_path"] = DOCS + "/missing-native.json"
            write(corpus, source_map, json.dumps({"sources": [row]}, indent=2))
            result = run_validator(corpus)
            assert_failure(self, result, row["destination_repository_path"])
            row["destination_repository_path"] = None
            row["source_sha256"] = None
            write(corpus, source_map, json.dumps({"sources": [row]}, indent=2))
            result = run_validator(corpus)
            assert_failure(self, result, row["source_path"])

    def test_exact_committed_create_line_exempts_absent_output(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            commit_all(corpus)
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_current_evidence_for_same_missing_output_is_rejected(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            source = Path(DOCS) / "current-evidence.md"
            write(corpus, source, f"Current evidence: `{SENTINEL}`.\n")
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, source)

    def test_ordinary_plan_reuse_is_not_a_planned_output(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                PLAN,
                f"- Create: `{SENTINEL}`\n\nCurrent evidence: `{SENTINEL}`.\n",
            )
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_materialization_resolves_create_ordinary_and_current_occurrences(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                PLAN,
                f"- Create: `{SENTINEL}`\n\nOrdinary reuse: `{SENTINEL}`.\n",
            )
            source = Path(DOCS) / "current-evidence.md"
            write(corpus, source, f"Current evidence: `{SENTINEL}`.\n")
            commit_all(corpus)
            absent = run_validator(corpus)
            write(corpus, SENTINEL, "{}\n")
            materialized = run_validator(corpus)
        assert_failure(self, absent, SENTINEL)
        self.assertEqual(
            0,
            materialized.returncode,
            materialized.stdout + materialized.stderr,
        )

    def test_untracked_plan_create_line_is_not_authoritative(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_staged_only_plan_create_line_is_not_authoritative(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
            run_git(corpus, "add", "--", PLAN.as_posix())
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_malformed_create_prefix_is_rejected(self):
        with temporary_corpus() as corpus:
            write(corpus, PLAN, f"- Create: `{SENTINEL}` after approval\n")
            commit_all(corpus)
            result = run_validator(corpus)
        assert_failure(self, result, SENTINEL, PLAN)

    def test_windows_style_ordinary_missing_path_is_rejected(self):
        missing = DOCS + "/future/WINDOWS-MISSING.json"
        with temporary_corpus() as corpus:
            source = Path(DOCS) / "windows-path.md"
            windows_missing = DOCS + "\\future\\WINDOWS-MISSING.json"
            write(corpus, source, f"Current evidence: `{windows_missing}`.\n")
            result = run_validator(corpus)
        assert_failure(self, result, missing, source)

    def test_absolute_environment_paths_are_not_repository_citations(self):
        with temporary_corpus() as corpus:
            absolute_script = (
                "C:" + "\\work" + "space\\repo\\" + "scr" + "ipts\\ENVIRONMENT-MISSING.py"
            )
            mixed_case_venv = "C:" + "\\venv\\Scripts\\python.exe"
            write(
                corpus,
                Path(DOCS) / "environment-path.md",
                f"Interpreter candidates: `{absolute_script}` and `{mixed_case_venv}`.\n",
            )
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_ignored_report_is_not_part_of_the_prospective_corpus(self):
        with temporary_corpus() as corpus:
            write(
                corpus,
                ".superpowers/sdd/ignored-report.md",
                f"Current evidence: `{DOCS}/future/IGNORED-MISSING.json`.\n",
            )
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_resolved_path_in_a_prospective_file_passes(self):
        with temporary_corpus() as corpus:
            target = DOCS + "/CITING.md"
            write(corpus, target, "# Existing target\n")
            write(corpus, Path(DOCS) / "resolved.md", f"Current evidence: `{target}`.\n")
            result = run_validator(corpus)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_temporary_corpus_cleanup_leaves_no_repository_residue(self):
        before = run_git(ROOT, "status", "--porcelain=v1", "--ignored").stdout
        success_path = None
        with temporary_corpus() as corpus:
            success_path = corpus
            write(corpus, PLAN, f"- Create: `{SENTINEL}`\n")
        self.assertFalse(success_path.exists())

        failure_path = None
        with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
            with temporary_corpus() as corpus:
                failure_path = corpus
                raise RuntimeError("synthetic failure")
        self.assertFalse(failure_path.exists())
        after = run_git(ROOT, "status", "--porcelain=v1", "--ignored").stdout
        self.assertEqual(before, after)

    def test_workflow_runs_focused_then_production_validator(self):
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
            encoding="utf-8"
        )
        focused = "python tests/test_internal_references.py"
        production = "python scripts/validate_internal_references.py"
        self.assertIn(f"{focused}\n          {production}", workflow)

    def test_unchanged_real_repository_production_validator_passes(self):
        result = run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
