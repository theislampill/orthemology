#!/usr/bin/env python3
"""Internal-reference validator (R4 independent review).

Fails when a document cites a repository path — a script, fixture, example,
schema, decision, reference file, or Markdown link target — that does not exist.

This checker exists because of R4 finding §4. Decision 0011, the companion
prose, and the correction ledger (marked DONE) all cited fixture CR-9,
`examples/shared-upstream-corroboration-failure.json`, and
`scripts/validate_claim_reasoning_paths.py` while none of them was in the tree.
Every validator was green, because no validator compared prose citations against
the filesystem. That is false closure inside a project about false closure, and
this is the check that makes the class impossible to repeat silently.

Two exemption kinds are declared in docs/reference-exemptions.yaml, each with a
stated reason: paths owned by ANOTHER repository (bounded-import provenance),
and deliberately RETIRED paths still named in preserved historical bodies (each
must name a successor that does resolve). A missing path is also tolerated
within one committed implementation plan when that plan declares the path on
an explicit ``- Create:`` inventory line. Other missing paths in the plan and
citations to that path elsewhere remain validated; planned-output treatment
ends once the path exists.

Deterministic; offline.
"""
import io
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

SCAN_EXT = (".md", ".yaml", ".json", ".py")
PATH_PATTERN = (
    r"(?<![A-Za-z0-9._/\\-])"
    r"(?:applications|experiments|scripts|tests|examples|schemas|references|"
    r"terminology|companion|theory|manuscript|docs)[\\/]"
    r"[A-Za-z0-9._/\\-]+\.(?:py|json|yaml|yml|md|bib|txt)"
)
PATH_RE = re.compile(PATH_PATTERN)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
CREATE_LINE_RE = re.compile(
    rf"^\s*-\s+Create:\s+(?:`{PATH_PATTERN}`|{PATH_PATTERN})\s*$"
)
PLAN_RE = re.compile(r"^docs/superpowers/plans/[^/]+\.md$")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name,
                         (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def _git_files(*args):
    """Return normalized repository paths from a NUL-delimited git listing."""
    result = subprocess.run(
        ["git", "ls-files", "-z", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git ls-files failed: "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    return {
        item.decode("utf-8").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    }


def _corpus_files():
    """Return tracked plus non-ignored worktree files in the validation corpus."""
    paths = _git_files("--cached", "--others", "--exclude-standard")
    return sorted(
        path
        for path in paths
        if path.endswith(SCAN_EXT) and os.path.isfile(os.path.join(ROOT, path))
    )


def _committed_plans():
    """Return plans in immutable HEAD, independent of mutable index state."""
    result = subprocess.run(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            "-z",
            "HEAD",
            "--",
            "docs/superpowers/plans",
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git ls-tree HEAD failed: "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    paths = {
        item.decode("utf-8").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    }
    return {path for path in paths if PLAN_RE.fullmatch(path)}


def _resolves(src, cited):
    if os.path.exists(os.path.join(ROOT, cited)):
        return True
    directory = os.path.dirname(src)
    while True:
        if os.path.exists(os.path.normpath(os.path.join(ROOT, directory, cited))):
            return True
        if not directory:
            return False
        directory = os.path.dirname(directory)


def _citation_occurrences(src, text):
    for line in text.splitlines():
        for cited in PATH_RE.findall(line):
            yield cited.replace("\\", "/"), line
        if src.endswith(".md"):
            for target in LINK_RE.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                yield (
                    os.path.normpath(os.path.join(os.path.dirname(src), target)).replace(
                        "\\", "/"
                    ),
                    line,
                )


def _is_planned_output_occurrence(src, cited, line, committed_plans):
    """Return true only for this exact ``- Create:`` occurrence in a HEAD plan."""
    if src not in committed_plans or not CREATE_LINE_RE.fullmatch(line):
        return False
    return cited in {match.replace("\\", "/") for match in PATH_RE.findall(line)}


def main():
    ex = yaml.safe_load(io.open(os.path.join(ROOT, "docs", "reference-exemptions.yaml"),
                                encoding="utf-8"))
    external = set(ex["external_paths"]["paths"])
    retired = {r["path"]: r for r in ex["retired_paths"]["paths"]}

    # every retired entry must name a successor that actually resolves, and every
    # exemption must carry a reason — an exemption list without reasons is just a
    # second place for false closure to hide
    for p, r in sorted(retired.items()):
        check("retired path %s names a resolving successor" % p,
              os.path.exists(os.path.join(ROOT, r.get("successor", ""))),
              "successor %r does not resolve" % r.get("successor"))
        check("retired path %s states a reason" % p, bool(str(r.get("reason", "")).strip()))
    check("external-path exemptions name their owning repository",
          bool(str(ex["external_paths"].get("owner_repository", "")).strip()))

    # an external exemption must not shadow a real local path: if the path exists
    # here, the exemption is wrong (or stale) and would mask a genuine local
    # citation target's future disappearance (R4 fresh-review hardening)
    for p in sorted(external):
        check("external exemption %s does not shadow a local path" % p,
              not os.path.exists(os.path.join(ROOT, p)),
              "the path exists in THIS repository — remove the external exemption")

    exempt = external | set(retired)
    corpus = _corpus_files()
    committed_plans = _committed_plans()
    missing = {}
    corpus_text = {}
    for src in corpus:
        try:
            text = io.open(os.path.join(ROOT, src), encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        corpus_text[src] = text
        for cited, line in _citation_occurrences(src, text):
            if cited in exempt:
                continue
            if cited.startswith(".."):
                # a relative link that normalizes to ABOVE the repository root
                # cannot be a valid internal reference; silently skipping it
                # would be a false-negative hole (R4 fresh-review hardening)
                missing.setdefault(cited + " (escapes the repository root)", set()).add(src)
                continue
            if _resolves(src, cited):
                continue
            if _is_planned_output_occurrence(src, cited, line, committed_plans):
                # Exemption is occurrence-local: only this exact inventory line
                # in a plan present in HEAD may name a not-yet-created output.
                continue
            missing.setdefault(cited, set()).add(src)

    check("every repository path cited in the corpus resolves (or is a declared exemption)",
          not missing,
          "; ".join("%s <- %s" % (p, sorted(s)[:2]) for p, s in sorted(missing.items())[:6]))

    # exemptions must stay live: an exemption nobody cites any more is stale state
    blob = "\n".join(corpus_text.values()).replace("\\", "/")
    for p in sorted(exempt):
        others = blob.count(p) - blob.count("- " + p) - blob.count("  - path: " + p)
        check("exemption %s is still actually cited somewhere" % p, others > 0,
              "no document cites it any more — remove the stale exemption")

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
