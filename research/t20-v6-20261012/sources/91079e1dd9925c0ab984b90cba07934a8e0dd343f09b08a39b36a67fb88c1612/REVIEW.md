# Independent exact internal-uniqueness independence transfer

Status: PASS. Frozen module and both independent controls freshly replayed without warnings or source defects. No further core expansion is included.

## Exact findings

The module transfers the previously reviewed Rigidity independence result to the literal existing InternalRecursorPrinciple.Uniqueness type using actual source proofs, not semantic reflection or a presumed Rigidity inhabitant.

For any alleged HasE [] p Uniqueness, `appE_arrow` applies the actual closed Uniqueness→Rigidity source proof to p. The resulting hypothetical HasE Rigidity derivation contradicts the existing external `rigidity_uninhabited`. No source evidence of Rigidity is assumed globally or produced unconditionally.

For any alleged HasE [] p (Uniqueness→bottom), `composeE` constructs the actual source term S(K p)(rigidity_implies_internal_uniqueness) at Rigidity→bottom. Original Form checks cover all arrow types and their instantiated codomains. This hypothetical source negation contradicts the previously established external `no_internal_negation` of Rigidity.

`appE_arrow` accepts arbitrary HasE function and argument derivations using actual piElim and inst_wk. `composeE` uses the actual S and K typing constructors and those applications. It does not assume general HasE weakening or substitution. Its generic endpoint types X/Y/Z have original Form evidence; that is sufficient for the exact closed Rigidity/Uniqueness/bottom specialization.

The final claims quantify over every source proof polynomial: neither Uniqueness nor Uniqueness→bottom has a closed HasE inhabitant. The smaller original Has calculus inherits both exclusions by the checked inclusion. These are external nonderivability statements, not source negation inhabitants or an inconsistency claim.

## Replay boundary

Frozen module plus independent exact-conclusion/source-composition/ancestry controls are compiled fresh with Lean 4.19.0 --trust=0, reusing retained dependencies read-only and never rebuilding the baseline. Source-only ancestry is checked for appE_arrow and composeE. The two independence branches are separately checked to inherit the correct Rigidity discriminator theorem. Earlier frozen review manifests and dependency objects are verified unchanged.

No higher coherence, UIP, new calculus adoption, or additional model construction is part of this review.
