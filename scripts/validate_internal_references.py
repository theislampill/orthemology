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
must name a successor that does resolve). Anything else must exist.

Deterministic; offline.
"""
import io
import os
import re
import sys

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

SKIP_DIRS = {".git", "__pycache__", "artifacts", "node_modules"}
SCAN_EXT = (".md", ".yaml", ".json", ".py")
PATH_RE = re.compile(
    r"(?:scripts|tests|examples|schemas|references|terminology|companion|theory|"
    r"manuscript|docs)/[A-Za-z0-9._\-/]+\.(?:py|json|yaml|yml|md|bib|txt)")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name,
                         (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


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
    missing = {}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith(SCAN_EXT):
                continue
            src = os.path.relpath(os.path.join(base, fn), ROOT).replace("\\", "/")
            try:
                text = io.open(os.path.join(base, fn), encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            cited = set(PATH_RE.findall(text))
            if fn.endswith(".md"):
                for target in LINK_RE.findall(text):
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    resolved = os.path.normpath(
                        os.path.join(os.path.dirname(src), target)).replace("\\", "/")
                    cited.add(resolved)
            for c in cited:
                if c in exempt:
                    continue
                if c.startswith(".."):
                    # a relative link that normalizes to ABOVE the repository root
                    # cannot be a valid internal reference; silently skipping it
                    # would be a false-negative hole (R4 fresh-review hardening)
                    missing.setdefault(c + " (escapes the repository root)",
                                       set()).add(src)
                    continue
                if not os.path.exists(os.path.join(ROOT, c)):
                    missing.setdefault(c, set()).add(src)

    check("every repository path cited in the corpus resolves (or is a declared exemption)",
          not missing,
          "; ".join("%s <- %s" % (p, sorted(s)[:2]) for p, s in sorted(missing.items())[:6]))

    # exemptions must stay live: an exemption nobody cites any more is stale state
    all_text = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if fn.endswith(SCAN_EXT):
                try:
                    all_text.append(io.open(os.path.join(base, fn), encoding="utf-8").read())
                except (UnicodeDecodeError, OSError):
                    pass
    blob = "\n".join(all_text)
    for p in sorted(exempt):
        others = blob.count(p) - blob.count("- " + p) - blob.count("  - path: " + p)
        check("exemption %s is still actually cited somewhere" % p, others > 0,
              "no document cites it any more — remove the stale exemption")

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
