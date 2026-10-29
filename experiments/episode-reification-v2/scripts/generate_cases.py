#!/usr/bin/env python3
"""ER-2 deterministic case generator (frozen seed 20260733).

5 archetypes x 4 surface variants = 20 case instances, each rendered from ONE
canonical fact-atom list (stable fact IDs) into both arms:

  fixtures/<case>/baseline-record.md   — chronological audit log of the atoms
  fixtures/<case>/treatment-record.json— the SAME atoms organized into an
      explicit episode-style structure (sections + typed links) with NO
      conclusions: no defect flags, no interpretation-bearing notes, no
      diagnostic titles (audit B8/H1 repair)
  fixtures/KEYS.json                   — hidden scoring truth (archetype,
      defect/remedy categories, closure legitimacy, supporting fact IDs)

public_files() returns only the 60 public renderings in memory. The CLI
requires an explicit output directory; scoring keys require a separate flag.
Case IDs are neutral (C01..C20). The defect must be INFERABLE (e.g. a
reference-data date outside a stated refresh interval), never stated.
"""
import argparse
import io
import json
import os
import random

SEED = 20260733
SUBJECTS = [("valve assembly VA-%d", "acceptance check"),
            ("survey plot SP-%d", "boundary check"),
            ("firmware image FW-%d", "release check"),
            ("sample tray ST-%d", "screening check")]


def facts_for(arch, rng, variant):
    subj_t, review = SUBJECTS[variant % len(SUBJECTS)]
    subj = subj_t % rng.randint(100, 999)
    day = rng.randint(8, 18)
    f = []

    def add(txt):
        f.append({"id": "F%02d" % (len(f) + 1), "text": txt})

    add("Case subject: %s, version v1, under %s." % (subj, review))
    add("The case was opened on 2026-05-%02d." % day)
    key = {"closure_legitimate": False}
    if arch == "A1":  # nominal control
        add("Measurement M-1 was taken on 2026-05-%02d; its scope line covers the checked property; its stated validity is 30 days." % (day + 1))
        add("The measuring procedure's reference data was updated on 2026-05-01; its stated refresh interval is 90 days.")
        add("The operator followed work instruction WI-4; the step log matches WI-4's steps.")
        add("The check result was PASS.")
        add("The obligations table has no open rows.")
        key.update(defect_category="none", remedy_category="none", closure_legitimate=True,
                   supporting=["F03", "F04", "F07"])
    elif arch == "A2":  # stopped-clock
        add("Screen S-2 compares against reference panel RP-A; RP-A's stated refresh interval is 60 days; RP-A was last updated on 2025-11-%02d." % day)
        add("Screen S-2 was run on 2026-05-%02d per its manual; the step log matches the manual." % (day + 1))
        add("Screen S-2 reported NEGATIVE.")
        add("An independent assay on 2026-05-%02d also reported NEGATIVE." % (day + 3))
        add("The draft completion statement declares screening complete on the S-2 result.")
        key.update(defect_category="procedure-reference-out-of-date",
                   remedy_category="update-procedure-reference",
                   supporting=["F03"])
    elif arch == "A3":  # rare miss below resolution
        add("The declared method resolves offsets to 5 cm; its recorded reference-class error rate is within the accepted band.")
        add("Survey E-3 was taken on 2026-05-%02d with a calibrated instrument and full step-log compliance." % (day + 1))
        add("The review concluded CONFORMS.")
        add("A later audit at 1 cm resolution, dated 2026-06-%02d, recorded a 3 cm offset." % day)
        add("The draft completion statement closes the review on the method's result.")
        key.update(defect_category="resolution-limit-miss",
                   remedy_category="add-discriminating-evidence",
                   supporting=["F03", "F06"])
    elif arch == "A4":  # wrong edition bound, faithful execution
        add("The job card lists acceptance standard edition AS-2019 for this case.")
        add("The governing contract row for this case class lists acceptance standard edition AS-2024.")
        add("The inspector applied the edition listed on the job card exactly; the step log matches it.")
        add("Under the applied edition the case PASSES; the margin sheet notes 0.2 units to the limit of the contract-listed edition.")
        add("The draft completion statement records acceptance with no note about editions.")
        key.update(defect_category="wrong-edition-bound",
                   remedy_category="rebind-correct-edition-and-rederive",
                   supporting=["F03", "F04"])
    else:  # A5 metamorphic marker
        add("Verifier V-7's configuration line reads: report result PASS when the output text contains the string 'ANALYSIS COMPLETE'.")
        add("Verifier V-7's declared purpose line reads: verify that the analysis section is complete and correct.")
        add("On this case's output, V-7 reported PASS; the analysis section is present and its figures check out.")
        add("Variant record A: the same output with the marker line removed; V-7 reported FAIL on it.")
        add("Variant record B: a truncated output with wrong figures that contains the marker line; V-7 reported PASS on it.")
        add("The draft completion statement declares verification complete on V-7's PASS.")
        key.update(defect_category="check-tracks-marker-not-property",
                   remedy_category="replace-check-with-property-tracking",
                   supporting=["F03", "F06", "F07"],
                   e5={"neighbor_a_expected_pass": False, "neighbor_b_expected_pass": True})
    return f, key


def render_baseline(case_id, facts):
    out = ["# Audit log — case %s" % case_id, ""]
    for a in facts:
        out.append("%s. [%s] %s" % (a["id"][1:], a["id"], a["text"]))
    out.append("")
    return "\n".join(out)


def render_treatment(case_id, facts):
    """Same atoms, explicit structure, NO conclusions."""
    sections = {"identity": [], "evidence": [], "procedure": [], "execution": [],
                "result": [], "obligations": [], "other": []}
    for a in facts:
        t = a["text"].lower()
        if "case subject" in t or "opened on" in t:
            k = "identity"
        elif "measurement" in t or "survey" in t or "screen s-2 was run" in t or "variant record" in t:
            k = "evidence"
        elif "reference" in t or "configuration line" in t or "purpose line" in t or "edition" in t and "lists" in t:
            k = "procedure"
        elif "followed" in t or "applied" in t or "step log" in t:
            k = "execution"
        elif "result was" in t or "reported" in t or "concluded" in t or "passes" in t:
            k = "result"
        elif "obligation" in t or "completion statement" in t:
            k = "obligations"
        else:
            k = "other"
        sections[k].append({"fact_id": a["id"], "text": a["text"]})
    return {"schema": "orthemology-er2-treatment-record-v1", "case": case_id,
            "note": "structured rendering of the identical fact atoms; links relate records, they do not conclude",
            "sections": {k: v for k, v in sections.items() if v},
            "links": [{"from": a["id"], "relation": "same-case", "to": facts[0]["id"]}
                      for a in facts[1:]]}


def public_cases():
    """Return only public facts; no key file is opened, serialized or returned."""
    rng = random.Random(SEED)
    cases = {}
    for arch in ("A1", "A2", "A3", "A4", "A5"):
        for variant in range(4):
            cid = "C%02d" % (len(cases) + 1)
            cases[cid] = facts_for(arch, rng, variant)[0]
    return cases


def public_files():
    """Render the original public bytes without a permanent fixture directory."""
    files = {}
    for cid, facts in public_cases().items():
        files[cid + "/facts.json"] = json.dumps(
            {"case": cid, "facts": facts}, indent=2, ensure_ascii=False) + "\n"
        files[cid + "/baseline-record.md"] = render_baseline(cid, facts)
        files[cid + "/treatment-record.json"] = json.dumps(
            render_treatment(cid, facts), indent=2, ensure_ascii=False) + "\n"
    return files


def scoring_keys():
    """Explicit scoring-side regeneration; never called by prompt assembly."""
    rng = random.Random(SEED)
    keys = []
    for arch in ("A1", "A2", "A3", "A4", "A5"):
        for variant in range(4):
            cid = "C%02d" % (len(keys) + 1)
            key = facts_for(arch, rng, variant)[1]
            keys.append({"case": cid, "archetype": arch, **key})
    return json.dumps({"schema": "orthemology-er2-keys-v1",
                       "note": "HIDDEN scoring truth — never loaded by the prompt-assembly path",
                       "keys": keys}, indent=2, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True,
                        help="explicit destination for the generated public renderings")
    parser.add_argument("--include-scoring-keys", action="store_true",
                        help="also regenerate scoring truth; never use it as prompt input")
    args = parser.parse_args()
    files = public_files()
    if args.include_scoring_keys:
        files["KEYS.json"] = scoring_keys()
    for relative, text in files.items():
        path = os.path.join(args.output_dir, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
    print("rendered %d cases" % len(public_cases()))


if __name__ == "__main__":
    main()
