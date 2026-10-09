# Independent formal and replay review

Date: 9 October 2026 UTC.

## Result

The received companion's portable Python replay passes all 56 tests, reproduces its canonical result byte for byte, and leaves both its received ZIP and all 39 extracted files unchanged. The written mathematical arguments D1–D10 are valid at their stated predicate-level or finite-model scope. No contradictory mathematical result was found in the inspected code or proofs. This review does not establish the philosophical applications, authenticate the cited source passages, or give any Lean file new kernel credit.

The most consequential additional control concerns D7's application: output-determining information can arise from factive knowledge alone. Connectedness must be tested on the very same local-state specification used to obtain determination. An explicit XOR refinement below demonstrates why connectedness of coarse states cannot be combined with determination by enriched states.

## Received identity and execution

- ZIP: `Orthemology_T20_Independent_Deep_Dive_20261009(1).zip`
- Bytes: 112,204.
- SHA-256: `c16bb8a75b84e4f79119d49635190e51ba1e862ffe207f137f0201cae542ae19`.
- Extracted tree: 39 files, comprising 37 manifest payloads and the two manifest files.
- Manifest SHA-256: `f2e7b0835df4d30dbea7d95b8b469749012afaad5cafcf46af98c92d4a2afa0f`.
- Replay environment: Python 3.12.14.
- Replay exit status: 0.
- Tests: 56, all passing; fresh log reports 7.446 seconds.
- Entire replay elapsed time: 14.889 seconds.
- Canonical result SHA-256: `8326a6daa597391aca913b4578b326149161e4484d2c78e6fd4108043fde0df6`.

All seven Python source files, including the replay, packaging helper and three test files, were read before execution. Their executed paths use standard-library calculation, hashing, file operations, disposable temporary directories, and one subprocess running the included tests. No executable path used the network; no installation, Lean execution, external upload, or predecessor-archive replay was performed. The supplied archive-extraction utility was inspected but was not used to re-extract the received archive; its disposable negative-control tests did run. A separate read-only primary webpage check was made for the short conditional diagnostic below.

Replay output was written to the new directory `portable-replay/` within this review directory, outside the input tree. The command used `python3 -B`, and its test subprocess also disabled bytecode creation. Independent inventories, rather than only the package's self-report, confirm unchanged original bytes. Those inventories are in `BEFORE_RECEIPT.json`, `AFTER_REPLAY_RECEIPT.json`, and `FINAL_INPUT_INTEGRITY.json`.

## Mathematical assessment

### D1 and D2: common requisites and witnesses

The common-requisite proof is a direct pointwise disjunction elimination. Its conclusion depends on exhaustivity and both requisite implications holding over the same world scope. It cannot by itself decide which premise a proposed deletion world must surrender.

The three-world negative-witness control genuinely distinguishes worldwise existence from one uniform selected witness. Both stated repairs are sufficient, retaining the background premise that P implies R at every world. Negative witnesses implying not-P is not itself needed for the repaired common-requisite deduction. A separate reviewer-authored enumeration checks both repairs over all 4,096 three-world tables for P, R, N0 and N1; it finds no violations. This is additional finite corroboration of the direct proof, not its general proof basis.

Neither the control nor this review evaluates all premises of Harrop's paper. The companion's local diagnostic should remain local.

### D3 and D4: explanatory facts and padding

The mutual-singleton proof follows from NEC and antisymmetric parthood. The cross-membership application additionally needs the stated projection and full-to-partial bridges. The total-explainer atomhood proof additionally needs source-part closure. All these hypotheses carry mathematical work; none follows from the label "explanation."

The Boolean implementation represents precisely the displayed model: 15 nonempty subsets of four atoms, q=1 explaining all 32,767 nonempty pluralities, and a=2 and b=4 each additionally explaining the designated singleton e=8. Bit-set inclusion correctly implements the all-target transitivity quantifier. The fresh result has one total explainer, local explainers [1,2,4], and all stated finite axioms passing. Its 245,762 full-explanation/member checks also agree with 15 times 2^14 memberships for the total source, plus the two additional local explanations.

The no-padding corollary is valid and requires only preservation of total explanation under enlargement, which is weaker than a full all-target weakening schema. One precision point: the delivered `padded=True` control adds q∨a=3 as a total explainer; it does not implement the complete upward closure of E. A single such required consequence already suffices to expose the contradiction, so this is not a defect in the corollary.

A small independent control evaluates the full upward closure, using the model's two exhaustive target-behaviour classes: the designated singleton {e}, and every other nonempty plurality. It produces total explainers [1,3,5,7,9,11,13,15], 14 local explainers, and all 15 facts as partial explainers of all targets. Source weakening then holds, but total uniqueness and NEC fail. The same NEC witness survives: x=2 partially explains {1}; 1 is distinct from and not part of 2; yet 1 partially explains {2}. This check does not repeat a new exhaustive 32,767-plurality campaign.

An immediate strengthened written consequence is available. Suppose the same fact domain has a total explaining fact q, total-explainer uniqueness, source weakening, binary fusions, and the supplied atomhood theorem for q. For any fact a, form r=q∨a. Weakening makes r total; uniqueness gives r=q. Fusion gives Part(a,r), hence Part(a,q). Atomhood gives a=q. Thus these combined assumptions force the entire fact domain to be a singleton. A domain with at least two distinct facts cannot retain them all. This is a standard conditional consequence of the supplied lemmas, not a new metaphysical conclusion or a kernel-checked theorem.

### D5 and D6: probability

The Bayesian formula and interval endpoints are correct under the stated valid-probability and positive-denominator conditions. The two exact posteriors are 10/11 and 1/101. Choosing alpha=1 is an explicit upper-endpoint assumption, not an identity derived from Bayes. This review makes no new claim about the authors' source wording or about warranted empirical likelihoods.

The covariance proof is general: every mixture of iid Bernoulli coordinates has covariance Var(Theta), hence nonnegative. The finite exchangeable law concentrated equally on 01 and 10 has covariance -1/4 and cannot be such a mixture. This does not challenge the correctly scoped infinite exchangeability representation theorem. Coherence, exchangeability, extendibility, and causal interpretation remain distinct. The uniform-Beta formula is correctly the probability of one specified word, not the entire head-count event.

### D7: compatibility components

The written component-propagation theorem is correct, as is the m^k count of vertex label assignments for k components. The tests genuinely enumerate all 16 relations on two states per side with two and three output labels. Declared isolated states are included. Disconnectedness allows nonconstant vertex labels; if one instead asks for distinct output values attained on admissible pairs, there must be at least two edge-bearing components. Isolated states alone do not produce a second jointly realised output.

Connectedness is not established by calling two sources independent, and informational determination is not by itself complete productive adequacy. The XOR control in the next section isolates this latter mapping issue.

### D8, D9 and D10

D8's reflexive but nontransitive frame correctly has Kp at world 0 and not KKp there. It is not a counterexample to positive introspection with the stronger frame assumptions that imply it.

D9's written unmapped multisort interpretation correctly combines one atomic fact with two distinct attribute tokens. Its supplied Python function returns literal antecedent/conclusion flags; its existing test checks those flags, rather than deriving them from the displayed relations. This is a limitation of executable evidence strength, not a falsification of the elementary written counterinterpretation. The reviewer-authored control separately evaluates atomicity and distinct qualification from the finite domains and relations and confirms them.

D10's written distinction between necessity of a bearer and necessity of a particular determination/effect is valid. The delivered packet accurately labels this section written-only. No executed D10 test or complete theory of divine volition is added here.

## XOR control: factive information is not original production

Let worlds be all four pairs (a,b) in {0,1}² and let h=a XOR b. On raw states A=a and B=b, every pair is co-realised: the compatibility graph is K2,2 and connected. Neither raw state determines h, since fixing either coordinate leaves both h values possible.

Now enrich each local state with factive information about the outcome: A'=(a,h), B'=(b,h). Both enriched states determine h by projection. The co-realisation edges are:

- A'(0,0) with B'(0,0).
- A'(0,1) with B'(1,1).
- A'(1,1) with B'(0,1).
- A'(1,0) with B'(1,0).

The refined graph has four single-edge components, two for each value of h. Every edge and path preserves h. The construction assigns no productive relation or productive power to either agent. Calling the retained value "factive output knowledge" changes none of this elementary mathematics.

Generally, refining both endpoint states by a shared outcome h makes every co-realisation edge h-preserving, hence every component h-constant. This holds regardless of what, if anything, either bearer produces. The example is therefore a counterexample to transporting raw-state connectedness into the enriched-state signature while using enriched-state determination. It is not a counterexample to D7, a novel graph theorem, a proof of divine omniscience, or an authenticated plural-original metaphysical model.

The useful application question is exact: which state description carries the claimed complete original productive adequacy, and why does the defended independence premise imply connectedness for that same description? Knowledge of another source or a common effect is not automatically productive dependence.

## Short conditional control: necessary-truth padding

Harrop's requisite definition excludes tautological forward conditionals, while the displayed sufficient-condition PSR does not impose that same exclusion on the reverse conditional. Section 5.2 distinguishes intended models from unrestricted logical interpretations. These definitions were checked directly in the [original article](https://onlinelibrary.wiley.com/doi/10.1111/phib.12377), without undertaking a further whole-paper assessment.

Consider independent propositional atoms S,T, intended worlds (S,T)=(0,1),(1,1), and R=S∧T. Throughout the intended scope T is necessary, S and R are contingent, and S→R holds. Over unrestricted classical valuations S→R fails at (1,0), so it is not tautological. R→S is tautological and therefore necessary. The extra control evaluates these claims directly.

Thus, if the fact domain admits this conjunction as a fact distinct from S, R is a nontrivial requisite under the displayed forward criterion and also a sufficient condition. Generalising to every contingent S requires a suitable necessary T that S does not logically entail, conjunction admission, and sufficiently fine-grained fact identity. Mere compositionality does not itself establish conjunction closure. Necessary-equivalence quotienting, a stronger noncircularity/relevance condition, or a different logical-validity criterion can block the construction. In particular, choosing a nonlogical necessary T is insufficient if S already logically entails T.

This is a conditional thinness diagnostic, not a refutation of PSR or a productive explanation. It concerns conditionals and conjunctive facts. D4 concerns a separate full-explanation relation and mereological fusion; no padding rule is transferred between those calculi.

## Lean and inheritance boundary

`formal/BridgeDiagnostics.lean` was inspected as source only. Its thirteen theorem candidates correspond to selected displayed arguments. The D7 candidate is the full-Cartesian special case, not the general connected-component theorem. No compiler was invoked and no elaboration, imported-axiom readback, or kernel success is claimed. The probability results and D9 do not gain Lean verification from this file.

The seven inherited Lean identities are records supplied inside the companion. Their original files were not reopened or replayed in this review. Existing historical credit is neither revoked nor refreshed. No modification of the input, protected repository, predecessor campaign, or T20 closure status is implied by this review.

## Review artifacts

- `portable-replay/TESTS.log`: fresh 56-test execution.
- `portable-replay/DIAGNOSTIC_RESULTS.json`: exact canonical reproduction.
- `portable-replay/REPLAY_RECEIPT.json`: supplied replay receipt.
- `BEFORE_RECEIPT.json`, `AFTER_REPLAY_RECEIPT.json`, `FINAL_INPUT_INTEGRITY.json`: independent input inventories and verification.
- `independent_controls.py`, `INDEPENDENT_CONTROLS.json`: small additional controls described above, with no imports from the supplied companion.

These results support using the companion's completed mathematical work without restarting its five research fronts. Philosophical premise selection, source attribution, and original-bearer realisation remain separate questions.
