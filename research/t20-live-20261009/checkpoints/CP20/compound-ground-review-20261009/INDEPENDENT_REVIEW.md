# Independent review: full material grounds and an R-theorem target

9 October 2026 UTC. Independent mathematical and source-scope review of `compound-ground-necessity-20261009`. Additive review only. No author-file edit, integration, programme closure, or source-body redistribution.

## Verdict

**The local formal result is correct.** The source-faithful eight-valued matrix validates all sixteen displayed R axiom schemes and both inference rules, yet the proposed valuation designates the complete material compound while rejecting its internal relevant implication to the theorem target and its relevant sensitivity formula. This eliminates the specific material-compound escape left open by the predecessor's four-valued control.

**The result does not establish an epistemic countermodel.** It identifies what material truth and bare R do not supply. It does not interpret knowledge, competent immediate inference, actual basing, non-presuppositional knowledge of the grounds, or the absence of an additional operative sensitive reason. Nor does it demonstrate that the epistemologists intended their implication premise to be material.

**There is no failure of consequence to the target:** N is an R theorem, so B ⊢R N and B semantically entails N in this sound matrix. The failed objects are the internal formula B →R N and the separate sensitivity formula ¬N →R ¬B. The current author report and checker now state this distinction explicitly.

## 1. Independent construction and source verification

I read the author's exact checker, result file, thirteen-line derivation, and subsequently supplied report. I did not import or execute the author's checker. `independent_checks.py` reconstructs the order from the twelve cover edges visibly displayed in the primary Hasse diagram, computes its transitive closure, and obtains meet and join as unique greatest lower and least upper bounds. This is independent of the author's three-bit implementation.

The implication and negation tables were separately transcribed from the image of printed p. 271. All 64 implication entries, all eight negation entries, and all 128 meet/join results agree with the author implementation. Negation is involutive; lattice join agrees with its De Morgan definition. The numerical-looking labels are names, not a linear numerical order. Numeric min/max would be an incorrect reconstruction.

The primary source is [Standefer, Actual Issues for Relevant Logics](https://shawn-standefer.github.io/pdfs/actual.pdf), printed pp. 270–271, Theorem 4 and Table 2. These pages provide the matrix, designation convention, variable-sharing argument, and an explicit statement that R's axioms and rules preserve designation. I inspected the complete extracted passage around Theorem 4 and the p. 271 table image. The source calls it the Anderson–Belnap matrix argument; this review's exact identification is Table 2, regardless of the submitted packet's M0 shorthand.

I separately read and visually checked printed pp. 176–177 of [Bimbó, Dunn and Ferenz, Two manuscripts, one by Routley, one by Meyer](https://ojs.wgtn.ac.nz/ajl/article/view/4066), including A1–A16, R1–R2, and Definition 1.1. Those exact schemes were independently entered into the review checker. No optional truth constant, fusion, actuality operator, or modal extension is used.

Fresh execution verifies:

- 7,576 assignments across all sixteen axiom schemes; zero failures.
- All 64 value pairs for modus ponens; zero preservation failures.
- All 64 value pairs for adjunction; zero preservation failures.
- Identity N = Q →R Q is an A1 instance, so its theoremhood is syntactic, not inferred merely from validity in one algebra.
- All eight Q values make N designated and ¬N undesignated.
- Corrupting the +0 identity-table entry is detected by reevaluation of A1.

The usual induction on derivations gives soundness for this matrix. This does not assert matrix completeness or a cognitive interpretation.

## 2. Exact witness and exact nonderivability

Let P and Q be distinct atoms. Define N = Q →R Q, M = ¬P ∨ N, and B = P ∧ M. At P = +1 and Q = +2, the independently reconstructed algebra gives:

- P = +1; ¬P = −1.
- N = +2; ¬N = −2.
- M = +3; ¬M = −3.
- B = +1; ¬B = −1.
- B →R N = −3.
- ¬N →R ¬B = −3.

All four displayed positive contents are designated; their negations are not. The Boolean designation projection also preserves conjunction, disjunction, and negation. Thus the witness does not require an actually designated contradiction or an undesignated target.

Take Γ = {P, M}; adding B and N does not remove the witness. Since Γ is designated but each disputed formula is not, soundness yields Γ ⊬R (B →R N) and Γ ⊬R (¬N →R ¬B). In particular, neither disputed formula is an R theorem. This is the exact formal nonderivability established here.

By contrast, Γ ⊢R N and B ⊢R N hold simply because N is already an axiom instance. The same is true semantically in M0. The unrestricted deduction-theorem inference from consequence to an internal relevant conditional is precisely what cannot be imported.

The exhaustive two-variable sweep finds 32 assignments with designated P and M, of which eight reject full-compound sensitivity. The count is a robustness check, not extra philosophical evidence.

## 3. The thirteen-line reduction

The independent parser reads the delivered proof text and checks axiom instances by schema matching, without trusting the author's substitution labels or proof-building code. It checks each modus-ponens reference and adjunction directly. All thirteen lines are valid with line 10 treated solely as the hypothetical theorem under reductio. The proof is rejected if that hypothesis is not allowed, and a corrupted final consequent is rejected.

For C = P ∧ ¬P, lines 1–9 establish ⊢R C →R B. If B →R N were a theorem, composition would establish C →R N. The antecedent has only P and the consequent only Q.

The variable-sharing restriction is not merely assumed from a secondary summary. The primary Standefer passage supplies the proof framework, and the review independently checks its algebraic core: {−1,+1} and {−2,+2} are each closed under every propositional operation, and all four arrows from the first pair to the second are undesignated. Structural induction then proves the restriction for arbitrary constant-free formulas on disjoint variable sets. Together with matrix soundness, this rules out C →R N and validates the reductio.

The contradiction C is not an actual or known premise. It appears only inside a metatheoretic argument about theoremhood. This distinction is explicit in the delivered derivation and must remain explicit in any summary.

## 4. Strongest compound-preserving repair

The new test retains both premises as B = P ∧ (¬P ∨ N). It does not repeat the predecessor's weaker P-only test. At the decisive valuation, P alone, M alone, and the complete B all fail sensitivity. Regrouping or repeating P and M leaves B unchanged. Even adding ¬(P ∧ ¬P) leaves the conjunction at +1 and sensitivity at −3.

Two formally successful alternatives clarify rather than erase the boundary:

1. **Use a relevant premise:** with Brel = P ∧ (P →R N), R proves Brel →R N and ¬N →R ¬Brel for arbitrary P and N. The independent parser verifies the predecessor's full nineteen-line proof. All 64 P,Q valuations also validate both formulas. At the present countervaluation, however, P →R N and Brel are undesignated. Replacing M with that relevant conditional adds a stronger input and excludes the countervaluation; it is not licensed by M's designation.
2. **Add the target to the ground:** B ∧ N has value +0 and both desired formulas have value +2. Similarly P ∧ N is sensitive. But adding an independently known operative N requires epistemic evidence and may presuppose the very conclusion whose acquisition is being explained. BA2010's non-presupposition clause makes that danger explicit. No such prior knowledge has been supplied.

There is also a useful equivalence warning. Classically B is equivalent to P ∧ N. In this matrix they have different values (+1 and +0) and different internal-arrow behavior. Classical equivalence cannot be treated as unrestricted relevant interchangeability. This does not refute classical equivalence or classical modus ponens: the review separately checks all four Boolean P,N assignments and finds no classical counterexample.

Accordingly the result challenges both (a) actual material truth as sufficient for relevant sensitivity and (b) a proposed universal upgrade from ordinary classical consequence to the internal relevant conditional or sensitivity. It does not challenge classical consequence itself. Even the weaker schematic fact P ∧ (¬P ∨ N) ⊨CL N remains valid.

## 5. Primary epistemic scope

A separate read-only source check independently inspected the relevant primary passages; I also reread the decisive passages myself.

[Barker and Adams, Epistemic Closure and Skepticism](https://logos-and-episteme.acadiasi.ro/wp-content/uploads/2015/02/EPISTEMIC-CLOSURE-AND-SKEPTICISM.pdf), printed p. 228 note 21, explicitly presupposes the implication-to-counterfactual bridge. It is therefore wrong to describe the authors as never stating the bridge. The new result bears on its interpretation or justification if implication is given a material or unrestricted classical reading. Their note does not claim that the bridge is a theorem of bare R.

The same article specifies competent immediate same-time inference at p. 222 note 1. Its p. 225 note 12 permits combined experiential and known reasons and requires that knowing a factive ground not presuppose the conclusion. Truth designation alone proves none of those conditions.

[Adams, Barker and Clarke, Knowledge as Fact-Tracking True Belief](https://www.scielo.br/j/man/a/JS5dxNB79fZvM9pJxRk3HzF/) invokes relevant conditionals in its later discussion, allows existing conditions and laws in interpreting an implicative subjunctive, and supplies an operative sensitive intellectual experience in its arithmetic example. Its note 19 blocks automatic inheritance of every premise-belief's supporting reasons. These resources cannot simply be omitted from a purported countermodel, but neither can an unspecified additional reason be silently inserted into the actual basis.

Neither inspected source identifies the known content “P implies Q” explicitly with ¬P ∨ Q. Therefore “the complete material compound” is warranted; “the authors' complete operative grounds” without qualification is not. A stronger relevant interpretation or an independently imposed bridge can exclude the present valuation. Showing the bridge is extra structure is not showing that this structure is inconsistent or epistemologically false.

No interpreted subject has been constructed who satisfies all source antecedent conditions while lacking the specified knowledge. No ordinary false-mathematical possible world, specific human recognition process, or Creator-recognition episode has been supplied. The accepted result remains a logical scope finding.

## 6. Review binding and stopping boundary

The initial hashes are retained in `INPUT_HASHES_INITIAL.sha256`. During review, the author updated the checker and JSON claim wording to distinguish internal implication from consequence, and supplied its report. I read the revised checker and complete report, reran the independent tests against the current table/results, and bind this verdict to the final hashes in `INPUT_HASHES.sha256`. The thirteen-line proof did not change.

The report's programme-allocation section was read but is outside this logical review's certification scope; no independent re-audit of those other research fronts is implied. The exact matrix/proof finding and its epistemic ceiling are accepted. No packaging, acceptance-state edit, programme exhaustion, or closure decision follows from this review.

Deliverables: this review, the independent checker, its machine-readable results and run log, input bindings, source-reading record, and output hashes. Primary PDFs and page images remain research witnesses in their existing locations and are not copied into this review deliverable.
