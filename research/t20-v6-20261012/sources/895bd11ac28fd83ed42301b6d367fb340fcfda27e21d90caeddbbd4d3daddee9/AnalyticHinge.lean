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
