# P15: Relative normative-gap disclosure with an exact continuous-weight checker

**Status:** completed scoped research return; formal disclosure application; mixed accepted, repaired and rejected bridges. All IO identifiers here are handoff-local work units. The mathematical arguments are ordinary proofs, with exact finite Python checks. There is no new Lean/kernel credit, canonical adoption, empirical validation, publication claim or global novelty claim.

## Result first

The useful result is stronger than recording two arbitrary normative valuations. A declared, Pareto-respecting class of positive two-criterion trade-offs admits an **exact continuous-domain disclosure procedure**: partition its rational weight interval at the zeroes of the affine comparisons appearing in a Boolean target. Evaluate each boundary and each open interval. This completely decides relative invariance, including strict preferences, ties, narrow interior regions and Boolean combinations. Endpoints alone are insufficient.

The philosophical conclusion remains conditional: an invariant judgment follows from the declared extraction, orientation, admissibility regime and evaluation semantics. A disagreement witnesses failure of determination within that regime. Neither result certifies that the regime captures every substantively admissible bridge, or that an encoded judgment has normative authority. The concrete advance is auditable dependence with an exact decision procedure, not a new universal is–ought theorem.

A second positive bridge connects finite dynamics to optimality: strict ascent outside the maximizing set plus closure of that set guarantees entry and persistence; pointwise fixation of maxima additionally gives equality of fixed points and maxima. These conditions are inspectable and stronger than bare stability.

## 0. Dependency and source identity

The supplied P15 packet and its bundled P14 packet are input/preparation artifacts. Their receipts say `SEALED_HANDOFF_ONLY`, with research not executed. We did not treat those as results. The new P14 completed return was separately read back, all 15 manifest-bound files checked, its seven unit tests rerun, and its negative results retained. The exact intake is `P14_INTAKE.json`; the final predecessor interface is copied byte-for-byte as `P14_INTERFACE.json`.

The predecessor archive SHA-256 is `437be32e1d2a909e353abd376f36bf99968c6679f1ccbcb401301aa48f8a4d37`. Both research returns are based on repository commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`. Source-byte bindings and input identities are in `SOURCE_BINDINGS.json`.

P14 repairs that constrain this return include:

- Injectivity, order preservation, order reflection and task sufficiency are different. A scalar can be sufficient for the task.
- The PDF §7.1 nonzero nonnegative cone excludes weak-all/strict-some gains; §7.2 every-coordinate-strict prose describes a different relation. We use named relations, not an ambiguous “Pareto” label.
- Finite mixed Nash needs its usual hypotheses. Finite response alphabets do not imply finite policy spaces over unlimited time.
- Positive-weight support of a vector-efficient equilibrium is an existence claim under the finite-polyhedral conditions; it does not choose canonical or authoritative weights.
- Nonlinear increasing transformations of pure payoffs can change mixed equilibria. Marginals do not determine joint or temporal law.

## 1. Typed enrichment and nontrivial admissibility (IO01)

Let `L_D` be a many-sorted base signature. It may describe alternatives A, criteria C, raw measurements, source provenance, consequence maps and physically feasible actions. Let `L_E` add orientation, evaluation, comparison and choice relations. An expansion N interprets `L_D ∪ L_E`; its reduct `red(N)` forgets the added symbols. Equality of reducts means the same carriers and interpretations, not merely observational similarity. An isomorphism-based variant must explicitly transport named alternatives and the target.

An admissibility regime B is a specified predicate on expansions, possibly parameterized by D. Define:

`Ext_B(D) = {N : red(N)=D and B(D,N)}`.

For a sentence φ in the expanded signature, write `D |=_B φ` precisely when every N in `Ext_B(D)` satisfies φ. Writing `D |= φ` for a formula whose symbols D does not interpret would be ill-typed.

**Partition guard.** A recorded number and its interpretation are different. Counting citations may be descriptive; treating the count as provenance quality or justificatory strength uses calibration and evaluation. Coordinate orientation (“higher is better”), selection of criteria and assessment of defeaters can already be normative or mixed before any scalar weights are chosen. This return therefore allows a typed *application base* containing disclosed mixed assumptions. Such a base supports relative model disclosure but cannot support the special claim that purely descriptive premises underdetermine a normative conclusion. The checker verifies declarations and required disclosure fields; it cannot certify that an author correctly classified a predicate as descriptive.

**Concrete class.** Fix two calibrated profiles e(a) in Q², signed orientations o_j in {−1,+1}, and rational endpoints 0<l≤u<1. An admissible expansion has parameter α in [l,u] and score

`s_α(a)=α o_1 e_1(a)+(1−α)o_2 e_2(a)`.

Its weak and strict preference relations are induced by ≥ and >. The class excludes negative priorities, incompleteness of the induced weak order, inconsistent comparison assignments and departures from the declared linear aggregation. Positive weights preserve every weak-all/strict-some improvement of the oriented profile. The interval restriction represents an independently supplied bounded-priority policy. Positivity is motivated by valuing each declared criterion; particular bounds require their own policy justification. Neither linearity nor [1/4,3/4] is proclaimed substantively correct by mathematics.

This is a restricted, testable class rather than all possible valuations. It is nevertheless only a conditional model of admissibility. A sound theory may justify nonlinear evaluation, lexicographic priority, a singleton bridge, or rejection of the chosen criteria. Such a theory changes B and requires a fresh certificate.

## 2. Relative determination theorem and edge cases (IO02)

**Theorem IO02-A.** If N₁,N₂ belong to `Ext_B(D)`, N₁ satisfies φ and N₂ satisfies ¬φ, then neither `D |=_B φ` nor `D |=_B ¬φ` holds.

**Proof.** N₂ refutes the first universal statement; N₁ refutes the second. Under classical bivalent satisfaction, the converse also holds: failure of each universal supplies one of the witnesses. This converse presupposes the entire designated class and ordinary classical semantics; it is not licensed by failure to find a proof or by an incomplete sample. ∎

There are four materially different cases:

1. Empty extension class: universal entailment is vacuously true in both directions, but the operational result is `NO_ADMISSIBLE_EXTENSION`. This says the selected regime has no model over D. It need not mean the world or D alone is inconsistent.
2. Singleton class: every closed target is determined, but authority does not follow from having stipulated one expansion.
3. Multiple expansions agreeing on φ: target determination without complete enrichment uniqueness. Dominating profiles are a positive example.
4. Multiple expansions disagreeing on φ: relative underdetermination, with explicit witnesses.

For (1,0) and (0,1), α=1/4 and 3/4 disagree on strict preference. For (2,2) and (1,1), every allowed α prefers the former. The singleton α=1/2 ties the crossing profiles and falsifies strict preference. A formula φ∨¬φ is invariant even when φ varies. Merely containing normative vocabulary therefore cannot be an adequate formal criterion for an is–ought prohibition.

A new independent bridge may remove the disagreement. If B′ implies B, then `Ext_B′(D)⊆Ext_B(D)`: positive entailments are preserved under nonempty restriction, while underdetermination need not be. An empty restriction must still be reported separately. Proving that a proposed restriction is justified is a substantive step, not something settled by the inclusion relation.

## 3. Ranking reversal and scalar positive controls (IO03)

For an oriented difference d=e(x)−e(y), the score difference is

`f(α)=d₂+α(d₁−d₂)`.

On a closed interval its extrema occur at endpoints. Two **opposite strict rankings** are possible exactly when `min(f(l),f(u))<0<max(f(l),f(u))`. Variation in the Boolean target “x strictly outranks y” instead needs `min≤0<max`: a tie and a strict preference already disagree on that target, without reversing the strict ranking. The distinction matters at interval boundaries.

P14 ET01-C proves that unrestricted strictly positive weights in any finite dimension yield both strict signs exactly when d has positive and negative coordinates. Restrictions can defeat reversal despite crossing: d=(1,−1), α in [3/4,7/8], always favors x. Positive dominance can never reverse in this class.

P14 ET01-A also supplies the exact order result: an order-preserving-and-reflecting map from a partial order to a total order requires the source order to be total. For any source pair, totality compares their images, and reflection compares the source pair. For finite chains, assigning increasing real ranks supplies the converse. This concerns faithful order embedding. An injective scalar encoding of a finite non-chain can still preserve all identities; it simply supplies comparisons absent from the original partial order. A noninjective scalar may still preserve a particular decision target if that target is constant on its fibres.

**Source-reliability positive control.** Under a fixed binary hypothesis model with positive likelihoods, the likelihood ratio λ(x)=P(x|H₁)/P(x|H₀) determines the posterior at any supplied prior π:

`P(H₁|x)=πλ(x)/(πλ(x)+1−π)`.

Consequently it preserves every decision determined solely by that posterior, supplied losses and a supplied tie rule. It need not embed a multidimensional evidence-quality order. With independent root reports of reliability .9, one report for H and one against H have λ=9·(1/9)=1. Duplicating the first report by copying changes no evidence; counting the copy as independent instead gives λ=9 and posterior .9 at prior .5, rather than .5. When the copy mechanism is known, the naive model violates the fixed descriptive model and is not an admissible normative alternative. When the mechanism is unknown, the disagreement may be model uncertainty rather than normative uncertainty. The two uncertainty axes must be recorded separately.

## 4. Evaluation in games and dynamics (IO04–IO05)

A game skeleton specifies players, feasible strategy sets and consequences. Evaluation may be supplied by scalar utility, a vector improvement relation, a common team objective, or a constraint-based admissibility relation. These objects have different types. A hard exclusion removes moves from the feasible set; assigning a low utility leaves them feasible. Treating an exclusion as genuinely normative belongs in the enrichment or in a disclosed mixed base.

A concrete fixed skeleton has two players, each choosing 0 or 1. Its consequence profile for a player's own choice is (1,0) at 0 and (0,1) at 1. Both use the positive α score. For α>1/2, (0,0) is the unique Nash equilibrium; for α<1/2, (1,1) is unique; at α=1/2 every mixed profile is Nash. The physical choices and consequence map are identical. The comparison bridge changes. This establishes dependence on evaluation, not that evaluation must be arbitrary or nonnatural.

For dynamics, let X be a nonempty finite set, G:X→X a deterministic transition and W:X→R an independently supplied evaluation. Let M=argmax W.

**Deletion countermodels.** On X={0,1}, W(0)=0,W(1)=1 and G constantly 0 give Fix(G)={0}, disjoint from M. The identity transition has Fix(G)=X, which contains a nonmaximum. A flip has no fixed point. On X={0,1,2}, W=(1,0,0), G=(0,2,1), Fix(G)=M={0}, yet the other two states cycle forever: equality of fixed points and optima does not itself give convergence.

**Theorem IO05-A.** Assume (a) W(Gx)>W(x) for every x outside M, and (b) G(M)⊆M. Then every trajectory enters M in at most |X\M| transitions and remains there. If additionally Gm=m for every m in M, then Fix(G)=M.

**Proof.** A pre-entry trajectory cannot repeat a state because W strictly increases on each pre-entry step. There are only |X\M| such states. Closure supplies persistence. A nonmaximum cannot be fixed under strict ascent, and pointwise fixation supplies the reverse inclusion. ∎

These premises are independently checkable relative to W and G. They do not define G to be correct, but they make the evaluation-sensitive progress condition explicit. Replacing strict by weak ascent permits a nonmaximal fixed point. Dropping closure allows exit from a maximum. Dropping pointwise fixation permits cycles within M while preserving target satisfaction. Neither the theorem nor Nash stability implies empirical truth or the substantive correctness of W.

P14's common-interest positive result remains available: a global team optimum is Nash; the converse needs more. Its ET05-C shows that, for a finite common-payoff game extended to the full product of independent mixed simplices, joint concavity is equivalent to additive separability of that scalar payoff. Thus this convenient sufficient condition removes payoff interaction; own-mixture concavity, which is automatic, does not suffice. This is about payoff structure, not the absence of all architectural or causal interaction.

## 5. Canonical enrichment made precise (IO06)

The reduct is an ordinary map from admissible enriched structures to base structures. Its fibre over D is the set already defined. A section would choose one member of each nonempty fibre. No category language is needed for these claims.

Four criteria differ: unique extension, unique target value, a choice invariant under the automorphisms of D, and explicit definability in a chosen language. Invariance under automorphisms is necessary for parameter-free definability, but we do not use it as a sufficient criterion in arbitrary structures.

Consider two alternatives a,b and two otherwise indistinguishable criteria 1,2, with profiles (1,0),(0,1). Here a,b and 1,2 are metalanguage labels, not distinguished constants fixed by the base signature; this symmetry example uses the swap-closed bridge interval [1/4,3/4]. The base has a simultaneous swap of alternatives and criteria. Any equivariant single-alternative selector at this base must be fixed by that swap, but neither a nor b is fixed. Such a selector does not exist. However, uniform weights (1/2,1/2) are fixed, yield a canonical weak ordering with a tie, and the selected set {a,b} is invariant. Therefore the obstruction is to a symmetry-respecting **single winner**, not to every canonical enrichment. Label-based tie breaking adds structure that destroys the relevant symmetry.

More generally, a normalized weight vector invariant under every permutation of m indistinguishable criteria has all coordinates equal, hence w_j=1/m. This is a mathematical uniqueness result under the symmetry assumption. It does not prove criteria are substantively exchangeable or equal importance is correct.

The nearby model-theoretic result is Beth definability: implicit determination across all models of a first-order theory entails explicit definability in that setting. Uniqueness over just one fixed D is weaker. Buss's author-hosted account explicitly warns using a standard-model arithmetic example that uniqueness there need not extend to nonstandard models. We claim neither a new definability theorem nor a converse from this finite application's certificate to global metaphysical supervenience. [Buss, §2.5.6](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/handbookI/ChapterI.pdf)

## 6. Exact checker and its proof (IO07)

The accepted target grammar consists of strict/weak pairwise score comparisons, Boolean constants, negation and finite conjunction/disjunction. Each comparison is an affine expression aα+b tested against zero. For rational profiles and orientations the coefficients and roots are rational.

**Theorem IO07-A (sign-cell completeness).** Let R contain the interval endpoints and every root −b/a lying in the interval for nonzero a. Evaluate the target at each distinct point of R and at one rational midpoint of each adjacent open interval. These finitely many values are exactly the truth values realized throughout [l,u].

**Proof.** An affine expression with nonzero slope has no zero and a constant strict sign within an open interval between successive roots. A constant expression has constant sign everywhere. Thus every atomic comparison, and by induction every Boolean formula of them, has constant truth value on each open cell. Roots are evaluated individually, so equality and strictness are preserved. The points and open cells cover the whole interval. Their representatives belong to their cells. ∎

There are at most 2k+3 representatives for k atomic occurrences, and fewer after root deduplication. This is continuous-domain completeness, not dense-grid approximation. A conjunction 0.49<α<0.51 inside [0.25,0.75] is false at both endpoints and true in an interior cell. The prototype catches it. Checking only original endpoints would falsely certify invariance.

`gap_disclosure.py` is a bounded research prototype, not a deployment-ready external-data parser. It uses exact fractions, a closed AST, field whitelists, input and syntax bounds, and recomputation of certificate content. Its statuses are `INVALID`, `NO_ADMISSIBLE_EXTENSION`, `DISAGREEMENT`, `INVARIANT_TRUE`, and `INVARIANT_FALSE`. A disagreement certificate records rational true and false witnesses. An invariant certificate records coverage count and rule identity; a verifier recomputes the complete partition rather than trusting the asserted count.

The certificate binds canonical-JSON hashes of base, regime and target, bridge schema/version, declared signature partition, assumption records and scope. It rejects stale bases, invented authority status, unsupported target operations and altered certificates. Hashes provide content binding, not author authentication or substantive evidence. The literal `SUPPLIED_NOT_CERTIFIED` applies to normative authority. The field `base_declared_purely_descriptive` summarizes declared kinds only; `partition_check` expressly prevents treating it as semantic certification. See `CERTIFICATE_SPEC.md` for the complete boundary.

Test-first development was recorded: 14 failing tests before implementation, then all 14 passing. A subsequent type-coercion review added two tests, exposed and fixed a Boolean/integer certificate-equality flaw, and all 16 passed. An independent mathematical review then prompted a safer declared-kind field name and a bounded regime ID; the final 17 tests passed. An independent exact linear-inequality feasibility oracle matched 35,000 atomic and 7,500 conjunction cases. Exact dynamics probes checked 21,504 map/evaluation pairs; 2,607 satisfied the ascent/closure conditions, with 10,209 trajectory-bound checks and 333 fixed-max cases. Twenty-five certificate mutations were rejected. These checks support implementation correctness within their finite ranges; the general proofs above carry the universal claims.

## 7. Domain instances and recoverability (IO08)

**Theorem IO08-A.** Given specified sets E,D,T, a projection π:E→D and target τ:E→T, there exists f on im(π) with τ=f∘π exactly when τ is constant on every π-fibre. Proof: a factorization forces equal target values on a common fibre; conversely define f(d) as its unique target value. Extending f outside im(π) needs a separate nonempty-target/default guard. This is standard factorization, already present in Orthemology's observation/refinement ancestry, not a novel discovery.

Its nontrivial application requires exact π, admissibility and τ:

| Example | Typed objects and class | Classification |
|---|---|---|
| Recorded profiles → permitted ranking | E=(D,α) under the declared positive interval; π forgets α; τ is a target preference formula | EXACT_INSTANCE, computed here |
| Feasible game skeleton → equilibrium set | E adds declared evaluations and comparison semantics; τ returns its equilibrium set | EXACT_INSTANCE for the finite example in §4 |
| Data → classifier label | E adds specified model family/thresholds; τ is prediction; class needs independent training/constraint rationale | CONDITIONAL_INSTANCE, usually predictive/model uncertainty rather than a moral gap |
| Observation → hidden source provenance | E contains acquisition graphs consistent with an explicitly fixed observation map; τ is root identity/independence | CONDITIONAL_INSTANCE; known copying must eliminate the false independent model |
| Likelihoods → posterior-based decision | E includes model, prior, loss and tie rule; τ is decision; λ is the proposed observation | EXACT_INSTANCE of positive target sufficiency for fixed model/prior/loss |
| World facts → moral rightness globally | No complete justified metaphysical class is supplied here | ANALOGY_ONLY; no global anti-naturalism or supervenience result |
| Ultimate ground → original intentional subject | Needs ontological/constitutive hosting premises, not the weight interval or data projection | NON_EQUIVALENT to this application theorem |
| Explicit provenance → normative authority | A certificate records supplied premises but has no rule deriving substantive authority | NON_EQUIVALENT; promotion rejected |

The same underlying reduct can have three very different intended classes: syntactically permitted structures, epistemically live models, and metaphysically possible structures. The theorem is valid over each specified class, but a witness in the first is not automatically a witness in the third. This is especially important for the impersonal R5 rival: formal predicate variation alone does not establish a metaphysically adequate alternative.

## 8. Prior-art and philosophical scope (IO09)

Hume asks that the transition to ought-relations be noticed and explained, including the purported deduction from importantly different premises. Our tool makes a supplied bridge and its consequence dependence visible; it does not adjudicate every interpretation of his thesis. [Treatise 3.1.1.27](https://davidhume.org/texts/t/3/1/1)

Prior challenges unrestricted formulations of ethical autonomy. In classical logic p entails p∨O even if O is an ethical sentence, and tautologies can contain ethical vocabulary. Consequently a syntactic new-word test cannot establish the desired prohibition. Our theorem uses actual semantic disagreement in a specified class, rather than a ban on ethical vocabulary in conclusions. [Prior, “The Autonomy of Ethics”](https://fitelson.org/piksi/piksi_22/prior_autonomy_of_ethics.pdf)

Moore's discussion concerns the analysis or identification of goodness and the open question, rather than this particular extension-fibre theorem. We do not infer the indefinability of good from varying α, or treat every naturalistic identification as already refuted. [Principia Ethica §§10–13](https://www.gutenberg.org/cache/epub/53430/pg53430-images.html)

Naturalist theories can propose constraints that uniquely determine evaluative interpretation. Jackson and Pettit's moral functionalism is a relevant positive rival, rather than a view eliminated by constructing a more permissive B. Their publication page and authored abstract identify the reductionist dispute; this return does not claim a full adjudication of their paper. [Author-hosted publication](https://ppettit.scholar.princeton.edu/publications/moral-functionalism-supervenience-and-reductionism), [authored abstract](https://philpapers.org/rec/JACMFS)

Metaphysical supervenience, logical definability, epistemic access and an executable decision rule are separate claims. A unique target within a supplied class need not supply a procedure; a procedure here works because the grammar and arithmetic are tightly restricted. Preference representation likewise represents an already constrained comparison structure. Representation alone does not warrant that ordering's normative correctness. P14's Nash, scalarization and transformation results supply the exact relevant mathematical controls.

**Strongest defensible contribution:** a typed, revision-bound formal disclosure application with exact continuous-weight invariance checking, useful positive controls, and a finite ascent-to-optimality bridge. **Rejected:** a new universal proof of Hume, an anti-naturalist theorem, global non-supervenience, universal scalar loss, automatic equilibrium correctness, or machine-certified normative authority. Global novelty positioning remains P09/U13 work.

## 9. Implementation disposition (IO10)

`IMPLEMENTATION_HANDOFF.md` gives proposed isolated module names, theorem statements, fixtures, schema and verifier contracts, source pins, negative controls and rollback boundaries. The present artifacts are research-only; authorizing or merging them into canonical Orthemology is a later owner decision. A higher-dimensional rational-polytope extension is a separate next research question, not silently covered by the interval checker.
