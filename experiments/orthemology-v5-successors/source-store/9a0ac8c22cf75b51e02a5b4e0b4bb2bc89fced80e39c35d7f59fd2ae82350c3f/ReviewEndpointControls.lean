import EndpointFixtures
import EndpointLawfulnessControls
open HiddenChange HiddenChangeEndpointTests EndpointLawfulness MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
noncomputable section
namespace EndpointIndependentReview
universe uR uZ uV
variable {n k : ℕ} [NeZero n] [NeZero k]

-- No measurable-space, countability, or standard-Borel restriction is introduced.
theorem arbitrary_seed_exclusion {R : Type uR} [MeasurableSpace R]
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R 1 1) :
    ¬ LawfulMeasurableWinner.{uR,uZ} (one 1)
      (by decide +kernel : Admissible (one 1)).1 0 ρ π (0,0) :=
  (bound_negative_excludes_seeded_winner _ (by decide +kernel) _
    oddSubmission (by decide +kernel) ρ π (0,0)).2.2

-- Both seed universes can be lifted independently, not silently fixed to zero.
theorem lifted_seed_exclusion {R : Type uR} [MeasurableSpace (ULift.{uV} R)]
    (ρ : Measure (ULift.{uV} R)) [IsProbabilityMeasure ρ]
    (π : Policy (ULift.{uV} R) 1 1) :
    ¬ LawfulMeasurableWinner.{max uR uV,uZ} (one 1)
      (by decide +kernel : Admissible (one 1)).1 0 ρ π (0,0) :=
  arbitrary_seed_exclusion ρ π

-- Universe choice does not weaken adversarial strength: both reduce to all indices.
theorem winner_universe_invariant {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n) (ρ : Measure R)
    [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k) :
    LawfulMeasurableWinner.{uR,uZ} I hI s ρ π d ↔
      LawfulMeasurableWinner.{uR,uV} I hI s ρ π d := by
  constructor
  · rintro ⟨hm,hl,hw⟩
    refine ⟨hm,hl,?_⟩
    exact (winsAll_iff_fixed_indices I hI s ρ π hm d).mpr
      ((winsAll_iff_fixed_indices I hI s ρ π hm d).mp hw)
  · rintro ⟨hm,hl,hw⟩
    refine ⟨hm,hl,?_⟩
    exact (winsAll_iff_fixed_indices I hI s ρ π hm d).mpr
      ((winsAll_iff_fixed_indices I hI s ρ π hm d).mp hw)

-- A winner supplies each independent obligation.
omit [NeZero k] in
theorem obligations_retained {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : I.Valid) (s : State n) (ρ : Measure R)
    (π : Policy R n k) (d : Pair n k)
    (hw : LawfulMeasurableWinner.{uR,uZ} I hI s ρ π d) :
    Measurable (fun z : R × PublicHistory n k => π z.1 z.2) ∧
      PolicyLawful I s π ∧ WinsAll.{uZ} I hI s ρ π d :=
  ⟨hw.1, (policyLawful_iff_allHistoryLawful I s π).mpr hw.2.1, hw.2.2⟩

-- Supplied malformed body still yields all-history lawful completion, not success.
example (I : Input n k) (hI : Admissible I) (s : State n) (c : PositiveBody n k) :
    PolicyLawful I s (compile I hI s c) :=
  (policyLawful_iff_allHistoryLawful I s _).mpr (compiled_all_history_lawful I hI s c)

-- Every metadata field is bound even when the unbound positive body still passes.
def relabelings : List (Input 1 1) :=
  [ {one 0 with interpretation := {(one 0).interpretation with modelCoding := ["new0","new1"]}},
    {one 0 with interpretation := {(one 0).interpretation with stateCoding := ["newstate"]}},
    {one 0 with interpretation := {(one 0).interpretation with actionCoding := ["newaction"]}},
    {one 0 with interpretation := {(one 0).interpretation with modelRevision := "newrevision"}},
    {one 0 with interpretation := {(one 0).interpretation with observation := "newobservation"}},
    {one 0 with interpretation := {(one 0).interpretation with occurrenceSource := "newsource"}},
    {one 0 with interpretation := {(one 0).interpretation with authority := "newauthority"}} ]
example : ∀ J ∈ relabelings, positiveCheck J 0 evenBody = true ∧
    boundPositiveCheck J 0 evenSubmission = false := by decide +kernel

-- Semantically identical raw menu encoding is deliberately still input-bound.
def supportOrder : Input 1 1 := {one 0 with menus := [⟨[1,0],0,[0]⟩]}
example : commonMenu supportOrder 0 = commonMenu (one 0) 0 := by decide +kernel
example : positiveCheck supportOrder 0 evenBody = true := by decide +kernel
example : boundPositiveCheck supportOrder 0 evenSubmission = false := by decide +kernel

-- The negative body also remains correct but is rejected for the wrong labels/initial state.
def renamedOdd : Input 1 1 :=
  {one 1 with interpretation := {(one 1).interpretation with actionCoding := ["renamed"]}}
example : negativeCheck renamedOdd 0 oddSubmission.body = true := by decide +kernel
example : boundNegativeCheck renamedOdd 0 oddSubmission = false := by decide +kernel
example : negativeCheck separator 1 separatorSubmission.body = true := by decide +kernel
example : boundNegativeCheck separator 1 separatorSubmission = false := by decide +kernel

-- Raw input binding is not merely row or support matching.
theorem positive_retains_whole_input (I : Input n k) (hI : Admissible I)
    (s : State n) (c : SubmittedPositive n k) (hc : boundPositiveCheck I s c = true)
    (d : Pair n k) : I = c.input ∧ s = c.initial := by
  have hh := bound_positive_compiled_semantics.{0} I hI s c hc d
  exact ⟨hh.1,hh.2.1⟩

-- The lawfulness bridge covers deliberately source-incoherent pair histories.
example {R : Type uR} (I : Input 2 1) (π : Policy R 2 1)
    (hl : AllHistoryLawful I 0 π) (r : R) :
    π r [(0,1),(0,0)] ∈ commonMenu I 1 := by
  have hh := (policyLawful_iff_allHistoryLawful I 0 π).mpr hl r
    [((0,0),1),((1,0),0)]
  exact hh

-- Lawfulness includes null-seed and off-policy histories, with no positivity assumption.
def nullSeedViolation : Policy Bool 1 2 := fun b _ => if b then 0 else 1
example : ¬ AllHistoryLawful forbiddenEven 0 nullSeedViolation := by
  intro h
  exact excluded_action (h false [])
def offPolicyViolation : Policy Unit 1 2 := fun _ h => if h = [(1,0)] then 1 else 0
example : offPolicyViolation () [] = 0 := by decide +kernel
example : ¬ AllHistoryLawful forbiddenEven 0 offPolicyViolation := by
  intro h
  exact excluded_action (h () [(1,0)])
example : ¬ PolicyLawful forbiddenEven 0 offPolicyViolation := by
  intro h
  have hh := h () [((0,1),0)]
  exact excluded_action hh

-- Explicit measurable-space adversary: discrete action readout of a coarse seed.
def CoarseSeed := Bool
instance : MeasurableSpace CoarseSeed := ⊥
instance : DecidableEq CoarseSeed := inferInstanceAs (DecidableEq Bool)
def coarsePolicy : Policy CoarseSeed 1 2 := fun b _ => if b = true then 1 else 0

theorem coarse_nonmeasurable :
    ¬ Measurable (fun z : CoarseSeed × PublicHistory 1 2 => coarsePolicy z.1 z.2) := by
  intro hm
  have hg : Measurable (fun b : CoarseSeed => (b, ([] : PublicHistory 1 2))) :=
    measurable_id.prodMk measurable_const
  have hm' : Measurable (fun b : CoarseSeed => coarsePolicy b []) := hm.comp hg
  have hs := hm' (measurableSet_singleton (1 : Action 2))
  change MeasurableSet[⊥] _ at hs
  rcases MeasurableSpace.measurableSet_bot_iff.mp hs with he | he
  · have ht : (true : CoarseSeed) ∈ (fun b : CoarseSeed => coarsePolicy b []) ⁻¹' {1} := by
      change coarsePolicy true [] = 1
      simp [coarsePolicy]
    rw [he] at ht
    exact ht
  · have ht : (false : CoarseSeed) ∈ (fun b : CoarseSeed => coarsePolicy b []) ⁻¹' {1} := by
      rw [he]
      trivial
    have hn : (false : CoarseSeed) ∉ (fun b : CoarseSeed => coarsePolicy b []) ⁻¹' {1} := by
      change coarsePolicy false [] ≠ 1
      simp [coarsePolicy, CoarseSeed]
    exact hn ht

theorem coarse_policy_not_winner (I : Input 1 2) (hI : I.Valid)
    (ρ : Measure CoarseSeed) :
    ¬ LawfulMeasurableWinner.{0,uZ} I hI 0 ρ coarsePolicy (0,0) := by
  intro hw
  exact coarse_nonmeasurable hw.1

-- An actual parity-only winner is nevertheless excluded for lack of permission.
example : WinsAll.{uZ} forbiddenEven
    (by decide +kernel : Admissible forbiddenEven).1 0 (Measure.dirac ()) choosesForbidden (0,0) :=
  forbidden_winsAll
example : ¬ DeterministicWinner.{uZ} forbiddenEven
    (by decide +kernel : Admissible forbiddenEven).1 0 (0,0) := by
  rw [← positive_iff_deterministic_winner _ (by decide +kernel) _ _]
  exact forbidden_no_body

#print axioms arbitrary_seed_exclusion
#print axioms lifted_seed_exclusion
#print axioms winner_universe_invariant
#print axioms obligations_retained
#print axioms positive_retains_whole_input
#print axioms coarse_nonmeasurable
#print axioms coarse_policy_not_winner

-- With the two independent obligations supplied, the negative sign refutes parity itself.
theorem negative_rules_out_all_adversary_parity {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : Admissible I) (s : State n)
    (c : SubmittedNegative n k) (hc : boundNegativeCheck I s c = true)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k)
    (hm : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hl : AllHistoryLawful I s π) : ¬ WinsAll.{uZ} I hI.1 s ρ π d := by
  intro hw
  exact (bound_negative_excludes_seeded_winner I hI s c hc ρ π d).2.2 ⟨hm,hl,hw⟩

-- Any permitted randomized winner yields deterministic existence for the same input/state.
theorem randomized_implies_deterministic {R : Type uR} [MeasurableSpace R]
    (I : Input n k) (hI : Admissible I) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k) (d : Pair n k)
    (hw : LawfulMeasurableWinner.{uR,uZ} I hI.1 s ρ π d) :
    DeterministicWinner.{uZ} I hI.1 s d :=
  (bound_positive_iff_deterministic_winner I hI s d).mp
    (seeded_winner_has_bound_positive I hI s ρ π d hw)

-- Neither the dummy history readout pair nor adversary-universe choice alters existence.
theorem deterministic_existence_invariant (I : Input n k) (hI : Admissible I)
    (s : State n) (d d' : Pair n k) :
    DeterministicWinner.{uZ} I hI.1 s d ↔ DeterministicWinner.{uV} I hI.1 s d' := by
  rw [← positive_iff_deterministic_winner I hI s d,
    ← positive_iff_deterministic_winner I hI s d']

#print axioms negative_rules_out_all_adversary_parity
#print axioms randomized_implies_deterministic
#print axioms deterministic_existence_invariant
end EndpointIndependentReview
