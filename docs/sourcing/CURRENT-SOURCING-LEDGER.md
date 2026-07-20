# Current sourcing state (consolidated view — R6, Decision 0019)

**Start here.** This view names, per claim area, where the *current* source
status lives. It deliberately duplicates no status value: the authoritative
rows stay in the surfaces linked below, and
[`SOURCING-STATUS-INDEX.yaml`](SOURCING-STATUS-INDEX.yaml) is the
machine-readable classification behind this page
(`scripts/validate_sourcing_state.py` enforces both). A green validator run
establishes classification and internal agreement, never source truth.

| Claim area | Current authority | Notes |
|---|---|---|
| Concrete/ideal-reason attribution chain | [`references/source-status.yaml`](../../references/source-status.yaml) rows `CIR-*` | CIR-1 bibliographic vs CIR-1W wording split; CIR-1W promotion trigger: publisher full-text access |
| El-Tobgui records | registry rows `ELT-*` | three distinct works |
| Atharī companion per-claim rows | registry rows `ATH-*` | ATH-3 = `COMPILATION_MEDIATED` (promotion trigger: direct edition access; doctrine unchanged) |
| Sequential latent-variable related work | registry rows `LAT-*` | bounded by Decision 0015 |
| Project's own formal extension | registry rows `EXT-*` | no external source claimed |
| Qurʾānic loci | [`references/quran-loci.yaml`](../../references/quran-loci.yaml) | 29 loci, primary-verified (R3), own CI validator |
| Academic corpus (manuscript related work etc.) | [`R3-SOURCING-LEDGER.md`](R3-SOURCING-LEDGER.md) | R3 regrading overlay over the R2 baseline; where R3 names a row, R3's status is current |
| Companion philosophical + classical layer | [`companion/sourcing/R3-COMPANION-SOURCING-LEDGER.md`](../../companion/sourcing/R3-COMPANION-SOURCING-LEDGER.md) | same overlay rule; inference-boundary labels retained there |

**Historical baselines (statuses superseded where regraded):**
[`SOURCING-LEDGER.md`](SOURCING-LEDGER.md) and
[`companion/sourcing/COMPANION-SOURCING-LEDGER.md`](../../companion/sourcing/COMPANION-SOURCING-LEDGER.md)
— R2 ledgers preserved verbatim with additive banners; the R2 vocabulary
(`WEB-VERIFIED` / `RECORD-CONFIRMED`) is not current status vocabulary.
The main ledger's later additive rows 31–38 remain readable there; rows
36–38 are additionally governed by registry family `LAT-*`.

**Standing research triggers (open, ordinary research — not owner-only):**
CIR-1W publisher full-text access; ATH-3 direct edition access (RR-1
pagination residual); RR-2 Evans 1998 p. 94; RR-3 Taymiyyan *Darʾ*
primary-locus queue.
