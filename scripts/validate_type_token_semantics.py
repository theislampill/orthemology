#!/usr/bin/env python3
"""Type/token semantic-role validator (Decision 0009).

Checks CURRENT normative prose for type/token collapses, with semantic-role
allowlisting rather than a blind phrase ban:
  - "concrete ortheme"/"concrete metaortheme"/"sound ortheme"/"objective
    ortheme" fail unless the line is a negating/analyzing context;
  - files using "concrete reason" must declare its interpretive-lens status;
  - files using "sound reason(ing)" must declare bearers/dimensions or cite
    the strict derived definition;
  - "fitrah = metaortheme" style identifications and "tawatur = majority"
    reductions fail anywhere in current prose;
  - the semantic-role registry must contain the Decision-0009 roles;
  - the verdict registry must NOT contain a primitive SOUND_REASON verdict;
  - the strict soundness predicate must be defined as derived.
Deterministic; no network. Historical dirs are out of scope by design.
"""
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

# Current normative prose (historical records, closure audits, and decision
# records — which quote analyzed defective phrasing — are deliberately excluded).
SCOPE = [
    "README.md", "STATUS.md",
    "docs/glossary.md", "docs/architecture-overview.md",
    "theory", "manuscript", "companion", "examples",
]

BANNED_LINE = [
    ("concrete ortheme", "judgment tokens are placements, not orthemes"),
    ("concrete metaortheme", "case-bound governing tokens are metaorthemmata"),
    ("sound ortheme", "soundness belongs to a placement/episode, not the type"),
]
# a line mentioning a banned phrase is allowed when it is negating/analyzing it
NEGATING = re.compile(
    r"not a|not an|never|instead of|replac|reject|forbidden|avoid|wrong|"
    r"mislabel|so-called|rather than|superseded|defect|collaps|two noun classes",
    re.I)

IDENTITY_BANS = [
    (re.compile(r"fi[ṭt]rah\s*(=|is a)\s*(the\s+)?metaortheme", re.I),
     "fitrah must not be identified with a metaortheme without a declared analysis"),
    (re.compile(r"fi[ṭt]rah\s*(=|is)\s*(the\s+)?orthing faculty", re.I),
     "fitrah must not be identified with the orthing faculty"),
    (re.compile(r"taw[āa]tur\s*(=|is|means)\s*(simple\s+|mere\s+)?majority", re.I),
     "tawatur must not be reduced to majority agreement"),
]

SENSE_MARK_CONCRETE = re.compile(r"modern interpretive|Evans|sense A|sense B|Decision 0009|CONCRETE-AND-SOUND-REASON", re.I)
SENSE_MARK_SOUND = re.compile(r"StrictlySoundReasoning|declared (bearer|dimensions)|its proper bearer|bearer and (threshold|dimensions)|dimensions", re.I)


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def iter_files():
    for entry in SCOPE:
        p = os.path.join(ROOT, entry)
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for dirpath, _dirnames, filenames in os.walk(p):
                if "sourcing" in dirpath:
                    continue  # ledgers quote defective historical rows
                for fn in sorted(filenames):
                    if fn.endswith(".md"):
                        yield os.path.join(dirpath, fn)


def main():
    files = list(iter_files())
    check("scope non-empty", len(files) > 5, str(len(files)))

    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        text = open(path, encoding="utf-8").read()
        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            low = line.lower()
            for phrase, why in BANNED_LINE:
                if phrase in low and not NEGATING.search(line):
                    check("%s:%d unqualified '%s'" % (rel, i, phrase), False, why)
            if "objective ortheme" in low and not NEGATING.search(line) \
                    and "shorthand" not in low and "correctly predicated" not in low:
                check("%s:%d 'objective ortheme' without shorthand qualification" % (rel, i), False,
                      "permitted only as declared shorthand")
            for rx, why in IDENTITY_BANS:
                if rx.search(line):
                    check("%s:%d banned identification" % (rel, i), False, why)
        if re.search(r"concrete reason\b", text, re.I) and not SENSE_MARK_CONCRETE.search(text):
            check("%s: 'concrete reason' without sense declaration" % rel, False,
                  "must be labeled as the Evans/Turner interpretive lens or sense-disambiguated")
        if re.search(r"sound reason", text, re.I) and not SENSE_MARK_SOUND.search(text):
            check("%s: 'sound reason' without declared bearer/dimensions" % rel, False,
                  "must declare bearer/dimensions or the strict derived definition")
    check("banned-phrase scan complete over %d files" % len(files), True)

    # role registry
    roles_path = os.path.join(ROOT, "docs", "semantic-roles.yaml")
    reg = yaml.safe_load(open(roles_path, encoding="utf-8"))
    have = {r["id"] for r in reg["roles"]}
    need = {"reasoning_faculty", "reasoning_episode", "judgment_token",
            "represented_meta_type", "metaorthemma_token", "execution_trace",
            "placement_correctness", "pathway_adequacy", "strict_reason_soundness",
            "fitrah_condition", "corroboration_configuration"}
    check("semantic-role registry contains all Decision-0009 roles", need <= have,
          str(sorted(need - have)))
    strict = next(r for r in reg["roles"] if r["id"] == "strict_reason_soundness")
    check("strict_reason_soundness marked derived", strict.get("derived") is True)

    # verdict registry unchanged: no primitive SOUND_REASON
    vreg = yaml.safe_load(open(os.path.join(ROOT, "docs", "verdict-registry.yaml"), encoding="utf-8"))
    ids = {v["id"] for v in vreg["verdicts"]}
    check("no primitive SOUND_REASON verdict in registry", "SOUND_REASON" not in ids)

    # strict soundness defined as derived in the companion note
    note = open(os.path.join(ROOT, "companion", "CONCRETE-AND-SOUND-REASON.md"), encoding="utf-8").read()
    check("StrictlySoundReasoning defined as PathwayAdequate AND TOKEN_TRUTH_LINKED",
          "StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)" in note)
    check("companion note states it is not a registry verdict",
          "not a new primitive verdict" in note or "NOT a registry verdict" in note
          or "No primitive `SOUND_REASON` verdict" in note)

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
