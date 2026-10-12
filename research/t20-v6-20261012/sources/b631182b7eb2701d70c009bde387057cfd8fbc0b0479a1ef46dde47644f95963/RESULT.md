# Full source soundness for the concrete homogeneous Henkin universe

## Checked result

`HenkinSoundness.lean` proves soundness for the actual imported `P01AC.ExtensionalRepair.HasE` judgment and formation/coherence for the actual imported `FormE` judgment. Neither source grammar is copied, restricted, or augmented with semantic premises. The mutual inductions follow the original recursors, including finite derivations, dependent Pi/Sigma, impredicative All introduction/elimination, identity introduction, J, proof erasure, conversion, Pi extensionality, and All extensionality.

Main results:

- `HenkinSoundness.fundamental`: every actual `HasE Γ p A` maps related environments to related realizers at `F A`.
- `HenkinSoundness.formation_eligible`: every actually formed type at an admissible environment belongs to the concrete homogeneous universe.
- `HenkinSoundness.formation_coherent`: actually formed types have equal interpretations at related environments.
- `HenkinSoundness.finite_sound`: soundness for the full original `FiniteDerives` grammar, including its own impredicative elimination.
- `HenkinSoundness.closed_not_derivable_of_empty` in `DependencyAudit.lean`: an empty interpretation of a closed type rules out every actual source proof polynomial of that type.

The interpretation uses all eligible saturated PERs, represented by the subtype `{ R : Rel // ConcreteUniverse.U R }`. It does not select a finite menu of test relations. `Raw` is the universal relation; `Id` is the I-conversion class if its endpoint relation holds and empty otherwise. These are semantic choices of this sound model, not modifications to the source grammar. There are no hypotheses asserting source soundness, closure of source-formed types, or coherence as model contracts: eligibility and coherence are established together with typing soundness.

## Carrier and source transport

The carrier and conversion are the separately checked `CaseOperational.T` and `CaseOperational.Conv`. Source zero/one embed as a0/a1, source I/K/S embed literally, and source application remains application. Polynomial interpretation is compositional and independent of type or derivation.

`SourceTransport.lean` transports the original K-priority abstraction beta theorem to arbitrary environments in the enlarged carrier, including environments containing ν. It uses a parameterized fold of the old open-term carrier; old variables `0` and `n+1` represent the new arbitrary argument and environment entries. It proves all actual original polynomial conversion generators sound. No restriction to source-image valuations is imposed.

## Verification

Run `./check.sh`. It checks the three additive modules with Lean 4.19.0 and `--trust=0`, reusing retained original imported source objects. The original baseline is not rebuilt or changed. `validation/check.log` records exact signatures and axiom audits.

The printed dependency footprints of `fundamental`, `form_sound`, `has_sound`, `formation_eligible`, `formation_coherent`, `finite_sound`, `fundamental_j`, `F_mixed`, and the closed-nonderivability corollary contain only `propext`, `Classical.choice`, and `Quot.sound`. There are no custom axioms or sorry dependencies. One harmless unused-variable warning records that proof erasure into universal Raw does not need its semantic identity premise.

`MANIFEST.json` records source input and additive Lean file hashes.

## Scope

This directory proves full source soundness. The actual original-W counterexample application is assembled separately by the model author from this theorem and its checked literal compiler endpoint calculations. Source nonderivability established that way is a meta-level theorem; it is not a source proof of `W → Bottom`, and it does not negate the already established validity of the endpoints in a different standard full-PER interpretation.
