#!/usr/bin/env python3
"""Cross-document consistency validator: the load-bearing agreements between the
registries, the formal core, the manuscript, the overview, the fixtures, and the
schemas. Deterministic; no empirical claim."""
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML required")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def main():
    reg = yaml.safe_load(read("docs/verdict-registry.yaml"))
    aliases = {v["id"]: v["alias"] for v in reg["verdicts"]}
    core_aliases = [aliases[i] for i in reg["core_path"]]

    core = read("theory/orthemic-core-formalization.md")
    ms = read("manuscript/orthemma-ortheme-systems-revised-draft.md")
    ov = read("docs/architecture-overview.md")
    fixtures = json.loads(read("tests/verdict-fixtures.json"))

    # 1. CorePath equation appears identically in core and manuscript, matching the registry
    expected = "{ " + ", ".join(core_aliases) + " }"
    expected_ms = "{" + ", ".join(core_aliases) + "}"
    check("core states the registry CorePath", expected in core, expected)
    check("manuscript states the registry CorePath", expected_ms in ms, expected_ms)

    # 2. Sole entailment stated in both
    check("core states the sole entailment V2b-T_q -> V1_q", "V2b-T_q(e) → V1_q(e)" in core)
    check("manuscript states the sole entailment", "V2b-T_q → V1_q" in ms)

    # 3. Episode signature agreement across core §2.2, manuscript §8.2, and the overview.
    #    R7D Phase K migrated all three from #raw monospace (U+20D7 vec -> notdef) to
    #    $...$ math; the check now verifies the migrated signature COMPONENTS agree in
    #    representation-consistent LaTeX (robust to `;\ ` vs `; ` separators).
    sig_parts = [r"\vec{\mu}, \mathrm{MetaTok}, \pi", r"\vec{C}, \hat{p}",
                 r"\mathcal{Q}", r"\mathrm{hand}_{\mathrm{in}}", r"a, \mathrm{Succ}"]
    check("episode signature (migrated math): core", all(p in core for p in sig_parts))
    check("episode signature (migrated math): manuscript", all(p in ms for p in sig_parts))
    check("episode signature (migrated math): overview", all(p in ov for p in sig_parts))

    # 4. Fixture IDs agree between tests and core fixture table
    fx_ids = [fx["id"] for fx in fixtures["fixtures"]]
    check("fixtures file has F1..F7", fx_ids == ["F1", "F2", "F3", "F4", "F5", "F6", "F7"], str(fx_ids))
    missing = [f for f in fx_ids if ("**%s — " % f) not in core]
    check("core fixture table lists every fixture", not missing, str(missing))
    check("manuscript cites F1–F7", "F1–F7" in ms)

    # 5. Overview verdict list consistent with registry aliases (each core alias mentioned)
    miss = [a for a in core_aliases if a not in ov]
    check("overview mentions every core-path alias", not miss, str(miss))

    # 6. Decision records referenced in current docs exist
    referenced = set(re.findall(r"Decision (\d{4})", core + ms + ov + read("docs/glossary.md")))
    have = {fn[:4] for fn in os.listdir(os.path.join(ROOT, "docs", "decisions")) if fn[:4].isdigit()}
    ghosts = sorted(referenced - have)
    check("every referenced decision record exists", not ghosts, str(ghosts))

    # 7. Zero-burden rule phrased via ReqPath in both (no stray App(e))
    check("zero-burden rule uses ReqPath in core", "V3c ∉ ReqPath(e)" in core)
    check("zero-burden rule uses ReqPath in manuscript", "V3c ∉ ReqPath(e)" in ms)

    # 8. Verdict-record schema enum equals registry IDs (also checked by validate_schemas)
    vr = json.loads(read("schemas/verdict-record.schema.json"))
    check("schema verdict enum equals registry IDs",
          set(vr["$defs"]["verdict_id"]["enum"]) == set(aliases))

    # 9. Definition 10 exists in the manuscript and is cited by the core
    check("manuscript defines the profile space (Definition 10)", "Definition 10 (Profile space" in ms)
    check("core cites manuscript Definition 10", "manuscript Definition 10" in core)

    # 10. Registry files agree with themselves (core+excluded partition) — quick recheck
    ids = [v["id"] for v in reg["verdicts"]]
    check("registry partition (core + excluded = all)",
          set(reg["core_path"]) | set(reg["excluded_from_core"]) == set(ids)
          and not set(reg["core_path"]) & set(reg["excluded_from_core"]))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
