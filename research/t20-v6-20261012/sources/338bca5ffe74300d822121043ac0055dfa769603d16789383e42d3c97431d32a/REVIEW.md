# Independent review: all-Raw source Church canonicity

Verdict: PASS, bounded to the stated all-Raw fragment. No blocking mathematical or implementation finding. No source changes requested.

Reviewed candidate: `hase-raw-context-uniformity-20261010`, exact frozen `RawContextUniformity.lean` SHA-256 `c5ec4ae7bb8da3e914320a9e3b7ce4e400c497af2369dec52c7821134c69f28b` and `RawContextControls.lean` SHA-256 `5515a1dac8cb4b6a443dc313ab1f67cd2756a8a079867d95f5d9a7d7dcbb86ae`. The complete input freeze is `REVIEW_INPUTS.json`; exact copies are under `frozen/`.

## Accepted result and proof audit

For every finite telescope consisting literally of the unchanged source `Ty.raw`, every actual `HasE Γ n N` has a count k and an actual `HasE Γ I (identity N n (inputNumeral k))`. The endpoint is the original polynomial n. This is a source identity under the whole telescope, not merely a family of closed-instance semantic equalities.

The proof correctly uses the following steps.

1. `FullPER.E []` requires a literal zero environment. `truncate_admissible` proves the finite zero-tail condition, including the empty case and the recursive head/tail obligations. Reflexivity of conversion suffices at each Raw coordinate. The scoping theorem for the actual HasE derivation then justifies `interp_agree`, so evaluation at arbitrary valuations is recovered without falsely declaring them admissible.
2. The shifted symbolic valuation assigns Raw coordinate j to open variable j+2, reserving variables 1 and 0 for the two Church observations. Whole-HasE FullPER soundness supplies Church membership; the inherited open-term standardness result supplies one count. This is not an assumption that a symbolic Church-typed hypothesis is itself a fixed numeral.
3. Reflection is specifically at the generic variable interpretation. The inherited `reify_interp` and `reify_embed` proofs retain source variables and packed atoms through the original bridge conversion rule. There is no semantic-completeness axiom or reflection at arbitrary collapsed environments.
4. `point_has` and `observation_has` use actual structural weakening with shifted source polynomials. `identity_of_observation` applies the existing identity introduction, two actual `HasE.piExt` constructors and one actual `HasE.allExt` constructor. Their typing, formation, scope and family premises remain present. Type-parameter weakening fixes an all-Raw telescope literally; its equality is supplied explicitly, not presumed for arbitrary contexts.
5. `raw_uniform_substitutions` lifts substitutions past the two reserved observation variables, then applies the existing polynomial-conversion substitution theorem. It concludes observation conversion for arbitrary polynomial replacements. It does not manufacture a typing or a substituted source identity without suitable scoping/typing premises.
6. `raw_uniform_evaluation` orders the count before all open-term valuations and arguments. The independent `same_count_everywhere` theorem strengthens the presentation by putting source identity, every polynomial substitution, and every valuation of every substituted endpoint into one existential package with the very same k.

The candidate contains no new grammar declarations, local replacement of HasE, conversion rules, axioms, or admitted proofs. New theorem axiom dependencies are restricted to the inherited standard Lean axioms `propext`, `Classical.choice`, and `Quot.sound`.

## Independent executable controls

`IndependentBoundaryChecks.lean` establishes:

- Any finite FullPER environment has a literal zero tail. The untruncated generic environment is inadmissible for every finite all-Raw telescope; the actual truncation repairs it.
- One count simultaneously supports the original open source identity, all polynomial substitutions, and all open-term evaluations of those substitutions.
- For every k and each coordinate j<m, `(K (inputNumeral k)) (var j)` is actually HasE-typed in `rawTel m`, has observation count k, and has the asserted source identity. This is nonvacuity at every count and every genuine finite Raw coordinate, not just a closed example.
- Replacing the free coordinate of the author's `(K I) (var 0)` by `var 100` retains observation count 1 but destroys HasE typing in `rawTel 1` by scoping. The unrestricted same-context typing-substitution claim is therefore false.
- Unrestricted reflection from conversion at `zeroEnv` is false: that valuation collapses distinct source variables whose generic interpretations are distinct normal forms.
- For every k and every proof polynomial r, `HasE [N] r (identity N (var 0) (inputNumeral k))` is false. FullPER soundness at the environment assigning that variable numeral k+1 would equate distinct iteration normal forms. Therefore general-context source canonicity itself is false, even allowing an arbitrary identity witness. This is stronger than merely refuting the generic-observation conclusion.
- The inherited I/SKK example remains source-identical while raw conversion remains false in the empty all-Raw context.

Three separate negative-compilation controls are rejected as expected: omitting the finite zero-tail proof, applying the all-Raw theorem to a Church-typed hypothesis, and using observation conversion as a source typing proof. The proved negative propositions above are the substantive boundary evidence; the compiler-rejection fixtures also check the exposed interfaces.

## Verification and reproducibility

Run `./check.sh` from this review directory, or `python3 replay.py`. The independent harness first verifies frozen candidate bytes, manifests, predecessor receipts, original grammar/source bindings, Lean binary, inherited object hashes, and acquisition byte/blob bindings. It reuses 92 verified baseline objects, the 4 scalar, 3 structural and 3 closed-identity additions, and the frozen extractor object. No inherited module or 83-module prerequisite baseline is rebuilt.

It then creates a fresh output directory and compiles only the two frozen candidate additions, the independent positive-control module, and the three expected-rejection fixtures with Lean 4.19.0 `--trust=0`. It checks exit codes, diagnostics, forbidden proof escapes and printed axiom dependencies. Candidate files are checked again after compilation. All 490 recorded hash checks pass in the final run.

Final replay: `validation/REVIEW_REPLAY.json` and `validation/REVIEW_REPLAY.log`. Fresh object and diagnostic hashes are recorded in the review manifest. Inherited objects are reused by hash and prior receipt rather than independently rebuilt in this bounded review. The fixture diagnostics are deliberately errors; the three positive modules have no warnings or errors.

## Scope and integration boundary

This is a genuine isolated extension from closed typed Church canonicity to finite all-Raw telescopes. It is not raw canonicity of n, strong normalization of arbitrary Raw replacements, arbitrary-context or arbitrary-type completeness, a general HasE substitution theorem, or an executable extraction procedure for new open derivations. The valuation carrier is the specified finite open SKI syntax.

Neither the proof nor this review establishes `HasE [] c3 (W q)`, an internal bound-n:N scalar identity, universal W, programme/T20/#9 closure, or field-level novelty. The [N] countermodel specifically prevents treating this result as generic Church-hypothesis canonicity. The original grammar and predecessor packets remain unchanged.
