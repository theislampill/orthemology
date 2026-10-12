# Independent review: canonical carrier projection

**Bounded assessment: PASS for the stated raw-index carrier-projection claims.**
No blocking discrepancy was found between the sealed sources, their reported theorem statements, the unchanged canonical constructor owners, and fresh Lean checks. This is an independent evidence review, not canonical adoption or a governor-issued lifecycle/closure decision.

## Object and evidence

- Reviewed archive: `P01_Canonical_Carrier_Projection_2026-09-30.zip`
- SHA256: `4b5590eaa1667a1fb86fd55714412311dba9f14d6f294c830c36766db5252756`
- Archive: 3,123,289 bytes; 166 unique safe members; exact manifest coverage and every listed size/hash verified
- Author receipt SHA256: `ccbd96a111709809947f3197759dc7629838447262a5844fbca34bbfafba6495`
- Lean: 4.19.0, compiler commit `6caaee842e94`; binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`; eight supporting package revisions independently checked against the sealed receipt, with tracked source trees clean

An independently written driver rebuilt all 30 local modules from the sealed source bytes, in a freshly resolved dependency order. Its LEAN_PATH contains only the new output directory and pinned external package caches in `private-locator:4b06887cf6b87610e5b8`. No author qualification helper or prior local P01 object was imported. A fresh independent Lean environment inspection confirmed 19 checked declarations: 3 definitions and 16 theorems. All exact printed types and axiom sets matched the sealed receipt. The axiom union is exactly `propext`, `Quot.sound`, `Classical.choice`; the main projection module emitted no diagnostics.

Primary machine-readable evidence: `RECEIPT.json`, `CONTROLS.json`, `FINAL_VERIFICATION.json`; full command/output evidence is under `evidence/`.

## Source-owner binding

Canonical checkout: commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, clean before and after review. Both working-tree files were independently compared to their Git blobs at this exact commit and to the fresh compiled copies:

- `experiments/orthemology-v5/source/lean/InternalPolymorphism.lean`: SHA256 `7cf85525305944e343b50f63e9b593a0fdcab3c89303f2f32cdb37d92c70b1ee`; owns actual `Code`, `Code.top`, `Code.arrow`
- `experiments/orthemology-v5/source/lean/EffectsAndDependence.lean`: SHA256 `0e3adde9d907e2c0a28afb5087feb42986e2e1fd880682edd70d4b4214790be2`; owns actual `CoherentFamily`, `dependentPi`, `dependentSigma`, `pairTerm`, `equalityCode`

The source owners were not substituted or edited. The entire author result tree retained its initial byte snapshot. The raw-index predecessor and recursive predecessor archive hashes also remained at their stated pins.

## Claim-level findings

1. **Carrier construction: verified.** `carrierCode P` accepts exactly `P.rel t t`. Its stability derives from the PER's raw-conversion saturation. `carrierCode rawPER = Code.top` is equality of the actual Code values.
2. **Raw Pi square: verified with its stated restriction.** A canonical unary inhabitant supplies each self-related output. Raw-convertible arguments and application congruence supply PiPER's cross-argument condition. Global raw coherence supplies the legitimate fibre family. Arbitrary domain PERs cannot replace rawPER in this equality.
3. **Represented Sigma square: verified.** Forward projection chooses actual first/second projections and the representation witness. Reverse projection uses a witnessed canonical pair and raw saturation of SigmaPER. The general-P theorem explicitly requires both P-relational coherence and global raw-conversion coherence; the syntax-generated raw family supplies these from index transport.
4. **Raw identity square: verified.** RawPER endpoint relation is precisely canonical Conv. The proof-code requirement remains Conv to I on both sides. It is not arbitrary PER identity or raw eta.
5. **Syntax instantiations and source preservation: verified.** The Pi/Sigma/identity squares use the actual recursive interpretation and canonical constructors. All three admission theorems retain exactly `eval p η` under an actual `Has` derivation. Projected fibres still contain the original recursive PER interpretation; these equalities do not recursively replace every PER constructor by a unary constructor.
6. **Generic one-way inclusions and strictness controls: verified.** Generic relational arrow carriers imply unary arrows; canonical raw equality implies PER identity. Their converse directions fail in the specified generality.

## Focused challenges

Thirteen additional theorems in `sources/ScopeControls.lean` passed fresh compilation and axiom readback:

- Same unary carrier can hide different binary relations: totalPER and rawPER have equal carriers but are distinct PERs
- Direct unrestricted Pi counterexample: I lies in the canonical unary product for totalPER/rawPER but not in the relational Pi carrier
- A distinct identity counterexample using totalPER: PER identity between I and SKK is inhabited while the canonical equality is not
- Raw identity rejects nonconvertible I/SKK endpoints, and canonical equality separately checks its proof program
- P-coherence does not imply global raw coherence: an empty-domain example makes the former vacuous while raw-convertible inspected indices have unequal fibres
- The syntax-generated anchored identity fibre is genuinely nonconstant; the canonical Sigma admits the evaluated I/I pair and rejects the SKK/I pair
- Empty fibres make raw-domain canonical Pi and Sigma empty
- Exact carrier-domain and represented-Sigma contracts

Three isolated incorrect uses were rejected by Lean with type mismatches and produced no artifacts: substituting totalPER into the raw Pi square, substituting it into the raw identity square, and using propositional reflexivity as raw I/SKK conversion. The first two mathematical failures are established by the proved counterexamples above; rejection alone is not treated as evidence of impossibility.

One initial audit-control draft had an ambiguous unqualified `skk` name because both P01R and P01DF were open. Only audit-local controls were corrected to `P01DF.skk`; the failed draft/output is retained under `attempts/01-ambiguous-control-names/`. No reviewed source or theorem was repaired.

## Limits and disposition

This review does not establish general arrow equality, arbitrary identity equality, AllPER/canonical All equality, a syntax-wide recursively canonical interpretation, arbitrary typed dependent contexts, arbitrary heterogeneous index transport, full U11, normalization, universal frontend refinement, novelty, or canonical adoption. The raw-index syntax admits nonnormalizing terms. Code-carrier equality deliberately forgets relational information.

The selected Lean compiler, operating system, and existing pinned standard-library/Mathlib package caches remain trusted; those external caches were not independently rebuilt. This run does independently rebuild the entire local imported source closure and checks the requested declarations' transitive axiom sets. There is no broader acceptance or release authority in this report.
