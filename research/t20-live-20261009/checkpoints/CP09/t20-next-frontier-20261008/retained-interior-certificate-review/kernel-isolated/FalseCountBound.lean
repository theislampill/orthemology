import Mathlib.Data.Fintype.Card
import Mathlib.Order.Monotone.Basic
import Lean.Elab.Tactic.Omega

/-! A pathwise retained-state certificate, deriving the obstruction from
coordinate gates rather than assuming pairwise incompatible witnesses.
No probability, calibration, independence, or physical-access axioms occur. -/
namespace RetainedInterior

variable {R A B : Type*} [Preorder B]

def Hit (GA : R → A → Prop) (GB : R → B → Prop) (a : A) (b : B) : Prop :=
  ∃ r, GA r a ∧ GB r b

/-- A route hitting q_i and q_j also hits the adjacent forbidden connector r_i.
The A coordinate is copied from q_i; only B monotonicity is needed here. -/
theorem connector_forced
    (GA : R → A → Prop) (GB : R → B → Prop)
    (a : ℕ → A) (b : ℕ → B)
    (hb : Antitone b) (hGB : ∀ r, Monotone (GB r))
    {i j : ℕ} (hij : i < j) {r : R}
    (hi : GA r (a i) ∧ GB r (b i))
    (hj : GA r (a j) ∧ GB r (b j)) :
    Hit GA GB (a i) (b (i + 1)) := by
  exact ⟨r, hi.1, hGB r (hb (by omega)) hj.2⟩

/-- All q_i hits and all adjacent connector misses force an injection into
the fixed occurrence type. Occurrence identities are not observed. -/
theorem witness_injection
    (GA : R → A → Prop) (GB : R → B → Prop)
    (a : ℕ → A) (b : ℕ → B) (m : ℕ)
    (hb : Antitone b) (hGB : ∀ r, Monotone (GB r))
    (hpositive : ∀ i : Fin m, Hit GA GB (a i.val) (b i.val))
    (hnegative : ∀ i : ℕ, i + 1 < m → ¬ Hit GA GB (a i) (b (i + 1))) :
    ∃ w : Fin m → R, Function.Injective w := by
  classical
  choose w hw using hpositive
  refine ⟨w, ?_⟩
  intro i j heq
  apply Fin.ext
  by_contra hne
  rcases lt_or_gt_of_ne hne with hij | hji
  · have hj := hw j
    rw [← heq] at hj
    exact hnegative i.val (by omega)
      (connector_forced GA GB a b hb hGB hij (hw i) hj)
  · have hi := hw i
    rw [heq] at hi
    exact hnegative j.val (by omega)
      (connector_forced GA GB a b hb hGB hji (hw j) hi)

theorem route_count_bound [Fintype R]
    (GA : R → A → Prop) (GB : R → B → Prop)
    (a : ℕ → A) (b : ℕ → B) (m : ℕ)
    (hb : Antitone b) (hGB : ∀ r, Monotone (GB r))
    (hpositive : ∀ i : Fin m, Hit GA GB (a i.val) (b i.val))
    (hnegative : ∀ i : ℕ, i + 1 < m → ¬ Hit GA GB (a i) (b (i + 1))) :
    m + 1 ≤ Fintype.card R := by
  obtain ⟨w, hw⟩ := witness_injection GA GB a b m hb hGB hpositive hnegative
  simpa using Fintype.card_le_of_injective w hw

/-- Threshold-coordinate AND is an explicit instance of the source semantics. -/
theorem threshold_route_count_bound [Fintype R]
    [Preorder A] (X : R → A) (Y : R → B)
    (a : ℕ → A) (b : ℕ → B) (m : ℕ)
    (hb : Antitone b)
    (hpositive : ∀ i : Fin m, ∃ r, X r ≤ a i.val ∧ Y r ≤ b i.val)
    (hnegative : ∀ i : ℕ, i + 1 < m →
      ¬ ∃ r, X r ≤ a i ∧ Y r ≤ b (i + 1)) :
    m + 1 ≤ Fintype.card R := by
  exact route_count_bound (fun r x => X r ≤ x) (fun r y => Y r ≤ y)
    a b m hb (fun _ _ _ h hY => le_trans hY h) hpositive hnegative

end RetainedInterior

#print axioms RetainedInterior.connector_forced
#print axioms RetainedInterior.witness_injection
#print axioms RetainedInterior.route_count_bound
#print axioms RetainedInterior.threshold_route_count_bound
