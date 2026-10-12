import CheckerSemantics

namespace PDChecker
noncomputable section
open scoped ENNReal

variable {m : ℕ} {Q Γ : Type*}

def initialAt (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) (i : Fin m) : State m Q Γ :=
  .live i (tape i) q0 h0

lemma initialAt_inj (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) (i j : Fin m) :
    initialAt tape q0 h0 i=initialAt tape q0 h0 j ↔ i=j := by
  constructor
  · intro h
    injection h
  · intro h;subst j;rfl

/-- The checker is sampled once in the explicit initial belief. No boot transition is inserted. -/
def initialBelief [Nonempty (Fin m)] (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) : PMF (State m Q Γ) :=
  PMF.map (initialAt tape q0 h0) (PMF.uniformOfFintype (Fin m))

lemma initialBelief_support [Nonempty (Fin m)] (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) :
    (initialBelief tape q0 h0).support=Set.range (initialAt tape q0 h0) := by
  simp [initialBelief,PMF.support_map,PMF.support_uniformOfFintype]

lemma initialBelief_apply [Nonempty (Fin m)] (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) (i : Fin m) :
    initialBelief tape q0 h0 (initialAt tape q0 h0 i)=(m:ℝ≥0∞)⁻¹ := by
  classical
  rw [initialBelief,PMF.map_apply]
  simp_rw [initialAt_inj]
  simp only [PMF.uniformOfFintype_apply,Fintype.card_fin]
  have heq : (fun j : Fin m => if i=j then (m:ℝ≥0∞)⁻¹ else 0) =
      (fun j : Fin m => if j=i then (m:ℝ≥0∞)⁻¹ else 0) := by
    funext j
    by_cases hij : i=j
    · subst j;rfl
    · simp [hij,Ne.symm hij]
  rw [heq]
  exact tsum_ite_eq i _

lemma initialBelief_positive [Nonempty (Fin m)] (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) (i : Fin m) :
    0 < initialBelief tape q0 h0 (initialAt tape q0 h0 i) := by
  rw [initialBelief_apply]
  simp

lemma initialBelief_normalized [Nonempty (Fin m)] [Fintype Q] [Fintype Γ]
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) :
    ∑ s : State m Q Γ, initialBelief tape q0 h0 s=1 := by
  rw [← tsum_fintype]
  exact PMF.tsum_coe _

end
end PDChecker
