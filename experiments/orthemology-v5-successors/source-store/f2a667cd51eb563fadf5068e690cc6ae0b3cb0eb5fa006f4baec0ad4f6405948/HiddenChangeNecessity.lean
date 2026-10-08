import HiddenChangeUncertainProgress
import HiddenChangeFixedIndex

/-! Arbitrary measurable private-seed necessity for one hidden irreversible
change. Finite region witnesses are constructed from this single original
policy's actual positive prefixes. The conclusion is a data-only positive body.
No controller sufficiency or full semantic equivalence is asserted here. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

/-- Every one original lawful measurable private-seed policy winning all actual
fixed-index laws has an accepted finite positive body. Safe regions, fairness,
recurrent components, and law transfer are derived, not supplied as premises. -/
theorem winning_policy_has_positive_body (I : Input n k) (hI : Admissible I)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : PolicyLawful I s π) (d : Pair n k)
    (hWin : ∀ κ, ∀ᵐ H ∂fixedLaw I hI.1 κ s ρ π, TaggedParity I d H) :
    ∃ body : PositiveBody n k, positiveCheck I s body = true := by
  let K := policyKnownRegion I hI.1 s ρ π
  let W := policyUncertainRegion I hI.1 s ρ π
  have hKpost : K ⊆ F1 I K := policyKnownRegion_postfixed I hI.1 s ρ π hπ hLaw d
    (fun N => hWin (some N))
  have hWpost : W ⊆ F I K W := policyUncertainRegion_postfixed I hI.1 s ρ π hπ hLaw d hWin
  have hK : K ⊆ knownRegion I := knownRegion_greatest I K hKpost
  have hW : W ⊆ uncertainRegion I := uncertainRegion_greatest I W
    (hWpost.trans (F_mono_both I hK (Finset.Subset.refl W)))
  exact (positiveCheck_iff_region I hI s).mpr
    (hW (initial_mem_policyUncertainRegion I hI.1 s ρ π hπ))

universe uZ
/-- Original all-adversary necessity. Measurability and common-menu lawfulness
remain separate explicit obligations; WinsAll itself expresses only parity. -/
theorem all_adversary_winner_has_positive_body [NeZero k]
    (I : Input n k) (hI : Admissible I)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : PolicyLawful I s π) (d : Pair n k)
    (hWin : WinsAll.{uZ} I hI.1 s ρ π d) :
    ∃ body : PositiveBody n k, positiveCheck I s body = true :=
  winning_policy_has_positive_body I hI s ρ π hπ hLaw d
    ((winsAll_iff_fixed_indices I hI.1 s ρ π hπ d).mp hWin)

/-- Computed exclusion rules out any original lawful measurable seeded winner
in the supplied arbitrary seed space. This is necessity, not controller soundness. -/
theorem computed_exclusion_forbids_winner (I : Input n k) (hI : Admissible I)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k) (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hLaw : PolicyLawful I s π) (d : Pair n k) (hLose : s ∉ uncertainRegion I) :
    ¬ ∀ κ, ∀ᵐ H ∂fixedLaw I hI.1 κ s ρ π, TaggedParity I d H := by
  intro hWin
  exact hLose ((positiveCheck_iff_region I hI s).mp
    (winning_policy_has_positive_body I hI s ρ π hπ hLaw d hWin))

end HiddenChange
