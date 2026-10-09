import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Lattice.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/-! General finite-support combinatorics of a graph-constrained Walsh pullback.
No probability or finite-enumeration premise occurs in the principal theorem. -/
namespace GraphContinuation

variable {α : Type*} [DecidableEq α]

/-- A finite nonempty connected set, presented by adding adjacent vertices. -/
inductive Grown (Adj : α → α → Prop) : Finset α → Prop
  | singleton (r : α) : Grown Adj {r}
  | insert {T : Finset α} {u v : α} : Grown Adj T → u ∈ T → v ∉ T →
      Adj u v → Grown Adj (insert v T)

/-- A mask execution records both current active slots and every visited slot.
A gate can be omitted when its accumulating slot is inactive; the explicit
idle constructor also permits counting such a no-op. -/
inductive Run (Adj : α → α → Prop) (r : α) : Finset α → Finset α → ℕ → Prop
  | start : Run Adj r {r} {r} 0
  | add {S T : Finset α} {n : ℕ} {u v : α} : Run Adj r S T n →
      u ∈ S → v ∉ S → Adj u v →
      Run Adj r (insert v S) (insert v T) (n + 1)
  | remove {S T : Finset α} {n : ℕ} {u v : α} : Run Adj r S T n →
      u ∈ S → v ∈ S → u ≠ v → Adj u v →
      Run Adj r (S.erase v) T (n + 1)
  | idle {S T : Finset α} {n : ℕ} : Run Adj r S T n →
      Run Adj r S T (n + 1)

 theorem active_subset {Adj : α → α → Prop} {r : α} {S T : Finset α} {n : ℕ}
    (h : Run Adj r S T n) : S ⊆ T := by
  induction h with
  | start => exact Finset.Subset.refl _
  | add h hu hv ha ih => exact Finset.insert_subset_insert _ ih
  | remove h hu hv hne ha ih => exact Finset.Subset.trans (Finset.erase_subset _ _) ih
  | idle h ih => exact ih

 theorem visited_grown {Adj : α → α → Prop} {r : α} {S T : Finset α} {n : ℕ}
    (h : Run Adj r S T n) : Grown Adj T := by
  induction h with
  | start => exact Grown.singleton _
  | @add S T n u v h hu hv ha ih =>
      by_cases hvT : v ∈ T
      · simpa [Finset.insert_eq_of_mem hvT] using ih
      · exact Grown.insert ih (active_subset h hu) hvT ha
  | remove h hu hv hne ha ih => exact ih
  | idle h ih => exact ih

/-- Every transient slot costs two toggles; final slots cost one, except the
initial singleton. The potential proof also covers repeated visits and no-ops. -/
 theorem visited_card_bound {Adj : α → α → Prop} {r : α}
    {S T : Finset α} {n : ℕ} (h : Run Adj r S T n) :
    2 * T.card ≤ n + S.card + 1 := by
  induction h with
  | start => simp
  | @add S T n u v h hu hv ha ih =>
      rw [Finset.card_insert_of_not_mem hv]
      by_cases hvT : v ∈ T
      · rw [Finset.card_insert_of_mem hvT]; omega
      · rw [Finset.card_insert_of_not_mem hvT]; omega
  | @remove S T n u v h hu hv hne ha ih =>
      have hc := Finset.card_erase_add_one hv
      omega
  | idle h ih => omega

/-- A finite connected witness can synthesize any nonempty selected mask
inside it. The proof uses only symmetric adjacency. -/
 theorem synthesize {Adj : α → α → Prop} (symm : Symmetric Adj)
    {T : Finset α} (ht : Grown Adj T) :
    ∀ S : Finset α, S.Nonempty → S ⊆ T →
      ∃ r U n, Run Adj r S U n ∧ n + S.card + 1 ≤ 2 * T.card := by
  induction ht with
  | singleton r =>
      intro S hS hsub
      have heq : S = {r} := Finset.eq_singleton_iff_unique_mem.mpr (by
        obtain ⟨s, hs⟩ := hS
        have hsr : s = r := by simpa using hsub hs
        subst s
        exact ⟨hs, fun y hy => by simpa using hsub hy⟩)
      subst S
      exact ⟨r, {r}, 0, Run.start, by simp⟩
  | @insert T u v ht hu hv ha ih =>
      intro S hS hsub
      by_cases hvS : v ∈ S
      · by_cases hempty : (S.erase v).Nonempty
        · let Q := insert u (S.erase v)
          have hQT : Q ⊆ T := by
            intro x hx
            rcases Finset.mem_insert.mp hx with hxu | hx
            · simpa [hxu] using hu
            · have hxS := (Finset.mem_erase.mp hx).2
              have hxv := (Finset.mem_erase.mp hx).1
              rcases Finset.mem_insert.mp (hsub hxS) with h | h
              · exact False.elim (hxv h)
              · exact h
          obtain ⟨r, U, n, hr, hn⟩ := ih Q (Finset.insert_nonempty _ _) hQT
          have huv : u ≠ v := by intro h; subst u; exact hv hu
          have hvQ : v ∉ Q := by simp [Q, Ne.symm huv]
          have huQ : u ∈ Q := Finset.mem_insert_self _ _
          have hadd := Run.add hr huQ hvQ ha
          by_cases huS : u ∈ S
          · have huE : u ∈ S.erase v := Finset.mem_erase.mpr ⟨huv, huS⟩
            have hQ : Q = S.erase v := Finset.insert_eq_of_mem huE
            have hfin : insert v Q = S := by rw [hQ, Finset.insert_erase hvS]
            have hc := Finset.card_erase_add_one hvS
            rw [hQ] at hn
            refine ⟨r, insert v U, n + 1, ?_, ?_⟩
            · simpa only [hfin] using hadd
            · rw [Finset.card_insert_of_not_mem hv]; omega
          · have hfin : (insert v Q).erase u = S := by
              change (insert v (insert u (S.erase v))).erase u = S
              rw [Finset.insert_comm, Finset.insert_erase hvS, Finset.erase_insert huS]
            have hvA : v ∈ insert v Q := Finset.mem_insert_self _ _
            have huA : u ∈ insert v Q := Finset.mem_insert_of_mem huQ
            have hrem := Run.remove hadd hvA huA (Ne.symm huv) (symm ha)
            have huE : u ∉ S.erase v := by
              intro h; exact huS (Finset.mem_of_mem_erase h)
            have hc := Finset.card_erase_add_one hvS
            have hqc : Q.card = (S.erase v).card + 1 :=
              Finset.card_insert_of_not_mem huE
            refine ⟨r, insert v U, (n + 1) + 1, ?_, ?_⟩
            · simpa only [hfin] using hrem
            · rw [Finset.card_insert_of_not_mem hv]; omega
        · have hsingleton : S = {v} := by
            apply Finset.eq_singleton_iff_unique_mem.mpr
            refine ⟨hvS, ?_⟩
            intro x hx
            by_cases hxv : x = v
            · exact hxv
            · exact False.elim (hempty ⟨x, Finset.mem_erase.mpr ⟨hxv, hx⟩⟩)
          subst S
          refine ⟨v, {v}, 0, Run.start, ?_⟩
          rw [Finset.card_insert_of_not_mem hv]
          simp only [Finset.card_singleton]
          omega
      · have hST : S ⊆ T := by
          intro x hx
          rcases Finset.mem_insert.mp (hsub hx) with h | h
          · exact False.elim (hvS (h ▸ hx))
          · exact h
        obtain ⟨r, U, n, hr, hn⟩ := ih S hS hST
        refine ⟨r, U, n, hr, ?_⟩
        rw [Finset.card_insert_of_not_mem hv]
        omega

/-- The minimum size is specified by its ordinary finite connected witness,
not by a minimum over executions. -/
def SteinerMinimum (Adj : α → α → Prop) (S : Finset α) (t : ℕ) : Prop :=
  (∃ T : Finset α, S ⊆ T ∧ Grown Adj T ∧ T.card = t) ∧
  ∀ T : Finset α, S ⊆ T → Grown Adj T → t ≤ T.card

/-- Exact optimum: a shortest execution has n + |S| + 1 = 2 t.
Equivalently n = 2 t - |S| - 1. No enumeration or bound on α is assumed. -/
theorem exact_steiner_cost {Adj : α → α → Prop} (symm : Symmetric Adj)
    {S : Finset α} (hS : S.Nonempty) {t : ℕ}
    (ht : SteinerMinimum Adj S t) :
    ∃ r U n, Run Adj r S U n ∧ n + S.card + 1 = 2 * t ∧
      ∀ r' U' n', Run Adj r' S U' n' → n ≤ n' := by
  obtain ⟨⟨T, hST, hT, hcard⟩, hmin⟩ := ht
  obtain ⟨r, U, n, hr, hn⟩ := synthesize symm hT S hS hST
  have hminU := hmin U (active_subset hr) (visited_grown hr)
  have hlow := visited_card_bound hr
  refine ⟨r, U, n, hr, ?_, ?_⟩
  · omega
  · intro r' U' n' hr'
    have hm' := hmin U' (active_subset hr') (visited_grown hr')
    have hl' := visited_card_bound hr'
    omega

 theorem reachable_iff_connected_superset {Adj : α → α → Prop}
    (symm : Symmetric Adj) {S : Finset α} (hS : S.Nonempty) :
    (∃ r U n, Run Adj r S U n) ↔
    ∃ T : Finset α, S ⊆ T ∧ Grown Adj T := by
  constructor
  · rintro ⟨r, U, n, hr⟩
    exact ⟨U, active_subset hr, visited_grown hr⟩
  · rintro ⟨T, hST, hT⟩
    obtain ⟨r, U, n, hr, _⟩ := synthesize symm hT S hS hST
    exact ⟨r, U, n, hr⟩


section SemanticBridge
variable {M : Type*} [CommMonoid M]

def character (S : Finset α) (x : α → M) : M := ∏ k ∈ S, x k

def toggle (S : Finset α) (j : α) : Finset α :=
  if j ∈ S then S.erase j else insert j S

def gate (i j : α) (x : α → M) : α → M :=
  Function.update x i (x i * x j)

/-- On sign-valued coordinates, toggling a character slot multiplies by that sign. -/
theorem character_toggle (S : Finset α) (j : α) (x : α → M)
    (hx : x j * x j = 1) :
    character (toggle S j) x = character S x * x j := by
  by_cases hj : j ∈ S
  · unfold toggle character
    rw [if_pos hj, ← Finset.mul_prod_erase S x hj]
    calc
      (∏ k ∈ S.erase j, x k) = (1 : M) * (∏ k ∈ S.erase j, x k) := by simp
      _ = (x j * x j) * (∏ k ∈ S.erase j, x k) := by rw [hx]
      _ = (x j * ∏ k ∈ S.erase j, x k) * x j := by ac_rfl
  · simp only [toggle, hj, if_false, character, Finset.prod_insert hj]
    exact mul_comm _ _

/-- This is the actual tensor-observable pullback, not an assumed mask rule. -/
theorem character_gate (S : Finset α) (i j : α) (x : α → M)
    (hx : x j * x j = 1) :
    character S (gate i j x) =
      character S x := by
  by_cases hi : i ∈ S
  · rw [if_pos hi, character_toggle S j x hx]
    unfold character gate
    rw [Finset.prod_update_of_mem hi, Finset.sdiff_singleton_eq_erase, ← Finset.mul_prod_erase S x hi]
    ac_rfl
  · rw [if_neg hi]
    exact Finset.prod_update_of_not_mem hi x (x i * x j)

end SemanticBridge

end GraphContinuation

#print axioms GraphContinuation.visited_card_bound
#print axioms GraphContinuation.synthesize
#print axioms GraphContinuation.exact_steiner_cost
#print axioms GraphContinuation.reachable_iff_connected_superset

#print axioms GraphContinuation.character_gate
