# Reverse literal completion-principle separation

## New checked result

For the literal retained E = SigmaTagBoundary.Eta and R = SourceRigidity.Rigidity, no polynomial p has either of these closed typings in unchanged HasE:

- p : E → R
- p : E → (R → Bottom)

The same exclusions hold in original Has by inclusion. This is the previously missing reverse orientation; the retained SigmaTagBoundary packet already excludes R → E and R → (E → Bottom). Searches across retained hase/homogeneous Lean and RESULT files found no existing reverse result before this additive proof.

## Small reused proof, no replacement model

1. HenkinSoundness.F interprets Raw by the universal relation and Sigma componentwise. Hence literal Sigma Raw Raw Eta has K I as a semantic witness, directly by True and K reduction.
2. The original compiler identity is empty in that model: instantiate its endomorphism equality at the existing nonstandard nu, then atomPER, scalarStep, and a0; the retained original_q_eval and scalar_not_convertible yield contradiction. This reuses the exact old actual-source compiler counterexample, not a replacement endpoint.
3. The retained closed source theorem rigidity_implies_identity, interpreted by retained HenkinSoundness.fundamental, therefore makes R semantically empty at the closed Henkin environment.
4. A hypothetical source E → R maps the Henkin E witness to that empty R.
5. Retained componentwise FullPER simultaneously validates E and R. Its soundness rules out E → (R → Bottom). full_joint_valid exposes both witnesses explicitly.

componentwise_eta also isolates the general semantic projection calculation: given component relations satisfying their saturation laws and z self-related at their componentwise Sigma, z is related to pair(fst z,snd z). This is a theorem about that representation with stated laws, not about all conceivable semantic pair relations.

## Cross-model interpretation

- Homogeneous Henkin: literal E valid; literal R empty at the closed environment. Raw is universal, the quantifier universe is restricted, and the nonstandard nu is retained.
- Tagged FullPER: literal R valid; literal E empty (existing packet). Raw is faithful conversion, and a tag distinguishes projection-equivalent noncanonical pairs.
- Componentwise FullPER: literal E and R simultaneously valid (existing witnesses, new explicit conjunction).

All three are retained sound models of the unchanged source, but they do not share the same Raw interpretation, polymorphic universe, or Sigma relation. The Raw difference is essential disclosure: this reverse proof does not claim a faithful-Raw homogeneous model validating E and refuting R.

## Actual project consequence and limits

The two literal premises cannot substitute for one another in the unchanged source. Supplying just literal SigmaRaw Eta cannot discharge the independently identified rigidity obligation; supplying just R cannot discharge the literal Sigma eta obligation. Their simultaneous semantic satisfiability also gives no incompatibility obstruction. Thus they are separately necessary obligations relative to the proposed completion requiring both literal principles, and neither can be removed merely by deriving it from the other in the retained calculus.

This is not independence of full external completion-rule extensions. The reviewed induction equivalence involves a metatheoretic full induction schema; the Sigma equivalence involves a metatheoretic full dependent elimination/eta schema. A single object-language SigmaRaw Eta premise does not quantify over all types or motives and cannot be substituted for the full schema. The componentwise semantic projection lemma likewise is not an actual-source derivation of that schema, a new soundness induction for an extended calculus, or completeness/reflection. No new axiom, source constructor, full initiality, philosophical transport, T21, integration, or programme closure is claimed.

## Validation

Run bash check.sh. Additive CompletionSeparation.lean and Controls.lean compile with Lean 4.19.0 --trust=0 against pinned retained compiled dependencies, without a baseline rebuild. Printed axioms for every new named theorem are only propext, Classical.choice, Quot.sound. Controls verify both literal implication directions, semantic R emptiness, and rejection of source reflection and transplanting the same componentwise Eta proof into the tagged model. These are bounded signature/model controls, not an independent review. No retained source files were modified.
