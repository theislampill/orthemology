/- Independent raw-semantics discriminator. A raw replacement without formation
   need not have diagonal identity, even at the same valuation. -/
import AllSemanticSubstitution
import P01DependentControls

namespace P01AC.IndependentMalformed
open OrthemologyV2 OrthemologyV3 P01D P01R

def badReplacement : Ty :=
  .sigma (.param 0) (.identity .raw (.var 0) (.atom .i))

def totalObjects : OEnv := fun _ => P01DF.totalPER

theorem malformed_unary_related :
    F badReplacement totalObjects zeroEnv
      (pairTerm .i .i) (pairTerm P01DF.skk .i) := by
  exact ⟨pair_represented _ _, pair_represented _ _, trivial,
    pair_first _ _, pair_second _ _, pair_second _ _⟩

theorem malformed_right_self_fails :
    ¬ F badReplacement totalObjects zeroEnv
      (pairTerm P01DF.skk .i) (pairTerm P01DF.skk .i) := by
  intro h
  have bad : Conv P01DF.skk .i := (pair_first _ _).symm.trans h.2.2.2.1
  exact P01Source.I_SKK_not_convertible bad.symm

theorem malformed_diagonal_fails :
    ¬ G badReplacement (diagEnv totalObjects) zeroEnv zeroEnv
      (pairTerm .i .i) (pairTerm P01DF.skk .i) := by
  intro h
  exact malformed_right_self_fails h.2.1

theorem unconditional_diagonal_is_false :
    ¬ (∀ (A : Ty) (ρ : OEnv) (η : Env) (t u : Term),
      G A (diagEnv ρ) η η t u ↔ F A ρ η t u) := by
  intro h
  exact malformed_diagonal_fails ((h _ _ _ _ _).mpr malformed_unary_related)

/-- The conditional semantic substitution interface actually excludes this raw
    malformed image; its diagonal requirement cannot be dropped as redundant. -/
theorem malformed_image_match_impossible (s : REnv) :
    ¬ ImageMatch (fun _ => badReplacement) (diagEnv totalObjects)
      zeroEnv zeroEnv s := by
  intro h
  have unary : (s.left 0).rel (pairTerm .i .i) (pairTerm P01DF.skk .i) :=
    Eq.mp (h.left 0 _ _) malformed_unary_related
  exact malformed_diagonal_fails (Eq.mpr (h.diagLeft 0 _ _) unary)

end P01AC.IndependentMalformed
