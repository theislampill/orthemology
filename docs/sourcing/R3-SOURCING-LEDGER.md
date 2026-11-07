# R3 sourcing ledger (main lane)

**Date:** 2026-07-20 · **Method:** every row previously marked `RECORD-CONFIRMED` in `SOURCING-LEDGER.md` was re-verified against publisher/official records this pass (Crossref DOI registration, live SEP pages + archive pages, JMLR/arXiv/W3C/ISO/davidhume.org, official aggregators where publishers block fetching). **Status hierarchy (R3):** `PRIMARY-TEXT-VERIFIED` > `OFFICIAL-PUBLISHER-VERIFIED` > `SECONDARY-VERIFIED` > `VIA-COMPILATION` > `UNVERIFIED-NONLOADBEARING`. The R2 ledger is retained unchanged as history; this ledger supersedes its statuses.

## Re-graded rows (academic corpus)

| R2 row | Bib key(s) | R3 status | Support judgment | Notes |
|---|---|---|---|---|
| 1 | kaelbling1998pomdp | OFFICIAL-PUBLISHER-VERIFIED | supports | Crossref 10.1016/S0004-3702(98)00023-X exact |
| 2 | littman2001predictive | SECONDARY-VERIFIED | supports | dblp (NeurIPS proceedings server refused connection) |
| 4 | larsen1991bisimulation | OFFICIAL-PUBLISHER-VERIFIED | supports | Crossref exact |
| 5 | hopcroft1971nlogn | OFFICIAL-PUBLISHER-VERIFIED | supports | Crossref exact |
| 6 | fisher1922foundations | OFFICIAL-PUBLISHER-VERIFIED | supports | Crossref exact |
| 7 | crutchfield1989inferring; shalizi2001computational | OFFICIAL-PUBLISHER-VERIFIED | supports | both Crossref exact |
| 8 | chow1970reject | OFFICIAL-PUBLISHER-VERIFIED | supports | IEEE TIT 16(1):41–46 exact |
| 9 | tsoumakas2007multilabel; silla2011hierarchical | OFFICIAL-PUBLISHER-VERIFIED | supports | both Crossref exact |
| 10 | elyaniv2010foundations; geifman2017selective | OFFICIAL (El-Yaniv, JMLR 11:1605–1641) / SECONDARY (Geifman, dblp) | supports | NeurIPS server blocked |
| 13 | scheirer2013openset; hendrycks2017baseline | OFFICIAL-PUBLISHER-VERIFIED | supports | Crossref; arXiv 1610.02136 (ICLR 2017) |
| 14 | howard1966voi; wald1947sequential | OFFICIAL (Howard) / SECONDARY (Wald via contemporary reviews) | supports | no live publisher page for a 1947 Wiley book |
| 15 | w3c2013provdm | OFFICIAL-PUBLISHER-VERIFIED | supports incl. the negative claim | PROV-DM Rec 2013; PROV-CONSTRAINTS validates provenance well-formedness, not result verdicts — the ledger's negative claim confirmed as written |
| 17 | iaasb2009isa330 | SECONDARY-VERIFIED | supports | controls-vs-substantive distinction confirmed from standard text |
| 18 | iso31000risk | OFFICIAL-PUBLISHER-VERIFIED | supports (guidelines-level, as scoped) | iso.org listing (direct fetch 403) |
| 19 | goldman1979justified; gettier1963justified; sep-reliabilism | OFFICIAL-PUBLISHER-VERIFIED | supports | all three exact |
| 20 | sep-types-tokens | OFFICIAL (archived edition) — **MISMATCH FIXED** | supports | live entry replaced 2026-05-01 (Liebesman); bib repointed to archived Wetzel edition, year corrected to 2006 |
| 21 | plantinga1993warrant | OFFICIAL-PUBLISHER-VERIFIED | supports | OUP 1993 |
| 22 | millikan1984language | SECONDARY-VERIFIED | supports | MIT Press blocks fetch; confirmed via reviews |
| 23 | sep-generality → Conee & Feldman 1998 | OFFICIAL-PUBLISHER-VERIFIED — **MALFORMED ENTRY FIXED** | complicates, as ledgered | R2 bib entry was a pseudo-SEP record (Bishop & Trout); rewritten as the real article (Crossref 10.1023/A:1004243308503) |
| 24 | sep-transcendental; stroud1968transcendental | OFFICIAL-PUBLISHER-VERIFIED — **AUTHOR SET FIXED** | supports | entry now Stern **& Cheng** (Fall 2023); bib updated; Stroud J Phil 65(9) 1968 exact |
| 25 | sep-abstract-objects; sep-modality-varieties | OFFICIAL-PUBLISHER-VERIFIED | supports | authors unchanged; edition years newer than bib (minor) |
| 26 | sep-ontological; sep-cosmological | OFFICIAL-PUBLISHER-VERIFIED — **AUTHOR SET FIXED** (ontological) | supports (contrast-class use) | entry now Oppy, Rasmussen & Schmid; bib updated; cosmological revised 2026-07-01, Reichenbach sole author |
| 27 | anderson2011lord | OFFICIAL-PUBLISHER-VERIFIED | supports | Philosophia Christi 13(2):321–338 |
| 28 | plantinga2011conflict | OFFICIAL-PUBLISHER-VERIFIED | supports | OUP 2011 |
| 29 | hume1739treatise; hume1748enquiry | SECONDARY-VERIFIED | supports (loci exact) | davidhume.org; EHU section titles match cited use |
| 30 | kemp_smith1905naturalism; garrett1997cognition; sep-hume; sep-induction | OFFICIAL / SECONDARY (Garrett) — **sep-hume MISMATCH FIXED** | complicates, as ledgered | live SEP Hume entry replaced 2026-06-16 (Qu & Radcliffe); bib repointed to archived Morris & Brown edition; Kemp Smith dual issue-numbering noted (not an error) |

Rows already `WEB-VERIFIED` in R2 (AURC lineage incl. Traub et al. 2024 criticism; HKUST-CS98-01 metamorphic TR; Givan et al. 2003; Hoover 2004) stand; Hoover 2004 carries a new **scope note**: the article establishes the eternal-genus/temporal-particulars doctrine for divine *acts/creation*; its extension to divine *speech* is in Hoover's related work (Atharī paper §3.2 states this inline).

**Counts:** 26 re-graded rows → 20 rows fully OFFICIAL-PUBLISHER-VERIFIED, 3 split official/secondary, 5 SECONDARY-VERIFIED (in every secondary case the official server blocked automated access; no doubt about the record), **0 UNVERIFIED**. Six bibliographic mismatches found; **all fixed in `references/orthemology.bib` this pass** (two replaced SEP entries repointed to archives; two author-set updates; one malformed entry rewritten; one unconfirmed year corrected).

## Modal support and grounding: inherited attribution scope

This additive section concerns the modal-support and grounding additions to `mathematics/information-and-inquiry.md` §9.13 and `foundations/received-actuality-and-intrinsic-necessity.md` §§7.6–7.7,10.24,12.18. It does not regrade the historical R3 rows above. Its evidence is Appendix D of the public September 2026 *Orthability and Necessary Being* supplement, Git blob `410dfe3f9465675481234ea36ec716f4641b4abe`. The full bibliographic entries and individual inherited reading scopes are directly readable in [the foundation work](../../foundations/received-actuality-and-intrinsic-necessity.md#inherited-modal-source-register).

`VIA-COMPILATION` here means that this consolidation inspected the exact public predecessor's report, **not** that it freshly opened or authenticated the external primary text. The predecessor-reported access is retained separately. Its philosophical attributions remain source-relative reportage; the displayed mathematical proofs do not acquire philosophical premise warrant from these citations. The earlier row 27 publisher-record status for Anderson/Welty is unchanged and does not alone verify the newly cited content.

| Source | Stable locator | New attribution status | Predecessor-reported access and exact use |
|---|---|---|---|
| Leibniz, *On the Ultimate Origination of Things* (1697), P1 | [Translation](https://www.leibniz-translations.com/ultimateorigination); LH 4, 1, 10, fols. 2–4 | VIA-COMPILATION | Indexed author-text translation; separate Inters page incomplete. Series-internal reasons versus total explanation, not later metaphysics. |
| Anderson and Welty, “The Lord of Non-Contradiction” (2011), P2 | [Author manuscript](https://www.proginosko.com/docs/The_Lord_of_Non-Contradiction.pdf); existing R3 row 27 | VIA-COMPILATION for content attribution; existing publisher-record status unchanged | Sections/footnotes 31–33 and relevant PDF pages reported read. Essential-owner argument and rotating-thinker response; no adoption. |
| Ibn Taymiyya, *Commentary on the Asfahani Creed*, P3 | [Usul transcription](https://usul.ai/t/sharh-caqida-isfahaniyya/94) | VIA-COMPILATION | Reported Arabic digital-transcription checks, not critical-edition or scanned-page authentication. URL 94/display 1/98 is not verified printed pagination. Separate Wikisource locator register unavailable in the supplied body. |
| Pearson, “Grounding, Well-Foundedness, and Terminating Chains,” P4 | DOI 10.1007/s11406-022-00593-x | VIA-COMPILATION | Primary article consulted according to predecessor; nuanced foundation versus termination, not warrant for this particular relation. |
| Bliss, “Viciousness and Circles of Ground,” P5 | DOI 10.1111/meta.12072 | VIA-COMPILATION | Publisher abstract/bibliographic record only, no full argument verification; challenge to automatic circularity exclusion. |
| Zalta, “Essence and Modality,” P6 | [Author abstract](https://mally.stanford.edu/abstracts/essence.html) | VIA-COMPILATION | Abstract only, not full-paper review; Fine counterexamples and differentiated response. |
| Boros, Gurvich, Milanič and Uno, “Conformal Hypergraphs: Duality and Implications for the Upper Clique Transversal Problem,” P7 | DOI 10.1002/jgt.23238; arXiv 2309.00098 | VIA-COMPILATION | Primary minimal-transversal and dual-hypergraph definitions inspected according to predecessor; no new blocker novelty. |
| Loss, “Grounds, Roots and Abysses,” P8 | DOI 10.1002/tht3.192 | VIA-COMPILATION | Publisher abstract only; grounding/recombination antecedent, no theorem-specific full-text claim. |
| Pruss, author-hosted Leibnizian cosmological argument treatment, P9 | [Author page](https://alexanderpruss.com/papers/LCA.html) | VIA-COMPILATION | Indexed passages; full-page open timed out. Explanatory sufficiency versus entailment, not full chapter/monograph review. |
| Trogdon, “Grounding: Necessary or Contingent?”, P10 | DOI 10.1111/papq.12009 | VIA-COMPILATION | Primary abstract only; epistemic/essence premises for full-ground necessitation. |
| Pearce, “Metaphysical Rationalism Requires Grounding Indeterminism,” P11 | DOI 10.1017/apa.2024.17 | VIA-COMPILATION | Primary full text reported consulted; autonomy, necessary existence and necessitation; no new novelty claim. |
| Hume, *Dialogues Concerning Natural Religion*, Part IX, P12 | [Hume Texts Online](https://davidhume.org/texts/d/9), 9.3 and 9.5–9.10 | VIA-COMPILATION | Primary-text access reported; Demea/Cleanthes/Philo voices separated, no automatic author endorsement. |

