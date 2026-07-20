#!/usr/bin/env python3
"""ER-2 run orchestrator (CI uses ONLY the mock adapter).

Assembles auditor prompts ONLY from the public case renderings (baseline log
or treatment record) and the frozen probes; never opens fixtures/KEYS.json
(payload isolation, proven by tests). Strict JSON parsing with one logged
format retry; failures recorded; raw retained; manifest written first.
"""
import argparse
import io
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(HERE)
FIX = os.path.join(PKT, "fixtures")

PROBES = ("Answer about the case record above. Reply with ONLY a JSON object: "
          '{"defect_category": "none|procedure-reference-out-of-date|resolution-limit-miss|'
          'wrong-edition-bound|check-tracks-marker-not-property|other", '
          '"grounding_fact_ids": ["F03", ...], '
          '"remedy_category": "none|update-procedure-reference|add-discriminating-evidence|'
          'rebind-correct-edition-and-rederive|replace-check-with-property-tracking|other", '
          '"endorse_completion": true|false, '
          '"e5": {"neighbor_a_expected_pass": true|false, "neighbor_b_expected_pass": true|false, '
          '"mismatch_identified": true|false} (include e5 only if variant records appear), '
          '"rationale": "..."}')

FORMAT_REMINDER = ("Your previous reply was not valid JSON of the required shape. "
                   "Reply with ONLY the JSON object, no prose.")


def cases():
    return sorted(d for d in os.listdir(FIX) if d.startswith("C") and
                  os.path.isdir(os.path.join(FIX, d)))


def payload(case, arm):
    if arm == "baseline":
        body = io.open(os.path.join(FIX, case, "baseline-record.md"), encoding="utf-8").read()
    else:
        body = json.dumps(json.load(io.open(os.path.join(FIX, case, "treatment-record.json"),
                                            encoding="utf-8")), indent=2)
    return body + "\n\n" + PROBES


class MockAdapter:
    """Deterministic offline auditor; reads ONLY the public rendering."""

    def __call__(self, prompt, seed):
        cautious = '"sections"' in prompt  # treatment structure enables the checks
        p = prompt
        if "refresh interval is 60 days" in p and "2025-11-" in p:
            cat, rem = "procedure-reference-out-of-date", "update-procedure-reference"
            ground = ["F03"]
        elif "1 cm resolution" in p:
            cat, rem = "resolution-limit-miss", "add-discriminating-evidence"
            ground = ["F03", "F06"]
        elif "AS-2024" in p and "job card" in p:
            cat, rem = "wrong-edition-bound", "rebind-correct-edition-and-rederive"
            ground = ["F03", "F04"]
        elif "ANALYSIS COMPLETE" in p:
            cat, rem = "check-tracks-marker-not-property", "replace-check-with-property-tracking"
            ground = ["F03", "F06", "F07"]
        else:
            cat, rem, ground = "none", "none", ["F03"]
        if not cautious:
            cat, rem = "none", "none"  # the baseline mock misses subtle defects
        ans = {"defect_category": cat, "grounding_fact_ids": ground,
               "remedy_category": rem,
               "endorse_completion": (cat == "none"),
               "rationale": "mock deterministic traversal"}
        if "Variant record" in p:
            ans["e5"] = {"neighbor_a_expected_pass": not cautious,
                         "neighbor_b_expected_pass": cautious,
                         "mismatch_identified": cautious}
        return json.dumps(ans)


def parse_strict(text):
    try:
        obj = json.loads(text.strip())
    except Exception:
        return None
    need = ("defect_category", "grounding_fact_ids", "remedy_category", "endorse_completion")
    if not isinstance(obj, dict) or any(k not in obj for k in need):
        return None
    return obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", choices=["mock", "cmd"], required=True)
    ap.add_argument("--cmd", default=None)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--raw", default=None)
    ap.add_argument("--dump-payloads", default=None)
    ap.add_argument("--seed", type=int, default=20260734)
    a = ap.parse_args()

    if a.adapter == "cmd":
        import subprocess

        def adapter(prompt, seed):
            r = subprocess.run(a.cmd, shell=True, input=prompt.encode("utf-8"),
                               capture_output=True)
            return r.stdout.decode("utf-8", errors="replace")
    else:
        adapter = MockAdapter()

    manifest = {"packet_id": "ER-2",
                "run_id": "mock-smoke" if a.adapter == "mock" else "cmd-run",
                "packet_freeze_hash": "recorded-at-freeze",
                "run_authorized_by": ("NONE — synthetic mock traversal"
                                      if a.adapter == "mock" else "SEE OWNER RECORD"),
                "started_at": "1970-01-01T00:00:00Z", "adapter": a.adapter,
                "executor": {"model_id": "mock", "model_version_or_hash": "mock",
                             "provider": "offline"},
                "sampling": {"temperature": 0.0, "top_p": 1.0, "max_output_tokens": 2048},
                "repeats": 1, "seeds": [a.seed],
                "registration_state": "NOT_REGISTERED",
                "synthetic_smoke": a.adapter == "mock"}
    os.makedirs(os.path.dirname(os.path.abspath(a.manifest)), exist_ok=True)
    io.open(a.manifest, "w", encoding="utf-8", newline="\n").write(json.dumps(manifest, indent=2))

    order = cases()
    random.Random(a.seed).shuffle(order)
    out_f = io.open(a.out, "w", encoding="utf-8", newline="\n")
    raw_f = io.open(a.raw, "w", encoding="utf-8", newline="\n") if a.raw else None
    pay_f = io.open(a.dump_payloads, "w", encoding="utf-8", newline="\n") if a.dump_payloads else None
    for cid in order:
        for arm in ("baseline", "treatment"):
            prompt = payload(cid, arm)
            if pay_f:
                pay_f.write(json.dumps({"case": cid, "arm": arm, "payload": prompt}) + "\n")
            text = adapter(prompt, a.seed)
            parsed = parse_strict(text)
            retried = False
            if parsed is None:
                retried = True
                text2 = adapter(prompt + "\n\n" + FORMAT_REMINDER, a.seed + 1)
                if raw_f:
                    raw_f.write(json.dumps({"case": cid, "arm": arm, "attempt": 2,
                                            "raw": text2}) + "\n")
                parsed = parse_strict(text2)
            if raw_f:
                raw_f.write(json.dumps({"case": cid, "arm": arm, "attempt": 1,
                                        "raw": text}) + "\n")
            out_f.write(json.dumps({"case_id": cid, "arm": arm, "repeat": 1,
                                    "seed": a.seed, "parsed_ok": parsed is not None,
                                    "format_retried": retried,
                                    "answer_tokens": len(text.split()),
                                    "synthetic_smoke": manifest["synthetic_smoke"],
                                    "answers": parsed}) + "\n")
    out_f.close()
    print("run records written:", a.out, "| synthetic:", manifest["synthetic_smoke"])


if __name__ == "__main__":
    main()
