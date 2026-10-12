# Full actual-E Sigma elimination is exactly propositional Sigma eta

## Central result

The retained original-Has premise restriction concealed no additional source principle. After the checked actual-E structural admissibility results, dependent Sigma elimination remains exactly equivalent to propositional Sigma eta. This is a conditional completion equivalence for the unchanged calculus, not a proof that either completion schema is derivable.

`SigmaCompletion.FullE.eta_iff_elimination` and `eta_iff_weak_elimination` quantify over arbitrary actual `CtxE`, `FormE` and `HasE` premises. The sharper `eta_iff_elimination_at` and `eta_iff_weak_elimination_at` establish the same equivalence at each fixed admissible input. No restriction to original-source contexts, families, branches or inputs remains.

## Exact premises and conclusions

Fix any telescope Γ, types A and B, and polynomial z with:

- `CtxE Γ`;
- `FormE Γ A`;
- `FormE (A :: Γ) B`;
- `HasE Γ z (sigma A B)`.

Write S for `sigma A B`. Then the following three statements are equivalent:

1. There exists an actual proof polynomial e with `HasE Γ e (identity S z (reconstruct z))`.
2. For every P and d with `FormE (S :: Γ) P` and `HasE (B :: A :: Γ) d (branchType P)`, there exists t with `HasE Γ t (inst P z)`.
3. For every P and d with exactly those same premises, there exists t with `HasE Γ t (inst P z)` and raw `P01DF.PolyConv t (branchAt d (fstPoly z) (sndPoly z))`.

Statement 2 is the weak schema. Statement 3 is the strong schema, with the everywhere-erasure clause inherited from the actual J implementation. No eta evidence is a premise of either elimination schema. Formation and typing premises are explicit; neither schema is defined as exclusivity, initiality, or eta under another name. The uniform schemas universally quantify over the four fixed-input premises as well.

These are metatheoretic rule schemas. There is no added universe, internal quantifier over all families, adopted axiom, new constructor, source-level internal equivalence type, or claim that one closed polynomial selects every existential eta witness. The explicit construction is uniform once a particular e is supplied.

## Literal construction and converse

Every polynomial and type expression is imported directly from the retained `SigmaCompletion` namespace: `reconstruct`, `pairSub`, `branchType`, `branchAt`, `elim` and `etaMotive`. No replacement definitions occur in the central module.

Forward: the actual projections of z type its reconstruction. The freshly proved actual-E dependent substitution theorem types the branch at that reconstructed pair. The already checked full-E J helper reverses the supplied identity and transports this branch from P(reconstruct z) to P(z). The resulting term is literally the old `SigmaCompletion.elim d z e`.

Converse: use the genuine dependent motive `Id_(wk S)(var 0,reconstruct(var 0))`. The file proves its actual-E formation, the generic pair's correct twice-weakened dependent typing, and its canonical branch using only raw projection beta. Applying weak elimination gives precisely the desired eta identity. The converse does not assume eta, raw pair eta, a computation clause, UIP, or identity reflection.

The actual-E dependent-term substitution packet directly discharges the branch step. The prior full-E J helper is reused from the reviewed `FullEInitiality` module. Its chain includes the mixed/type-parameter substitution packet; no new mixed-substitution principle is assumed here. This proof closes a missing source interface rather than adding a semantic law.

## Raw computation versus typed identity

The retained `elim_erases` and `elim_pair_computation` apply unchanged to the literal term. At every raw canonical pair, for arbitrary d, a, b and e:

`PolyConv (elim d (pairPoly a b) e) (branchAt d a b)`.

This raw theorem is axiom-free and independent of typing or equality between proof arguments. The new `elim_pair_identity` separately checks all actual-E formations and endpoint typings before constructing typed propositional computation. Its premises include the explicit eta witness used by that particular eliminator instance. No typed identity is reflected into raw conversion, and no equality of the proofs themselves is asserted.

## Proved scope expansion

`FullESigmaScopeControls.lean` uses the retained Church witness at `E = Id_N(I,SKK)` and `D = Id_E(I,I)`. It proves:

- `CtxE [D]`, but not original `Ctx [D]`;
- the motive `wk D` is actually formed over the original well-formed context `[SigmaRaw]`, but has no original Form derivation;
- a branch at that motive has actual HasE typing in the original well-formed telescope `[Raw,Raw]`, while no original-Has polynomial inhabits that branch type;
- the closed pair `pair I I` has actual HasE type `Sigma E Raw`, while no original-Has polynomial inhabits that Sigma type.

These exclusions are positive kernel-checked proofs. They are not inferred from failed elaboration or constructor provenance. The motive/branch and closed-input tests are independent of the context test, so their separation is not merely rejection of an ill-formed original context.

`combined_elimination` exercises the complete new interface in `[D]` with the actual-E input, motive and branch and a directly constructed canonical eta witness. `combined_raw_beta` checks the retained computation. These canonical-pair/constant-motive examples are explicitly scope tests. They do not show that eta is necessary for those easy instances. Necessity for elimination over all motives is established by the general converse, and failure of the uniform schema by the retained model below.

## The inherited boundary under R still applies

`FullESigmaBoundary.lean` reuses `SigmaTagBoundary.no_eta_under_rigidity` directly. That result was already sound for the actual full FormE/HasE grammar, including all extensionality constructors, so no new model or redundant soundness proof is needed.

The new file verifies the actual context Γ = `[SigmaRaw,R]`, its Sigma variable z = var 0, and the available proof var 1 of the literal Rigidity R. At this very input, the retained theorem excludes eta; the new pointwise equivalence therefore excludes both weak and strong dependent elimination over all formed motives and typed branches. Consequently neither unrestricted full-E schema is presently available.

`inherited_eta_relative_independence` is explicitly only an alias of the existing two-sided source nonderivability statement: neither `R → Eta` nor `R → (Eta → Bottom)` has an actual HasE closed proof. The componentwise model side and tagged-model side receive no new credit here. This statement about the retained object-language Eta type is not silently identified with an internal encoding of the external schemas.

## Verification, ancestry and limits

Run `python3 hase-full-e-sigma-elimination-20261010/verify.py` or the narrow `check.sh`. The three additive modules compile with installed Lean 4.19.0, `--trust=0`. Existing retained objects are reused; the baseline is not rebuilt and protected inputs are not edited. The author replay verifies recorded source and retained-object hashes before and after compilation.

The central constructive theorems use only standard Lean `propext` and `Quot.sound`. The separately identified inherited discriminator and model controls also use `Classical.choice`. The raw computation control has no axioms. No `sorryAx`, new axiom, new source rule, semantic reflection, UIP, raw identity collapse or unrelated uninhabited-target claim is used.

The exact constructive ancestry is the original-source Sigma completion proof, the actual-E dependent substitution/weakening lemmas, and the already reviewed actual-E J transport. This is a new full-E central conditional interface, not new raw computation, a new model, a proof-cost estimate, or merely an adapter lemma. It establishes neither eta itself, premise-free unrestricted Sigma elimination, full relational parametricity, nor overall T20/programme closure. Independent review is separate.
