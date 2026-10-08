import FeedbackRequests
import IndependentProductFamilies
import PolicyRowLaw

noncomputable section
open MeasureTheory ProbabilityTheory Set Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u
variable {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

abbrev FlatStack (A Y : Type u) := (A × ℕ) → Y
abbrev RowOracle (A Y : Type u) := ℕ → A → Y

def actionMeasure (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (a : A) : Measure Y :=
  (rowMeasure P hP hN).map (fun w => w a)
instance actionMeasure_probability (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) : IsProbabilityMeasure (actionMeasure P hP hN a) := by
  unfold actionMeasure
  exact isProbabilityMeasure_map (measurable_pi_apply a).aemeasurable
lemma actionMeasure_singleton (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) (y : Y) :
    actionMeasure P hP hN a {y} = ENNReal.ofReal (P a y) := by
  rw [actionMeasure,Measure.map_apply (measurable_pi_apply a) (measurableSet_singleton y)]
  exact rowMeasure_coordinate P hP hN a y

def stackMeasure (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : Measure (FlatStack A Y) :=
  Measure.infinitePi (fun an : A × ℕ => actionMeasure P hP hN an.1)
instance stackMeasure_probability (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) : IsProbabilityMeasure (stackMeasure P hP hN) := by
  unfold stackMeasure
  infer_instance

def feedbackLaw (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    Measure (FlatStack A Y × RowOracle A Y) :=
  (stackMeasure base hb hbn).prod (FiniteAlphabetQuery.iidOracle (rowMeasure P hP hN))

instance feedbackLaw_probability (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    IsProbabilityMeasure (feedbackLaw base P hb hbn hP hN) := by
  unfold feedbackLaw
  infer_instance

/-- One fixed common base law is used for every stack coordinate, including
unused outside-U entries. It is not silently changed to the rival's law. -/
def sourceFamily : (k : FeedbackKey A) → FlatStack A Y × RowOracle A Y → FamilyValue Y (A → Y) k :=
  productFamily (fun an X => X an) (fun n oracle => oracle n)

def sourceRead : (k : FeedbackKey A) → A → FamilyValue Y (A → Y) k → Y
  | Sum.inl _, _, y => y
  | Sum.inr _, a, row => row a

omit [Fintype A] [Fintype Y] [DecidableEq A] [MeasurableSingletonClass Y] in
lemma sourceRead_measurable (k : FeedbackKey A) (a : A) : Measurable (sourceRead (Y := Y) k a) := by
  cases k
  · exact measurable_id
  · exact measurable_pi_apply a

def transcriptSample (U : Finset A) (h : History A Y) (i : Fin h.length)
    (ω : FlatStack A Y × RowOracle A Y) : Y :=
  readFeedback (fun a n => ω.1 (a,n)) ω.2 (requestKey U h i) h[i].1

omit [Fintype A] [Fintype Y] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma transcriptSample_eq_source (U : Finset A) (h : History A Y) (i : Fin h.length) :
    transcriptSample U h i = sourceRead (requestKey U h i) h[i].1 ∘ sourceFamily (requestKey U h i) := by
  funext ω
  cases hk : requestKey U h i <;> simp [transcriptSample,hk,readFeedback,sourceRead,sourceFamily,productFamily]

omit [MeasurableSingletonClass Y] in
/-- Freshness is proved from the actual independent product laws and the
injectivity of the fixed transcript's consulted latent slots. -/
theorem transcriptSamples_independent (U : Finset A) (h : History A Y) (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) :
    iIndepFun (transcriptSample U h) (feedbackLaw base P hb hbn hP hN) := by
  have hs : iIndepFun (sourceFamily (A := A) (Y := Y)) (feedbackLaw base P hb hbn hP hN) :=
    independent_product_families _ _ _ _
      (infinite_product_coordinates_independent (fun an : A × ℕ => actionMeasure base hb hbn an.1))
      (infinite_product_coordinates_independent (fun _ : ℕ => rowMeasure P hP hN))
  have hi := (hs.precomp (requestKey_injective U h)).comp
    (fun i => sourceRead (requestKey U h i) h[i].1)
    (fun i => sourceRead_measurable _ _)
  have heq : transcriptSample U h = fun i => sourceRead (requestKey U h i) h[i].1 ∘ sourceFamily (requestKey U h i) := by
    funext i
    exact transcriptSample_eq_source U h i
  rw [heq]
  exact hi

lemma feedbackLaw_left_marginal (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (n : ℕ) (y : Y) :
    feedbackLaw base P hb hbn hP hN {ω | ω.1 (a,n) = y} = ENNReal.ofReal (base a y) := by
  have hs : {ω : FlatStack A Y × RowOracle A Y | ω.1 (a,n) = y} =
      {X | X (a,n) = y} ×ˢ Set.univ := by ext ω; simp
  rw [feedbackLaw,hs,Measure.prod_prod,measure_univ,mul_one]
  change stackMeasure base hb hbn ((fun X => X (a,n)) ⁻¹' {y}) = _
  rw [← Measure.map_apply (measurable_pi_apply (a,n)) (measurableSet_singleton y),
    stackMeasure,infinite_product_coordinate_law]
  exact actionMeasure_singleton base hb hbn a y

lemma feedbackLaw_right_marginal (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (a : A) (n : ℕ) (y : Y) :
    feedbackLaw base P hb hbn hP hN {ω | ω.2 n a = y} = ENNReal.ofReal (P a y) := by
  have hs : {ω : FlatStack A Y × RowOracle A Y | ω.2 n a = y} =
      Set.univ ×ˢ {oracle | oracle n a = y} := by ext ω; simp
  rw [feedbackLaw,hs,Measure.prod_prod,measure_univ,one_mul]
  change FiniteAlphabetQuery.iidOracle (rowMeasure P hP hN)
    ((fun oracle => oracle n) ⁻¹' {row : A → Y | row a = y}) = _
  have hm : Measurable (fun oracle : RowOracle A Y => oracle n) := measurable_pi_apply n
  have hset : MeasurableSet {row : A → Y | row a = y} :=
    (measurableSet_singleton y).preimage (measurable_pi_apply a)
  rw [← Measure.map_apply hm hset, FiniteAlphabetQuery.iidOracle,infinite_product_coordinate_law]
  exact rowMeasure_coordinate P hP hN a y

theorem transcriptSample_marginal (U : Finset A) (h : History A Y) (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) (i : Fin h.length) :
    feedbackLaw base P hb hbn hP hN {ω | transcriptSample U h i ω = h[i].2} =
      ENNReal.ofReal (P h[i].1 h[i].2) := by
  rcases requestKey_branch U h i with ⟨⟨n,hk⟩,ha⟩ | ⟨⟨n,hk⟩,_⟩
  · simp only [transcriptSample,hk,readFeedback]
    rw [feedbackLaw_left_marginal, hagree _ ha]
  · simp only [transcriptSample,hk,readFeedback]
    exact feedbackLaw_right_marginal base P hb hbn hP hN _ n _

/-- Exact P3 feedback-fiber probability, derived from fresh product coordinates.
Only the U coordinates of the one common stack law must agree with P. -/
theorem feedbackCompatible_probability (U : Finset A) (h : History A Y) (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) :
    feedbackLaw base P hb hbn hP hN {ω | FeedbackCompatible U (fun a n => ω.1 (a,n)) ω.2 h} =
      ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2) := by
  have hs : {ω : FlatStack A Y × RowOracle A Y | FeedbackCompatible U (fun a n => ω.1 (a,n)) ω.2 h} =
      ⋂ i ∈ (Finset.univ : Finset (Fin h.length)), (transcriptSample U h i) ⁻¹' {h[i].2} := by
    ext ω
    simp only [Set.mem_setOf_eq,Set.mem_iInter,Finset.mem_univ,true_implies,Set.mem_preimage,Set.mem_singleton_iff]
    exact feedbackCompatible_iff_requests U (fun a n => ω.1 (a,n)) ω.2 h
  rw [hs,(transcriptSamples_independent U h base P hb hbn hP hN).measure_inter_preimage_eq_mul
    _ (fun i _ => measurableSet_singleton h[i].2)]
  apply Finset.prod_congr rfl
  intro i _
  exact transcriptSample_marginal U h base P hb hbn hP hN hagree i

end Orthemology.Tranche2.PolicyEmbedding
