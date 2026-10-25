#!/usr/bin/env python3
"""Check a bounded representative reader crosswalk, not scientific truth.

The input population comes from an exact Git baseline, separately from the
editorial sample. Existing publication ownership is read rather than copied into
a competing scientific registry. This checker is read-only and does not fetch
URLs, execute source payloads, extract theorems, or infer semantic acceptance.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

from resolve_t20_v6_source import (
    HISTORICAL_PROSE, HISTORICAL_PROSE_PUBLIC_PATHS, HISTORICAL_PROSE_REVISION,
    historical_source_bytes,
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
    """Admit exactly the reviewed additive CI step, not mutable science owners.

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
    return (before.count(anchor) == 1 and addition not in before
            and body == before.replace(anchor, addition + anchor, 1))



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


def permitted_historical_status_pin(repo, row, body):
    """Admit exact navigation and finite historical-prose bindings, not identities.

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
        return candidate == expected
    except (KeyError, TypeError, ValueError):
        return False



# These are the existing Issue-35 implementation surfaces, not a science
# exclusion by extension or directory name. A new original work even inside
# docs/reader/ requires corpus admission; untracked scratch is not published.
REFACTOR_EDIT_PATHS = {
    "README.md", "STATUS.md", "CONTRIBUTING.md",
    ".github/workflows/validate.yml", ".github/workflows/reader-refactor-snapshot.yml",
    "scripts/reader_census.py", "scripts/check_reader_pilot.py",
    "tests/test_reader_census.py", "tests/test_reader_pilot.py",
    # Exact existing integrity owners changed for the finite history contract;
    # this does not admit any new source path or predecessor modification.
    "scripts/resolve_t20_v6_source.py", "scripts/validate_t20_v6_projection.py",
    "tests/test_t20_v6_projection.py",
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
    if (not isinstance(declared, list) or len(declared) != len(HISTORICAL_PROSE)
            or any(not isinstance(row, dict) or set(row) != fields
                   or not isinstance(row.get("path"), str) for row in declared)
            or {row["path"] for row in declared} != set(HISTORICAL_PROSE)):
        return {}, ["historical-source: expected the five distinct qualified path dispositions"]
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
                if forms != [{"source": key, "relationship": "historical-source"}] or relations != [expected]:
                    raise ValueError("reader source lacks its exact historical/incorporation relationship")
                if any(key in j.get("source_keys", []) for j in cross.get("reader_journeys", [])):
                    raise ValueError("an ordinary journey still requires this physical source")
            admitted[path] = historical_source_bytes(
                repo, path, binding["repository_revision"], binding["git_blob"])
        except (KeyError, TypeError, ValueError, OSError, UnicodeError) as exc:
            errors.append("historical-source: " + path + ": " + str(exc))
    return admitted, errors


def check_corpus_currentness(repo, baseline, admitted_paths=(), historical_paths=()):
    """New/changed tracked sources cannot disappear behind a frozen census.

    Compare the index and actual worktree separately with the approved commit.
    A combined diff alone can hide a staged change behind worktree absence or
    restored bytes. Operational reader edits retain their exact owners/checks;
    new corpus material needs a finite source/work/support admission. This is
    not a source classifier or an external-literature crawl.
    """
    errors = []
    editable = REFACTOR_EDIT_PATHS | set(admitted_paths)
    for cached in (True, False):
        result = subprocess.run(
            ["git", "diff", *(["--cached"] if cached else []),
             "--no-ext-diff", "--no-textconv", "--no-renames",
             "--name-status", "-z", baseline, "--"],
            cwd=repo, capture_output=True, check=False,
        )
        if result.returncode:
            return ["corpus-currentness: could not compare the approved corpus with the index/worktree candidate"]
        try:
            values = result.stdout.decode("utf-8").rstrip("\0").split("\0") if result.stdout else []
            if len(values) % 2:
                raise ValueError("malformed tracked change")
        except (UnicodeError, ValueError):
            return ["corpus-currentness: a tracked change has an unrepresentable path or status"]
        errors.extend("corpus-currentness: " + path +
                      " requires source-baseline and work/support disposition review"
                      for status, path in zip(values[::2], values[1::2])
                      if path not in editable and not
                      (status == "D" and path in HISTORICAL_PROSE and path in historical_paths))
    return list(dict.fromkeys(errors))


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
    additions, addition_errors = check_source_additions(repo, indexed, owners, cross)
    errors.extend(addition_errors)
    historical, historical_errors = check_historical_sources(repo, indexed, owners, cross, additions)
    errors.extend(historical_errors)
    errors.extend(check_corpus_currentness(repo, owners["baseline"]["commit"], additions, historical))
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
        row = indexed.get(path)
        if not row or row["kind"] != "blob" or row["mode"] not in ("100644", "100755"):
            fail("owner", str(path) + " is not a regular pinned discovery owner")
            continue
        try:
            body = safe_path(repo, path).read_bytes()
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
    for key, source in sources.items():
        try:
            path = source["path"]
            body = historical[path] if path in historical else safe_path(repo, path).read_bytes()
        except (KeyError, ValueError, OSError) as exc:
            fail("unsafe-source", str(key) + ": " + str(exc))
            continue
        row = indexed.get(path) or additions.get(path)
        if not row or row["kind"] != "blob" or row["mode"] not in ("100644", "100755"):
            fail("unsafe-source", path + " is outside the regular-file baseline")
        else:
            raw = b"blob " + str(len(body)).encode("ascii") + b"\0" + body
            oid = (hashlib.sha1(raw) if len(row["git_oid"]) == 40 else hashlib.sha256(raw)).hexdigest()
            if oid != row["git_oid"]:
                fail("baseline-source" if path in indexed else "source-addition",
                     path + " differs from the independently bound source")
            mode = ("100644" if path in historical else
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
