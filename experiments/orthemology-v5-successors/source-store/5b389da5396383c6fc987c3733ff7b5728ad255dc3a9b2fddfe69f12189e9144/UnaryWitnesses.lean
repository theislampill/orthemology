/- Explicit total finite comparison and distinguishing-input search. -/
import UnaryNormalForm

namespace P01AC.UnaryIdentity

def comparisonBound (d e : Description) : Nat :=
  max d.exceptions.length e.exceptions.length + separationBound d.coeffs e.coeffs

theorem description_prefix_complete (d e : Description)
    (h : ∀ n, n ≤ comparisonBound d e → d.denote n = e.denote n) :
    ∀ n, d.denote n = e.denote n := by
  let m := comparisonBound d e
  have hdl : d.exceptions.length ≤ m := by dsimp [m, comparisonBound]; omega
  have hel : e.exceptions.length ≤ m := by dsimp [m, comparisonBound]; omega
  have hcut : separationBound d.coeffs e.coeffs ≤ m := by dsimp [m, comparisonBound]; omega
  have hp : polyEqual d.coeffs e.coeffs = true := by
    apply (eval_eq_iff_polyEqual_of_bound _ _ hcut).mp
    have hm := h m (Nat.le_refl _)
    simpa only [Description.tail d hdl, Description.tail e hel] using hm
  intro n
  by_cases hn : n ≤ m
  · exact h n hn
  · have hdn : d.exceptions.length ≤ n := by omega
    have hen : e.exceptions.length ≤ n := by omega
    rw [Description.tail d hdn, Description.tail e hen]
    exact polyEqual_implies_eval hp n

def finiteBound (e f : Expr) : Nat := comparisonBound (normalise e) (normalise f)

theorem finite_prefix_iff_valid (e f : Expr) :
    (∀ n, n ≤ finiteBound e f → e.denote n = f.denote n) ↔ Valid e f := by
  rw [valid_iff_denote]
  constructor
  · intro h
    have hc := description_prefix_complete (normalise e) (normalise f)
      (fun n hn => by simpa only [normalise_correct] using h n hn)
    simpa only [normalise_correct] using hc
  · intro h n _
    exact h n

/-- Descending finite search. `none` is distinct from the witness `some 0`. -/
def findMismatch (f g : Nat → Nat) : Nat → Option Nat
  | 0 => none
  | b+1 => if f b = g b then findMismatch f g b else some b

theorem findMismatch_sound (f g : Nat → Nat) (b : Nat) {n : Nat}
    (h : findMismatch f g b = some n) : n < b ∧ f n ≠ g n := by
  induction b with
  | zero => simp [findMismatch] at h
  | succ b ih =>
    by_cases he : f b = g b
    · have ht : findMismatch f g b = some n := by simpa [findMismatch, he] using h
      obtain ⟨hn, hd⟩ := ih ht
      exact ⟨by omega, hd⟩
    · have hn : b = n := by simpa [findMismatch, he] using h
      subst n
      exact ⟨by omega, he⟩

theorem findMismatch_none_iff (f g : Nat → Nat) (b : Nat) :
    findMismatch f g b = none ↔ ∀ n, n < b → f n = g n := by
  induction b with
  | zero => simp [findMismatch]
  | succ b ih =>
    by_cases he : f b = g b
    · simp only [findMismatch, if_pos he, ih]
      constructor
      · intro h n hn
        by_cases hnb : n < b
        · exact h n hnb
        · have hne : n = b := by omega
          simpa [hne] using he
      · intro h n hn
        exact h n (by omega)
    · simp only [findMismatch, if_neg he, Option.noConfusion]
      constructor
      · intro h; cases h
      · intro h
        exact False.elim (he (h b (Nat.lt_succ_self b)))

def distinguishingInput (e f : Expr) : Option Nat :=
  findMismatch (normalise e).denote (normalise f).denote (finiteBound e f + 1)

theorem distinguishingInput_sound (e f : Expr) {n : Nat}
    (h : distinguishingInput e f = some n) :
    n ≤ finiteBound e f ∧ e.denote n ≠ f.denote n := by
  obtain ⟨hn, hd⟩ := findMismatch_sound (normalise e).denote (normalise f).denote _ h
  exact ⟨by omega, by simpa only [normalise_correct] using hd⟩

theorem distinguishingInput_none_iff_valid (e f : Expr) :
    distinguishingInput e f = none ↔ Valid e f := by
  rw [distinguishingInput, findMismatch_none_iff]
  simp only [normalise_correct, Nat.lt_succ_iff]
  exact finite_prefix_iff_valid e f

theorem distinguishingInput_complete (e f : Expr) (h : ¬ Valid e f) :
    ∃ n, distinguishingInput e f = some n := by
  cases hw : distinguishingInput e f with
  | none => exact False.elim (h ((distinguishingInput_none_iff_valid e f).mp hw))
  | some n => exact ⟨n, rfl⟩

def verifyNegative (e f : Expr) (n : Nat) : Bool := decide (e.denote n ≠ f.denote n)

theorem verifyNegative_sound (e f : Expr) (n : Nat) (h : verifyNegative e f n = true) :
    ¬ Valid e f := by
  intro hv
  have hn : e.denote n ≠ f.denote n := by simpa [verifyNegative] using h
  exact hn ((valid_iff_denote e f).mp hv n)

theorem negative_certificate_complete (e f : Expr) :
    (∃ n, verifyNegative e f n = true) ↔ ¬ Valid e f := by
  constructor
  · rintro ⟨n, hn⟩
    exact verifyNegative_sound e f n hn
  · intro h
    obtain ⟨n, hn⟩ := distinguishingInput_complete e f h
    exact ⟨n, by simpa [verifyNegative] using (distinguishingInput_sound e f hn).2⟩

example : distinguishingInput exceptionalExample .variable = some 2 := rfl
example : distinguishingInput (.ifEq .variable (.constant 0) (.constant 3) .variable)
    .variable = some 0 := rfl
example : distinguishingInput (.add .variable (.constant 0)) .variable = none := rfl
example : verifyNegative exceptionalExample .variable 2 = true := rfl
example : verifyNegative exceptionalExample .variable 3 = false := rfl

#print axioms finite_prefix_iff_valid
#print axioms distinguishingInput_none_iff_valid
#print axioms negative_certificate_complete
end P01AC.UnaryIdentity
