import Mathlib.Data.List.Basic

/-! Finite local rejection trees. The generic atom evaluator is instantiated only
with the explicit finite atomic language in PositiveFormula; no checker or
semantic predicate is an atom of that language. Quantifiers are finite folds. -/
namespace OrthemicCertificate.Signed

inductive Formula (α : Type) where
  | constant (value : Bool)
  | literal (atom : α) (expected : Bool)
  | conj (left right : Formula α)
  | disj (left right : Formula α)
  deriving DecidableEq, Repr

namespace Formula
variable {α : Type}

def eval (atomEval : α → Bool) : Formula α → Bool
  | .constant b => b
  | .literal a expected => atomEval a == expected
  | .conj p q => eval atomEval p && eval atomEval q
  | .disj p q => eval atomEval p || eval atomEval q

def neg : Formula α → Formula α
  | .constant b => .constant (!b)
  | .literal a expected => .literal a (!expected)
  | .conj p q => .disj (neg p) (neg q)
  | .disj p q => .conj (neg p) (neg q)

@[simp] theorem eval_neg (atomEval : α → Bool) (p : Formula α) :
    eval atomEval p.neg = !(eval atomEval p) := by
  induction p with
  | constant b => rfl
  | literal a expected => cases expected <;> cases h : atomEval a <;> simp [neg, eval, h]
  | conj p q hp hq => simp [neg, eval, hp, hq]
  | disj p q hp hq => simp [neg, eval, hp, hq]

def all (ps : List (Formula α)) : Formula α := ps.foldr .conj (.constant true)
def any (ps : List (Formula α)) : Formula α := ps.foldr .disj (.constant false)
def implies (p q : Formula α) : Formula α := .disj p.neg q

def every {β : Type} (xs : List β) (p : β → Formula α) : Formula α := all (xs.map p)
def someOf {β : Type} (xs : List β) (p : β → Formula α) : Formula α := any (xs.map p)

@[simp] theorem eval_all_true (atomEval : α → Bool) (ps : List (Formula α)) :
    eval atomEval (all ps) = true ↔ ∀ p ∈ ps, eval atomEval p = true := by
  induction ps with
  | nil => simp [all, eval]
  | cons p ps ih =>
    change (eval atomEval p && eval atomEval (all ps)) = true ↔ _
    simp [ih]

@[simp] theorem eval_any_true (atomEval : α → Bool) (ps : List (Formula α)) :
    eval atomEval (any ps) = true ↔ ∃ p ∈ ps, eval atomEval p = true := by
  induction ps with
  | nil => simp [any, eval]
  | cons p ps ih =>
    change (eval atomEval p || eval atomEval (any ps)) = true ↔ _
    simp [ih]

@[simp] theorem eval_every_true {β : Type} (atomEval : α → Bool) (xs : List β)
    (p : β → Formula α) :
    eval atomEval (every xs p) = true ↔ ∀ x ∈ xs, eval atomEval (p x) = true := by
  simp [every]

@[simp] theorem eval_someOf_true {β : Type} (atomEval : α → Bool) (xs : List β)
    (p : β → Formula α) :
    eval atomEval (someOf xs p) = true ↔ ∃ x ∈ xs, eval atomEval (p x) = true := by
  simp [someOf]

@[simp] theorem eval_implies_true (atomEval : α → Bool) (p q : Formula α) :
    eval atomEval (implies p q) = true ↔
      (eval atomEval p = true → eval atomEval q = true) := by
  unfold implies
  rw [eval, eval_neg]
  cases p.eval atomEval <;> cases q.eval atomEval <;> decide

/-- List quantification retains submitted order and multiplicity. -/
def pairwise {β : Type} (rel : β → β → Formula α) : List β → Formula α
  | [] => .constant true
  | x :: xs => .conj (every xs (rel x)) (pairwise rel xs)

@[simp] theorem eval_pairwise_true {β : Type} (atomEval : α → Bool)
    (rel : β → β → Formula α) (xs : List β) :
    eval atomEval (pairwise rel xs) = true ↔
      xs.Pairwise (fun x y => eval atomEval (rel x y) = true) := by
  induction xs with
  | nil => simp [pairwise, eval]
  | cons x xs ih => simp [pairwise, eval, ih, List.pairwise_cons]

end Formula

inductive Refutation where
  | leaf
  | left (child : Refutation)
  | right (child : Refutation)
  | both (left right : Refutation)
  deriving DecidableEq, Repr

/-- Every evidence node must agree with the formula constructor. A rejected
conjunction names one failing branch; a rejected disjunction covers both. -/
def rejectCheck {α : Type} (atomEval : α → Bool) : Formula α → Refutation → Bool
  | .constant b, .leaf => !b
  | .literal a expected, .leaf => !(atomEval a == expected)
  | .conj p _, .left r => rejectCheck atomEval p r
  | .conj _ q, .right r => rejectCheck atomEval q r
  | .disj p q, .both r s => rejectCheck atomEval p r && rejectCheck atomEval q s
  | _, _ => false

theorem refutation_sound {α : Type} (atomEval : α → Bool) (p : Formula α)
    (r : Refutation) (h : rejectCheck atomEval p r = true) :
    p.eval atomEval = false := by
  induction p generalizing r with
  | constant b => cases r <;> simpa [rejectCheck, Formula.eval] using h
  | literal a expected => cases r <;> simpa [rejectCheck, Formula.eval] using h
  | conj p q hp hq =>
    cases r with
    | leaf => simp [rejectCheck] at h
    | left r => simp [Formula.eval, hp r h]
    | right r => simp [Formula.eval, hq r h]
    | both r s => simp [rejectCheck] at h
  | disj p q hp hq =>
    cases r with
    | leaf => simp [rejectCheck] at h
    | left r => simp [rejectCheck] at h
    | right r => simp [rejectCheck] at h
    | both r s =>
      have hs : rejectCheck atomEval p r = true ∧ rejectCheck atomEval q s = true := by
        simpa [rejectCheck] using h
      simp [Formula.eval, hp r hs.1, hq s hs.2]

/-- Structurally terminating generation; on true formulas the result is merely a
candidate and is never accepted. The option wrapper below suppresses it. -/
def refutationCandidate {α : Type} (atomEval : α → Bool) : Formula α → Refutation
  | .constant _ => .leaf
  | .literal _ _ => .leaf
  | .conj p q => if p.eval atomEval then .right (refutationCandidate atomEval q)
      else .left (refutationCandidate atomEval p)
  | .disj p q => .both (refutationCandidate atomEval p) (refutationCandidate atomEval q)

theorem refutationCandidate_correct {α : Type} (atomEval : α → Bool) (p : Formula α)
    (h : p.eval atomEval = false) :
    rejectCheck atomEval p (refutationCandidate atomEval p) = true := by
  induction p with
  | constant b => simpa [Formula.eval, refutationCandidate, rejectCheck] using h
  | literal a expected => simpa [Formula.eval, refutationCandidate, rejectCheck] using h
  | conj p q hp hq =>
    cases he : p.eval atomEval with
    | false => simp [refutationCandidate, he, rejectCheck, hp he]
    | true =>
      have hqe : q.eval atomEval = false := by simpa [Formula.eval, he] using h
      simp [refutationCandidate, he, rejectCheck, hq hqe]
  | disj p q hp hq =>
    have hs : p.eval atomEval = false ∧ q.eval atomEval = false := by
      simpa [Formula.eval] using h
    simp [refutationCandidate, rejectCheck, hp hs.1, hq hs.2]

theorem refutation_complete {α : Type} (atomEval : α → Bool) (p : Formula α)
    (h : p.eval atomEval = false) : ∃ r, rejectCheck atomEval p r = true :=
  ⟨refutationCandidate atomEval p, refutationCandidate_correct atomEval p h⟩

def refute {α : Type} (atomEval : α → Bool) (p : Formula α) : Option Refutation :=
  if p.eval atomEval then none else some (refutationCandidate atomEval p)

@[simp] theorem refute_eq_none_iff {α : Type} (atomEval : α → Bool) (p : Formula α) :
    refute atomEval p = none ↔ p.eval atomEval = true := by
  simp [refute]

theorem refute_checked {α : Type} (atomEval : α → Bool) (p : Formula α)
    (r : Refutation) (h : refute atomEval p = some r) :
    rejectCheck atomEval p r = true := by
  unfold refute at h
  split at h
  · contradiction
  · cases h
    exact refutationCandidate_correct atomEval p (by simpa using ‹¬p.eval atomEval = true›)

end OrthemicCertificate.Signed
