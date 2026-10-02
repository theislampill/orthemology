import NudgeRigidity

/-! Coherent-endpoint-directed nudges, explicitly separate from the frozen
ambient-direction premise in NudgeRigidity. -/
noncomputable section
open scoped Topology BigOperators
open Filter Set SmoothRigidity GeneratorRigidity NudgeRigidity

namespace CoherentNudgeRigidity
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def CommonCoherentLocalNudges (s t : ι → SmoothScalar.Score) (i0 : ι) : Prop :=
  ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
    ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, (p + e n • vertex i0) i ∈ Ioo 0 1) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, hessian s (p + e n • vertex i0) (p + e n • vertex i0 - vertex i)
        (c n - (p + e n • vertex i0)) < 0) ∧
      (∀ n i, hessian t (p + e n • vertex i0) (p + e n • vertex i0 - vertex i)
        (c n - (p + e n • vertex i0)) < 0)

lemma coherent_nudges_are_ambient (s t : ι → SmoothScalar.Score) (i0 : ι)
    (hc : CommonCoherentLocalNudges s t i0) : CommonLocalNudges s t i0 := by
  intro p hp hsum
  obtain ⟨e, c, hep, hel, hbi, hci, hcs, hs, ht⟩ := hc p hp hsum
  exact ⟨e, (fun n => c n - (p + e n • vertex i0)), hep, hel, hbi, hs, ht⟩

lemma single_score_coherent_nudges (s : ι → SmoothScalar.Score) (i0 : ι) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1) :
    ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
      (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
      (∀ n i, (p + e n • vertex i0) i ∈ Ioo 0 1) ∧
      (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
      (∀ n i, hessian s (p + e n • vertex i0) (p + e n • vertex i0 - vertex i)
        (c n - (p + e n • vertex i0)) < 0) := by
  obtain ⟨e, q, hepos, helim, hbint, hqint, hqsum, hqgain⟩ :=
    BregmanProjection.single_score_local_repairs s p (vertex i0) hp hsum
  let base : ℕ → Vec ι := fun n => p + e n • vertex i0
  let A : ℕ → ι → ℝ := fun n i => ((s i).ddf (base n i))⁻¹
  let S : ℕ → ℝ := fun n => ∑ i, A n i
  let Sp : ℝ := ∑ i, ((s i).ddf (p i))⁻¹
  have hApos : ∀ n i, 0 < A n i := fun n i => inv_pos.mpr ((s i).positive _ (hbint n i))
  have hSpos : ∀ n, 0 < S n := by
    intro n
    exact Finset.sum_pos' (fun i _ => (hApos n i).le) ⟨i0, Finset.mem_univ i0, hApos n i0⟩
  have hSppos : 0 < Sp := by
    exact Finset.sum_pos' (fun i _ => (inv_pos.mpr ((s i).positive _ (hp i))).le)
      ⟨i0, Finset.mem_univ i0, inv_pos.mpr ((s i0).positive _ (hp i0))⟩
  have hbase : Tendsto base atTop (𝓝 p) := by
    simpa [base] using
      (tendsto_const_nhds : Tendsto (fun _ : ℕ => p) atTop (𝓝 p)).add
        (helim.smul (tendsto_const_nhds : Tendsto (fun _ : ℕ => vertex i0) atTop (𝓝 (vertex i0))))
  have hAt : ∀ i, Tendsto (fun n => A n i) atTop (𝓝 (((s i).ddf (p i))⁻¹)) := by
    intro i
    have ht := ((s i).cont_second.continuousAt (Ioo_mem_nhds (hp i).1 (hp i).2)).tendsto.comp
      ((tendsto_pi_nhds.mp hbase) i)
    exact ht.inv₀ (ne_of_gt ((s i).positive _ (hp i)))
  have hSt : Tendsto S atTop (𝓝 Sp) := tendsto_finset_sum _ (fun i _ => hAt i)
  let c : ℕ → Vec ι := fun n i => base n i - e n * A n i / S n
  have hct : Tendsto c atTop (𝓝 p) := by
    apply tendsto_pi_nhds.mpr
    intro i
    have hh := ((tendsto_pi_nhds.mp hbase) i).sub
      ((helim.mul (hAt i)).div hSt (ne_of_gt hSppos))
    simpa [c] using hh
  have hcsum : ∀ n, ∑ i, c n i = 1 := by
    intro n
    have hbsum : ∑ i, base n i = 1 + e n := by
      simp only [base, Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_add_distrib,
        ← Finset.mul_sum, hsum, vertex_sum, mul_one]
    simp only [c, Finset.sum_sub_distrib, ← Finset.sum_div, ← Finset.mul_sum, hbsum]
    change 1 + e n - e n * S n / S n = 1
    field_simp [ne_of_gt (hSpos n)]
  have hdiff : ∀ n, c n - base n = (S n)⁻¹ •
      (fun i => (1 - ∑ k, base n k) / (s i).ddf (base n i)) := by
    intro n
    have hbsum : ∑ i, base n i = 1 + e n := by
      simp only [base, Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_add_distrib,
        ← Finset.mul_sum, hsum, vertex_sum, mul_one]
    ext i
    simp only [c, A, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, hbsum]
    ring
  have hgain : ∀ n i, hessian s (base n) (base n - vertex i) (c n - base n) < 0 := by
    intro n i
    rw [hdiff, map_smul, smul_eq_mul, canonical_nudge_gain s (base n) (hbint n)]
    have hbsum : ∑ i, base n i = 1 + e n := by
      simp only [base, Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_add_distrib,
        ← Finset.mul_sum, hsum, vertex_sum, mul_one]
    rw [hbsum]
    apply mul_neg_of_pos_of_neg (inv_pos.mpr (hSpos n))
    have hh := sq_pos_of_pos (hepos n)
    nlinarith
  have hcint : ∀ᶠ n in atTop, ∀ i, c n i ∈ Ioo 0 1 := by
    apply Filter.eventually_all.mpr
    intro i
    exact ((tendsto_pi_nhds.mp hct) i).eventually (Ioo_mem_nhds (hp i).1 (hp i).2)
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.mp hcint
  refine ⟨(fun n => e (n+N)), (fun n => c (n+N)), (fun n => hepos (n+N)),
    (tendsto_add_atTop_iff_nat N).mpr helim, (fun n i => hbint (n+N) i),
    (fun n i => hN (n+N) (Nat.le_add_left N n) i), (fun n => hcsum (n+N)), ?_⟩
  intro n i
  exact hgain (n+N) i


theorem universal_coherent_nudge_iff_affine (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonCoherentLocalNudges s t i0 ↔ BregmanProjection.PositiveAffineEquivalent s t := by
  constructor
  · intro hn
    exact (universal_local_nudge_iff_affine hcard s t i0).mp (coherent_nudges_are_ambient s t i0 hn)
  · rintro ⟨a, ha, f, g, hfg⟩
    intro p hp hpsum
    obtain ⟨e, c, hepos, helim, hbint, hcint, hcsum, ht⟩ := single_score_coherent_nudges t i0 p hp hpsum
    refine ⟨e, c, hepos, helim, hbint, hcint, hcsum, ?_, ht⟩
    intro n i
    rw [affine_hessian_direction s t a f g hfg _ _ _ (hbint n)]
    exact mul_neg_of_pos_of_neg ha (ht n i)

/-- Endpoint-directed nudging and actual dominating endpoints have the same
universal fixed-generator class. No pointwise equivalence is claimed. -/
theorem universal_coherent_nudge_iff_common_repair (hcard : 3 ≤ Fintype.card ι)
    (s t : ι → SmoothScalar.Score) (i0 : ι) :
    CommonCoherentLocalNudges s t i0 ↔ BregmanProjection.CommonLocalRepairs s t i0 :=
  (universal_coherent_nudge_iff_affine hcard s t i0).trans
    (BregmanProjection.universal_common_repair_iff_affine hcard s t i0).symm

#print CommonCoherentLocalNudges
#print axioms single_score_coherent_nudges
#print axioms universal_coherent_nudge_iff_affine
#print axioms universal_coherent_nudge_iff_common_repair
#check universal_coherent_nudge_iff_affine
#check universal_coherent_nudge_iff_common_repair
end CoherentNudgeRigidity

