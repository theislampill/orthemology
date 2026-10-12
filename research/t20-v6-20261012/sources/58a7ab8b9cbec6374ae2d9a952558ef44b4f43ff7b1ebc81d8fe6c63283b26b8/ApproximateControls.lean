import ApproximateRepairIdentification
open MeasureTheory Set Filter
open scoped Topology
namespace ApproximateAudit
open Orthemology.Tranche2 Orthemology.Tranche2.FiniteQuery

theorem zero_tolerance_exact (a e q : ℝ) :
    BinaryApproxGood a e 0 q ↔ BinaryGood a e q := by
  simp [BinaryApproxGood,BinaryGood]

theorem no_query_linear_tolerance_all_norms
    (e : ℕ → ℝ) (he : ∀ n, 0 ≤ e n) (o : Oracle)
    (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    ∀ᶠ n in atTop,
      (fun _ : Unit => false) (run (fun _ => false) (fun s _ => s) o () n).1 = false ∧
      BinaryApproxGood a (e n) (e n) (1/2) :=
  Eventually.of_forall (fun n => ⟨rfl,no_information_linear_tolerance a (e n) ha0 ha1 (he n)⟩)

theorem linear_ratio_not_vanishing (e : ℕ → ℝ) (he : ∀ n, 0 < e n) :
    ¬ Tendsto (fun n => e n/e n) atTop (𝓝 0) := by
  intro h
  have heq : (fun n => e n/e n) = (fun _ => (1:ℝ)) :=
    funext fun n => div_self (ne_of_gt (he n))
  rw [heq] at h
  have hf : (1:ℝ)=0 := tendsto_nhds_unique tendsto_const_nhds h
  norm_num at hf

-- Nonnegative tolerance may admit incoherent outputs. The no-go is stronger
-- because it permits all real outputs; coherence of approximate repairs is not assumed.
theorem large_tolerance_does_not_enforce_coherence :
    BinaryApproxGood (1/2) (1/4) 4 (-1) ∧ ¬ (0 ≤ (-1:ℝ) ∧ (-1:ℝ) ≤ 1) := by
  norm_num [BinaryApproxGood]

-- Exact main type: common domination, rather than identical marginals;
-- arbitrary input measures are allowed, so probability prose is an instantiation.
example {S : Type*} [MeasurableSpace S]
    (ask : S → Bool) (next : S → Bool → S)
    (ha : Measurable ask) (hn : ∀ b, Measurable (fun s => next s b))
    (ρ : Measure S) [IsProbabilityMeasure ρ]
    (inputLaw : ℝ → Measure (S × Oracle))
    (hseed : ∀ a, (inputLaw a).map Prod.fst ≪ ρ)
    (e eta : ℕ → ℝ) (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (heta : ∀ n, 0 ≤ eta n) (he : Tendsto e atTop (𝓝 0))
    (hratio : Tendsto (fun n => eta n/e n) atTop (𝓝 0))
    (score : ℕ → S → ℝ) (hscore : ∀ n, Measurable (score n)) :
    Set.Countable {a : ℝ | a ∈ Icc 0 1 ∧
      0 < inputLaw a {z | ∀ᶠ n in atTop,
        ask (run ask next z.2 z.1 n).1 = false ∧
        BinaryApproxGood a (e n) (eta n) (score n (run ask next z.2 z.1 n).1)}} :=
  countable_positive_approximate_causal_restoration ask next ha hn ρ inputLaw hseed e eta he0 he1 heta he hratio score hscore
end ApproximateAudit
#print axioms ApproximateAudit.zero_tolerance_exact
#print axioms ApproximateAudit.no_query_linear_tolerance_all_norms
#print axioms ApproximateAudit.linear_ratio_not_vanishing
#print axioms ApproximateAudit.large_tolerance_does_not_enforce_coherence
