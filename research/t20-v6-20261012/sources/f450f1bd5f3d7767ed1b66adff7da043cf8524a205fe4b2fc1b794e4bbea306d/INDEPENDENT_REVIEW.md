# Independent review: open-term full-PER standardness

## Verdict

PASS for the explicitly bounded open-term full-PER claims. I found no blocking mathematical or Lean defect in `OpenTermStandardness.lean`, `FrozenCompilerMirror.lean`, or `PERInterface.lean` at the hashes recorded in `independent-reviewed-sha256.txt`.

The inherited literal judgement `HasE [] c3 (W q)` remains OPEN. This review does not establish a sound interpretation of HasE, an imported-source theorem, or a general impossibility of all PER countermodels.

## Fresh verification

Lean 4.19.0 (commit `6caaee842e94`) rebuilt all three modules in order into a fresh reviewer output directory. The build used only those freshly rebuilt local modules plus Lean's standard library; it did not rely on the author's existing local `.olean` files. All commands exited successfully. The complete output is in `independent-clean-build.log`.

The main standardness and characterization results depend only on `propext`. Mirror abstraction/fusion and typed endpoint equality depend on `propext` and `Quot.sound`. No `sorryAx`, new postulate, unsafe implementation, or external oracle occurs in their reported dependencies. These are kernel-checked theorems with the listed ordinary Lean axioms, not axiom-free results.

Reviewer-only `ReviewerChecks.lean` additionally verifies the converse `UniformIter n → Church n`, concrete Church inhabitants, the independence of `eval qPoly` from its environment, and the vacuity of testing only the total PER. Its final build also succeeds without `sorryAx`. No author Lean source or supplied source copy was edited by this reviewer.

## 1. Full PER versus Henkin boundary

`SatPER` ranges over every binary relation on the finite open-term carrier that is symmetric, transitive, and saturated under the stated SKI conversion relation. `Church n` universally quantifies over this complete Lean type, not an unstated chosen collection of admissible relations.

The orbit relation is a genuine saturated PER: it relates conversion-equivalent terms that lie in the conversion closure of a finite iterate of the chosen seed. Its proof neither presumes distinct iteration indices are distinguishable nor presumes the result to be standard.

The decisive relation is the fresh-generator orbit selected for each particular input term. `one_fresh_orbit_suffices` accurately records the weaker sufficient premise. A Henkin/subcollection interpretation can use this theorem only after proving that this particular orbit is admissible. No such closure is automatic. Similarly, a closed-only SKI carrier does not provide the fresh variables used here. The theorem must not be advertised as standardness for every PER interpretation or every carrier.

The full premise is not merely vacuous: concrete finite successor numerals satisfy it, and the new interface proves `Church n ↔ UniformIter n`.

## 2. Fresh substitution fixes arbitrary finite open inputs

The support bound is proved structurally over every constructor, including application and the inert zero/one markers. Every variable occurring in `n` has index strictly below `bound n`. The selected indices `bound n` and `bound n + 1` are therefore distinct and absent from `n`.

`freshSubst_fixed` is universally quantified over arbitrary replacement terms `f` and `a`; it does not assume that `n` is closed or that the replacements avoid the fresh indices. Substitution is simultaneous and does not recursively resubstitute inside its replacements. This is exactly what is needed. `Conv.subst` separately proves stability of the whole conversion relation under that substitution.

The witness count is extracted once from the fresh-orbit instance, before arbitrary `f` and `a` are introduced. Consequently the conclusion really is `∃ k, ∀ f a, ...`, not the weaker `∀ f a, ∃ k, ...`.

## 3. No disguised relational-parametricity premise

`ChurchAt` is ordinary self-membership in the arrow-PER interpretation of `(R → R) → (R → R)`. The proof uses a single same-carrier PER instance and syntactic substitution stability. It does not assume an abstraction theorem, graph-relations theorem, naturality law for all semantic maps, representation theorem, or derivability hypothesis.

`PERInterface` constructs ordinary arrow and Church PERs explicitly. `identity_q_related` treats arbitrary related Church inputs `n,m`, obtains Church membership of `m` from PER symmetry/transitivity, and transports the two endpoints by conversion saturation. Its result is genuine typed relational equality in this reduct, not just agreement on identical inputs.

## 4. Source formula correspondence

I compared the actual supplied source definitions against the mirror:

- `P01Polynomials.lean`: polynomial substitution/renaming, free-variable test, predecessor drop, whole-subterm K-priority abstraction, pair, and both projections.
- `EffectiveObserver.lean`: iteration body and twice-abstracted input numeral.
- `EffectivePrimitiveRecursion.lean`: successor body and its three abstractions; the retained recursion formula is consistent with the named pair-state body.
- `UArrowAndCompilerControls.lean`, compiler-body namespace: diagonal successor step, double-zero pair seed, literal pair-state body, and the outer abstraction in `redundant_closed_exact`.

No changed binder algorithm, eta contraction, body normalization, or altered pair-state recursion was introduced. Differences are type/name changes, alpha-renaming of local binders, equivalent evaluation notation, and omitted inferable type annotations. The mirror's choice of default environment does not affect its q: reviewer theorem `q_environment_independent` kernel-checks this directly.

This is checked formula correspondence, not a formal imported embedding theorem. The supplied compiler-control statement about `redundantExpr.closed` is not recompiled against its missing full source dependency closure by this isolated test. Keep that provenance/import boundary explicit. The unrelated `UArrowControl.q = K K` in the same source file is a different namespace and must not be confused with the mirrored compiler q.

## 5. Precise conclusion and overclaim guards

Established:

1. Full saturated-PER Church membership on this open-term SKI carrier is equivalent to a uniform finite iteration behavior.
2. The retained compiler formula mirror has scalar fusion after two arbitrary erased applications on every such Church member.
3. I and the compiler formula mirror q are related at the Church-to-Church arrow PER, including heterogeneous related inputs. Therefore this particular reduct cannot distinguish those endpoints at that type.

Not established:

- Uniqueness of the iteration index. The current result is existence of a uniform index.
- Bare raw conversion `n ≈ numeral`, `q n ≈ n`, or `q ≈ I`; the standardness/fusion statements concern applications, and the endpoint theorem concerns a typed PER relation.
- Closure or soundness of the full dependent/impredicative HasE interpretation, especially identity and dependent type rules.
- The original syntactic witness `HasE [] c3 (W q)`, its nonderivability, or any completeness principle transferring reduct equality to that judgement.
- Elimination of countermodels using another carrier, an admissible-relation/Henkin restriction, or another valid interpretation of the missing full calculus.

The source comments and parent task's stated open boundary are consistent with these limits.
