import UniformSection
namespace InitialityIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
-- Total-space binder substitution: index changes, ambient variables shift once.
example (P : Ty) : totalStepType P =
    subst (cons nextIndex (fun k => .var (k+1))) P := by
  simp only [totalStepType, inst, subst_comp]
  congr 1
  funext n
  cases n <;> rfl

-- Arbitrary dependent P and arbitrary source evidence, with no extra certificate.
example {Γ : Tel} {P : Ty} {p d r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero))
    (hd : Has (.sigma N P :: Γ) d (totalStepType P))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    ∃ e, HasE Γ e (inst P n) :=
  dependent_section_from_rigidity hc hP hp hd hr hn

-- The actual total-space endomap and projected source equations are constructed.
example {Γ : Tel} {P : Ty} {p d : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero))
    (hd : Has (total P :: Γ) d (totalStepType P)) :
    Has Γ (totalStep d) (arr (total P) (total P)) ∧
    Has Γ ident (ZeroAt (projectedFold (totalStep d) (totalSeed p))) ∧
    Has Γ (abstract ident) (StepAt (projectedFold (totalStep d) (totalSeed p))) :=
  ⟨total_step_has hc hP hd, projected_zero_evidence hc hP hp hd,
    projected_step_evidence hc hP hp hd⟩

-- Ordinary curried step uses the unchanged n when forming P(succ n).
example (P : Ty) (n : Poly) : inst (successorFamily P) n =
    inst P (.app P01AC.BooleanPrimitive.succPoly n) := by
  simp only [successorFamily, inst, subst_comp]
  congr 1
  funext k
  cases k with
  | zero => simp [cons, psub, P01AC.BooleanPrimitive.psub_closed (has_scoped P01AC.BooleanPrimitive.succ_has)]
  | succ k => rfl
example {Γ : Tel} {P : Ty} {p s r n : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero)) (hs : Has Γ s (dependentStepType P))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    HasE Γ (sndPoly (.app (.app n (totalStep (uncurriedStep s))) (totalSeed p)))
      (inst P n) := dependent_section_curried hc hP hp hs hr hn
-- Applying the checked source implication accepts arbitrary HasE rigidity evidence.
theorem uniform_from_arbitrary_rigidity {Γ : Tel} {P : Ty} {p s r : Poly}
    (hc : Ctx Γ) (hP : Form (N :: Γ) P)
    (hp : Has Γ p (inst P zero)) (hs : Has Γ s (dependentStepType P))
    (hr : HasE Γ r Rigidity) :
    HasE Γ (.app (abstract (sectionPoly (pren Nat.succ p) (pren Nat.succ s))) r)
      (.pi N P) := by
  have hf := rigidity_implies_section hc hP hp hs
  have hPi : Form Γ (.pi N P) := .pi (N_form hc) hP
  have ht := form_arr (rigidity_formed hc) hPi
  have result := HasE.piElim (form_inclusion ht)
    (form_inclusion (show Form Γ (inst (wk (.pi N P)) r) from by
      simpa only [inst_wk] using hPi)) hf hr
  simpa only [inst_wk] using result

example (P : Ty) : inst (shiftedFamily P) (.var 0) = P := shifted_at_var P
#print axioms uniform_from_arbitrary_rigidity
#print axioms dependent_section_from_rigidity
end InitialityIndependentReview
