/- Canonical polynomial plus finite deviations, represented by exact dense lists. -/
import UnaryPolynomial

namespace P01AC.UnaryIdentity

theorem atDefault_eq_getElem? {α : Type} (z : α) (p : List α) (n : Nat) :
    atDefault z p n = (p[n]?).getD z := by
  induction p generalizing n with
  | nil => rfl
  | cons a p ih => cases n <;> simp [atDefault, ih]

theorem atDefault_of_length_le {α : Type} (z : α) (p : List α) {n : Nat}
    (h : p.length ≤ n) : atDefault z p n = z := by
  rw [atDefault_eq_getElem?, List.getElem?_eq_none h]
  rfl

theorem atDefault_map_range {α : Type} (z : α) (b n : Nat) (g : Nat → α) :
    atDefault z ((List.range b).map g) n = if n < b then g n else z := by
  rw [atDefault_eq_getElem?, List.getElem?_map]
  by_cases h : n < b
  · rw [List.getElem?_range h]
    simp [h]
  · have hl : (List.range b).length ≤ n := by simp; omega
    rw [List.getElem?_eq_none hl]
    simp [h]

structure Description where
  coeffs : List Nat
  exceptions : List (Option Nat)
  deriving DecidableEq, Repr

def Description.denote (d : Description) (n : Nat) : Nat :=
  (atDefault none d.exceptions n).getD (polyEval d.coeffs n)

def Description.Canonical (d : Description) : Prop :=
  trimDefault 0 d.coeffs = d.coeffs ∧
  trimDefault none d.exceptions = d.exceptions ∧
  ∀ n v, atDefault none d.exceptions n = some v → v ≠ polyEval d.coeffs n

theorem Description.ext (d e : Description) (hp : d.coeffs = e.coeffs)
    (he : d.exceptions = e.exceptions) : d = e := by
  cases d
  cases e
  cases hp
  cases he
  rfl

theorem Description.tail (d : Description) {n : Nat} (h : d.exceptions.length ≤ n) :
    d.denote n = polyEval d.coeffs n := by
  simp only [Description.denote, atDefault_of_length_le none d.exceptions h, Option.getD_none]

def makeDescription (p : List Nat) (b : Nat) (f : Nat → Nat) : Description :=
  ⟨trimDefault 0 p,
   trimDefault none ((List.range b).map
     (fun n => if f n = polyEval p n then none else some (f n)))⟩

theorem makeDescription_lookup (p : List Nat) (b n : Nat) (f : Nat → Nat) :
    atDefault none (makeDescription p b f).exceptions n =
      if n < b then (if f n = polyEval p n then none else some (f n)) else none := by
  exact (trimDefault_getD none _ n).trans (atDefault_map_range none b n _)

theorem makeDescription_correct (p : List Nat) (b : Nat) (f : Nat → Nat)
    (h : ∀ n, b ≤ n → f n = polyEval p n) (n : Nat) :
    (makeDescription p b f).denote n = f n := by
  rw [Description.denote, makeDescription_lookup]
  change (if n < b then (if f n = polyEval p n then none else some (f n)) else none).getD
      (polyEval (trimDefault 0 p) n) = f n
  rw [polyEval_trim]
  by_cases hn : n < b
  · by_cases he : f n = polyEval p n <;> simp [hn, he]
  · have he := h n (by omega)
    simp [hn, he]

theorem makeDescription_canonical (p : List Nat) (b : Nat) (f : Nat → Nat) :
    (makeDescription p b f).Canonical := by
  refine ⟨trimDefault_idempotent 0 p, trimDefault_idempotent none _, ?_⟩
  intro n v hv
  rw [makeDescription_lookup] at hv
  by_cases hn : n < b
  · by_cases he : f n = polyEval p n
    · simp [hn, he] at hv
    · have hv' : f n = v := by simpa [hn, he] using hv
      change v ≠ polyEval (trimDefault 0 p) n
      rw [polyEval_trim, ← hv']
      exact he
  · simp [hn] at hv

theorem canonical_description_unique (d e : Description)
    (hd : d.Canonical) (he : e.Canonical)
    (h : ∀ n, d.denote n = e.denote n) : d = e := by
  let n := max d.exceptions.length e.exceptions.length + separationBound d.coeffs e.coeffs
  have hdl : d.exceptions.length ≤ n := by dsimp [n]; omega
  have hel : e.exceptions.length ≤ n := by dsimp [n]; omega
  have hbd : separationBound d.coeffs e.coeffs ≤ n := by dsimp [n]; omega
  have hp : d.coeffs = e.coeffs := by
    have hn := h n
    rw [Description.tail d hdl, Description.tail e hel] at hn
    have hc := (polyEqual_true_iff d.coeffs e.coeffs).mp
      ((eval_eq_iff_polyEqual_of_bound d.coeffs e.coeffs hbd).mp hn)
    simpa only [hd.1, he.1] using hc
  have hex : d.exceptions = e.exceptions := by
    have heq : trimDefault none d.exceptions = trimDefault none e.exceptions := by
      apply (trimDefault_eq_iff none _ _).mpr
      intro k
      have hk := h k
      simp only [Description.denote, hp] at hk
      cases hdk : atDefault none d.exceptions k with
      | none =>
        cases hek : atDefault none e.exceptions k with
        | none => rfl
        | some v =>
          have hv : polyEval e.coeffs k = v := by simpa [hdk, hek] using hk
          exact False.elim ((he.2.2 k v hek) hv.symm)
      | some u =>
        cases hek : atDefault none e.exceptions k with
        | none =>
          have hu : u = polyEval d.coeffs k := by simpa [hdk, hek, ← hp] using hk
          exact False.elim ((hd.2.2 k u hdk) hu)
        | some v =>
          have huv : u = v := by simpa [hdk, hek] using hk
          exact congrArg some huv
    simpa only [hd.2.1, he.2.1] using heq
  exact Description.ext d e hp hex

theorem canonical_description_eq_iff (d e : Description)
    (hd : d.Canonical) (he : e.Canonical) :
    d = e ↔ ∀ n, d.denote n = e.denote n :=
  ⟨fun h => by subst e; intro n; rfl, canonical_description_unique d e hd he⟩

example : makeDescription [0, 1] 3 (fun n => if n = 2 then 7 else n) =
    ⟨[0, 1], [none, none, some 7]⟩ := rfl
example : makeDescription [0, 1, 0] 7 (fun n => n) = ⟨[0, 1], []⟩ := rfl
example : makeDescription [0] 1 (fun n => if n = 0 then 4 else 0) =
    ⟨[], [some 4]⟩ := rfl

#print axioms makeDescription_correct
#print axioms canonical_description_unique
end P01AC.UnaryIdentity
