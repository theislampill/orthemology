# Sourcing ledger (R2, 2026-07-20)

One row per load-bearing claim–source pair in the current public corpus. Bib database: [`references/orthemology.bib`](../../references/orthemology.bib). Verification statuses:

- **WEB-VERIFIED** — bibliographic record and claim-relevant content confirmed against the publisher/official page or full text during this pass (2026-07-20);
- **RECORD-CONFIRMED** — standard, widely reproduced bibliographic record stated with high confidence from the assistant's knowledge; identifier included; not re-fetched this pass; flagged for routine re-check before any external submission;
- **VIA-COMPILATION** — locus taken from an attributed secondary compilation supplied to the project (an Islamic-fatwa-style article citing its primary sources with page/volume loci); the primary edition was not independently opened; every such claim is flagged in the companion text itself.

No entry is cited beyond what its "supports" column states. Rows marked *complicates* are cited AS complications, not as support.

| # | Locus (document → claim) | Source (bib key) | Type | Identifier | Status | Relation to claim | Flags |
|---|---|---|---|---|---|---|---|
| 1 | Manuscript §12: maintained candidate structure ≈ POMDP belief state | kaelbling1998pomdp | journal | doi:10.1016/S0004-3702(98)00023-X | RECORD-CONFIRMED | supports (belief-state formalism exists and predates this work) | — |
| 2 | Manuscript §12: predictive-state alternative | littman2001predictive | conf | NIPS 2001 | RECORD-CONFIRMED | supports | — |
| 3 | Manuscript §2.7 inherited result 3 (safe merger/bisimulation); §12 | givan2003equivalence | journal | doi:10.1016/S0004-3702(02)00376-4 | WEB-VERIFIED | supports (MDP equivalence/minimization is established; the "inherited, not new" concession) | — |
| 4 | Manuscript §12: probabilistic bisimulation lineage | larsen1991bisimulation | journal | doi:10.1016/0890-5401(91)90030-6 | RECORD-CONFIRMED | supports | — |
| 5 | Manuscript §12: automata minimization | hopcroft1971nlogn | chapter | doi:10.1016/B978-0-12-417750-5.50022-1 | RECORD-CONFIRMED | supports | — |
| 6 | Manuscript §12: sufficient statistics as type-individuation ancestor | fisher1922foundations | journal | doi:10.1098/rsta.1922.0009 | RECORD-CONFIRMED | supports | — |
| 7 | Manuscript §12: causal states | crutchfield1989inferring; shalizi2001computational | journal | doi:10.1103/PhysRevLett.63.105; doi:10.1023/A:1010388907793 | RECORD-CONFIRMED | supports | — |
| 8 | Manuscript §12: reject option | chow1970reject | journal | doi:10.1109/TIT.1970.1054406 | RECORD-CONFIRMED | supports | — |
| 9 | Manuscript §12: multi-label / hierarchical classification | tsoumakas2007multilabel; silla2011hierarchical | journal | doi:10.4018/jdwm.2007070101; doi:10.1007/s10618-010-0175-9 | RECORD-CONFIRMED | supports | — |
| 10 | Manuscript §12–13: selective prediction foundations | elyaniv2010foundations; geifman2017selective | journal/conf | JMLR 11 (2010); NeurIPS 2017 | RECORD-CONFIRMED | supports | — |
| 11 | Manuscript §13.1: AURC as the established risk–coverage metric | geifman2019biasreduced | conf | ICLR 2019 (arXiv:1805.08206) | WEB-VERIFIED (metric attribution confirmed via secondary literature) | supports (AURC/E-AURC derived there) | earlier draft's "risk–coverage AUROC" was corrected against this |
| 12 | Manuscript §13.1: methodological criticisms of AURC to be weighed pre-freeze | traub2024overcoming | conf | NeurIPS 2024; arXiv:2407.01032 | WEB-VERIFIED | complicates (criticizes AURC-style evaluation; proposes AUGRC) | cited as caveat, not adopted endpoint |
| 13 | Manuscript §12: open-set / OOD neighbors of quarantine | scheirer2013openset; hendrycks2017baseline | journal/conf | doi:10.1109/TPAMI.2012.256; ICLR 2017 | RECORD-CONFIRMED | supports | — |
| 14 | Manuscript §12: value-of-information stopping | howard1966voi; wald1947sequential | journal/book | doi:10.1109/TSSC.1966.300074 | RECORD-CONFIRMED | supports | — |
| 15 | Manuscript §8.6/§12, core §4.3: provenance/audit systems are operational but verdict-free | w3c2013provdm | W3C Rec | https://www.w3.org/TR/prov-dm/ | RECORD-CONFIRMED | supports (PROV-DM's scope is entities/activities/agents; it defines no result-vs-pathway verdict layer — checked against the Recommendation's data model) | negative claim kept narrow ("typically carry no…") |
| 16 | Manuscript §8/§13.2, core §4: metamorphic testing as V6's neighbor | chen1998metamorphic; chen2018metamorphicsurvey | techreport/journal | HKUST-CS98-01; doi:10.1145/3143561 | WEB-VERIFIED | supports | — |
| 17 | Manuscript §12: control-effectiveness vs outcome testing | iaasb2009isa330 | standard | ISA 330 | RECORD-CONFIRMED | supports (tests of controls vs substantive procedures distinction is the standard's own) | — |
| 18 | Manuscript §12: risk registers | iso31000risk | standard | ISO 31000:2018 | RECORD-CONFIRMED | supports (risk-register practice; the standard is guidelines-level) | — |
| 19 | Manuscript §8.5–8.6, core §4.3: process reliabilism names correct-result-through-unreliable-process; Gettier structure | goldman1979justified; gettier1963justified; sep-reliabilism | chapter/journal/SEP | doi:10.1007/978-94-009-9493-5_1; doi:10.1093/analys/23.6.121 | RECORD-CONFIRMED | supports | the "for beliefs; no operational record schema" contrast is this paper's claim, not the sources' |
| 20 | Manuscript §2/glossary: type–token distinction background | sep-types-tokens | SEP | plato.stanford.edu/entries/types-tokens/ | RECORD-CONFIRMED | supports | — |
| 21 | Companion (school-neutral) §faculties: proper functionalism | plantinga1993warrant | book | doi:10.1093/0195078640.001.0001 | RECORD-CONFIRMED | supports | — |
| 22 | Companion §faculties: selected-function naturalism | millikan1984language | book | MIT Press 1984 | RECORD-CONFIRMED | supports (the naturalist alternative is real and must be answered, not dismissed) | — |
| 23 | Companion §faculties: generality/reference-class problem | sep-generality (primary: Conee & Feldman 1998) | journal | doi:10.1023/A:1004243308503 | RECORD-CONFIRMED | complicates (applies to orthemic reliability talk too; conceded in text) | — |
| 24 | Companion §transcendental: nature and limits of transcendental arguments | sep-transcendental; stroud1968transcendental | SEP/journal | doi:10.2307/2024395 | RECORD-CONFIRMED | complicates and frames (Stroud-style objection is presented as a live objection) | — |
| 25 | Companion §rivals: Platonism/abstracta; modality | sep-abstract-objects; sep-modality-varieties | SEP | URLs in bib | RECORD-CONFIRMED | frames rival taxonomy | — |
| 26 | Companion §contrast: modal ontological and cosmological arguments | sep-ontological; sep-cosmological | SEP | URLs in bib | RECORD-CONFIRMED | supports the "this is not that argument" contrasts | — |
| 27 | Companion §rivals: divine conceptualism about logic | anderson2011lord | journal | doi:10.5840/pc201113229 | RECORD-CONFIRMED | supports (a published argument of the adjacent form; treated as neighbor, not authority) | — |
| 28 | Companion §faculties: evolutionary debunking neighbor | plantinga2011conflict | book | doi:10.1093/acprof:oso/9780199812097.001.0001 | RECORD-CONFIRMED | frames (EAAN is a neighbor argument; differences stated) | — |
| 29 | Companion §Hume: Hume's own account of reason, induction, scepticism | hume1739treatise (T 1.3.6, 1.4.1, 1.4.7); hume1748enquiry (EHU 4–5, 12) | primary | Norton/Beauchamp critical editions | RECORD-CONFIRMED (standard loci) | complicates the "Hume is self-refuting" charge — see disposition in the companion | primary-text loci are standard; edition pagination not reproduced |
| 30 | Companion §Hume: naturalist/skeptical-realist readings | kemp_smith1905naturalism; garrett1997cognition; sep-hume; sep-induction | journal/book/SEP | doi:10.1093/mind/XIV.2.149 | RECORD-CONFIRMED | complicates (the scholarship reads Hume as no simple self-refuter) | drives the "overstated" disposition |
| 31 | Atharī companion: Allah speaks with speech that is heard; letters; sound | quran (4:87; 4:122; 5:116; 20:11; 19:52; 42:11); ibnuthaymin-lumah p.73 | primary/classical | sūrah:āyah | VIA-COMPILATION (Qurʾānic āyāt themselves are checkable; the creed-inference locus p.73 is via the compilation) | supports the creed-internal claim as an Atharī position | school-flagged: Atharī |
| 32 | Atharī companion: Qurʾān = Allah's word, not created; creation/command distinction | quran (9:6; 7:54; 36:82; 55:1–3; 2:120); ibntaymiyya-majmu 12/53, 12/98; bukhari-khalq (2/70, p.143); tahawi-aqida §Qurʾān | primary/classical | loci as listed | VIA-COMPILATION | supports as Atharī creed-internal doctrine | school-flagged; never presented as neutral philosophy |
| 33 | Atharī companion: words of Creator / voice of reciter | ibntaymiyya-majmu 12/98; bukhari-khalq | classical | 12/98 | VIA-COMPILATION | supports | school-flagged |
| 34 | Atharī companion: genus-eternal / particulars-when-He-wills formulation | ibnuthaymin-wasitiyya 1/418–441; ibnqayyim-sawaiq 503–510 | classical | loci as listed | VIA-COMPILATION | supports (the taʿlīq the paper builds on) | the paper marks this the *Taymiyyan/Atharī* articulation; other Sunni schools differ (kalām nafsī) and are described neutrally |
| 35 | Atharī companion: al-Lālikāʾī's 550-scholar report | lalikai-sharh (493) | classical | entry 493 | VIA-COMPILATION | supports (historical breadth of the position among early scholars) | reported as a classical author's claim, not an independently verified census |

## Unresolved source limitations (honest residuals)

1. **VIA-COMPILATION rows (31–35):** the classical loci come from an attributed modern compilation supplied to the project; the printed editions were not independently opened. Every dependent claim in the Atharī companion carries an inline flag, and no load-bearing claim rests *solely* on an unattributed assertion — but edition-level verification remains an open burden (listed in the closure ledger).
2. **RECORD-CONFIRMED rows:** identifiers are stated from standard bibliographic knowledge and were not all re-fetched this pass; a routine re-check is required before any external (journal/preprint) submission. The three most error-prone records (AURC lineage, metamorphic-testing report, MDP equivalence) *were* web-verified this pass.
3. No citation was manufactured for a field merely because the related-work table names it; where no specific source is load-bearing (e.g., "ticket state machines" as commodity practice), the text now claims only commodity practice and cites nothing.
