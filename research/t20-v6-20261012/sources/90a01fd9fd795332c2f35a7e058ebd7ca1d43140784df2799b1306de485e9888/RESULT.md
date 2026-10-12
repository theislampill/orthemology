# Weak actual-E dependent induction exactly characterizes literal rigidity inhabitation

## Checked result

The additive module `InductionRigidityConverse.lean`, namespace `RigidityInitiality.FullE.InductionConverse`, proves:

- `weak_induction_iff_closed_rigidity`: the full actual-E weak dependent-induction schema is equivalent to `∃ r, HasE [] r SourceRigidity.Rigidity`.
- `weak_induction_implies_closed_rigidity`: the converse constructs a derivation of the literal retained Rigidity type with closed polynomial `abstract (abstract (abstract ident))`.
- `weak_induction_iff_generic_context`: the full schema is equivalent to its restriction to the single generic telescope `[StepAt (var 1), ZeroAt (var 0), NT]`.
- `contextual_weak_induction_iff_rigidity`: for any `CtxE Γ`, weak induction in every well-formed finite telescope extension of Γ is equivalent to `∃ r, HasE Γ r Rigidity`.
- `weak_induction_not_admissible` and `generic_induction_not_admissible`: the existing closed-R nonderivability theorem rules out the full schema and its generic-context restriction in the unchanged calculus.

`WeakInductionAt Γ` quantifies externally over a source family P, seed p and curried successor step s. Given `FormE (N :: Γ) P`, `HasE Γ p (inst P zero)` and `HasE Γ s (dependentStepType P)`, it asserts only `∃ t, HasE Γ t (.pi N P)`. There is no prescribed section polynomial, computation equation, coherence obligation or naturality requirement. `WeakInduction` quantifies this schema over all actual-E well-formed contexts. These are Lean metapropositions about derivability, not new object-language types or universes.

## Direct converse

For an arbitrary actual-E typed endomorphism u and its zero and successor witnesses, use the family

`P(n) = Id_N(u n,n)`.

The zero witness is already the required seed. `nat_congr` uses actual source J to lift the induction hypothesis through successor; `step_point` composes it with the supplied endomorphism successor law. `family_step` explicitly abstracts the induction-hypothesis and n binders, with actual-E formation and weakening. Thus the hypothetical schema supplies a section of this equality family.

The section is weakened and evaluated at the generic n. Actual J gives symmetry and transitivity, joining the raw identity-combinator beta equation to obtain `Id_N(I n,u n)`. The existing actual `piExt` constructor, with all type, endpoint and scope premises, yields the literal `ResultAt u = Id_(N→N)(I,u)`. Finally three actual Pi introductions discharge u, its zero witness and its successor witness, yielding the exact closed Rigidity type.

The canonical closed polynomial erases those dependencies: `piExt` returns I and the outer binders abstract it. Its typing derivation nevertheless depends essentially on the section derivation supplied by the hypothetical induction schema. This is not a premise-free typing claim, raw conversion from u to I, or reflection from typed identity into raw equality.

No internal Uniqueness proposition, U-to-R implication, original compiler identity, or semantic completeness theorem occurs in this argument. Three elementary shift equalities for the literal R ingredients are reproduced from the retained uniqueness-converse module to avoid importing or invoking that implication. Forward induction reuses the checked full-E conditional section theorem, after certified actual-E weakening of the closed R witness.

## Local qualification

The precise local result uses `ContextualWeakInduction Γ`, which explicitly ranges over all well-formed extensions `Δ ++ Γ`. Only the three-hypothesis extension is needed in the reverse direction. In the forward direction, the local R witness is weakened through the finite telescope and the retained section theorem applies.

`endomorphism_rigid` also proves that `WeakInductionAt Γ` at a single fixed Γ forces rigidity of every endomorphism whose endomorphism and law witnesses are already available there. Packaging a general R witness in this proof requires applying induction beneath the generic hypotheses. No theorem here says that `WeakInductionAt []` is strictly weaker than the full schema, or that a converse from it is impossible. Such a separation would need a separate argument.

## Negative consequence and scope

The schema is nonadmissible because it would produce a closed literal R witness, contradicting the already retained `RigidityDiscriminator.rigidity_uninhabited`. This transfers existing negative evidence; it is not a new model, model validation, or independence construction. It neither internalizes the negation of the schema nor produces a source witness of `R → bottom`.

All raw syntax, types, typing constructors and structural rules are retained. No new constructor, axiom, UIP, equality reflection, Sigma eta, computation law, or universe is added. No theorem identifies a propositional successor identity with unrestricted raw successor conversion. There is no protected edit, baseline rebuild, integration, merge, T21 claim or programme closure.

## Reproduction

Run `bash hase-induction-rigidity-converse-20261010/check.sh` from the workspace root. It compiles only the one new module with the retained Lean 4.19.0 binary and `--trust=0`, reusing retained compiled dependencies. `validation/build.log` records the successful replay and printed axiom dependencies: standard Lean `propext`, `Quot.sound`, and (for inherited forward/model infrastructure) `Classical.choice`; no `sorryAx` or new axiom.

The positive converse and local endomorphism theorem need only `propext` and `Quot.sound`. The negative corollaries deliberately depend on the inherited discriminator. `validation/SOURCE_HASHES.json` pins this packet and directly reused source inputs. Independent review, if performed, is separate.
