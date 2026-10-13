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


ROLES = {
    "manuscript", "research-note", "component", "composite-reference",
    "preserved-edition", "source-substrate", "synthesis", "review",
    "supporting-reference", "application-proposal",
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
    if cross.get("coverage_stage") != "representative-pilot":
        fail("stage", "This checker qualifies a representative pilot only")
    if owners.get("external_body_admissions") != []:
        fail("external", "This baseline contract admits no external bodies")
    try:
        rows = entries_at(repo, owners["baseline"]["commit"])
    except (KeyError, ValueError, OSError, UnicodeError) as exc:
        fail("baseline", str(exc))
        return errors
    indexed = {row["path"]: row for row in rows}
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
            if digest != row["git_oid"] and not permitted_reader_ci_addition(repo, row, body):
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
            body = safe_path(repo, path).read_bytes()
        except (KeyError, ValueError, OSError) as exc:
            fail("unsafe-source", str(key) + ": " + str(exc))
            continue
        row = indexed.get(path)
        if not row or row["kind"] != "blob" or row["mode"] not in ("100644", "100755"):
            fail("unsafe-source", path + " is outside the regular-file baseline")
        else:
            raw = b"blob " + str(len(body)).encode("ascii") + b"\0" + body
            oid = (hashlib.sha1(raw) if len(row["git_oid"]) == 40 else hashlib.sha256(raw)).hexdigest()
            if oid != row["git_oid"]:
                fail("baseline-source", path + " differs from the independently pinned source")
            mode = "100755" if safe_path(repo, path).stat().st_mode & 0o111 else "100644"
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
    except (KeyError, ValueError, TypeError, OSError) as exc:
        parser.exit(2, "PILOT INPUT ERROR: " + str(exc) + "\n")
    for error in errors:
        print(error)
    print("Mechanical pilot bindings: " + ("FAIL" if errors else "PASS"))
    print("Whole-corpus semantic coverage and independent review: NOT_ESTABLISHED_BY_THIS_CHECK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
