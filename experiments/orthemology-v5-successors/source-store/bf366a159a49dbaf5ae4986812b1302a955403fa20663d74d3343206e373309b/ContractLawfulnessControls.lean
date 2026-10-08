import HiddenChangeNecessity
open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic

/-- The helper's redundant source-labelled formulation is exactly the original
all-public-history common-menu lawfulness; it is not an extra restriction. -/
theorem policyLawful_iff_original {n k : ℕ} [NeZero n] {R : Type*}
    (I : HiddenChange.Input n k) (s : State n) (π : Policy R n k) :
    PolicyLawful I s π ↔ AllHistoryLawful I s π := by
  constructor
  · intro hlaw r h
    let q : PairHistory n k := h.map (fun z => ((s,z.1),z.2))
    have hh := hlaw r q
    have he : erasePairSources q = h := by
      simp [q,erasePairSources,List.map_map,Function.comp_def]
    have hs : currentState s q = currentObserved s h := by cases h <;> rfl
    simpa only [he,hs] using hh
  · intro hlaw r h
    have hh := hlaw r (erasePairSources h)
    cases h <;> exact hh

universe uZ
example {n k : ℕ} [NeZero n] [NeZero k] {R : Type*} [MeasurableSpace R]
    (I : HiddenChange.Input n k) (hI : Admissible I) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : AllHistoryLawful I s π) (d : Pair n k) (hWin : WinsAll.{uZ} I hI.1 s ρ π d) :
    ∃ body : PositiveBody n k, positiveCheck I s body = true :=
  all_adversary_winner_has_positive_body I hI s ρ π hπ
    ((policyLawful_iff_original I s π).mpr hLaw) d hWin

#print axioms policyLawful_iff_original
