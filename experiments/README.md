# Experiments — NONE RUN

No empirical experiment has been executed. The **canonical machine-readable
state of every experiment packet** is
[`experiment-status.yaml`](experiment-status.yaml) (Decisions 0018/0020),
validated in CI by `scripts/validate_experiment_readiness.py` and, for the
benchmark packets, the methods gate `scripts/validate_experiment_methods.py`
(Decision 0022). This README defers to it.

| Packet | Purpose | Status | Where |
|---|---|---|---|
| `FCSP-2` | false-closure / selective-prediction benchmark (§13.1) | READY_TO_RUN (methods gate passed) | [`false-closure-selective-prediction-v2/`](false-closure-selective-prediction-v2/) |
| `ER-2` | episode-reification incremental-value test (§13.2) | READY_TO_RUN (methods gate passed) | [`episode-reification-v2/`](episode-reification-v2/) |
| `FCSP-1` | benchmark v1 (R6) | **HISTORICAL** — methods-unready, superseded by FCSP-2 (Decision 0020) | [`false-closure-selective-prediction/`](false-closure-selective-prediction/) |
| `ER-1` | episode test v1 (R6) | **HISTORICAL** — methods-unready, superseded by ER-2 (Decision 0020) | [`episode-reification/`](episode-reification/) |
| `TERM-P0-V1` | terminology Pilot 0 v1 | immutable superseded history | [`../terminology/pilot0/`](../terminology/pilot0/) |
| `TERM-P0-V2` | terminology Pilot 0 v2 | READY_FOR_HUMAN_MATCHING_REVIEW | [`../terminology/pilot0-v2/`](../terminology/pilot0-v2/) |
| `TERM-P1-TEMPLATE` | Pilot 1 template | DRAFT | [`../terminology/pilot1/`](../terminology/pilot1/) |
| `TERM-CONFIRMATORY-TEMPLATE` | confirmatory template (only stage that can adopt/retire a term) | DRAFT | [`../terminology/confirmatory-v1-template/`](../terminology/confirmatory-v1-template/) |

The historical R6 packets `FCSP-1`/`ER-1` are preserved byte-frozen; their
in-packet `STATUS.yaml` records what R6 claimed, as history. The corrected
current classification lives only in `experiment-status.yaml` (Decision 0020).

**A Git freeze is not an external preregistration**; execution, spend, human
review, and registry submission are owner/external acts. Packet smoke tests
produce no result and are never empirical outcomes.

The deterministic semantic fixtures under [`../tests/`](../tests/) are
validator inputs, not experiments.
