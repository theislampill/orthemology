import ExecutablePruning

/-! The exact coBüchi specialization uses priority 2 for good and 1 for bad.
This module proves that both qualification and odd-layer deletion specialize
to their all-good / delete-bad counterparts, for every finite input. -/
namespace HiddenParity

variable {Pair Model Row : Type*} [DecidableEq Pair]

/-- Correct minimum-parity encoding of coBüchi pair acceptance. -/
def coBuchiPriority (good : Pair → Prop) [DecidablePred good] (e : Pair) : ℕ :=
  if good e then 2 else 1

omit [DecidableEq Pair] in
theorem coBuchi_even_minimum_iff (good : Pair → Prop) [DecidablePred good]
    (E : Finset Pair) (hne : E.Nonempty) :
    (∃ d, IsMinimum (coBuchiPriority good) E d ∧ d % 2 = 0) ↔
      ∀ e ∈ E, good e := by
  constructor
  · rintro ⟨d, hd, hEven⟩ e he
    obtain ⟨f, hf, hdf⟩ := hd.1
    have hd2 : d = 2 := by
      by_cases hgf : good f
      · simpa [coBuchiPriority, hgf] using hdf.symm
      · simp [coBuchiPriority, hgf] at hdf
        omega
    by_contra hnge
    have hle := hd.2 e he
    simp only [coBuchiPriority, if_neg hnge] at hle
    omega
  · intro hgood
    obtain ⟨e, he⟩ := hne
    refine ⟨2, ⟨⟨e, he, ?_⟩, ?_⟩, rfl⟩
    · simp [coBuchiPriority, hgood e he]
    · intro f hf
      simp [coBuchiPriority, hgood f hf]

/-- The self-verifying target test is exactly matching-model all-good acceptance. -/
theorem coBuchi_valid_iff
    (C : ComponentFamily Pair) (B : Finset Model) (row : Model → Pair → Row)
    (good : Model → Pair → Prop) [∀ σ, DecidablePred (good σ)]
    (θ : Model) (E : Finset Pair) :
    Valid C B row (fun σ => coBuchiPriority (good σ)) θ E ↔
      C.component E ∧ ∀ σ ∈ B, Match row θ σ E → ∀ e ∈ E, good σ e := by
  constructor
  · intro h
    refine ⟨h.1, ?_⟩
    intro σ hσ hm
    exact (coBuchi_even_minimum_iff (good σ) E (C.nonempty h.1)).mp (h.2 σ hσ hm)
  · rintro ⟨hc, h⟩
    refine ⟨hc, ?_⟩
    intro σ hσ hm
    exact (coBuchi_even_minimum_iff (good σ) E (C.nonempty hc)).mpr (h σ hσ hm)

omit [DecidableEq Pair] in
/-- On a used pair, being on an odd minimum layer is exactly being bad. -/
theorem coBuchi_odd_layer_iff (good : Pair → Prop) [DecidablePred good]
    {E : Finset Pair} {e : Pair} (he : e ∈ E) :
    (IsMinimum (coBuchiPriority good) E (coBuchiPriority good e) ∧
      coBuchiPriority good e % 2 = 1) ↔ ¬ good e := by
  constructor
  · rintro ⟨_, ho⟩ hg
    simp [coBuchiPriority, hg] at ho
  · intro hg
    have hp : coBuchiPriority good e = 1 := by simp [coBuchiPriority, hg]
    rw [hp]
    refine ⟨⟨⟨e, he, hp⟩, ?_⟩, rfl⟩
    intro f _
    by_cases hgf : good f <;> simp [coBuchiPriority, hgf]

/-- Every deletion round, including re-matching after earlier deletions, coincides
with matching-model bad-pair pruning under the 2/1 encoding. -/
theorem coBuchi_badPair_iff
    (C : ComponentFamily Pair) (B : Finset Model) (row : Model → Pair → Row)
    (good : Model → Pair → Prop) [∀ σ, DecidablePred (good σ)]
    (θ : Model) (U : Finset Pair) (e : Pair) :
    BadPair C B row (fun σ => coBuchiPriority (good σ)) θ U e ↔
      ∃ D ∈ maximalComponents C U, e ∈ D ∧ ∃ σ ∈ B,
        Match row θ σ D ∧ ¬ good σ e := by
  constructor
  · rintro ⟨D, hD, he, σ, hσ, hm, hmin, ho⟩
    exact ⟨D, hD, he, σ, hσ, hm, (coBuchi_odd_layer_iff (good σ) he).mp ⟨hmin, ho⟩⟩
  · rintro ⟨D, hD, he, σ, hσ, hm, hg⟩
    have h := (coBuchi_odd_layer_iff (good σ) he).mpr hg
    exact ⟨D, hD, he, σ, hσ, hm, h.1, h.2⟩

end HiddenParity
