import Mathlib.Data.List.Basic

namespace MultivaluedReset
universe u v
variable {I : Type u} {A : I → Type v} [DecidableEq I]
abbrev State := (i : I) → A i

def put (x : State (A := A)) (i : I) (a : A i) : State (A := A) := Function.update x i a

@[simp] theorem put_same (x : State (A := A)) (i : I) : put x i (x i) = x := by
  exact Function.update_eq_self i x

/-- The relation induced by every common context, not merely present output. -/
def Coordinate (R : State (A := A) → State (A := A) → Prop)
    (i : I) (a b : A i) : Prop := ∀ z, R (put z i a) (put z i b)

def mask (l : List I) (i : I) (z x : State (A := A)) : State (A := A) :=
  match l with
  | [] => x
  | j :: js => if j = i then mask js i z x else mask js i z (put x j (z j))

theorem mask_value (l : List I) (i : I) (z x : State (A := A)) (k : I) :
    mask l i z x k = if k ≠ i ∧ k ∈ l then z k else x k := by
  induction l generalizing x with
  | nil => simp [mask]
  | cons j js ih =>
    by_cases hji : j = i
    · subst j
      by_cases hki : k = i
      · subst k; simp [mask, ih]
      · simp [mask, ih, hki]
    · simp only [mask, if_neg hji, ih]
      by_cases hki : k = i
      · subst k; simp [hji, Ne.symm hji, put]
      · by_cases hkj : k = j
        · subst k; simp [hji, put]
        · simp [hki, hkj, put]

theorem mask_eq (l : List I) (covers : ∀ i, i ∈ l)
    (i : I) (z x : State (A := A)) : mask l i z x = put z i (x i) := by
  funext k
  rw [mask_value]
  by_cases hki : k = i
  · subst k; simp [put]
  · simp [hki, covers k, put]

theorem mask_preserves (R : State (A := A) → State (A := A) → Prop)
    (stable : ∀ i a x y, R x y → R (put x i a) (put y i a))
    (l : List I) (i : I) (z x y : State (A := A)) (h : R x y) :
    R (mask l i z x) (mask l i z y) := by
  induction l generalizing x y with
  | nil => exact h
  | cons j js ih =>
    by_cases hji : j = i
    · simpa [mask, hji] using ih x y h
    · simpa [mask, hji] using ih _ _ (stable j (z j) x y h)

theorem coordinate_equivalence (R : State (A := A) → State (A := A) → Prop)
    (hR : Equivalence R) (i : I) : Equivalence (Coordinate R i) := by
  constructor
  · intro a z; exact hR.refl _
  · intro a b h z; exact hR.symm (h z)
  · intro a b c h k z; exact hR.trans (h z) (k z)

theorem coordinates_of_related (R : State (A := A) → State (A := A) → Prop)
    (stable : ∀ i a x y, R x y → R (put x i a) (put y i a))
    (l : List I) (covers : ∀ i, i ∈ l) (x y : State (A := A)) (h : R x y) :
    ∀ i, Coordinate R i (x i) (y i) := by
  intro i z
  have hm := mask_preserves R stable l i z x y h
  simpa only [mask_eq l covers] using hm

theorem related_of_coordinates_aux (R : State (A := A) → State (A := A) → Prop)
    (hR : Equivalence R) (l : List I) (x y : State (A := A))
    (hdiff : ∀ j, x j ≠ y j → j ∈ l)
    (hc : ∀ i, Coordinate R i (x i) (y i)) : R x y := by
  classical
  induction l generalizing x with
  | nil =>
    have he : x = y := by
      funext j
      by_contra hn
      exact List.not_mem_nil (hdiff j hn)
    subst y
    exact hR.refl x
  | cons i l ih =>
    let z := put x i (y i)
    have hxz : R x z := by
      have h := hc i x
      simpa only [put_same] using h
    apply hR.trans hxz
    apply ih z
    · intro j hne
      have hji : j ≠ i := by
        intro e; subst j
        exact hne (by simp [z, put])
      have hxy : x j ≠ y j := by simpa [z, put, hji] using hne
      exact (List.mem_cons.mp (hdiff j hxy)).resolve_left hji
    · intro j
      by_cases hji : j = i
      · subst j
        simpa [z, put] using (coordinate_equivalence R hR i).refl (y i)
      · simpa [z, put, hji] using hc j

/-- Any reset-congruent equivalence on a finite full dependent product factors
exactly into its universal-context coordinate-value equivalences. -/
theorem factorisation (R : State (A := A) → State (A := A) → Prop)
    (hR : Equivalence R)
    (stable : ∀ i a x y, R x y → R (put x i a) (put y i a))
    (l : List I) (covers : ∀ i, i ∈ l) (x y : State (A := A)) :
    R x y ↔ ∀ i, Coordinate R i (x i) (y i) := by
  constructor
  · exact coordinates_of_related R stable l covers x y
  · intro hc
    exact related_of_coordinates_aux R hR l x y (fun j _ => covers j) hc

#print axioms factorisation
#print axioms coordinate_equivalence
section Observational
variable {L O : Type*}

def run (T : L → State (A := A) → State (A := A)) :
    List L → State (A := A) → State (A := A)
  | [], x => x
  | a :: w, x => run T w (T a x)

def Observational (h : State (A := A) → O)
    (T : L → State (A := A) → State (A := A))
    (x y : State (A := A)) : Prop := ∀ w, h (run T w x) = h (run T w y)

omit [DecidableEq I] in
theorem observational_equivalence (h : State (A := A) → O)
    (T : L → State (A := A) → State (A := A)) : Equivalence (Observational h T) := by
  constructor
  · intro x w; rfl
  · intro x y he w; exact (he w).symm
  · intro x y z he hf w; exact (he w).trans (hf w)

omit [DecidableEq I] in
theorem observational_step (h : State (A := A) → O)
    (T : L → State (A := A) → State (A := A))
    (a : L) (x y : State (A := A)) (he : Observational h T x y) :
    Observational h T (T a x) (T a y) := fun w => he (a :: w)

/-- Direct application to independently defined future observation semantics.
All reset labels are supplied with their actual state-action correspondence. -/
theorem observational_factorisation (h : State (A := A) → O)
    (T : L → State (A := A) → State (A := A))
    (resetLabel : (i : I) → A i → L)
    (resetCorrect : ∀ i a x, T (resetLabel i a) x = put x i a)
    (l : List I) (covers : ∀ i, i ∈ l) (x y : State (A := A)) :
    Observational h T x y ↔
      ∀ i, Coordinate (Observational h T) i (x i) (y i) := by
  apply factorisation _ (observational_equivalence h T) _ l covers x y
  intro i a u v he
  simpa only [resetCorrect] using observational_step h T (resetLabel i a) u v he

#print axioms observational_factorisation
end Observational
end MultivaluedReset
