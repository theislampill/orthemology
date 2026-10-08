/- Exact expressive image, constructive finite-description reification, and a
   genuine boundary: truncated predecessor is outside the declared grammar. -/
import UnaryNormalForm

namespace P01AC.UnaryIdentity

def Expr.fromCoefficients : List Nat → Expr
  | [] => .constant 0
  | a :: p => .add (.constant a) (.mul .variable (fromCoefficients p))

theorem Expr.fromCoefficients_denote (p : List Nat) (n : Nat) :
    (fromCoefficients p).denote n = polyEval p n := by
  induction p with
  | nil => rfl
  | cons a p ih => simp only [fromCoefficients, denote, polyEval, ih]

def Expr.withExceptions (base : Expr) : Nat → List (Option Nat) → Expr
  | _, [] => base
  | k, none :: rest => withExceptions base (k+1) rest
  | k, some v :: rest =>
      .ifEq .variable (.constant k) (.constant v) (withExceptions base (k+1) rest)

theorem Expr.withExceptions_before (base : Expr) (xs : List (Option Nat)) :
    ∀ k n, n < k → (withExceptions base k xs).denote n = base.denote n := by
  induction xs with
  | nil => intro k n _; rfl
  | cons a xs ih =>
    intro k n hn
    cases a with
    | none => exact ih (k+1) n (by omega)
    | some v =>
      have hne : n ≠ k := by omega
      simpa only [withExceptions, denote, if_neg hne] using ih (k+1) n (by omega)

theorem Expr.withExceptions_at (base : Expr) (xs : List (Option Nat)) :
    ∀ k i, (withExceptions base k xs).denote (k+i) =
      (atDefault none xs i).getD (base.denote (k+i)) := by
  induction xs with
  | nil => intro k i; rfl
  | cons a xs ih =>
    intro k i
    cases i with
    | zero =>
      cases a with
      | none =>
        simpa only [withExceptions, atDefault, Option.getD_none, Nat.add_zero] using
          withExceptions_before base xs (k+1) k (Nat.lt_succ_self k)
      | some v => simp [withExceptions, denote, atDefault]
    | succ i =>
      have hne : k+(i+1) ≠ k := by omega
      have hshift : k+(i+1) = (k+1)+i := by omega
      have hne' : (k+1)+i ≠ k := by omega
      cases a with
      | none => simpa only [withExceptions, atDefault, hshift] using ih (k+1) i
      | some v =>
        simpa only [withExceptions, denote, if_neg hne, if_neg hne', atDefault, hshift] using ih (k+1) i

def Expr.reify (d : Description) : Expr :=
  withExceptions (fromCoefficients d.coeffs) 0 d.exceptions

theorem Expr.reify_denote (d : Description) (n : Nat) :
    (reify d).denote n = d.denote n := by
  have h := withExceptions_at (fromCoefficients d.coeffs) d.exceptions 0 n
  simpa only [reify, Nat.zero_add, fromCoefficients_denote, Description.denote] using h

theorem canonical_reify_normalise (d : Description) (h : d.Canonical) :
    normalise (Expr.reify d) = d := by
  apply canonical_description_unique _ _ (normalise_canonical _) h
  intro n
  rw [normalise_correct, Expr.reify_denote]

theorem expressible_iff_eventually_polynomial (f : Nat → Nat) :
    (∃ e : Expr, ∀ n, e.denote n = f n) ↔
      ∃ p : List Nat, ∃ b : Nat, ∀ n, b ≤ n → f n = polyEval p n := by
  constructor
  · rintro ⟨e,he⟩
    refine ⟨(tailData e).2, (tailData e).1, ?_⟩
    intro n hn
    rw [← he n]
    exact tailData_correct e n hn
  · rintro ⟨p,b,h⟩
    refine ⟨Expr.reify (makeDescription p b f), ?_⟩
    intro n
    rw [Expr.reify_denote]
    exact makeDescription_correct p b f h n

theorem truncated_predecessor_not_expressible :
    ¬ ∃ e : Expr, ∀ n, e.denote n = n-1 := by
  rintro ⟨e, he⟩
  let p := (tailData e).2
  let q := polyAdd p [1]
  let m := max (tailData e).1 (separationBound q [0, 1]) + 1
  have htail : (tailData e).1 ≤ m := by dsimp [m]; omega
  have hcut : separationBound q [0, 1] ≤ m := by dsimp [m]; omega
  have hpos : 0 < m := by dsimp [m]; omega
  have hvalue : polyEval q m = polyEval [0, 1] m := by
    calc
      polyEval q m = polyEval p m + 1 := by simp [q, polyAdd_eval, polyEval]
      _ = (m-1)+1 := by rw [← tailData_correct e m htail, he m]
      _ = m := by omega
      _ = polyEval [0, 1] m := by simp [polyEval]
  have hp := (eval_eq_iff_polyEqual_of_bound q [0, 1] hcut).mp hvalue
  have hz := polyEqual_implies_eval hp 0
  simp [q, polyAdd_eval, polyEval] at hz

example : normalise (Expr.reify ⟨[0, 1], [none, none, some 7]⟩) =
    ⟨[0, 1], [none, none, some 7]⟩ := rfl
example : normalise (Expr.reify ⟨[0, 1, 0], [none, some 1, none]⟩) =
    ⟨[0, 1], []⟩ := rfl

#print axioms expressible_iff_eventually_polynomial
#print axioms truncated_predecessor_not_expressible
end P01AC.UnaryIdentity
