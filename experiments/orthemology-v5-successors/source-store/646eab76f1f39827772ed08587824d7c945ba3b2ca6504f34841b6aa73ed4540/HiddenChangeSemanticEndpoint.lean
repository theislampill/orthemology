import HiddenChangeBinding
import HiddenChangeControllerEndpoint
import HiddenChangeNecessity

/-! Signed semantic endpoint for the finite rational one-hidden-change class.
The checked body, literal public-history controller, actual changing-mode laws,
and arbitrary-private-seed necessity are the imported proved constructions.
`WinsAll` expresses parity only. Measurability and all-history common-menu
lawfulness are independent, retained obligations. No runtime correspondence
between this Lean body and the Python certificate format is asserted. -/

noncomputable section
open MeasureTheory ProbabilityTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic
namespace HiddenChange
universe uR uZ
variable {n k : ℕ} [NeZero n] [NeZero k]

omit [NeZero n] [NeZero k] in
/-- The source-labelled helper is exactly the original public-history contract. -/
theorem policyLawful_iff_allHistoryLawful {R : Type uR}
    (I : Input n k) (s : State n) (π : Policy R n k) :
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

/-- One specified private-seed policy satisfies all three semantic obligations.
`uZ` is the universe of the adversary's private seed; `uR` is the policy seed's
universe. The probability hypothesis on rho is supplied by endpoint theorems. -/
def LawfulMeasurableWinner {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n) (ρ : Measure R)
    (π : Policy R n k) (d : Pair n k) : Prop :=
  Measurable (fun z : R × PublicHistory n k => π z.1 z.2) ∧
  AllHistoryLawful I s π ∧ WinsAll.{uZ} I hI s ρ π d

/-- Deterministic existence is expressed using Unit and its point probability.
This is a proposition, not an executable body-selection or synthesis program. -/
def DeterministicWinner (I : Input n k) (hI : I.Valid) (s : State n) (d : Pair n k) : Prop :=
  ∃ π : Policy Unit n k, LawfulMeasurableWinner.{0,uZ} I hI s (Measure.dirac ()) π d

/-- Every accepted positive body drives the actual literal deterministic policy. -/
theorem positive_compiled_semantics (I : Input n k) (hI : Admissible I)
    (s : State n) (c : PositiveBody n k) (hc : positiveCheck I s c = true) (d : Pair n k) :
    LawfulMeasurableWinner.{0,uZ} I hI.1 s (Measure.dirac ()) (compile I hI s c) d :=
  ⟨compiled_measurable I hI s c, compiled_all_history_lawful I hI s c,
    compiled_winsAll I hI s c hc d⟩

/-- Any lawful measurable policy over any supplied probability seed space
produces actual accepted finite evidence. No restriction to compiled policies. -/
theorem seeded_winner_has_positive {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : Admissible I) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k)
    (hWin : LawfulMeasurableWinner.{uR,uZ} I hI.1 s ρ π d) :
    ∃ c : PositiveBody n k, positiveCheck I s c = true :=
  all_adversary_winner_has_positive_body I hI s ρ π hWin.1
    ((policyLawful_iff_allHistoryLawful I s π).mpr hWin.2.1) d hWin.2.2

/-- Exact finite/semantic equivalence, for every adversary-seed universe. -/
theorem positive_iff_deterministic_winner (I : Input n k) (hI : Admissible I)
    (s : State n) (d : Pair n k) :
    (∃ c : PositiveBody n k, positiveCheck I s c = true) ↔
      DeterministicWinner.{uZ} I hI.1 s d := by
  constructor
  · rintro ⟨c,hc⟩
    exact ⟨compile I hI s c, positive_compiled_semantics I hI s c hc d⟩
  · rintro ⟨π,hπ⟩
    exact seeded_winner_has_positive I hI s (Measure.dirac ()) π d hπ

/-- Full raw input and initial state are bound before any semantic guarantee. -/
theorem bound_positive_compiled_semantics (I : Input n k) (hI : Admissible I)
    (s : State n) (c : SubmittedPositive n k)
    (hc : boundPositiveCheck I s c = true) (d : Pair n k) :
    I = c.input ∧ s = c.initial ∧
      LawfulMeasurableWinner.{0,uZ} I hI.1 s (Measure.dirac ()) (compile I hI s c.body) d := by
  obtain ⟨hinput,hstate,hbody⟩ := (boundPositiveCheck_iff I s c).mp hc
  exact ⟨hinput,hstate,positive_compiled_semantics I hI s c.body hbody d⟩

/-- Completeness retains the original input and initial-state binding. -/
theorem seeded_winner_has_bound_positive {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : Admissible I) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k)
    (hWin : LawfulMeasurableWinner.{uR,uZ} I hI.1 s ρ π d) :
    ∃ c : SubmittedPositive n k, boundPositiveCheck I s c = true := by
  obtain ⟨c,hc⟩ := seeded_winner_has_positive I hI s ρ π d hWin
  exact ⟨⟨I,s,c⟩,(boundPositiveCheck_iff I s _).mpr ⟨rfl,rfl,hc⟩⟩

theorem bound_positive_iff_deterministic_winner (I : Input n k) (hI : Admissible I)
    (s : State n) (d : Pair n k) :
    (∃ c : SubmittedPositive n k, boundPositiveCheck I s c = true) ↔
      DeterministicWinner.{uZ} I hI.1 s d := by
  rw [boundPositiveCheck_iff_region I hI s,
    ← positiveCheck_iff_region I hI s, positive_iff_deterministic_winner I hI s d]

/-- A negative certificate excludes every lawful measurable policy on each
arbitrary supplied probability seed space, not merely the deterministic compiler. -/
theorem bound_negative_excludes_seeded_winner {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : Admissible I) (s : State n)
    (c : SubmittedNegative n k) (hc : boundNegativeCheck I s c = true)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k) :
    I = c.input ∧ s = c.initial ∧
      ¬ LawfulMeasurableWinner.{uR,uZ} I hI.1 s ρ π d := by
  obtain ⟨hinput,hstate,hbody⟩ := (boundNegativeCheck_iff I s c).mp hc
  refine ⟨hinput,hstate,fun hWin => ?_⟩
  exact (negativeCheck_sound I s c.body hbody)
    ((positiveCheck_iff_region I hI s).mp (seeded_winner_has_positive I hI s ρ π d hWin))

/-- The complete negative check characterizes failure of deterministic
existence; the preceding arbitrary-seed theorem gives its stronger exclusion. -/
theorem bound_negative_iff_no_deterministic_winner (I : Input n k) (hI : Admissible I)
    (s : State n) (d : Pair n k) :
    (∃ c : SubmittedNegative n k, boundNegativeCheck I s c = true) ↔
      ¬ DeterministicWinner.{uZ} I hI.1 s d := by
  rw [boundNegativeCheck_iff_region I hI s,
    ← bound_positive_iff_deterministic_winner I hI s d,
    boundPositiveCheck_iff_region I hI s]

/-- Exactly one sign has accepted finite evidence. The positive sign includes
an actual literal deterministic winner; the negative sign excludes every lawful
measurable seeded policy, separately instantiated in any policy-seed universe. -/
theorem signed_semantic_alternatives (I : Input n k) (hI : Admissible I)
    (s : State n) (d : Pair n k) :
    ((∃ c : SubmittedPositive n k, boundPositiveCheck I s c = true) ∧
      DeterministicWinner.{uZ} I hI.1 s d ∧
      ¬ ∃ c : SubmittedNegative n k, boundNegativeCheck I s c = true) ∨
    ((∃ c : SubmittedNegative n k, boundNegativeCheck I s c = true) ∧
      ¬ DeterministicWinner.{uZ} I hI.1 s d ∧
      ¬ ∃ c : SubmittedPositive n k, boundPositiveCheck I s c = true) := by
  rcases signed_finite_alternatives I hI s with ⟨hp,hn⟩ | ⟨hn,hp⟩
  · exact Or.inl ⟨hp,(bound_positive_iff_deterministic_winner I hI s d).mp hp,hn⟩
  · exact Or.inr ⟨hn,(bound_negative_iff_no_deterministic_winner I hI s d).mp hn,hp⟩

end HiddenChange
