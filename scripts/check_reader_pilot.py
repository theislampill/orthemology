#!/usr/bin/env python3
"""Check a bounded representative reader crosswalk, not scientific truth.

The input population comes from an exact Git baseline, separately from the
editorial sample. Existing publication ownership is read rather than copied into
a competing scientific registry. This checker is read-only and does not fetch
URLs, execute source payloads, extract theorems, or infer semantic acceptance.
"""

from resolve_t20_v6_source import NEXT250
from resolve_t20_v6_source import AFTER3384_PATHS, after3384_absences
from resolve_t20_v6_source import AFTER3634_PATHS, after3634_absences

from resolve_t20_v6_source import (NEW250_PATHS, new250_absences, new250_provider_additions, new250_reader_sources)

from resolve_t20_v6_source import (DIGEST_RECORD_PATHS, digest_record_absences,
    ADMISSION_RECORD_MEMBERS, ADMISSION_RECORD_PATHS, admission_record_bytes, _administrative_git)

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import stat
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

from validate_ar8r_reconciliation import (
    PMR007_DEEP_PREFIX, pmr007_deep_duplicate_paths,
    PMR007_ROUNDS_PREFIX, PMR007_ROUNDS_FORMALIZATION,
    pmr007_rounds_duplicate_paths, pmr007_rounds_formalization_navigation,
)

from resolve_t20_v6_source import (
    HISTORICAL_PROSE, HISTORICAL_PROSE_PUBLIC_PATHS, HISTORICAL_PROSE_REVISION,
    historical_source_bytes, HISTORICAL_PROSE_REVISIONS, HISTORICAL_PROSE_DISPOSITIONS,
    MEDIATOR_PROSE, MEDIATOR_GUIDE, mediator_guide_source_bytes, readonly_git_diff,
    ORIGINAL_HISTORICAL_PROSE_PATHS, FISHER_AUDIT, FISHER_PROSE_REVISION,
    TYPED_PROSE, TYPED_PROSE_REVISION, TYPED_GUIDES, typed_guide_source_bytes,
    CONTINUATION_READER_PROSE, T4_READER_PROSE, T4_READER_SUPPORT_PROSE,
    SPARSE_PRIOR_PROSE, SPARSE_PRIOR_SUPPORT_PROSE,
    NEXT24_PROSE, NEXT24_SUPPORT_PROSE, NEXT24_PUBLIC_PROSE,
    CONTINUATION_COPY_ROOT, continuation_duplicate_paths,
    ADMIN_RECORD_PATHS, administrative_record_bytes, administrative_record_absences,
    ADMIN_GUIDES, ADMIN_PUBLIC_GUIDE_PATHS, ADMIN_RECORD_BASE, administrative_guide_source_bytes,
    PUBLIC_READER_NOTE_PATHS, CONTINUATION_REGISTRY_PATH, CONTINUATION_REGISTRY_REVISION,
    CHECKPOINT_COPY_PATHS, checkpoint_duplicate_paths,
    CHECKPOINT_PUBLIC_COPY_PATHS, checkpoint_public_duplicate_paths,
    CHECKPOINT_RECORD_COPY_PATHS, checkpoint_record_duplicate_paths,
    CHECKPOINT_PACKAGE_COPY_PATHS, checkpoint_package_duplicate_paths,
    FORMAL_COPY_PATHS, formal_duplicate_paths,
    FORMAL_PROVIDER_PATHS, formal_provider_absences,
    CHECKPOINT_CODE_COPY_PATHS, checkpoint_code_duplicate_paths,
    SUCCESSOR_INPUT_PATHS, SUCCESSOR_INPUT_REGISTRY, SUCCESSOR_INPUT_REPLAY_ORIGINAL,
    successor_input_bytes, successor_input_absences, successor_input_registry_original_bytes,
    GENERATED_FIXTURE_PATHS, generated_fixture_absences,
    SUCCESSOR_CALCULUS_MAP, SUCCESSOR_CALCULUS_GUIDES, successor_calculus_map_absences,
    successor_calculus_guide_source_bytes,
    SUCCESSOR_READ_BATCH_PATHS, successor_read_batch_bytes, successor_read_batch_absences,
    FIRST50_ASSURANCE_PATHS, first50_assurance_absences,
    SUCCESSOR_REMAINDER_BATCH_PATHS, successor_remainder_batch_bytes, successor_remainder_batch_absences,
    binding_record_candidate, is_binding_record, binding_record_bytes, binding_record_absences,
    status_record_candidate, status_record_absences, STATUS_RECORD_OWNERS, status_owner_edition,
)


ROLES = {
    "manuscript", "research-note", "component", "composite-reference",
    "preserved-edition", "source-substrate", "synthesis", "review",
    "supporting-reference", "application-proposal", "research-software",
}
PROBES = {"recognition-correction", "tensor-geometry", "cross-avenue"}


def safe_path(repo, rel):
    if not isinstance(rel, str) or not rel or "\\" in rel:
        raise ValueError("Expected a nonempty repository-relative path")
    parts = rel.split("/")
    if any(p in ("", ".", "..", ".git") for p in parts) or ":" in parts[0]:
        raise ValueError("Unsafe repository-relative path")
    node = repo
    for part in parts:
        node = node / part
        if node.is_symlink():
            raise ValueError("A source path contains a symlink")
    if not node.is_file():
        raise ValueError("Source is missing or not a regular file")
    return node


def entries_at(repo, commit):
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise ValueError("An exact full commit object ID is required")
    def git(*args):
        p = subprocess.run(["git", *args], cwd=repo, capture_output=True, check=False)
        if p.returncode:
            raise ValueError("Required pinned Git objects are unavailable")
        return p.stdout
    if git("rev-parse", "--verify", commit + "^{commit}").decode().strip() != commit:
        raise ValueError("Expected a commit identity")
    rows = []
    for raw in git("ls-tree", "-r", "-l", "-z", "--full-tree", commit).split(b"\0"):
        if not raw:
            continue
        meta, path = raw.split(b"\t", 1)
        mode, kind, oid, size = meta.decode("ascii").split()
        rows.append({"path": path.decode("utf-8"), "mode": mode, "kind": kind,
                     "git_oid": oid, "bytes": None if size == "-" else int(size)})
    rows.sort(key=lambda row: row["path"])
    return rows


def matches(path, selectors):
    return any(path.startswith(s) if s.endswith("/") else path == s for s in selectors)



DISPOSITION_ROLES = {"work-source", "historical-edition", "formal-component",
                     "executable-component", "test-fixture", "provenance-record",
                     "reference-material", "collection-guide", "integration-adapter"}


def check_collection_dispositions(rows, owners, cross):
    """Check explicit editorial roles against the independent frozen denominator.

    A disposition is not a reading receipt, scientific result, or acceptance.
    Support paths retain their exact Git identity through baseline/path; hashes
    and descriptions are not copied into another scientific source registry.
    """
    errors = []
    groups = {g["key"]: g for g in owners.get("collections", [])}
    declared = cross.get("collection_dispositions", {})
    if not isinstance(declared, dict):
        return ["collection-coverage: malformed collection dispositions"]
    works = {w["key"] for w in cross.get("works", [])}
    sources = cross.get("sources", {})
    required_groups = set(owners.get("disposition_required_groups", []))
    if cross.get("coverage_stage") == "reader-candidate":
        required_groups.update(groups)
    for required in sorted(required_groups):
        if required not in declared:
            errors.append("collection-missing: " + required)
    primary_paths = set(owners.get("required_work_sources", []))
    primary_works, work_paths = {}, {}
    if any(isinstance(record, dict) and "supporting_population" in record
           for record in declared.values()):
        for work in cross.get("works", []):
            keys, forms = work.get("source_keys", []), work.get("reading_forms", [])
            supporting = work.get("supporting_source_keys", [])
            if any(not isinstance(refs, list) for refs in (keys, forms, supporting)):
                errors.append("collection-source: malformed source references " + str(work.get("key")))
                continue
            keys = keys + [form.get("source") if isinstance(form, dict) else None for form in forms]
            for references, primary in ((keys, True), (supporting, False)):
                for key in references:
                    source = sources.get(key) if isinstance(key, str) else None
                    if (not isinstance(source, dict) or not isinstance(source.get("path"), str)
                            or not source["path"]):
                        errors.append("collection-source: undefined source " + str(key))
                        continue
                    work_paths.setdefault(work["key"], set()).add(source["path"])
                    if primary:
                        primary_paths.add(source["path"])
                        primary_works.setdefault(source["path"], set()).add(work["key"])
    for name, record in declared.items():
        if name not in groups or not isinstance(record, dict):
            errors.append("collection-coverage: unknown or malformed group " + str(name))
            continue
        g = groups[name]
        expected = {r["path"] for r in rows if matches(r["path"], g["include"])
                    and not matches(r["path"], g.get("exclude", []))}
        items = record.get("items", [])
        if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
            errors.append("collection-coverage: malformed items " + name)
            continue
        paths = [i.get("path") for i in items]
        if any(not isinstance(path, str) or not path for path in paths):
            errors.append("collection-coverage: malformed item paths " + name)
            continue
        if len(paths) != len(set(paths)):
            errors.append("collection-duplicate: " + name)
        if "supporting_population" in record:
            # Only residual support/history is implicit. Sources and reading
            # forms stay explicit even when their work spans several groups.
            required = {path for path in primary_paths if matches(path, g["include"])
                        and not matches(path, g.get("exclude", []))}
            if set(paths) - expected or required - set(paths):
                errors.append("collection-coverage: " + name + " has extra paths or omitted work sources")
            primary_roles = {"work-source", "historical-edition", "formal-component",
                             "executable-component", "collection-guide"}
            for item in items:
                if item["path"] in required:
                    if (not isinstance(item.get("work"), str)
                            or item["work"] not in primary_works.get(item["path"], set())):
                        errors.append("collection-work: " + item["path"] + " is not bound to its declared work")
                    if not isinstance(item.get("role"), str) or item["role"] not in primary_roles:
                        errors.append("collection-role: " + item["path"] + " needs a primary or component role")
            support = record["supporting_population"]
            if not isinstance(support, dict):
                errors.append("collection-coverage: malformed supporting population " + name)
            else:
                has_destination = False
                if "work_keys" in support:
                    work_keys = support["work_keys"]
                    related_works = {key for key, paths in work_paths.items() if paths & expected}
                    if (not isinstance(work_keys, list) or not work_keys
                            or any(not isinstance(key, str) or key not in related_works for key in work_keys)
                            or len(work_keys) != len(set(work_keys))):
                        errors.append("collection-work: invalid or unrelated supporting population " + name)
                    else:
                        has_destination = True
                if "owner_paths" in support:
                    owner_paths = support["owner_paths"]
                    if (not isinstance(owner_paths, list) or not owner_paths
                            or any(not isinstance(path, str) or path not in g.get("owners", [])
                                   for path in owner_paths)
                            or len(owner_paths) != len(set(owner_paths))):
                        errors.append("collection-owner: invalid supporting population " + name)
                    else:
                        has_destination = True
                if not has_destination:
                    errors.append("collection-coverage: " + name + " lacks a work or owner support destination")
                roles = support.get("roles")
                support_roles = DISPOSITION_ROLES - {"work-source", "historical-edition"}
                if (not isinstance(roles, list) or not roles
                        or any(not isinstance(role, str) or role not in support_roles for role in roles)
                        or len(roles) != len(set(roles))):
                    errors.append("collection-role: invalid supporting population " + name)
                scope_note = support.get("scope_note")
                if not isinstance(scope_note, str) or not scope_note.strip():
                    errors.append("collection-coverage: " + name + " lacks supporting population scope")
        elif set(paths) != expected:
            errors.append("collection-coverage: " + name + " has missing or extra paths")
        if not record.get("scope") or not record.get("reading_record"):
            errors.append("collection-coverage: " + name + " lacks scope/reading record")
        basis = record.get("basis_sources", [])
        if (not isinstance(basis, list) or not basis
                or any(not isinstance(key, str) or key not in sources for key in basis)):
            errors.append("collection-coverage: " + name + " lacks source-owner basis")
        elif "supporting_population" in record and any(
                not isinstance(sources[key], dict) or sources[key].get("path") not in g.get("owners", [])
                for key in basis):
            errors.append("collection-coverage: " + name + " basis must name actual collection owners")
        for item in items:
            if not isinstance(item.get("role"), str) or item["role"] not in DISPOSITION_ROLES:
                errors.append("collection-role: " + str(item.get("path")))
            if not isinstance(item.get("work"), str) or item["work"] not in works:
                errors.append("collection-work: " + str(item.get("path")))
    return errors



def check_collection_result_routes(repo, owners, cross):
    """Resolve editorial work routes against the collection's actual result owner.

    No theorem extraction, new scientific identifiers, copied claims or copied
    verdicts. A public result's explicit availability/reference route can remain
    useful without inventing a missing original source body.
    """
    errors = []
    work_ids = {w["key"] for w in cross.get("works", [])}
    records = cross.get("collection_dispositions", {})
    if not isinstance(records, dict):
        return ["result-routes: malformed collection dispositions"]
    for group in owners.get("collections", []):
        owner_path = group.get("result_owner")
        if not owner_path:
            continue
        record = records.get(group["key"], {})
        if (owner_path not in group.get("owners", [])
                or record.get("result_owner") != owner_path):
            errors.append("result-owner: " + group["key"])
            continue
        try:
            original = json.loads(safe_path(Path(repo), owner_path).read_text(),
                                  object_pairs_hook=unique_object)
            rows = original["results"]
            ids = [r["id"] for r in rows]
            if not ids or len(ids) != len(set(ids)):
                raise ValueError("empty or duplicate original result IDs")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("result-owner: " + group["key"] + ": " + str(exc))
            continue
        routes = record.get("result_routes", {})
        if not isinstance(routes, dict) or set(routes) != set(ids):
            errors.append("result-routes: " + group["key"] + " omitted or invented a result ID")
            continue
        for result_id, destinations in routes.items():
            if (not isinstance(destinations, list) or not destinations
                    or any(not isinstance(w, str) or w not in work_ids for w in destinations)
                    or len(destinations) != len(set(destinations))):
                errors.append("result-work: " + result_id)
    return errors


def permitted_reader_ci_addition(repo, row, body):
    """Admit only the finite reviewed operational CI forms.

    Every original workflow byte, gate and permission must survive. This
    narrowly scoped operational change is not a free-form hash exemption.
    """
    if row["path"] != ".github/workflows/validate.yml":
        return False
    original = subprocess.run(["git", "cat-file", "blob", row["git_oid"]],
                              cwd=repo, capture_output=True, check=False)
    if original.returncode:
        return False
    anchor = b"      - name: T20 v6 independent public projection and source boundaries\n"
    addition = (
        b"      - name: Reader pilot source, edition and navigation controls (not semantic acceptance)\n"
        b"        run: |\n"
        b"          python -B tests/test_reader_census.py\n"
        b"          python -B -O tests/test_reader_census.py\n"
        b"          python -B tests/test_reader_pilot.py\n"
        b"          python -B -O tests/test_reader_pilot.py\n"
        b"          python -B scripts/check_reader_pilot.py\n"
    )
    before = original.stdout
    if before.count(anchor) != 1 or addition in before:
        return False
    reader_candidate = before.replace(anchor, addition + anchor, 1)
    if body == reader_candidate:
        return True
    # The hosted absence increment has its own finite, independently reviewed
    # transaction and evidence boundary. Every original workflow byte and the
    # complete earlier reader block must survive this second exact insertion.
    absence_anchor = b"      - name: Dependency lock consistency\n"
    absence_addition = (
        b"      - name: Source-alias admission and evidence controls\n"
        b"        env:\n"
        b"          PYTHONPATH: scripts\n"
        b"          PYTHONDONTWRITEBYTECODE: \"1\"\n"
        b"        run: |\n"
        b"          python -B tests/test_source_alias_absence_population.py\n"
        b"          python -B tests/test_source_alias_absence_boundary.py\n"
        b"          python -B tests/test_source_alias_absence_evidence.py\n"
        b"      - name: Combined public source-alias absence and exact restoration\n"
        b"        id: source_alias_absence\n"
        b"        if: github.event_name == 'pull_request'\n"
        b"        env:\n"
        b"          PYTHONDONTWRITEBYTECODE: \"1\"\n"
        b"        run: setsid --wait python -B scripts/check_source_alias_absence.py run\n"
        b"      - name: Receive bounded source-alias evidence\n"
        b"        if: ${{ always() && github.event_name == 'pull_request' && steps.source_alias_absence.outcome != 'skipped' }}\n"
        b"        env:\n"
        b"          PYTHONDONTWRITEBYTECODE: \"1\"\n"
        b"        run: python -B scripts/check_source_alias_absence.py export\n"
        b"      - name: Preserve bounded source-alias evidence\n"
        b"        if: ${{ always() && github.event_name == 'pull_request' && steps.source_alias_absence.outcome != 'skipped' }}\n"
        b"        uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2\n"
        b"        with:\n"
        b"          name: r0002-source-alias-evidence-${{ github.run_id }}-${{ github.run_attempt }}\n"
        b"          path: ${{ runner.temp }}/r0002-source-alias-receipts/\n"
        b"          if-no-files-found: error\n"
        b"          include-hidden-files: false\n"
        b"          archive: true\n"
    )
    if reader_candidate.count(absence_anchor) != 1 or absence_addition in reader_candidate:
        return False
    absence_candidate = reader_candidate.replace(absence_anchor, absence_addition + absence_anchor, 1)
    if body == absence_candidate:
        return True
    # Public123 follows the complete earlier absence transaction. Its success
    # dependency, process wait, state, export and upload guards stay exact.
    public123_addition = (
        b'      - name: Public123 generated-source absence and exact restoration\n'
        b'        id: public_fixture123\n'
        b"        if: ${{ github.event_name == 'pull_request' && steps.source_alias_absence.outcome == 'success' }}\n"
        b'        env:\n'
        b'          PYTHONDONTWRITEBYTECODE: "1"\n'
        b'        run: setsid --wait python -B scripts/check_source_alias_absence.py run-fixtures --state "$RUNNER_TEMP/r0002-public-fixtures123-absence"\n'
        b'      - name: Receive bounded public123 evidence\n'
        b"        if: ${{ always() && github.event_name == 'pull_request' && steps.public_fixture123.outcome != 'skipped' }}\n"
        b'        env:\n'
        b'          PYTHONDONTWRITEBYTECODE: "1"\n'
        b'        run: python -B scripts/check_source_alias_absence.py export-fixtures --state "$RUNNER_TEMP/r0002-public-fixtures123-absence"\n'
        b'      - name: Preserve bounded public123 evidence\n'
        b"        if: ${{ always() && github.event_name == 'pull_request' && steps.public_fixture123.outcome != 'skipped' }}\n"
        b'        uses: actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9 # v7.0.2\n'
        b'        with:\n'
        b'          name: r0002-public-fixtures123-evidence-${{ github.run_id }}-${{ github.run_attempt }}\n'
        b'          path: ${{ runner.temp }}/r0002-public-fixtures123-receipts/\n'
        b'          if-no-files-found: error\n'
        b'          include-hidden-files: false\n'
        b'          archive: true\n'
    )
    if public123_addition in reader_candidate:
        return False
    public123_candidate = reader_candidate.replace(
        absence_anchor, absence_addition + public123_addition + absence_anchor, 1)
    if body == public123_candidate:
        return True
    # The reviewed resource correction is a paired replacement inside that
    # exact admission step, not permission for arbitrary workflow edits.
    resource_addition = absence_addition
    for family in (b"boundary", b"evidence"):
        plain = b"          python -B tests/test_source_alias_absence_" + family + b".py\n"
        qualified = (b'          PUBLIC123_REVISION_RESOURCES="$(mktemp -d '
                     b'"$RUNNER_TEMP/r0002-public123-' + family + b'.XXXXXX")" '
                     b"python -B tests/test_source_alias_absence_" + family + b".py\n")
        if resource_addition.count(plain) != 1:
            return False
        resource_addition = resource_addition.replace(plain, qualified, 1)
    resource_candidate = reader_candidate.replace(
        absence_anchor, resource_addition + public123_addition + absence_anchor, 1)
    if body == resource_candidate:
        return True
    # These two original receipt controls run early in both interpreter modes.
    # The complete previous workflow remains the exact prefix/insertion owner.
    continuation_anchor = b"      - name: Combined public source-alias absence and exact restoration\n"
    continuation_addition = (
        b'      - name: Previously failed continuation receipt controls\n'
        b'        env:\n'
        b'          PYTHONDONTWRITEBYTECODE: "1"\n'
        b'        run: |\n'
        b'          python -B tests/test_research_continuations.py ActualEvidenceAssociationTests.test_array_receipt_has_descriptive_validation_failure ActualEvidenceAssociationTests.test_qualified_original_controls_require_provenance\n'
        b'          python -B -O tests/test_research_continuations.py ActualEvidenceAssociationTests.test_array_receipt_has_descriptive_validation_failure ActualEvidenceAssociationTests.test_qualified_original_controls_require_provenance\n'
    )
    if resource_candidate.count(continuation_anchor) != 1 or continuation_addition in resource_candidate:
        return False
    return body == resource_candidate.replace(
        continuation_anchor, continuation_addition + continuation_anchor, 1)



CONTRIBUTOR_NAVIGATION_MARKER = b"\n<!-- reader-maintenance:issue-35 -->\n"


def permitted_contributor_navigation(repo, row, body):
    """Admit appended reader maintenance, never a change to inherited policy.

    CONTRIBUTING is a discovery owner. Its original bytes remain a prefix and
    its added section has an explicit boundary; this is not a hash refresh or
    a directory-wide owner exemption. Root route checks qualify the links.
    """
    if row["path"] != "CONTRIBUTING.md":
        return False
    original = subprocess.run(["git", "cat-file", "blob", row["git_oid"]],
                              cwd=repo, capture_output=True, check=False)
    if original.returncode:
        return False
    before = original.stdout
    return (body.startswith(before + CONTRIBUTOR_NAVIGATION_MARKER)
            and body.count(CONTRIBUTOR_NAVIGATION_MARKER) == 1
            and b"\n## Reader maintenance\n" in body[len(before):])


PMR007_ROUNDS_PARENT = "docs/project-closure/ar8r-v11/post-merge-proposals/README.md"
PMR007_ROUNDS_PARENT_REVISION = "a7ff0e33d1a299db640041c46b1af81ca70851f6"


def pmr007_rounds_parent_source_bytes(repo):
    """Authenticate one current custody adaptation and return its original source.

    This does not admit a missing snapshot member. The existing finite snapshot
    and formalization gates own that decision. Original directory wording is
    valid only while the corresponding current/index edition remains present.
    """
    repo = Path(repo)
    path = PMR007_ROUNDS_PARENT
    revision = PMR007_ROUNDS_PARENT_REVISION
    blob = "9628152cf22670418bc2c88aa13e496047fba40c"
    identity = "d20707cf0d24dd5b2b966f2b1f3640ec7672092ef8a19b57f60fc61897cd6b50"
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("rounds parent requires its exact original revision")

    def git(*args):
        result = subprocess.run(
            ["git", "--no-replace-objects", "--literal-pathspecs", "-c", "core.fsmonitor=false", *args],
            cwd=repo, capture_output=True, check=False,
            env=dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0"))
        if result.returncode:
            raise ValueError("rounds parent original or staged Git objects unavailable")
        return result.stdout

    expected = ("100644 blob " + blob + "\t" + path + "\0").encode()
    if (git("cat-file", "-t", revision) != b"commit\n"
            or git("ls-tree", "-z", revision, "--", path) != expected):
        raise ValueError("rounds parent original path, blob or mode differs")
    original = git("cat-file", "blob", blob)
    original_blob = hashlib.sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest()
    if (len(original), hashlib.sha256(original).hexdigest(), original_blob) != (4073, identity, blob):
        raise ValueError("rounds parent original source identity differs")
    old = (
        b"The `pmr007-rounds11-20` directory is an exact, public-safe copy of the final sanitized "
        b"repository-update proposal recovered from the authenticated research thread. Its internal "
        b"files are preserved without correction so their original hashes remain testable."
    )
    new = (
        b"The original `pmr007-rounds11-20` import is the exact, public-safe copy of the final sanitized "
        b"repository-update proposal recovered from the authenticated research thread. Its complete "
        b"131-file edition is retained at Git commit `a7ff0e33d1a299db640041c46b1af81ca70851f6`. "
        b"The current snapshot preserves its unchanged 130-row hash manifest and requires its 32 "
        b"distinct or context-dependent members; 98 exact same-relative copies may resolve through "
        b"`pmr007-deep-a-bk` under the finite snapshot gate. The existing rounds adoption-boundary "
        b"correction records those current routes and their limits; original source bytes and hashes "
        b"remain testable."
    )
    if original.count(old) != 1:
        raise ValueError("rounds parent original paragraph count differs")
    adapted = original.replace(old, new, 1)
    current_path = safe_path(repo, path)
    current = current_path.read_bytes()
    if current_path.stat().st_mode & 0o111 or current not in (original, adapted):
        raise ValueError("rounds parent is not its exact ordinary navigation adaptation")
    adapted_blob = hashlib.sha1(b"blob " + str(len(adapted)).encode() + b"\0" + adapted).hexdigest()
    indexed = git("ls-files", "--stage", "-z", "--", path)
    choices = {("100644 " + oid + " 0\t" + path + "\0").encode(): body
               for oid, body in ((blob, original), (adapted_blob, adapted))}
    if indexed not in choices:
        raise ValueError("rounds parent index is missing, conflicted or has an unqualified edition/mode")
    if git("cat-file", "blob", indexed.split()[1].decode()) != choices[indexed]:
        raise ValueError("rounds parent staged object identity differs")

    # Presence metadata only: original wording may not describe an incomplete
    # edition as an exact current directory. This grants no absence fallback.
    members = [row for row in git("ls-tree", "-r", "-z", revision, "--", PMR007_ROUNDS_PREFIX).split(b"\0") if row]
    if len(members) != 131:
        raise ValueError("rounds parent original edition membership differs")
    original_stages = set()
    complete_worktree = True
    for row in members:
        metadata, member = row.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        member = member.decode("utf-8")
        if (mode != "100644" or kind != "blob" or not re.fullmatch(r"[0-9a-f]{40}", oid)
                or not member.startswith(PMR007_ROUNDS_PREFIX + "/")):
            raise ValueError("rounds parent original edition metadata differs")
        original_stages.add((mode + " " + oid + " 0\t" + member).encode())
        try:
            node = safe_path(repo, member)
            complete_worktree = complete_worktree and not node.stat().st_mode & 0o111
        except (ValueError, OSError):
            complete_worktree = False
    staged_members = set(git("ls-files", "--stage", "-z", "--", PMR007_ROUNDS_PREFIX).split(b"\0"))
    if not complete_worktree and current != adapted:
        raise ValueError("rounds parent current wording requires its complete original edition")
    if not original_stages.issubset(staged_members) and choices[indexed] != adapted:
        raise ValueError("rounds parent staged wording requires its complete original edition")
    return original



# Exact original and independently reviewed public fixture-consumer editions.
# These bindings change no source/public identity or scientific disposition.
FIXTURE_CONSUMER_REVISION = "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c"
FIXTURE_STATUS_PATH = "experiments/experiment-status.yaml"
FIXTURE_CONSUMER_ORIGINAL = {'experiments/episode-reification-v2/README.md': ('62c5a4b3b4af1d0860a0d9b6184a0f5604670836',
                                                  'cf660c095bf11d03bec1f13d36eaf994226b63329dbd53f31a714d7899767da4',
                                                  1561),
 'experiments/episode-reification-v2/analysis/analyze_er2.py': ('2addf30dab7b3b6f4f094a37250bd11f50718cc2',
                                                                '448d7f598916a94855dd6e1060361f7686240ab542caef1a44b8fb9637026f3b',
                                                                10418),
 'experiments/episode-reification-v2/harness/run_er.py': ('c4fa618a88160e0b4da89644abb3e9a49d49626a',
                                                          'bd84fdfa3d8973b39f04a9dc0014f3dc1b5574caf61ed7643ca78ae782455d20',
                                                          7347),
 'experiments/episode-reification-v2/scripts/generate_cases.py': ('7eab184f0ff3cdc4869600528ceae1665865e9b8',
                                                                  'd4ae498ed5b992ec366a752300a949ba64a3d90ce01c63c28392dacbe9827aa3',
                                                                  8526),
 'experiments/episode-reification-v2/tests/test_smoke.py': ('4da6e02cdf9777b74afa2f6a2d19f236d8a9ccab',
                                                            '41517fa67f0998e92ccbaff09843bac86b20a7144a9c7016927fb4bc4d6f412f',
                                                            8543),
 'experiments/episode-reification/README.md': ('28f48c3f8ef3c56bca366fbf6fac0b9bf54a4f40',
                                               'ca21e76e775fe1637098aa90b6e6544fa732ef4a82c874de5aab6cbf6f4451b6',
                                               1197),
 'experiments/episode-reification/scripts/generate_fixtures.py': ('2d971fd8c236334a9a2069e48cc53333d141b7c1',
                                                                  '7ce757842bf2e9fa87a23004675d147687009b1a84a4cf3fc08908f227d45564',
                                                                  8187),
 'experiments/episode-reification/tests/test_smoke.py': ('9c74297fd87351299f1223624d8b8e50c76ffd45',
                                                         '3606f98b6f2072c5a39fbb24e3d4728b4e9b047b82c65f7d4b8187ef3d010c1c',
                                                         5936),
 'experiments/experiment-status.yaml': ('eb979d8fd40710cbe9adeabd1c76c3571c4f22d6',
                                        '88e59fdfc9e1e4a3ab751fef6e2f6bc1c5a644fc5863bf679b35c2ceb56cf2b2',
                                        6886),
 'scripts/generate_current_state.py': ('84429a260b6084fce35dd0934a9fd6c72efc3a09',
                                       'a64b60308dd916505e0e10ce585e3e08c5f20172560b0c1e7deda0e086e830de',
                                       8057),
 'scripts/validate_experiment_readiness.py': ('dcb5c2a61e443a8d704b8e9516c1abe444ade712',
                                              '3c7db3b6a05c9c21a1ef255f083b24842ddebee0512ea61a4a074d9c88f1346b',
                                              10208),
 'scripts/validate_negative_fixtures.py': ('5521fbfea42ff7e20a85fdd8c31ee4b85d1bdfc5',
                                           '6631cc99253d14a78b91022b95b646dba48bae1f34a0b86390fbd3e4dd85d92b',
                                           7429),
 'tests/schema-negative/NEGATIVE-FIXTURES.json': ('a002ee8e159a7678e6c704323ca62670cc389880',
                                                  'b342240297511473b5c5568d4662de413d1f69fef20a7a55dc59c24657e7580b',
                                                  10709)}
FIXTURE_CONSUMER_CURRENT = {'experiments/episode-reification-v2/README.md': ('c183888b63c7e73b6a17fb4f1c398906eca3f317',
                                                  '7ea04abc91a0964525d1257181dc08f4e412d4780b1f2b32e0f09179edaf40eb',
                                                  2405),
 'experiments/episode-reification-v2/analysis/analyze_er2.py': ('b44531cd3eb4e4530d5d6ca733b0fecff51ad8a1',
                                                                '0a9b691158bdd5d9590ca50f5501dbe9057880e7720b16df1a40cd5923da11a2',
                                                                11120),
 'experiments/episode-reification-v2/harness/run_er.py': ('e10f76b5412c6a793deaff17aa68fc0068444700',
                                                          '15af564935d25d8d43a6007d88377cbea76d785437dffaf1260ef57a305d7666',
                                                          7263),
 'experiments/episode-reification-v2/scripts/generate_cases.py': ('e43f016e6a12594c29deef253cf1ba65d86462be',
                                                                  '3b449a7580426fdf89f85612018473f92c3c2c274d4eea47e7046d1bcfe1bc89',
                                                                  9631),
 'experiments/episode-reification-v2/tests/test_smoke.py': ('2e143f2c2d07f1683c6ec86b08529c085c979973',
                                                            '65d2195b2723b00fb750f14b5487f6b267aa0132400eac96cdf2a1baac819dab',
                                                            9060),
 'experiments/episode-reification/README.md': ('2732cd09c8895c22b5fbce4b00a326826da6cb19',
                                               'e27914d286579b38c1ad480618498dd8968d85464c06b7f6e26b73577e823bc7',
                                               1900),
 'experiments/episode-reification/scripts/generate_fixtures.py': ('be7dd10d2f60ad16c4cf9df2ea3316d778b0c8fc',
                                                                  '9c39be153165e8d1c5a074243fc5f4ba467862ccc0d433bb42e7471230e4b929',
                                                                  8675),
 'experiments/episode-reification/tests/test_smoke.py': ('c92237319812ec5adb1f3de28dc692efcdf13018',
                                                         '8678c6b1e7c5287e153503441ad825f618bb65fb3311d827199e4da509e9b2ad',
                                                         6005),
 'experiments/experiment-status.yaml': ('e1b4fb336a5ed3a7c890c0e50697364f965574dc', 'c52451c812bb17a8599b82adcb46944d728ba412fb4e845629ac9eece443e7bd', 8344),
 'scripts/generate_current_state.py': ('121d31f0ca3d2b8821c4cd1252b1831b8348b53c',
                                       '49c28230be2def0930c1e71ee117adc2b3a36260aa3369dd3f9f7b8cec2a084d',
                                       8007),
 'scripts/validate_experiment_readiness.py': ('80ca472586848f9aeee28771a2f40e07083fc556', '263222ca3869d0dd13abcf2324619e65977024f0490e309313848e2838cfcc32', 18037),
 'scripts/validate_negative_fixtures.py': ('5c64a4cffa037eb604d519033181c88539e7d78b',
                                           '8e3ff766e20c981628a19fc5d809343a873bfce773885af6197d972a335ea321',
                                           9037),
 'tests/schema-negative/NEGATIVE-FIXTURES.json': ('20b6e5801823e87db6b5fb1638d0e3992eee36e6',
                                                  'b229103cc93bb15d046cb15a1794d99d0cb40200fbc8fe9ac7ceff358c88d3e9',
                                                  108213)}


def check_fixture_consumer_edition(repo, baseline_rows=None):
    """Authenticate one complete thirteen-owner edition and its old status view.

    The current public consumers are distinct from their original T20 evidence.
    An exact historical status body serves the original discovery/crosswalk role
    only after every staged and present successor has independently bound bytes.
    No missing, executable, symlinked, hardlinked or mixed edition is admitted.
    """
    repo = Path(repo)
    paths = sorted(FIXTURE_CONSUMER_ORIGINAL)
    if baseline_rows is not None and not set(paths).intersection(baseline_rows):
        return {}, None, []
    try:
        if baseline_rows is not None:
            for path in paths:
                blob, _, size = FIXTURE_CONSUMER_ORIGINAL[path]
                row = baseline_rows.get(path, {})
                if (row.get('kind'), row.get('mode'), row.get('git_oid'), row.get('bytes')) != (
                        'blob', '100644', blob, size):
                    raise ValueError('original fixture-consumer census differs: ' + path)
        command = ['git', '--no-replace-objects', '--literal-pathspecs',
                   'ls-files', '--stage', '-z', '--', *paths]
        staged = subprocess.run(command, cwd=repo, capture_output=True, check=False)
        if staged.returncode:
            raise ValueError('could not inspect staged fixture consumers')
        edition = None
        for candidate in (FIXTURE_CONSUMER_ORIGINAL, FIXTURE_CONSUMER_CURRENT):
            expected = b''.join(('100644 ' + candidate[path][0] + ' 0\t' + path + '\0').encode()
                                for path in paths)
            if staged.stdout == expected:
                edition = candidate
                break
        if edition is None:
            raise ValueError('staged fixture consumers are not one complete admitted edition')
        for ancestor in (repo, *repo.parents):
            if ancestor.is_symlink():
                raise ValueError('fixture consumer root contains a symlink')
        for path in paths:
            blob, identity, size = edition[path]
            node = safe_path(repo, path)
            fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as stream:
                start = os.fstat(stream.fileno())
                if (not stat.S_ISREG(start.st_mode) or start.st_nlink != 1
                        or start.st_mode & 0o111 or start.st_size != size):
                    raise ValueError('fixture consumer is not an ordinary exact-sized file: ' + path)
                body = stream.read()
                finish = os.fstat(stream.fileno())
            fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
            if any(getattr(start, field) != getattr(finish, field) for field in fields):
                raise ValueError('fixture consumer changed during its read: ' + path)
            oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            if (oid, hashlib.sha256(body).hexdigest(), len(body)) != (blob, identity, size):
                raise ValueError('present and staged fixture consumer editions differ: ' + path)
        repeated = subprocess.run(command, cwd=repo, capture_output=True, check=False)
        if repeated.returncode or repeated.stdout != staged.stdout:
            raise ValueError('fixture consumer index changed during qualification')
        if edition is FIXTURE_CONSUMER_ORIGINAL:
            return {}, None, []
        blob, identity, size = FIXTURE_CONSUMER_ORIGINAL[FIXTURE_STATUS_PATH]
        tree = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs',
            'ls-tree', '-z', FIXTURE_CONSUMER_REVISION, '--', FIXTURE_STATUS_PATH],
            cwd=repo, capture_output=True, check=False)
        original = subprocess.run(['git', '--no-replace-objects', 'cat-file', 'blob',
            FIXTURE_CONSUMER_REVISION + ':' + FIXTURE_STATUS_PATH],
            cwd=repo, capture_output=True, check=False)
        if (tree.returncode or original.returncode
                or tree.stdout != ('100644 blob ' + blob + '\t' + FIXTURE_STATUS_PATH + '\0').encode()
                or (hashlib.sha1(b'blob ' + str(len(original.stdout)).encode() + b'\0' + original.stdout).hexdigest(),
                    hashlib.sha256(original.stdout).hexdigest(), len(original.stdout)) != (blob, identity, size)):
            raise ValueError('original experiment-status evidence is unavailable or differs')
        owners = {path: {'path': path, 'kind': 'blob', 'mode': '100644',
                        'git_oid': edition[path][0], 'bytes': edition[path][2]} for path in paths}
        return owners, original.stdout, []
    except (ValueError, OSError) as exc:
        return {}, None, ['fixture-consumer: ' + str(exc)]


def _permitted_projection_consumer_pins(original, candidate):
    """Admit only complete previously reviewed coordinate migrations."""
    from copy import deepcopy
    import validate_v5_successors as owners
    earlier = {
        path: (*HISTORICAL_PROSE[path], HISTORICAL_PROSE_REVISIONS[path])
        for path in PUBLIC_READER_NOTE_PATHS}
    earlier[CONTINUATION_REGISTRY_PATH] = (
        *owners.PRESERVATION_OWNER_ORIGINAL[CONTINUATION_REGISTRY_PATH],
        CONTINUATION_REGISTRY_REVISION)
    next24 = {
        path: (*HISTORICAL_PROSE[path], HISTORICAL_PROSE_REVISIONS[path])
        for path in NEXT24_PUBLIC_PROSE}
    fixtures = {path: (*binding, FIXTURE_CONSUMER_REVISION)
                for path, binding in FIXTURE_CONSUMER_ORIGINAL.items()}
    combined = dict(earlier, **next24)
    replay_input = {'scripts/replay_v5_successors.py': SUCCESSOR_INPUT_REPLAY_ORIGINAL}
    calculus_fixture = {'tests/v5_successor_fixtures.py': (
        'ccf0bd64f34b10f65ed8bd1bdd8a88adcaf03c7f',
        '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
        13030, '69f3f9284f2cb94433958c0669fc9b06a9760fe7')}
    # Reviewed digest176 consumers retain their original T20 evidence.
    # This complete extension changes only revision/blob coordinates.
    digest_consumers = {
        'scripts/validate_ar8r_codex_corpus_synthesis_v14.py': (
            'bf5693e9eaf14f932a7afef314772c5d6cfd19c3',
            'c2153d22937864584ca0310a129cb41badbcbea96e3a2175b53bd1a9a666a626',
            43318, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_external_challenges.py': (
            '814d716588deff5a8f479deafc8e4d7e91e19c58',
            '621c70320e6695ea77d85c7bec7147193d3c3f013bada94ea6bae328a8616c7e',
            9558, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_ar8r_six_lane_v14_intake.py': (
            'd9511107288776ddab58e06e3892bb61f3bd66e9',
            '33de0e6b174499960cc2c521ab5ab5f2f13cb66467247636aa460419073745a3',
            19144, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bk_public_snapshot.py': (
            'b7a701ad73a96d9de760f22778a17f2128eb7799',
            'ba437ce44adf1ab03d1f797a3c5a72f8991b99186a733bdfc2f9574b02d3d4fd',
            20394, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bv_semantic_reissue.py': (
            '06a0f45454a02b7c849682e563f0b1aa98cab963',
            '818230667805e3db999dc52bd22376a4425e58a85f75e561da4ca39acd75e680',
            16337, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'scripts/validate_pmr007_deep_bw_cj_semantic_reissue.py': (
            'cb72e0de65eb40d0bd659e49e2a4b8a46ef197a9',
            '0d75bcefc899d15b2d35377fa15b54c6d12d180a74a506bc9cd84212206c3311',
            19380, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
    }
    # Original public evidence remains pinned while current reviewed owners advance.
    attribution_consumers = {'docs/sourcing/R3-SOURCING-LEDGER.md': ('2ed9e182cb9db7d38d7c56c0f043983c99f8c940',
                                         '2177de55bb84adc24b69dd8551c12893e7f4dd7eae2a5d5d643b372b9236b770',
                                         5421,
                                         '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
 'scripts/validate_review_state.py': ('95087964f175e00c5dc1a628bc83d40377c6b911',
                                      '240dd79778d8fded8744873ddfc298e3206fa120dbe0417b50198983975efff0',
                                      34750,
                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    # One reviewed validator successor retains its exact original public source.
    governance_consumers = {
        'scripts/validate_cross_record_semantics.py':
            ('af71a10aa182f32795e7736c23e0a620073b994a',
             '3b75bca002978c6c47dc5120e9114fc8c601b7f7f6da36bdf061799b899fc1e5',
             45554, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    # The two reviewed frontier live-test owners keep their exact original evidence.
    frontier_test_consumers = {'tests/test_pmr007_deep_bk_public_snapshot.py': ('249a89266da20b19a84131e7b27a0814aaadd54f',
                                                      'fd6dbafefb2eb6b24119c0d94634251df621d30122c246f690cce146ed5c9ce5',
                                                      12480,
                                                      '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
     'tests/test_pmr007_deep_bv_semantic_reissue.py': ('b932096c9490c9e31bfc3f596f2990a4dfd1e8ba',
                                                       '334034b9019f5f27ca2fcac36e568982bda3d7d6e7c2daca40e565d16792a37f',
                                                       9724,
                                                       '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    # The reviewed current intake test preserves its original evidence edition.
    intake_test_consumer = {'tests/test_ar8r_six_lane_v14_intake.py': ('c0b79431bafc486c71a083b3b8afdec0db431236',
                                                '548d4358ca89755bbfd29b2df9a4b6b2b6ca36541cc5994e523198c40ddea26c',
                                                11625,
                                                '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    # The reviewed current Codex test preserves its original evidence edition.
    codex_test_consumer = {'tests/test_ar8r_codex_corpus_synthesis_v14.py': ('b5aa03c18c2e9df149f460955184bec83a6b46a0',
                                                       '7801ae286ca0b8c8c4c1bce7e73aedc9dfb914474d66ea58c029c756ea1ef67e',
                                                       46305,
                                                       '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    # The reviewed BW test preserves its exact original public evidence.
    reissue_test_consumer = {'tests/test_pmr007_deep_bw_cj_semantic_reissue.py': ('a33743bf20cddf6363021f938a1cef2e0e9baf84', '22f0d82eabb228d0d6d0b0c10a5146bf93ca17b6877d34a169cb8986c1f0710e', 6275, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c')}
    central_public = {
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v1_results.json': ('5fd34db7773639f256f3ebec7aed4cbafc1aabac', 'cd83895b3ef8ec0501fe0cb21e37d0c9f3c86b03278e51835e51f1876cf76959', 8832, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v2_results.json': ('673281f18f0b593948d2df7ea7dbb734027b5dd5', '8484e8099295969760ddab0223778b482e260e1eb69a7c0bd2f802e722aa76f6', 2407, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v1_results.json': ('204ad8f25f3217bdd67d50e8330287cd51d0ed66', '780fd0f7bce609988e0e0e92c468b735c5ee2fe04e587ee459a0f740a2c78381', 525, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v2_results.json': ('f44d983d728803f8c2427f95eaaaf6b8c521e7c7', 'c82f11ce9d56c5adfde56942cc0b5b725bf445802139aa3ad151ac6908a01f5c', 565, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v1_failed_results.json': ('785651477832ccbb072cc75af50155b177148a2a', '039a58147dd5aa9ea3b96a050971c67293e97a96a13e361dce3db5e714f196fc', 2799, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v2_results.json': ('1f37d6723ddbd1d13d70c58b550a1e6807e1ad0a', 'bc5c47709a4e783c6d35327215cd8c0c73402a22fd6cebcfb4a554a18aab5646', 2795, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v3_results.json': ('45f0bccbd77cd6ca4af186884b012a8ed968a037', '4bf52e1ff74a0384a6db5645cd44f5b0871f84a083a6b18317283409c652a0d1', 2795, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v1_results.json': ('e1eb7e352c4fe70e59ae0cff91ddeeb04c4cbb4e', 'a5a8b61ed789e0ee3aa3eee2aad28a2da8f16c5e58c3aa61eff9b6e92913f6a6', 408, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v2_results.json': ('b355d3d8ec253779fa4a4998d486d6c11c128a7f', '17d3572cc0866dff23438a8b5cd185d7052456e8dbded683f65dd3304955c5a6', 603, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_distinct_bisimulation_rereview_results.json': ('f89950fa8dea2251d7f2a5c9f98b126e30d07e6b', 'a185c8b2f37dbd743de6abfa2e109a10e125a155e143235498910e6b5f10592f', 1053, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v1_results.json': ('6c6063513181fee22875150d9e36f8b8296bd6f4', '1e3f646e1df4be1c865c2b1a052237196c1db486f77aa7f76c95f1d6409bdc83', 757, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v2_results.json': ('80f42ef3444bc86186c3979c5c9027b274bdd0b1', '430e46e3e718fcbbce9688139b8e7e2418be806f662a2fabd36688ed5eb5ca5b', 740, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_distinct_fibre_cover_rereview_results.json': ('dd4f79acaeb8395d8612d5500305e1df090a7a78', '2384534787c19c7c8a27c7cf59ad32a865a4e25fc18d2918c5a55424d2437c4f', 248, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v1_results.json': ('0adc064cf4b9d7e2b3ba05687f6a48e72d30b98d', '9f9266588d75cbc61b3b763bbd2ff6c1daf04986ef4087e1123ba569d4328d02', 352, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v2_results.json': ('7a2fa6e4e6180ca950b3b44dfdf5f8a3b80588ff', '8808624a3bbb09426f95603981ca84e104f96c977d4dc091913b2a69040040e8', 369, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_distinct_conflict_graph_rereview_results.json': ('1a5e61df2ecc45fd07d6fbc3d07fbb6f244ec42b', 'fa16d66f6c7527eb0164c6f4a1151fb2d0ab8a760159ab1fe62dc71f55b22494', 975, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v1_results.json': ('9a52c8eb568a33e83f9c1a8f6d0e6b71294eb111', '26ed4259faa972bbf56f2691de6085a8b3e9c17ae0bac3899612d5d567e8fd8f', 3882, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v2_results.json': ('488f34eeb82faa575976fcfbee7ab2e7ba4a627f', '3906cf8498d6858014e7112a4238ad6796690dd7c9ffb86e97b66494cdf2946b', 1168, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_CONCRETE_ARCHITECTURE_MAP_V1.yaml': ('ffc8b62232dfc42ce07ea1aa43d8d458f5a4e8d3', 'ebcc532f9981f0d2a25be1e05e83f1d2a240e6c5696518f6a896823f0d030853', 3918, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V1.yaml': ('2a4ec7fecc1bc1c724323d62ecd71dde5ffcea10', '9eae438bebd069f2ada1ab861bda8290c0b44bd2f3ad0202a4093096ef9e7ca4', 2491, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V2.yaml': ('1f81a89d311d51b6aa77c24c7c0b2f371e80af43', '2da6b0cfdde4ea5d5871d17eb3282169df1daf85bcaf4efdf5a14ff982f7738d', 4686, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR-007_DEEP_CL_ADMISSION_OVERLAY.yaml': ('26f53b5f13e3f71a82643d261cc6e1a5f3a593ac', 'ef987bf8670007688841e9ddaa2fc6e85455a67644751b010223801a3a926908', 1390, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V1.yaml': ('f0f12ecc568086ba133836b786dc0cb7b89e5128', '3350c31b6aeae6a13ea23837fb1817fed485f6ad8d11964ba7c22bf6720832bb', 2454, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V2.yaml': ('9d4365ce30e5d4ba08f622ba925429ef58d83431', '27aa21fac900517a75a0cef30fe99e928c4f43c679c407e7db0bc96fc07d3318', 3162, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR-007_DEEP_CM_ADMISSION_OVERLAY.yaml': ('27eaaf7620fa0d9cbb475ef471fb8ab9ec574ef9', '67f7b3d658ea5ace55558ab590fd0c6cfffef95f15bf295f3fc7443bfe49120d', 1473, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V1.yaml': ('da75ddf4e9288e0b788f22837964e14976b6e956', 'da7d7fddfb87dc56eadfd6bcc5a605601ad847aa5ee97263ba2a1a7eecec7160', 2451, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V2.yaml': ('95dc33114b1b10d7926fd13069ef966e5cbb2ca5', 'c564bf8c94d16ac02b089acb320107a7a7502dbe6b638b6fde987d773b0b9023', 2751, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR-007_DEEP_CN_ADMISSION_OVERLAY.yaml': ('07340bd737e98c68b7bd499398c0b14733473a0b', '4964c5c38a109deb4f680a526deb9b80c9169ed485d6e3e6ec3f8c3524b5c916', 1694, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V1.yaml': ('91eac41938d9363f29b2aaa6cc356d3662f2f721', 'b239062074fcd058f173aed1898fbeece56974673b62cccdce97e8c7cf27c6a8', 2363, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V2.yaml': ('4ba04371b0d153e2385e770c892dfe08ca992906', 'd3787af3cf0554f39fb62f630fb3804cda9f985036d22aa1d615b48e6fc4e614', 3891, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR-007_DEEP_CO_ADMISSION_OVERLAY.yaml': ('5d7b3607d263060f8cd27f4b70f78c5ea858b03c', '561bd97f52d5b076668e0b643215fc64378499d44c8fd3f3f491d1b9935858ef', 1518, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V1.yaml': ('d5cccbe6b4b76936a304852cdf64a67f4f0bfab7', '745a3a7e41cc9c452a0be4e76b58468d18add7fe86a229effd0365d5c092d8f6', 1439, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V2.yaml': ('2ba1b3b358e7505354ac44d20e644a44f2bafb1d', '8406e983c4c36d7803c8cec61bd97e4ad70b0bb77b9e485a9a67450b18edf317', 1935, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR-007_DEEP_CP_ADMISSION_OVERLAY.yaml': ('3ff592b02ff973d55d457a5b2a17012333a9260f', '87c4d60944526bcbe32ea002d913fbd374e8633270aa11c5aeede226424c76c5', 1754, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V1.yaml': ('4c90195800538c0f8bab0841bf61c50a0e975e5e', 'ef27f520e22cab9c3d19c70b8a21287f52695770f98980d2fb310d7feb3b584e', 3033, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V2.yaml': ('d9466caca6cf9213595bdfa489d413251fba67b6', 'a1498322eb840c7cb9d88e4c65d0503ac264da961d96d93fe34d589d52e3e42f', 4084, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR-007_DEEP_CQ_ADMISSION_OVERLAY.yaml': ('4037fcd491eba593dadbaab5a89a3fdca61319ca', '70609844141c6fe0f177ea9f0c0078c1f204f0f49e81975dde97940d94403183', 1968, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V1.yaml': ('45b7c1b3e61ab2616702ae6a291e582f10d3d74c', 'e246434684eaa9e6b5c2e203c1dd5dd6dc7cd0f6aa00cb69f34f178f05823910', 2755, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V2.yaml': ('dd3ecc53b8c02865acce709205babe160a241c5d', '258e982a41350546b4bba775088b10cc1a1fc9ca8dbb07be548ddbab85158679', 3383, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V1.yaml': ('dd2ec65d7b6bb9732b022cf3ffe9afc06b7af68a', '207dcc4f28697598805b7242776bd8ca0c539111b2fff25eb0f6d3bd999b5c44', 1340, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V2.yaml': ('e2a37b6a0c1e1584ac209eb8bf0432a13f7d60d9', '7e0ce54a6a3f1fb53e816ba8019314ed7bf037803e340ebac69da34b868b50ba', 2515, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR-007_DEEP_CS_ADMISSION_OVERLAY.yaml': ('13b662a5c995a191670c7394335f08ea2fbd4d0a', 'fc35f95ca8d802f6191898806961ec1e4dcac0ba9d535253387bc564b8e86ffa', 928, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V1.yaml': ('188a4d22366041568a9d3b34816159763176247c', '1aff4e8f6e17bc8625cecbce36ce60b18a60aaedd25872b509f6496d811eb84b', 738, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V2.yaml': ('13d956d17c456cc4e05c5f4206cd14fe1c99a9dc', 'cbb0e891acd1bd80b5bfeb12951eb92cb63294a37f796ce814aae4f8efe2444f', 1319, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR-007_DEEP_CT_ADMISSION_OVERLAY.yaml': ('b4f5b958c6b25087f1d7d934d5700bf85bb3b905', '412593543dd7a13ddf77da5c780125b3b9d47b480176949d5ddc63672050da51', 1127, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V1.yaml': ('f364375dc4acb7bc750c01f112af1fd4253a1aa7', '2051a104e5708ed3d359b10c015db876e8c75a229843598a7c6f660532a828f6', 782, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V2.yaml': ('9cda0d95b4da50eda06e527eb4b75d6771fa67b9', 'e4160767e9d9622a6408c0f39868f802688433ad68d86fe342a015dfd1bff5bd', 2098, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
    }
    abk_public = {
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AQ_SOURCE_COMPATIBLE_ARCHITECTURE_MODELS_V2.yaml': ('bb110c6493c333eb7ae8b6b09610f53715424a4c', 'b460af8e73d3db6db8ed6223dc24a548b5519efd175eeefca03433d76c690520', 3307, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AR_PROVENANCE_ROOT_EVIDENCE_MODELS_V2.yaml': ('475c318bb1ae3b5db3f0fce01f06d4bf66724409', 'ab7398b15130cdf60bbc1131403a6dbb5008651d876ff56405b43b1716a29a18', 2004, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V2.yaml': ('3c89aa19631f03d2fc1814ad3045cc06bb49fd5c', '991763b96ac886e37c4ff01dfb6e4f3961cda00b57ada958f97aa3b18ddd5a05', 1509, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V2.yaml': ('0d0a7223aa0ff2ee6e4da155b12ee06df152874c', 'be1e7519b3007a18bf856c4e0baf29b0684b729c6d4b42e753274c10198b457a', 1444, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V2.yaml': ('86b3609b228da4e42b50a365bc7b094413719437', '1c3a637ff73691d0f4e7303384c17fbd1b4291626073ced5db4d448b58d611c9', 1461, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V2.yaml': ('f7e067f1195c13211cd8a067c560ba96b4b49e54', '993a403134973bcd90c3c8ead4b9140ab7a4111f6866bf471150a97deae13f44', 1149, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BA_INTERFACE_RELATIVE_CAUSAL_QUOTIENT_MODELS_V1.yaml': ('8c90bb5a7e6608f9219361fb21d14dcd374ab267', '9f01b79e842c9e25a9deccc1f316956a5f25ab52970a87c8a474d89529c66d02', 1215, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BB_JOINT_CAUSAL_INTERFACE_MODELS_V1.yaml': ('cf33648d43be6aa32f9f6112abe4be83caeaa5c4', 'c71f4dd9e225f8fe8da3f5d581daaff8bc37bddfaf886691c068d82db558b053', 875, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BC_UNIVERSAL_INTERFACE_EXPERIMENT_PARITY_MODELS_V1.yaml': ('d8fe3c0b6b5e38d64a508a95c83ae1810e1a27fe', '82beb4c893c0d12eb9727d20ad1428b1aa45397ae567725ddfece1571b4c833c', 660, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BD_LATENT_SOURCE_ORIENTATION_MODELS_V2.yaml': ('c20193aeee354f6fb17727e889062893cd8cc2c8', 'be48fe63092df4f66ff66a0fe52ffbf50c8bfd11f3c05ce67a443fb54bf4c02d', 2159, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V2.yaml': ('69367d117baefe6702b7bcdc22042042bf8e3923', '40e08b9ef186620e9eb988e7e556694bfc94b94e3dd308d15a682ca03dca2291', 1605, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V2.yaml': ('36ad7d6244e5d54eeb650d0f360acd6a45a53c0c', '4ea76f85945aca04192fb5beb74db8b9d3d0307a254de2b329d917d39674aca7', 2069, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BG_INTEGRATED_R5_COMMON_MODEL_V2.yaml': ('23ae320500f7788577a3a9e62f37786b93cee2a2', '97d7482dbf3ed4b50de79699cedc77067323b095dfd6c7eb3afb557acdfcfcc4', 1769, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V2.yaml': ('e272acb828534d7e09b890f07017e172fb9d7dd4', '14bc65a43c165e7c71208fc873160cdcf88cc5be50e49a49cbb68adfbaf55f33', 1646, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V2.yaml': ('ee15782926dbe3ae049c5fc9ccfa530f1866a58f', '27a4e79b4b11916d4047ad7677db26735f886ed7cbb2b01d5bd89754f33da080', 1333, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V2.yaml': ('01adca7afe96d67a0da61ccb8787c9e267e9208e', 'd6e99abc7d0038a9ff47cb02809d52e8004251b79d5e2164b3aad0dcca66c616', 1082, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BA_ADMISSION_OVERLAY.yaml': ('132b73791a09d81358e33e1f7d9698959c9146a2', '49f6ed3dda0270e58cb85b44c762be4e31620af9deac7249eac364be899e90fa', 1560, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BB_ADMISSION_OVERLAY.yaml': ('23e4ce4a982031b1730c365bca1ec6a3684ea436', '8dd3b5e550662103f8f00b647219d4756a9e182fd6a5b86ae2782812e1e730fe', 1674, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BC_ADMISSION_OVERLAY.yaml': ('0cdaac12accc57d203c0272eda273279d2b792b8', 'c9ead1aeaf5d93742865ef8015556fed11f85b9f9813e9a23c7804400683978a', 1719, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BD_ADMISSION_OVERLAY.yaml': ('6546f5ba202e9fb5e256c22379f61a42069f6665', 'bc66bf8cea8fa9f454ea2cf7c97a0a1e33d50521a1646c519f12c8adbd8e5ab2', 1788, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BE_ADMISSION_OVERLAY.yaml': ('a532439c13d961df272781b0b7d49a6213d136a6', '12f4e83b712fa0d58b100169644aa17561a74fe6221466e50752d417c07f185b', 1774, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AT_NEUTRAL_INTERVENTIONAL_TRACE_MODELS_V1.yaml': ('81939539fe9ae4b34412e9af80243b69dade62dd', '0ed0bc80aefa85b01a682fbd8d9f0c579b3316372f7dc50a7bd054e0787b7877', 2379, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V1.yaml': ('8535624b656ca283113d322fecbc566290912f4e', '82cee72fcc9a4135275de39175a69d5b603ca62eaf2d3c9f87df9fabeed5c82c', 1292, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V1.yaml': ('6471321e88bf946175d204afb78650463332f70b', '132d6bc9ea2de7927682ff4822ad611c3f5d43af17329130df2aeeac13cb8b69', 1042, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V1.yaml': ('c7a8d6fa611e9a5f7535f701ceb66b0805fe7c17', 'a5429ef4ae52c5a62c13eb56d9b2098673b2b04013a051e22aa87648c853b993', 1549, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V1.yaml': ('84eb89781eb35bbf74dfa74e78ee32bc332a7e89', 'b5d353a56596143c1f02001e571e2d4bfd635331c08bf26530f6850b77c3a29f', 955, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BD_LATENT_SOURCE_RELIABILITY_ORIENTATION_MODELS_V1.yaml': ('d8fb38df99a36119cdfd9d0cd7b027599d304256', '1433c3131749f686a2823fe0e9d7c27d6f6b1b4b64c05ff7d0bbd747bf3f5c6c', 2345, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V1.yaml': ('991381e40dbc0a041a79b3375bba389320c3af14', 'bcc3caaf8ee5fe6910de9b0f4eb80939388fed07ae02e307437723a5a2825e72', 1362, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V1.yaml': ('7c94adf7f1f36a636ba8cf24139fcdea66269e9d', 'db4f7664cd22dc28425e5fa5da03cac18645ec3b72856b87ec5f11aee5a104fb', 1375, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V1.yaml': ('3996ff60410db02f1ccd11f9cba4f36b1ba8f0b7', '864b04f56a250ed8ad05dacfbd4970a0343367a0b0feaecab2bba9de34a13066', 1455, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V1.yaml': ('68add8fc26f0f801b6e4b20ead7d5b93681be1cc', '4a4e5b750c57c3b4a65934c7edd4de495a74ce00c0d8eadd511651bb93eda0e5', 910, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
        'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V1.yaml': ('19306d597907bb1fc1508e484d250b82e7905555', '1317a7369c5daf99935a085cd03b8b60eeec87c3c6ce640f4494d17acab8f966', 1041, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'),
    }
    for bindings in (earlier, next24, combined, dict(combined, **fixtures),
                     dict(combined, **fixtures, **replay_input),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers, **intake_test_consumer),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers, **intake_test_consumer, **codex_test_consumer),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers, **intake_test_consumer, **codex_test_consumer,
                          **reissue_test_consumer),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers, **intake_test_consumer, **codex_test_consumer,
                          **reissue_test_consumer, **central_public),
                     dict(combined, **fixtures, **replay_input, **calculus_fixture,
                          **digest_consumers, **attribution_consumers, **governance_consumers,
                          **frontier_test_consumers, **intake_test_consumer, **codex_test_consumer,
                          **reissue_test_consumer, **central_public, **abk_public)):
        expected = deepcopy(original)
        try:
            for path, (blob, identity, size, revision) in bindings.items():
                rows = [r for r in expected['objects'] if r.get('repository_path') == path]
                if len(rows) != 1:
                    break
                source = rows[0]
                if (source.get('disposition') != 'REUSE'
                        or source.get('source_sha256') != identity
                        or source.get('public_sha256') != identity
                        or source.get('source_bytes') != size or source.get('public_bytes') != size):
                    break
                source.update(repository_revision=revision, git_blob=blob)
            else:
                if candidate == expected:
                    return True
        except (KeyError, TypeError, ValueError):
            return False
    return False


def _permitted_administrative_guide_pins(original, candidate):
    """Admit the exact two already-public guide coordinates as a whole group."""
    from copy import deepcopy
    expected = deepcopy(original)
    try:
        for path in ADMIN_PUBLIC_GUIDE_PATHS:
            blob, identity, size, _ = ADMIN_GUIDES[path]
            rows = [row for row in expected['objects'] if row.get('repository_path') == path]
            if len(rows) != 1:
                return False
            source = rows[0]
            if (source.get('disposition') != 'REUSE' or source.get('source_sha256') != identity
                    or source.get('public_sha256') != identity or source.get('source_bytes') != size
                    or source.get('public_bytes') != size):
                return False
            source.update(repository_revision=ADMIN_RECORD_BASE, git_blob=blob)
        return candidate == expected or _permitted_projection_consumer_pins(expected, candidate)
    except (KeyError, TypeError, ValueError):
        return False


def permitted_historical_status_pin(repo, row, body):
    """Admit exact navigation and finite historical-source bindings, not identities.

    The live status index and contributor guide have authorised reader additions.
    T20 retains both original bodies at its original baseline, using the existing
    resolver's historical REUSE form. No source/public hash, length, role, count,
    eligibility, scientific claim or unrelated record may change.
    """
    if row["path"] != "research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json":
        return False
    original = subprocess.run(["git", "cat-file", "blob", row["git_oid"]],
                              cwd=repo, capture_output=True, check=False)
    if original.returncode:
        return False
    try:
        expected = json.loads(original.stdout, object_pairs_hook=unique_object)
        candidate = json.loads(body, object_pairs_hook=unique_object)
        bindings = (
            ("94fb4c0a0fbe7406570711b222ac0e5dbc7493867cd28cb6f0ef08c6fea99074",
             "docs/project-closure/HISTORICAL-STATUS-INDEX.yaml", 5312,
             "d4ec27e7da404b830f1a6fe687809c1cf2011413"),
            ("5e00b728e533c019b656032a86b5427f820d281056c40d78df0d0cf2c1549bc1",
             "CONTRIBUTING.md", 3392,
             "790eb3546a0db6627d3a51df43b1e178f464b067"),
        )
        for identity, path, size, blob in bindings:
            selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
            if len(selected) != 1:
                return False
            source = selected[0]
            if (source.get("disposition") != "REUSE"
                    or source.get("repository_path") != path
                    or source.get("source_bytes") != size
                    or source.get("public_bytes") != size
                    or source.get("public_sha256") != identity):
                return False
            source.update(repository_revision="7efc6217c090b92d65f2c4cb8b011c18eb96bf7c",
                          git_blob=blob)
        if candidate == expected:
            return True  # The original two-navigation-binding contract remains valid.
        for path in HISTORICAL_PROSE_PUBLIC_PATHS:
            if path not in ORIGINAL_HISTORICAL_PROSE_PATHS:
                continue
            blob, identity, size = HISTORICAL_PROSE[path]
            selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
            if len(selected) != 1:
                return False
            source = selected[0]
            if (source.get("disposition") != "REUSE"
                    or source.get("repository_path") != path
                    or source.get("source_bytes") != size
                    or source.get("public_bytes") != size
                    or source.get("public_sha256") != identity):
                return False
            source.update(repository_revision=HISTORICAL_PROSE_REVISION, git_blob=blob)
        if candidate == expected:
            return True  # Retain the independently qualified original five-path contract.
        extra = [(path, HISTORICAL_PROSE[path], HISTORICAL_PROSE_REVISIONS[path],
                  HISTORICAL_PROSE_DISPOSITIONS[path]) for path in MEDIATOR_PROSE]
        extra.append(("scripts/validate_v5_successors.py",
                      ("62457f5f61e6e433b7714948e1b0c2545a00fbb1",
                       "fc70d3afba7df52044a67a4d77de438e929a8e44e8b58bff4f2cc808e8f0e185", 51484),
                      HISTORICAL_PROSE_REVISION, "REUSE"))
        for path, (blob, identity, size), revision, disposition in extra:
            selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
            if len(selected) != 1:
                return False
            source = selected[0]
            if (source.get("disposition") != disposition or source.get("repository_path") != path
                    or source.get("source_bytes") != size or source.get("public_bytes") != size
                    or source.get("public_sha256") != identity):
                return False
            source.update(repository_revision=revision, git_blob=blob)
        if candidate == expected:
            return True  # Preserve the finite mediator and original-validator evidence form.
        math_code = (
            ("tests/test_math_source_validator.py",
             "dcb9a7171c3f82114936c36529093674e98417ca",
             "3c04cf4922e82d9a587b5d6c1105906cb3a18ecfb6fbb358cada239e8300a6f3", 5084),
            ("scripts/validate_math_source.py",
             "7a72d773ca5248b26383624ee1837448b9a2479c",
             "3c52ed4d872e7b3a6b1a35a0d3dd6624cd4b8052736cc55a78e055731d58177a", 38178),
        )
        for path, blob, identity, size in math_code:
            selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
            if len(selected) != 1:
                return False
            source = selected[0]
            if (source.get("disposition") != "REUSE" or source.get("repository_path") != path
                    or source.get("source_bytes") != size or source.get("public_bytes") != size
                    or source.get("public_sha256") != identity):
                return False
            source.update(repository_revision=HISTORICAL_PROSE_REVISION, git_blob=blob)
        if candidate == expected:
            return True  # Preserve the exact seven-path plus math-code evidence form.
        blob, identity, size = HISTORICAL_PROSE[FISHER_AUDIT]
        selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
        if len(selected) != 1:
            return False
        source = selected[0]
        if (source.get("disposition") != "ADD_EXACT" or source.get("repository_path") != FISHER_AUDIT
                or source.get("source_bytes") != size or source.get("public_bytes") != size
                or source.get("public_sha256") != identity):
            return False
        source.update(repository_revision=FISHER_PROSE_REVISION, git_blob=blob)
        if candidate == expected:
            return True  # Preserve the Fisher form before the legacy-test code pin.
        identity = "77f9a6bb323345942a400353a614caeacb2546cc11cbde95cb082ca4acaf1a09"
        selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
        if len(selected) != 1:
            return False
        source = selected[0]
        if (source.get("disposition") != "REUSE"
                or source.get("repository_path") != "tests/test_v5_twentieth_data.py"
                or source.get("source_bytes") != 6819 or source.get("public_bytes") != 6819
                or source.get("public_sha256") != identity):
            return False
        source.update(repository_revision=HISTORICAL_PROSE_REVISION,
                      git_blob="e1bad4344f949d9ddbe32ca6c4e6bd4158515a86")
        if candidate == expected:
            return True  # Preserve the exact Fisher and legacy-test code form.
        for path, (blob, identity, size) in TYPED_PROSE.items():
            selected = [r for r in expected["objects"] if r["source_sha256"] == identity]
            if len(selected) != 1:
                return False
            source = selected[0]
            if (source.get("disposition") != "REUSE" or source.get("repository_path") != path
                    or source.get("source_bytes") != size or source.get("public_bytes") != size
                    or source.get("public_sha256") != identity):
                return False
            source.update(repository_revision=TYPED_PROSE_REVISION, git_blob=blob)
        if candidate == expected:
            return True  # Preserve the exact typed-prose form.
        # These current consumer bodies have changed, while their T20 evidence
        # identities still denote the original BASE bodies. The finite duplicate
        # class supplies the only other admissible historical routes.
        consumer_paths = {
            "tests/test_ar8r_v11_reconciliation.py":
                ("30b8c5ff2679423af0d8231852fd2dd826f91972db891cc461894709d9840606", 91370),
            "docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md":
                ("327fd8a2e5ea986f785270f3713e6e034975ecbea9bda2cf5bca04ef374112b6", 1977),
            "scripts/validate_ar8r_reconciliation.py":
                ("84cd7f17f9961142e76f76fa427bb49aaf4b29fdc8d9d5056c3c53e8c8c20669", 168547),
        }
        aliases = pmr007_deep_duplicate_paths(repo)
        selected = [r for r in expected["objects"]
                    if r.get("repository_path") in aliases | consumer_paths.keys()]
        if (len(aliases) != 824 or len(selected) != 587
                or len({r["repository_path"] for r in selected}) != 587
                or sum(r["repository_path"] in aliases for r in selected) != 584):
            return False
        revision = "7efc6217c090b92d65f2c4cb8b011c18eb96bf7c"
        objects = subprocess.run(
            ["git", "--no-replace-objects", "cat-file", "--batch"], cwd=repo,
            input="".join(revision + ":" + r["repository_path"] + "\n" for r in selected).encode(),
            capture_output=True, check=False)
        if objects.returncode:
            return False
        offset = 0
        for source in selected:
            path, identity, size = (source["repository_path"], source["source_sha256"], source["source_bytes"])
            if (source.get("disposition") != "REUSE" or source.get("public_sha256") != identity
                    or source.get("public_bytes") != size
                    or (path in consumer_paths and consumer_paths[path] != (identity, size))):
                return False
            end = objects.stdout.find(b"\n", offset)
            if end < 0:
                return False
            header = objects.stdout[offset:end].decode("ascii").split()
            if len(header) != 3 or header[1:] != ["blob", str(size)]:
                return False
            original_body = objects.stdout[end + 1:end + 1 + size]
            offset = end + 2 + size
            blob = hashlib.sha1(b"blob " + str(size).encode() + b"\0" + original_body).hexdigest()
            if (len(original_body) != size or objects.stdout[offset - 1:offset] != b"\n"
                    or hashlib.sha256(original_body).hexdigest() != identity or blob != header[0]):
                return False
            source.update(repository_revision=revision, git_blob=blob,
                          publication_basis=("exact_existing_public_git_blob; current_consumer_has_distinct_identity"
                              if path in consumer_paths else
                              "exact_existing_public_git_blob; retained_counterpart_qualified_by_snapshot_validator"))
        if offset != len(objects.stdout):
            return False
        if candidate == expected:
            return True  # Preserve the exact 587-row snapshot form.
        # The two further copy migrations change these three original owners.
        # Only their original evidence routes may change; every other field and
        # every unrelated object must still equal an already admitted form.
        further_consumers = {
            "scripts/validate_research_continuations.py":
                ("5157341400df0d327cb39f698838ac8ba49f82eb6bf71c8e40f84f670b3e55f7", 29272,
                 "ef5422f8e877f628e8aedbe61dc4dd2af614cb0a"),
            "docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md":
                ("66cc0fbc5ab06ab0dfffdb1e6fe1845775cfa0f12233f7517d12042ae16d9486", 1354,
                 "6240db1cb6e2f844506a989ee2cfa14783c6d6d6"),
            "docs/project-closure/ar8r-v11/post-merge-proposals/README.md":
                ("d20707cf0d24dd5b2b966f2b1f3640ec7672092ef8a19b57f60fc61897cd6b50", 4073,
                 "9628152cf22670418bc2c88aa13e496047fba40c"),
        }
        for path, (identity, size, blob) in further_consumers.items():
            matches = [r for r in expected["objects"] if r.get("repository_path") == path]
            if len(matches) != 1:
                return False
            source = matches[0]
            if (source.get("disposition") != "REUSE" or source.get("source_sha256") != identity
                    or source.get("public_sha256") != identity or source.get("source_bytes") != size
                    or source.get("public_bytes") != size):
                return False
            entry = subprocess.run(["git", "--no-replace-objects", "--literal-pathspecs",
                "ls-tree", "-z", revision, "--", path], cwd=repo, capture_output=True, check=False)
            original = subprocess.run(["git", "--no-replace-objects", "cat-file", "blob",
                revision + ":" + path], cwd=repo, capture_output=True, check=False)
            if (entry.returncode or original.returncode
                    or entry.stdout != ("100644 blob " + blob + "\t" + path + "\0").encode()
                    or len(original.stdout) != size or hashlib.sha256(original.stdout).hexdigest() != identity
                    or hashlib.sha1(b"blob " + str(size).encode() + b"\0" + original.stdout).hexdigest() != blob):
                return False
            source.update(repository_revision=revision, git_blob=blob,
                          publication_basis="exact_existing_public_git_blob; current_consumer_has_distinct_identity")
        return (candidate == expected or _permitted_projection_consumer_pins(expected, candidate)
                or _permitted_administrative_guide_pins(expected, candidate))
    except (KeyError, TypeError, ValueError, OSError):
        return False



# Temporary, exact reviewed attribution-ledger successor. The root-approved
# v4 modal packet is c52ca63023cb01215f323a37495fc70a1ef2806009936bc567d16ccb6abfffb0;
# separate correction review is fe7e8aa047475a3df7ea72919c6db81b594343499fa013ae59329fc5b1d184c2.
# This is neither an arbitrary operational-edit waiver nor final reader design.
REVIEWED_SOURCING_LEDGER = (
    'docs/sourcing/R3-SOURCING-LEDGER.md',
    'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
    ('2ed9e182cb9db7d38d7c56c0f043983c99f8c940',
     '2177de55bb84adc24b69dd8551c12893e7f4dd7eae2a5d5d643b372b9236b770', 5421),
    ('947ad35bde130263dc4a057a1adebb72837f2d2f',
     '1cf0a9885997a0dbaa37fbf03d63e4b500cc12ad75340d3b83170fd8bf755d6b', 10030),
)


def reviewed_indexed_modification(repo, contract):
    """Authenticate one exact ordinary indexed/present reviewed source successor."""
    repo = Path(repo)
    path, revision, original, current = contract
    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=repo, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('reviewed source edition native evidence unavailable')
        return result.stdout
    def identity(body):
        return (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                hashlib.sha256(body).hexdigest(), len(body))
    tree = git('ls-tree', '-z', revision, '--', path)
    if original is None:
        if tree != b'':
            raise ValueError('reviewed source addition predecessor is not absent')
    else:
        if tree != ('100644 blob ' + original[0] + '\t' + path + '\0').encode():
            raise ValueError('reviewed source edition predecessor tree differs')
        if identity(git('cat-file', 'blob', revision + ':' + path)) != original:
            raise ValueError('reviewed source edition predecessor bytes differ')
    expected = ('100644 ' + current[0] + ' 0\t' + path + '\0').encode()
    if git('ls-files', '--stage', '-z', '--', path) != expected:
        raise ValueError('reviewed source edition index differs')
    for ancestor in (repo, *repo.parents):
        if ancestor.is_symlink():
            raise ValueError('reviewed source edition root is symlinked')
    node = safe_path(repo, path)
    fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        start = os.fstat(stream.fileno())
        if (not stat.S_ISREG(start.st_mode) or start.st_nlink != 1
                or start.st_mode & 0o111 or start.st_size != current[2]):
            raise ValueError('reviewed source edition is not an ordinary exact-sized file')
        body = stream.read()
        finish = os.fstat(stream.fileno())
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    if (any(getattr(start, f) != getattr(finish, f) for f in fields)
            or identity(body) != current):
        raise ValueError('reviewed source edition present bytes differ or changed')
    if git('ls-files', '--stage', '-z', '--', path) != expected:
        raise ValueError('reviewed source edition index changed during qualification')
    final = node.lstat()
    if any(getattr(start, f) != getattr(final, f) for f in fields):
        raise ValueError('reviewed source edition path changed during qualification')
    return {path}



def reviewed_sourcing_ledger_modifications(repo):
    """Preserve the existing exact attribution-ledger contract unchanged."""
    return reviewed_indexed_modification(repo, REVIEWED_SOURCING_LEDGER)


# The original three-owner successor remains exact (reviewed reconstruction8fd004ba).
# The independently reviewed governed-path owner and genuinely new live test below
# use the same indexed-edition guard, with authenticated absence only for that test.
# This temporary migration contract neither adopts science nor admits arbitrary edits.
REVIEWED_AUTHORITY_EDITS = {
 '.gitattributes': ('.gitattributes',
                   '0784acddd4770f1190f758f264ba52b2b110bd27',
                   ('92d2f4dd081139c9bcd97759b7920e86ee6b5b38',
                    '70e8d3d8c90547f026df30f42870b60bf17c48bd642a9d7f336cb109e658dc70',
                    1871),
                   ('95a8280b070ac0babbefb477f25fa7f1f5ed3c6d',
                    '09180182f40a449c28b2b3e5a4b1f1cbe8f48f13963ec6d2de402d660a1dc209',
                    1935)),
 'scripts/validate_candidate_state.py': ('scripts/validate_candidate_state.py',
                                         'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
                                         ('f978626577743edc5f18a90edcc9661b3935f91c',
                                          '8808f2d7278885021b2fb812b5149dd157e9e53fcae49e24b3bea9353dc68215',
                                          6410),
                                         ('a8e5c1caff041069010374af1093f279d320a168',
                                          'dd0c826ca8a32eb2beeee02a8e443d4d2a5886d22c8854afb2f0fc6348f3b9ca',
                                          4789)),
 'scripts/validate_review_state.py': ('scripts/validate_review_state.py',
                                      'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
                                      ('95087964f175e00c5dc1a628bc83d40377c6b911',
                                       '240dd79778d8fded8744873ddfc298e3206fa120dbe0417b50198983975efff0',
                                       34750),
                                      ('89938d0e0190627b04ca849de028c3e6908e38e5',
                                       'e69772afa041b7044874c15c1b83169ab06d89b167a7b00796051df49167faf0',
                                       36059)),
 'tests/test_candidate_state.py': ('tests/test_candidate_state.py',
                                   'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
                                   ('a2c0369810339d315bca87ecf02f29dc2d1b0a0d',
                                    'fefd90abb169e79644813129e1b11acc9a973a9a39128645682c46d51108a8e9',
                                    17484),
                                   ('35dfb35cb5e190ee81caea56ccc59a5083882fb1',
                                    'cd3cd8df68677335cb7a08457e2791058c8f01b14d41d68e85019313c958cf22',
                                    13417)),
 'scripts/validate_cross_record_semantics.py': ('scripts/validate_cross_record_semantics.py',
                                                'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
                                                ('af71a10aa182f32795e7736c23e0a620073b994a',
                                                 '3b75bca002978c6c47dc5120e9114fc8c601b7f7f6da36bdf061799b899fc1e5',
                                                 45554),
                                                ('bcb8ae0680493508bd4a1a6431b598778a09b16a',
                                                 '24e0a43664c74a76282228f090835e70652ffccaa292f5497ebd76fc3eda1982',
                                                 48293)),
 'tests/test_cross_record_semantics.py': ('tests/test_cross_record_semantics.py',
                                          'c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce',
                                          None,
                                          ('efe2457f0f37360cb651a581e20931f123c0c4c5',
                                           '8fcf08ed2d1fb40700318880977743412abc2fbe8c2a19d50036a502505169a7',
                                           11482)),
 'tests/test_pmr007_deep_bk_public_snapshot.py': ('tests/test_pmr007_deep_bk_public_snapshot.py',
                                                  '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                  ('249a89266da20b19a84131e7b27a0814aaadd54f',
                                                   'fd6dbafefb2eb6b24119c0d94634251df621d30122c246f690cce146ed5c9ce5',
                                                   12480),
                                                  ('338a965b1d3464dcc71571057cb3749e6db4d2f6',
                                                   '393836cabe9e060109fa747c907f8d80c4df23cd5c739eb2efe56879e71df900',
                                                   18014)),
 'tests/test_pmr007_deep_bv_semantic_reissue.py': ('tests/test_pmr007_deep_bv_semantic_reissue.py',
                                                   '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                   ('b932096c9490c9e31bfc3f596f2990a4dfd1e8ba',
                                                    '334034b9019f5f27ca2fcac36e568982bda3d7d6e7c2daca40e565d16792a37f',
                                                    9724),
                                                   ('c58ba28e58995bba573184dac867ef38673abfc1',
                                                    '5ee60a37fb6fa5a18f5bc78a47c1d342a7dee7b3ea4a0862473782ca114e156f',
                                                    14419)),
 'tests/test_ar8r_six_lane_v14_intake.py': ('tests/test_ar8r_six_lane_v14_intake.py',
                                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                            ('c0b79431bafc486c71a083b3b8afdec0db431236',
                                             '548d4358ca89755bbfd29b2df9a4b6b2b6ca36541cc5994e523198c40ddea26c',
                                             11625),
                                            ('9c5c787c71490d4e4f7807df028e02ba510a0dc5',
                                             '8fbf27f3b400015c472a16d4a23ff63ee8ef050409f4f875564b1cda2ef0e6b4',
                                             33249)),
 'tests/test_ar8r_codex_corpus_synthesis_v14.py': ('tests/test_ar8r_codex_corpus_synthesis_v14.py',
                                                   '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                                                   ('b5aa03c18c2e9df149f460955184bec83a6b46a0',
                                                    '7801ae286ca0b8c8c4c1bce7e73aedc9dfb914474d66ea58c029c756ea1ef67e',
                                                    46305),
                                                   ('851669b52eabe0a9262c8f7a5ca9cc2cd57971a8',
                                                    'f535c52b5d47ef2fe21b8663d52505762dac7e7b8124c1b3cc5afb44f9c9f8d6',
                                                    35766)),
 'formal/certificate-frontier/CertificateFrontier.lean': ('formal/certificate-frontier/CertificateFrontier.lean',
                                                          '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                          None,
                                                          ('208cf6e6250c6ff50d0b03575a6ae7926b70d1ed',
                                                           '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0',
                                                           12278)),
 'formal/certificate-frontier/Controls.lean': ('formal/certificate-frontier/Controls.lean',
                                               '0784acddd4770f1190f758f264ba52b2b110bd27',
                                               None,
                                               ('1c6b8900e600c63e30f0aa83f49f7db8211a7cdf',
                                                '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132',
                                                2410)),
 'formal/certificate-frontier/ScopeChecks.lean': ('formal/certificate-frontier/ScopeChecks.lean',
                                                  '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                  None,
                                                  ('2efba39e95c7b0cf38b246654d64f16e099f8e31',
                                                   '6218ff6fa7b6e5b304859c2f4ad3d512118f1a3c9b68ec7e446d6cc1cd2d78a6',
                                                   1345)),
 'formal/certificate-frontier/mutations/CostBlind.lean': ('formal/certificate-frontier/mutations/CostBlind.lean',
                                                          '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                          None,
                                                          ('01cef9257fc16b90c16ae14ca9e65aef41cdd787',
                                                           'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776',
                                                           227)),
 'formal/certificate-frontier/mutations/CurrentCost.lean': ('formal/certificate-frontier/mutations/CurrentCost.lean',
                                                            '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                            None,
                                                            ('9ad7316c3906603cd262cb781736078b18cd14a5',
                                                             '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d',
                                                             249)),
 'formal/certificate-frontier/mutations/InfinitePrice.lean': ('formal/certificate-frontier/mutations/InfinitePrice.lean',
                                                              '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                              None,
                                                              ('ffa13821c157cd943b1bcb5f6aa514c917f198b1',
                                                               '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe',
                                                               293)),
 'formal/certificate-frontier/run-primary.sh': ('formal/certificate-frontier/run-primary.sh',
                                                '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                None,
                                                ('fb83caac96791a44fcfb3001cae2e4be03a91b9c',
                                                 '9a3980fefd48afc8ba9dd2bec1741110c0ab191a088e52fc3e07500c0c88fd95',
                                                 3589)),
 'formal/certificate-frontier/run-scope-review.sh': ('formal/certificate-frontier/run-scope-review.sh',
                                                     '0784acddd4770f1190f758f264ba52b2b110bd27',
                                                     None,
                                                     ('8402995d37601853f80ddd7f989cc4fe4c600950',
                                                      '95fb6990e711f319f5bd15e610269bb8bfd462f3f9a718b06324c2ed381495cf',
                                                      3298)),
 'tests/test_pmr007_deep_bw_cj_semantic_reissue.py': ('tests/test_pmr007_deep_bw_cj_semantic_reissue.py', '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c', ('a33743bf20cddf6363021f938a1cef2e0e9baf84', '22f0d82eabb228d0d6d0b0c10a5146bf93ca17b6877d34a169cb8986c1f0710e', 6275), ('1c3cad17a21642e63b1e264f88ef403173c1dd1b', '71703c3507b08e5da55e749afc3af8128444e833ac66c9e6b1b57e97235c2afc', 37844))}


def reviewed_authority_modifications(repo, paths):
    """Admit only requested exact indexed/present authority-owner editions."""
    admitted = set()
    for path in sorted(paths):
        if path not in REVIEWED_AUTHORITY_EDITS:
            raise ValueError('unreviewed authority owner: ' + path)
        admitted.update(reviewed_indexed_modification(repo, REVIEWED_AUTHORITY_EDITS[path]))
    return admitted


# These are the existing Issue-35 implementation surfaces, not a science
# exclusion by extension or directory name. A new original work even inside
# docs/reader/ requires corpus admission; untracked scratch is not published.
REFACTOR_EDIT_PATHS = {
    "README.md", "STATUS.md", "CONTRIBUTING.md",
    ".github/workflows/validate.yml", ".github/workflows/reader-refactor-snapshot.yml",
    "scripts/reader_census.py", "scripts/check_reader_pilot.py",
    # Reviewed hosted absence transaction helpers and focused controls. This
    # finite engineering-support population adds no source/work denominator;
    # similarly named files still require their own disposition review.
    "scripts/check_source_alias_absence.py", "scripts/source_alias_absence_boundary.py",
    "scripts/source_alias_absence_context.py", "scripts/source_alias_absence_continuations.py",
    "scripts/source_alias_absence_evidence.py", "scripts/source_alias_absence_guard.py",
    "scripts/source_alias_absence_metadata.py", "scripts/source_alias_absence_population.py",
    "scripts/source_alias_absence_reader.py",
    "tests/test_source_alias_absence_boundary.py", "tests/test_source_alias_absence_evidence.py",
    "tests/test_source_alias_absence_population.py",
    # Exact existing engineering consumers changed by the reviewed digest176 migration.
    # Their original evidence remains pinned by the finite projection contract.
    "scripts/validate_ar8r_codex_corpus_synthesis_v14.py",
    "scripts/validate_ar8r_external_challenges.py",
    "scripts/validate_ar8r_six_lane_v14_intake.py",
    "scripts/validate_pmr007_deep_bk_public_snapshot.py",
    "scripts/validate_pmr007_deep_bv_semantic_reissue.py",
    "scripts/validate_pmr007_deep_bw_cj_semantic_reissue.py",
    # Existing integrity owners for the finite A-AP duplicate retirement.
    "scripts/validate_ar8r_reconciliation.py", "tests/test_ar8r_v11_reconciliation.py",
    "docs/project-closure/ar8r-v11/SHA256SUMS",
    "docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md",
    "docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md",
    "docs/project-closure/ar8r-v11/post-merge-proposals/README.md",
    "tests/test_reader_census.py", "tests/test_reader_pilot.py",
    "tests/test_internal_references.py",
    # Exact existing integrity owners changed for the finite history contract;
    # this does not admit any new source path or predecessor modification.
    "scripts/resolve_t20_v6_source.py", "scripts/validate_t20_v6_projection.py",
    "tests/test_t20_v6_projection.py", "scripts/validate_v5_successors.py",
    "tests/test_v5_twentieth_data.py",
    # Existing synthetic controls now read the actual result/status owner.
    "tests/test_v5_successors.py", "tests/v5_successor_fixtures.py",
    # Existing source-ID and replay owners for the finite continuation copies.
    "scripts/validate_research_continuations.py", "scripts/replay_research_continuations.py",
    "scripts/replay_v5_successors.py",
    "tests/test_research_continuations.py", "scripts/replay_continuation_controls.py",
    # Current reference consumers for the same four exact typed prose identities.
    "scripts/validate_repo.py", "scripts/validate_internal_references.py",
    # Existing source-display integrity owner and its focused regression tests;
    # scholarly bodies still require their exact source/work/review admission.
    "scripts/validate_math_source.py", "tests/test_math_source_validator.py",
    "docs/project-closure/r7e-sol/R7E-SOL-ADVERSARIAL-REPORT.md",
    "docs/current-state.yaml", "docs/provenance/RELEASE-MANIFEST.sha256",
    "docs/project-closure/HISTORICAL-STATUS-INDEX.yaml",
    "research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json",
} | {"docs/reader/" + name for name in (
    "RESEARCH-ATLAS.md", "PAPER-CATALOGUE.md", "RESULT-INDEX.md",
    "CURRENT-FRONTIERS.md", "APPLICATIONS.md", "VERIFICATION-GUIDE.md",
)} | {"docs/project-closure/reader-refactor-issue-35/" + name for name in (
    "EXECUTION.md", "CONTINUATION.md", "CENSUS.json", "OWNER-MAP.json",
    "CROSSWALK.json", "PILOT.md", "PILOT-QUALIFICATION.md", "RECOVERY-04.md",
    "APPLICATION-COVERAGE.md", "IDENTITY-COVERAGE.md", "FIFTEENTH-COVERAGE.md",
    "REPORT-REANALYSIS-COVERAGE.md", "PRIMARY-WORK-COVERAGE.md", "PROGRESS.md",
    "COLLECTION-COVERAGE.md", "C05-REVIEW.json",
)}


def check_source_additions(repo, baseline_rows, owners, cross):
    """Bind finite new expositions and review support without rebasing history.

    The owner map admits exact tracked objects. Existing crosswalk work/source
    edges own their reading roles; a review table binds each exact new edition.
    These mechanical bindings neither assess the science nor adopt its claims.
    """
    declared = owners.get("source_additions", [])
    if declared == []:
        return {}, []
    errors, admitted, bindings = [], {}, {}
    def fail(message):
        errors.append("source-addition: " + message)
    fields = {"key", "path", "mode", "git_oid", "bytes", "sha256", "role",
              "work_keys", "supporting_source_keys"}
    if not isinstance(declared, list):
        return {}, ["source-addition: expected a finite list"]
    sources = cross.get("sources", {})
    works = cross.get("works", [])
    paths = set()
    for row in declared:
        try:
            if not isinstance(row, dict) or set(row) != fields:
                raise ValueError("incomplete or unknown identity/relationship fields")
            key, path = row["key"], row["path"]
            if not isinstance(key, str) or not key or key in bindings or path in paths:
                raise ValueError("duplicate or malformed source key/path")
            if path in baseline_rows or path in REFACTOR_EDIT_PATHS:
                raise ValueError("a baseline or operational path cannot masquerade as new scholarship")
            node = safe_path(repo, path)
            body = node.read_bytes()
            if (row["mode"] not in ("100644", "100755")
                    or type(row["bytes"]) is not int or row["bytes"] < 0
                    or not isinstance(row["git_oid"], str)
                    or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", row["git_oid"])
                    or not isinstance(row["sha256"], str)
                    or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])):
                raise ValueError("malformed exact source identity")
            raw = b"blob " + str(len(body)).encode("ascii") + b"\0" + body
            oid = (hashlib.sha1(raw) if len(row["git_oid"]) == 40 else hashlib.sha256(raw)).hexdigest()
            mode = "100755" if node.stat().st_mode & 0o111 else "100644"
            if (len(body), hashlib.sha256(body).hexdigest(), oid, mode) != (
                    row["bytes"], row["sha256"], row["git_oid"], row["mode"]):
                raise ValueError("path/mode/bytes/blob/SHA identity differs")
            tracked = subprocess.run(["git", "--literal-pathspecs", "ls-files", "--stage", "-z", "--", path],
                                     cwd=repo, capture_output=True, check=False)
            expected = (mode + " " + oid + " 0\t" + path + "\0").encode("utf-8")
            if tracked.returncode or tracked.stdout != expected:
                raise ValueError("source is untracked, conflicted, or differs from its index object")
            source = sources.get(key)
            if (not isinstance(source, dict) or source.get("path") != path
                    or source.get("sha256") != row["sha256"]
                    or not isinstance(source.get("read_scope"), str) or not source["read_scope"].strip()
                    or [k for k, v in sources.items() if isinstance(v, dict) and v.get("path") == path] != [key]):
                raise ValueError("source key, identity or actual read scope is missing, changed or aliased")
            for name in ("work_keys", "supporting_source_keys"):
                values = row[name]
                if (not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values)
                        or len(values) != len(set(values))):
                    raise ValueError("malformed or duplicate work/support references")
            if (row["role"] not in ("work-source", "review") or not row["work_keys"]
                    or (row["role"] == "work-source" and
                        (len(row["work_keys"]) != 1 or not row["supporting_source_keys"]))
                    or (row["role"] == "review" and row["supporting_source_keys"])):
                raise ValueError("invalid scholarly or review-support role")
            bindings[key] = row
            paths.add(path)
            admitted[path] = dict(row, kind="blob")
        except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
            fail(str(row.get("key") if isinstance(row, dict) else row) + ": " + str(exc))

    primary = {key: row for key, row in bindings.items() if row["role"] == "work-source"}
    added_works = {name for row in primary.values() for name in row["work_keys"]}
    historical = sorted(w["key"] for w in works if w.get("key") not in added_works)
    population = owners.get("baseline_work_population", {})
    digest = hashlib.sha256(json.dumps(historical, separators=(",", ":")).encode()).hexdigest()
    if (not isinstance(population, dict) or population.get("count") != len(historical)
            or population.get("keys_sha256") != digest):
        fail("historical work denominator or identities changed")
    for key, row in bindings.items():
        actual_primary = [w["key"] for w in works if key in w.get("source_keys", [])]
        actual_support = [w["key"] for w in works if key in w.get("supporting_source_keys", [])]
        actual_reading = [w["key"] for w in works if isinstance(w.get("reading_forms", []), list)
                          and any(isinstance(f, dict) and f.get("source") == key
                                  for f in w.get("reading_forms", []))]
        if row["role"] == "review":
            if actual_primary or actual_reading or sorted(actual_support) != sorted(row["work_keys"]):
                fail(key + ": review is not bound exactly as support to its declared works")
            continue
        selected = [w for w in works if w.get("key") == row["work_keys"][0]]
        if (actual_primary != row["work_keys"] or actual_reading != row["work_keys"]
                or actual_support or len(selected) != 1
                or selected[0].get("role") != "synthesis" or selected[0].get("source_keys") != [key]
                or selected[0].get("reading_forms") != [{"source": key, "relationship": "authored-synthesis"}]
                or selected[0].get("supporting_source_keys") != row["supporting_source_keys"]):
            fail(key + ": missing, duplicate, extra or substituted work/support relationship")
        for support_key in row["supporting_source_keys"]:
            support = bindings.get(support_key)
            if (not support or support["role"] != "review"
                    or row["work_keys"][0] not in support["work_keys"]):
                fail(key + ": required exact review support is absent")
                continue
            try:
                # The existing compact review has one ordinary table row per
                # reviewed work: local work link, exact SHA-256, logical bytes.
                tokens = MarkdownIt("commonmark").enable("table").parse(
                    safe_path(repo, support["path"]).read_text(encoding="utf-8"))
                candidates, cells = [], None
                for token in tokens:
                    if token.type == "tr_open":
                        cells = []
                    elif token.type == "inline" and cells is not None:
                        cells.append(token)
                    elif token.type == "tr_close" and cells is not None:
                        links = [resolve_reader_link(repo, support["path"], t.attrGet("href"))
                                 for t in cells[0].children or [] if t.type == "link_open"] if cells else []
                        if (row["path"], "") in links:
                            candidates.append((cells, links))
                        cells = None
                if len(candidates) != 1:
                    raise ValueError("missing or duplicate exact reviewed-work row")
                cells, links = candidates[0]
                if (len(cells) < 3 or links != [(row["path"], "")]
                        or cells[1].content != chr(96) + row["sha256"] + chr(96)
                        or cells[2].content.replace(",", "") != str(row["bytes"])):
                    raise ValueError("review does not bind this work's exact source identity")
            except (ValueError, OSError, UnicodeError) as exc:
                fail(key + ": " + str(exc))
    return admitted, errors



def check_historical_sources(repo, baseline_rows, owners, cross, additions):
    """Bind exactly reviewed originals to history and physically readable science.

    Original path identities and source/work entries stay in the frozen census.
    This finite source-owner disposition is not scientific review, custody or
    permission to delete. Only a validated absent original can cross currentness.
    """
    declared = owners.get("historical_source_bindings", [])
    if declared == []:
        return {}, []
    fields = {"path", "repository_revision", "git_blob", "role", "reading_source", "basis"}
    if (not isinstance(declared, list)
            or any(not isinstance(row, dict) or set(row) != fields
                   or not isinstance(row.get("path"), str) for row in declared)):
        return {}, ["historical-source: malformed finite path dispositions"]
    paths = {row["path"] for row in declared}
    original = set(ORIGINAL_HISTORICAL_PROSE_PATHS)
    mediator = original | set(MEDIATOR_PROSE)
    fisher = mediator | {FISHER_AUDIT}
    typed = fisher | set(TYPED_PROSE)
    if (len(paths) != len(declared) or paths not in
            (original, mediator, fisher, typed, typed | set(CONTINUATION_READER_PROSE),
              typed | set(CONTINUATION_READER_PROSE) | set(T4_READER_PROSE),
              typed | set(CONTINUATION_READER_PROSE) | set(T4_READER_PROSE) | set(NEXT24_PROSE),
               typed | set(CONTINUATION_READER_PROSE) | set(T4_READER_PROSE) | set(NEXT24_PROSE) | set(SPARSE_PRIOR_PROSE))):
        return {}, ["historical-source: expected exactly the original five, mediator seven, Fisher eight, typed twelve, continuation sixteen, T4 twenty-six, next24 fifty or sparse-prior seventy-five path dispositions"]
    admitted, errors = {}, []
    sources = cross.get("sources", {})
    for binding in declared:
        path = binding["path"]
        try:
            blob, identity, size = HISTORICAL_PROSE[path]
            original = baseline_rows.get(path, {})
            if (original.get("kind"), original.get("mode"), original.get("git_oid"),
                    original.get("bytes")) != ("blob", "100644", blob, size):
                raise ValueError("original census identity differs")
            if binding["role"] != "historical-source":
                raise ValueError("the original needs an explicit historical-only role")
            current = sources.get(binding["reading_source"], {})
            review = sources.get(binding["basis"], {})
            scholarly = additions.get(current.get("path"), {})
            support = additions.get(review.get("path"), {})
            if (scholarly.get("key") != binding["reading_source"]
                    or scholarly.get("role") != "work-source"
                    or binding["basis"] not in scholarly.get("supporting_source_keys", [])
                    or support.get("key") != binding["basis"] or support.get("role") != "review"):
                raise ValueError("current scholarship and its existing review owner are required")
            for source, admission in ((current, scholarly), (review, support)):
                node = safe_path(repo, source["path"])
                body = node.read_bytes()
                mode = "100755" if node.stat().st_mode & 0o111 else "100644"
                if (hashlib.sha256(body).hexdigest(), len(body), mode) != (
                        admission["sha256"], admission["bytes"], admission["mode"]):
                    raise ValueError("current scholarly or review edition differs")
            for key, source in sources.items():
                if source.get("path") != path:
                    continue
                if source.get("sha256") != identity:
                    raise ValueError("original reader source identity differs")
                forms = [form for work in cross.get("works", [])
                         for form in work.get("reading_forms", [])
                         if isinstance(form, dict) and form.get("source") == key]
                expected = {"from": key, "to": binding["reading_source"],
                            "kind": "logical-content-incorporated-historical-source-retained",
                            "basis": binding["basis"]}
                relations = [r for r in cross.get("relations", []) if r.get("from") == key
                             and r.get("kind") == expected["kind"]]
                expected_forms = ([] if path in T4_READER_SUPPORT_PROSE | NEXT24_SUPPORT_PROSE | SPARSE_PRIOR_SUPPORT_PROSE else
                                  [{"source": key, "relationship": "historical-source"}])
                if forms != expected_forms or relations != [expected]:
                    raise ValueError("reader source lacks its exact historical/incorporation relationship")
                if any(key in j.get("source_keys", []) for j in cross.get("reader_journeys", [])):
                    raise ValueError("an ordinary journey still requires this physical source")
            admitted[path] = historical_source_bytes(
                repo, path, binding["repository_revision"], binding["git_blob"])
        except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
            errors.append("historical-source: " + path + ": " + str(exc))
    return admitted, errors


# Exact historical-only source disposition; scientific preservation review36daa0ce.
# No retrieval fallback or physical-removal authority is introduced.
FRONTIER_HISTORY_REVISION = "c47eeb419ea3cdcfbbc0191ded6ddd7223b353ce"
FRONTIER_HISTORY_RECORDS = {'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/ARCHIVE_BUILD_BOUNDARY.yaml': ('2fbf5bd4723e8cf18eb73d75b645e4824024595d',
                                                                                                     '24fcefce930bcf6871159c511338ad0098efa14b7b0db4a23275c846a9bf2e06',
                                                                                                     214),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_DEPENDENCY_AND_FLYWHEEL_UPDATES/PMR-007_DEEP_BA_BE_CENTRAL_DELTA.yaml': ('ee8117f9eccd6beff3a4566a1c84e31024d726f9',
                                                                                                                                                        '8ccb2fb0327b33bef5f52ad760071ea66a4bdaede43404751c942eba31a53f4b',
                                                                                                                                                        858),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_DEPENDENCY_AND_FLYWHEEL_UPDATES/PMR-007_POST_BF_WHOLE_FRONTIER_SELECTION_GATE_V1.yaml': ('17df8182f9c2103cff22fd5600fbe1a20e0dbff3',
                                                                                                                                                                        '78c2a19ceaf8cb75885530d6daa294cd517d5a5d542492cfb1e96a2c918d9409',
                                                                                                                                                                        1844),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_DEPENDENCY_AND_FLYWHEEL_UPDATES/ROLLING_CUSTODY_RECEIPT_DEEP_BA_BE.yaml': ('19cf575f33d16a6713d6b0f8f0583b3a61ea1c24',
                                                                                                                                                          'c15468c0fb3ef5f5af3f935ba99bc31058d5e87fb3dd6f0c382936e255b8c12e',
                                                                                                                                                          594),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_DEPENDENCY_AND_FLYWHEEL_UPDATES/WHOLE_PROGRAM_FRONTIER_ROTATION_LEDGER_AQ_AZ_V1.yaml': ('0f28511582bd8dd88aeb04ceae51f6ec39285d2c',
                                                                                                                                                                       'af232e953969e9c1241aaa5b637c0b89f605ad576ba305306f538f56f2148769',
                                                                                                                                                                       4002),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEAN_AND_FORMALIZATION_MAP/PMR007_FORMALIZATION_MAP.yaml': ('3f750ec2e38a57a54430838e5e6216076c6bd712',
                                                                                                                                           '8086b738be42e797f586013a04df50279bdef42433bc9476a9b79d637191dc56',
                                                                                                                                           5727),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEAN_AND_FORMALIZATION_MAP/PMR007_FORMALIZATION_MAP_AQ_AZ.yaml': ('332790bffbf674d8e411152ef5def65c4d7a96e0',
                                                                                                                                                 'aec05a3eee4341155f0052285584f5dc383c0360b7b774d6f99c9ffe5bf3b7a6',
                                                                                                                                                 1548),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/CURRENT_STATE_AZ.yaml': ('01fb91076b226c8401f90a288953440e302c4b15',
                                                                                                                       '84a8a45b7be1fceaf95f96e113aba85d1416b198631273ecf1db0bbaf0f4e020',
                                                                                                                       981),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BF_ADMISSION_OVERLAY.yaml': ('30b810373b157d4737bd6f61f9dc3148c8742f62',
                                                                                                                                        'fe56e099f2fed7663b10ad999c3412886a969ee68f7ab7e308ee2345b3ec29a9',
                                                                                                                                        2406),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BG_ADMISSION_OVERLAY.yaml': ('838f850f6379eb03005edeaacd3f071760bc8475',
                                                                                                                                        'f2544e177f4b7c5019ac8174096f8f96fd2ffb7d940e7c68bcc733489c702c93',
                                                                                                                                        2140),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BH_ADMISSION_OVERLAY.yaml': ('e6a215a34d29fd39651e0a9735cb17c0c9853a0f',
                                                                                                                                        '88f126c762f4df8d3cc59bc9f415c72ed0ee02fd9358eedc1cd4444be6be5434',
                                                                                                                                        2405),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BI_ADMISSION_OVERLAY.yaml': ('df2493d4e78ca1e42127f68363dec9aa1f6080eb',
                                                                                                                                        'e9de900f77f56ed5cce8965c6d4caedfecc31e0f0eccabeaf7930458c373f22a',
                                                                                                                                        2310),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BJ_ADMISSION_OVERLAY.yaml': ('29cc4ab62d494797730aa60d7f34af7da46d6e5b',
                                                                                                                                        '1f47ce410b0a302535f0fcba98bc59a5d16cb351bb6d477de3417ceec479fd13',
                                                                                                                                        1946),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BK_ADMISSION_OVERLAY.yaml': ('eac537ebad72e3fc5e36088b1fb3aad301b4db8e',
                                                                                                                                        'd17636bb0d84a0ff5edd86c92396898ac6733d4e2aeb59c0ac699d9556747314',
                                                                                                                                        1806),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PROPOSED_RESULT_INDEX_AQ_AZ.yaml': ('5c2c1286fcbb4ad504b5a9c409007b57fb25df56',
                                                                                                                                  '7e364381bc13ff9e9bbe901d1a03aef9b2dac3c2e6d491f86bb19791d97c4384',
                                                                                                                                  2437),
 'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PROPOSED_RESULT_INDEX_BA_BE.yaml': ('b4a46f072602c85ff68b98331b464e9f9d21f788',
                                                                                                                                  '8baf2f274c6689728f59de60a75df13d8d03e562613675c3435db539c7f0134d',
                                                                                                                                  1179)}
FRONTIER_HISTORY_SUPPORT = {'consolidated-foundations': 'foundations/received-actuality-and-intrinsic-necessity.md',
 'consolidated-information-and-inquiry': 'mathematics/information-and-inquiry.md',
 'consolidated-objective-normativity': 'foundations/objective-normativity-and-corrective-cognition.md'}


def _frontier_record_file_state(repo, path, identity, *, allow_absent=False):
    """Read one ordinary fixed identity and retain its complete stable file state."""
    node = Path(repo)
    for ancestor in (node, *node.parents):
        if ancestor.is_symlink():
            raise ValueError('frontier record root contains a symlink')
    for part in path.split('/'):
        if part in ('', '.', '..', '.git') or '\\' in part:
            raise ValueError('unsafe frontier record path')
        node = node / part
        try:
            entry = node.lstat()
        except FileNotFoundError:
            if allow_absent:
                return None
            raise ValueError('current frontier support is absent')
        if stat.S_ISLNK(entry.st_mode):
            raise ValueError('frontier record path contains a symlink')
        if node != Path(repo) / path and not stat.S_ISDIR(entry.st_mode):
            raise ValueError('frontier record ancestor is not a directory')
    if (not stat.S_ISREG(entry.st_mode) or entry.st_nlink != 1
            or entry.st_mode & 0o111 or entry.st_size != identity[2]):
        raise ValueError('frontier record is not an ordinary exact-sized file')
    fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                or before.st_mode & 0o111 or before.st_size != identity[2]):
            raise ValueError('frontier record is not an ordinary exact-sized file')
        body = stream.read()
        after = os.fstat(stream.fileno())
    fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    state = tuple(getattr(before, name) for name in fields)
    final = node.lstat()
    actual = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
              hashlib.sha256(body).hexdigest(), len(body))
    if (actual != identity or state != tuple(getattr(after, n) for n in fields)
            or state != tuple(getattr(final, n) for n in fields)):
        raise ValueError('frontier record bytes or file state differ')
    return state


CENTRAL_PUBLIC_HISTORY_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
CENTRAL_PUBLIC_HISTORY_RECORDS = {
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v1_results.json': ('5fd34db7773639f256f3ebec7aed4cbafc1aabac', 'cd83895b3ef8ec0501fe0cb21e37d0c9f3c86b03278e51835e51f1876cf76959', 8832),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cl_anchor_cover_primary_check_v2_results.json': ('673281f18f0b593948d2df7ea7dbb734027b5dd5', '8484e8099295969760ddab0223778b482e260e1eb69a7c0bd2f802e722aa76f6', 2407),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v1_results.json': ('204ad8f25f3217bdd67d50e8330287cd51d0ed66', '780fd0f7bce609988e0e0e92c468b735c5ee2fe04e587ee459a0f740a2c78381', 525),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cm_objective_fitted_function_primary_check_v2_results.json': ('f44d983d728803f8c2427f95eaaaf6b8c521e7c7', 'c82f11ce9d56c5adfde56942cc0b5b725bf445802139aa3ad151ac6908a01f5c', 565),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v1_failed_results.json': ('785651477832ccbb072cc75af50155b177148a2a', '039a58147dd5aa9ea3b96a050971c67293e97a96a13e361dce3db5e714f196fc', 2799),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v2_results.json': ('1f37d6723ddbd1d13d70c58b550a1e6807e1ad0a', 'bc5c47709a4e783c6d35327215cd8c0c73402a22fd6cebcfb4a554a18aab5646', 2795),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cn_authority_indexed_anchor_primary_check_v3_results.json': ('45f0bccbd77cd6ca4af186884b012a8ed968a037', '4bf52e1ff74a0384a6db5645cd44f5b0871f84a083a6b18317283409c652a0d1', 2795),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v1_results.json': ('e1eb7e352c4fe70e59ae0cff91ddeeb04c4cbb4e', 'a5a8b61ed789e0ee3aa3eee2aad28a2da8f16c5e58c3aa61eff9b6e92913f6a6', 408),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_co_profile_correction_primary_check_v2_results.json': ('b355d3d8ec253779fa4a4998d486d6c11c128a7f', '17d3572cc0866dff23438a8b5cd185d7052456e8dbded683f65dd3304955c5a6', 603),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_distinct_bisimulation_rereview_results.json': ('f89950fa8dea2251d7f2a5c9f98b126e30d07e6b', 'a185c8b2f37dbd743de6abfa2e109a10e125a155e143235498910e6b5f10592f', 1053),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v1_results.json': ('6c6063513181fee22875150d9e36f8b8296bd6f4', '1e3f646e1df4be1c865c2b1a052237196c1db486f77aa7f76c95f1d6409bdc83', 757),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cp_eligible_ui_experiment_primary_check_v2_results.json': ('80f42ef3444bc86186c3979c5c9027b274bdd0b1', '430e46e3e718fcbbce9688139b8e7e2418be806f662a2fabd36688ed5eb5ca5b', 740),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_distinct_fibre_cover_rereview_results.json': ('dd4f79acaeb8395d8612d5500305e1df090a7a78', '2384534787c19c7c8a27c7cf59ad32a865a4e25fc18d2918c5a55424d2437c4f', 248),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v1_results.json': ('0adc064cf4b9d7e2b3ba05687f6a48e72d30b98d', '9f9266588d75cbc61b3b763bbd2ff6c1daf04986ef4087e1123ba569d4328d02', 352),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_cs_partition_refinement_primary_check_v2_results.json': ('7a2fa6e4e6180ca950b3b44dfdf5f8a3b80588ff', '8808624a3bbb09426f95603981ca84e104f96c977d4dc091913b2a69040040e8', 369),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_distinct_conflict_graph_rereview_results.json': ('1a5e61df2ecc45fd07d6fbc3d07fbb6f244ec42b', 'fa16d66f6c7527eb0164c6f4a1151fb2d0ab8a760159ab1fe62dc71f55b22494', 975),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v1_results.json': ('9a52c8eb568a33e83f9c1a8f6d0e6b71294eb111', '26ed4259faa972bbf56f2691de6085a8b3e9c17ae0bac3899612d5d567e8fd8f', 3882),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/checks/pmr007_deep_ct_partial_domain_primary_check_v2_results.json': ('488f34eeb82faa575976fcfbee7ab2e7ba4a627f', '3906cf8498d6858014e7112a4238ad6796690dd7c9ffb86e97b66494cdf2946b', 1168),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_CONCRETE_ARCHITECTURE_MAP_V1.yaml': ('ffc8b62232dfc42ce07ea1aa43d8d458f5a4e8d3', 'ebcc532f9981f0d2a25be1e05e83f1d2a240e6c5696518f6a896823f0d030853', 3918),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V1.yaml': ('2a4ec7fecc1bc1c724323d62ecd71dde5ffcea10', '9eae438bebd069f2ada1ab861bda8290c0b44bd2f3ad0202a4093096ef9e7ca4', 2491),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ck/PMR007_DEEP_CK_SOURCE_FORMAL_WORLD_MODELS_V2.yaml': ('1f81a89d311d51b6aa77c24c7c0b2f371e80af43', '2da6b0cfdde4ea5d5871d17eb3282169df1daf85bcaf4efdf5a14ff982f7738d', 4686),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR-007_DEEP_CL_ADMISSION_OVERLAY.yaml': ('26f53b5f13e3f71a82643d261cc6e1a5f3a593ac', 'ef987bf8670007688841e9ddaa2fc6e85455a67644751b010223801a3a926908', 1390),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V1.yaml': ('f0f12ecc568086ba133836b786dc0cb7b89e5128', '3350c31b6aeae6a13ea23837fb1817fed485f6ad8d11964ba7c22bf6720832bb', 2454),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cl/PMR007_DEEP_CL_ARCHITECTURE_ANCHOR_REGISTRY_V2.yaml': ('9d4365ce30e5d4ba08f622ba925429ef58d83431', '27aa21fac900517a75a0cef30fe99e928c4f43c679c407e7db0bc96fc07d3318', 3162),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR-007_DEEP_CM_ADMISSION_OVERLAY.yaml': ('27eaaf7620fa0d9cbb475ef471fb8ab9ec574ef9', '67f7b3d658ea5ace55558ab590fd0c6cfffef95f15bf295f3fc7443bfe49120d', 1473),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V1.yaml': ('da75ddf4e9288e0b788f22837964e14976b6e956', 'da7d7fddfb87dc56eadfd6bcc5a605601ad847aa5ee97263ba2a1a7eecec7160', 2451),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cm/PMR007_DEEP_CM_OBJECTIVE_FITTED_FUNCTION_MODELS_V2.yaml': ('95dc33114b1b10d7926fd13069ef966e5cbb2ca5', 'c564bf8c94d16ac02b089acb320107a7a7502dbe6b638b6fde987d773b0b9023', 2751),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR-007_DEEP_CN_ADMISSION_OVERLAY.yaml': ('07340bd737e98c68b7bd499398c0b14733473a0b', '4964c5c38a109deb4f680a526deb9b80c9169ed485d6e3e6ec3f8c3524b5c916', 1694),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V1.yaml': ('91eac41938d9363f29b2aaa6cc356d3662f2f721', 'b239062074fcd058f173aed1898fbeece56974673b62cccdce97e8c7cf27c6a8', 2363),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cn/PMR007_DEEP_CN_AUTHORITY_INDEXED_ANCHOR_MODELS_V2.yaml': ('4ba04371b0d153e2385e770c892dfe08ca992906', 'd3787af3cf0554f39fb62f630fb3804cda9f985036d22aa1d615b48e6fc4e614', 3891),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR-007_DEEP_CO_ADMISSION_OVERLAY.yaml': ('5d7b3607d263060f8cd27f4b70f78c5ea858b03c', '561bd97f52d5b076668e0b643215fc64378499d44c8fd3f3f491d1b9935858ef', 1518),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V1.yaml': ('d5cccbe6b4b76936a304852cdf64a67f4f0bfab7', '745a3a7e41cc9c452a0be4e76b58468d18add7fe86a229effd0365d5c092d8f6', 1439),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_co/PMR007_DEEP_CO_PROFILE_MEASURABLE_CORRECTION_MODELS_V2.yaml': ('2ba1b3b358e7505354ac44d20e644a44f2bafb1d', '8406e983c4c36d7803c8cec61bd97e4ad70b0bb77b9e485a9a67450b18edf317', 1935),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR-007_DEEP_CP_ADMISSION_OVERLAY.yaml': ('3ff592b02ff973d55d457a5b2a17012333a9260f', '87c4d60944526bcbe32ea002d913fbd374e8633270aa11c5aeede226424c76c5', 1754),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V1.yaml': ('4c90195800538c0f8bab0841bf61c50a0e975e5e', 'ef27f520e22cab9c3d19c70b8a21287f52695770f98980d2fb310d7feb3b584e', 3033),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cp/PMR007_DEEP_CP_ELIGIBLE_UI_EXPERIMENT_REGISTRY_V2.yaml': ('d9466caca6cf9213595bdfa489d413251fba67b6', 'a1498322eb840c7cb9d88e4c65d0503ac264da961d96d93fe34d589d52e3e42f', 4084),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR-007_DEEP_CQ_ADMISSION_OVERLAY.yaml': ('4037fcd491eba593dadbaab5a89a3fdca61319ca', '70609844141c6fe0f177ea9f0c0078c1f204f0f49e81975dde97940d94403183', 1968),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V1.yaml': ('45b7c1b3e61ab2616702ae6a291e582f10d3d74c', 'e246434684eaa9e6b5c2e203c1dd5dd6dc7cd0f6aa00cb69f34f178f05823910', 2755),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cq/PMR007_DEEP_CQ_NORM_UNCERTAIN_RESTORATION_MODEL_V2.yaml': ('dd3ecc53b8c02865acce709205babe160a241c5d', '258e982a41350546b4bba775088b10cc1a1fc9ca8dbb07be548ddbab85158679', 3383),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V1.yaml': ('dd2ec65d7b6bb9732b022cf3ffe9afc06b7af68a', '207dcc4f28697598805b7242776bd8ca0c539111b2fff25eb0f6d3bd999b5c44', 1340),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cr/PMR007_DEEP_CR_SOURCE_RESTRICTION_MODEL_V2.yaml': ('e2a37b6a0c1e1584ac209eb8bf0432a13f7d60d9', '7e0ce54a6a3f1fb53e816ba8019314ed7bf037803e340ebac69da34b868b50ba', 2515),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR-007_DEEP_CS_ADMISSION_OVERLAY.yaml': ('13b662a5c995a191670c7394335f08ea2fbd4d0a', 'fc35f95ca8d802f6191898806961ec1e4dcac0ba9d535253387bc564b8e86ffa', 928),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V1.yaml': ('188a4d22366041568a9d3b34816159763176247c', '1aff4e8f6e17bc8625cecbce36ce60b18a60aaedd25872b509f6496d811eb84b', 738),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_cs/PMR007_DEEP_CS_REFINEMENT_LATTICE_MODEL_V2.yaml': ('13d956d17c456cc4e05c5f4206cd14fe1c99a9dc', 'cbb0e891acd1bd80b5bfeb12951eb92cb63294a37f796ce814aae4f8efe2444f', 1319),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR-007_DEEP_CT_ADMISSION_OVERLAY.yaml': ('b4f5b958c6b25087f1d7d934d5700bf85bb3b905', '412593543dd7a13ddf77da5c780125b3b9d47b480176949d5ddc63672050da51', 1127),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V1.yaml': ('f364375dc4acb7bc750c01f112af1fd4253a1aa7', '2051a104e5708ed3d359b10c015db876e8c75a229843598a7c6f660532a828f6', 782),
    'docs/project-closure/ar8r-v11/post-merge-proposals/six-lane-v14-intake/central/source-files/PROPOSAL_ARTIFACTS/deep_ct/PMR007_DEEP_CT_PARTIAL_INTERVENTION_MODEL_V2.yaml': ('9cda0d95b4da50eda06e527eb4b75d6771fa67b9', 'e4160767e9d9622a6408c0f39868f802688433ad68d86fe342a015dfd1bff5bd', 2098),
}


ABK_PUBLIC_HISTORY_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
ABK_PUBLIC_HISTORY_RECORDS = {
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AQ_SOURCE_COMPATIBLE_ARCHITECTURE_MODELS_V2.yaml': ('bb110c6493c333eb7ae8b6b09610f53715424a4c', 'b460af8e73d3db6db8ed6223dc24a548b5519efd175eeefca03433d76c690520', 3307),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AR_PROVENANCE_ROOT_EVIDENCE_MODELS_V2.yaml': ('475c318bb1ae3b5db3f0fce01f06d4bf66724409', 'ab7398b15130cdf60bbc1131403a6dbb5008651d876ff56405b43b1716a29a18', 2004),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V2.yaml': ('3c89aa19631f03d2fc1814ad3045cc06bb49fd5c', '991763b96ac886e37c4ff01dfb6e4f3961cda00b57ada958f97aa3b18ddd5a05', 1509),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V2.yaml': ('0d0a7223aa0ff2ee6e4da155b12ee06df152874c', 'be1e7519b3007a18bf856c4e0baf29b0684b729c6d4b42e753274c10198b457a', 1444),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V2.yaml': ('86b3609b228da4e42b50a365bc7b094413719437', '1c3a637ff73691d0f4e7303384c17fbd1b4291626073ced5db4d448b58d611c9', 1461),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V2.yaml': ('f7e067f1195c13211cd8a067c560ba96b4b49e54', '993a403134973bcd90c3c8ead4b9140ab7a4111f6866bf471150a97deae13f44', 1149),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BA_INTERFACE_RELATIVE_CAUSAL_QUOTIENT_MODELS_V1.yaml': ('8c90bb5a7e6608f9219361fb21d14dcd374ab267', '9f01b79e842c9e25a9deccc1f316956a5f25ab52970a87c8a474d89529c66d02', 1215),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BB_JOINT_CAUSAL_INTERFACE_MODELS_V1.yaml': ('cf33648d43be6aa32f9f6112abe4be83caeaa5c4', 'c71f4dd9e225f8fe8da3f5d581daaff8bc37bddfaf886691c068d82db558b053', 875),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BC_UNIVERSAL_INTERFACE_EXPERIMENT_PARITY_MODELS_V1.yaml': ('d8fe3c0b6b5e38d64a508a95c83ae1810e1a27fe', '82beb4c893c0d12eb9727d20ad1428b1aa45397ae567725ddfece1571b4c833c', 660),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BD_LATENT_SOURCE_ORIENTATION_MODELS_V2.yaml': ('c20193aeee354f6fb17727e889062893cd8cc2c8', 'be48fe63092df4f66ff66a0fe52ffbf50c8bfd11f3c05ce67a443fb54bf4c02d', 2159),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V2.yaml': ('69367d117baefe6702b7bcdc22042042bf8e3923', '40e08b9ef186620e9eb988e7e556694bfc94b94e3dd308d15a682ca03dca2291', 1605),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V2.yaml': ('36ad7d6244e5d54eeb650d0f360acd6a45a53c0c', '4ea76f85945aca04192fb5beb74db8b9d3d0307a254de2b329d917d39674aca7', 2069),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BG_INTEGRATED_R5_COMMON_MODEL_V2.yaml': ('23ae320500f7788577a3a9e62f37786b93cee2a2', '97d7482dbf3ed4b50de79699cedc77067323b095dfd6c7eb3afb557acdfcfcc4', 1769),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V2.yaml': ('e272acb828534d7e09b890f07017e172fb9d7dd4', '14bc65a43c165e7c71208fc873160cdcf88cc5be50e49a49cbb68adfbaf55f33', 1646),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V2.yaml': ('ee15782926dbe3ae049c5fc9ccfa530f1866a58f', '27a4e79b4b11916d4047ad7677db26735f886ed7cbb2b01d5bd89754f33da080', 1333),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_COUNTERMODEL_FILES/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V2.yaml': ('01adca7afe96d67a0da61ccb8787c9e267e9208e', 'd6e99abc7d0038a9ff47cb02809d52e8004251b79d5e2164b3aad0dcca66c616', 1082),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BA_ADMISSION_OVERLAY.yaml': ('132b73791a09d81358e33e1f7d9698959c9146a2', '49f6ed3dda0270e58cb85b44c762be4e31620af9deac7249eac364be899e90fa', 1560),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BB_ADMISSION_OVERLAY.yaml': ('23e4ce4a982031b1730c365bca1ec6a3684ea436', '8dd3b5e550662103f8f00b647219d4756a9e182fd6a5b86ae2782812e1e730fe', 1674),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BC_ADMISSION_OVERLAY.yaml': ('0cdaac12accc57d203c0272eda273279d2b792b8', 'c9ead1aeaf5d93742865ef8015556fed11f85b9f9813e9a23c7804400683978a', 1719),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BD_ADMISSION_OVERLAY.yaml': ('6546f5ba202e9fb5e256c22379f61a42069f6665', 'bc66bf8cea8fa9f454ea2cf7c97a0a1e33d50521a1646c519f12c8adbd8e5ab2', 1788),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/PROPOSED_LEDGER_UPDATES/PMR-007_DEEP_BE_ADMISSION_OVERLAY.yaml': ('a532439c13d961df272781b0b7d49a6213d136a6', '12f4e83b712fa0d58b100169644aa17561a74fe6221466e50752d417c07f185b', 1774),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AT_NEUTRAL_INTERVENTIONAL_TRACE_MODELS_V1.yaml': ('81939539fe9ae4b34412e9af80243b69dade62dd', '0ed0bc80aefa85b01a682fbd8d9f0c579b3316372f7dc50a7bd054e0787b7877', 2379),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AV_NEUTRAL_BRIDGE_INTERPOLATION_MODELS_V1.yaml': ('8535624b656ca283113d322fecbc566290912f4e', '82cee72fcc9a4135275de39175a69d5b603ca62eaf2d3c9f87df9fabeed5c82c', 1292),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AW_PROVENANCE_ROOT_ROBUST_DIAGNOSIS_MODELS_V1.yaml': ('6471321e88bf946175d204afb78650463332f70b', '132d6bc9ea2de7927682ff4822ad611c3f5d43af17329130df2aeeac13cb8b69', 1042),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AX_SOURCE_TESTIMONY_WORLD_GATE_MODELS_V1.yaml': ('c7a8d6fa611e9a5f7535f701ceb66b0805fe7c17', 'a5429ef4ae52c5a62c13eb56d9b2098673b2b04013a051e22aa87648c853b993', 1549),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_AZ_CROSSED_SEMANTIC_INTERVENTION_MODELS_V1.yaml': ('84eb89781eb35bbf74dfa74e78ee32bc332a7e89', 'b5d353a56596143c1f02001e571e2d4bfd635331c08bf26530f6850b77c3a29f', 955),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BD_LATENT_SOURCE_RELIABILITY_ORIENTATION_MODELS_V1.yaml': ('d8fb38df99a36119cdfd9d0cd7b027599d304256', '1433c3131749f686a2823fe0e9d7c27d6f6b1b4b64c05ff7d0bbd747bf3f5c6c', 2345),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BE_CROSS_LANE_JOINT_INTERACTION_MODELS_V1.yaml': ('991381e40dbc0a041a79b3375bba389320c3af14', 'bcc3caaf8ee5fe6910de9b0f4eb80939388fed07ae02e307437723a5a2825e72', 1362),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BF_IMPERSONAL_LATENT_REALIZATION_MODELS_V1.yaml': ('7c94adf7f1f36a636ba8cf24139fcdea66269e9d', 'db4f7664cd22dc28425e5fa5da03cac18645ec3b72856b87ec5f11aee5a104fb', 1375),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BH_TRUTH_CALIBRATED_CORRECTION_MODELS_V1.yaml': ('3996ff60410db02f1ccd11f9cba4f36b1ba8f0b7', '864b04f56a250ed8ad05dacfbd4970a0343367a0b0feaecab2bba9de34a13066', 1455),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BI_FINITE_ARTICULABILITY_MODELS_V1.yaml': ('68add8fc26f0f801b6e4b20ead7d5b93681be1cc', '4a4e5b750c57c3b4a65934c7edd4de495a74ce00c0d8eadd511651bb93eda0e5', 910),
    'docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk/REJECTED_AND_BLOCKED_EVIDENCE/PMR007_DEEP_BK_NECESSITY_CONCRETENESS_MODELS_V1.yaml': ('19306d597907bb1fc1508e484d250b82e7905555', '1317a7369c5daf99935a085cd03b8b60eeec87c3c6ce640f4494d17acab8f966', 1041),
}


def check_abk_public_absences(repo, baseline_rows):
    """Qualify only the fixed32 public records after exact pinned-reader admission.

    Original native objects, whole selected projection rows and ordinary current
    nodes are mandatory even when every working file is present. No corruption
    becomes a fallback, and only stable physical absence grants a D allowance.
    """
    try:
        paths = sorted(ABK_PUBLIC_HISTORY_RECORDS)
        revision = ABK_PUBLIC_HISTORY_REVISION
        if len(paths) != 32 or revision != '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c':
            raise ValueError('exact abk public population and revision are required')
        states = {}
        for path in paths:
            blob, digest, size = ABK_PUBLIC_HISTORY_RECORDS[path]
            row = baseline_rows.get(path, {})
            if (row.get('kind'), row.get('mode'), row.get('git_oid'), row.get('bytes')) != (
                    'blob', '100644', blob, size):
                raise ValueError('abk original census identity differs')
            states[path] = _frontier_record_file_state(repo, path, (blob, digest, size), allow_absent=True)
        manifest_path = 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        node = Path(repo)
        for ancestor in (node, *node.parents):
            if ancestor.is_symlink():
                raise ValueError('abk projection root contains a symlink')
        for part in manifest_path.split('/'):
            node = node / part
            entry = node.lstat()
            if stat.S_ISLNK(entry.st_mode):
                raise ValueError('abk projection path contains a symlink')
            if node != Path(repo) / manifest_path and not stat.S_ISDIR(entry.st_mode):
                raise ValueError('abk projection ancestor is not a directory')
        if not stat.S_ISREG(entry.st_mode) or entry.st_nlink != 1 or entry.st_mode & 0o111:
            raise ValueError('abk projection must be an ordinary file')
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        state = tuple(getattr(entry, name) for name in fields)
        fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_mode & 0o111
                    or tuple(getattr(before, name) for name in fields) != state):
                raise ValueError('abk projection descriptor differs')
            manifest_bytes = stream.read()
            after = os.fstat(stream.fileno())
        if (tuple(getattr(after, name) for name in fields) != state
                or tuple(getattr(node.lstat(), name) for name in fields) != state):
            raise ValueError('abk projection changed during reading')
        manifest_identity = (hashlib.sha1(b'blob ' + str(len(manifest_bytes)).encode() + b'\0'
                                         + manifest_bytes).hexdigest(),
                             hashlib.sha256(manifest_bytes).hexdigest(), len(manifest_bytes))
        if _frontier_record_file_state(repo, manifest_path, manifest_identity) != state:
            raise ValueError('abk projection initial state differs')
        def unique_object(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('duplicate abk projection JSON key')
                result[key] = value
            return result
        manifest = json.loads(manifest_bytes.decode('utf-8'), object_pairs_hook=unique_object)
        if not isinstance(manifest, dict) or not isinstance(manifest.get('objects'), list):
            raise ValueError('abk projection object list is required')
        selected = {}
        for row in manifest['objects']:
            if not isinstance(row, dict):
                raise ValueError('abk projection has a non-object row')
            # Unpublished/identity-only metadata has no repository path.
            # Only the fixed selected population can grant absence permission.
            if 'repository_path' not in row:
                continue
            path = row['repository_path']
            if not isinstance(path, str):
                raise ValueError('abk projection has an invalid path')
            if path in ABK_PUBLIC_HISTORY_RECORDS:
                if path in selected:
                    raise ValueError('abk projection selected row is duplicated')
                selected[path] = row
        if set(selected) != set(paths):
            raise ValueError('abk projection selected population differs')
        for path in paths:
            blob, digest, size = ABK_PUBLIC_HISTORY_RECORDS[path]
            expected = dict(source_sha256=digest, source_action='include', source_bytes=size,
                            role='qualified_metadata', declared_eligibility_basis='reviewed_distribution_metadata',
                            required_dependencies=[], disposition='REUSE', repository_path=path,
                            public_sha256=digest, public_bytes=size,
                            publication_basis='exact_existing_public_repository_object',
                            repository_revision=revision, git_blob=blob)
            if selected[path] != expected:
                raise ValueError('abk projection selected row identity or policy differs')
        def git(*args):
            return _administrative_git(repo, *args)
        if git('cat-file', '-t', revision) != b'commit\n':
            raise ValueError('abk original revision is not a commit')
        expected_tree = b''.join(('100644 blob ' + ABK_PUBLIC_HISTORY_RECORDS[p][0]
                                 + '\t' + p + '\0').encode() for p in paths)
        if git('ls-tree', '-z', revision, '--', *paths) != expected_tree:
            raise ValueError('abk original tree population differs')
        indexed = git('ls-files', '--stage', '-z', '--', *paths)
        expected_index = {('100644 ' + ABK_PUBLIC_HISTORY_RECORDS[p][0]
                          + ' 0\t' + p).encode() for p in paths}
        index_rows = indexed.split(b'\0')
        if (index_rows[-1] != b'' or len(index_rows[:-1]) != len(set(index_rows[:-1]))
                or not set(index_rows[:-1]) <= expected_index):
            raise ValueError('abk index differs or is conflicted')
        for path in paths:
            expected = ABK_PUBLIC_HISTORY_RECORDS[path]
            body = git('cat-file', 'blob', expected[0])
            actual = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                      hashlib.sha256(body).hexdigest(), len(body))
            if actual != expected:
                raise ValueError('abk original body identity differs')
        if git('ls-files', '--stage', '-z', '--', *paths) != indexed:
            raise ValueError('abk index changed during qualification')
        if any(_frontier_record_file_state(repo, p, ABK_PUBLIC_HISTORY_RECORDS[p], allow_absent=True)
               != states[p] for p in paths):
            raise ValueError('abk absence or present file state changed')
        if _frontier_record_file_state(repo, manifest_path, manifest_identity) != state:
            raise ValueError('abk projection state changed during qualification')
        return {p for p in paths if states[p] is None}, []
    except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
        return set(), ['abk-public-history: ' + str(exc)]


def check_central_public_absences(repo, baseline_rows):
    """Qualify only the fixed47 public records after exact pinned-reader admission.

    Original native objects, whole selected projection rows and ordinary current
    nodes are mandatory even when every working file is present. No corruption
    becomes a fallback, and only stable physical absence grants a D allowance.
    """
    try:
        paths = sorted(CENTRAL_PUBLIC_HISTORY_RECORDS)
        revision = CENTRAL_PUBLIC_HISTORY_REVISION
        if len(paths) != 47 or revision != '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c':
            raise ValueError('exact central public population and revision are required')
        states = {}
        for path in paths:
            blob, digest, size = CENTRAL_PUBLIC_HISTORY_RECORDS[path]
            row = baseline_rows.get(path, {})
            if (row.get('kind'), row.get('mode'), row.get('git_oid'), row.get('bytes')) != (
                    'blob', '100644', blob, size):
                raise ValueError('central original census identity differs')
            states[path] = _frontier_record_file_state(repo, path, (blob, digest, size), allow_absent=True)
        manifest_path = 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        node = Path(repo)
        for ancestor in (node, *node.parents):
            if ancestor.is_symlink():
                raise ValueError('central projection root contains a symlink')
        for part in manifest_path.split('/'):
            node = node / part
            entry = node.lstat()
            if stat.S_ISLNK(entry.st_mode):
                raise ValueError('central projection path contains a symlink')
            if node != Path(repo) / manifest_path and not stat.S_ISDIR(entry.st_mode):
                raise ValueError('central projection ancestor is not a directory')
        if not stat.S_ISREG(entry.st_mode) or entry.st_nlink != 1 or entry.st_mode & 0o111:
            raise ValueError('central projection must be an ordinary file')
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        state = tuple(getattr(entry, name) for name in fields)
        fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_mode & 0o111
                    or tuple(getattr(before, name) for name in fields) != state):
                raise ValueError('central projection descriptor differs')
            manifest_bytes = stream.read()
            after = os.fstat(stream.fileno())
        if (tuple(getattr(after, name) for name in fields) != state
                or tuple(getattr(node.lstat(), name) for name in fields) != state):
            raise ValueError('central projection changed during reading')
        manifest_identity = (hashlib.sha1(b'blob ' + str(len(manifest_bytes)).encode() + b'\0'
                                         + manifest_bytes).hexdigest(),
                             hashlib.sha256(manifest_bytes).hexdigest(), len(manifest_bytes))
        if _frontier_record_file_state(repo, manifest_path, manifest_identity) != state:
            raise ValueError('central projection initial state differs')
        def unique_object(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('duplicate central projection JSON key')
                result[key] = value
            return result
        manifest = json.loads(manifest_bytes.decode('utf-8'), object_pairs_hook=unique_object)
        if not isinstance(manifest, dict) or not isinstance(manifest.get('objects'), list):
            raise ValueError('central projection object list is required')
        selected = {}
        for row in manifest['objects']:
            if not isinstance(row, dict):
                raise ValueError('central projection has a non-object row')
            # Unpublished/identity-only metadata has no repository path.
            # Only the fixed selected population can grant absence permission.
            if 'repository_path' not in row:
                continue
            path = row['repository_path']
            if not isinstance(path, str):
                raise ValueError('central projection has an invalid path')
            if path in CENTRAL_PUBLIC_HISTORY_RECORDS:
                if path in selected:
                    raise ValueError('central projection selected row is duplicated')
                selected[path] = row
        if set(selected) != set(paths):
            raise ValueError('central projection selected population differs')
        for path in paths:
            blob, digest, size = CENTRAL_PUBLIC_HISTORY_RECORDS[path]
            expected = dict(source_sha256=digest, source_action='include', source_bytes=size,
                            role='qualified_metadata', declared_eligibility_basis='reviewed_distribution_metadata',
                            required_dependencies=[], disposition='REUSE', repository_path=path,
                            public_sha256=digest, public_bytes=size,
                            publication_basis='exact_existing_public_repository_object',
                            repository_revision=revision, git_blob=blob)
            if selected[path] != expected:
                raise ValueError('central projection selected row identity or policy differs')
        def git(*args):
            return _administrative_git(repo, *args)
        if git('cat-file', '-t', revision) != b'commit\n':
            raise ValueError('central original revision is not a commit')
        expected_tree = b''.join(('100644 blob ' + CENTRAL_PUBLIC_HISTORY_RECORDS[p][0]
                                 + '\t' + p + '\0').encode() for p in paths)
        if git('ls-tree', '-z', revision, '--', *paths) != expected_tree:
            raise ValueError('central original tree population differs')
        indexed = git('ls-files', '--stage', '-z', '--', *paths)
        expected_index = {('100644 ' + CENTRAL_PUBLIC_HISTORY_RECORDS[p][0]
                          + ' 0\t' + p).encode() for p in paths}
        index_rows = indexed.split(b'\0')
        if (index_rows[-1] != b'' or len(index_rows[:-1]) != len(set(index_rows[:-1]))
                or not set(index_rows[:-1]) <= expected_index):
            raise ValueError('central index differs or is conflicted')
        for path in paths:
            expected = CENTRAL_PUBLIC_HISTORY_RECORDS[path]
            body = git('cat-file', 'blob', expected[0])
            actual = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                      hashlib.sha256(body).hexdigest(), len(body))
            if actual != expected:
                raise ValueError('central original body identity differs')
        if git('ls-files', '--stage', '-z', '--', *paths) != indexed:
            raise ValueError('central index changed during qualification')
        if any(_frontier_record_file_state(repo, p, CENTRAL_PUBLIC_HISTORY_RECORDS[p], allow_absent=True)
               != states[p] for p in paths):
            raise ValueError('central absence or present file state changed')
        if _frontier_record_file_state(repo, manifest_path, manifest_identity) != state:
            raise ValueError('central projection state changed during qualification')
        return {p for p in paths if states[p] is None}, []
    except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
        return set(), ['central-public-history: ' + str(exc)]


def check_frontier_record_absences(repo, baseline_rows, owners, cross, additions):
    """Qualify sixteen reviewed historical absences, never supply a read fallback.

    This is source/work/support receiving, not scientific review, custody or
    permission to delete. All originals authenticate before any absence returns.
    """
    declared = owners.get('frontier_history_disposition')
    if declared is None:
        return set(), []
    paths = sorted(FRONTIER_HISTORY_RECORDS)
    expected = {'role': 'historical-only', 'repository_revision': FRONTIER_HISTORY_REVISION,
                'source_paths': paths, 'reading_sources': sorted(FRONTIER_HISTORY_SUPPORT),
                'basis': 'scientific-consolidation-review'}
    try:
        if declared != expected or len(paths) != 16:
            raise ValueError('exact reviewed sixteen-record disposition is required')
        def git(*args):
            result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                    cwd=repo, capture_output=True, check=False)
            if result.returncode:
                raise ValueError('frontier record native identity evidence unavailable')
            return result.stdout
        states = {}
        for path in paths:
            blob, sha, size = FRONTIER_HISTORY_RECORDS[path]
            row = baseline_rows.get(path, {})
            if (row.get('kind'), row.get('mode'), row.get('git_oid'), row.get('bytes')) != (
                    'blob', '100644', blob, size):
                raise ValueError('frontier record original census identity differs')
            states[path] = _frontier_record_file_state(repo, path, (blob, sha, size), allow_absent=True)
        sources = cross.get('sources', {})
        if any(source.get('path') in FRONTIER_HISTORY_RECORDS for source in sources.values()):
            raise ValueError('a current crosswalk source still requires a historical record')
        support_states = {}
        review_key = expected['basis']
        review_source = sources.get(review_key, {})
        review = additions.get(review_source.get('path'), {})
        if review.get('key') != review_key or review.get('role') != 'review':
            raise ValueError('current exact review support is required')
        for key, path in FRONTIER_HISTORY_SUPPORT.items():
            source = sources.get(key, {})
            admission = additions.get(path, {})
            if (source.get('path') != path or admission.get('key') != key
                    or admission.get('role') != 'work-source'
                    or review_key not in admission.get('supporting_source_keys', [])
                    or not admission.get('work_keys')
                    or not set(admission['work_keys']) <= set(review.get('work_keys', []))):
                raise ValueError('current frontier science and review relationship differs')
        for key, path in {**FRONTIER_HISTORY_SUPPORT, review_key: review_source['path']}.items():
            source, admission = sources[key], additions[path]
            identity = (admission['git_oid'], admission['sha256'], admission['bytes'])
            if admission.get('mode') != '100644' or source.get('sha256') != identity[1]:
                raise ValueError('current frontier support metadata differs')
            support_states[path] = (identity, _frontier_record_file_state(repo, path, identity))
        support_paths = sorted(support_states)
        support_index = b''.join(('100644 ' + support_states[p][0][0] + ' 0\t' + p + '\0').encode()
                                 for p in support_paths)
        if git('ls-files', '--stage', '-z', '--', *support_paths) != support_index:
            raise ValueError('current frontier support index differs')
        revision = FRONTIER_HISTORY_REVISION
        if git('cat-file', '-t', revision) != b'commit\n':
            raise ValueError('frontier record original revision is not a commit')
        expected_tree = b''.join(('100644 blob ' + FRONTIER_HISTORY_RECORDS[p][0] + '\t' + p + '\0').encode()
                                 for p in paths)
        if git('ls-tree', '-z', revision, '--', *paths) != expected_tree:
            raise ValueError('frontier record original tree population differs')
        indexed = git('ls-files', '--stage', '-z', '--', *paths)
        expected_index = {('100644 ' + FRONTIER_HISTORY_RECORDS[p][0] + ' 0\t' + p).encode() for p in paths}
        rows = indexed.split(b'\0')
        if (rows[-1] != b'' or len(rows[:-1]) != len(set(rows[:-1]))
                or not set(rows[:-1]) <= expected_index):
            raise ValueError('frontier record index differs or is conflicted')
        for path in paths:
            identity = FRONTIER_HISTORY_RECORDS[path]
            body = git('cat-file', 'blob', identity[0])
            actual = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                      hashlib.sha256(body).hexdigest(), len(body))
            if actual != identity:
                raise ValueError('frontier record original body identity differs')
        if git('ls-files', '--stage', '-z', '--', *paths) != indexed:
            raise ValueError('frontier record index changed during qualification')
        if any(_frontier_record_file_state(repo, p, FRONTIER_HISTORY_RECORDS[p], allow_absent=True) != states[p]
               for p in paths):
            raise ValueError('frontier record actual absence set or present state changed')
        if any(_frontier_record_file_state(repo, p, identity) != before
               for p, (identity, before) in support_states.items()):
            raise ValueError('current frontier support changed during qualification')
        if git('ls-files', '--stage', '-z', '--', *support_paths) != support_index:
            raise ValueError('current frontier support index changed during qualification')
        return {p for p in paths if states[p] is None}, []
    except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
        return set(), ['frontier-history: ' + str(exc)]


CONTINUATION_OWNER_PATHS = (
    "docs/provenance/v5-research-continuations/EVIDENCE_BINDINGS.json",
    "docs/provenance/v5-research-continuations/README.md",
    "docs/provenance/v5-research-continuations/SOURCE_MAP.json",
    "experiments/orthemology-v5-continuations/registry.json",
)
CONTINUATION_OWNER_ORIGINAL = {
    CONTINUATION_OWNER_PATHS[0]: ("1c4ab596107c4573e5b6b8ec053551edb0123e37",
        "eea355a54d547170b57b48d66263a0527f783d84c076fe30bcb6f192ae51d56b", 2216593),
    CONTINUATION_OWNER_PATHS[1]: ("14f2a432915bb24800c80ec4dbab37cf37bdf149",
        "ee7df681b2545e99a9f951b6a6916f45d9ad898af60ef69735505aa482bd3fb7", 44289),
    CONTINUATION_OWNER_PATHS[2]: ("0f565ab802d53fae8a3a929e65f291e3dade7242",
        "a6c2c87082f27c8560cfb4790059cc242effb5f45e3f7bdf30adf8b722b808c7", 5990901),
    CONTINUATION_OWNER_PATHS[3]: ("d90b5647de1cf290d3b7dbe20a805983c75f0fcf",
        "51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff", 192971),
}
CONTINUATION_OWNER_CURRENT = {'docs/provenance/v5-research-continuations/EVIDENCE_BINDINGS.json': ('d3442f385e96d16d83bdb6de3c3d22d9069a7d2d',
                                                                      'c379b06184091ef65c71ec53836c45d82faf18edc72f0e66a5b854a9631f086c',
                                                                      2124501),
 'docs/provenance/v5-research-continuations/README.md': ('25b47c9b01a2e1bff5d98b66e95968a94cbfd8ca',
                                                         '1afc3bdde01b03fdfa58b325d2089f95d972554a1af63ce1e7ca231501c5b6f0',
                                                         47487),
 'docs/provenance/v5-research-continuations/SOURCE_MAP.json': ('c5da80acfdf209cb3c96a73576f362be1f5be292',
                                                               'e7cce0f3ad6c7742ea2b3702963dfad8920e06e3f1208f15656d926922e64725',
                                                               5942902),
 'experiments/orthemology-v5-continuations/registry.json': ('d8a37112646af3922ffe6a7ee86d1ded72996b54',
                                                            '53eff919af5543ce3750f988c0b1c10422dd3ba883f9fbfc77b4840650a86258',
                                                            175135)}

CONTINUATION_OWNER_SPARSE_PRIOR = dict(CONTINUATION_OWNER_CURRENT, **{
    'docs/provenance/v5-research-continuations/README.md': ('b0195c6b5f1db05ff38ba01ced7390a7d46929dc', 'fc1eb9a3fb03e334670571838c045e46d16dd5a770993a796f323b0711d52b3e', 52968)})


def check_continuation_owner_edition(repo, baseline_rows):
    """Bind four existing owners to one exact original or consolidated edition."""
    if not set(CONTINUATION_OWNER_PATHS).intersection(baseline_rows):
        return {}, []
    try:
        for path in CONTINUATION_OWNER_PATHS:
            blob, _, size = CONTINUATION_OWNER_ORIGINAL[path]
            row = baseline_rows.get(path, {})
            if (row.get("kind"), row.get("mode"), row.get("git_oid"), row.get("bytes")) != (
                    "blob", "100644", blob, size):
                raise ValueError("original census identity differs: " + path)
        # This fixed metadata query has its own native scope; it is not a diff
        # request covered by HeldReaderDiffBoundary and requests no blob bodies.
        staged = subprocess.run(
            ["git", "--no-replace-objects", "--literal-pathspecs", "ls-files", "--stage", "-z",
             "--", *CONTINUATION_OWNER_PATHS], cwd=repo, capture_output=True, check=False)
        if staged.returncode:
            raise ValueError("could not inspect the four staged owners")
        edition = None
        for candidate in (CONTINUATION_OWNER_ORIGINAL, CONTINUATION_OWNER_CURRENT, CONTINUATION_OWNER_SPARSE_PRIOR):
            expected = b"".join(("100644 " + candidate[path][0] + " 0\t" + path + "\0").encode()
                                for path in CONTINUATION_OWNER_PATHS)
            if staged.stdout == expected:
                edition = candidate
                break
        if edition is None:
            raise ValueError("staged owners are not one complete accepted edition")
        for ancestor in (Path(repo), *Path(repo).parents):
            if ancestor.is_symlink():
                raise ValueError("continuation owner root contains a symlink")
        for path in CONTINUATION_OWNER_PATHS:
            blob, identity, size = edition[path]
            node = safe_path(repo, path)
            fd = os.open(node, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, "rb") as stream:
                before = os.fstat(stream.fileno())
                if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                        or before.st_mode & 0o111 or before.st_size != size):
                    raise ValueError("owner is not an ordinary exact-sized file: " + path)
                body = stream.read()
                after = os.fstat(stream.fileno())
            fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size", "st_mtime_ns", "st_ctime_ns")
            if any(getattr(before, name) != getattr(after, name) for name in fields):
                raise ValueError("owner changed during the ordinary read: " + path)
            actual_blob = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
            if (actual_blob, hashlib.sha256(body).hexdigest(), len(body)) != (blob, identity, size):
                raise ValueError("worktree and staged owner editions differ: " + path)
        if edition is CONTINUATION_OWNER_ORIGINAL:
            return {}, []
        return {path: {"path": path, "kind": "blob", "mode": "100644", "git_oid": edition[path][0],
                       "bytes": edition[path][2]} for path in CONTINUATION_OWNER_PATHS}, []
    except (ValueError, OSError) as exc:
        return {}, ["continuation-owner: " + str(exc)]


def check_corpus_currentness(repo, baseline, admitted_paths=(), historical_paths=(), navigation_paths=(),
                            continuation_owners=(), fixture_owners=(), frontier_paths=(), central_paths=(), abk_paths=()):
    """New/changed tracked sources cannot disappear behind a frozen census.

    Compare the index and actual worktree separately with the approved commit.
    A combined diff alone can hide a staged change behind worktree absence or
    restored bytes. Operational reader edits retain their exact owners/checks;
    new corpus material needs a finite source/work/support admission. This is
    not a source classifier or an external-literature crawl.
    """
    errors = []
    editable = REFACTOR_EDIT_PATHS | set(admitted_paths)
    duplicate_paths = {}
    try:
        duplicate_paths['next250'] = NEXT250.snapshot(repo)[1]
    except (ValueError, OSError) as exc:
        errors.append('corpus-currentness: NEXT250 evidence: ' + str(exc))
        duplicate_paths['next250'] = set()
    try:
        duplicate_paths['new250'] = new250_absences(repo) if NEW250_PATHS else set()
        old_classes = (CHECKPOINT_COPY_PATHS, CHECKPOINT_RECORD_COPY_PATHS, CHECKPOINT_PACKAGE_COPY_PATHS,
                       FORMAL_COPY_PATHS, FORMAL_PROVIDER_PATHS, CHECKPOINT_CODE_COPY_PATHS,
                       DIGEST_RECORD_PATHS, SUCCESSOR_READ_BATCH_PATHS, SUCCESSOR_REMAINDER_BATCH_PATHS,
                       FIRST50_ASSURANCE_PATHS)
        if any(NEW250_PATHS.intersection(population) for population in old_classes):
            raise ValueError('NEW250 overlaps an existing finite provider')
    except (ValueError, OSError, UnicodeError) as exc:
        errors.append('corpus-currentness: NEW250 evidence: ' + str(exc))
        duplicate_paths['new250'] = set()
    qualified_frontier = (set(frontier_paths) & set(FRONTIER_HISTORY_RECORDS)) if frontier_paths else set()
    qualified_central = (set(central_paths) & set(CENTRAL_PUBLIC_HISTORY_RECORDS)) if central_paths else set()
    qualified_abk = (set(abk_paths) & set(ABK_PUBLIC_HISTORY_RECORDS)) if abk_paths else set()
    continuation_paths = None
    for cached in (True, False):
        result = readonly_git_diff(repo,
            ["git", "diff", *(["--cached"] if cached else []),
             "--no-ext-diff", "--no-textconv", "--no-renames",
             "--name-status", "-z", baseline, "--"],
        )
        if result.returncode:
            return ["corpus-currentness: could not compare the approved corpus with the index/worktree candidate"]
        try:
            values = result.stdout.decode("utf-8").rstrip("\0").split("\0") if result.stdout else []
            if len(values) % 2:
                raise ValueError("malformed tracked change")
        except (UnicodeError, ValueError):
            return ["corpus-currentness: a tracked change has an unrepresentable path or status"]
        for prefix, qualify in ((PMR007_DEEP_PREFIX, pmr007_deep_duplicate_paths),
                                (PMR007_ROUNDS_PREFIX, pmr007_rounds_duplicate_paths)):
            if prefix not in duplicate_paths and any(
                    status == "D" and path.startswith(prefix + "/") and path not in qualified_frontier
                    for status, path in zip(values[::2], values[1::2])):
                try:
                    duplicate_paths[prefix] = qualify(Path(repo))
                except (ValueError, OSError, UnicodeError) as exc:
                    errors.append("corpus-currentness: duplicate evidence: " + str(exc))
                    duplicate_paths[prefix] = set()
        # Exact finite aliases retain original identity and a present, unchanged
        # provider. A class qualifier admits actual absences only; neither a
        # staged modification nor a corrupt present alias gains an allowance.
        for key, population, qualify in (
                ("after3384", AFTER3384_PATHS, after3384_absences),
                ("after3634", AFTER3634_PATHS, after3634_absences),
                ("checkpoint-public", CHECKPOINT_PUBLIC_COPY_PATHS, checkpoint_public_duplicate_paths),
                ("checkpoint-copy", set(CHECKPOINT_COPY_PATHS) - CHECKPOINT_PUBLIC_COPY_PATHS, checkpoint_duplicate_paths),
                ("checkpoint-record", set(CHECKPOINT_RECORD_COPY_PATHS) - CHECKPOINT_PUBLIC_COPY_PATHS, checkpoint_record_duplicate_paths),
                ("checkpoint-package", set(CHECKPOINT_PACKAGE_COPY_PATHS) - CHECKPOINT_PUBLIC_COPY_PATHS, checkpoint_package_duplicate_paths),
                ("formal-copy", FORMAL_COPY_PATHS, formal_duplicate_paths),
            ("formal-provider", FORMAL_PROVIDER_PATHS, formal_provider_absences),
                ("checkpoint-code", CHECKPOINT_CODE_COPY_PATHS, checkpoint_code_duplicate_paths),
                ("historical-digest", DIGEST_RECORD_PATHS, digest_record_absences),
                ("successor-read-batch", SUCCESSOR_READ_BATCH_PATHS, successor_read_batch_absences),
                ("first50-assurance", FIRST50_ASSURANCE_PATHS, first50_assurance_absences),
                ("successor-remainder-batch", SUCCESSOR_REMAINDER_BATCH_PATHS, successor_remainder_batch_absences)):
            if key not in duplicate_paths and any(
                    status == "D" and path in population
                    for status, path in zip(values[::2], values[1::2])):
                try:
                    duplicate_paths[key] = qualify(Path(repo))
                except (ValueError, OSError, UnicodeError) as exc:
                    errors.append("corpus-currentness: " + key + " evidence: " + str(exc))
                    duplicate_paths[key] = set()
        rounds_navigation = set()
        if any((status == "D" and path.startswith(PMR007_ROUNDS_PREFIX + "/"))
               or (status == "M" and path == PMR007_ROUNDS_FORMALIZATION)
               for status, path in zip(values[::2], values[1::2])):
            try:
                rounds_navigation.add(pmr007_rounds_formalization_navigation(Path(repo), indexed=cached))
            except (ValueError, OSError, UnicodeError) as exc:
                errors.append("corpus-currentness: rounds navigation: " + str(exc))
        if continuation_paths is None and any(
                status == "D" and path.startswith(CONTINUATION_COPY_ROOT) and path not in NEW250_PATHS
                for status, path in zip(values[::2], values[1::2])):
            try:
                continuation_paths = continuation_duplicate_paths(Path(repo))
            except (ValueError, OSError, UnicodeError) as exc:
                errors.append("corpus-currentness: continuation copy evidence: " + str(exc))
                continuation_paths = set()
        input_paths = set()
        input_owners = set()
        if any((status == "D" and path in SUCCESSOR_INPUT_PATHS)
               or (status == "M" and path == SUCCESSOR_INPUT_REGISTRY)
               for status, path in zip(values[::2], values[1::2])):
            try:
                input_paths = successor_input_absences(repo)
                input_owners.add(SUCCESSOR_INPUT_REGISTRY)
            except (ValueError, OSError) as exc:
                errors.append("corpus-currentness: consolidated input evidence: " + str(exc))
        calculus_paths = set()
        if any(status == "D" and path == SUCCESSOR_CALCULUS_MAP
               for status, path in zip(values[::2], values[1::2])):
            try:
                calculus_paths = successor_calculus_map_absences(repo)
            except (ValueError, OSError) as exc:
                errors.append("corpus-currentness: calculus historical view: " + str(exc))
        generated_paths = set()
        if any(status == "D" and path in GENERATED_FIXTURE_PATHS
               for status, path in zip(values[::2], values[1::2])):
            try:
                generated_paths = generated_fixture_absences(repo)
            except (ValueError, OSError) as exc:
                errors.append("corpus-currentness: live-derived fixture evidence: " + str(exc))
        binding_paths = set()
        if any(status == "D" and binding_record_candidate(path)
               for status, path in zip(values[::2], values[1::2])):
            try:
                binding_paths = binding_record_absences(repo)
            except (ValueError, OSError) as exc:
                errors.append("corpus-currentness: source binding record: " + str(exc))
        status_paths = set()
        status_requests = {path for status, path in zip(values[::2], values[1::2])
                           if status == 'D' and status_record_candidate(path)}
        if status_requests:
            try:
                status_paths = status_record_absences(repo, status_requests)
            except (ValueError, OSError) as exc:
                errors.append('corpus-currentness: historical status source: ' + str(exc))
        sourcing_paths = set()
        if any(status == 'M' and path == 'docs/sourcing/R3-SOURCING-LEDGER.md'
               for status, path in zip(values[::2], values[1::2])):
            try:
                sourcing_paths = reviewed_sourcing_ledger_modifications(repo)
            except (ValueError, OSError) as exc:
                errors.append('corpus-currentness: reviewed sourcing ledger: ' + str(exc))
        authority_paths = set()
        authority_requests = {path for status, path in zip(values[::2], values[1::2])
                              if path in REVIEWED_AUTHORITY_EDITS
                              and status == ('A' if (REVIEWED_AUTHORITY_EDITS[path] is not None
                                  and REVIEWED_AUTHORITY_EDITS[path][2] is None) else 'M')}
        if authority_requests:
            try:
                authority_paths = reviewed_authority_modifications(repo, authority_requests)
            except (ValueError, OSError) as exc:
                errors.append('corpus-currentness: reviewed authority source: ' + str(exc))
        administrative_paths = set()
        if any(status == "D" and path in ADMIN_RECORD_PATHS
               for status, path in zip(values[::2], values[1::2])):
            try:
                administrative_paths = administrative_record_absences(repo)
            except (ValueError, OSError) as exc:
                errors.append("corpus-currentness: frozen administrative evidence: " + str(exc))
        administrative_guides = set()
        for path in ADMIN_GUIDES:
            if any(status == "M" and name == path for status, name in zip(values[::2], values[1::2])):
                try:
                    administrative_guide_source_bytes(repo, path)
                    administrative_guides.add(path)
                except (ValueError, OSError) as exc:
                    errors.append("corpus-currentness: administrative guide: " + str(exc))
        # Five still-live public records retain their exact native bytes. This
        # admits actual absences only, not changed files or historical skips.
        admission_paths = set()
        admission_requests = {path for status, path in zip(values[::2], values[1::2])
                              if status == "D" and path in ADMISSION_RECORD_PATHS}
        for path in sorted(admission_requests):
            try:
                identities = {p: (blob, sha, size) for p, blob, sha, size in ADMISSION_RECORD_MEMBERS}
                identity = identities[path]
                before = _frontier_record_file_state(repo, path, identity, allow_absent=True)
                body = admission_record_bytes(repo, path)
                actual = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                          hashlib.sha256(body).hexdigest(), len(body))
                if actual != identity:
                    raise ValueError('native admission record identity differs')
                after = _frontier_record_file_state(repo, path, identity, allow_absent=True)
                if after != before:
                    raise ValueError('admission record state changed during qualification')
                if before is None:
                    admission_paths.add(path)
            except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
                errors.append('corpus-currentness: admission record evidence: ' + str(exc))
        allowed_duplicates = set().union(*duplicate_paths.values())
        errors.extend("corpus-currentness: " + path +
                      " requires source-baseline and work/support disposition review"
                      for status, path in zip(values[::2], values[1::2])
                      if path not in editable and not
                      ((status == "D" and path in qualified_frontier)
                        or (status == "D" and path in qualified_central)
                        or (status == "D" and path in qualified_abk)
                        or (status == "M" and path in sourcing_paths)
                        or (path in authority_paths and status == ('A' if (
                            REVIEWED_AUTHORITY_EDITS[path] is not None
                            and REVIEWED_AUTHORITY_EDITS[path][2] is None) else 'M'))
                        or (status == "D" and path in HISTORICAL_PROSE and path in historical_paths)
                        or (status == "D" and path in allowed_duplicates)
                        or (status == "D" and path in administrative_paths)
                        or (status == "D" and path in admission_paths)
                        or (status == "D" and path in binding_paths)
                        or (status == "D" and path in status_paths)
                        or (status == "D" and path in input_paths)
                        or (status == "D" and path in calculus_paths)
                        or (status == "M" and path in input_owners)
                        or (status == "D" and path in generated_paths)
                        or (status == "D" and path in (continuation_paths or ()))
                        or (status == "M" and path in rounds_navigation)
                        or (status == "M" and path in administrative_guides)
                         or (status == "M" and path in CONTINUATION_OWNER_PATHS
                             and path in continuation_owners)
                         or (status == "M" and path in STATUS_RECORD_OWNERS
                             and path in continuation_owners)
                         or (status == "M" and path in FIXTURE_CONSUMER_ORIGINAL
                             and path in fixture_owners)
                        or (status == "M" and path in {MEDIATOR_GUIDE, *TYPED_GUIDES, *SUCCESSOR_CALCULUS_GUIDES}
                            and path in navigation_paths)))
    return list(dict.fromkeys(errors))


def check_continuation_provider_additions(repo, baseline_rows, continuation_owners, baseline):
    """Bind unchanged ordinary providers without creating scientific work entries."""
    path = CONTINUATION_OWNER_PATHS[2]
    if path not in continuation_owners:
        return {}, []
    try:
        if not isinstance(baseline, str) or not re.fullmatch(r'[0-9a-f]{40}', baseline):
            raise ValueError('original baseline must be an immutable commit')
        expected = CONTINUATION_OWNER_CURRENT[path]
        owner = continuation_owners[path]
        if (owner.get('kind'), owner.get('mode'), owner.get('git_oid'), owner.get('bytes')) != (
                'blob', '100644', expected[0], expected[2]):
            raise ValueError('source-map owner is not the reviewed current edition')
        body = safe_path(Path(repo), path).read_bytes()
        identity = (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                    hashlib.sha256(body).hexdigest(), len(body))
        if identity != expected:
            raise ValueError('source-map current bytes differ')
        sources = json.loads(body)['sources']
        selected = [r for r in sources if isinstance(r.get('path'), str)
                    and r['path'].startswith('formal/type-theory/')]
        if len(selected) != 206 or len({r['id'] for r in selected}) != 206:
            raise ValueError('ordinary provider source-ID population differs')
        providers, originals = {}, {}
        for row in selected:
            current, sha, size = row['path'], row['sha256'], row['bytes']
            if (not current.endswith('.lean') or not isinstance(row['id'], str) or not row['id']
                    or not re.fullmatch(r'[0-9a-f]{64}', sha)
                    or type(size) is not int or size <= 0
                    or row['projection'] != 'EXACT' or row['derivation'] is not None
                    or row['original_sha256'] != sha
                    or type(row['original_bytes']) is not int or row['original_bytes'] != size):
                raise ValueError('ordinary provider is not an exact original source')
            original = CONTINUATION_COPY_ROOT + sha + '.lean'
            previous = baseline_rows.get(original, {})
            blob = previous.get('git_oid')
            if (current in baseline_rows or previous.get('kind') != 'blob'
                    or previous.get('mode') != '100644' or previous.get('bytes') != size
                    or not isinstance(blob, str) or not re.fullmatch(r'[0-9a-f]{40}', blob)):
                raise ValueError('original provider or destination census identity differs')
            binding = (blob, sha, size)
            if current in providers and providers[current] != binding:
                raise ValueError('one ordinary provider has inconsistent source identities')
            providers[current] = binding
            originals[original] = blob
        if len(providers) != 39 or len(originals) != 39:
            raise ValueError('ordinary provider destination or original population differs')
        original_tree = subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs', 'ls-tree', '-z', baseline,
             '--', *sorted(originals)], cwd=repo, capture_output=True, check=False)
        expected_tree = b''.join(('100644 blob ' + originals[name] + '\t' + name + '\0').encode()
                                 for name in sorted(originals))
        if original_tree.returncode or original_tree.stdout != expected_tree:
            raise ValueError('original provider tree receiving differs or failed')
        admitted = {}
        for name, binding in sorted(providers.items()):
            # Reuse successful original-absence, exact mode/index/body and TOCTOU checks.
            if reviewed_indexed_modification(repo, (name, baseline, None, binding)) != {name}:
                raise ValueError('ordinary provider current receiving is incomplete')
            admitted[name] = {'path': name, 'kind': 'blob', 'mode': '100644',
                              'git_oid': binding[0], 'bytes': binding[2]}
        return admitted, []
    except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
        return {}, ['continuation-provider: ' + str(exc)]


def corpus_currentness_context(repo, indexed, owners, cross):
    """Return the existing authenticated contexts and every qualification error."""
    errors = []
    def fail(code, message):
        errors.append(code + ": " + message)
    continuation_owners, continuation_errors = check_continuation_owner_edition(repo, indexed)
    errors.extend(continuation_errors)
    try:
        # Reuse the discovery edition namespace; original census rows and
        # collection routing remain unchanged. Only this exact pair joins it.
        continuation_owners.update(status_owner_edition(repo, indexed, owners.get("baseline", {})))
    except (ValueError, OSError) as exc:
        fail("status-owner", str(exc))
    fixture_owners, fixture_status, fixture_errors = check_fixture_consumer_edition(repo, indexed)
    errors.extend(fixture_errors)
    additions, addition_errors = check_source_additions(repo, indexed, owners, cross)
    errors.extend(addition_errors)
    providers, provider_errors = check_continuation_provider_additions(
        repo, indexed, continuation_owners, owners.get("baseline", {}).get("commit"))
    errors.extend(provider_errors)
    if set(additions).intersection(providers):
        fail("continuation-provider", "ordinary provider overlaps authored-source admission")
    else:
        additions.update(providers)
    try:
        packed_additions = new250_provider_additions(repo)
        if set(packed_additions).intersection(additions) or set(packed_additions).intersection(indexed):
            raise ValueError('NEW250 provider overlaps baseline or authored additions')
        additions.update(packed_additions)
    except (ValueError, OSError) as exc:
        fail('new250-provider', str(exc))
    try:
        next_additions = NEXT250.snapshot(repo)[2]
        if set(next_additions).intersection(additions) or set(next_additions).intersection(indexed):
            raise ValueError('NEXT250 provider overlaps baseline or authored additions')
        additions.update(next_additions)
    except (ValueError, OSError) as exc:
        fail('next250-provider', str(exc))
    historical, historical_errors = check_historical_sources(repo, indexed, owners, cross, additions)
    errors.extend(historical_errors)
    navigation = {}
    if fixture_status is not None:
        navigation[FIXTURE_STATUS_PATH] = fixture_status
    if SUCCESSOR_INPUT_REGISTRY in indexed:
        try:
            navigation[SUCCESSOR_INPUT_REGISTRY] = successor_input_registry_original_bytes(repo)
        except (ValueError, OSError) as exc:
            fail("navigation-source", SUCCESSOR_INPUT_REGISTRY + ": " + str(exc))
    if PMR007_ROUNDS_PARENT in indexed:
        try:
            navigation[PMR007_ROUNDS_PARENT] = pmr007_rounds_parent_source_bytes(repo)
        except (ValueError, OSError) as exc:
            fail("navigation-source", PMR007_ROUNDS_PARENT + ": " + str(exc))
    if MEDIATOR_GUIDE in indexed:
        try:
            navigation[MEDIATOR_GUIDE] = mediator_guide_source_bytes(repo, allow_original=True)
        except (ValueError, OSError) as exc:
            fail("navigation-source", MEDIATOR_GUIDE + ": " + str(exc))
    for path in SUCCESSOR_CALCULUS_GUIDES:
        if path in indexed:
            try:
                navigation[path] = successor_calculus_guide_source_bytes(repo, path)
            except (ValueError, OSError) as exc:
                fail("navigation-source", path + ": " + str(exc))
    for path in ADMIN_GUIDES:
        if path in indexed:
            try:
                navigation[path] = administrative_guide_source_bytes(repo, path)
            except (ValueError, OSError) as exc:
                fail("navigation-source", path + ": " + str(exc))
    for path in TYPED_GUIDES:
        if path in indexed:
            try:
                navigation[path] = typed_guide_source_bytes(repo, path, allow_original=True)
            except (ValueError, OSError) as exc:
                fail("navigation-source", path + ": " + str(exc))
    return (additions, historical, navigation, continuation_owners, fixture_owners), errors


# Exact existing reader keys, paths, identities and read scopes for the 31 originals.
# This does not remove work/support ownership or reclassify historical evidence.
SUCCESSOR_READ_BATCH_READER_ROWS_SHA256 = '3e7fc81b94a3a30d321296144e23d2568383ac22e7a9742317ade853811de3cf'


def read_batch_reader_sources(repo, sources):
    """Authenticate the unchanged finite reader rows before native source reads."""
    selected = {key: row for key, row in sources.items()
                if isinstance(row, dict) and row.get("path") in SUCCESSOR_READ_BATCH_PATHS}
    if not selected:
        return {}
    raw = json.dumps(selected, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    if hashlib.sha256(raw).hexdigest() != SUCCESSOR_READ_BATCH_READER_ROWS_SHA256:
        raise ValueError("read-batch reader key/path/identity/scope population differs")
    return {row["path"]: successor_read_batch_bytes(repo, row["path"])
            for row in selected.values()}


# Exact selected remainder source rows; existing work and read scopes are retained.
SUCCESSOR_REMAINDER_BATCH_READER_ROWS_SHA256 = 'fb5eb9d1e0bb25eaceee080d75d9c4aab4884758996af9744236d1fd43585949'


def remainder_batch_reader_sources(repo, sources, *, required=False):
    """Authenticate the unchanged finite reader rows before native source reads."""
    selected = {key: row for key, row in sources.items()
                if isinstance(row, dict) and row.get("path") in SUCCESSOR_REMAINDER_BATCH_PATHS}
    if not selected and not required:
        return {}
    raw = json.dumps(selected, sort_keys=True, ensure_ascii=False,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    if hashlib.sha256(raw).hexdigest() != SUCCESSOR_REMAINDER_BATCH_READER_ROWS_SHA256:
        raise ValueError("remainder-batch reader key/path/identity/scope population differs")
    return {row["path"]: successor_remainder_batch_bytes(repo, row["path"])
            for row in selected.values()}



def check(repo, owners, cross):
    """Return precise mechanical errors; an empty list is not semantic acceptance."""
    repo = Path(repo)
    errors = []
    def fail(code, message):
        errors.append(code + ": " + message)
    if owners.get("schema") != "orthemology-reader-owner-map-v1":
        fail("schema", "Unknown owner map")
    if cross.get("schema") != "orthemology-reader-crosswalk-v1":
        fail("schema", "Unknown crosswalk")
    if cross.get("coverage_stage") not in ("representative-pilot", "reader-candidate"):
        fail("stage", "This checker qualifies a representative pilot or reader candidate only")
    if owners.get("external_body_admissions") != []:
        fail("external", "This baseline contract admits no external bodies")
    try:
        rows = entries_at(repo, owners["baseline"]["commit"])
    except (KeyError, ValueError, OSError, UnicodeError) as exc:
        fail("baseline", str(exc))
        return errors
    indexed = {row["path"]: row for row in rows}
    (additions, historical, navigation, continuation_owners, fixture_owners), context_errors = (
        corpus_currentness_context(repo, indexed, owners, cross))
    errors.extend(context_errors)
    frontier_paths, frontier_errors = check_frontier_record_absences(repo, indexed, owners, cross, additions)
    errors.extend(frontier_errors)
    central_paths, central_errors = check_central_public_absences(repo, indexed)
    errors.extend(central_errors)
    abk_paths, abk_errors = check_abk_public_absences(repo, indexed)
    errors.extend(abk_errors)
    errors.extend(check_corpus_currentness(repo, owners["baseline"]["commit"], additions,
                                          historical, navigation, continuation_owners, fixture_owners, frontier_paths, central_paths, abk_paths))
    errors.extend(check_collection_dispositions(rows, owners, cross))
    errors.extend(check_collection_result_routes(repo, owners, cross))
    if owners["baseline"].get("tree"):
        actual_tree = subprocess.run(
            ["git", "rev-parse", owners["baseline"]["commit"] + "^{tree}"],
            cwd=repo, capture_output=True, text=True, check=False,
        )
        if actual_tree.returncode or actual_tree.stdout.strip() != owners["baseline"]["tree"]:
            fail("baseline", "Recorded tree is not the pinned commit tree")
    expected_digest = owners.get("entries_sha256")
    if expected_digest:
        canonical = json.dumps(rows, sort_keys=True, ensure_ascii=False,
                               separators=(",", ":")).encode()
        if hashlib.sha256(canonical).hexdigest() != expected_digest:
            fail("baseline", "Candidate denominator differs from the recorded census")
    groups = owners.get("collections", [])
    group_ids = [c.get("key") for c in groups]
    if len(set(group_ids)) != len(group_ids):
        fail("owner", "Duplicate collection key")
    group_counts = Counter()
    for row in rows:
        path = row["path"]
        assigned = [c["key"] for c in groups if matches(path, c.get("include", []))
                    and not matches(path, c.get("exclude", []))]
        if not assigned:
            fail("unassigned-source", path)
        elif len(assigned) != 1:
            fail("overlapping-source", path)
        else:
            group_counts[assigned[0]] += 1
    for group in groups:
        if "candidate_paths" in group and group["candidate_paths"] != group_counts[group["key"]]:
            fail("owner-count", group["key"] + " count differs from the pinned population")
    discovered_owners = set()
    for group in groups:
        if not group.get("owners"):
            fail("owner", str(group.get("key")) + " has no discovery owner")
        discovered_owners.update(group.get("owners", []))
    for path in sorted(discovered_owners):
        row = continuation_owners.get(path) or indexed.get(path)
        if not row or row["kind"] != "blob" or row["mode"] not in ("100644", "100755"):
            fail("owner", str(path) + " is not a regular pinned discovery owner")
            continue
        try:
            body = (navigation[path] if path in (PMR007_ROUNDS_PARENT, FIXTURE_STATUS_PATH, SUCCESSOR_INPUT_REGISTRY) and path in navigation
                    else safe_path(repo, path).read_bytes())
            raw = b"blob " + str(len(body)).encode("ascii") + b"\0" + body
            digest = (hashlib.sha1(raw) if len(row["git_oid"]) == 40 else hashlib.sha256(raw)).hexdigest()
            if (digest != row["git_oid"]
                    and not permitted_reader_ci_addition(repo, row, body)
                    and not permitted_historical_status_pin(repo, row, body)
                    and not permitted_contributor_navigation(repo, row, body)):
                fail("owner", path + " changed; review its routing scope")
            mode = "100755" if safe_path(repo, path).stat().st_mode & 0o111 else "100644"
            if mode != row["mode"]:
                fail("owner", path + " changed executable mode")
        except (ValueError, OSError) as exc:
            fail("owner", str(path) + ": " + str(exc))

    sources = cross.get("sources", {})
    def physical_reader_source(key, source):
        nonlocal next250_source
        path = source['path']
        NEXT250.reject_alias(path)
        if path in NEXT250.paths:
            body = NEXT250.reader_source(repo, key, source)
            next250_source = True
            return body
        return safe_path(repo, path).read_bytes()
    try:
        new250_sources = new250_reader_sources(repo, sources)
    except (ValueError, TypeError, OSError) as exc:
        fail('new250-source', str(exc))
        new250_sources = {}
    try:
        read_batch_sources = read_batch_reader_sources(repo, sources)
    except (TypeError, ValueError, OSError) as exc:
        fail("read-batch-source", str(exc))
        read_batch_sources = {}
    try:
        remainder_batch_sources = remainder_batch_reader_sources(
            repo, sources, required=cross.get("coverage_stage") == "reader-candidate")
    except (TypeError, ValueError, OSError) as exc:
        fail("remainder-batch-source", str(exc))
        remainder_batch_sources = {}
    for key, source in sources.items():
        try:
            path = source["path"]
            next250_source = False
            new250_source = path in NEW250_PATHS
            read_batch_source = path in SUCCESSOR_READ_BATCH_PATHS
            remainder_batch_source = path in SUCCESSOR_REMAINDER_BATCH_PATHS
            binding_record = False if new250_source or read_batch_source or remainder_batch_source else is_binding_record(repo, path)
            body = (new250_sources[path] if new250_source else
                    read_batch_sources[path] if read_batch_source else
                    remainder_batch_sources[path] if remainder_batch_source else
                    binding_record_bytes(repo, path) if binding_record else
                    historical[path] if path in historical else navigation[path]
                    if path in navigation else administrative_record_bytes(repo, path)
                    if path in ADMIN_RECORD_PATHS else successor_input_bytes(repo, path)
                    if path in SUCCESSOR_INPUT_PATHS else physical_reader_source(key, source))
        except (KeyError, ValueError, OSError) as exc:
            fail("unsafe-source", str(key) + ": " + str(exc))
            continue
        row = indexed.get(path) or additions.get(path)
        if not row or row["kind"] != "blob" or row["mode"] not in ("100644", "100755"):
            fail("unsafe-source", path + " is outside the regular-file baseline")
        else:
            raw = b"blob " + str(len(body)).encode("ascii") + b"\0" + body
            oid = (hashlib.sha1(raw) if len(row["git_oid"]) == 40 else hashlib.sha256(raw)).hexdigest()
            if oid != continuation_owners.get(path, row)["git_oid"]:
                fail("baseline-source" if path in indexed else "source-addition",
                     path + " differs from the independently bound source")
            mode = ("100644" if next250_source or new250_source or read_batch_source or remainder_batch_source or binding_record or path in historical or path in ADMIN_RECORD_PATHS or path in SUCCESSOR_INPUT_PATHS else
                    "100755" if safe_path(repo, path).stat().st_mode & 0o111 else "100644")
            if mode != row["mode"]:
                fail("source-mode", path + " changed executable mode")
        if hashlib.sha256(body).hexdigest() != source.get("sha256"):
            fail("source-drift", str(key) + " requires source/summary review")
        if not source.get("read_scope"):
            fail("source-scope", str(key) + " has no reading or identity-only scope")

    works = cross.get("works", [])
    work_ids = [w.get("key") for w in works]
    duplicates = [key for key, count in Counter(work_ids).items() if count > 1]
    if duplicates:
        fail("duplicate-work", repr(duplicates))
    covered = set()
    for work in works:
        if work.get("role") not in ROLES:
            fail("role", str(work.get("key")) + " has an unsupported role")
        if not work.get("title") or not work.get("source_keys"):
            fail("work", str(work.get("key")) + " lacks title or substantive source")
        for key in work.get("source_keys", []):
            if key not in sources:
                fail("work", str(work.get("key")) + " refers to an absent source")
                continue
            path = sources[key]["path"]
            covered.add(path)
            if path.startswith(("publication/latex/", "artifacts/")):
                fail("generated-work", path + " is a rendering, not another authored source")
        forms = work.get("reading_forms", [])
        if not isinstance(forms, list):
            fail("reading-form", str(work.get("key")) + " has malformed reading forms")
            continue
        for form in forms:
            if not isinstance(form, dict) or form.get("source") not in sources:
                fail("reading-form", str(work.get("key")) + " refers to an absent reading form")
                continue
            if form.get("relationship") == "governed-rendering":
                artifact_id = form.get("artifact_id", work.get("artifact_id", ""))
                expected = "artifacts/" + str(artifact_id) + ".pdf"
                if sources[form["source"]]["path"] != expected:
                    fail("rendering-target", str(work.get("key")) + " points to another rendering")
    for path in owners.get("required_work_sources", []):
        if path not in covered:
            fail("missing-work", path + " disappeared from the independent pilot input list")

    profile_path = owners.get("publication_profile")
    try:
        profile = yaml.safe_load(safe_path(repo, profile_path).read_text())
        artifact_specs = profile["artifacts"]
    except (KeyError, ValueError, OSError, TypeError, yaml.YAMLError) as exc:
        fail("artifact", "Publication owner cannot be read: " + str(exc))
        artifact_specs = []
    def governed_ids(work):
        # A work can have several governed editions. The existing work-level
        # ID remains the default; additional reading forms name the existing
        # publication-profile ID rather than becoming duplicate scholarly works.
        ids = {work["artifact_id"]} if "artifact_id" in work else set()
        forms = work.get("reading_forms", [])
        if isinstance(forms, list):
            for form in forms:
                if isinstance(form, dict) and form.get("relationship") == "governed-rendering":
                    identity = form.get("artifact_id", work.get("artifact_id"))
                    if isinstance(identity, str) and identity:
                        ids.add(identity)
        return ids

    declared = {a["artifact_id"] for a in artifact_specs}
    actual = [identity for work in works for identity in governed_ids(work)]
    if set(actual) != declared or len(actual) != len(set(actual)):
        fail("artifact", "The governed rendering population is missing, extra or duplicated")
    for work in works:
        associated = [a for a in artifact_specs if a["artifact_id"] in governed_ids(work)]
        if not associated:
            continue
        # Every component of every represented edition must remain discoverable.
        # The profile, not a copied synopsis, owns each edition's exact inputs.
        required_paths = {path for artifact in associated for path in artifact["sources"]}
        actual_paths = {sources[k]["path"] for k in work.get("source_keys", []) if k in sources}
        if actual_paths != required_paths:
            fail("composite", str(work.get("key")) + " lost or added an edition source component")
        for artifact in associated:
            if len(artifact["sources"]) > 1 and work.get("role") != "composite-reference":
                fail("composite", artifact["artifact_id"] + " must remain explicitly composite")
            if artifact.get("profile_kind") == "diagnostic-reference" and work.get("role") != "supporting-reference":
                fail("reference-role", artifact["artifact_id"] + " is a diagnostic reference")

    relations = cross.get("relations", [])
    for rel in relations:
        if any(rel.get(field) not in sources for field in ("from", "to", "basis")):
            fail("relation", "A relation lacks a bound endpoint or evidential basis")
    for rule in owners.get("edition_constraints", []):
        relevant = [r for r in relations
                    if sources.get(r.get("from"), {}).get("path") == rule["source"]
                    and sources.get(r.get("to"), {}).get("path") == rule["rendering"]]
        if not relevant or any(r.get("kind") != rule["permitted_relation"]
                               or sources.get(r.get("basis"), {}).get("path") != rule["basis"]
                               for r in relevant):
            fail("edition", rule["source"] + " has lost its explicitly limited source relationship")

    probes = cross.get("probes", [])
    keys = [p.get("key") for p in probes]
    if set(keys) != PROBES or len(keys) != len(set(keys)):
        fail("probe", "Recognition/correction, tensor/geometry and cross-avenue routes are required")
    for probe in probes:
        links = probe.get("works", [])
        source_links = probe.get("sources", [])
        minimum = 2 if probe.get("key") == "cross-avenue" else 1
        if len(set(links)) < minimum or any(w not in work_ids for w in links):
            fail("probe", str(probe.get("key")) + " lacks its substantive work route")
        if not source_links or any(s not in sources for s in source_links):
            fail("probe", str(probe.get("key")) + " lacks its bound source route")
    return errors



READER_PAGES = (
    "RESEARCH-ATLAS.md", "PAPER-CATALOGUE.md", "RESULT-INDEX.md",
    "CURRENT-FRONTIERS.md", "APPLICATIONS.md", "VERIFICATION-GUIDE.md",
)
JOURNEYS = {"J%02d" % i for i in range(1, 8)}


def markdown_index(text):
    """Index ordinary Markdown headings and real links, never fenced decoys.

    The slug rule covers these authored reader headings, not a claim to emulate
    all GitHub rendering features. Explicit HTML id/name anchors are retained.
    Actual rendered reading and semantic adjudication remain separate checks.
    """
    tokens = MarkdownIt("commonmark", {"html": True}).parse(text)
    headings, links, used = [], [], set()
    for i, token in enumerate(tokens):
        if token.type == "heading_open" and token.map:
            inline = tokens[i + 1]
            title = "".join(t.content for t in inline.children or []
                            if t.type in ("text", "code_inline", "image"))
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            candidate, suffix = slug, 0
            while candidate in used:
                suffix += 1
                candidate = slug + "-" + str(suffix)
            used.add(candidate)
            headings.append((candidate, int(token.tag[1:]), token.map[0]))
        if token.type == "inline" and token.map:
            for child in token.children or []:
                if child.type == "link_open":
                    links.append((token.map[0], child.attrGet("href")))
        if token.type in ("html_block", "inline"):
            fragments = ([token.content] if token.type == "html_block" else
                         [c.content for c in token.children or [] if c.type == "html_inline"])
            for fragment in fragments:
                used.update(re.findall(r"\b(?:id|name)=[\"']([^\"']+)[\"']", fragment))
    return {"anchors": used, "headings": headings, "links": links,
            "line_count": len(text.splitlines())}


def resolve_reader_link(repo, owner, href):
    """Return a local (path, fragment), or None for an ordinary external link."""
    if not isinstance(href, str):
        raise ValueError("Missing link target")
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme in ("https", "http") and parsed.netloc:
            return None
        raise ValueError("Unsupported external or machine-local link")
    raw_path = unquote(parsed.path)
    if raw_path.startswith("/") or "\\" in raw_path or "\0" in raw_path:
        raise ValueError("Absolute or unsafe local link")
    rel = posixpath.normpath(posixpath.join(posixpath.dirname(owner), raw_path)) if raw_path else owner
    if rel.startswith("../") or rel in ("..", ".") or ".git" in rel.split("/"):
        raise ValueError("Link escapes the repository reading surface")
    node = Path(repo)
    for part in rel.split("/"):
        node = node / part
        if node.is_symlink():
            raise ValueError("Link follows a symlink")
    if not node.exists() or not (node.is_file() or node.is_dir()):
        raise ValueError("Link target is absent")
    return rel, unquote(parsed.fragment)


def check_reader_pages(repo, cross):
    """Check seven declared routes and six pages, not the truth of their prose."""
    repo = Path(repo)
    errors, indexes, resolved_links = [], {}, {}
    def fail(code, message):
        errors.append(code + ": " + message)
    def index(rel):
        if rel not in indexes:
            indexes[rel] = markdown_index(safe_path(repo, rel).read_text(encoding="utf-8"))
        return indexes[rel]
    page_paths = {"docs/reader/" + name for name in READER_PAGES}
    for rel in sorted(page_paths):
        try:
            page = index(rel)
        except (ValueError, OSError, UnicodeError) as exc:
            fail("reader-page", rel + ": " + str(exc))
            continue
        targets = []
        for line, href in page["links"]:
            try:
                target = resolve_reader_link(repo, rel, href)
                if target is None:
                    continue
                path, fragment = target
                if fragment:
                    if not path.endswith(".md") or fragment not in index(path)["anchors"]:
                        fail("reader-fragment", rel + " -> " + href)
                targets.append((line, path, fragment))
            except (ValueError, OSError, UnicodeError) as exc:
                fail("reader-link", rel + " -> " + str(href) + ": " + str(exc))
        resolved_links[rel] = targets
    if cross.get("coverage_stage") == "reader-candidate":
        # This establishes destination existence. Section-to-work identity
        # remains a separate, per-entry reading qualification.
        for work in cross.get("works", []):
            entry = work.get("catalogue_entry", "")
            rel, separator, fragment = entry.partition("#") if isinstance(entry, str) else ("", "", "")
            if (rel != "docs/reader/PAPER-CATALOGUE.md" or rel not in indexes
                    or not separator or not fragment or fragment not in indexes[rel]["anchors"]):
                fail("catalogue-entry", str(work.get("key")) + " lacks an existing catalogue section")
    journeys = cross.get("reader_journeys", [])
    ids = [j.get("id") for j in journeys if isinstance(j, dict)]
    if set(ids) != JOURNEYS or len(ids) != len(JOURNEYS) or len(ids) != len(journeys):
        fail("journey-map", "All seven distinct J01-J07 reading routes are required")
    sources = cross.get("sources", {})
    for journey in journeys:
        if not isinstance(journey, dict):
            continue
        name = str(journey.get("id"))
        entry = journey.get("entry", "")
        rel, separator, fragment = entry.partition("#") if isinstance(entry, str) else ("", "", "")
        if rel not in page_paths or rel not in indexes or not separator:
            fail("journey-entry", name + " does not enter a reader section")
            continue
        page = indexes[rel]
        selected = [h for h in page["headings"] if h[0] == fragment]
        if len(selected) != 1:
            fail("journey-entry", name + " has an absent or ambiguous entry heading")
            continue
        _, level, start = selected[0]
        end = next((h[2] for h in page["headings"] if h[2] > start and h[1] <= level), page["line_count"])
        targets = {(path, anchor) for line, path, anchor in resolved_links.get(rel, [])
                   if start <= line < end}
        keys = journey.get("source_keys", [])
        if not keys or len(keys) != len(set(keys)):
            fail("journey-target", name + " needs distinct source targets")
        for key in keys:
            source = sources.get(key)
            if not isinstance(source, dict) or not source.get("path"):
                fail("journey-target", name + " has an unbound source target")
                continue
            expected = source["path"]
            required_fragment = journey.get("source_fragments", {}).get(key)
            found = any(path == expected and (required_fragment is None or anchor == required_fragment)
                        for path, anchor in targets)
            if not found:
                fail("journey-target", name + " section does not directly reach " + expected)
    return errors



def check_root_navigation(repo, owners, cross, texts=None):
    """Check root-to-reader routes, source identities and inherited policy.

    This is a navigation/byte-preservation contract, not reader comprehension
    or scholarly acceptance. ``texts`` permits in-memory negative controls;
    every target is still resolved against the real repository.
    """
    errors, indexes, targets, originals = [], {}, {}, {}
    roots = ("README.md", "STATUS.md", "CONTRIBUTING.md")
    bodies = texts if texts is not None else {
        p: safe_path(repo, p).read_text(encoding="utf-8") for p in roots}
    base = owners["baseline"]["commit"]
    for path in roots:
        original = subprocess.run(["git", "show", base + ":" + path],
                                  cwd=repo, capture_output=True, check=False)
        if original.returncode:
            errors.append("root-baseline: " + path)
            continue
        originals[path] = original.stdout
        if "file://" in bodies[path].lower():
            errors.append("root-link: " + path + " contains a machine-local locator")
        page = markdown_index(bodies[path])
        indexes[path] = page
        if not markdown_index(original.stdout.decode())["anchors"] <= page["anchors"]:
            errors.append("root-anchor: " + path + " loses an existing section")
        targets[path] = []
        for line, href in page["links"]:
            try:
                target = resolve_reader_link(repo, path, href)
                if target is None:
                    continue
                rel, fragment = target
                if fragment:
                    body = bodies[rel] if rel in bodies else safe_path(repo, rel).read_text()
                    if not rel.endswith(".md") or fragment not in markdown_index(body)["anchors"]:
                        raise ValueError("source section is absent")
                targets[path].append((line, rel, fragment))
            except (ValueError, OSError, UnicodeError) as exc:
                errors.append("root-link: " + path + " -> " + str(href) + ": " + str(exc))
    if len(originals) != len(roots):
        return errors

    readme = indexes["README.md"]
    headings = {slug: (level, line) for slug, level, line in readme["headings"]}
    required = ("what-to-read", "two-ideas-that-carry-the-theory", "a-worked-case",
                "integration-history")
    if (not set(required) <= headings.keys()
            or not (headings.get("two-ideas-that-carry-the-theory", (0, 10**9))[1]
                    < headings.get("integration-history", (0, -1))[1])
            or not (headings.get("what-to-read", (0, 10**9))[1]
                    < headings.get("integration-history", (0, -1))[1])):
        errors.append("root-order: research and reading routes must precede integration history")
    start = headings.get("what-to-read", (2, -1))[1]
    end = next((line for _, level, line in readme["headings"] if line > start and level <= 2), -1)
    front_routes = {path for line, path, fragment in targets["README.md"]
                    if start < line < end and not fragment}
    expected = {"docs/reader/" + name for name in READER_PAGES}
    if not expected <= front_routes:
        errors.append("root-route: missing distinct front-door destinations: " +
                      ", ".join(sorted(expected - front_routes)))
    # The existing reader check separately verifies the next leg to each exact
    # primary source. Here each journey's page must be a direct root route.
    for journey in cross.get("reader_journeys", []):
        if journey["entry"].partition("#")[0] not in front_routes:
            errors.append("root-journey: " + journey["id"] + " lacks a direct root entrance")
    example = ("examples/compaction-stale-steer.md", "3-five-predicates-that-must-not-be-collapsed")
    if example not in {(p, a) for _, p, a in targets["README.md"]}:
        errors.append("root-example: the worked distinction must reach its actual source section")
    for path, needed in {
        "STATUS.md": {"docs/current-state.yaml", "docs/reader/CURRENT-FRONTIERS.md",
                      "docs/reader/VERIFICATION-GUIDE.md"},
        "CONTRIBUTING.md": {"docs/publication-profile.yaml", "docs/reader/VERIFICATION-GUIDE.md",
                            "docs/project-closure/reader-refactor-issue-35/CROSSWALK.json"},
    }.items():
        if not needed <= {p for _, p, _ in targets[path]}:
            errors.append("root-maintenance: " + path + " lacks its actual owners/reading routes")

    markers = {"README.md": ("example-json-count", "decision-range"),
               "STATUS.md": ("claim-status-by-lane",)}
    for path, fields in markers.items():
        for field in fields:
            begin = "<!-- state:" + field + " -->"
            finish = "<!-- /state:" + field + " -->"
            before = originals[path].decode()
            after = bodies[path]
            if (any(text.count(marker) != 1 for text in (before, after) for marker in (begin, finish))
                    or before.partition(begin)[2].partition(finish)[0]
                    != after.partition(begin)[2].partition(finish)[0]):
                errors.append("root-state: " + path + " altered or duplicated " + field)
    before = originals["CONTRIBUTING.md"]
    raw = b"blob " + str(len(before)).encode() + b"\0" + before
    oid = hashlib.sha1(raw).hexdigest()
    if not permitted_contributor_navigation(repo, {"path": "CONTRIBUTING.md", "git_oid": oid},
                                             bodies["CONTRIBUTING.md"].encode()):
        errors.append("root-policy: inherited CONTRIBUTING bytes must survive before the bounded addition")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--owner-map", default="docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json")
    parser.add_argument("--crosswalk", default="docs/project-closure/reader-refactor-issue-35/CROSSWALK.json")
    args = parser.parse_args()
    try:
        owners = json.loads(safe_path(args.repo, args.owner_map).read_text(), object_pairs_hook=unique_object)
        cross = json.loads(safe_path(args.repo, args.crosswalk).read_text(), object_pairs_hook=unique_object)
        errors = check(args.repo, owners, cross)
        errors.extend(check_reader_pages(args.repo, cross))
        errors.extend(check_root_navigation(args.repo, owners, cross))
    except (KeyError, ValueError, TypeError, OSError) as exc:
        parser.exit(2, "PILOT INPUT ERROR: " + str(exc) + "\n")
    for error in errors:
        print(error)
    print("Mechanical pilot bindings: " + ("FAIL" if errors else "PASS"))
    print("Whole-corpus semantic coverage and independent review: NOT_ESTABLISHED_BY_THIS_CHECK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
