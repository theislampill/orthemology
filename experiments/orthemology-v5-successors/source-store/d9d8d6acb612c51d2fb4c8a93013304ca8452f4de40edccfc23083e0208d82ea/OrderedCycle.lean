import Mathlib.Data.Finset.Sort

/-! Executable increasing-order cycles. No arbitrary finite equivalence is used. -/
namespace OrthemicCertificate.Direct
variable {A : Type*} [LinearOrder A]

/-- The order is the literal increasing sort of the submitted finite menu. -/
def cycleAction (F : Finset A) (fallback : A) (n : ℕ) : A :=
  if h : F.Nonempty then
    (F.orderIsoOfFin rfl ⟨n % F.card, Nat.mod_lt _ (Finset.card_pos.mpr h)⟩).val
  else fallback

theorem cycleAction_mem (F : Finset A) (fallback : A) (h : F.Nonempty) (n : ℕ) :
    cycleAction F fallback n ∈ F := by
  simp only [cycleAction, dif_pos h]
  exact Subtype.property _

theorem cycleAction_at_index (F : Finset A) (fallback : A) (a : F) (k : ℕ) :
    cycleAction F fallback (k * F.card + ((F.orderIsoOfFin rfl).symm a).val) = a.val := by
  have hn : F.Nonempty := ⟨a.val, a.property⟩
  simp only [cycleAction, dif_pos hn]
  have hi : (k * F.card + ((F.orderIsoOfFin rfl).symm a).val) % F.card =
      ((F.orderIsoOfFin rfl).symm a).val := by
    rw [Nat.mul_add_mod_self_right]
    exact Nat.mod_eq_of_lt ((F.orderIsoOfFin rfl).symm a).isLt
  have hfin : (⟨(k * F.card + ((F.orderIsoOfFin rfl).symm a).val) % F.card,
      Nat.mod_lt _ (Finset.card_pos.mpr hn)⟩ : Fin F.card) =
      (F.orderIsoOfFin rfl).symm a := Fin.ext hi
  rw [hfin, OrderIso.apply_symm_apply]

/-- An explicit cycle supplies every member arbitrarily late. -/
theorem exists_cycle_barrier (B : Finset A) (fallback σ : A) (hσ : σ ∈ B) (M : ℕ) :
    ∃ j, M ≤ j ∧ cycleAction B fallback j = σ := by
  let i : B := ⟨σ,hσ⟩
  let j := (M+1) * B.card + ((B.orderIsoOfFin rfl).symm i).val
  have hcard : 0 < B.card := Finset.card_pos.mpr ⟨σ,hσ⟩
  refine ⟨j,?_,?_⟩
  · dsimp [j]
    exact (Nat.le_succ M).trans ((Nat.le_mul_of_pos_right _ hcard).trans (Nat.le_add_right _ _))
  · exact cycleAction_at_index B fallback i (M+1)

end OrthemicCertificate.Direct
