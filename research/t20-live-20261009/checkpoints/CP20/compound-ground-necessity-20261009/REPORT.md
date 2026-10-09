# Full material grounds and necessary targets in System R

9 October 2026 UTC. One bounded discriminating operation within active T20. No protected repository edit, integration, packaging, upload, external contact, or programme closure.

## Result

**Combining a premise with its materially true conditional still does not, in System R alone, provide the relevant sensitivity required by the inspected knowledge account. This remains so when the target is an R theorem, both premises and their complete conjunction are designated, and their negations are undesignated.**

The prior four-valued control left precisely this case undecided. The source-tabulated eight-valued Belnap M0 matrix supplies a countervaluation. A separate syntactic reduction to R's variable-sharing property explains why the proposed necessary-target theorem cannot hold. This is a new local scope result, not a new discovery about relevant logic in general.

**It is not a counterexample to knowledge closure.** No subject's knowledge, competent inference, or actual basing is interpreted by this algebra. The source explicitly adds an implication-to-counterfactual bridge. An independently justified relevant implication still yields the positive factive-ground result already proved. What changes is that the full material conjunction and the target's theoremhood cannot themselves discharge that additional bridge.

**Consequence is not the failed relation.** Because N is already an R theorem, B ⊢R N holds, and B semantically entails N in M0. The negative result concerns the internal-arrow formula B →R N and the sensitivity formula ¬N →R ¬B. Both fail even as consequences of the designated material grounds in the exhibited matrix. Do not summarize this as “B does not entail N.” The distinction between deriving a conclusion and obtaining an internal conditional that supports counterfactual sensitivity is central to the result.

## 1. Exact question and actual predecessor comparison

The inherited `necessary-truth-operative-basing-20261009/REPORT.md` and `relevant-closure-review-20261009/INDEPENDENT_REVIEW.md` correctly distinguished three things:

1. A relevant conditional P →R N, whose use in the compound ground P ∧ (P →R N) supports a positive sensitivity theorem.
2. Material truth of ¬P ∨ N, which does not automatically give premise-only relevant sensitivity.
3. The stronger complete material ground B = P ∧ (¬P ∨ N), for which their selected four-valued matrix did **not** supply a counterexample when N was designated.

The predecessor author script, `check_relevant_bridge.py`, checks the identity target N = Q →R Q in all sixteen P,Q valuations of its matrix. Every full-ground implication and sensitivity passes. The independent review checks the broader positive-target restriction with the same outcome. Its failures for the unrestricted formula have an undesignated conclusion and ground. Those failures cannot answer the stronger present question.

The predecessor expressly says that success in one sound matrix is not an R theoremhood proof. Accordingly, there is no mistake in its stated verdict to retract. The present operation resolves its named logical residual:

> With N an R theorem, do the truth conditions of the full material ground suffice in R for B →R N or ¬N →R ¬B?

Answer: no. The test is performed on the full ground, not by omitting the second operative premise. It also avoids assigning a false or contradictory value to the identity target. No prior file inspected here contains this M0 application or the variable-sharing reduction. The absence claim is restricted to the named predecessor reports, scripts, and review, rather than every historical mathematical activity.

## 2. Primary control and logical interpretation

The actual primary technical source is Shawn Standefer, *Actual Issues for Relevant Logics*, Ergo 7(8), 2020, printed pp.270–271: [author PDF](https://shawn-standefer.github.io/pdfs/actual.pdf#page=30), [DOI](https://doi.org/10.3998/ergo.12405314.0007.008).

Those two complete pages, including the proof and footnote59, were read in extracted text and visually. Table2 and its Hasse diagram were visually checked on printed271. The table is explicitly credited to the Anderson–Belnap matrix argument. Standefer uses it to preserve variable sharing when adding specified actuality operators, and explicitly states soundness for R. This investigation uses only its propositional reduct. It neither reenacts the original 1960/1975 publication nor claims whole-paper reading.

For the exact R axioms, the already retained Bimbó, Dunn and Ferenz2018, printed176–177, was reread and compared with the predecessor's list. Its A1–A16 and R1–R2 are the formal contract. This is a source recheck, not new reading of a previously unexamined argument. The two printed pages define R and distinguish its fragments and optional truth/fusion extension. No optional truth constant, actuality operator, modal operator, or fusion connective occurs in the present target.

The M0 values are −3, −2, −1, −0, +0, +1, +2, +3; the four plus-labelled values are designated. Negation swaps the matching signed labels. Conjunction and disjunction are the meet and join of the displayed lattice, **not numeric minimum and maximum on the printed label order**. The checker represents this lattice by subsets of three atoms. Its implication table is transcribed from the primary page.

The mathematical term “designated” must be retained. No physical or cognitive interpretation of these values is claimed. The target N is an R theorem and is designated on every valuation; its negation is undesignated on every valuation in M0. This is a sharp logical necessary-target control without inventing a false mathematical metaphysical world.

## 3. The decisive full-ground countervaluation

Let P and Q be different propositional atoms, let N = Q →R Q, and let B = P ∧ (¬P ∨ N). Assign P = +1 and Q = +2.

The primary table and lattice then give:

- N = +2; ¬N = −2.
- P = +1; ¬P = −1.
- The material conditional ¬P ∨ N = +3.
- Its conjunction with P, namely B, equals +1.
- B →R N = −3.
- ¬N →R ¬B = −3.

Thus P, N, the material conditional, and B are all designated, while each of their negations is undesignated. Neither full-ground relevant implication nor full-ground relevant sensitivity is designated. The premise-only source bridge fails here too, but that is not the new discriminator.

At the metalevel, N remains derivable without assumptions and hence from B. It is also a semantic consequence of every premise set in M0. What fails semantically from the displayed designated grounds is the **formula** B →R N and, separately, the sensitivity formula. No unrestricted deduction theorem identifying those relations is available here.

The distinction from the previous countervaluation is exact: the old four-value matrix defeated the P-only shortcut but its material conjunction was sensitive for every designated N. Here the **complete** material conjunction fails despite theoremhood of N and noncontradictory designation of the actual ground. This rules out repairing that shortcut merely by conjoining the materially true conditional.

### Soundness and controls

`check_compound_ground.py` checks every assignment of each axiom's distinct schematic variables, totalling7,576 evaluations across the sixteen axioms. It checks all64 value pairs for designation preservation under modus ponens and under adjunction. There are no failures. Induction on derivations therefore yields soundness for the displayed finite matrix and exact R calculus.

This count is intentionally different from the predecessor's4,096: that checker uses all four variables even for axioms mentioning fewer; the present checker uses eight values and enumerates only variables occurring in each axiom. No larger count is itself extra philosophical evidence.

The script separately verifies the target's theorem/negation behavior under all eight Q values, every displayed countervaluation value, and closure of the two subalgebras used below. A deliberately changed identity entry is rejected by A1 at +0. A mutated final consequent is rejected by the syntactic checker. These are Python/syntactic controls; no Lean or other trusted proof-assistant kernel replay is claimed.

## 4. Why variable sharing blocks the proposed theorem

Let C = P ∧ ¬P. Using conjunction projections, disjunction introduction, composition and conjunction introduction, R proves C →R B. `VARIABLE_SHARING_REDUCTION.md` supplies the exact thirteen-line calculation from the inspected axiom schemes. Lines1–9 derive C →R B. Line10 supposes, for reductio, that B →R N were an R theorem. The remaining composition steps then derive C →R N.

That last implication has only P in its antecedent and only Q in its consequent. It violates variable sharing. No claim is made that C is actual, that a subject knows a contradiction, or that C is an operative epistemic ground. C serves solely in a metatheoretic reduction about what could be an R theorem.

The relevant variable-sharing proof is itself checked at its elementary matrix core. The pairs {−1,+1} and {−2,+2} are each closed under all four propositional operations. Every implication from a value in the first pair to a value in the second is undesignated. If the antecedent and consequent have disjoint atoms, assign their atoms to the two respective pairs. Structural induction keeps each whole formula in its pair, so the implication fails. Matrix soundness precludes its theoremhood.

This proves the claimed non-theoremhood for the chosen necessary identity independently of the direct calculation's presentation. More generally the same reduction applies to any constant-free theorem N whose atoms are disjoint from P. This is an explanatory generality of the **same** operation; no broader relevance-logic optimization campaign is proposed.

## 5. Strongest epistemological reply and exact consequence

Barker and Adams2010, printed227–228 and note21, expressly posit the bridge from an obtaining premise plus its implication relation to the premise's counterfactual absence under denial of the conclusion. Their note12 permits combined grounds and constrains presupposition. The present pass reread the retained text around the closure argument; it does not count the already read source as newly discovered. Adams, Barker and Clarke2017's relevant-conditional interpretation and competent factive-ground route remain the controlling stronger account.

The strongest reply is consequently available and substantive: “implies” is not mere material truth, or the counterfactual bridge is independently part of the intended model. An actual mathematical derivation can use content and laws that support a relevant implication. The inherited positive proof handles that case. Alternatively, an extra bridge can restrict the admissible interpretations beyond bare R. An arbitrary R matrix is not automatically admissible for a richer epistemic/counterfactual theory.

The countervaluation does not deny these replies. It shows what they must supply. Neither actual truth of all material premises, conjoining those premises, nor logical theoremhood of the target suffices to recover the required relevant relation from the base calculus. The earlier source bridge cannot be dismissed as missing, but it also cannot be derived simply from those weaker conditions.

For unrestricted classical entailment the implication issue is especially clear: classically, every premise entails an independent logical theorem. Yet the displayed full material ground still lacks the relevant relation. This is not proof that a genuinely competent, nonpresupposing knower can satisfy the source's entire antecedent while failing to know its conclusion. Such a counterexample would require an epistemic and basing interpretation, not just an all-designated logical valuation.

Nor is the use of paraconsistent proof theory an allegation that the actual mathematical premise or target is contradictory. Their negations are undesignated in the decisive case, and N's negation is never designated in this matrix. The contradictory formula C appears only in the explanatory nonderivability argument.

The earned result therefore changes the conditional scope claim, not the retained first-order knowledge or recognition appraisal. The complete material-premise repair has now been ruled out at precisely the logical level where the earlier matrix left it open. Selecting the correct additional bridge for an actual recognitional capacity remains a different, substantive task.

## 6. Allocation against the original programme

The recovery `closure-case-current/OBLIGATION_MATRIX.md` names four fronts, with the later computational A–H objective separate. Its broad front labels, not completion of the latest packet, govern this selection.

- **F1, original explanation and the same necessary bearer:** the latest Ameri causal reading correctly separates required actual background from an unreceived resource. Lack of deterministic necessitation is not the missing Completion premise. Useful next progress needs a warranted original-resource or whole-account step; another indeterministic example does not provide it.
- **F2, a complete common source:** the actual-original-production report already audits actual requisite dependence, endpoint dependence, concordance, and nonabsorption. A new operation needs a separately grounded requisite, a further substantive original-production argument, or positive original-resource ontology. Another response table is not that input. The agency report adds positive practical-perfection appraisal but explicitly does not discriminate necessarily concordant agents by number.
- **F3, communication to warranted knowledge and obligation:** the present conditional-typing operation is selected from its epistemic continuation. It resolves one explicit formal residual. An application to transmitted authoritative communication still needs the actual source, context, dispatch, force, and basing evidence required by the recovery front.
- **F4, organisational continuation:** the recovery results already test twins, migration, constitution changes, and joint procedures. A consequential new application needs a selected actual institution/dossier or an independently motivated wider institutional type. None was supplied by the six latest reports; another definition-led toy would duplicate prior work.
- **Independent mathematics and the later computational objective:** a separate bounded screen inspected the inherited mathematical records and actual pinned continuation manuscript. General stochastic/feedback spans, exact continuous-encoder dimensions, augmentation, and linear-moment approximation are already done. The adaptive discharge memory–query–risk frontier is genuinely inherited but lacks a complete specified law/dynamics/query/cost/encoder/error contract and a concrete proposed improvement. The paused specialised sampling refinements were not reopened. The graph branch's explicit exclusions alone do not justify a new graph variant. No additional operation was launched.

This comparison selects exactly one ready discriminator. It does not declare the wider programme exhausted or turn absent application inputs into final philosophical defeat.

## Stopping condition

The selected question is now answered by a primary-controlled countervaluation, an exact syntactic explanation, and explicit source-scope adjudication. Independent review remains desirable before adopting the result. Do not begin table-size optimization, another matrix hunt, or an empirical belief-formation campaign. No global T20 stopping or acceptance decision follows.
