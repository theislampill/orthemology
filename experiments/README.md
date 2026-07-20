# Experiments — NONE RUN

No empirical experiment has been executed for this project. The **canonical,
machine-readable state of every experiment packet** is
[`experiment-status.yaml`](experiment-status.yaml) (Decision 0018), validated
in CI by `scripts/validate_experiment_readiness.py`. This README defers to it.

| Packet | Purpose | Where |
|---|---|---|
| `FCSP-1` | false-closure / selective-prediction benchmark (manuscript §13.1) | [`false-closure-selective-prediction/`](false-closure-selective-prediction/) |
| `ER-1` | episode-reification incremental-value test (manuscript §13.2) | [`episode-reification/`](episode-reification/) |
| `TERM-P0-V1` | terminology Pilot 0 v1 — immutable superseded history | [`../terminology/pilot0/`](../terminology/pilot0/) |
| `TERM-P0-V2` | terminology Pilot 0 v2 — current feasibility instrument candidate | [`../terminology/pilot0-v2/`](../terminology/pilot0-v2/) |
| `TERM-P1-TEMPLATE` | Pilot 1 template | [`../terminology/pilot1/`](../terminology/pilot1/) |
| `TERM-CONFIRMATORY-TEMPLATE` | confirmatory-study template (the only stage that can adopt/retire a term) | [`../terminology/confirmatory-v1-template/`](../terminology/confirmatory-v1-template/) |

Statuses use the closed Decision 0018 vocabularies. **A Git freeze is not an
external preregistration**; registry submission, execution, spend, and human
review are owner/external acts. Deterministic packet smoke tests produce no
result and are never empirical outcomes.

The deterministic semantic fixtures under [`../tests/`](../tests/) are
validator inputs, not experiments; they measure nothing empirical.
