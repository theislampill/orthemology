# R3 Review B — source and citation forensics (adversarial)

**Posture: assume citations are wrong until re-derived.** Every row re-checked against the R3 verification records; attacks per mandate §13.

| Attack | Result | Disposition |
|---|---|---|
| Wrong verse number | Found exactly one across 29 āyāt: 20:11 (should be 20:11–12) | **FIXED corpus-wide**; registry + CI validator prevent recurrence |
| Wrong hadith number | Muslim 2708 primary-verified (exact wording) | **CLEAN** |
| Fabricated/incorrect DOI | All DOI-bearing records resolve via Crossref to exactly the claimed works; 0 fabrications | **CLEAN** |
| Secondary compilation masquerading as primary | The compilation-mediated classical loci were flagged VIA-COMPILATION in R2 and are now work-level verified (existence/attribution primary or official); page numbers remain edition-dependent and are *flagged as such inline* | **FIXED at work level; pagination deferred** (trigger: edition acquisition/library check before external submission) |
| Live-reference rot | Two SEP entries were REPLACED since R2 (hume 2026-06-16; types-tokens 2026-05-01); two gained co-authors (transcendental; ontological); one bib entry was malformed (pseudo-SEP generality); one year unconfirmed (Wetzel) | **ALL SIX FIXED** — archive-edition URLs (win2025 hume archive existence re-verified), author sets updated, entry rewritten |
| Quote/context mismatch | Majmūʿ-vol-12 words/voice formula verbatim-confirmed in vol 12; Hoover 2004 scope-noted (acts/creation focus, speech in related work); 2:120/3:61/55:1–3 marked school-internal inference in the registry | **FIXED/annotated** |
| Unsupported negative literature claim | PROV negative claim re-confirmed against PROV-DM + PROV-CONSTRAINTS scope; "no practice…" universals remain scoped to the internal record | **HOLDS** |
| Attribution laundering via the compilation | The "concrete/ideal reason" phrase pair could NOT be confirmed in Evans's or Turner's accessible text — prose softened to compilation-reported; open item; Darʾ loci held in a verification queue, all companion attributions labeled secondary reconstruction | **DOWNSCOPED, honestly** |
| Hagiography as history | Courtroom narrative downgraded to doctrinal-usage evidence with Cooperson/Melchert/Madelung noted | **FIXED** |

**Residual findings:** (1) six classical page numbers edition-dependent — deferred with trigger, non-load-bearing; (2) Evans/Turner phrase pair — open item, non-load-bearing; (3) Ashʿarī/Māturīdī sourcing is SECONDARY-VERIFIED (tradition-internal anchors read via surveys/databases), not page-level primary — stated inline in §7. No unavailable-source purchase blocker was identified after the documented search.

**Verdict:** no load-bearing current claim rests solely on VIA-COMPILATION or UNVERIFIED material; the sourcing lane is closed **to the stated threshold** (work-level verification; graded statuses; open items itemized with triggers).
