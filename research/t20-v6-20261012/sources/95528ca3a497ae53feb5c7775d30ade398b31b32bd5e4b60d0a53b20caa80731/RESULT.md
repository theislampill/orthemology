# Church canonicity in a syntactically constrained structured context fragment

Status: isolated constructive intermediate, 10 October 2026. No integration, T20 closure, T21 work, or claim of arbitrary-type completeness. The original universal `HasE [] c3 (W originalQ)` and its negation remain OPEN.

## Exact increment

The previous all-literal-Raw theorem extends to a recursively specified class of genuinely structured source types. Every actual `HasE Γ n N`, when every entry of Γ belongs to the new syntactic class `Opaque`, has one finite k and an actual source derivation

`HasE Γ I (identity N n (inputNumeral k))`.

The original polynomial n, including its free structured coordinates, remains the endpoint. The class assumption is an inductive predicate on the unchanged source type syntax. It is not semantic admissibility supplied as a premise, source-proof existence used to define semantics, or either desired graph projection bridge.

Two grammars expose the variance condition:

- `Rigid`: Raw; Bottom; any identity type `Id_B p q`; or All of a Rigid body.
- `Opaque`: Raw; Pi with Rigid domain and Opaque codomain; Sigma of two Opaque parts; All of an Opaque body; or Pi with Bottom domain and any codomain.

These predicates do not independently certify source formation. Formation/scoping comes from the actual HasE derivation. Identity endpoints and carriers in the negative class, and the arbitrary codomain of a Bottom-domain Pi, may contain genuine type and term dependencies.

Thus admitted hypotheses include `Raw → Raw`, `Sigma Raw Raw`, nested products, Raw-curried functions, irrelevant All wrappers, functions out of identity-proof domains, and `Bottom → N`. The result holds for every derivable Church endpoint in such a telescope, not just the displayed example.

`opaque_uniform_substitutions` additionally gives the SAME k with the source identity and with generic-observation conversion after every polynomial substitution. `opaque_uniform_evaluation` orders one k before all open-term valuations and arguments, including valuations that do not preserve the structured typing. These last two conclusions concern conversion/evaluation; they do not assert a new HasE typing after arbitrary substitution.

## Constructive content of the new context bridge

`rigid_reflects` proves that the existing FullPER interpretation of a Rigid type relates only Raw-convertible representatives. For identities this follows from both proof representatives converting to I; it does not require the identity endpoints to be Raw-convertible. For All, one available PER instance suffices.

`opaque_admits` then proves that every Raw-convertible pair belongs to the interpretation of an Opaque type. In the Pi case, the proven negative-domain reflection and conversion congruence justify application. In the Sigma case, conversion of whole representatives gives conversion of each projection; no pair eta or reverse projection reflection is used. All works at every PER. Bottom-domain Pi is vacuous on its domain, without a restriction on its codomain.

Both lemmas compile without axioms. They are concrete induction proofs from the actual retained FullPER definition, not assumed relational contracts.

The new finite-telescope theorem establishes the exact zero-tail `FullPER.E` obligation. Scoping then recovers arbitrary full valuations as in the all-Raw predecessor. Whole-HasE soundness, inherited Church standardness, and inherited generic conversion reflection yield the uniform observation count. These three inherited ingredients are not claimed as new.

## A separate source improvement: arbitrary-context observation extensionality

`identity_of_observation` now works in ANY actual HasE context:

`HasE Γ p N → HasE Γ q N → PolyConvPlus (observe p) (observe q) → HasE Γ I (identity N p q)`.

Unlike the previous helper, it does not require an older-grammar `Ctx Γ` premise or `twkTel Γ = Γ`. It obtains `CtxE Γ` from the actual derivation, explicitly type-weakens both endpoint derivations into `twkTel Γ`, uses the type-closedness of N to retain their Church type, constructs the two Pi-extensionality steps there, and supplies that body proof to the unchanged `HasE.allExt` constructor in Γ.

This preserves all source formation, typing, scope, family and type-weakening obligations. It does not relax allExt or identify Γ with its type-weakened telescope. The observation conversion is still a genuine premise; the theorem does not produce that premise for an arbitrary n:N hypothesis.

The checked example `parameterSensitive = Pi (Id_(A→A) I I) Raw` is formed in the original source grammar, belongs to Opaque, and changes under twk. Its singleton context is covered by the new uniformity theorem, demonstrating that literal type-weakening invariance is genuinely unnecessary.

## Executable controls and sharp scope boundaries

The concrete context `[Raw→Raw, Sigma Raw Raw, Raw]` is source-formed and Opaque. Its source expression `f (fst z)` is typed Raw by actual Pi elimination and Sigma projection. Applying typed K and an actually typed Church I to this expression gives an open structured endpoint whose observation count is 1 and whose actual source identity to numeral 1 is checked. The universal theorem for every Church endpoint in that context is also instantiated.

A higher-order countercontrol explains the Pi polarity condition. Let

`u = var 1`, `v = S (K (var 1)) I`.

They are related in the retained interpretation of `Raw→Raw`, because every application of v converts to the corresponding application of u. They are distinct Raw normal forms, so they are not Raw-convertible. Consequently, a generic variable g cannot be self-related at `(Raw→Raw)→Raw`: that would require Raw conversion of the distinct normal forms `g u` and `g v`. Lean checks all conversions, normality proofs, and the inherited normal-form uniqueness application.

This proves failure of generic-variable admissibility for that particular higher-order type in this FullPER interpretation, and proves `Raw→Raw` is not Rigid and the higher-order type is not Opaque. It does NOT prove source noninhabitation, failure of every possible uniformity proof, or either negation of the original universal graph bridge.

The actual source Church variable in `[N]` remains excluded: the inherited no-count control proves N is not Opaque. The predecessor's stronger independent result refuting arbitrary-context source numeral canonicity remains unchanged.

## Residual gap

This enlarges an actual source uniformity class and removes an unnecessary fixed-telescope restriction from its source extensionality step. It does not establish the arbitrary-carrier projection bridges needed by the original scalar compiler. In particular it supplies no uniform numeral count for a free Church hypothesis, no internal scalar identity under n:N, and neither a proof nor a countermodel for `HasE [] c3 (W originalQ)`.

No new global normalization claim, raw conversion of n itself to a numeral, executable extraction procedure, general HasE term-substitution theorem, or field-level novelty claim is made.

## Verification and retained dependencies

`python3 replay.py` verifies pinned predecessor source/manifests/receipts, the Lean 4.19.0 binary, 92 retained baseline objects, 4 scalar objects, 3 structural objects, 3 closed-identity objects, the frozen extractor object, and the two raw-context objects. It then freshly compiles only the two new Lean modules with `--trust=0`. The original 83-module baseline is not rebuilt.

The new modules contain no admitted proofs, new axioms, native evaluator escapes, grammar replacement, or changed conversion rules. Reported dependencies are confined to inherited `propext`, `Classical.choice`, and `Quot.sound`. Initial compiler diagnostics are retained separately as author-work records; the final replay requires no warnings/errors and no sorryAx. No independent review is claimed by this author packet.

The precise retained-object paths and hashes are recorded in `INPUTS.json`; the new deliverable files are sealed by `MANIFEST.json`. Replay records fresh output hashes and repeats the input checks after compilation. Original predecessor bytes are only read.
