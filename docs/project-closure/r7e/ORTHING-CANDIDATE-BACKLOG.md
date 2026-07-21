# R7E — orthing candidate backlog (3-pass workflow, 36 agents)

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

Owner-requested 3-pass orthing (Pass 1 generative, Pass 2 read-only discovery, Pass 3 adversarial). 237 candidates -> **221 adversarially-survived** (99 keep / 122 bound), **16 rejected**. A focused, verified subset is integrated this pass (R7E closeout); the remainder is recorded here for fresh-Fable triage. Proposed target paths are shown extension-stripped and marked `[proposed]` (they are agent proposals, not live citations). Sourcing labels are the AGENTS' claims and MUST be independently verified before merge — any classical-source `primary-text-verified` addition needs a located primary locus (repo sourcing discipline; secondary != primary).

## Survivor distribution

- verdict: keep 99, bound 122
- substance: substantive 163, borderline 55, fluff 3
- sourcing (agent-claimed): orthemological-extension 35, cross-source-synthesis 74, secondary-reconstruction 35, primary-text-verified 63, creed-internal-inference 8, unsourced 6
- topic: other 27, terminology 17, epistemology 33, metaphysics 23, osm-latent 39, daee-runtime 34, governed-gradient-descent 22, meta-noetic-memetics 12, field-topology 14

## Rejected by the adversarial pass

- **ORTH-MS-07** (other): Mischaracterizes both attributions. The ninety-ninety rule (Cargill/Bentley 1985) is about NONLINEARITY OF EFFORT (the last 10% of code takes as long as the first 90%), not about incommensurability of burden types; and earned-valu
- **P2-CORE-12** (terminology): The central factual premise is fabricated. Manuscript §2.2 (line 131) writes bare 'Omega : M -> X' and 'x = Omega(m)' — there is NO 'x = Omega_e(m)' (episode-indexed) form anywhere (grep of Omega across the manuscript returns line
- **P2-M-02** (osm-latent): The finding's central premise is FALSE. §12.1's clause ('several compared models reach the same endpoint while only one matched the reported longitudinal trajectory') is directly and specifically tied to a reported result: OSM sou
- **P2-M-05** (epistemology): Not a defect. §4 already presents {structural, behavioral, provenance} as a stipulated 'working hypothesis of the framework, not a theorem,' with the subclass mechanism as the sanctioned extension point and an explicit non-exhaust
- **P2-02** (metaphysics): Firewall 1 breach. The proposal is to cite [S19] check_owner_activation_ordering.py as the VERIFYING mechanism for the route-reproducibility/determinism ortheme. But (1) firewall 1 is explicit that co-development is NOT validation
- **P2-10** (other): Two independent reasons to reject. (1) Firewall 1 breach: the proposed_location is REBAKE §7.4 'between the ranking-objective sentence and the reproducibility-policy sentence (lines 585-586)' — that is a read-only, pinned daee doc
- **D2-04-noetic-structure-as-topology** (field-topology): Premise is inaccurate and the proposed object invites the exact conflation the crosswalk forbids. The read-target is already typed: DAEE-ORTHEMOLOGY-CROSSWALK.yaml typed_distinctions list both 'inferred noetic profile / Psi-I' (th
- **CC-GD-01** (governed-gradient-descent): Central factual claims are FALSE against the pin. Verified at c86b3c66: docs/algebraic-notation-and-noetic-formalism [proposed]:61 contains verbatim 'Route-ranking functional …' and 'Not literal physical gradient'; lines 62-63,91 contain 

## Survivors (compact; full drafts in the workflow journal.jsonl)

| id | topic | verdict | substance | sourcing (claimed) | proposed target |
|---|---|---|---|---|---|
| META-THEO-07-assessment-backlog-resolution-crossref | other | bound | borderline | cross-source-synthesis | A dated editorial cross-reference note appended  |
| META-THEO-02-argument-from-eternal-truths-lineage | metaphysics | bound | substantive | secondary-reconstruction | A fourth bullet in companion/orthability-and-the |
| P2-M-11 | other | bound | borderline | orthemological-extension | A short subsection near Section 8.2 (episode sig |
| P2-06 | epistemology | keep | substantive | cross-source-synthesis | Any daee application file citing v0.4.4.0 proof  |
| O2-three-role-owner-activation-plan-vs-execution | daee-runtime | bound | substantive | primary-text-verified | CURRENT-RUNTIME-BOUNDARY.md |
| O3-controlled-delta-result-token-not-correctness | daee-runtime | bound | substantive | cross-source-synthesis | CURRENT-RUNTIME-CROSSWALK.yaml |
| O7-field-witness-nar-convergence-checked-projection | daee-runtime | keep | substantive | primary-text-verified | CURRENT-RUNTIME-CROSSWALK.yaml |
| D2-05-register-bridge-and-firewall-completeness | field-topology | bound | substantive | secondary-reconstruction | CURRENT-RUNTIME-CROSSWALK.yaml (register-set cor |
| D2-08-NLA-bound-missing | daee-runtime | bound | substantive | secondary-reconstruction | CURRENT-RUNTIME-CROSSWALK.yaml (row beside T_lan |
| D2-09-owner-activation-verification-chain | daee-runtime | bound | substantive | secondary-reconstruction | CURRENT-RUNTIME-CROSSWALK.yaml correspondence bl |
| D2-02-pin-witness-gap | daee-runtime | bound | substantive | primary-text-verified | CURRENT-RUNTIME-CROSSWALK.yaml dual_pin.verified |
| O8-discovery-tlang-citation-mislocated | daee-runtime | keep | borderline | primary-text-verified | DAEE-ORTHEMOLOGY-CROSSWALK.yaml |
| D2-06-claim-level-ladder | epistemology | keep | substantive | secondary-reconstruction | DAEE-ORTHEMOLOGY-CROSSWALK.yaml (new row) + EPIS |
| D2-12-layerA-layerB-progressive-disclosure | daee-runtime | keep | borderline | secondary-reconstruction | DAEE-ORTHEMOLOGY-CROSSWALK.yaml (new row) or CUR |
| D2-03-nabla-div-curl-loopbreak-untyped | governed-gradient-descent | bound | substantive | cross-source-synthesis | DAEE-ORTHEMOLOGY-CROSSWALK.yaml (new rows beside |
| D2-07-concealment-vs-deformation | terminology | bound | substantive | creed-internal-inference | DAEE-ORTHEMOLOGY-CROSSWALK.yaml (split the Psi-I |
| P2-OSM-13 | osm-latent | bound | borderline | orthemological-extension | DYNAMIC-FIXTURES.yaml DYN-8 (level or a clarifyi |
| OSM-F1 | osm-latent | bound | substantive | primary-text-verified | DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md |
| P2-OSM-09 | daee-runtime | keep | borderline | orthemological-extension | DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md D8  |
| P2-OSM-08 | osm-latent | keep | borderline | primary-text-verified | DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md dia |
| P2-OSM-14 | governed-gradient-descent | bound | borderline | orthemological-extension | DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md §2/ |
| P2-OSM-02 | epistemology | bound | substantive | orthemological-extension | DYNAMIC-ORTHING-AND-LATENT-STATE-LEARNING.md §4  |
| P2-01 | daee-runtime | bound | substantive | primary-text-verified | Decision 0021 (add a governed-pin/drift clause)  |
| P2-03 | osm-latent | keep | substantive | secondary-reconstruction | Decision 0024 Problem/§5 and applications/latent |
| P2-13 | osm-latent | keep | borderline | orthemological-extension | Decision 0024 §4 and applications/latent-state-o |
| P2-11 | meta-noetic-memetics | bound | borderline | orthemological-extension | Decision 0025 §1 or REPRESENTED-STANDARD.schema. |
| P2-06 | governed-gradient-descent | keep | substantive | cross-source-synthesis | Decision 0025 §4 (inline 'superseded by 0033 §1' |
| P2-07 | governed-gradient-descent | bound | substantive | cross-source-synthesis | Decision 0025 §4 anti-gaming block (inline 'supe |
| P2-05 | daee-runtime | bound | substantive | primary-text-verified | Decision 0027 §1 and applications/daee-epistemic |
| P2-12 | daee-runtime | bound | borderline | primary-text-verified | Decision 0027 §5 (R2) and NOETIC-TARGET-FIXTURES |
| P2-08 | meta-noetic-memetics | keep | substantive | cross-source-synthesis | Decision 0028 §3 (inline 'superseded by 0032 §1' |
| P2-04 | meta-noetic-memetics | bound | substantive | secondary-reconstruction | Decision 0028 §4 (add the same secondary-reconst |
| P2-M-04 | terminology | bound | substantive | primary-text-verified | Definition 2 (line 111) / Definition 7 (line 201 |
| P2-M-09 | metaphysics | bound | borderline | primary-text-verified | Definition 3 (line 120) and Section 2.1 (line 33 |
| O6-inference-boundary-status-vs-weight-legend | epistemology | bound | substantive | primary-text-verified | EPISTEMOLOGICAL-AND-METAPHYSICAL-BOUNDARY.md §F1 |
| P2-13 | daee-runtime | keep | substantive | unsourced | Governs the whole slice (sections 6-9); any supp |
| P2-M-12 | other | bound | borderline | primary-text-verified | Header revision line (line 6) and R7B footer (li |
| D2-11-mrp-generated-burden-fold | meta-noetic-memetics | bound | borderline | secondary-reconstruction | NOETIC-FIELD-DYNAMICS.yaml corrective_dynamics + |
| O1-daee-runtime-enforces-antireification | daee-runtime | keep | substantive | primary-text-verified | NOETIC-ORTHING-APPLICATION.md |
| META-THEO-01-bootstrapping-aseity | metaphysics | bound | substantive | cross-source-synthesis | New row A7 in companion/OBJECTIONS-AND-REPLIES.m |
| META-THEO-03-euthyphro-priority-of-fittingness | metaphysics | bound | substantive | cross-source-synthesis | New row A8 in companion/OBJECTIONS-AND-REPLIES.m |
| P2-04 | meta-noetic-memetics | bound | substantive | orthemological-extension | New subsection or table bridging 8.2 (MRP result |
| OSM-B1 | osm-latent | keep | substantive | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml |
| OSM-D1 | osm-latent | keep | substantive | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml |
| P2-OSM-01 | osm-latent | keep | substantive | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml (add a per-row s |
| P2-OSM-10 | osm-latent | keep | borderline | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml adaptation row n |
| P2-OSM-04 | osm-latent | bound | substantive | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml final row (osm_c |
| P2-OSM-03 | osm-latent | keep | substantive | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml orthogonalizatio |
| P2-OSM-15 | osm-latent | keep | borderline | primary-text-verified | OSM-CSCG-ORTHEME-CROSSWALK.yaml row 'CSCG unique |
| OSM-A1 | osm-latent | keep | substantive | primary-text-verified | OSM-DYNAMICS-DEFINITIONS.yaml |
| OSM-C1 | osm-latent | keep | substantive | primary-text-verified | OSM-DYNAMICS-DEFINITIONS.yaml |
| OSM-E1 | osm-latent | bound | substantive | primary-text-verified | OSM-DYNAMICS-DEFINITIONS.yaml |
| P2-OSM-06 | osm-latent | keep | borderline | primary-text-verified | OSM-DYNAMICS-DEFINITIONS.yaml geometry_definitio |
| P2-OSM-07 | terminology | bound | borderline | primary-text-verified | README.md (glossary line) and OSM-CSCG-ORTHEME-C |
| P2-OSM-12 | terminology | keep | borderline | primary-text-verified | README.md:21; DYNAMIC-ORTHING-AND-LATENT-STATE-L |
| P2-08 | terminology | keep | substantive | secondary-reconstruction | Reconcile Section 6.1 IR enum (line 412) with Se |
| P2-M-01 | osm-latent | keep | substantive | primary-text-verified | References section (lines 943-969) plus inline a |
| P2-F15-flag-groundbreaking-framing | other | keep | fluff | unsourced | Reject-flag: record in the R7E ledger as a do-no |
| P2-F14-flag-nla-true-compiler | daee-runtime | keep | borderline | primary-text-verified | Reject-flag: record in the R7E ledger; if any NL |
| P2-F13-flag-civilisational-scale-metrics | field-topology | keep | fluff | unsourced | Reject-flag: record in the R7E supplementation l |
| P2-F12-flag-finite-families-quantification | meta-noetic-memetics | keep | fluff | unsourced | Reject-flag: record in the R7E supplementation l |
| P2-F16-flag-restorative-fitrah-completeness | metaphysics | keep | borderline | creed-internal-inference | Reject/bound-flag: any restoration language stay |
| O4-nabla-div-curl-typed-field-diagnostics | governed-gradient-descent | bound | substantive | primary-text-verified | SOUND-DESCENT-MODEL-COMPARISON.md |
| O5-loopbreak-partial-transition-fitrah-one-ground | governed-gradient-descent | keep | substantive | cross-source-synthesis | SOUND-DESCENT-MODEL-COMPARISON.md |
| D2-01-stale-G1-adopted | governed-gradient-descent | keep | substantive | primary-text-verified | SOUND-DESCENT-MODEL-COMPARISON.md (G1 heading li |
| D2-10-vision-scale-overclaim-firewall | other | bound | substantive | cross-source-synthesis | SOURCE-BOUNDARY.md (evidence-status boundary) or |
| P2-F11-declared-incapacity-integrity | epistemology | bound | substantive | cross-source-synthesis | STATUS.md / manuscript limitations section, and  |
| P2-M-13 | epistemology | keep | borderline | primary-text-verified | Section 1.2 / 2.1 (cite Wetzel 2018 at the type/ |
| ORTH-MS-02 | other | keep | substantive | secondary-reconstruction | Section 10.1 at 'A player's information set is t |
| ORTH-MS-06 | other | bound | borderline | secondary-reconstruction | Section 12 Related Work table, extending the exi |
| P2-M-03 | daee-runtime | keep | borderline | primary-text-verified | Section 12.2, line 826 (the 'inspected read-only |
| P2-M-07 | epistemology | bound | substantive | orthemological-extension | Section 2.6 (analysis-version transport paragrap |
| P2-M-10 | epistemology | keep | borderline | primary-text-verified | Section 2.7, after Definition 7 (lines 200-205), |
| ORTH-MS-03 | other | keep | substantive | secondary-reconstruction | Section 3, appended to the closing paragraph aft |
| ORTH-MS-04 | other | bound | substantive | secondary-reconstruction | Section 5.2, appended after the five-states sent |
| P2-M-14 | other | bound | borderline | primary-text-verified | Section 5.3 (lines 340-347), with a cross-refere |
| P2-M-06 | epistemology | bound | borderline | primary-text-verified | Section 6.2, governed-components list (lines 385 |
| P2-M-15 | epistemology | bound | substantive | primary-text-verified | Section 6.2, negative-example paragraph (lines 3 |
| P2-14 | osm-latent | bound | substantive | orthemological-extension | Section 6.4 (owner activation / NLA latent), at  |
| P2-03 | daee-runtime | keep | substantive | unsourced | Section 6.4 (owner activation checker facets) an |
| P2-11 | daee-runtime | bound | substantive | cross-source-synthesis | Section 6.4 or a short subsection in section 8 c |
| ORTH-MS-01 | other | bound | substantive | secondary-reconstruction | Section 7.5, appended to the opening sentence (' |
| P2-06 | daee-runtime | keep | substantive | unsourced | Section 8.2 (MRP block / STOP requirement) and 8 |
| P2-07 | daee-runtime | bound | substantive | secondary-reconstruction | Section 8.2, the sentence at line 690 ('the MRP  |
| P2-M-08 | epistemology | bound | substantive | primary-text-verified | Section 8.3, V6 row (line 574), and the ReqPath  |
| ORTH-MS-05 | epistemology | keep | substantive | cross-source-synthesis | Section 8.3, as a sentence following the verdict |
| P2-12 | field-topology | bound | substantive | secondary-reconstruction | Section 8.4 (coverage vs collapse) and 8.7 (two- |
| P2-01 | field-topology | bound | substantive | secondary-reconstruction | Section 8.5 (MRP exhaustion lemma), immediately  |
| P2-05 | daee-runtime | bound | substantive | secondary-reconstruction | Section 9 (Application Workflow), as a new subse |
| P2-09 | epistemology | bound | substantive | secondary-reconstruction | Section 9 (workflow), new definition adjacent to |
| P2-OSM-05 | osm-latent | bound | substantive | orthemological-extension | UPDATE-COUPLING.yaml (add a per-transition prove |
| P2-F10-minimal-corrective-transition | governed-gradient-descent | bound | substantive | cross-source-synthesis | applications/daee-epistemics/ near CORRECTIVE-TR |
| R7E-O1 | daee-runtime | bound | substantive | secondary-reconstruction | applications/daee-epistemics/CURRENT-RUNTIME-BOU |
| R7E-P1-05 | daee-runtime | bound | borderline | cross-source-synthesis | applications/daee-epistemics/CURRENT-RUNTIME-BOU |
| P2-05 | daee-runtime | bound | substantive | secondary-reconstruction | applications/daee-epistemics/CURRENT-RUNTIME-BOU |
| R7E-P1-06 | epistemology | keep | borderline | cross-source-synthesis | applications/daee-epistemics/CURRENT-RUNTIME-BOU |
| P2-03 | field-topology | keep | substantive | cross-source-synthesis | applications/daee-epistemics/CURRENT-RUNTIME-BOU |
| R7E-P1-01 | daee-runtime | keep | substantive | cross-source-synthesis | applications/daee-epistemics/CURRENT-RUNTIME-CRO |
| R7E-P1-05 | epistemology | bound | substantive | creed-internal-inference | applications/daee-epistemics/EPISTEMOLOGICAL-AND |
| R7E-P1-02 | epistemology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/EPISTEMOLOGICAL-AND |
| P2-12 | epistemology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/EPISTEMOLOGICAL-AND |
| P2-07 | metaphysics | bound | substantive | creed-internal-inference | applications/daee-epistemics/EPISTEMOLOGICAL-AND |
| P2-04 | epistemology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/EPISTEMOLOGICAL-AND |
| DA-F | meta-noetic-memetics | keep | substantive | orthemological-extension | applications/daee-epistemics/META-NOETIC-MEMETIC |
| P2-14 | meta-noetic-memetics | bound | borderline | cross-source-synthesis | applications/daee-epistemics/META-NOETIC-MEMETIC |
| R7E-P1-03 | daee-runtime | bound | substantive | cross-source-synthesis | applications/daee-epistemics/META-NOETIC-MEMETIC |
| R7E-P1-04 | meta-noetic-memetics | keep | substantive | cross-source-synthesis | applications/daee-epistemics/META-NOETIC-MEMETIC |
| R7E-O3 | field-topology | keep | substantive | secondary-reconstruction | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| R7E-O4 | field-topology | bound | substantive | secondary-reconstruction | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| R7E-O5 | field-topology | bound | substantive | secondary-reconstruction | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| R7E-O6 | governed-gradient-descent | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| cc-01-field-topology-precondition | field-topology | bound | substantive | secondary-reconstruction | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| cc-02-operator-bounds-table | governed-gradient-descent | keep | substantive | secondary-reconstruction | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| cc-06-two-timescale-coupling-channel | governed-gradient-descent | keep | substantive | primary-text-verified | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| CC-FT-04 | field-topology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| P2-09 | governed-gradient-descent | bound | substantive | orthemological-extension | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| CC-FT-06 | field-topology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| CC-GD-07 | governed-gradient-descent | bound | borderline | cross-source-synthesis | applications/daee-epistemics/NOETIC-FIELD-DYNAMI |
| R7E-P1-01 | daee-runtime | keep | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| R7E-P1-02 | governed-gradient-descent | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| R7E-P1-04 | daee-runtime | keep | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| R7E-P1-07 | field-topology | keep | borderline | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| R7E-P1-03 | daee-runtime | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| P2-01 | terminology | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| P2-08 | meta-noetic-memetics | keep | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| P2-09 | meta-noetic-memetics | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| P2-11 | meta-noetic-memetics | bound | substantive | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| P2-13 | field-topology | keep | borderline | cross-source-synthesis | applications/daee-epistemics/NOETIC-ORTHING-APPL |
| DA-E | governed-gradient-descent | keep | substantive | orthemological-extension | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| R7E-O2 | governed-gradient-descent | keep | substantive | cross-source-synthesis | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| cc-03-sound-descent-status-staleness | governed-gradient-descent | keep | substantive | primary-text-verified | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| cc-04-descent-sense-firewall-cross-source | governed-gradient-descent | keep | substantive | cross-source-synthesis | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| R7E-P1-07 | governed-gradient-descent | keep | borderline | orthemological-extension | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| CC-GD-02 | governed-gradient-descent | keep | substantive | primary-text-verified | applications/daee-epistemics/SOUND-DESCENT-MODEL |
| R7E-P1-06 | terminology | keep | substantive | cross-source-synthesis | applications/daee-epistemics/SOURCE-BOUNDARY.md |
| OS-A | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/DYNAMIC-ORTHIN |
| OS-B | osm-latent | bound | substantive | primary-text-verified | applications/latent-state-orthing/DYNAMIC-ORTHIN |
| OS-C | osm-latent | bound | substantive | primary-text-verified | applications/latent-state-orthing/DYNAMIC-ORTHIN |
| OS-D | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/DYNAMIC-ORTHIN |
| P2-01 | osm-latent | bound | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-03 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-04 | osm-latent | bound | substantive | cross-source-synthesis | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-05 | osm-latent | bound | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-06 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-07 | osm-latent | bound | substantive | cross-source-synthesis | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-08 | osm-latent | keep | borderline | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| P2-09 | osm-latent | bound | borderline | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-01 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-02 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-03 | terminology | bound | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-04 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-05 | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| osm-p1-06 | osm-latent | keep | borderline | primary-text-verified | applications/latent-state-orthing/OSM-CSCG-ORTHE |
| cc-05-osm-trajectory-order-discriminator | osm-latent | keep | substantive | primary-text-verified | applications/latent-state-orthing/OSM-DYNAMICS-D |
| ORTH-DYN-03 | terminology | keep | substantive | orthemological-extension | companion |
| ORTH-DYN-02 | osm-latent | bound | substantive | primary-text-verified | companion 8.1 (appended bounded note after the m |
| ORTH-DYN-04 | epistemology | keep | substantive | orthemological-extension | companion section 12 (Limitations), appended par |
| ORTH-DYN-05 | epistemology | keep | substantive | orthemological-extension | companion section 9 (note after the rung table); |
| DYN-P2-02 | other | keep | substantive | cross-source-synthesis | companion §13 references (lines 211-215); script |
| DYN-P2-11 | metaphysics | bound | borderline | cross-source-synthesis | companion §4 (lines 58-62) |
| DYN-P2-12 | terminology | bound | borderline | orthemological-extension | companion §8 (first use of 'corrigibility') or a |
| DYN-P2-09 | governed-gradient-descent | bound | substantive | cross-source-synthesis | companion §8 (line 127) and argument-map rung 2  |
| DYN-P2-08 | metaphysics | bound | substantive | cross-source-synthesis | companion §8 / §8.1 (anti-creation clause); cros |
| DYN-P2-10 | terminology | keep | borderline | cross-source-synthesis | companion §8 line 127 |
| DYN-P2-07 | epistemology | keep | borderline | orthemological-extension | companion §8.1 (line 109 and the enumerated list |
| DYN-P2-06 | epistemology | bound | substantive | orthemological-extension | companion §8.1 / §9 boundary; a short crosswalk  |
| DYN-P2-01 | terminology | bound | substantive | cross-source-synthesis | companion §8.1 modalities 3 and 5; a companion d |
| DYN-P2-15 | daee-runtime | bound | borderline | cross-source-synthesis | companion §9 (line 132) and §11 DAEE reply (line |
| DYN-P2-05 | osm-latent | bound | substantive | primary-text-verified | companion §9 (rung 3 discussion) and/or §8.1 mod |
| ORTH-DYN-01 | metaphysics | keep | substantive | orthemological-extension | companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP [proposed]  |
| DYN-P2-04 | metaphysics | keep | substantive | cross-source-synthesis | companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP [proposed]  |
| DYN-P2-03 | epistemology | bound | substantive | cross-source-synthesis | companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP [proposed]  |
| P2-01 | epistemology | bound | substantive | secondary-reconstruction | companion/orthability-and-the-ground-of-intellig |
| P2-03 | metaphysics | keep | substantive | secondary-reconstruction | companion/orthability-and-the-ground-of-intellig |
| P2-06 | metaphysics | keep | borderline | secondary-reconstruction | companion/orthability-and-the-ground-of-intellig |
| P2-12 | metaphysics | bound | borderline | secondary-reconstruction | companion/orthability-and-the-ground-of-intellig |
| P2-04 | metaphysics | bound | substantive | secondary-reconstruction | companion/orthability-divine-attributes-and-spee |
| META-THEO-04-taymiyyan-kalam-bi-mashiah-tasalsul | metaphysics | bound | substantive | secondary-reconstruction | companion/orthability-divine-attributes-and-spee |
| P2-09 | metaphysics | bound | borderline | creed-internal-inference | companion/orthability-divine-attributes-and-spee |
| P2-07 | metaphysics | bound | substantive | creed-internal-inference | companion/orthability-divine-attributes-and-spee |
| P2-13 | metaphysics | keep | borderline | secondary-reconstruction | companion/orthability-divine-attributes-and-spee |
| META-THEO-06-ilm-not-kalam-location | metaphysics | bound | substantive | creed-internal-inference | companion/orthability-divine-attributes-and-spee |
| P2-05 | metaphysics | bound | substantive | orthemological-extension | companion/orthability-divine-attributes-and-spee |
| META-THEO-05-taaddud-al-qudama | metaphysics | keep | borderline | creed-internal-inference | companion/orthability-divine-attributes-and-spee |
| P2-08 | metaphysics | keep | borderline | secondary-reconstruction | companion/orthability-divine-attributes-and-spee |
| P2-11 | other | bound | borderline | cross-source-synthesis | companion/orthemic-modal-metaphysical-assessment |
| P2-CORE-04 | other | bound | substantive | orthemological-extension | core §1 (level-indexing / regress) and §3.1 (gov |
| P2-CORE-01 | other | bound | substantive | cross-source-synthesis | core §2.2 (immediately after the component table |
| P2-CORE-11 | other | keep | borderline | orthemological-extension | core §3.1 (governed-component boundary) |
| P2-CORE-13 | other | bound | borderline | orthemological-extension | core §3.1 (model C); §3.4 (selection bullet); §4 |
| P2-CORE-03 | epistemology | keep | substantive | cross-source-synthesis | core §4 V2b-P (the RelSpec_q(e) tuple, lines 435 |
| P2-CORE-02 | epistemology | keep | substantive | cross-source-synthesis | core §4 V6 (PerturbSpec tuple) and schemas/pertu |
| P2-CORE-08 | epistemology | keep | substantive | orthemological-extension | core §4 V6 (clause (ii), lines 526–528) |
| P2-CORE-06 | epistemology | keep | substantive | primary-text-verified | core §4.3 (nearest-neighbors paragraph) |
| P2-CORE-05 | other | bound | substantive | orthemological-extension | core §5.2 (Composition, condition 3, and the par |
| P2-CORE-07 | other | bound | substantive | cross-source-synthesis | core §5.3 (Compat/Conflict definitions); note §2 |
| P2-CORE-10 | terminology | bound | borderline | cross-source-synthesis | core §5.3 (GoalSchema and 𝒢 bullets); note §3 re |
| P2-CORE-09 | other | bound | substantive | cross-source-synthesis | core §5.3 (φ definition); note §2 C2 and §3 |
| P2-F04-anti-mimicry-negative-examples | daee-runtime | bound | substantive | cross-source-synthesis | docs/architecture governance note or CONTRIBUTIN |
| P2-F06-graded-proof-strength-ladder | epistemology | bound | substantive | cross-source-synthesis | docs/architecture/ORTHEMOLOGY-LAYER-MAP [proposed] (evid |
| P2-F05-no-stage-laundering | other | bound | substantive | cross-source-synthesis | docs/architecture/ORTHEMOLOGY-LAYER-MAP [proposed] (fire |
| P2-F02-proposer-not-verifier | epistemology | bound | substantive | cross-source-synthesis | docs/architecture/ORTHEMOLOGY-LAYER-MAP.md/ [proposed] |
| CC-GD-03 | governed-gradient-descent | keep | substantive | primary-text-verified | docs/decisions/0025-meta-noetic-memetics-and-sou |
| CC-FT-05 | field-topology | keep | borderline | primary-text-verified | docs/integrations/daee-epistemics-orthemology-ma |
| P2-OSM-11 | terminology | bound | substantive | cross-source-synthesis | docs/notation-registry [proposed] (register Geom_A, Pr |
| P2-F07-redundant-independent-cross-check | epistemology | bound | substantive | cross-source-synthesis | manuscript methods/auditability section or docs/ |
| P2-F08-reproducibility-required-partition | daee-runtime | bound | substantive | cross-source-synthesis | manuscript reproducibility/auditability section  |
| EP-G | epistemology | keep | substantive | cross-source-synthesis | manuscript/orthemma-ortheme-systems-revised-draf |
| MT-H | daee-runtime | keep | substantive | orthemological-extension | manuscript/orthemma-ortheme-systems-revised-draf |
| DYN-P2-13 | epistemology | bound | substantive | cross-source-synthesis | references/source-status [proposed] (new EXT/dynamic r |
| DYN-P2-14 | metaphysics | keep | borderline | cross-source-synthesis | static companion orthability-and-the-ground-of-i |
| P1-CORE-01 | other | keep | substantive | orthemological-extension | theory/orthemic-core-formalization [proposed] |
| P1-CORE-02 | other | keep | substantive | orthemological-extension | theory/orthemic-core-formalization [proposed] |
| P1-CORE-03 | other | keep | substantive | orthemological-extension | theory/orthemic-core-formalization [proposed] |
| P1-CORE-04 | other | bound | substantive | orthemological-extension | theory/orthemic-core-formalization [proposed] |
| P1-CORE-05 | terminology | keep | borderline | cross-source-synthesis | theory/orthemic-core-formalization [proposed] |
| P2-F01-reconstructibility-property | daee-runtime | bound | substantive | cross-source-synthesis | theory/orthemic-core-formalization [proposed] (candidate |
| P2-F09-availability-not-application | terminology | bound | substantive | cross-source-synthesis | theory/orthemic-core-formalization [proposed] (type/toke |
| P2-F03-closed-vocabulary-latent-stability | terminology | bound | substantive | cross-source-synthesis | theory/orthemic-core-formalization [proposed] or manuscr |
| P1-CORE-06 | other | bound | substantive | orthemological-extension | theory/orthemic-multi-actor-conflict-note [proposed] |
| P1-CORE-07 | other | keep | substantive | orthemological-extension | theory/orthemic-multi-actor-conflict-note [proposed] |
