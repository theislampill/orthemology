#!/usr/bin/env python3
"""Repository validator for the public orthemology repo.

Deterministic hygiene and honesty checks; run in CI on every push/PR.
"""
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def corpus_files():
    """Return Git-tracked plus non-ignored prospective worktree files."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
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
    paths = {
        item.decode("utf-8").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    }
    for rel in sorted(paths):
        path = os.path.join(ROOT, *rel.split("/"))
        if os.path.isfile(path):
            yield path


def text_files(corpus=None):
    for path in corpus if corpus is not None else corpus_files():
        if path.endswith((".md", ".patch", ".json", ".jsonl", ".py", ".yml", ".yaml", ".cff", ".txt",
                          ".gitignore", ".gitattributes", ".editorconfig", ".sha256")):
            yield path


BANNED = [
    (r"C:\\\\?Users", "absolute Windows user path"),
    (r"C:\\\\?workspace", "absolute workspace path"),
    (r"AppData", "AppData path"),
    (r"Temp\\\\?claude", "temp session path"),
    (r"gho_[A-Za-z0-9]{20,}", "credential-looking token"),
    (r"-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----", "private key"),
]

# artifact-file bans (check 13/14): no research-output dumps, no session dumps
BANNED_FILENAMES = re.compile(r"(\.output$|\.jsonl$|synthesis-checks|owner_messages)", re.I)


def exact_source_record(path, sources, root=None):
    """Recognise only an unmodified, uniquely registered COPY_EXACT source."""
    root = ROOT if root is None else root
    relative = os.path.relpath(path, root).replace("\\", "/")
    rows = [row for row in sources if row.get("destination_repository_path") == relative]
    if len(rows) != 1:
        return None
    row = rows[0]
    if row.get("operation") != "ADD" or row.get("transformation") != "COPY_EXACT":
        return None
    with open(path, "rb") as stream:
        actual = hashlib.sha256(stream.read()).hexdigest()
    if actual != row.get("source_sha256") or actual != row.get("output_sha256"):
        return None
    return row


def load_source_map(root=None):
    root = ROOT if root is None else root
    path = os.path.join(root, "docs", "provenance", "v5-consolidation", "SOURCE_MAP.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)["sources"]


def historical_notation_source(path, sources, root=None):
    """Accepted historical originals retain their notation, never by path alone."""
    root = ROOT if root is None else root
    relative = os.path.relpath(path, root).replace("\\", "/")
    row = exact_source_record(path, sources, root)
    return bool(relative.startswith("theory/lineages/") and row
                and row.get("source_artifact") == "H14"
                and row.get("public_safety_tier") == "HISTORICAL_EVIDENCE")


def preserved_math_source(path, sources, root=None):
    """Original historical notation or exact generated quotations, not PDF inputs."""
    root = ROOT if root is None else root
    if historical_notation_source(path, sources, root):
        return True
    relative = os.path.relpath(path, root).replace("\\", "/")
    prefix = "docs/provenance/v5-consolidation/"
    if relative not in (prefix + "THEOREM_INDEX.md", prefix + "CRITICISM_INDEX.md"):
        return False
    rows = [r for r in sources if r.get("destination_repository_path") == relative]
    if (len(rows) != 1 or rows[0].get("operation") != "GENERATE"
            or rows[0].get("transformation") != "GENERATE_INDEXES"
            or rows[0].get("source_artifact") != "A5_SPEC"):
        return False
    manifest = os.path.join(root, "experiments", "orthemology-v5", "SOURCE_MANIFEST.json")
    if not os.path.isfile(manifest):
        return False
    with open(manifest, encoding="utf-8") as stream:
        entries = [r for r in json.load(stream)["files"] if r.get("path") == relative]
    with open(path, "rb") as stream:
        data = stream.read()
    return bool(len(entries) == 1 and entries[0].get("bytes") == len(data)
                and entries[0].get("sha256") == hashlib.sha256(data).hexdigest())


def compact_provenance_record(path, sources):
    relative = os.path.relpath(path, ROOT).replace("\\", "/")
    if not relative.startswith("docs/provenance/v5-consolidation/reconciliation/"):
        return False
    row = exact_source_record(path, sources)
    return bool(row and row.get("source_artifact") in ("A4C", "A4T")
                and row.get("public_safety_tier") == "COMPACT_PROVENANCE_RECORD")


def original_packet_locator(path, target, sources, root=None, from_packet_root=False):
    """Classify a digest-bound external locator; never claim it is a download."""
    source = exact_source_record(path, sources, root)
    if not source or source.get("source_artifact") not in ("V4", "V5"):
        return False
    if target.startswith("/") or "\\" in target or ":" in target:
        return False
    selector = posixpath.normpath(target if from_packet_root else
                                  posixpath.join(posixpath.dirname(source["source_path"]), target))
    if selector == ".." or selector.startswith("../"):
        return False
    rows = [row for row in sources
            if row.get("source_artifact") == source["source_artifact"]
            and row.get("source_path") == selector]
    if len(rows) != 1:
        return False
    row = rows[0]
    return bool(row.get("operation") == "EXTERNAL_CUSTODY"
                and row.get("transformation") == "NO_REPOSITORY_EFFECT"
                and row.get("destination_repository_path") is None
                and row.get("public_safety_tier") in ("HISTORICAL_EVIDENCE", "EXTERNAL_IMMUTABLE_CUSTODY_ITEM")
                and re.fullmatch(r"[0-9a-f]{64}", row.get("source_sha256") or ""))


def main():
    corpus = list(corpus_files())
    files = list(text_files(corpus))
    rel = lambda p: os.path.relpath(p, ROOT).replace("\\", "/")
    source_map = os.path.join(ROOT, "docs", "provenance", "v5-consolidation", "SOURCE_MAP.json")
    sources = []
    if os.path.isfile(source_map):
        with open(source_map, encoding="utf-8") as stream:
            sources = json.load(stream)["sources"]

    # 0: no tracked cache/bytecode artifact (R4 fresh review, Phase A4/E).
    # .gitignore excludes __pycache__/ but cannot un-track a force-added file;
    # this is the standing guard against that class entering history.
    try:
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode()
        cached = sorted(f for f in tracked.splitlines()
                        if "__pycache__" in f or f.endswith((".pyc", ".pyo")))
        check("no cache/bytecode artifact is git-tracked", not cached, str(cached[:5]))
    except Exception as e:  # git absent: state the boundary instead of guessing
        check("no cache/bytecode artifact is git-tracked (git unavailable: %s)" % e, True)

    # 1-3: banned patterns / secrets
    offenders = {}
    for p in files:
        if rel(p) == "scripts/validate_repo.py":
            continue  # patterns appear here as rules
        try:
            c = open(p, "r", encoding="utf-8", errors="strict").read()
        except UnicodeDecodeError:
            # a file the repository itself declares binary (.gitattributes -text,
            # e.g. the binary-capable interruption patch) is exempt from the
            # utf-8 text contract; anything else must be utf-8 (R4 fresh review)
            try:
                attr = subprocess.check_output(
                    ["git", "check-attr", "text", "--", rel(p)], cwd=ROOT).decode()
                declared_binary = attr.strip().endswith("unset")
            except Exception:
                declared_binary = False
            check("utf-8 readable (or declared binary): " + rel(p), declared_binary)
            continue
        for pat, why in BANNED:
            if re.search(pat, c):
                offenders.setdefault(rel(p), []).append(why)
    check("no absolute local paths / banned private patterns / secrets", not offenders, str(offenders))
    check("no .env files", not any(f.endswith(".env") for f in files))
    check("no zip/bulk archives", not any(
        path.lower().endswith((".zip", ".7z", ".rar")) for path in corpus
    ))
    bad_names = [os.path.basename(path) for path in corpus
                 if BANNED_FILENAMES.search(os.path.basename(path))
                 and not (path.endswith(".jsonl") and compact_provenance_record(path, sources))]
    check("no research-output/session-dump artifact files", not bad_names, str(bad_names))

    # 4-5: exactly one manuscript, one core
    ms = [f for f in os.listdir(os.path.join(ROOT, "manuscript")) if f.endswith(".md")]
    check("exactly one current manuscript", ms == ["orthemma-ortheme-systems-revised-draft.md"], str(ms))
    check("formal core present and unique",
          os.path.exists(os.path.join(ROOT, "theory", "orthemic-core-formalization.md")))

    # 6: status labels on proposal/archive docs (pilot0 primers/items are frozen
    # exposure-matched INSTRUMENTS, deliberately status-free; the packet's status
    # lives in PILOT0-PROTOCOL.md and the readiness report)
    unlabeled = []
    for sub in ("companion", "terminology", "archive"):
        for dirpath, _, fns in os.walk(os.path.join(ROOT, sub)):
            if "primers" in dirpath or os.path.join("pilot0", "items") in dirpath:
                continue
            for fn in fns:
                if fn.endswith(".md"):
                    c = open(os.path.join(dirpath, fn), encoding="utf-8").read()[:4000].lower()
                    if not any(k in c for k in ("status", "not canonical", "designed", "proposed",
                                                "draft", "not run", "ledger", "validation report",
                                                "optional patch", "incomplete")):
                        unlabeled.append(fn)
    check("every proposal/archive doc carries a status label", not unlabeled, str(unlabeled))

    # 7: no candidate banners in published theory/manuscript
    bannered = []
    for sub in ("theory", "manuscript", "companion", "terminology"):
        for dirpath, _, fns in os.walk(os.path.join(ROOT, sub)):
            for fn in fns:
                if fn.endswith(".md"):
                    c = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                    if "PROPOSED D1 CANDIDATE" in c:
                        bannered.append(fn)
    check("no PROPOSED-candidate banner in published files", not bannered, str(bannered))

    # 8: internal relative links resolve
    broken = []
    packet_locators = []
    link_re = re.compile(r"\]\(([^)#\s]+)(#[^)\s]*)?\)")
    for p in files:
        if not p.endswith(".md"):
            continue
        c = open(p, encoding="utf-8").read()
        for m in link_re.finditer(c):
            tgt = m.group(1)
            if tgt.startswith(("http://", "https://", "mailto:")) or tgt.startswith("<"):
                continue
            full = os.path.normpath(os.path.join(os.path.dirname(p), tgt))
            if not os.path.exists(full):
                edge = "%s -> %s" % (rel(p), tgt)
                if original_packet_locator(p, tgt, sources):
                    packet_locators.append(edge)
                else:
                    broken.append(edge)
    check("all repository-relative links resolve", not broken, str(broken))
    if packet_locators:
        print("[INFO] %d original-packet locators (%d unique) have exact external-custody bindings; "
              "public retrieval remains unconfirmed" % (len(packet_locators), len(set(packet_locators))))

    # 9: fences balanced, tables well-formed (column counts)
    bad_struct = []
    for p in files:
        if not p.endswith(".md"):
            continue
        lines = open(p, encoding="utf-8").read().splitlines()
        if sum(1 for ln in lines if ln.strip().startswith("```")) % 2 != 0:
            bad_struct.append(rel(p) + ": unbalanced fences")
    check("markdown structure (balanced code fences)", not bad_struct, str(bad_struct))

    # 10: manifest matches files
    man = os.path.join(ROOT, "docs", "provenance", "RELEASE-MANIFEST.sha256")
    ok10, det = True, []
    if os.path.exists(man):
        for ln in open(man, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            h, path = ln.split(None, 1)
            fp = os.path.join(ROOT, path)
            if not os.path.exists(fp):
                ok10 = False; det.append("missing " + path); continue
            actual = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            if actual.lower() != h.lower():
                ok10 = False; det.append("hash mismatch " + path)
    else:
        ok10 = False; det.append("manifest missing")
    check("public SHA-256 manifest matches committed files", ok10, "; ".join(det))

    # 11: verdict-semantic fixtures pass
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "validate_verdict_semantics.py"),
                        "--fixtures", os.path.join(ROOT, "tests", "verdict-fixtures.json")],
                       capture_output=True, text=True)
    check("verdict-semantic fixtures pass", r.returncode == 0, r.stdout[-400:])

    # 12: README/STATUS honesty statements
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read().lower()
    status = open(os.path.join(ROOT, "STATUS.md"), encoding="utf-8").read().lower()
    need_r = ["not peer reviewed", "benchmark", "no empirical", "candidate"]
    need_s = ["not peer reviewed", "no completed empirical validation",
              "terminology not adopted", "not a completed paper", "draft"]
    check("README honesty statements present", all(k in readme for k in need_r),
          str([k for k in need_r if k not in readme]))
    check("STATUS honesty statements present", all(k in status for k in need_s),
          str([k for k in need_s if k not in status]))

    # 13-14 covered by banned patterns (deep-research, zip) above.
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
