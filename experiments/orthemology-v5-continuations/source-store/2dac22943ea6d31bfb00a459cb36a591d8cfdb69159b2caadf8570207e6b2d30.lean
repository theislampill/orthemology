import SmoothRigidity

noncomputable section
open scoped Topology BigOperators
open Set Filter SmoothRigidity

namespace GeneratorRigidity
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

lemma vertex_sum (i : ι) : ∑ j, (vertex i : Vec ι) j = 1 := by
  simp [vertex, Pi.single_apply]

lemma tangent_sum_zero (p x : Vec ι) (hp : ∑ i, p i = 1)
    (hx : x ∈ Submodule.span ℝ (Set.range (fun i => p - vertex i))) : ∑ i, x i = 0 := by
  induction hx using Submodule.span_induction with
  | mem x hx =>
      obtain ⟨i, rfl⟩ := hx
      simp only [Pi.sub_apply, Finset.sum_sub_distrib, hp, vertex_sum, sub_self]
  | zero => simp
  | add x y hx hy hxe hye => simpa only [Pi.add_apply, Finset.sum_add_distrib, hxe, hye, add_zero]
  | smul a x hx hxe => simp only [Pi.smul_apply, smul_eq_mul, ← Finset.mul_sum, hxe, mul_zero]

lemma vertex_transverse (p : Vec ι) (hp : ∑ i, p i = 1) (i : ι) :
    vertex i ∉ Submodule.span ℝ (Set.range (fun j => p - vertex j)) := by
  intro hmem
  have hz := tangent_sum_zero p (vertex i) hp hmem
  rw [vertex_sum] at hz
  norm_num at hz

lemma vertex_difference_tangent (p : Vec ι) (i j : ι) :
    vertex i - vertex j ∈ Submodule.span ℝ (Set.range (fun k => p - vertex k)) := by
  have hm := Submodule.sub_mem (Submodule.span ℝ (Set.range (fun k => p - vertex k)))
    (Submodule.subset_span (Set.mem_range_self j)) (Submodule.subset_span (Set.mem_range_self i))
  convert hm using 1 <;> abel

lemma hessian_vertex (s : ι → SmoothScalar.Score) (p u : Vec ι) (i : ι) :
    hessian s p u (vertex i) = (s i).ddf (p i) * u i := by
  rw [hessian_apply]
  simp [vertex, Pi.single_apply]

lemma positive_normal_proportional (a b u : ι → ℝ)
    (ha : ∀ i, 0 < a i) (hb : ∀ i, 0 < b i) (hu : u ≠ 0)
    (hA : ∀ i j, a i * u i = a j * u j)
    (hB : ∀ i j, b i * u i = b j * u j) :
    ∃ r > 0, ∀ i, a i = r * b i := by
  have hex : ∃ i, u i ≠ 0 := by
    by_contra! hn
    apply hu
    funext i
    exact hn i
  obtain ⟨j, hj⟩ := hex
  refine ⟨a j / b j, div_pos (ha j) (hb j), ?_⟩
  intro i
  have hui : u i ≠ 0 := by
    intro hzero
    have he := hA i j
    rw [hzero, mul_zero] at he
    exact (mul_ne_zero (ne_of_gt (ha j)) hj) he.symm
  have h1 := congrArg (fun x : ℝ => x * b j) (hA i j)
  have h2 := congrArg (fun x : ℝ => x * a j) (hB i j)
  have hm : (a i * b j - a j * b i) * u i = 0 := by
    dsimp at h1 h2
    nlinarith
  have hcross : a i * b j = a j * b i :=
    sub_eq_zero.mp ((mul_eq_zero.mp hm).resolve_right hui)
  field_simp [ne_of_gt (hb j)]
  nlinarith

/-- Actual common repairs force proportional diagonal Hessians at each tested p. -/
theorem common_repairs_hessians_proportional
    (s t : ι → SmoothScalar.Score) (i0 : ι) (p : Vec ι)
    (hp : ∀ i, p i ∈ Ioo 0 1) (hsum : ∑ i, p i = 1)
    (e : ℕ → ℝ) (c : ℕ → Vec ι)
    (hepos : ∀ n, 0 < e n) (he : Tendsto e atTop (𝓝 0))
    (hc : ∀ n i, c n i ∈ Ioo 0 1) (hcsum : ∀ n, ∑ i, c n i = 1)
    (hsgain : ∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0))
    (htgain : ∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0)) :
    ∃ r > 0, ∀ i, (s i).ddf (p i) = r * (t i).ddf (p i) := by
  let fam : Bool → ι → SmoothScalar.Score := fun k => if k then t else s
  have hboth : ∀ n k i, totalDiv (fam k) (vertex i) (c n) ≤
      totalDiv (fam k) (vertex i) (p + e n • vertex i0) := by
    intro n k i
    cases k
    · exact hsgain n i
    · exact htgain n i
  obtain ⟨z, hz, hnormal⟩ := smooth_common_repair_hessian_necessary fam false p (vertex i0)
    hp hsum e c hepos he hc hcsum hboth
  let u := vertex i0 - z
  have hu : u ≠ 0 := by
    intro hzero
    have heq : vertex i0 = z := sub_eq_zero.mp hzero
    exact vertex_transverse p hsum i0 (heq ▸ hz)
  apply positive_normal_proportional (fun i => (s i).ddf (p i))
    (fun i => (t i).ddf (p i)) u (fun i => (s i).positive (p i) (hp i))
    (fun i => (t i).positive (p i) (hp i)) hu
  · intro i j
    have hn := hnormal false (vertex i - vertex j) (vertex_difference_tangent p i j)
    change hessian s p u (vertex i - vertex j) = 0 at hn
    rw [map_sub, hessian_vertex, hessian_vertex] at hn
    exact sub_eq_zero.mp hn
  · intro i j
    have hn := hnormal true (vertex i - vertex j) (vertex_difference_tangent p i j)
    change hessian t p u (vertex i - vertex j) = 0 at hn
    rw [map_sub, hessian_vertex, hessian_vertex] at hn
    exact sub_eq_zero.mp hn



/-- Three or more genuine outcomes let any two positive subunit coordinates
coexist in an interior probability vector. -/
lemma fill_two_coordinates (hcard : 3 ≤ Fintype.card ι)
    (i j : ι) (hij : i ≠ j) (x y : ℝ) (hx : 0 < x) (hy : 0 < y) (hxy : x + y < 1) :
    ∃ p : Vec ι, (∀ k, p k ∈ Ioo 0 1) ∧ (∑ k, p k = 1) ∧ p i = x ∧ p j = y := by
  let N : ℝ := Fintype.card ι
  have hN : 3 ≤ N := by dsimp [N]; exact_mod_cast hcard
  have hden : 0 < N - 2 := by linarith
  let d : ℝ := (1 - x - y) / (N - 2)
  have hdpos : 0 < d := div_pos (by linarith) hden
  have hdlt : d < 1 := (div_lt_iff₀ hden).mpr (by linarith)
  let p : Vec ι := x • vertex i + y • vertex j + d • ((fun _ => 1) - vertex i - vertex j)
  have hpi : p i = x := by simp [p, vertex, Pi.single_apply, hij, hij.symm]
  have hpj : p j = y := by simp [p, vertex, Pi.single_apply, hij, hij.symm]
  refine ⟨p, ?_, ?_, hpi, hpj⟩
  · intro k
    by_cases hki : k = i
    · subst k
      rw [hpi]
      exact ⟨hx, by linarith⟩
    by_cases hkj : k = j
    · subst k
      rw [hpj]
      exact ⟨hy, by linarith⟩
    have hpk : p k = d := by simp [p, vertex, Pi.single_apply, hki, hkj, Ne.symm hki, Ne.symm hkj]
    rw [hpk]
    exact ⟨hdpos, hdlt⟩
  · dsimp [p]
    simp only [Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul,
      Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, vertex_sum,
      Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one]
    dsimp [d, N]
    field_simp
    ring

lemma simplex_ratio_connectivity (hcard : 3 ≤ Fintype.card ι) (r : ι → ℝ → ℝ)
    (hcompat : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∀ i j, r i (p i) = r j (p j)) :
    ∃ a : ℝ, ∀ i x, x ∈ Ioo 0 1 → r i x = a := by
  haveI : Nontrivial ι := Fintype.one_lt_card_iff_nontrivial.mp (by omega)
  have hconst : ∀ i x y, x ∈ Ioo 0 1 → y ∈ Ioo 0 1 → r i x = r i y := by
    intro i x y hx hy
    obtain ⟨j, hji⟩ := exists_ne i
    let u := min (1 - x) (1 - y) / 2
    have hup : 0 < u := half_pos (lt_min (sub_pos.mpr hx.2) (sub_pos.mpr hy.2))
    have hux : x + u < 1 := by
      have hm := min_le_left (1 - x) (1 - y)
      dsimp [u]
      linarith [hx.2]
    have huy : y + u < 1 := by
      have hm := min_le_right (1 - x) (1 - y)
      dsimp [u]
      linarith [hy.2]
    obtain ⟨p, hp, hpsum, hpx, hpu⟩ := fill_two_coordinates hcard i j hji.symm x u hx.1 hup hux
    obtain ⟨q, hq, hqsum, hqy, hqu⟩ := fill_two_coordinates hcard i j hji.symm y u hy.1 hup huy
    have h1 := hcompat p hp hpsum i j
    have h2 := hcompat q hq hqsum i j
    rw [hpx, hpu] at h1
    rw [hqy, hqu] at h2
    exact h1.trans h2.symm
  let i0 : ι := Classical.arbitrary ι
  let N : ℝ := Fintype.card ι
  have hN : 3 ≤ N := by dsimp [N]; exact_mod_cast hcard
  have hNp : 0 < N := by linarith
  let p : Vec ι := fun _ => 1 / N
  have hp : ∀ i, p i ∈ Ioo 0 1 := by
    intro i
    exact ⟨one_div_pos.mpr hNp, (div_lt_iff₀ hNp).mpr (by linarith)⟩
  have hpsum : ∑ i, p i = 1 := by
    simp only [p, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    dsimp [N] at *
    field_simp
  refine ⟨r i0 (1 / N), ?_⟩
  intro i x hx
  exact (hconst i x (1 / N) hx (hp i)).trans (hcompat p hp hpsum i i0)



lemma generators_affine_of_hessian_eq (s t : SmoothScalar.Score) (a : ℝ)
    (hdd : ∀ x ∈ Ioo 0 1, s.ddf x = a * t.ddf x) :
    ∃ b c : ℝ, ∀ x ∈ Icc 0 1, s.f x = a * t.f x + b * x + c := by
  have hsd : DifferentiableOn ℝ s.df (Ioo 0 1) :=
    fun x hx => (s.second x hx).differentiableAt.differentiableWithinAt
  have htd : DifferentiableOn ℝ (fun x => a * t.df x) (Ioo 0 1) :=
    fun x hx => ((t.second x hx).const_mul a).differentiableAt.differentiableWithinAt
  have hdeq : EqOn (deriv s.df) (deriv (fun x => a * t.df x)) (Ioo 0 1) := by
    intro x hx
    rw [(s.second x hx).deriv, ((t.second x hx).const_mul a).deriv]
    exact hdd x hx
  obtain ⟨b, hb⟩ := isOpen_Ioo.exists_eq_add_of_deriv_eq isPreconnected_Ioo hsd htd hdeq
  have hsf : DifferentiableOn ℝ s.f (Ioo 0 1) :=
    fun x hx => (s.deriv x hx).differentiableAt.differentiableWithinAt
  have htfder : ∀ x ∈ Ioo 0 1,
      HasDerivAt (fun x => a * t.f x + b * x) (a * t.df x + b) x := by
    intro x hx
    simpa using ((t.deriv x hx).const_mul a).add ((hasDerivAt_id x).const_mul b)
  have htf : DifferentiableOn ℝ (fun x => a * t.f x + b * x) (Ioo 0 1) :=
    fun x hx => (htfder x hx).differentiableAt.differentiableWithinAt
  have hfeq : EqOn (deriv s.f) (deriv (fun x => a * t.f x + b * x)) (Ioo 0 1) := by
    intro x hx
    rw [(s.deriv x hx).deriv, (htfder x hx).deriv]
    exact hb hx
  obtain ⟨c, hc⟩ := isOpen_Ioo.exists_eq_add_of_deriv_eq isPreconnected_Ioo hsf htf hfeq
  refine ⟨b, c, ?_⟩
  apply hc.of_subset_closure s.cont
  · exact ((continuousOn_const.mul t.cont).add (continuousOn_const.mul continuousOn_id)).add continuousOn_const
  · exact fun x hx => ⟨hx.1.le, hx.2.le⟩
  · rw [closure_Ioo (by norm_num : (0 : ℝ) ≠ 1)]

/-- Load-bearing necessity of S2 for every finite number of outcomes >= 3.
The premise is existence of actual common coherent Bregman repairs near EVERY
interior probability vector; no Hessian compatibility premise is assumed. -/
theorem universal_common_repairs_force_affine
    (hcard : 3 ≤ Fintype.card ι) (s t : ι → SmoothScalar.Score) (i0 : ι)
    (hcommon : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∃ (e : ℕ → ℝ) (c : ℕ → Vec ι),
        (∀ n, 0 < e n) ∧ Tendsto e atTop (𝓝 0) ∧
        (∀ n i, c n i ∈ Ioo 0 1) ∧ (∀ n, ∑ i, c n i = 1) ∧
        (∀ n i, totalDiv s (vertex i) (c n) ≤ totalDiv s (vertex i) (p + e n • vertex i0)) ∧
        (∀ n i, totalDiv t (vertex i) (c n) ≤ totalDiv t (vertex i) (p + e n • vertex i0))) :
    ∃ a > 0, ∃ b d : ι → ℝ, ∀ i x, x ∈ Icc 0 1 →
      (s i).f x = a * (t i).f x + b i * x + d i := by
  let r : ι → ℝ → ℝ := fun i x => (s i).ddf x / (t i).ddf x
  have hcompat : ∀ p : Vec ι, (∀ i, p i ∈ Ioo 0 1) → (∑ i, p i = 1) →
      ∀ i j, r i (p i) = r j (p j) := by
    intro p hp hsum i j
    obtain ⟨e, c, hepos, helim, hc, hcsum, hs, ht⟩ := hcommon p hp hsum
    obtain ⟨a, ha, haa⟩ := common_repairs_hessians_proportional s t i0 p hp hsum e c
      hepos helim hc hcsum hs ht
    dsimp [r]
    rw [haa i, haa j]
    field_simp [ne_of_gt ((t i).positive (p i) (hp i)), ne_of_gt ((t j).positive (p j) (hp j))]
  obtain ⟨a, ha⟩ := simplex_ratio_connectivity hcard r hcompat
  have hmid : (1 : ℝ) / 2 ∈ Ioo 0 1 := by constructor <;> norm_num
  have hapos : 0 < a := by
    have hm : 0 < r i0 ((1 : ℝ) / 2) :=
      div_pos ((s i0).positive _ hmid) ((t i0).positive _ hmid)
    rw [ha i0 ((1 : ℝ) / 2) hmid] at hm
    exact hm
  have hdd : ∀ i x, x ∈ Ioo 0 1 → (s i).ddf x = a * (t i).ddf x := by
    intro i x hx
    exact (div_eq_iff (ne_of_gt ((t i).positive x hx))).mp (ha i x hx)
  choose b d hbd using fun i => generators_affine_of_hessian_eq (s i) (t i) a (hdd i)
  exact ⟨a, hapos, b, d, hbd⟩

#print axioms generators_affine_of_hessian_eq
#print axioms universal_common_repairs_force_affine
#check universal_common_repairs_force_affine
end GeneratorRigidity
