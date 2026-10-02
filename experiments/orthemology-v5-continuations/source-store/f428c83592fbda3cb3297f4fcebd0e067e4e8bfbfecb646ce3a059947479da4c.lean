import Mathlib

/-! A separate analytic formal extension. The author candidate is unchanged. -/
namespace SparsePriorAnalytic
noncomputable section
open Finset
open scoped ENNReal

/-- Unnormalized all-zero-prefix overlap, with real power-weight exponent. -/
def zeroPrefix (u v p : ℝ) (n : ℕ) : ℝ :=
  min (u ^ p * (1-u)^n) (v ^ p * (1-v)^n)

lemma log_one_sub_lower {x : ℝ} (hx : 0 ≤ x) (hx2 : x ≤ (1/2 : ℝ)) :
    -2*x ≤ Real.log (1-x) := by
  have hd : 0 < 1-x := by linarith
  have hl := Real.one_sub_inv_le_log_of_pos hd
  have haux : -2*x ≤ 1-(1-x)⁻¹ := by
    apply (mul_le_mul_right hd).mp
    rw [sub_mul, one_mul, inv_mul_cancel₀ (ne_of_gt hd)]
    nlinarith [mul_nonneg hx (show 0 ≤ 1-2*x by linarith)]
  exact haux.trans hl

lemma weighted_log_ratio_le {u v : ℝ} (hu : 0 < u) (hv : 0 < v) :
    v * Real.log (u/v) ≤ u := by
  have hl := mul_le_mul_of_nonneg_left
    (Real.log_le_sub_one_of_pos (div_pos hu hv)) (le_of_lt hv)
  have he : v * (u/v-1) = u-v := by field_simp
  rw [he] at hl
  linarith

lemma one_sub_pow_eq_exp {x : ℝ} (hx : x < 1) (n : ℕ) :
    (1-x)^n = Real.exp ((n:ℝ)*Real.log (1-x)) := by
  rw [Real.exp_nat_mul, Real.exp_log (by linarith : 0 < 1-x)]

lemma zeroPrefix_nonneg {u v p : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hv1 : v ≤ 1) (n : ℕ) :
    0 ≤ zeroPrefix u v p n := by
  apply le_min
  · exact mul_nonneg (Real.rpow_nonneg hu p) (pow_nonneg (by linarith) _)
  · exact mul_nonneg (Real.rpow_nonneg hv p) (pow_nonneg (by linarith) _)

/-- Analytic lower bound for every integer in the prior-odds zero-prefix window. -/
lemma zeroPrefix_window_lower {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu2 : u ≤ (1/2 : ℝ)) (hvu : v ≤ u) (hp : 0 < p) (n : ℕ)
    (hn : 2*u*(n:ℝ) ≤ p * Real.log (u/v)) :
    v ^ p * Real.exp (-p) ≤ zeroPrefix u v p n := by
  have hv2 : v ≤ (1/2 : ℝ) := hvu.trans hu2
  have hnu : -2*u*(n:ℝ) ≤ (n:ℝ) * Real.log (1-u) := by
    have h := mul_le_mul_of_nonneg_left (log_one_sub_lower hu.le hu2)
      (Nat.cast_nonneg n : 0 ≤ (n:ℝ))
    nlinarith
  have hlog : Real.log (u/v) = Real.log u - Real.log v :=
    Real.log_div (ne_of_gt hu) (ne_of_gt hv)
  have hpowu : v ^ p ≤ u ^ p * (1-u)^n := by
    rw [Real.rpow_def_of_pos hv, Real.rpow_def_of_pos hu,
      one_sub_pow_eq_exp (by linarith : u < 1), ← Real.exp_add]
    apply Real.exp_le_exp.mpr
    rw [hlog] at hn
    nlinarith
  have hnv : 2*v*(n:ℝ) ≤ p := by
    apply (mul_le_mul_right hu).mp
    calc
      (2*v*(n:ℝ))*u = v*(2*u*(n:ℝ)) := by ring
      _ ≤ v*(p*Real.log (u/v)) := mul_le_mul_of_nonneg_left hn hv.le
      _ = p*(v*Real.log (u/v)) := by ring
      _ ≤ p*u := mul_le_mul_of_nonneg_left (weighted_log_ratio_le hu hv) hp.le
  have hpowv : Real.exp (-p) ≤ (1-v)^n := by
    rw [one_sub_pow_eq_exp (by linarith : v < 1)]
    apply Real.exp_le_exp.mpr
    have h := mul_le_mul_of_nonneg_left (log_one_sub_lower hv.le hv2)
      (Nat.cast_nonneg n : 0 ≤ (n:ℝ))
    nlinarith
  apply le_min
  · have he : Real.exp (-p) ≤ 1 := Real.exp_le_one_iff.mpr (by linarith)
    exact (mul_le_of_le_one_right (Real.rpow_nonneg hv.le p) he).trans hpowu
  · exact mul_le_mul_of_nonneg_left hpowv (Real.rpow_nonneg hv.le p)

/-- Shifting the all-zero overlap charges a genuine post-acquisition report. -/
lemma zeroPrefix_shift {u v p : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu2 : u ≤ (1/2 : ℝ)) (hv2 : v ≤ (1/2 : ℝ)) (n : ℕ) :
    zeroPrefix u v p n / 2 ≤ zeroPrefix u v p (n+1) := by
  have hU : 0 ≤ u^p*(1-u)^n :=
    mul_nonneg (Real.rpow_nonneg hu p) (pow_nonneg (by linarith) _)
  have hV : 0 ≤ v^p*(1-v)^n :=
    mul_nonneg (Real.rpow_nonneg hv p) (pow_nonneg (by linarith) _)
  have hmU : zeroPrefix u v p n ≤ u^p*(1-u)^n := min_le_left _ _
  have hmV : zeroPrefix u v p n ≤ v^p*(1-v)^n := min_le_right _ _
  unfold zeroPrefix
  rw [pow_succ, pow_succ]
  apply le_min
  · have h := mul_nonneg hU (show 0 ≤ (1/2 : ℝ)-u by linarith)
    dsimp [zeroPrefix] at hmU
    nlinarith
  · have h := mul_nonneg hV (show 0 ≤ (1/2 : ℝ)-v by linarith)
    dsimp [zeroPrefix] at hmV
    nlinarith

/-- Number of zero prefixes in the odds window, including the zero prefix
only as an algebraic device before shifting every charged index by one. -/
def windowLength (u v p : ℝ) : ℕ :=
  Nat.floor (p * Real.log (u/v)/(2*u)) + 1

/-- Uniform lower bound on an explicit finite sum of genuine n>=1 overlaps. -/
theorem zeroPrefix_finite_lower {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu2 : u ≤ (1/2 : ℝ)) (hvu : v ≤ u) (hp : 0 < p) :
    (p * Real.exp (-p)/4) * (v^p/u) * Real.log (u/v) ≤
      ∑ n ∈ range (windowLength u v p), zeroPrefix u v p (n+1) := by
  let X : ℝ := p * Real.log (u/v)/(2*u)
  have hL : 0 ≤ Real.log (u/v) :=
    Real.log_nonneg ((le_div_iff₀ hv).mpr (by simpa using hvu))
  have hX : 0 ≤ X := div_nonneg (mul_nonneg hp.le hL) (by positivity)
  have hfloor : (Nat.floor X : ℝ) ≤ X := Nat.floor_le hX
  have hterm : ∀ n ∈ range (windowLength u v p),
      v^p * Real.exp (-p)/2 ≤ zeroPrefix u v p (n+1) := by
    intro n hn
    have hnat : n ≤ Nat.floor X := by
      have h := mem_range.mp hn
      change n < Nat.floor X + 1 at h
      omega
    have hnX : (n:ℝ) ≤ X := (Nat.cast_le.mpr hnat).trans hfloor
    have hn' : 2*u*(n:ℝ) ≤ p * Real.log (u/v) := by
      have h := (le_div_iff₀ (by positivity : 0 < 2*u)).mp hnX
      nlinarith
    exact (div_le_div_of_nonneg_right
      (zeroPrefix_window_lower hu hv hu2 hvu hp n hn') (by norm_num : (0:ℝ) ≤ 2)).trans
      (zeroPrefix_shift hu.le hv.le hu2 (hvu.trans hu2) n)
  have hsum : (windowLength u v p : ℝ) * (v^p * Real.exp (-p)/2) ≤
      ∑ n ∈ range (windowLength u v p), zeroPrefix u v p (n+1) := by
    calc
      _ = ∑ _n ∈ range (windowLength u v p), v^p * Real.exp (-p)/2 := by simp
      _ ≤ _ := Finset.sum_le_sum hterm
  have hcast : X ≤ (windowLength u v p : ℝ) := by
    have h := (Nat.lt_floor_add_one X).le
    simpa only [windowLength, Nat.cast_add, Nat.cast_one] using h
  calc
    _ = X * (v^p * Real.exp (-p)/2) := by dsimp [X]; field_simp; ring
    _ ≤ (windowLength u v p : ℝ) * (v^p * Real.exp (-p)/2) :=
      mul_le_mul_of_nonneg_right hcast (by positivity)
    _ ≤ _ := hsum

/-- The same lower bound lifted to the extended nonnegative lifetime sum. -/
theorem zeroPrefix_lifetime_lower {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu2 : u ≤ (1/2 : ℝ)) (hvu : v ≤ u) (hp : 0 < p) :
    ENNReal.ofReal ((p * Real.exp (-p)/4) * (v^p/u) * Real.log (u/v)) ≤
      ∑' n : ℕ, ENNReal.ofReal (zeroPrefix u v p (n+1)) := by
  have h := ENNReal.ofReal_le_ofReal (zeroPrefix_finite_lower hu hv hu2 hvu hp)
  rw [ENNReal.ofReal_sum_of_nonneg (fun n _ =>
    zeroPrefix_nonneg hu.le hv.le (by linarith) (by linarith) (n+1))] at h
  exact h.trans (ENNReal.sum_le_tsum (range (windowLength u v p)))

/-- Explicit finite Bernoulli binary overlap, with unnormalized weights u^p,v^p. -/
def binaryOverlap (u v p : ℝ) (n : ℕ) : ℝ :=
  ∑ k ∈ range (n+1), (n.choose k : ℝ) *
    min (u^p * u^k * (1-u)^(n-k)) (v^p * v^k * (1-v)^(n-k))

lemma binaryOverlap_nonneg {u v p : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hv1 : v ≤ 1) (n : ℕ) :
    0 ≤ binaryOverlap u v p n := by
  have hu0 : 0 ≤ 1-u := sub_nonneg.mpr hu1
  have hv0 : 0 ≤ 1-v := sub_nonneg.mpr hv1
  unfold binaryOverlap
  apply sum_nonneg
  intro k hk
  apply mul_nonneg (Nat.cast_nonneg _)
  apply le_min <;> positivity

lemma zeroPrefix_le_binaryOverlap {u v p : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hv1 : v ≤ 1) (n : ℕ) :
    zeroPrefix u v p n ≤ binaryOverlap u v p n := by
  have hu0 : 0 ≤ 1-u := sub_nonneg.mpr hu1
  have hv0 : 0 ≤ 1-v := sub_nonneg.mpr hv1
  have h := Finset.single_le_sum (f := fun k => (n.choose k : ℝ) *
      min (u^p * u^k * (1-u)^(n-k)) (v^p * v^k * (1-v)^(n-k)))
    (s := range (n+1)) (a := 0)
    (fun k hk => by apply mul_nonneg (Nat.cast_nonneg _); apply le_min <;> positivity)
    (show 0 ∈ range (n+1) by simp)
  simpa [zeroPrefix, binaryOverlap] using h

/-- Fully proved uniform lower bound for the actual binary-overlap lifetime. -/
theorem binaryOverlap_lifetime_lower {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu2 : u ≤ (1/2 : ℝ)) (hvu : v ≤ u) (hp : 0 < p) :
    ENNReal.ofReal ((p * Real.exp (-p)/4) * (v^p/u) * Real.log (u/v)) ≤
      ∑' n : ℕ, ENNReal.ofReal (binaryOverlap u v p (n+1)) := by
  apply (zeroPrefix_lifetime_lower hu hv hu2 hvu hp).trans
  apply ENNReal.tsum_le_tsum
  intro n
  exact ENNReal.ofReal_le_ofReal
    (zeroPrefix_le_binaryOverlap hu.le hv.le (by linarith) (by linarith) (n+1))

/-- Integration over countably many adjacent pairs, with nonnegative Tonelli.
This is a bound for the explicit overlap series; its identification with the
all-policy statistical Bayes risk is still an ordinary theorem in the packet. -/
theorem integrated_binaryOverlap_lower (a : ℕ → ℝ) {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hmono : ∀ i, a (i+1) ≤ a i) :
    (∑' i : ℕ, ENNReal.ofReal
      ((p * Real.exp (-p)/4) * ((a (i+1))^p/a i) * Real.log (a i/a (i+1)))) ≤
      ∑' n : ℕ, ∑' i : ℕ, ENNReal.ofReal (binaryOverlap (a i) (a (i+1)) p (n+1)) := by
  rw [ENNReal.tsum_comm]
  exact ENNReal.tsum_le_tsum (fun i =>
    binaryOverlap_lifetime_lower (hpos i) (hpos (i+1)) (hhalf i) (hmono i) hp)

/-- Weighted geometric means dominate a minimum. -/
lemma min_le_rpow_mix {A B s : ℝ} (hA : 0 < A) (hB : 0 < B)
    (hs : 0 ≤ s) (hs1 : s ≤ 1) :
    min A B ≤ A^s * B^(1-s) := by
  rcases le_total A B with h | h
  · rw [min_eq_left h]
    calc
      A = A^s * A^(1-s) := by rw [← Real.rpow_add hA]; simp
      _ ≤ A^s * B^(1-s) := mul_le_mul_of_nonneg_left
        (Real.rpow_le_rpow hA.le h (by linarith)) (Real.rpow_nonneg hA.le s)
  · rw [min_eq_right h]
    calc
      B = B^s * B^(1-s) := by rw [← Real.rpow_add hB]; simp
      _ ≤ A^s * B^(1-s) := mul_le_mul_of_nonneg_right
        (Real.rpow_le_rpow hB.le h hs) (Real.rpow_nonneg hB.le (1-s))

lemma sqrt_product_eq_exp {x y : ℝ} (hx : 0 < x) (hy : 0 < y) :
    Real.sqrt x * Real.sqrt y = Real.exp ((Real.log x + Real.log y)/2) := by
  rw [Real.sqrt_eq_rpow, Real.sqrt_eq_rpow, Real.rpow_def_of_pos hx,
    Real.rpow_def_of_pos hy, ← Real.exp_add]
  congr 1
  ring

/-- Convexity chord between exponent zero and exponent one half. -/
lemma rpow_mix_chord {x y s : ℝ} (hx : 0 < x) (hy : 0 < y)
    (hs : 0 ≤ s) (hs2 : s ≤ (1/2 : ℝ)) :
    x^s * y^(1-s) ≤ (1-2*s)*y + 2*s*(Real.sqrt x * Real.sqrt y) := by
  calc
    _ = Real.exp ((1-2*s)*Real.log y + 2*s*((Real.log x+Real.log y)/2)) := by
      rw [Real.rpow_def_of_pos hx, Real.rpow_def_of_pos hy, ← Real.exp_add]
      congr 1
      ring
    _ ≤ (1-2*s)*Real.exp (Real.log y) +
        2*s*Real.exp ((Real.log x+Real.log y)/2) :=
      convexOn_exp.2 (Set.mem_univ _) (Set.mem_univ _)
        (by linarith) (by linarith) (by ring)
    _ = _ := by rw [Real.exp_log hy, ← sqrt_product_eq_exp hx hy]

/-- A coarse but uniform Hellinger deficit for half-separated Bernoulli points. -/
lemma half_affinity_deficit {u v : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hvu : v ≤ u/2) :
    u/32 ≤ 1-(Real.sqrt u*Real.sqrt v + Real.sqrt (1-u)*Real.sqrt (1-v)) := by
  have hv1 : v ≤ 1 := by linarith
  have hsu := Real.sq_sqrt hu
  have hsv := Real.sq_sqrt hv
  have hsu1 := Real.sq_sqrt (show 0 ≤ 1-u by linarith)
  have hsv1 := Real.sq_sqrt (show 0 ≤ 1-v by linarith)
  have hsu0 := Real.sqrt_nonneg u
  have hsv0 := Real.sqrt_nonneg v
  have hsqrt : Real.sqrt v ≤ (3/4 : ℝ)*Real.sqrt u := by
    apply Real.sqrt_le_iff.mpr
    constructor
    · positivity
    · nlinarith
  have hgap : u/16 ≤ (Real.sqrt u-Real.sqrt v)^2 := by
    have h := mul_nonneg
      (show 0 ≤ Real.sqrt u-Real.sqrt v-Real.sqrt u/4 by linarith)
      (show 0 ≤ Real.sqrt u-Real.sqrt v+Real.sqrt u/4 by linarith)
    nlinarith
  nlinarith [sq_nonneg (Real.sqrt (1-u)-Real.sqrt (1-v))]

/-- Bernoulli Chernoff affinity. -/
def affinity (u v s : ℝ) : ℝ :=
  u^s*v^(1-s) + (1-u)^s*(1-v)^(1-s)

lemma affinity_nonneg {u v s : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hv1 : v ≤ 1) : 0 ≤ affinity u v s := by
  have hu0 : 0 ≤ 1-u := sub_nonneg.mpr hu1
  have hv0 : 0 ≤ 1-v := sub_nonneg.mpr hv1
  unfold affinity
  positivity

/-- Quantitative affinity deficit, proved from convexity and exact square roots. -/
lemma affinity_deficit {u v s : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu1 : u < 1) (hvu : v ≤ u/2) (hs : 0 ≤ s) (hs2 : s ≤ (1/2 : ℝ)) :
    s*u/16 ≤ 1-affinity u v s := by
  have hv1 : v < 1 := by linarith
  have h0 := rpow_mix_chord hu hv hs hs2
  have h1 := rpow_mix_chord (show 0 < 1-u by linarith)
    (show 0 < 1-v by linarith) hs hs2
  have hh := half_affinity_deficit hu.le hv.le hu1.le hvu
  have hm := mul_le_mul_of_nonneg_left hh hs
  dsimp [affinity]
  nlinarith

lemma rpow_prod3 {A B C s : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B) (hC : 0 ≤ C) :
    (A*B*C)^s = A^s*B^s*C^s := by
  rw [Real.mul_rpow (mul_nonneg hA hB) hC, Real.mul_rpow hA hB]

lemma rpow_natpow_swap {x s : ℝ} (hx : 0 ≤ x) (k : ℕ) :
    (x^k)^s = (x^s)^k := by
  rw [← Real.rpow_natCast_mul hx, ← Real.rpow_mul_natCast hx]
  congr 1
  ring

lemma mixed_likelihood_factorization {u v p s : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v)
    (hu1 : u ≤ 1) (hv1 : v ≤ 1) (k l : ℕ) :
    (u^p*u^k*(1-u)^l)^s * (v^p*v^k*(1-v)^l)^(1-s) =
      ((u^p)^s*(v^p)^(1-s)) * (u^s*v^(1-s))^k * ((1-u)^s*(1-v)^(1-s))^l := by
  have hu0 : 0 ≤ 1-u := sub_nonneg.mpr hu1
  have hv0 : 0 ≤ 1-v := sub_nonneg.mpr hv1
  rw [rpow_prod3 (Real.rpow_nonneg hu p) (pow_nonneg hu k) (pow_nonneg hu0 l),
      rpow_prod3 (Real.rpow_nonneg hv p) (pow_nonneg hv k) (pow_nonneg hv0 l),
      rpow_natpow_swap hu k, rpow_natpow_swap hv k,
      rpow_natpow_swap hu0 l, rpow_natpow_swap hv0 l,
      mul_pow, mul_pow]
  ring

/-- Direct binomial Chernoff bound, without a probability-space concentration premise. -/
theorem binaryOverlap_chernoff {u v p s : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu1 : u < 1) (hv1 : v < 1) (hs : 0 ≤ s) (hs1 : s ≤ 1) (n : ℕ) :
    binaryOverlap u v p n ≤ ((u^p)^s*(v^p)^(1-s)) * (affinity u v s)^n := by
  have hu0 : 0 < 1-u := sub_pos.mpr hu1
  have hv0 : 0 < 1-v := sub_pos.mpr hv1
  unfold binaryOverlap
  calc
    _ ≤ ∑ k ∈ range (n+1), (n.choose k : ℝ) *
        (((u^p)^s*(v^p)^(1-s)) * (u^s*v^(1-s))^k *
          ((1-u)^s*(1-v)^(1-s))^(n-k)) := by
      apply sum_le_sum
      intro k hk
      apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
      have h := min_le_rpow_mix
        (show 0 < u^p*u^k*(1-u)^(n-k) by positivity)
        (show 0 < v^p*v^k*(1-v)^(n-k) by positivity) hs hs1
      rwa [mixed_likelihood_factorization hu.le hv.le hu1.le hv1.le] at h
    _ = ((u^p)^s*(v^p)^(1-s)) *
        ∑ k ∈ range (n+1), (u^s*v^(1-s))^k *
          ((1-u)^s*(1-v)^(1-s))^(n-k) * (n.choose k : ℝ) := by
      rw [mul_sum]
      apply sum_congr rfl
      intro k hk
      ring
    _ = _ := by rw [← add_pow]; rfl

/-- An explicit Chernoff exponent adapted to the prior odds. -/
def chosenExponent (u v p : ℝ) : ℝ := 1 / (4*(p+1)*Real.log (u/v))

lemma log_ratio_half {u v : ℝ} (_hu : 0 < u) (hv : 0 < v) (hvu : v ≤ u/2) :
    (1/2 : ℝ) ≤ Real.log (u/v) := by
  have hlog2 : (1/2 : ℝ) ≤ Real.log 2 := by
    have h := Real.one_sub_inv_le_log_of_pos (by norm_num : (0:ℝ) < 2)
    norm_num at h
    exact h
  have hr : (2:ℝ) ≤ u/v := (le_div_iff₀ hv).mpr (by linarith)
  exact hlog2.trans (Real.log_le_log (by norm_num) hr)

lemma chosenExponent_bounds {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hvu : v ≤ u/2) (hp : 0 < p) :
    0 < chosenExponent u v p ∧ chosenExponent u v p ≤ (1/2 : ℝ) := by
  have hL := log_ratio_half hu hv hvu
  have hp1 : 0 < p+1 := by linarith
  have hd : 0 < 4*(p+1)*Real.log (u/v) := by positivity
  constructor
  · exact one_div_pos.mpr hd
  · unfold chosenExponent
    apply (div_le_iff₀ hd).mpr
    nlinarith [mul_nonneg (show 0 ≤ p by linarith)
      (show 0 ≤ Real.log (u/v)-(1/2:ℝ) by linarith)]

lemma prior_factor_identity {u v p s : ℝ} (hu : 0 < u) (hv : 0 < v) :
    (u^p)^s * (v^p)^(1-s) = v^p * Real.exp (p*s*Real.log (u/v)) := by
  rw [Real.rpow_def_of_pos (Real.rpow_pos_of_pos hu p),
      Real.rpow_def_of_pos (Real.rpow_pos_of_pos hv p),
      Real.log_rpow hu, Real.log_rpow hv,
      Real.rpow_def_of_pos hv, ← Real.exp_add, ← Real.exp_add,
      Real.log_div (ne_of_gt hu) (ne_of_gt hv)]
  congr 1
  ring

lemma chosen_prior_factor_bound {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hvu : v ≤ u/2) (hp : 0 < p) :
    (u^p)^(chosenExponent u v p) * (v^p)^(1-chosenExponent u v p) ≤ 2*v^p := by
  have hL := log_ratio_half hu hv hvu
  have hL0 : Real.log (u/v) ≠ 0 := by linarith
  have hp1 : p+1 ≠ 0 := by linarith
  have heq : p*chosenExponent u v p*Real.log (u/v) = p/(4*(p+1)) := by
    unfold chosenExponent
    field_simp
    ring
  have hsmall : p/(4*(p+1)) ≤ (1/4 : ℝ) := by
    apply (div_le_iff₀ (by positivity : 0 < 4*(p+1))).mpr
    linarith
  have hlog2 : (1/4 : ℝ) ≤ Real.log 2 := by
    have h := Real.one_sub_inv_le_log_of_pos (by norm_num : (0:ℝ) < 2)
    norm_num at h
    linarith
  have hexp : Real.exp (p*chosenExponent u v p*Real.log (u/v)) ≤ 2 := by
    rw [← Real.exp_log (by norm_num : (0:ℝ) < 2)]
    apply Real.exp_le_exp.mpr
    rw [heq]
    exact hsmall.trans hlog2
  rw [prior_factor_identity hu hv]
  nlinarith [mul_le_mul_of_nonneg_left hexp (Real.rpow_nonneg hv.le p)]

lemma ennreal_geometric_envelope {A r : ℝ} (hA : 0 ≤ A) (hr : 0 ≤ r) (hr1 : r < 1) :
    (∑' n : ℕ, ENNReal.ofReal (A*r^n)) = ENNReal.ofReal (A/(1-r)) := by
  have hs : Summable (fun n : ℕ => A*r^n) :=
    (summable_geometric_of_lt_one hr hr1).mul_left A
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun n => mul_nonneg hA (pow_nonneg hr n)) hs,
    tsum_mul_left, tsum_geometric_of_lt_one hr hr1, div_eq_mul_inv]

/-- Uniform lifetime upper bound for the actual finite-binomial overlaps.
Every bound is derived here from weighted geometric means, convexity,
the binomial theorem, and a geometric series. No concentration theorem or
probability-space estimate is assumed. -/
theorem binaryOverlap_lifetime_upper {u v p : ℝ} (hu : 0 < u) (hv : 0 < v)
    (hu2 : u ≤ (1/2 : ℝ)) (hvu : v ≤ u/2) (hp : 0 < p) :
    (∑' n : ℕ, ENNReal.ofReal (binaryOverlap u v p (n+1))) ≤
      ENNReal.ofReal ((128*(p+1)) * (v^p/u) * Real.log (u/v)) := by
  let s := chosenExponent u v p
  let r := affinity u v s
  have hu1 : u < 1 := by linarith
  have hv1 : v < 1 := by linarith
  have hs : 0 < s := (chosenExponent_bounds hu hv hvu hp).1
  have hs2 : s ≤ (1/2 : ℝ) := (chosenExponent_bounds hu hv hvu hp).2
  have hr : 0 ≤ r := affinity_nonneg hu.le hv.le hu1.le hv1.le
  have hdef : s*u/16 ≤ 1-r := affinity_deficit hu hv hu1 hvu hs.le hs2
  have hden : 0 < s*u/16 := by positivity
  have hr1 : r < 1 := by linarith
  have hfactor : (u^p)^s*(v^p)^(1-s) ≤ 2*v^p :=
    chosen_prior_factor_bound hu hv hvu hp
  have hBn : ∀ n : ℕ, binaryOverlap u v p (n+1) ≤ 2*v^p*r^n := by
    intro n
    calc
      _ ≤ ((u^p)^s*(v^p)^(1-s))*r^(n+1) :=
        binaryOverlap_chernoff hu hv hu1 hv1 hs.le (by linarith) (n+1)
      _ ≤ (2*v^p)*r^(n+1) := mul_le_mul_of_nonneg_right hfactor (pow_nonneg hr _)
      _ ≤ (2*v^p)*r^n := by
        apply mul_le_mul_of_nonneg_left _ (by positivity)
        rw [pow_succ]
        exact mul_le_of_le_one_right (pow_nonneg hr _) hr1.le
  have hL := log_ratio_half hu hv hvu
  have hL0 : Real.log (u/v) ≠ 0 := by linarith
  have hp1 : p+1 ≠ 0 := by linarith
  have hreal : (2*v^p)/(1-r) ≤ (128*(p+1))*(v^p/u)*Real.log (u/v) := by
    calc
      _ ≤ (2*v^p)/(s*u/16) :=
        div_le_div_of_nonneg_left (by positivity) hden hdef
      _ = _ := by dsimp [s, chosenExponent]; field_simp; ring
  calc
    _ ≤ ∑' n : ℕ, ENNReal.ofReal (2*v^p*r^n) :=
      ENNReal.tsum_le_tsum (fun n => ENNReal.ofReal_le_ofReal (hBn n))
    _ = ENNReal.ofReal ((2*v^p)/(1-r)) :=
      ennreal_geometric_envelope (by positivity) hr hr1
    _ ≤ _ := ENNReal.ofReal_le_ofReal hreal

/-- Countable integration of the independently proved lifetime upper bound. -/
theorem integrated_binaryOverlap_upper (a : ℕ → ℝ) {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) :
    (∑' n : ℕ, ∑' i : ℕ, ENNReal.ofReal (binaryOverlap (a i) (a (i+1)) p (n+1))) ≤
      ∑' i : ℕ, ENNReal.ofReal
        ((128*(p+1)) * ((a (i+1))^p/a i) * Real.log (a i/a (i+1))) := by
  rw [ENNReal.tsum_comm]
  exact ENNReal.tsum_le_tsum (fun i =>
    binaryOverlap_lifetime_upper (hpos i) (hpos (i+1)) (hhalf i) (hsep i) hp)

/-- The nonnegative raw support-spacing series, without the prior normalizer. -/
def spacingTotal (a : ℕ → ℝ) (p : ℝ) : ℝ≥0∞ :=
  ∑' i : ℕ, ENNReal.ofReal (((a (i+1))^p/a i) * Real.log (a i/a (i+1)))

/-- Total explicit adjacent binary-overlap mass, charging n>=1 only. -/
def overlapTotal (a : ℕ → ℝ) (p : ℝ) : ℝ≥0∞ :=
  ∑' n : ℕ, ∑' i : ℕ, ENNReal.ofReal (binaryOverlap (a i) (a (i+1)) p (n+1))

/-- Two-sided quantitative comparison after countable integration. -/
theorem integrated_comparison (a : ℕ → ℝ) {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) :
    ENNReal.ofReal (p*Real.exp (-p)/4) * spacingTotal a p ≤ overlapTotal a p ∧
    overlapTotal a p ≤ ENNReal.ofReal (128*(p+1)) * spacingTotal a p := by
  have hc : 0 ≤ p*Real.exp (-p)/4 := by positivity
  have hK : 0 ≤ 128*(p+1) := by positivity
  have hmono : ∀ i, a (i+1) ≤ a i := by
    intro i
    have h := hsep i
    have hp := hpos i
    linarith
  have hl := integrated_binaryOverlap_lower a hp hpos hhalf hmono
  have hu := integrated_binaryOverlap_upper a hp hpos hhalf hsep
  constructor
  · change ENNReal.ofReal (p*Real.exp (-p)/4) *
      (∑' i : ℕ, ENNReal.ofReal (((a (i+1))^p/a i) * Real.log (a i/a (i+1)))) ≤ _
    rw [← ENNReal.tsum_mul_left]
    convert hl using 1
    apply tsum_congr
    intro i
    rw [← ENNReal.ofReal_mul hc]
    congr 1
    ring
  · change _ ≤ ENNReal.ofReal (128*(p+1)) *
      (∑' i : ℕ, ENNReal.ofReal (((a (i+1))^p/a i) * Real.log (a i/a (i+1))))
    rw [← ENNReal.tsum_mul_left]
    convert hu using 1
    apply tsum_congr
    intro i
    rw [← ENNReal.ofReal_mul hK]
    congr 1
    ring

/-- Sharp finiteness iff for the actual explicit infinite overlap series.
No infinite-sum finiteness or risk comparison is supplied as a hypothesis. -/
theorem overlapTotal_finite_iff (a : ℕ → ℝ) {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) :
    overlapTotal a p < ⊤ ↔ spacingTotal a p < ⊤ := by
  have hb := integrated_comparison a hp hpos hhalf hsep
  constructor
  · intro h
    have hprod := lt_of_le_of_lt hb.1 h
    apply ENNReal.lt_top_of_mul_ne_top_right (ne_of_lt hprod)
    exact ne_of_gt (ENNReal.ofReal_pos.mpr (by positivity))
  · intro h
    exact lt_of_le_of_lt hb.2 (ENNReal.mul_lt_top ENNReal.ofReal_lt_top h)

lemma ofReal_tsum_finite_iff_summable {f : ℕ → ℝ} (hf : ∀ i, 0 ≤ f i) :
    (∑' i : ℕ, ENNReal.ofReal (f i)) < ⊤ ↔ Summable f := by
  change (∑' i : ℕ, ((f i).toNNReal : ℝ≥0∞)) < ⊤ ↔ Summable f
  rw [lt_top_iff_ne_top, ENNReal.tsum_coe_ne_top_iff_summable_coe]
  simp only [Real.coe_toNNReal', max_eq_left (hf _)]

/-- The sharp formal criterion in the ordinary real-series Summable notation. -/
theorem overlapTotal_finite_iff_summable (a : ℕ → ℝ) {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) :
    overlapTotal a p < ⊤ ↔
      Summable (fun i : ℕ => ((a (i+1))^p/a i) * Real.log (a i/a (i+1))) := by
  rw [overlapTotal_finite_iff a hp hpos hhalf hsep]
  apply ofReal_tsum_finite_iff_summable
  intro i
  have hlog := log_ratio_half (hpos i) (hpos (i+1)) (hsep i)
  apply mul_nonneg (div_nonneg (Real.rpow_nonneg (hpos (i+1)).le p) (hpos i).le)
  linarith

#print axioms zeroPrefix_finite_lower
#print axioms binaryOverlap_lifetime_lower
#print axioms affinity_deficit
#print axioms binaryOverlap_chernoff
#print axioms binaryOverlap_lifetime_upper
#print axioms integrated_comparison
#print axioms overlapTotal_finite_iff
#print axioms overlapTotal_finite_iff_summable
end
end SparsePriorAnalytic



/-!
Scoped finite certificates for the sparse-prior packet.

This file proves loss separation and a finite adjacent-minimum identity.
It does not formalize the infinite prior, Bayes selector, concentration,
integrability criterion, or endpoint-atom theorem.
-/
namespace SparsePriorGeometry

noncomputable section
open Finset

/-- Both-truth weak acceptance for the exact inherited excesses. -/
def Accepted (a epsilon q : ℝ) : Prop :=
  q ^ 2 - (1 / 4 : ℝ) - a * epsilon * (1 + epsilon) ≤ 0 ∧
  (1 - q) ^ 2 - (1 / 4 : ℝ) + a * epsilon * (1 - epsilon) ≤ 0

/-- The hypothesis-specific affine report has its exact negative margin. -/
theorem own_report_margin (a epsilon : ℝ) :
    ((1 / 2 : ℝ) + epsilon * a) ^ 2 - (1 / 4 : ℝ) -
        a * epsilon * (1 + epsilon) = -epsilon ^ 2 * a * (1-a) ∧
    (1 - ((1 / 2 : ℝ) + epsilon * a)) ^ 2 - (1 / 4 : ℝ) +
        a * epsilon * (1 - epsilon) = -epsilon ^ 2 * a * (1-a) := by
  constructor <;> ring

/-- Any common accepted report bounds the multiplicative parameter ratio. -/
theorem acceptance_ratio {a b epsilon q : ℝ} (he : 0 < epsilon)
    (ha : Accepted a epsilon q) (hb : Accepted b epsilon q) :
    b * (1-epsilon) ≤ a * (1+epsilon) := by
  apply (mul_le_mul_right he).mp
  have hsq : 0 ≤ (q - (1 / 2 : ℝ)) ^ 2 := sq_nonneg _
  rcases ha with ⟨ha0, ha1⟩
  rcases hb with ⟨hb0, hb1⟩
  nlinarith

/-- A factor-two gap separates the exact acceptance sets. -/
theorem no_common_report_at_factor_two {a b epsilon q : ℝ}
    (ha : 0 < a) (he : 0 < epsilon) (he4 : epsilon ≤ (1 / 4 : ℝ))
    (hab : 2 * a ≤ b) : ¬ (Accepted a epsilon q ∧ Accepted b epsilon q) := by
  intro h
  have hr := acceptance_ratio he h.1 h.2
  have hp : 0 ≤ 1-epsilon := by linarith
  have hm := mul_le_mul_of_nonneg_right hab hp
  have hs : 0 ≤ a * ((1 / 4 : ℝ)-epsilon) :=
    mul_nonneg (le_of_lt ha) (by linarith)
  nlinarith

/-- Finite exact adjacent-minimum identity for a sequence with a declared mode.
The hypotheses are local monotonicity on either side; no nonnegativity is
needed for this finite algebraic identity. -/
theorem adjacent_min_sum (a : ℕ → ℝ) (n m : ℕ) (hm : m ≤ n)
    (hup : ∀ i, i < m → a i ≤ a (i+1))
    (hdown : ∀ i, m ≤ i → i < n → a (i+1) ≤ a i) :
    (∑ i ∈ range n, min (a i) (a (i+1))) =
      (∑ i ∈ range (n+1), a i) - a m := by
  induction n with
  | zero =>
      have hm0 : m = 0 := by omega
      subst m
      simp
  | succ n ih =>
      by_cases hm' : m ≤ n
      · have hdown' : ∀ i, m ≤ i → i < n → a (i+1) ≤ a i := by
          intro i hmi hin
          exact hdown i hmi (by omega)
        have hprev := ih hm' hdown'
        rw [sum_range_succ, hprev, min_eq_right (hdown n hm' (by omega))]
        simp only [sum_range_succ]
        ring
      · have heq : m = n+1 := by omega
        subst m
        have heach : (∑ i ∈ range (n+1), min (a i) (a (i+1))) =
            ∑ i ∈ range (n+1), a i := by
          apply sum_congr rfl
          intro i hi
          exact min_eq_left (hup i (mem_range.mp hi))
        rw [heach]
        simp only [sum_range_succ]
        ring

#print axioms own_report_margin
#print axioms acceptance_ratio
#print axioms no_common_report_at_factor_two
#print axioms adjacent_min_sum

end
end SparsePriorGeometry

/-! The prefix above is the exact accepted finite geometry certificate.
This separate, unfinished extension explores the countable Bayes-risk bridge. -/
namespace SparsePriorBayes
noncomputable section
open Finset Filter
open scoped Topology ENNReal

lemma adjacent_min_summable {a : ℕ → ℝ} (ha : Summable a) (h0 : ∀ i, 0 ≤ a i) :
    Summable (fun i => min (a i) (a (i+1))) := by
  exact Summable.of_nonneg_of_le (fun i => le_min (h0 i) (h0 (i+1)))
    (fun i => min_le_left _ _) ha

/-- The finite modal identity passes to the countably infinite sum. -/
theorem adjacent_min_tsum {a : ℕ → ℝ} (ha : Summable a) (h0 : ∀ i, 0 ≤ a i)
    (m : ℕ) (hup : ∀ i, i < m → a i ≤ a (i+1))
    (hdown : ∀ i, m ≤ i → a (i+1) ≤ a i) :
    (∑' i : ℕ, min (a i) (a (i+1))) = (∑' i : ℕ, a i) - a m := by
  have hm := (adjacent_min_summable ha h0).hasSum.tendsto_sum_nat
  have hs := ha.hasSum.tendsto_sum_nat
  have hs1 : Tendsto (fun n : ℕ => (∑ i ∈ range (n+1), a i) - a m)
      atTop (𝓝 ((∑' i : ℕ, a i)-a m)) := by
    exact (hs.comp (tendsto_add_atTop_nat 1)).sub_const _
  have he : (fun n : ℕ => ∑ i ∈ range n, min (a i) (a (i+1))) =ᶠ[atTop]
      (fun n : ℕ => (∑ i ∈ range (n+1), a i)-a m) := by
    filter_upwards [eventually_ge_atTop m] with n hn
    exact SparsePriorGeometry.adjacent_min_sum a n m hn hup
      (fun i hmi _ => hdown i hmi)
  exact tendsto_nhds_unique hm (hs1.congr' he.symm)

/-- A positive summable sequence attains a maximum at a finite index. -/
lemma exists_mode_of_summable {s : ℕ → ℝ} (hs : Summable s) (hpos : 0 < s 0) :
    ∃ m : ℕ, ∀ i, s i ≤ s m := by
  have he : ∀ᶠ i in atTop, s i < s 0 :=
    (tendsto_order.mp hs.tendsto_atTop_zero).2 (s 0) hpos
  obtain ⟨N,hN⟩ := eventually_atTop.mp he
  obtain ⟨m,hm,hmmax⟩ := (range (N+1)).exists_max_image s (by simp)
  refine ⟨m,fun i => ?_⟩
  by_cases hi : i < N+1
  · exact hmmax i (mem_range.mpr hi)
  · have hiN : N ≤ i := by omega
    exact (hN i hiN).le.trans (hmmax 0 (by simp))

/-- Interval quasiconcavity plus a global maximum supplies an actual mode. -/
lemma mode_sides {s : ℕ → ℝ} (m : ℕ) (hm : ∀ i, s i ≤ s m)
    (hq : ∀ i j k, i ≤ j → j ≤ k → min (s i) (s k) ≤ s j) :
    (∀ i, i < m → s i ≤ s (i+1)) ∧
    (∀ i, m ≤ i → s (i+1) ≤ s i) := by
  constructor
  · intro i hi
    have h := hq i (i+1) m (by omega) (by omega)
    simpa [min_eq_left (hm i)] using h
  · intro i hi
    have h := hq m i (i+1) hi (by omega)
    simpa [min_eq_right (hm (i+1))] using h

lemma support_antitone {a : ℕ → ℝ} (hpos : ∀ i, 0 < a i)
    (hsep : ∀ i, a (i+1) ≤ a i/2) : Antitone a := by
  apply antitone_nat_of_succ_le
  intro i
  have hp := hpos i
  have hs := hsep i
  linarith

lemma support_geometric {a : ℕ → ℝ} (hsep : ∀ i, a (i+1) ≤ a i/2) (i : ℕ) :
    a i ≤ a 0 * (1/2 : ℝ)^i := by
  induction i with
  | zero => simp
  | succ i ih =>
    have hs := hsep i
    rw [pow_succ]
    nlinarith

lemma rpow_natpow_swap {x s : ℝ} (hx : 0 ≤ x) (k : ℕ) :
    (x^k)^s = (x^s)^k := by
  rw [← Real.rpow_natCast_mul hx, ← Real.rpow_mul_natCast hx]
  congr 1
  ring

lemma power_weights_summable {a : ℕ → ℝ} {p : ℝ} (hpos : ∀ i, 0 < a i)
    (hsep : ∀ i, a (i+1) ≤ a i/2) (hp : 0 < p) : Summable (fun i => (a i)^p) := by
  have hr0 : 0 ≤ (1/2 : ℝ)^p := Real.rpow_nonneg (by norm_num) p
  have hr1 : (1/2 : ℝ)^p < 1 := Real.rpow_lt_one (by norm_num) (by norm_num) hp
  have hmajor := (summable_geometric_of_lt_one hr0 hr1).mul_left ((a 0)^p)
  apply Summable.of_nonneg_of_le (fun i => Real.rpow_nonneg (hpos i).le p) _ hmajor
  intro i
  calc
    (a i)^p ≤ (a 0*(1/2 : ℝ)^i)^p :=
      Real.rpow_le_rpow (hpos i).le (support_geometric hsep i) hp.le
    _ = (a 0)^p * ((1/2 : ℝ)^p)^i := by
      rw [Real.mul_rpow (hpos 0).le (by positivity), rpow_natpow_swap (by norm_num)]

/-- Unnormalized likelihood mass of an exact word with k ones in n receipts. -/
def score (n k : ℕ) (p x : ℝ) : ℝ := x^p*x^k*(1-x)^(n-k)

def logScore (n k : ℕ) (p x : ℝ) : ℝ :=
  (p+(k:ℝ))*Real.log x + ((n-k:ℕ):ℝ)*Real.log (1-x)

lemma score_pos {x p : ℝ} (hx : 0 < x) (hx1 : x < 1) (n k : ℕ) :
    0 < score n k p x := by
  have hx0 : 0 < 1-x := sub_pos.mpr hx1
  unfold score
  positivity

lemma score_le_weight {x p : ℝ} (hx : 0 ≤ x) (hx1 : x ≤ 1) (n k : ℕ) :
    score n k p x ≤ x^p := by
  have hx0 : 0 ≤ 1-x := sub_nonneg.mpr hx1
  have hpow0 : x^k ≤ 1 := pow_le_one₀ hx hx1
  have hpow1 : (1-x)^(n-k) ≤ 1 := pow_le_one₀ hx0 (by linarith)
  unfold score
  exact (mul_le_of_le_one_right (by positivity) hpow1).trans
    (mul_le_of_le_one_right (Real.rpow_nonneg hx p) hpow0)

lemma score_summable {a : ℕ → ℝ} {p : ℝ} (hpos : ∀ i, 0 < a i)
    (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (hsep : ∀ i, a (i+1) ≤ a i/2)
    (hp : 0 < p) (n k : ℕ) : Summable (fun i => score n k p (a i)) := by
  apply Summable.of_nonneg_of_le
    (fun i => (score_pos (hpos i) (by have h := hhalf i; linarith) n k).le)
    (fun i => score_le_weight (hpos i).le (by have h := hhalf i; linarith) n k)
    (power_weights_summable hpos hsep hp)

lemma natpow_eq_exp {x : ℝ} (hx : 0 < x) (n : ℕ) :
    x^n = Real.exp ((n:ℝ)*Real.log x) := by
  rw [Real.exp_nat_mul, Real.exp_log hx]

lemma score_eq_exp {x p : ℝ} (hx : 0 < x) (hx1 : x < 1) (n k : ℕ) :
    score n k p x = Real.exp (logScore n k p x) := by
  unfold score logScore
  rw [Real.rpow_def_of_pos hx, natpow_eq_exp hx k,
    natpow_eq_exp (by linarith : 0 < 1-x) (n-k), ← Real.exp_add, ← Real.exp_add]
  congr 1
  ring

lemma logScore_concave {p : ℝ} (hp : 0 ≤ p) (n k : ℕ) :
    ConcaveOn ℝ (Set.Ioo (0:ℝ) 1) (logScore n k p) := by
  refine ⟨convex_Ioo 0 1, ?_⟩
  intro x hx y hy t r ht hr htr
  have h0 := strictConcaveOn_log_Ioi.concaveOn.2 hx.1 hy.1 ht hr htr
  have h1 := strictConcaveOn_log_Ioi.concaveOn.2
    (show 0 < 1-x by linarith [hx.2]) (show 0 < 1-y by linarith [hy.2]) ht hr htr
  simp only [smul_eq_mul] at h0 h1 ⊢
  have he : t*(1-x)+r*(1-y)=1-(t*x+r*y) := by nlinarith
  rw [he] at h1
  have hc0 : 0 ≤ p+(k:ℝ) := by positivity
  have hc1 : 0 ≤ ((n-k:ℕ):ℝ) := Nat.cast_nonneg _
  have hm0 := mul_le_mul_of_nonneg_left h0 hc0
  have hm1 := mul_le_mul_of_nonneg_left h1 hc1
  dsimp [logScore]
  nlinarith

lemma score_quasiconcave {a : ℕ → ℝ} {p : ℝ} (hp : 0 ≤ p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (hanti : Antitone a)
    (n k i j l : ℕ) (hij : i ≤ j) (hjl : j ≤ l) :
    min (score n k p (a i)) (score n k p (a l)) ≤ score n k p (a j) := by
  have hmem (t : ℕ) : a t ∈ Set.Ioo (0:ℝ) 1 :=
    ⟨hpos t, by have h := hhalf t; linarith⟩
  have h := (logScore_concave hp n k).min_le_of_mem_Icc
    (hmem l) (hmem i) (show a j ∈ Set.Icc (a l) (a i) from ⟨hanti hjl,hanti hij⟩)
  rw [score_eq_exp (hpos i) (hmem i).2,
    score_eq_exp (hpos l) (hmem l).2, score_eq_exp (hpos j) (hmem j).2]
  rcases le_total (logScore n k p (a i)) (logScore n k p (a l)) with hle | hle
  · rw [min_eq_right hle] at h
    rw [min_eq_left (Real.exp_le_exp.mpr hle)]
    exact Real.exp_le_exp.mpr h
  · rw [min_eq_left hle] at h
    rw [min_eq_right (Real.exp_le_exp.mpr hle)]
    exact Real.exp_le_exp.mpr h

/-- The actual countable Bernoulli score sequence has an attained mode and the
exact infinite adjacent-overlap identity, derived rather than assumed. -/
theorem score_mode_and_adjacent_identity {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n k : ℕ) :
    ∃ m : ℕ, (∀ i, score n k p (a i) ≤ score n k p (a m)) ∧
      (∑' i : ℕ, min (score n k p (a i)) (score n k p (a (i+1)))) =
        (∑' i : ℕ, score n k p (a i)) - score n k p (a m) := by
  have hs := score_summable hpos hhalf hsep hp n k
  have hpositive (i : ℕ) : 0 < score n k p (a i) :=
    score_pos (hpos i) (by have h := hhalf i; linarith) n k
  obtain ⟨m,hm⟩ := exists_mode_of_summable hs (hpositive 0)
  have hq := score_quasiconcave hp.le hpos hhalf (support_antitone hpos hsep) n k
  have hmode := mode_sides m hm hq
  exact ⟨m,hm,adjacent_min_tsum hs (fun i => (hpositive i).le) m hmode.1 hmode.2⟩

/-- No arbitrary real report can cover two points of the half-separated support. -/
lemma accepted_index_unique {a : ℕ → ℝ} {epsilon q : ℝ}
    (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2)
    (he : 0 < epsilon) (he4 : epsilon ≤ (1/4 : ℝ))
    (i j : ℕ) (hi : SparsePriorGeometry.Accepted (a i) epsilon q)
    (hj : SparsePriorGeometry.Accepted (a j) epsilon q) : i = j := by
  have hanti := support_antitone hpos hsep
  by_contra hne
  rcases lt_or_gt_of_ne hne with hij | hji
  · have hgap := (hanti (show i+1 ≤ j by omega)).trans (hsep i)
    exact SparsePriorGeometry.no_common_report_at_factor_two (hpos j) he he4
      (by linarith : 2*a j ≤ a i) ⟨hj,hi⟩
  · have hgap := (hanti (show j+1 ≤ i by omega)).trans (hsep j)
    exact SparsePriorGeometry.no_common_report_at_factor_two (hpos i) he he4
      (by linarith : 2*a i ≤ a j) ⟨hi,hj⟩

lemma own_report_accepted {x epsilon : ℝ} (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    SparsePriorGeometry.Accepted x epsilon ((1/2 : ℝ)+epsilon*x) := by
  have hm := SparsePriorGeometry.own_report_margin x epsilon
  have hp : 0 ≤ epsilon^2*x*(1-x) :=
    mul_nonneg (mul_nonneg (sq_nonneg _) hx) (sub_nonneg.mpr hx1)
  constructor
  · rw [hm.1]
    nlinarith
  · rw [hm.2]
    nlinarith

/-- The prior-weighted failure mass after one exact prefix. -/
def reportRisk (a : ℕ → ℝ) (n k : ℕ) (p epsilon q : ℝ) : ℝ := by
  classical
  exact ∑' i : ℕ, if SparsePriorGeometry.Accepted (a i) epsilon q
    then 0 else score n k p (a i)

lemma reportRisk_nonneg {a : ℕ → ℝ} {p epsilon q : ℝ}
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (n k : ℕ) :
    0 ≤ reportRisk a n k p epsilon q := by
  classical
  apply tsum_nonneg
  intro i
  split_ifs
  · rfl
  · exact (score_pos (hpos i) (by have h := hhalf i; linarith) n k).le

lemma reportRisk_of_accepted {a : ℕ → ℝ} {p epsilon q : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (n k j : ℕ)
    (hj : SparsePriorGeometry.Accepted (a j) epsilon q) :
    reportRisk a n k p epsilon q = (∑' i : ℕ, score n k p (a i)) - score n k p (a j) := by
  classical
  have hterm (i : ℕ) :
      (if SparsePriorGeometry.Accepted (a i) epsilon q then 0 else score n k p (a i)) =
      (if i=j then 0 else score n k p (a i)) := by
    by_cases hij : i=j
    · subst i
      simp [hj]
    · have hi : ¬ SparsePriorGeometry.Accepted (a i) epsilon q := by
        intro hi
        exact hij (accepted_index_unique hpos hsep he he4 i j hi hj)
      simp [hi,hij]
  unfold reportRisk
  simp_rw [hterm]
  have ht := (score_summable hpos hhalf hsep hp n k).tsum_eq_add_tsum_ite j
  linarith

lemma reportRisk_of_none {a : ℕ → ℝ} {p epsilon q : ℝ} (n k : ℕ)
    (hnone : ∀ i, ¬ SparsePriorGeometry.Accepted (a i) epsilon q) :
    reportRisk a n k p epsilon q = ∑' i : ℕ, score n k p (a i) := by
  classical
  simp [reportRisk,hnone]

/-- Exact countable conditional Bayes decision theorem for the repair loss.
It covers all real q, obtains an attained supported report, and derives the
adjacent-overlap expression from the actual Bernoulli score sequence. -/
theorem conditional_bayes_identification {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (n k : ℕ) :
    ∃ m : ℕ,
      (∀ q : ℝ, (∑' i : ℕ, min (score n k p (a i)) (score n k p (a (i+1)))) ≤
          reportRisk a n k p epsilon q) ∧
      reportRisk a n k p epsilon ((1/2 : ℝ)+epsilon*a m) =
        ∑' i : ℕ, min (score n k p (a i)) (score n k p (a (i+1))) := by
  classical
  obtain ⟨m,hm,hidentity⟩ := score_mode_and_adjacent_identity hp hpos hhalf hsep n k
  refine ⟨m,?_,?_⟩
  · intro q
    rw [hidentity]
    by_cases hex : ∃ j, SparsePriorGeometry.Accepted (a j) epsilon q
    · obtain ⟨j,hj⟩ := hex
      rw [reportRisk_of_accepted hp hpos hhalf hsep he he4 n k j hj]
      linarith [hm j]
    · have hnone : ∀ i, ¬ SparsePriorGeometry.Accepted (a i) epsilon q := by
        simpa only [not_exists] using hex
      rw [reportRisk_of_none n k hnone]
      have hsm := score_pos (hpos m) (by have h := hhalf m; linarith) n k (p:=p)
      linarith
  · rw [reportRisk_of_accepted hp hpos hhalf hsep he he4 n k m
      (own_report_accepted (hpos m).le (by have h := hhalf m; linarith)), hidentity]

/-- Optimal joint failure mass of one exact receipt prefix. -/
def optimalWordRisk (a : ℕ → ℝ) (n k : ℕ) (p : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (∑' i : ℕ, min (score n k p (a i)) (score n k p (a (i+1))))

lemma optimalWordRisk_eq_tsum {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n k : ℕ) :
    optimalWordRisk a n k p = ∑' i : ℕ,
      ENNReal.ofReal (min (score n k p (a i)) (score n k p (a (i+1)))) := by
  have hs := score_summable hpos hhalf hsep hp n k
  have h0 (i : ℕ) : 0 ≤ score n k p (a i) :=
    (score_pos (hpos i) (by have h := hhalf i; linarith) n k).le
  exact ENNReal.ofReal_tsum_of_nonneg
    (fun i => le_min (h0 i) (h0 (i+1))) (adjacent_min_summable hs h0)

/-- Grouping all full receipt words by their number of ones gives exactly the
finite-binomial overlap used in the analytic supplement. -/
theorem sum_optimal_words_eq_overlap {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n : ℕ) :
    (∑ S ∈ (range n).powerset, optimalWordRisk a n S.card p) =
      ∑' i : ℕ, ENNReal.ofReal (SparsePriorAnalytic.binaryOverlap (a i) (a (i+1)) p n) := by
  have hgroup (k : ℕ) :
      (∑ S ∈ powersetCard k (range n), optimalWordRisk a n S.card p) =
        (n.choose k : ℝ≥0∞) * optimalWordRisk a n k p := by
    simpa only [Finset.card_range, nsmul_eq_mul] using
      Finset.sum_powersetCard k (range n) (fun k => optimalWordRisk a n k p)
  rw [Finset.sum_powerset]
  simp only [Finset.card_range]
  simp_rw [hgroup, optimalWordRisk_eq_tsum hp hpos hhalf hsep, ← ENNReal.tsum_mul_left]
  rw [← Summable.tsum_finsetSum (fun k hk => ENNReal.summable)]
  apply tsum_congr
  intro i
  have hnonneg (k : ℕ) : 0 ≤ min (score n k p (a i)) (score n k p (a (i+1))) := by
    apply le_min
    · exact (score_pos (hpos i) (by have h := hhalf i; linarith) n k).le
    · exact (score_pos (hpos (i+1)) (by have h := hhalf (i+1); linarith) n k).le
  change _ = ENNReal.ofReal (∑ k ∈ range (n+1),
    (n.choose k : ℝ) * min (score n k p (a i)) (score n k p (a (i+1))))
  rw [ENNReal.ofReal_sum_of_nonneg (s := range (n+1))
    (f := fun k => (n.choose k : ℝ) * min (score n k p (a i)) (score n k p (a (i+1))))
    (fun k hk => mul_nonneg (Nat.cast_nonneg (n.choose k)) (hnonneg k))]
  apply sum_congr rfl
  intro k hk
  rw [ENNReal.ofReal_mul (Nat.cast_nonneg _)]
  simp only [ENNReal.ofReal_natCast, score]

/-- A deterministic policy may use the entire receipt word, represented by its
set of one positions, rather than only its count. -/
abbrev Policy := ℕ → Finset ℕ → ℝ

/-- Unnormalized expected lifetime failure mass in the explicit passive
Bernoulli finite-prefix experiment. Every counted report has n>=1. -/
def policyCost (a : ℕ → ℝ) (p epsilon : ℝ) (pi : Policy) : ℝ≥0∞ :=
  ∑' n : ℕ, ∑ S ∈ (range (n+1)).powerset,
    ENNReal.ofReal (reportRisk a (n+1) S.card p epsilon (pi (n+1) S))

/-- Universal real-report lower bound after summing all full words and times. -/
theorem policyCost_lower {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (pi : Policy) :
    SparsePriorAnalytic.overlapTotal a p ≤ policyCost a p epsilon pi := by
  apply ENNReal.tsum_le_tsum
  intro n
  rw [← sum_optimal_words_eq_overlap hp hpos hhalf hsep (n+1)]
  apply sum_le_sum
  intro S hS
  obtain ⟨m,hm,hatt⟩ := conditional_bayes_identification hp hpos hhalf hsep he he4 (n+1) S.card
  exact ENNReal.ofReal_le_ofReal (hm (pi (n+1) S))

/-- One common deterministic policy attains the explicit overlap series. -/
theorem exists_policyCost_eq {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    ∃ pi : Policy, policyCost a p epsilon pi = SparsePriorAnalytic.overlapTotal a p := by
  classical
  have hex : ∀ n k : ℕ, ∃ m : ℕ,
      reportRisk a n k p epsilon ((1/2 : ℝ)+epsilon*a m) =
      ∑' i : ℕ, min (score n k p (a i)) (score n k p (a (i+1))) := by
    intro n k
    obtain ⟨m,hm,hatt⟩ := conditional_bayes_identification hp hpos hhalf hsep he he4 n k
    exact ⟨m,hatt⟩
  choose m hm using hex
  let pi : Policy := fun n S => (1/2 : ℝ)+epsilon*a (m n S.card)
  refine ⟨pi,?_⟩
  apply tsum_congr
  intro n
  rw [← sum_optimal_words_eq_overlap hp hpos hhalf hsep (n+1)]
  apply sum_congr rfl
  intro S hS
  change ENNReal.ofReal (reportRisk a (n+1) S.card p epsilon
    ((1/2 : ℝ)+epsilon*a (m (n+1) S.card))) = _
  rw [hm (n+1) S.card]
  rfl

/-- Sharp iff for existence of a finite-cost full-history deterministic policy
in the explicit countable-prior Bernoulli prefix model. -/
theorem exists_finite_policyCost_iff {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    (∃ pi : Policy, policyCost a p epsilon pi < ⊤) ↔
      Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))) := by
  rw [← SparsePriorAnalytic.overlapTotal_finite_iff_summable a hp hpos hhalf hsep]
  constructor
  · rintro ⟨pi,hpi⟩
    exact lt_of_le_of_lt (policyCost_lower hp hpos hhalf hsep he he4 pi) hpi
  · intro h
    obtain ⟨pi,hpi⟩ := exists_policyCost_eq hp hpos hhalf hsep he he4
    exact ⟨pi,by rw [hpi]; exact h⟩

/-- Positive finite real normalizer for the power-weighted countable prior. -/
def normalizer (a : ℕ → ℝ) (p : ℝ) : ℝ := ∑' i : ℕ, (a i)^p

lemma normalizer_pos {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2) :
    0 < normalizer a p := by
  have hs := power_weights_summable hpos hsep hp
  have heq := hs.tsum_eq_add_tsum_ite 0
  have hrest : 0 ≤ ∑' i : ℕ, if i=0 then 0 else (a i)^p := by
    apply tsum_nonneg
    intro i
    split_ifs
    · rfl
    · exact Real.rpow_nonneg (hpos i).le p
  have hfirst := Real.rpow_pos_of_pos (hpos 0) p
  unfold normalizer
  linarith

def priorWeight (a : ℕ → ℝ) (p : ℝ) (i : ℕ) : ℝ := (a i)^p/normalizer a p

lemma priorWeight_pos {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2) (i : ℕ) :
    0 < priorWeight a p i :=
  div_pos (Real.rpow_pos_of_pos (hpos i) p) (normalizer_pos hp hpos hsep)

lemma priorWeight_sum_one {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2) :
    (∑' i : ℕ, priorWeight a p i) = 1 := by
  unfold priorWeight
  rw [tsum_div_const]
  exact div_self (ne_of_gt (normalizer_pos hp hpos hsep))

lemma sum_word_likelihood (x : ℝ) (n : ℕ) :
    (∑ S ∈ (range n).powerset, x^S.card*(1-x)^(n-S.card)) = 1 := by
  have hgroup (k : ℕ) :
      (∑ S ∈ powersetCard k (range n), x^S.card*(1-x)^(n-S.card)) =
        (n.choose k : ℝ) * (x^k*(1-x)^(n-k)) := by
    simpa only [Finset.card_range, nsmul_eq_mul] using
      Finset.sum_powersetCard k (range n) (fun k => x^k*(1-x)^(n-k))
  rw [Finset.sum_powerset]
  simp only [Finset.card_range]
  simp_rw [hgroup]
  calc
    _ = (x+(1-x))^n := by
      rw [add_pow]
      apply sum_congr rfl
      intro k hk
      ring
    _ = 1 := by simp

/-- The explicit Bernoulli-prefix mixture is normalized over every complete
set of receipt words. This verifies it is a finite-prefix probability law. -/
theorem sum_joint_word_mass_one {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n : ℕ) :
    (∑ S ∈ (range n).powerset, (∑' i : ℕ, score n S.card p (a i))/normalizer a p) = 1 := by
  rw [← sum_div]
  have htotal : (∑ S ∈ (range n).powerset, ∑' i : ℕ, score n S.card p (a i)) =
      normalizer a p := by
    have hswap := Summable.tsum_finsetSum
      (s := (range n).powerset) (f := fun (S : Finset ℕ) (i : ℕ) => score n S.card p (a i))
      (fun S _hS => score_summable hpos hhalf hsep hp n S.card)
    rw [← hswap]
    apply tsum_congr
    intro i
    calc
      _ = (a i)^p * (∑ S ∈ (range n).powerset, (a i)^S.card*(1-a i)^(n-S.card)) := by
        rw [mul_sum]
        apply sum_congr rfl
        intro S hS
        simp only [score]
        ring
      _ = (a i)^p := by rw [sum_word_likelihood]; ring
  rw [htotal]
  exact div_self (ne_of_gt (normalizer_pos hp hpos hsep))

def normalizationFactor (a : ℕ → ℝ) (p : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (1/normalizer a p)

lemma normalizationFactor_pos {a : ℕ → ℝ} {p : ℝ} (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2) :
    0 < normalizationFactor a p :=
  ENNReal.ofReal_pos.mpr (one_div_pos.mpr (normalizer_pos hp hpos hsep))

def normalizedPolicyCost (a : ℕ → ℝ) (p epsilon : ℝ) (pi : Policy) : ℝ≥0∞ :=
  normalizationFactor a p * policyCost a p epsilon pi

lemma normalizedPolicyCost_finite_iff {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hsep : ∀ i, a (i+1) ≤ a i/2)
    (pi : Policy) : normalizedPolicyCost a p epsilon pi < ⊤ ↔ policyCost a p epsilon pi < ⊤ := by
  constructor
  · intro h
    exact ENNReal.lt_top_of_mul_ne_top_right (ne_of_lt h)
      (ne_of_gt (normalizationFactor_pos hp hpos hsep))
  · intro h
    exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top h

lemma normalizedPolicyCost_lower {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (pi : Policy) :
    normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p ≤
      normalizedPolicyCost a p epsilon pi :=
  mul_le_mul_left' (policyCost_lower hp hpos hhalf hsep he he4 pi) _

open MeasureTheory

/-- The same seed selects an entire full-history policy. Its averaging law is
independent of the fixed prior and all receipt likelihoods in policyCost. -/
def randomizedCost {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    (a : ℕ → ℝ) (p epsilon : ℝ) (pi : Z → Policy) : ℝ≥0∞ :=
  ∫⁻ z, normalizedPolicyCost a p epsilon (pi z) ∂eta

/-- Arbitrary independent probability-space randomization cannot improve the
countable-prior Bayes lower bound. -/
theorem randomizedCost_lower {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (pi : Z → Policy) :
    normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p ≤
      randomizedCost eta a p epsilon pi := by
  have h : (∫⁻ _z : Z, normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p ∂eta) ≤
      randomizedCost eta a p epsilon pi :=
    lintegral_mono (fun z => normalizedPolicyCost_lower hp hpos hhalf hsep he he4 (pi z))
  simpa only [lintegral_const, measure_univ, mul_one] using h

/-- A constant-in-seed MAP policy is measurable in every report coordinate and
attains the normalized Bayes cost on any probability-space seed. -/
theorem exists_measurable_randomizedCost_eq {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    ∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      randomizedCost eta a p epsilon pi =
        normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p := by
  obtain ⟨pi,hpi⟩ := exists_policyCost_eq hp hpos hhalf hsep he he4
  refine ⟨fun _z => pi, (fun _n _S => measurable_const), ?_⟩
  simp only [randomizedCost, normalizedPolicyCost, hpi, lintegral_const, measure_univ, mul_one]

/-- End-to-end sharp normalized finite-budget iff, including arbitrary
full-history real reports and measurable probability-space seed randomization,
for the explicit passive Bernoulli finite-prefix risk model. -/
theorem exists_finite_randomizedCost_iff {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] {a : ℕ → ℝ} {p epsilon : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    (∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      randomizedCost eta a p epsilon pi < ⊤) ↔
      Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))) := by
  rw [← SparsePriorAnalytic.overlapTotal_finite_iff_summable a hp hpos hhalf hsep]
  constructor
  · rintro ⟨pi,_hmeas,hpi⟩
    have h := lt_of_le_of_lt (randomizedCost_lower eta hp hpos hhalf hsep he he4 pi) hpi
    exact ENNReal.lt_top_of_mul_ne_top_right (ne_of_lt h)
      (ne_of_gt (normalizationFactor_pos hp hpos hsep))
  · intro h
    obtain ⟨pi,hmeas,hpi⟩ := exists_measurable_randomizedCost_eq eta hp hpos hhalf hsep he he4
    refine ⟨pi,hmeas,?_⟩
    rw [hpi]
    exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top h

#print axioms score_mode_and_adjacent_identity
#print axioms conditional_bayes_identification
#print axioms sum_optimal_words_eq_overlap
#print axioms exists_finite_policyCost_iff
#print axioms priorWeight_sum_one
#print axioms sum_joint_word_mass_one
#print axioms randomizedCost_lower
#print axioms exists_finite_randomizedCost_iff
end
end SparsePriorBayes

/-! Actual infinite-process bridge. This block is new and remains separate from
all previously frozen certificates. The infinitePi construction follows the
retained third-return BernoulliPrefixLaw source, with explicit subset words. -/
namespace SparsePriorProcess
noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped ENNReal BigOperators
open SparsePriorBayes

abbrev Receipts := ℕ → Bool

def prefixSet (n : ℕ) (y : Receipts) : Finset ℕ :=
  (range n).filter (fun k => y k = true)

def prefixEvent (n : ℕ) (S : Finset ℕ) : Set Receipts := {y | prefixSet n y = S}

def decoder (S : Finset ℕ) (k : ℕ) : Bool := decide (k ∈ S)

lemma prefixSet_subset (n : ℕ) (y : Receipts) : prefixSet n y ⊆ range n :=
  filter_subset _ _

lemma prefixSet_eq_iff (n : ℕ) (S : Finset ℕ) (hS : S ⊆ range n) (y : Receipts) :
    prefixSet n y = S ↔ ∀ k, k<n → y k = decoder S k := by
  constructor
  · intro heq k hk
    have hm : (y k = true) ↔ k ∈ S := by
      have h : k ∈ prefixSet n y ↔ k ∈ S := by rw [heq]
      simpa only [prefixSet, mem_filter, mem_range, hk, true_and] using h
    cases hy : y k with
    | false =>
      have hnot : k ∉ S := by intro h; have := hm.mpr h; simp [hy] at this
      simp [decoder,hnot,hy]
    | true =>
      have hin : k ∈ S := hm.mp hy
      simp [decoder,hin,hy]
  · intro h
    apply Finset.ext
    intro k
    by_cases hk : k<n
    · have hy := h k hk
      simp [prefixSet, hk, hy, decoder]
    · have hnot : k ∉ S := by
        intro hi
        exact hk (mem_range.mp (hS hi))
      simp [prefixSet,hk,hnot]

lemma prefixEvent_eq_pi (n : ℕ) (S : Finset ℕ) (hS : S ⊆ range n) :
    prefixEvent n S = Set.pi (range n : Set ℕ) (fun k => {decoder S k}) := by
  ext y
  simp only [prefixEvent, Set.mem_setOf_eq, Set.mem_pi, mem_coe, mem_range, Set.mem_singleton_iff]
  exact prefixSet_eq_iff n S hS y

lemma prefixEvent_measurable (n : ℕ) (S : Finset ℕ) (hS : S ⊆ range n) :
    MeasurableSet (prefixEvent n S) := by
  rw [prefixEvent_eq_pi n S hS]
  exact MeasurableSet.pi (Set.to_countable _) (fun k hk => measurableSet_singleton _)

def coinMass (x : ℝ) (b : Bool) : ℝ := if b then x else 1-x

lemma coinMass_nonneg {x : ℝ} (hx : 0 ≤ x) (hx1 : x ≤ 1) (b : Bool) :
    0 ≤ coinMass x b := by cases b <;> simp [coinMass] <;> linarith

def sourceCoin (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) : PMF Bool :=
  PMF.ofFintype (fun b => ENNReal.ofReal (coinMass x b)) (by
    rw [Fintype.sum_bool, ← ENNReal.ofReal_add
      (coinMass_nonneg hx hx1 true) (coinMass_nonneg hx hx1 false)]
    simp [coinMass])

def sourceCoinMeasure (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) : Measure Bool :=
  (sourceCoin x hx hx1).toMeasure

instance sourceCoin_probability (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    IsProbabilityMeasure (sourceCoinMeasure x hx hx1) := by
  unfold sourceCoinMeasure
  infer_instance

def receiptLaw (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) : Measure Receipts :=
  Measure.infinitePi (fun _ : ℕ => sourceCoinMeasure x hx hx1)

instance receiptLaw_probability (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    IsProbabilityMeasure (receiptLaw x hx hx1) := by
  unfold receiptLaw
  infer_instance

lemma sourceCoin_singleton (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1) (b : Bool) :
    sourceCoinMeasure x hx hx1 {b} = ENNReal.ofReal (coinMass x b) := by
  unfold sourceCoinMeasure
  rw [PMF.toMeasure_apply_singleton _ b (measurableSet_singleton b)]
  rfl

lemma decoder_product (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1)
    (n : ℕ) (S : Finset ℕ) (hS : S ⊆ range n) :
    (∏ k ∈ range n, ENNReal.ofReal (coinMass x (decoder S k))) =
      ENNReal.ofReal (x^S.card*(1-x)^(n-S.card)) := by
  rw [← ENNReal.ofReal_prod_of_nonneg (fun k hk => coinMass_nonneg hx hx1 (decoder S k))]
  congr 1
  simp only [coinMass,decoder,Bool.decide_coe,decide_eq_true_eq]
  rw [Finset.prod_ite]
  have hfilter : (range n).filter (fun k => k ∈ S) = S := by
    ext k
    simp only [mem_filter]
    exact ⟨fun h => h.2,fun h => ⟨hS h,h⟩⟩
  have hfilter' : (range n).filter (fun k => k ∉ S) = range n \ S := by
    ext k
    simp
  rw [hfilter,hfilter']
  simp only [Finset.prod_const, Finset.card_sdiff hS, Finset.card_range]

/-- Actual iid infinite-product law has the required finite-word marginals. -/
theorem receiptLaw_prefix_mass (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1)
    (n : ℕ) (S : Finset ℕ) (hS : S ⊆ range n) :
    receiptLaw x hx hx1 (prefixEvent n S) = ENNReal.ofReal (x^S.card*(1-x)^(n-S.card)) := by
  rw [prefixEvent_eq_pi n S hS, receiptLaw,
    Measure.infinitePi_pi _ (fun k hk => measurableSet_singleton _)]
  simp_rw [sourceCoin_singleton]
  exact decoder_product x hx hx1 n S hS

/-- Draw one latent support index once; conditional on it, retain the entire
infinite iid Bernoulli stream. -/
def latentLaw (a : ℕ → ℝ) (p : ℝ) (_hp : 0 < p) (hpos : ∀ i, 0 < a i)
    (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (_hsep : ∀ i, a (i+1) ≤ a i/2) :
    Measure (ℕ × Receipts) :=
  Measure.sum (fun i => ENNReal.ofReal (priorWeight a p i) •
    (Measure.dirac i).prod (receiptLaw (a i) (hpos i).le (by have h := hhalf i; linarith)))

instance latentLaw_probability (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) : IsProbabilityMeasure (latentLaw a p hp hpos hhalf hsep) := by
  constructor
  unfold latentLaw
  rw [Measure.sum_apply _ MeasurableSet.univ]
  simp only [Measure.smul_apply, smul_eq_mul, measure_univ, mul_one]
  have hs : Summable (fun i => priorWeight a p i) :=
    (power_weights_summable hpos hsep hp).div_const (normalizer a p)
  rw [← ENNReal.ofReal_tsum_of_nonneg (fun i => (priorWeight_pos hp hpos hsep i).le) hs,
    priorWeight_sum_one hp hpos hsep]
  simp

/-- The seed is independent of the latent index and the entire receipt stream
by construction of the outer product law. -/
def experimentLaw {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p) (hpos : ∀ i, 0 < a i)
    (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (hsep : ∀ i, a (i+1) ≤ a i/2) :
    Measure (Z × (ℕ × Receipts)) := eta.prod (latentLaw a p hp hpos hhalf hsep)

instance experimentLaw_probability {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p) (hpos : ∀ i, 0 < a i)
    (hhalf : ∀ i, a i ≤ (1/2 : ℝ)) (hsep : ∀ i, a (i+1) ≤ a i/2) :
    IsProbabilityMeasure (experimentLaw eta a p hp hpos hhalf hsep) := by
  unfold experimentLaw
  infer_instance

/-- Finite partition by complete observed words. -/
lemma prefix_partition (n : ℕ) (y : Receipts) (f : Finset ℕ → ℝ≥0∞) :
    f (prefixSet n y) = ∑ S ∈ (range n).powerset,
      if prefixSet n y = S then f S else 0 := by
  classical
  rw [Finset.sum_ite_eq]
  simp only [Finset.mem_powerset, prefixSet_subset, if_true]

/-- Exact literal failure indicator. -/
def literalFailure (x epsilon q : ℝ) : ℝ≥0∞ := by
  classical
  exact if SparsePriorGeometry.Accepted x epsilon q then 0 else 1

lemma literalFailure_measurable {Z : Type*} [MeasurableSpace Z] {f : Z → ℝ}
    (hf : Measurable f) (x epsilon : ℝ) : Measurable (fun z => literalFailure x epsilon (f z)) := by
  classical
  have h0 : Measurable (fun z => (f z)^2-(1/4 : ℝ)-x*epsilon*(1+epsilon)) := by fun_prop
  have h1 : Measurable (fun z => (1-f z)^2-(1/4 : ℝ)+x*epsilon*(1-epsilon)) := by fun_prop
  have hA : MeasurableSet {z | SparsePriorGeometry.Accepted x epsilon (f z)} :=
    (measurableSet_le h0 measurable_const).inter (measurableSet_le h1 measurable_const)
  exact Measurable.ite hA measurable_const measurable_const

/-- Per-report literal loss evaluated on the observed prefix only. -/
def stageFailure {Z : Type*} (a : ℕ → ℝ) (epsilon : ℝ) (pi : Z → Policy)
    (n : ℕ) (omega : Z × (ℕ × Receipts)) : ℝ≥0∞ :=
  literalFailure (a omega.2.1) epsilon (pi omega.1 n (prefixSet n omega.2.2))

/-- Every report coordinate is measurable whenever the seed's policy
coordinates are measurable. No unobserved receipt is used. -/
lemma stageFailure_measurable {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (epsilon : ℝ) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) (n : ℕ) :
    Measurable (stageFailure a epsilon pi n) := by
  classical
  have hfixed (i : ℕ) : Measurable (fun zy : Z × Receipts =>
      literalFailure (a i) epsilon (pi zy.1 n (prefixSet n zy.2))) := by
    have hpart (S : Finset ℕ) (hS : S ∈ (range n).powerset) :
        Measurable (fun zy : Z × Receipts =>
          if prefixSet n zy.2 = S then literalFailure (a i) epsilon (pi zy.1 n S) else 0) := by
      have he : MeasurableSet {zy : Z × Receipts | prefixSet n zy.2 = S} :=
        (prefixEvent_measurable n S (mem_powerset.mp hS)).preimage measurable_snd
      exact Measurable.ite he
        ((literalFailure_measurable (hpi n S) (a i) epsilon).comp measurable_fst) measurable_const
    have hsum := ((range n).powerset).measurable_sum hpart
    convert hsum using 1
    funext zy
    exact prefix_partition n zy.2 (fun S => literalFailure (a i) epsilon (pi zy.1 n S))
  have hc : Measurable (fun zyi : (Z × Receipts) × ℕ =>
      literalFailure (a zyi.2) epsilon (pi zyi.1.1 n (prefixSet n zyi.1.2))) :=
    measurable_from_prod_countable hfixed
  exact hc.comp ((measurable_fst.prodMk (measurable_snd.snd)).prodMk (measurable_snd.fst))

/-- Literal total count, with report indices one through infinity. -/
def totalFailures {Z : Type*} (a : ℕ → ℝ) (epsilon : ℝ) (pi : Z → Policy)
    (omega : Z × (ℕ × Receipts)) : ℝ≥0∞ := ∑' n : ℕ, stageFailure a epsilon pi (n+1) omega

lemma totalFailures_measurable {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (epsilon : ℝ) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) : Measurable (totalFailures a epsilon pi) :=
  Measurable.ennreal_tsum (fun n => stageFailure_measurable a epsilon pi hpi (n+1))

/-- Integrating any function of one observed prefix uses the derived cylinder
masses of the actual infinite product law. -/
lemma lintegral_prefix_function (x : ℝ) (hx : 0 ≤ x) (hx1 : x ≤ 1)
    (n : ℕ) (f : Finset ℕ → ℝ≥0∞) :
    (∫⁻ y, f (prefixSet n y) ∂receiptLaw x hx hx1) =
      ∑ S ∈ (range n).powerset, f S * ENNReal.ofReal (x^S.card*(1-x)^(n-S.card)) := by
  classical
  have hpart (S : Finset ℕ) (hS : S ∈ (range n).powerset) :
      Measurable (fun y : Receipts => if prefixSet n y = S then f S else 0) :=
    Measurable.ite (prefixEvent_measurable n S (mem_powerset.mp hS)) measurable_const measurable_const
  calc
    _ = ∫⁻ y, ∑ S ∈ (range n).powerset, if prefixSet n y = S then f S else 0 ∂receiptLaw x hx hx1 := by
      apply lintegral_congr
      intro y
      exact prefix_partition n y f
    _ = ∑ S ∈ (range n).powerset,
        ∫⁻ y, (if prefixSet n y = S then f S else 0) ∂receiptLaw x hx hx1 :=
      lintegral_finset_sum _ hpart
    _ = _ := by
      apply sum_congr rfl
      intro S hS
      have hsub := mem_powerset.mp hS
      have hind : (fun y : Receipts => if prefixSet n y = S then f S else 0) =
          (prefixEvent n S).indicator (fun _y => f S) := by
        funext y
        simp [prefixEvent,Set.indicator_apply]
      rw [hind, lintegral_indicator (prefixEvent_measurable n S hsub), lintegral_const,
        Measure.restrict_apply_univ, receiptLaw_prefix_mass x hx hx1 n S hsub]

/-- Integral decomposition of the actual fixed-latent-index mixture law. -/
lemma latentLaw_lintegral (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (f : ℕ × Receipts → ℝ≥0∞) (hf : Measurable f) :
    (∫⁻ iy, f iy ∂latentLaw a p hp hpos hhalf hsep) =
      ∑' i : ℕ, ENNReal.ofReal (priorWeight a p i) *
        ∫⁻ y, f (i,y) ∂receiptLaw (a i) (hpos i).le (by have h := hhalf i; linarith) := by
  unfold latentLaw
  rw [lintegral_sum_measure]
  apply tsum_congr
  intro i
  rw [lintegral_smul_measure, smul_eq_mul,
    lintegral_prod f hf.aemeasurable, lintegral_dirac]

lemma ofReal_reportRisk_eq_tsum {a : ℕ → ℝ} {p epsilon q : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n k : ℕ) :
    ENNReal.ofReal (reportRisk a n k p epsilon q) =
      ∑' i : ℕ, ENNReal.ofReal (score n k p (a i)) * literalFailure (a i) epsilon q := by
  classical
  let g : ℕ → ℝ := fun i => if SparsePriorGeometry.Accepted (a i) epsilon q
    then 0 else score n k p (a i)
  have hscore (i : ℕ) : 0 ≤ score n k p (a i) :=
    (score_pos (hpos i) (by have h := hhalf i; linarith) n k).le
  have hg0 (i : ℕ) : 0 ≤ g i := by
    dsimp [g]
    split_ifs
    · rfl
    · exact hscore i
  have hgle (i : ℕ) : g i ≤ score n k p (a i) := by
    dsimp [g]
    split_ifs
    · exact hscore i
    · rfl
  have hgs : Summable g := Summable.of_nonneg_of_le hg0 hgle
    (score_summable hpos hhalf hsep hp n k)
  change ENNReal.ofReal (∑' i, g i) = _
  rw [ENNReal.ofReal_tsum_of_nonneg hg0 hgs]
  apply tsum_congr
  intro i
  by_cases h : SparsePriorGeometry.Accepted (a i) epsilon q <;> simp [g,literalFailure,h]

lemma weighted_likelihood_identity {a : ℕ → ℝ} {p : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (_hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n k i : ℕ) :
    ENNReal.ofReal (priorWeight a p i) * ENNReal.ofReal ((a i)^k*(1-a i)^(n-k)) =
      normalizationFactor a p * ENNReal.ofReal (score n k p (a i)) := by
  unfold normalizationFactor
  rw [← ENNReal.ofReal_mul (priorWeight_pos hp hpos hsep i).le,
    ← ENNReal.ofReal_mul (one_div_nonneg.mpr (normalizer_pos hp hpos hsep).le)]
  congr 1
  unfold priorWeight score
  ring

lemma weighted_failure_sum {a : ℕ → ℝ} {p epsilon q : ℝ}
    (hp : 0 < p) (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (n k : ℕ) :
    (∑' i : ℕ, ENNReal.ofReal (priorWeight a p i) *
      (literalFailure (a i) epsilon q * ENNReal.ofReal ((a i)^k*(1-a i)^(n-k)))) =
      normalizationFactor a p * ENNReal.ofReal (reportRisk a n k p epsilon q) := by
  rw [ofReal_reportRisk_eq_tsum hp hpos hhalf hsep, ← ENNReal.tsum_mul_left]
  apply tsum_congr
  intro i
  calc
    _ = (ENNReal.ofReal (priorWeight a p i) *
          ENNReal.ofReal ((a i)^k*(1-a i)^(n-k))) * literalFailure (a i) epsilon q := by ring
    _ = _ := by rw [weighted_likelihood_identity hp hpos hhalf hsep]; ring

/-- Identification of each actual stage expectation, conditional on one fixed
seed value, with the normalized full-word risk sum. -/
theorem stage_expectation_eq_prefix_risk {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) (z : Z) (n : ℕ) :
    (∫⁻ iy, stageFailure a epsilon pi n (z,iy) ∂latentLaw a p hp hpos hhalf hsep) =
      normalizationFactor a p * ∑ S ∈ (range n).powerset,
        ENNReal.ofReal (reportRisk a n S.card p epsilon (pi z n S)) := by
  have hf : Measurable (fun iy : ℕ × Receipts => stageFailure a epsilon pi n (z,iy)) :=
    (stageFailure_measurable a epsilon pi hpi n).comp (measurable_const.prodMk measurable_id)
  rw [latentLaw_lintegral a p hp hpos hhalf hsep _ hf]
  simp only [stageFailure]
  have hsource (i : ℕ) :
      (∫⁻ y, literalFailure (a i) epsilon (pi z n (prefixSet n y))
        ∂receiptLaw (a i) (hpos i).le (by have h := hhalf i; linarith)) =
      ∑ S ∈ (range n).powerset, literalFailure (a i) epsilon (pi z n S) *
        ENNReal.ofReal ((a i)^S.card*(1-a i)^(n-S.card)) :=
    lintegral_prefix_function (a i) (hpos i).le (by have h := hhalf i; linarith)
      n (fun S => literalFailure (a i) epsilon (pi z n S))
  simp_rw [hsource]
  simp_rw [mul_sum]
  rw [Summable.tsum_finsetSum (s := (range n).powerset)
    (f := fun (S : Finset ℕ) (i : ℕ) => ENNReal.ofReal (priorWeight a p i) *
      (literalFailure (a i) epsilon (pi z n S) * ENNReal.ofReal ((a i)^S.card*(1-a i)^(n-S.card))))
    (fun _S _hS => ENNReal.summable)]
  simp_rw [weighted_failure_sum hp hpos hhalf hsep]

/-- Tonelli identifies the literal infinite total-count expectation after a
fixed seed with the already checked normalized policy cost. -/
theorem conditional_total_expectation_eq {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) (z : Z) :
    (∫⁻ iy, totalFailures a epsilon pi (z,iy) ∂latentLaw a p hp hpos hhalf hsep) =
      normalizedPolicyCost a p epsilon (pi z) := by
  unfold totalFailures
  have hm (n : ℕ) : Measurable (fun iy : ℕ × Receipts => stageFailure a epsilon pi (n+1) (z,iy)) :=
    (stageFailure_measurable a epsilon pi hpi (n+1)).comp
      ((measurable_const : Measurable (fun _iy : ℕ × Receipts => z)).prodMk measurable_id)
  rw [lintegral_tsum (f := fun n (iy : ℕ × Receipts) => stageFailure a epsilon pi (n+1) (z,iy))
    (fun n => (hm n).aemeasurable)]
  simp_rw [stage_expectation_eq_prefix_risk a p epsilon hp hpos hhalf hsep pi hpi z]
  rw [ENNReal.tsum_mul_left]
  rfl

/-- Actual abstract infinite-process expectation equals the checked seeded
prefix-risk functional. This equality is derived from the constructed product
measure and proved finite-word marginals, not assumed. -/
theorem actual_expectation_eq_randomizedCost {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) :
    (∫⁻ omega, totalFailures a epsilon pi omega ∂experimentLaw eta a p hp hpos hhalf hsep) =
      randomizedCost eta a p epsilon pi := by
  unfold experimentLaw
  rw [lintegral_prod _ (totalFailures_measurable a epsilon pi hpi).aemeasurable]
  simp_rw [conditional_total_expectation_eq a p epsilon hp hpos hhalf hsep pi hpi]
  rfl

/-- Universal lower bound for actual expected literal count under the
constructed one-time-latent-draw infinite receipt process. -/
theorem actual_expectation_lower {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) [IsProbabilityMeasure eta]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) (pi : Z → Policy)
    (hpi : ∀ n S, Measurable (fun z => pi z n S)) :
    normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p ≤
      ∫⁻ omega, totalFailures a epsilon pi omega ∂experimentLaw eta a p hp hpos hhalf hsep := by
  rw [actual_expectation_eq_randomizedCost eta a p epsilon hp hpos hhalf hsep pi hpi]
  exact randomizedCost_lower eta hp hpos hhalf hsep he he4 pi

/-- A common measurable policy attains the normalized overlap cost as an actual
expected count under the infinite receipt process. -/
theorem exists_actual_expectation_eq {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) [IsProbabilityMeasure eta]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    ∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∫⁻ omega, totalFailures a epsilon pi omega ∂experimentLaw eta a p hp hpos hhalf hsep) =
        normalizationFactor a p * SparsePriorAnalytic.overlapTotal a p := by
  obtain ⟨pi,hpi,heq⟩ := exists_measurable_randomizedCost_eq eta hp hpos hhalf hsep he he4
  refine ⟨pi,hpi,?_⟩
  rw [actual_expectation_eq_randomizedCost eta a p epsilon hp hpos hhalf hsep pi hpi]
  exact heq

/-- End-to-end sharp finite expected literal-count criterion for the actual
fixed-parameter, independent-seed, infinite passive Bernoulli receipt process.
All base assumptions are explicit; the expected-count/risk-series identity
is proved above and is not a premise. -/
theorem exists_finite_actual_expectation_iff {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) [IsProbabilityMeasure eta]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ)) :
    (∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∫⁻ omega, totalFailures a epsilon pi omega ∂experimentLaw eta a p hp hpos hhalf hsep) < ⊤) ↔
      Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))) := by
  constructor
  · rintro ⟨pi,hpi,hfin⟩
    rw [actual_expectation_eq_randomizedCost eta a p epsilon hp hpos hhalf hsep pi hpi] at hfin
    exact (exists_finite_randomizedCost_iff eta hp hpos hhalf hsep he he4).mp ⟨pi,hpi,hfin⟩
  · intro hsum
    obtain ⟨pi,hpi,hfin⟩ := (exists_finite_randomizedCost_iff eta hp hpos hhalf hsep he he4).mpr hsum
    refine ⟨pi,hpi,?_⟩
    rw [actual_expectation_eq_randomizedCost eta a p epsilon hp hpos hhalf hsep pi hpi]
    exact hfin

/-- Divergence of the structural spacing series excludes every allowed policy,
not merely the empirical or MAP policy. -/
theorem every_policy_infinite_of_not_summable {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) [IsProbabilityMeasure eta]
    (a : ℕ → ℝ) (p epsilon : ℝ) (hp : 0 < p)
    (hpos : ∀ i, 0 < a i) (hhalf : ∀ i, a i ≤ (1/2 : ℝ))
    (hsep : ∀ i, a (i+1) ≤ a i/2) (he : 0 < epsilon)
    (he4 : epsilon ≤ (1/4 : ℝ))
    (hnot : ¬ Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))))
    (pi : Z → Policy) (hpi : ∀ n S, Measurable (fun z => pi z n S)) :
    (∫⁻ omega, totalFailures a epsilon pi omega ∂experimentLaw eta a p hp hpos hhalf hsep) = ⊤ := by
  by_contra hne
  have hfin := lt_top_iff_ne_top.mpr hne
  exact hnot ((exists_finite_actual_expectation_iff eta a p epsilon hp hpos hhalf hsep he he4).mp
    ⟨pi,hpi,hfin⟩)

#print axioms receiptLaw_prefix_mass
#print axioms latentLaw_probability
#print axioms totalFailures_measurable
#print axioms actual_expectation_eq_randomizedCost
#print axioms actual_expectation_lower
#print axioms exists_actual_expectation_eq
#print axioms exists_finite_actual_expectation_iff
#print axioms every_policy_infinite_of_not_summable
end
end SparsePriorProcess
