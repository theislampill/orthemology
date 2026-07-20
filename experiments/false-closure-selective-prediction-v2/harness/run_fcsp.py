#!/usr/bin/env python3
"""FCSP-2 run orchestrator (packet harness; CI uses ONLY the mock adapter).

Usage:
  python run_fcsp.py --adapter mock --manifest out/manifest.json \
      --out out/runs.jsonl [--raw out/raw.jsonl] [--dump-payloads out/payloads.jsonl]
  python run_fcsp.py --adapter cmd --cmd "your-executor --stdin" ...
  (a provider adapter INTERFACE exists; no credentials, no live call in CI)

Guarantees:
  - prompt payloads are assembled ONLY from items/PUBLIC-ITEMS.json and the
    frozen arm instruction files — the harness never opens items/KEYS.json
    (payload isolation; proven by tests and the --dump-payloads audit file);
  - strict JSON parsing of executor output with ONE logged format retry;
  - failed item-repeats recorded, never dropped;
  - raw outputs retained; manifest written before the first call;
  - deterministic mock adapter derives its answer only from the public facts.
"""
import argparse
import hashlib
import io
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKT = os.path.dirname(HERE)

FORMAT_REMINDER = ("Your previous reply was not valid JSON of the required shape. "
                   "Reply with ONLY the JSON object, no prose.")

ANSWER_SHAPE = ("Reply with ONLY a JSON object: "
                '{"placement": "no-defect|defect-confirmed|underdetermined|abstain-escalate", '
                '"confidence": 0..1, "closure_claimed": true|false, '
                '"live_alternatives": [...], "route_selected": "...", '
                '"residual_burdens": [{"burden": "...", "disposition": '
                '"resolved|open|deferred|transferred|owner-assigned|risk-accepted"}], '
                '"rationale": "..."}')


def load_public():
    p = os.path.join(PKT, "items", "PUBLIC-ITEMS.json")
    return json.load(io.open(p, encoding="utf-8"))["items"]


def arm_instruction(arm):
    fn = {"baseline": "baselines/BASELINE-ARM.md",
          "treatment": "treatments/TREATMENT-ARM.md"}[arm]
    text = io.open(os.path.join(PKT, fn), encoding="utf-8").read()
    return text.split("---", 1)[1].strip()


def assemble_prompt(item, arm):
    return (arm_instruction(arm) + "\n\n" + "\n".join(item["facts"])
            + "\n\n" + ANSWER_SHAPE)


class MockAdapter:
    """Deterministic offline executor for smoke runs. Derives its answer ONLY
    from the public facts (it has no key access by construction)."""

    def __call__(self, prompt, seed):
        rng = random.Random(seed + len(prompt))
        cautious = "Still-live alternatives" in prompt or "obligation" in prompt.lower()
        no_result = "no recorded result" in prompt
        stale = "validity window is 30 days" in prompt and "2026-04-" in prompt
        answer = {
            "placement": ("abstain-escalate" if (cautious and (no_result or stale))
                          else ("no-defect" if "clear no-defect reading" in prompt
                                else "defect-confirmed" if "defect class" in prompt
                                else "underdetermined")),
            "confidence": round(0.55 + 0.4 * rng.random(), 2),
            "closure_claimed": ("every listed check completed" in prompt) or not cautious,
            "live_alternatives": (["condition A", "condition B"]
                                  if "condition A" in prompt and cautious else []),
            "route_selected": ("H-2" if "may not be used" in prompt and cautious
                               else "S-1" if "safe interim handling" in prompt and cautious
                               else "standard"),
            "residual_burdens": ([{"burden": "handed obligation", "disposition": "deferred"},
                                  {"burden": "risk-accepted obligation", "disposition": "risk-accepted"}]
                                 if "accepted-as-risk" in prompt and cautious else
                                 ([{"burden": "open check", "disposition": "open"}]
                                  if cautious and no_result else [])),
            "rationale": "mock deterministic traversal",
        }
        return json.dumps(answer)


class CmdAdapter:
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self, prompt, seed):
        r = subprocess.run(self.cmd, shell=True, input=prompt.encode("utf-8"),
                           capture_output=True)
        return r.stdout.decode("utf-8", errors="replace")


class ProviderAdapterInterface:
    """Interface only. Instantiating raises: live provider calls are an
    owner-authorized run act and are never made from this repository's CI."""

    def __init__(self, *_a, **_k):
        raise RuntimeError("provider adapter requires an owner-authorized run "
                           "environment; no credentials or live calls exist here")


def parse_strict(text):
    try:
        obj = json.loads(text.strip())
    except Exception:
        return None
    if not isinstance(obj, dict) or "placement" not in obj or "confidence" not in obj \
            or "closure_claimed" not in obj:
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
    ap.add_argument("--arms", default="baseline,treatment")
    ap.add_argument("--seed", type=int, default=20260729)
    a = ap.parse_args()

    adapter = MockAdapter() if a.adapter == "mock" else CmdAdapter(a.cmd)
    items = load_public()
    order = list(range(len(items)))
    random.Random(a.seed).shuffle(order)

    manifest = {
        "packet_id": "FCSP-2", "run_id": "mock-smoke" if a.adapter == "mock" else "cmd-run",
        "packet_freeze_hash": "recorded-at-freeze", "run_authorized_by":
            ("NONE — synthetic mock traversal" if a.adapter == "mock" else "SEE OWNER RECORD"),
        "started_at": "1970-01-01T00:00:00Z", "adapter": a.adapter,
        "executor": {"model_id": "mock" if a.adapter == "mock" else "cmd",
                     "model_version_or_hash": "mock", "provider": "offline"},
        "sampling": {"temperature": 0.0, "top_p": 1.0, "max_output_tokens": 2048},
        "repeats": 1, "seeds": [a.seed],
        "registration_state": "NOT_REGISTERED",
        "synthetic_smoke": a.adapter == "mock",
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.manifest)), exist_ok=True)
    io.open(a.manifest, "w", encoding="utf-8", newline="\n").write(json.dumps(manifest, indent=2))

    out_f = io.open(a.out, "w", encoding="utf-8", newline="\n")
    raw_f = io.open(a.raw, "w", encoding="utf-8", newline="\n") if a.raw else None
    pay_f = io.open(a.dump_payloads, "w", encoding="utf-8", newline="\n") if a.dump_payloads else None

    for idx in order:
        item = items[idx]
        for arm in a.arms.split(","):
            prompt = assemble_prompt(item, arm)
            if pay_f:
                pay_f.write(json.dumps({"item_id": item["item_id"], "arm": arm,
                                        "payload_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                                        "payload": prompt}) + "\n")
            text = adapter(prompt, a.seed)
            retried = False
            parsed = parse_strict(text)
            if parsed is None:
                retried = True
                text2 = adapter(prompt + "\n\n" + FORMAT_REMINDER, a.seed + 1)
                if raw_f:
                    raw_f.write(json.dumps({"item_id": item["item_id"], "arm": arm,
                                            "attempt": 2, "raw": text2}) + "\n")
                parsed = parse_strict(text2)
            if raw_f:
                raw_f.write(json.dumps({"item_id": item["item_id"], "arm": arm,
                                        "attempt": 1, "raw": text}) + "\n")
            rec = {"item_id": item["item_id"], "arm": arm, "repeat": 1, "seed": a.seed,
                   "parsed_ok": parsed is not None, "format_retried": retried,
                   "synthetic_smoke": manifest["synthetic_smoke"],
                   "record": parsed if parsed is not None else None}
            out_f.write(json.dumps(rec) + "\n")
    out_f.close()
    print("run records written:", a.out, "| adapter:", a.adapter,
          "| synthetic:", manifest["synthetic_smoke"])


if __name__ == "__main__":
    main()
