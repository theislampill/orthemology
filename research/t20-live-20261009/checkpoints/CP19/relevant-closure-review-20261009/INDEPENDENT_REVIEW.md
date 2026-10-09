# Independent review: relevant implication and knowledge closure

Date: 2026-10-09. Scope: substantive source/formal review only; no integration or closure authority.

## Verdict

**Accept the positive relevant-implication derivation, with its present epistemic limits. Do not promote the matrix to a refutation of KnowledgeClosure.** The published argument has a genuine factive-basing mechanism. Its implication-to-counterfactual bridge is also explicitly acknowledged in the earlier closure paper. What remains is a conditional-typing/scope question if “implies” is read as unrestricted classical consequence; the present controls do not decide the strongest full-inference version of that question.

## 1. Strongest source reading

Adams, Barker and Clarke (2017), “Knowledge via Closure,” does not try to transfer the sensitivity of Jimmy’s original visual experience directly to the conclusion. Correct inference makes his premise belief operative; because that belief is knowledge, EpistemicBasing makes the fact that the animal is a zebra a ground of the conclusion. The zoological incompatibility then supports the relevant counterfactual: were the conclusion false, that fact would not obtain. His inability to distinguish visually a zebra from a zonkey does not defeat their generic-knowledge claim. Omitting the known premise, correct inference, or factive ground would miss this argument.

The 2017 necessary-truth discussion explicitly rejects Thesis B, the automatic passage from a necessary truth to arbitrary counterfactual consequences of its negation. Its arithmetic example separately specifies reliable testimony and an intellectual experience sensitive to the mathematical result. Reproducing nonvacuity is therefore a control on the authors’ intended logic, not a new epistemological objection. Notes 26–28 point to antecedent/background-law accounts and relevant matrices; they do not themselves select a full counterfactual model. Note 32 expressly credits contraposition to implicative conditionals. Note 13 allows conjunctive/intermediate-conclusion resources; note 19 warns against automatically inheriting all reasons for premises.

A targeted check of the source cited for closure strengthens the authors’ case. Barker and Adams (2010), p.222 n.1, explicitly requires same-time competent immediate inference. Its p.225 n.12 permits combined grounds, while excluding knowledge of a ground that presupposes the target. Most importantly, p.228 n.21 explicitly assumes the bridge from obtaining p plus the implication claim to the counterfactual absence of p under not-q; n.22 connects this with an entailment-based factive-ground argument. The bridge is therefore **acknowledged**, not wholly missing from their closure literature. The 2010 paper treats its subjunctive as primitive (p.225 n.13); it does not settle whether every classical consequence licenses that bridge.

Sources: [ABC2017](https://doi.org/10.1590/0100-6045.2017.V40N4.FA), retained lines 122–150, 208–224 and notes 13, 19, 26–28, 32; [BA2010, official journal PDF](https://logos-and-episteme.acadiasi.ro/wp-content/uploads/2015/02/EPISTEMIC-CLOSURE-AND-SKEPTICISM.pdf), printed pp.222, 225, 227–228.

## 2. Three readings that must remain separate

1. **Relevant implication p →R q.** The p-only published route is straightforward: the known implication is true; contraposition supplies ¬q →R ¬p; the known, operative fact p is sensitive. Alternatively, the complete relevant-premise ground B = p ∧ (p →R q) satisfies B →R q and ¬q →R ¬B. This is a genuine positive result, conditional on the specified facts being known and actually used.
2. **A materially true conditional p ⊃ q = ¬p ∨ q.** Actual truth of p and p ⊃ q does not, by itself, turn p into a sensitive ground for q. The checked p=2, q=1 valuation separates these claims. It does not interpret knowledge or inference, and it omits the possible contribution of the other operative premise when testing the p-only ground.
3. **Classical entailment p ⊨CL q.** This is stronger than the accidental truth of a material conditional and should not be conflated with it. The authors’ ordinary “implies” may naturally denote entailment. If it includes every classical entailment to an independent necessary target, the p-only counterfactual bridge needs defense beyond System R’s contraposition. Their earlier paper openly presupposes the bridge. That is a legitimate place to locate a scope question, rather than silently assigning them the weaker material reading.

For a necessary target N, the valid relevant proof requires no special appeal to necessity. Its work is done by the relevant implication and operative factive premises. A proper mathematical derivation could supply the required connection; mere necessity cannot automatically replace it.

## 3. Independent formal check

I reviewed the author’s 19-line derivation of

¬N →R ¬[P ∧ (P →R N)].

The axiom list matches the primary R presentation in Bimbó, Dunn and Ferenz (2018), printed pp.176–177. An independent matcher checked every axiom instance without relying on the author’s stored substitution certificate, and separately checked every modus-ponens dependency. All 19 lines pass. The argument uses conjunction projections, composition, exchange, contraction, double-negation introduction and contraposition; no material arrow is substituted.

An independently tabulated evaluator also verified all 4,096 axiom assignments and both designation-preserving rules for D={−2,−1,1,2}, with designated positive values. This establishes a sound finite control for the stated propositional axiomatization, not a completeness theorem or a model of cognition. No value and its negation are simultaneously designated.

**Decisive steelman control:** let Bmat = P ∧ (¬P ∨ N). In this matrix Bmat →R N and its contraposition pass not only for every identity target N=(Q →R Q), but for every positive N. Thus the p=2, N=1 valuation does not refute the full compound material-premise route. The general Bmat →R q schema does have failures, but each has q=−2 and an undesignated Bmat. Those failures establish non-theoremhood of that unrestricted formula; they are not instances of factive known-premise closure failing.

## 4. Claim ceilings and disposition

- Positive result: a checked relevant factive-premise transmission theorem, compatible with the authors’ strongest closure mechanism.
- Source improvement: the implication-to-counterfactual bridge is expressly presupposed in BA2010 n.21.
- Bounded negative result: material truth, classical consequence and relevant implication cannot be silently interchanged in the p-only argument.
- Not established: failure of full classical KnowledgeClosure with all known operative grounds and competent inference preserved; failure of the arithmetic case; a new refutation based on necessary-truth nonvacuity.
- Remaining research, if wanted: formulate the full epistemic/counterfactual semantics and test the whole operative ground under an explicit classical-entailment bridge. A single sound algebra and free experience assignments cannot settle that issue.

Evidence: `review_checks.py`, `INDEPENDENT_CHECK_RESULTS.json`, and the retained BA2010 PDF/text in `research-intermediates/`. Author files were not edited. The checked author-script digest is recorded in the JSON.
