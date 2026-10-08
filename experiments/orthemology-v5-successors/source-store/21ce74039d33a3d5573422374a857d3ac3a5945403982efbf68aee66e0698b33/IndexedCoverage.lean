import Refutation
import Mathlib.Data.List.Range

namespace OrthemicCertificate.Signed

/-- Evidence is in exact increasing index order. Length mismatches, repeated
indices, omitted positions and out-of-range extra entries reject structurally. -/
def indexedCheck {α : Type} (accept : α → Refutation → Bool) :
    Nat → List α → List (Nat × Refutation) → Bool
  | _, [], [] => true
  | i, x :: xs, (j,r) :: rs => decide (j = i) && accept x r && indexedCheck accept (i+1) xs rs
  | _, _, _ => false

/-- Acceptance forces the exact complete ordered index span. -/
theorem indexedCheck_indices {α : Type} (accept : α → Refutation → Bool)
    (i : Nat) (xs : List α) (rs : List (Nat × Refutation))
    (h : indexedCheck accept i xs rs = true) :
    rs.map Prod.fst = List.range' i xs.length := by
  induction xs generalizing i rs with
  | nil => cases rs <;> simpa [indexedCheck] using h
  | cons x xs ih =>
    cases rs with
    | nil => simp [indexedCheck] at h
    | cons jr rs =>
      rcases jr with ⟨j,r⟩
      have hs : (j = i ∧ accept x r = true) ∧ indexedCheck accept (i+1) xs rs = true := by
        simpa [indexedCheck] using h
      simp [hs.1.1, ih (i+1) rs hs.2, List.range'_succ]

theorem indexedCheck_length {α : Type} (accept : α → Refutation → Bool)
    (i : Nat) (xs : List α) (rs : List (Nat × Refutation))
    (h : indexedCheck accept i xs rs = true) : rs.length = xs.length := by
  have heq := congrArg List.length (indexedCheck_indices accept i xs rs h)
  simpa using heq

/-- Every submitted domain member has locally checked evidence. -/
theorem indexedCheck_sound {α : Type} (accept : α → Refutation → Bool)
    (i : Nat) (xs : List α) (rs : List (Nat × Refutation))
    (h : indexedCheck accept i xs rs = true) :
    ∀ x ∈ xs, ∃ r, accept x r = true := by
  induction xs generalizing i rs with
  | nil => simp
  | cons x xs ih =>
    cases rs with
    | nil => simp [indexedCheck] at h
    | cons jr rs =>
      rcases jr with ⟨j,r⟩
      have hs : (j = i ∧ accept x r = true) ∧ indexedCheck accept (i+1) xs rs = true := by
        simpa [indexedCheck] using h
      intro y hy
      rcases List.mem_cons.mp hy with rfl | hy
      · exact ⟨r,hs.1.2⟩
      · exact ih (i+1) rs hs.2 y hy

/-- Generation is a structurally recursive traversal of the actual domain. -/
def indexedCandidate {α β : Type} (atomEval : β → Bool) (formula : α → Formula β) :
    Nat → List α → List (Nat × Refutation)
  | _, [] => []
  | i, x :: xs => (i,refutationCandidate atomEval (formula x)) ::
      indexedCandidate atomEval formula (i+1) xs

theorem indexedCandidate_correct {α β : Type} (atomEval : β → Bool)
    (formula : α → Formula β) (i : Nat) (xs : List α)
    (h : ∀ x ∈ xs, (formula x).eval atomEval = false) :
    indexedCheck (fun x r => rejectCheck atomEval (formula x) r) i xs
      (indexedCandidate atomEval formula i xs) = true := by
  induction xs generalizing i with
  | nil => rfl
  | cons x xs ih =>
    have hx := refutationCandidate_correct atomEval (formula x) (h x (by simp))
    have ht := ih (i+1) (fun y hy => h y (by simp [hy]))
    simp [indexedCandidate, indexedCheck, hx, ht]

end OrthemicCertificate.Signed
