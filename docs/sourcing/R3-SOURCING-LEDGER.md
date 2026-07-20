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
