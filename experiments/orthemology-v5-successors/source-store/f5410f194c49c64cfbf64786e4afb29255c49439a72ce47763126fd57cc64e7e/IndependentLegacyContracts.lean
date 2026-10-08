import TypedLegacy
namespace TypedNucleusIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01TC P01TC.Legacy

/-- Closed final syntax alone does not qualify a tree with an unscoped premise. -/
def hiddenOpenTree : Derivation (.atom .i) .raw :=
  .conv (.raw (.app (.app (.atom .k) (.atom .i)) (.var 0))) (.k _ _)

def rawLeavesScoped (n : Nat) {p A} : Derivation p A → Prop
  | .raw p => Scoped n p
  | .finite _ | .i _ | .k _ _ | .s _ _ _ | .identityIntro _ => True
  | .allIntro _ | .allElim _ => False
  | .app hf ha => rawLeavesScoped n hf ∧ rawLeavesScoped n ha
  | .piIntro hb => rawLeavesScoped (n+1) hb
  | .piElim hb | .sigmaIntro hb | .sigmaSnd hb => rawLeavesScoped n hb
  | .j he hd => rawLeavesScoped n he ∧ rawLeavesScoped n hd
  | .conv hp _ => rawLeavesScoped n hp

theorem restricted_raw_leaves {n p A} {h : Derivation p A} {A'}
    (hr : Restricted n h A') : rawLeavesScoped n h := by
  induction hr <;> simp_all only [rawLeavesScoped, and_self]

theorem hidden_open_tree_excluded : ¬ Restricted 0 hiddenOpenTree .raw := by
  intro h
  exact Nat.not_lt_zero 0 (restricted_raw_leaves h).2

theorem hidden_open_tree_still_has_closed_conclusion :
    P01DF.Has (.atom .i) .raw ∧ Scoped 0 (.atom .i) :=
  ⟨hiddenOpenTree.erase,True.intro⟩

def oldConvertedProof : Derivation P01DF.convertedProof
    (.identity (.atom .i) (.atom .i)) :=
  .conv (.identityIntro (.refl _)) (.symm (.i _))

def oldProofJ : Derivation (jPoly (.atom .i) (.atom .i) P01DF.convertedProof)
    (P01DF.motiveAt (.identity (.var 0) (.atom .i)) (.atom .i) P01DF.convertedProof) :=
  .j oldConvertedProof (.identityIntro (.refl _))

theorem old_proof_j_is_restricted :
    Restricted 0 oldProofJ
      (P01TC.motiveAt (.identity .raw (.var 0) (.atom .i)) (.atom .i) P01DF.convertedProof) := by
  apply Restricted.j
  · exact .identity (Nat.zero_lt_succ 1) True.intro
  · trivial
  · trivial
  · exact .conv (.symm (.i _)) ⟨True.intro,True.intro⟩
      (.identityIntro (.refl _) True.intro True.intro)
  · exact .identityIntro (.refl _) True.intro True.intro

theorem old_proof_j_code_preserved :
    Has [] (jPoly (.atom .i) (.atom .i) P01DF.convertedProof)
      (P01TC.motiveAt (.identity .raw (.var 0) (.atom .i)) (.atom .i) P01DF.convertedProof) :=
  old_proof_j_is_restricted.raw_embed

#print P01TC.Legacy.Derivation
#print P01TC.Legacy.Derivation.erase
#print P01TC.Legacy.Restricted
#print P01TC.Legacy.Restricted.raw_embed
#print P01TC.Legacy.Restricted.old_judgment
#print P01TC.Legacy.Restricted.object_agrees
#print P01TC.Legacy.Restricted.heterogeneous_agrees
#print P01TC.Legacy.Translation.all_image
#print P01TC.Legacy.no_allIntro
#print P01TC.Legacy.no_allElim
#print axioms P01TC.Legacy.Restricted.raw_embed
#print axioms P01TC.Legacy.Derivation.erase
#print axioms P01TC.Legacy.Translation.F_agrees
#print axioms P01TC.Legacy.Translation.G_agrees
#print axioms P01TC.Legacy.no_allIntro
#print axioms P01TC.Legacy.no_allElim
#print axioms P01TC.Legacy.no_dependentPolyType
#print axioms P01TC.Legacy.no_excludedFiniteConclusion
#print axioms hidden_open_tree_excluded
#print axioms old_proof_j_code_preserved
end TypedNucleusIndependentReview
