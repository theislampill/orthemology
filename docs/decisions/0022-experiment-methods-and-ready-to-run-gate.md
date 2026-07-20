# Decision 0022 — Experiment methods and the READY_TO_RUN gate

**Date:** 2026-07-20 · **Authority:** R7 owner authorization · **Status:** adopted · **Reopens nothing:** Decisions 0001–0021 stand; extends Decision 0018's readiness ladder with an enforced methods gate.

## Problem

R6's readiness validator checked packet *shape* (files, vocabulary, freeze, smoke traversal) and passed while the packets were scientifically unready — no harness, incomplete analysis, leaky stimuli, a scoring bug (Decision 0020). A green shape check is compatible with an instrument that cannot produce a valid result.

## Decision

A benchmark packet (`FCSP-*`, `ER-*`) may hold `READY_TO_RUN` only when it passes the **methods gate** `scripts/validate_experiment_methods.py`, which exercises the packet's own harness and analysis on the deterministic mock adapter and asserts, per packet:

1. an executable **run harness** with an offline **mock adapter** (the only adapter CI uses), a `cmd` adapter, and a provider **interface that cannot live-call in CI**;
2. **public/scoring isolation** — the harness assembles prompts without any code path that reads the hidden scoring keys, and its exact payloads (audited via `--dump-payloads`) carry no key material, family/archetype label, or diagnostic conclusion;
3. a **strict parser** with a **logged format-retry** path and recorded (never dropped) failures;
4. **every declared endpoint** is produced by the analysis;
5. the **decision rules execute mechanically** (unit-tested in the packet smoke test; synthetic runs adjudicate nothing);
6. a stated **unit of inference** with repeats not counted as independent evidence;
7. a **synthetic end-to-end run** that produces no adjudicated scientific outcome;
8. the **no-run guard** holds.

`validate_experiment_readiness.py` and this gate run together in CI; a current packet failing either may not be `READY_TO_RUN` and takes the highest honest lower status. The gate establishes methods/engineering readiness only — never an empirical result, and never that a run *should* occur (execution, spend, ethics, and external registration remain owner/external acts).

## Consequences

New: `scripts/validate_experiment_methods.py` + CI step; `docs/project-closure/r7/EXPERIMENT-METHODS-AUDIT.md` (the human-readable audit). `FCSP-2` and `ER-2` pass the gate and are `READY_TO_RUN`; `FCSP-1`/`ER-1` remain historical and cannot hold it.
