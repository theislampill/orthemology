# Pilot 1 — template (NOT RUN; parameters unfilled by design)

**Status: READY TO PARAMETERIZE AFTER PILOT 0; no data exists.** Pilot 1 estimates effect and variance structure well enough to power confirmatory v1. It still adjudicates nothing: the three-outcome rule's ADOPT/RETIRE branches remain closed to it.

## 1. Item-variant inventory (target: ≥3 independent variants per family)

| Family | Pilot-0 seed | Variant plan (domains rotated: software / lab-physical / clinical-abstract / games / documents) |
|---|---|---|
| occurrence/version identity | P0-ID-1 | ID-2 reused storage slot (lab sample rack); ID-3 stale checkout vs current (document revision) |
| plural profile | P0-PL-1 | PL-2 word-token with two morphological findings; PL-3 patient-abstract with symptom+cause axes |
| pathway vs result | P0-PW-1 | PW-2 dashboard-green from cached previous run; PW-3 reviewer approves via proxy signal |
| false closure | P0-FC-1 | FC-2 release notes claim completion over deferred flake; FC-3 audit sign-off over transferred item |
| rule revision | P0-RR-1 | RR-2 recurring mislabel class from ambiguous SOP; RR-3 repeated near-miss from threshold rule |
| **metaorthemma/binding** | P0-MB-1 | MB-2 assay run under wrong-fixture calibration, result luckily right; MB-3 deployment gate bound to wrong environment config, faithful execution |
| multi-actor | P0-MA-1 | MA-2 imperfect-information variant (poker-like observation split); MA-3 cooperative variant (shared target, divergent evidence) |
| negative controls | P0-NC-1/2 | NC-3, NC-4 (one per new domain) |

**Held-out-domain plan:** one domain (declared before the run, e.g., clinical-abstract) appears ONLY in transfer items: primers/training items never mention it; per-family transfer endpoints score the held-out items separately.

## 2. Rater-assignment plan

≥3 raters; between-subject for primer exposure (each rater sees exactly one of {A-filler, B, C, C′} as their trained condition; content-scoring raters are drawn from the unexposed pool per v0 B.8); Latin-square order; double-scoring of 100% of primary-family items (Krippendorff α reported), ≥30% of secondary items.

## 3. Simulation-based power

`power_simulation.py` — simulates the crossed random-effects design (item × rater × executor-run) from PLACEHOLDER parameters clearly marked synthetic; after Pilot 0/1 data exist, the placeholder block is replaced by estimated components and the script re-run to set confirmatory n. Target ≥0.8 power at the frozen MIE (+15 pp primary / 0.5 SD secondary). **The placeholders are not estimates and must never be reported as pilot results.**

## 4. Analysis specification

[`MIXED-MODEL-ANALYSIS-SPEC.md`](MIXED-MODEL-ANALYSIS-SPEC.md): logistic mixed model per endpoint family; arm fixed; item, rater, executor-run random; gatekept co-primaries (false-closure family, then pathway-defect family); Holm–Bonferroni across secondary families; compression via accuracy-matched token comparison with primer amortization; C′ analyzed as the label-specificity contrast (C vs C′) *secondary* to the structural contrasts (B vs A; C vs B).

## 5. Exit conditions

Pilot 1 ends with: estimated variance components; item-set freeze candidate; sham-gate verdict (C′ into confirmatory or not, by the Pilot-0/1 interpretability and matching gates); a filled power table. It never ends with an adoption or retirement statement.
