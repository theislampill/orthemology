import GlobalParitySufficiency

/-! Exact coBüchi target-safety consequences for the accepted controller.
These are finite semantic facts, not a proof of its expected total cost. -/
noncomputable section
namespace HiddenParity.Cost

/-- Minimum-parity encoding of a coBüchi objective: bad has priority 1. -/
def coBuchiPriority {Pair : Type*} (bad : Pair → Prop) [DecidablePred bad] (e : Pair) : ℕ :=
  if bad e then 1 else 2

theorem cobuchi_minimum_even_iff {Pair : Type*} (bad : Pair → Prop)
    [DecidablePred bad] (E : Finset Pair) (hE : E.Nonempty) :
    (∃ d, IsMinimum (coBuchiPriority bad) E d ∧ d % 2 = 0) ↔
      ∀ e ∈ E, ¬ bad e := by
  constructor
  · rintro ⟨d,⟨⟨f,hf,hfd⟩,hmin⟩,hd⟩ e he hbad
    have hde := hmin e he
    simp only [coBuchiPriority,if_pos hbad] at hde
    unfold coBuchiPriority at hfd
    split_ifs at hfd <;> omega
  · intro hgood
    refine ⟨2,⟨?_,?_⟩,by decide⟩
    · obtain ⟨e,he⟩ := hE
      exact ⟨e,he,by simp [coBuchiPriority,hgood e he]⟩
    · intro e he
      simp [coBuchiPriority,hgood e he]

/-- A fully matching qualifying target has no bad pair at all. This is stronger
than eventual absence and explains why an eternal matched operating segment
contributes zero cost even if stale tests later interrupt it. -/
theorem qualifying_matching_all_good {State Pair Model : Type*}
    [Fintype State] [DecidableEq State] [DecidableEq Pair]
    (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (bad : Model → Pair → Prop) [∀ σ, DecidablePred (bad σ)]
    (θ σ : Model) (hσ : σ ∈ B) (allowed E : Finset Pair)
    (hQ : MarkovQualifying P source B (fun σ => coBuchiPriority (bad σ)) θ allowed E)
    (hm : Match P.row θ σ E) : ∀ e ∈ E, ¬ bad σ e := by
  exact (cobuchi_minimum_even_iff (bad σ) E hQ.2.2.1.nonempty).mp (hQ.2.2.2 σ hσ hm)

/-- The restriction to priorities 1 and 2 cannot be dropped: a winning minimum
of 0 permits a bad (odd-priority) pair in the same recurrent component. -/
theorem unrestricted_parity_even_min_allows_odd :
    (∃ d, IsMinimum (fun b : Bool => if b then 1 else 0) Finset.univ d ∧ d % 2 = 0) ∧
      (∃ b ∈ (Finset.univ : Finset Bool), (if b then 1 else 0 : ℕ) % 2 = 1) := by
  constructor
  · refine ⟨0,⟨⟨false,by simp,by simp⟩,?_⟩,by decide⟩
    intro b _
    omega
  · exact ⟨true,by simp,by simp⟩

end HiddenParity.Cost
