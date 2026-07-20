# Pilot-0 v2 packet history

- **v2.0** (R3 freeze, packet hash `a1edbd2c5e2f2df598b4a6d01a52229c455b3b68d043f10046053d0a3622a2a2`):
  the original v2 execution specification is preserved byte-for-byte here as
  [`EXECUTION-SPEC-v2.0.md`](EXECUTION-SPEC-v2.0.md). Its §4 decision rule
  (*adopt-candidate / reject / undetermined*) conflicted with the v1
  protocol's feasibility-only constraint, described unstated margins as
  "pre-registered", referenced an analysis variant that did not exist in the
  tree, and repeated the mis-stated v1 freeze hash (`ece0412f…`; the correct
  v1 hash has always been `988a6522…` — R4 correction SELF-1).
- **v2.1** (R6): the live packet at [`../pilot0-v2/`](../pilot0-v2/) —
  feasibility-only outcomes (`ADVANCE_TO_PILOT1` /
  `REVISE_AND_RETEST_INSTRUMENT` / `DO_NOT_ADVANCE_THIS_ITEM_VERSION` /
  `INCONCLUSIVE`), numeric feasibility gates or named deferral markers, a
  real flag-aware v2 analysis script with mock traversal, and Decision 0018
  status vocabulary. New freeze hash in `../pilot0-v2/FREEZE-HASH.txt`.

No run of any version has occurred; no term is adopted or retired.
