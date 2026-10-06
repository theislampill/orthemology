/- Executable univariate coefficient lists and a natural digit separation bound.
   No polynomial oracle, classical decider, or approximate arithmetic is used. -/
import PolynomialTestBoundary

namespace P01AC.UnaryIdentity

def atDefault {α : Type} (z : α) : List α → Nat → α
  | [], _ => z
  | a :: _, 0 => a
  | _ :: p, n+1 => atDefault z p n

def trimDefault {α : Type} [DecidableEq α] (z : α) : List α → List α
  | [] => []
  | a :: p =>
    let t := trimDefault z p
    if a = z ∧ t = [] then [] else a :: t

theorem trimDefault_getD {α : Type} [DecidableEq α] (z : α) (p : List α) (n : Nat) :
    atDefault z (trimDefault z p) n = atDefault z p n := by
  induction p generalizing n with
  | nil => rfl
  | cons a p ih =>
    by_cases h : a = z ∧ trimDefault z p = []
    · rcases h with ⟨ha, ht⟩
      cases n with
      | zero => simp [trimDefault, ha, ht, atDefault]
      | succ n =>
        have hn := ih n
        simpa [ht, trimDefault, ha, atDefault] using hn
    · cases n <;> simp [trimDefault, h, atDefault, ih]

theorem trimDefault_eq_nil_iff {α : Type} [DecidableEq α] (z : α) (p : List α) :
    trimDefault z p = [] ↔ ∀ n, atDefault z p n = z := by
  constructor
  · intro h n
    rw [← trimDefault_getD z p n, h]
    rfl
  · induction p with
    | nil => intro _; rfl
    | cons a p ih =>
      intro h
      have ha : a = z := h 0
      have ht : trimDefault z p = [] := ih (fun n => h (n+1))
      simp [trimDefault, ha, ht]

theorem trimDefault_eq_iff {α : Type} [DecidableEq α] (z : α) (p q : List α) :
    trimDefault z p = trimDefault z q ↔ ∀ n, atDefault z p n = atDefault z q n := by
  constructor
  · intro h n
    rw [← trimDefault_getD z p n, ← trimDefault_getD z q n, h]
  · induction p generalizing q with
    | nil =>
      intro h
      exact ((trimDefault_eq_nil_iff z q).mpr (fun n => (h n).symm)).symm
    | cons a p ih =>
      cases q with
      | nil =>
        intro h
        exact (trimDefault_eq_nil_iff z (a :: p)).mpr h
      | cons b q =>
        intro h
        have hab : a = b := h 0
        have ht := ih q (fun n => h (n+1))
        simp only [trimDefault, hab, ht]

theorem trimDefault_idempotent {α : Type} [DecidableEq α] (z : α) (p : List α) :
    trimDefault z (trimDefault z p) = trimDefault z p :=
  (trimDefault_eq_iff z _ _).mpr (trimDefault_getD z p)

def polyEval : List Nat → Nat → Nat
  | [], _ => 0
  | a :: p, n => a + n * polyEval p n

theorem polyEval_trim (p : List Nat) (n : Nat) :
    polyEval (trimDefault 0 p) n = polyEval p n := by
  induction p with
  | nil => rfl
  | cons a p ih =>
    by_cases h : a = 0 ∧ trimDefault 0 p = []
    · rcases h with ⟨ha, ht⟩
      have hp : polyEval p n = 0 := by simpa [ht, polyEval] using ih.symm
      simp [trimDefault, ha, ht, polyEval, hp]
    · simp [trimDefault, h, polyEval, ih]

def polyAdd : List Nat → List Nat → List Nat
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a+b) :: polyAdd p q

theorem polyAdd_eval (p q : List Nat) (n : Nat) :
    polyEval (polyAdd p q) n = polyEval p n + polyEval q n := by
  induction p generalizing q with
  | nil => simp [polyAdd, polyEval]
  | cons a p ih =>
    cases q with
    | nil => simp [polyAdd, polyEval]
    | cons b q => simp [polyAdd, polyEval, ih, Nat.mul_add, Nat.add_assoc, Nat.add_left_comm]

def polyScale (a : Nat) (p : List Nat) : List Nat := p.map (a * ·)

theorem polyScale_eval (a : Nat) (p : List Nat) (n : Nat) :
    polyEval (polyScale a p) n = a * polyEval p n := by
  induction p with
  | nil => simp [polyScale, polyEval]
  | cons b p ih =>
    simp only [polyScale, List.map_cons, polyEval]
    simp only [polyScale] at ih
    rw [ih, Nat.mul_add]
    simp only [Nat.mul_assoc, Nat.mul_left_comm]

def polyMul : List Nat → List Nat → List Nat
  | [], _ => []
  | a :: p, q => polyAdd (polyScale a q) (0 :: polyMul p q)

theorem polyMul_eval (p q : List Nat) (n : Nat) :
    polyEval (polyMul p q) n = polyEval p n * polyEval q n := by
  induction p with
  | nil => simp [polyMul, polyEval]
  | cons a p ih =>
    simp [polyMul, polyAdd_eval, polyScale_eval, polyEval, ih,
      Nat.add_mul, Nat.mul_assoc]

theorem member_le_sum (p : List Nat) {a : Nat} (h : a ∈ p) : a ≤ p.sum := by
  induction p with
  | nil => simp at h
  | cons b p ih =>
    rcases List.mem_cons.mp h with rfl | ht
    · simp
    · simp only [List.sum_cons]
      exact Nat.le_trans (ih ht) (Nat.le_add_left _ _)

theorem polyEval_zero_coefficients (p : List Nat) {n : Nat} (hn : 0 < n)
    (h : polyEval p n = 0) : ∀ i, atDefault 0 p i = 0 := by
  induction p with
  | nil => intro i; rfl
  | cons a p ih =>
    have ha : a = 0 := Nat.eq_zero_of_add_eq_zero_right h
    have ht : polyEval p n = 0 := by
      have hm : n * polyEval p n = n * 0 := by
        simpa only [Nat.mul_zero] using Nat.eq_zero_of_add_eq_zero_left h
      exact Nat.mul_left_cancel hn hm
    intro i
    cases i with
    | zero => exact ha
    | succ i => exact ih ht i

theorem polyEval_coefficients_of_small_digits (p q : List Nat) {n : Nat} (hn : 0 < n)
    (hp : ∀ a ∈ p, a < n) (hq : ∀ a ∈ q, a < n)
    (he : polyEval p n = polyEval q n) : ∀ i, atDefault 0 p i = atDefault 0 q i := by
  induction p generalizing q with
  | nil =>
    exact fun i => (polyEval_zero_coefficients q hn he.symm i).symm
  | cons a p ih =>
    cases q with
    | nil => exact polyEval_zero_coefficients (a :: p) hn he
    | cons b q =>
      have ha : a < n := hp a (by simp)
      have hb : b < n := hq b (by simp)
      have hab : a = b := by
        have hmod := congrArg (fun t => t % n) he
        simpa only [polyEval, Nat.add_mul_mod_self_left,
          Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hb] using hmod
      have ht : polyEval p n = polyEval q n := by
        have hmul : n * polyEval p n = n * polyEval q n := by
          apply Nat.add_left_cancel (n := a)
          simpa only [polyEval, hab] using he
        exact Nat.mul_left_cancel hn hmul
      have htall := ih q (fun c hc => hp c (by simp [hc]))
        (fun c hc => hq c (by simp [hc])) ht
      intro i
      cases i with
      | zero => exact hab
      | succ i => exact htall i

def polyEqual (p q : List Nat) : Bool := decide (trimDefault 0 p = trimDefault 0 q)
def separationBound (p q : List Nat) : Nat := 2 + p.sum + q.sum

theorem polyEqual_true_iff (p q : List Nat) :
    polyEqual p q = true ↔ trimDefault 0 p = trimDefault 0 q := by
  simp [polyEqual]

theorem polyEqual_implies_eval {p q : List Nat} (h : polyEqual p q = true) (n : Nat) :
    polyEval p n = polyEval q n := by
  rw [← polyEval_trim p n, ← polyEval_trim q n, (polyEqual_true_iff p q).mp h]

theorem eval_eq_iff_polyEqual_of_bound (p q : List Nat) {n : Nat}
    (hn : separationBound p q ≤ n) :
    polyEval p n = polyEval q n ↔ polyEqual p q = true := by
  constructor
  · intro he
    apply (polyEqual_true_iff p q).mpr
    apply (trimDefault_eq_iff 0 p q).mpr
    have hpos : 0 < n := by simp only [separationBound] at hn; omega
    apply polyEval_coefficients_of_small_digits p q hpos
    · intro a ha
      have hle := member_le_sum p ha
      simp only [separationBound] at hn
      omega
    · intro a ha
      have hle := member_le_sum q ha
      simp only [separationBound] at hn
      omega
    · exact he
  · intro h
    exact polyEqual_implies_eval h n

theorem polyEqual_iff_all_eval (p q : List Nat) :
    polyEqual p q = true ↔ ∀ n, polyEval p n = polyEval q n := by
  constructor
  · exact fun h n => polyEqual_implies_eval h n
  · intro h
    exact (eval_eq_iff_polyEqual_of_bound p q (Nat.le_refl _)).mp (h _)

example : trimDefault 0 [0, 0, 0] = [] := rfl
example : trimDefault 0 [3, 0, 2, 0, 0] = [3, 0, 2] := rfl
example : trimDefault (none : Option Nat) [none, some 7, none] = [none, some 7] := rfl
example : polyEqual [1, 2, 0] [1, 2] = true := rfl
example : polyEqual [0, 1] [0, 0, 1] = false := rfl
example : polyEval [0, 1] 1 = polyEval [0, 0, 1] 1 := rfl
example : polyEval [0, 1] (separationBound [0, 1] [0, 0, 1]) ≠
    polyEval [0, 0, 1] (separationBound [0, 1] [0, 0, 1]) := by decide

#print axioms eval_eq_iff_polyEqual_of_bound
#print axioms polyEqual_iff_all_eval
end P01AC.UnaryIdentity
