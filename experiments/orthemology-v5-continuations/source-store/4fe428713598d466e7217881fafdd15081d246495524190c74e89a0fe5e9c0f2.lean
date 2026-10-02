import FiniteAuditRepair

noncomputable section
open MeasureTheory ProbabilityTheory Finset Filter
open scoped BigOperators
namespace Orthemology.Tranche3.FiniteAuditRepair
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding

/-- Deliberately broken source/standard coupling: both hidden standards produce
the same fair audit bits while their literal score targets remain different. -/
def uninformativeKernel (_ _ _ : Bool) : ℝ := 1/2
lemma uninformative_nonneg : ∀ θ a y, 0 ≤ uninformativeKernel θ a y := by intros; norm_num [uninformativeKernel]
lemma uninformative_normalized : ∀ θ a, ∑ y, uninformativeKernel θ a y = 1 := by
  intros; norm_num [uninformativeKernel,Fintype.sum_bool]

lemma uninformative_support_stays (B : Finset Bool) (a y : Bool) :
    supportUpdate uninformativeKernel B a y = B := by
  ext θ
  simp [supportUpdate,uninformativeKernel]

/-- Erasing the informative source/score coupling destroys the certificate.
Literal repair targets are not enough to identify the hidden standard. -/
theorem uninformative_not_winning :
    ¬ RecursiveWinning uninformativeKernel literalGood publicMenu Finset.univ := by
  intro hw
  obtain ⟨acts,hne,_,_,hcert⟩ := recursiveWinning_witness uninformativeKernel literalGood publicMenu hw false (by simp)
  obtain ⟨a,ha⟩ := List.exists_mem_of_ne_nil acts hne
  rcases hcert with hp | hs
  · obtain ⟨b,hb,y,hy,_⟩ := hp
    exact (supportStay_false uninformativeKernel Finset.univ b y).mp hy
      (uninformative_support_stays Finset.univ b y)
  · have h0 := hs.1 (List.mem_toFinset.mpr ha)
    have h1 := hs.2 true (by simp) (fun _ _ => rfl) (List.mem_toFinset.mpr ha)
    simp only [literalGood_exact,Finset.mem_singleton] at h0 h1
    exact Bool.false_ne_true (h0.symm.trans h1)

/-- Under uninformative receipts no common measurable causal policy can repair
both literal standards almost surely, despite each target being individually feasible. -/
theorem uninformative_no_shared_policy
    {R : Type*} [MeasurableSpace R] (ρ : Measure R) [IsProbabilityMeasure ρ] :
    ¬ ∃ π : R → History Bool Bool → Bool,
      Measurable (fun z : R × History Bool Bool => π z.1 z.2) ∧
      (∀ r h, ActionCompatible π r h → (historySupport uninformativeKernel Finset.univ h).Nonempty →
        π r h ∈ publicMenu (historySupport uninformativeKernel Finset.univ h)) ∧
      ∀ θ ∈ (Finset.univ : Finset Bool),
        ∀ᵐ x ∂actionLaw π ρ (uninformativeKernel θ) (uninformative_nonneg θ) (uninformative_normalized θ) false,
          ∀ᶠ n in atTop, x n ∈ literalGood θ := by
  rw [seeded_policy_exists_iff_recursiveWinning uninformativeKernel literalGood publicMenu
    uninformative_nonneg uninformative_normalized Finset.univ (by simp) ρ false]
  exact uninformative_not_winning
end Orthemology.Tranche3.FiniteAuditRepair
