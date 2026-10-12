# Concrete countermodel for the original HasE universal W

10 October 2026. The tentative homogeneous-PER model succeeds. The actual original universal scalar-fusion type is uninhabited in HasE, proved by a fully constructed, sound semantic countermodel.

## Exact checked conclusion

`HomogeneousOriginalW.original_W_uninhabited` proves, for every original source polynomial p,

    ¬ P01AC.ExtensionalRepair.HasE [] p
        (P01AC.ExtensionalRepair.ExactScalarFusion.W
          P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed).

`original_c3_not_W` states the original requested c3 instance directly. `W_empty` proves that the semantic relation interpreting the actual W has no elements; `nu_N` supplies a concrete admitted Church member. This is an external source-nonderivability theorem, not a source inhabitant of W→Bottom. No theorem about global #9/T20 closure, completeness, all proposed extensions, or arbitrary compiler targets is asserted.

`HomogeneousOriginalIdentity.literal_original_identity_uninhabited` also proves that no p inhabits the original compiler identity Id_(N→N)(variableExpr.closed, redundantExpr.closed). It invokes the already retained source theorem ScalarFusionCore.forward_fixed and original endpoint typing; no later four-way module is required.

## Why this is a genuine whole-source countermodel

The carrier is an explicitly constructed finite-term algebra with I/K/S, two inert atoms, application, and one extra semantic case combinator ν. The exact compatible thirteen-rule rewrite system is proved confluent by parallel complete developments. Atom separation and the application head-origin lemma are derived, not postulated.

The type universe contains all conversion-saturated PERs with atom-only support, function-only support, or the universal relation. Pi/Sigma/All closure is proved. In the difficult Sigma case with universal first PER, dependent-family extensionality forces all fibers to be equal; the result is universal or function-supported. Raw is universal, Bottom empty, and identity evidence has I-class support.

The new HenkinSoundness module proves formation eligibility, dependent coherence and the fundamental theorem by induction on all actual FormE/HasE constructors. The source grammar, finite typing rules, original conversion and compiler are imported unchanged. There is no assumed model-existence or soundness contract.

The same ν is used at every type. It performs zero iterations on atom-valued seeds and one on function-valued seeds, while respecting every member of the entire admitted universe. It is not a type-indexed zero-on-Pi/one-on-Sigma family and it passes the literal cross-typing observer.

Take the discrete two-atom PER, n=ν, f=K a1 and a=a0. The left scalar endpoint reduces to a0. The unchanged original q runs n at the encoded state seed, which is a function weak-head value, so q ν reduces to successor zero and the right scalar endpoint reduces to a1. These atoms are proved distinct. `LiteralCounterexample.original_q_eval` binds this calculation to actual `redundantExpr.closed`, using the retained original compiler theorem, rather than an unbound formula mirror.

## Files and verification

- `operational/CaseOperational.lean`: concrete carrier, confluence, strictness, separation, ν laws
- `../homogeneous-per-closure-20261010/HomogeneousPER.lean`: PER closure, with no closure postulates
- `../homogeneous-per-closure-20261010/ConcreteUniverse.lean`: actual carrier/universe adapter and ν Church membership
- `../homogeneous-henkin-source-soundness-20261010/SourceTransport.lean`: exact original-source transport
- `../homogeneous-henkin-source-soundness-20261010/HenkinSoundness.lean`: whole actual-source soundness
- `LiteralCounterexample.lean`: imported original q and concrete scalar computation
- `OriginalWNoninhabitation.lean`: actual universal W emptiness and all-term source noninhabitation
- `OriginalIdentityNoninhabitation.lean`: exact original unary compiler identity noninhabitation
- `MATHEMATICAL_CONSTRUCTION.md`: complete mathematical construction and all-twenty-rule audit

Run `python homogeneous-per-model-20261010/replay.py` from the workspace. It checks frozen source hashes and pinned original inputs, then compiles all eight new modules in a fresh output directory under Lean 4.19.0, --trust=0. It reuses the verified original baseline objects read-only and does not rebuild the 83-module closure. The retained actual ScalarFusionCore SHA-256 is 975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618.

The fresh combined replay receipt is `validation/REPLAY.json`, status PASS. Printed axiom dependencies are limited to Lean's ordinary propext, Classical.choice and Quot.sound. No sorry/admit, custom axiom, unsafe implementation or native evaluation shortcut is present. The one recorded linter warning is an unused proofErase premise, because Raw is universal.

Independent review is separate from this author's replay. No protected source or predecessor file was edited; no repository integration or publication occurred.
