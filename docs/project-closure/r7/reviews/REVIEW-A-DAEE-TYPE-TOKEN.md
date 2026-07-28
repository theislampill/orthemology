# R7 Review A — daee type/token audit

Surfaced model: `claude-opus-4-8` (substituted; draft PR, not merged). Attacks tried to collapse: deformation→metaortheme, Ψᴵ→ground truth, Diagnostic IR→one metaorthemma, runtime closure→restoration.

- deformation collapsed into a metaortheme governing standard — **DEFEATED** (crosswalk validator: deformation row must map to ortheme-level candidate state-types, not metaortheme).
- Ψᴵ asserted as ground truth — **first-run SUCCEEDED, then repaired**: the not-ground-truth check passed on any row's "not ground truth" string (the Diagnostic IR row also contains it), so it was not anchored to the Ψᴵ row. Hardened to check the Ψᴵ row's own non_claims disclaim ground truth AND soul access; attack re-run → DEFEATED.
- Diagnostic IR collapsed into one metaorthemma / runtime closure into restoration — **DEFEATED** (crosswalk validator: IR row is many-to-one and "NOT one metaorthemma"; runtime-closure row and fixture N9 keep Ψᴺ separate from uptake).

No blocking findings after the Ψᴵ hardening.
