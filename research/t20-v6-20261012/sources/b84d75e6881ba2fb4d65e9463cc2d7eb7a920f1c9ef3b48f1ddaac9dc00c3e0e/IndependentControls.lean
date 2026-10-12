import JointRecursorAudit
import JointInductionRawBoundary

namespace IndependentRecursorReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
open JointCompletion JointCompletion.InductionComputation
open JointCompletion.RecursorUniqueness
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- No extra law uniformity assumption is needed beyond one generic-context
source derivation. Conversely, a packaged source law yields that derivation. -/
theorem generic_packaged_laws_equivalent {Γ : Tel} {P : Ty} {s u : Poly}
    (hc : CtxJ Γ) :
    (∃ l, HasJ (N :: Γ) l (successorLawFamily P s u)) ↔
    (∃ l, HasJ Γ l (.pi N (successorLawFamily P s u))) := by
  constructor
  · rintro ⟨l, hl⟩
    exact ⟨abstract l, .piIntro (.pi (N_form hc) (has_form hl)) hl
      (scoped_abstract (has_scoped hl))⟩
  · rintro ⟨l, hl⟩
    exact ⟨.app (pren Nat.succ l) (.var 0),
      section_at_variable hc (pi_body_form (has_form hl)) hl⟩

/-- The identity premise cannot be omitted or replaced by endpoint typing. -/
theorem identity_premise_control {Γ : Tel} {A B : Ty} {f x y e : Poly}
    (hc : CtxJ Γ) (hA : FormJ Γ A) (hB : FormJ Γ B)
    (hf : HasJ Γ f (arr A B)) (hx : HasJ Γ x A) (hy : HasJ Γ y A)
    (he : HasJ Γ e (.identity A x y)) :
    HasJ Γ ident (.identity B (.app f x) (.app f y)) := by
  fail_if_success exact arrow_congr hc hA hB hf hx hy
  fail_if_success exact arrow_congr hc hA hB hf hx hy hx
  exact arrow_congr hc hA hB hf hx hy he

/-- A second section law for an unrelated operation cannot be silently used. -/
theorem shared_operation_control {Γ : Tel} {P : Ty} {s t u v lu lv lt : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P)) (hv : HasJ Γ v (.pi N P))
    (hlu : HasJ Γ lu (.pi N (successorLawFamily P s u)))
    (hlv : HasJ Γ lv (.pi N (successorLawFamily P s v)))
    (_hlt : HasJ Γ lt (.pi N (successorLawFamily P t v))) :
    HasJ Γ (abstract (abstract ident)) (dependentStepType (comparisonFamily P u v)) := by
  fail_if_success exact comparison_step hc hP hs hu hv hlu _hlt
  exact comparison_step hc hP hs hu hv hlu hlv

/-- The canonical result also follows from ordinary un-packaged generic laws. -/
theorem canonical_generic_law {Γ : Tel} {P : Ty} {p s u zu lu : Poly}
    (hc : CtxJ Γ) (hP : FormJ (N :: Γ) P)
    (hp : HasJ Γ p (inst P zero)) (hs : HasJ Γ s (dependentStepType P))
    (hu : HasJ Γ u (.pi N P))
    (hzu : HasJ Γ zu (.identity (inst P zero) (.app u zero) p))
    (hlu : HasJ (N :: Γ) lu (successorLawFamily P s u)) :
    HasJ Γ ident (.identity (.pi N P) u (sectionPoly p s)) := by
  exact unique_to_canonical hc hP hp hs hu hzu
    (.piIntro (.pi (N_form hc) (has_form hlu)) hlu (scoped_abstract (has_scoped hlu)))

/-- The new-family result remains an actual source judgment after weakening
into a genuinely newly formed context. -/
theorem new_context_control :
    HasJ [JointCompletion.Controls.newMotive] ident
      (wk (.identity (.pi N InductionComputation.Controls.family)
        (abstract ident) (sectionPoly ident InductionComputation.Controls.step))) := by
  have hM : FormJ [] JointCompletion.Controls.newMotive :=
    has_form JointCompletion.Controls.new_motive_reentry
  exact has_wk RecursorUniqueness.Controls.new_family_uniqueness .nil hM

/-- Both sides of the strict typed/Raw distinction still coexist with uniqueness. -/
theorem strict_raw_boundary_preserved :
    (∃ e, HasJ [N] e (.identity N RawBoundary.left RawBoundary.right)) ∧
    ¬ P01AC.Intensional.Plus.PolyConvPlus RawBoundary.left RawBoundary.right :=
  ⟨RawBoundary.successor_typed_identity, RawBoundary.successor_not_raw⟩

#print axioms generic_packaged_laws_equivalent
#print axioms identity_premise_control
#print axioms shared_operation_control
#print axioms canonical_generic_law
#print axioms new_context_control
#print axioms strict_raw_boundary_preserved
#print recursor_unique
#print recursor_unique_generic_laws
#print unique_to_canonical

end IndependentRecursorReview
