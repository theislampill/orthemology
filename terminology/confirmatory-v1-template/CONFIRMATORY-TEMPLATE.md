# Confirmatory v1 — preregistration template (NOT RUN; not freezable until Pilot 1 fills it)

**Status: template. Every ⟨…⟩ slot must be filled from Pilot 0/1 outputs before the freeze; freezing with placeholder values is prohibited.**

## Freeze checklist (all boxes required before any run)

- [ ] Item set frozen: ⟨list⟩ — ≥3 variants per family incl. the metaorthemma/binding family; held-out transfer domain declared: ⟨domain⟩
- [ ] Arms frozen: A, B, C mandatory; C′ included? ⟨yes/no per the Pilot-0/1 sham gates; if no, reason recorded⟩ — C′ never replaces the A/B/C primaries
- [ ] Co-primaries + gatekeeping order frozen (incl. any pre-freeze promotion of the binding family): ⟨order⟩
- [ ] MIE, noninferiority margin, harm ceilings: frozen v0 values restated: +15 pp / 0.5 SD; −5 pp; ceilings ⟨absolute counts⟩
- [ ] n from simulation-based power at estimated components: items ⟨n_i⟩, raters ⟨n_r⟩, runs ⟨n_run⟩, models ⟨≥2 pinned ids⟩; power table attached
- [ ] Underpowered? If feasible n < target: declared IN ADVANCE; all conclusions pre-downgraded to "indicative"
- [ ] Rater plan: between-subject exposure; double-scoring plan; drift reporting
- [ ] Analysis code frozen (hash): ⟨sha256⟩; deviation ledger opened
- [ ] Scoring manual + adjudication manual version: ⟨version/hash⟩
- [ ] Endpoint metrics frozen — incl., if an abstention axis exists, the selective-prediction metric (AURC or a pre-freeze-chosen alternative; never swapped after freeze)
- [ ] Packet SHA-256 published BEFORE any run: ⟨hash⟩ (v0 B.8 rule)
- [ ] Three-outcome rule restated verbatim in the frozen packet (ADOPT / DO NOT ADOPT YET / RETIRE-REJECT)

## Decision surface (unchanged from v0 B.6/B.8, restated for the freeze)

Per construct family and for the coordinated vocabulary: ADOPT only on an adequately powered win at the MIE; DO NOT ADOPT YET on any insufficient evidence (every underpowered null, every ordinary tie); RETIRE/REJECT only on adequately powered equivalence or a harm-ceiling breach. "Arm C beats Arm B" per the exact v0 definition. Distinction verdicts (B vs A) and vocabulary verdicts (C vs B) never transfer to each other; C vs C′ adjudicates label specificity only.

## What no template can pre-decide

Participant recruitment, compensation, and any human-subjects process are OWNER-ONLY burdens (resources + responsibility) and are not scheduled by this repository.
