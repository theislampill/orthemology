# Mixed-model analysis specification (Pilot 1 → confirmatory v1)

**Status: specification only; no data.** Inherits every frozen v0 B.8 rule not restated here.

- **Unit:** one scored probe response (binary) or one measured quantity (tokens, seconds).
- **Primary model (per endpoint family):** logistic mixed model — `score ~ arm + (1|item) + (1|rater) + (1|executor_run)`; executors as a fixed stratum if ≥2 model families (report per-family and pooled); arm contrasts of record: **B−A** (distinctions), **C−B** (vocabulary), **C−C′** (label specificity; secondary).
- **Co-primaries & gatekeeping:** (1) false-closure family, then (2) pathway-defect family at α=0.05 hierarchical (v0 rule). Metaorthemma/binding family is a **key secondary** in v1 (added by DESIGN-V1); it may be promoted to a third gatekept position in the confirmatory freeze if Pilot 1 shows adequate variance behavior — a promotion decided before, never after, the confirmatory freeze.
- **Secondaries:** Holm–Bonferroni within the declared secondary set; compression analyzed among accuracy-matched responses plus an accuracy-adjusted regression as sensitivity; burden (time + load scale) as continuous LMM.
- **Equivalence/retirement:** TOST with the frozen −5 pp margin; only an adequately powered equivalence result (or harm-ceiling breach) can retire.
- **Missing/refused responses:** scored 0 only for content probes with an item-ambiguity flag review; excluded from compression.
- **Reporting:** every endpoint carries its blinding flag; every family reports its n, ICCs, and whether it was powered; underpowered families report "indicative" verdicts only.
- **Selective-prediction note:** if a confirmatory variant adds a confidence/abstention axis, the endpoint metric is **AURC** (with the Traub et al. 2024 criticisms weighed at freeze time; any alternative like AUGRC must be chosen before the freeze, never after).
