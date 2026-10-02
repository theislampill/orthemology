import ANDIntrinsic
import ConstraintBounds

set_option maxHeartbeats 1200000
noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection ANDScore ANDRepair ANDPotentialBinding PolynomialBounds

namespace ExplicitANDScale

structure Data where
  s : ℝ
  z : ℝ
  w : ℝ
  h1 : ℝ
  h2 : ℝ
  hz : ℝ
  hw : ℝ

namespace Data

def valid (d : Data) : Prop :=
  0 < d.s ∧ d.s < d.z ∧ d.s < d.w ∧ d.z+d.w < 1+d.s ∧ d.h1 ≠ d.h2

def e (d : Data) : ℝ := variance d.h1 d.h2
def b (d : Data) : ℝ := beta d.s (d.z+d.w) d.e
def g (d : Data) : ℝ := gamma d.s (d.z+d.w) d.e
def p0 (d : Data) : Fin 4 → ℝ := ![d.s,d.s,d.z,d.w]
def hvec (d : Data) : Fin 4 → ℝ := ![d.h1,d.h2,d.hz,d.hw]
def bary0 (d : Data) : Fin 4 → ℝ := ![1+d.s-d.z-d.w,d.z-d.s,d.w-d.s,d.s]
def bary1 (d : Data) : Fin 4 → ℝ :=
  ![mean d.h1 d.h2-d.hz-d.hw,d.hz-mean d.h1 d.h2,d.hw-mean d.h1 d.h2,mean d.h1 d.h2]
def bary2 (d : Data) : Fin 4 → ℝ := ![d.b-2*d.g,d.g-d.b,d.g-d.b,d.b]

def input (d : Data) (eps : ℝ) : Fin 4 → ℝ := baseline d.s d.z d.w d.h1 d.h2 d.hz d.hw eps
def output (d : Data) (eps : ℝ) : Fin 4 → ℝ := candidate d.s d.z d.w d.h1 d.h2 d.hz d.hw eps

def gHead (d : Data) (i : Fin 4) : ℝ := leadG d.s (d.z+d.w) d.e (truth i 0) (truth i 2+truth i 3)
def fHead (d : Data) (i : Fin 4) : ℝ := leadF d.s (d.z+d.w) d.e (truth i 0) (truth i 2+truth i 3)

def heads (d : Data) (j : Fin 5 × Fin 4) : ℝ :=
  ![d.gHead,d.fHead,d.bary0,d.p0,(fun i => 1-d.p0 i)] j.1 j.2

def budgets (d : Data) (j : Fin 5 × Fin 4) : ℝ :=
  ![(fun _ => budget (gCoefficients d.h1 d.h2 d.hz d.hw d.b d.g)),
    (fun i => budget (fCoefficients d.s (truth i 0) d.h1 d.h2 d.hz d.hw d.b d.g)),
    (fun i => |d.bary1 i|+|d.bary2 i|),
    (fun i => |d.hvec i|),(fun i => |d.hvec i|)] j.1 j.2

def rem (d : Data) (j : Fin 5 × Fin 4) (eps : ℝ) : ℝ :=
  ![(fun _ => gRem d.h1 d.h2 d.hz d.hw d.b d.g eps),
    (fun i => fRem d.s (truth i 0) d.h1 d.h2 d.hz d.hw d.b d.g eps),
    (fun i => d.bary1 i+eps*d.bary2 i),d.hvec,(fun i => -d.hvec i)] j.1 j.2

/-- A finite rational expression when the supplied context and direction are rational. -/
def delta (d : Data) : ℝ := ConstraintBounds.radius d.heads d.budgets

def constraints (d : Data) (j : Fin 5 × Fin 4) (eps : ℝ) : ℝ :=
  ![(fun i => insideG d.s d.z d.w d.h1 d.h2 d.hz d.hw i eps),
    (fun i => insideF d.s d.z d.w d.h1 d.h2 d.hz d.hw i eps),
    (fun i => bary d.s d.z d.w d.h1 d.h2 d.hz d.hw eps i),
    d.input eps,(fun i => 1-d.input eps i)] j.1 j.2

lemma score_heads_positive (d : Data) (hd : d.valid) :
    ∀ i : Fin 4, 0 < d.gHead i ∧ 0 < d.fHead i := by
  obtain ⟨hs,hz,hw,hsum,hne⟩ := hd
  have hs1 : d.s < 1 := by linarith
  have hT0 : 2*d.s < d.z+d.w := by linarith
  have hh := all_leading_positive d.s (d.z+d.w) d.e hs hs1 hT0 hsum
    (variance_pos d.h1 d.h2 hne)
  intro i
  fin_cases i
  · simpa [gHead,fHead,truth] using And.intro hh.1 hh.2.2.2.1
  · simpa [gHead,fHead,truth] using And.intro hh.2.1 hh.2.2.2.2.1
  · simpa [gHead,fHead,truth] using And.intro hh.2.1 hh.2.2.2.2.1
  · change (0 < leadG d.s (d.z+d.w) d.e 1 (1+1)) ∧
      (0 < leadF d.s (d.z+d.w) d.e 1 (1+1))
    norm_num
    exact ⟨hh.2.2.1,hh.2.2.2.2.2⟩

lemma heads_positive (d : Data) (hd : d.valid) : ∀ j, 0 < d.heads j := by
  have hg := d.score_heads_positive hd
  obtain ⟨hs,hz,hw,hsum,hne⟩ := hd
  have hs1 : d.s < 1 := by linarith
  have hz1 : d.z < 1 := by linarith
  have hw1 : d.w < 1 := by linarith
  rintro ⟨k,i⟩
  fin_cases k
  · simpa [heads] using (hg i).1
  · simpa [heads] using (hg i).2
  · fin_cases i <;> simp [heads,bary0] <;> linarith
  · fin_cases i <;> simp [heads,p0] <;> linarith
  · fin_cases i <;> simp [heads,p0] <;> linarith

lemma budgets_nonneg (d : Data) : ∀ j, 0 ≤ d.budgets j := by
  rintro ⟨k,i⟩
  fin_cases k
  · simpa [budgets] using budget_nonneg (gCoefficients d.h1 d.h2 d.hz d.hw d.b d.g)
  · simpa [budgets] using budget_nonneg (fCoefficients d.s (truth i 0) d.h1 d.h2 d.hz d.hw d.b d.g)
  · change 0 ≤ |d.bary1 i|+|d.bary2 i|
    positivity
  · simpa [budgets] using abs_nonneg (d.hvec i)
  · simpa [budgets] using abs_nonneg (d.hvec i)

lemma rem_bound (d : Data) (j : Fin 5 × Fin 4) (eps : ℝ)
    (he0 : 0 ≤ eps) (he1 : eps ≤ 1) : |d.rem j eps| ≤ d.budgets j := by
  rcases j with ⟨k,i⟩
  fin_cases k
  · simpa [rem,budgets] using gRem_bound d.h1 d.h2 d.hz d.hw d.b d.g eps he0 he1
  · simpa [rem,budgets] using fRem_bound d.s (truth i 0) d.h1 d.h2 d.hz d.hw d.b d.g eps he0 he1
  · change |d.bary1 i+eps*d.bary2 i| ≤ |d.bary1 i|+|d.bary2 i|
    calc
      |d.bary1 i+eps*d.bary2 i| ≤ |d.bary1 i|+|eps*d.bary2 i| := abs_add _ _
      _ ≤ |d.bary1 i|+|d.bary2 i| := by
        rw [abs_mul,abs_of_nonneg he0]
        exact add_le_add_left (mul_le_of_le_one_left (abs_nonneg _) he1) _
  · simp [rem,budgets]
  · simp [rem,budgets]

lemma bary_identity (d : Data) (i : Fin 4) (eps : ℝ) :
    bary d.s d.z d.w d.h1 d.h2 d.hz d.hw eps i=
      d.bary0 i+eps*(d.bary1 i+eps*d.bary2 i) := by
  fin_cases i
  · change 1+(d.s+eps*mean d.h1 d.h2+eps^2*d.b)-(d.z+eps*d.hz+eps^2*d.g)-
      (d.w+eps*d.hw+eps^2*d.g) = 1+d.s-d.z-d.w+
        eps*((mean d.h1 d.h2-d.hz-d.hw)+eps*(d.b-2*d.g))
    ring
  · change (d.z+eps*d.hz+eps^2*d.g)-(d.s+eps*mean d.h1 d.h2+eps^2*d.b) =
      d.z-d.s+eps*((d.hz-mean d.h1 d.h2)+eps*(d.g-d.b))
    ring
  · change (d.w+eps*d.hw+eps^2*d.g)-(d.s+eps*mean d.h1 d.h2+eps^2*d.b) =
      d.w-d.s+eps*((d.hw-mean d.h1 d.h2)+eps*(d.g-d.b))
    ring
  · change d.s+eps*mean d.h1 d.h2+eps^2*d.b = d.s+eps*(mean d.h1 d.h2+eps*d.b)
    ring

lemma input_identity (d : Data) (i : Fin 4) (eps : ℝ) : d.input eps i=d.p0 i+eps*d.hvec i := by
  fin_cases i <;> rfl

lemma constraint_identity (d : Data) (j : Fin 5 × Fin 4) (eps : ℝ) :
    d.constraints j eps=d.heads j+eps*d.rem j eps := by
  rcases j with ⟨k,i⟩
  fin_cases k
  · rfl
  · rfl
  · simpa [constraints,heads,rem] using d.bary_identity i eps
  · simpa [constraints,heads,rem] using d.input_identity i eps
  · change 1-d.input eps i = (1-d.p0 i)+eps*(-d.hvec i)
    rw [input_identity]
    ring

lemma delta_positive (d : Data) (hd : d.valid) : 0 < d.delta :=
  ConstraintBounds.radius_pos d.heads d.budgets (d.heads_positive hd) d.budgets_nonneg

lemma constraints_positive (d : Data) (hd : d.valid) (eps : ℝ)
    (he : 0 < eps) (hsmall : eps < d.delta) : ∀ j, 0 < d.constraints j eps := by
  have hh := ConstraintBounds.positive_inside_radius d.heads d.budgets d.rem
    (d.heads_positive hd) d.budgets_nonneg d.rem_bound eps he hsmall
  intro j
  rw [constraint_identity]
  exact hh j

/-- Explicit delta, actual Bregman gains, and both forecasts inside the open
cube. Every construction is a finite arithmetic expression in the input data. -/
theorem explicit_strict_repair (d : Data) (hd : d.valid) :
    0 < d.delta ∧ ∀ eps : ℝ, 0 < eps → eps < d.delta →
      (∀ i : Fin 4, d.input eps i ∈ Ioo 0 1) ∧
      d.output eps ∈ hull ∧
      (∀ i : Fin 4, d.output eps i ∈ Ioo 0 1) ∧
      (∀ i : Fin 4,
        divergence coordG coordDG (truth i) (d.output eps) < divergence coordG coordDG (truth i) (d.input eps) ∧
        divergence coordF coordDF (truth i) (d.output eps) < divergence coordF coordDF (truth i) (d.input eps)) := by
  refine ⟨d.delta_positive hd,?_⟩
  intro eps he hsmall
  have hp := d.constraints_positive hd eps he hsmall
  have hbase : ∀ i : Fin 4, d.input eps i ∈ Ioo 0 1 := by
    intro i
    have hlo := hp (3,i)
    have hhi := hp (4,i)
    simp [constraints] at hlo hhi
    exact ⟨hlo,by linarith⟩
  have hb0 := hp (2,0)
  have hb1 := hp (2,1)
  have hb2 := hp (2,2)
  have hb3 := hp (2,3)
  have h0 : 0 < d.output eps 0 := by simpa [constraints,output,bary] using hb3
  have h1 : d.output eps 0 < d.output eps 2 := by
    have hh : 0 < d.output eps 2-d.output eps 0 := by simpa [constraints,output,bary] using hb1
    linarith
  have h2 : d.output eps 0 < d.output eps 3 := by
    have hh : 0 < d.output eps 3-d.output eps 0 := by simpa [constraints,output,bary] using hb2
    linarith
  have hsum : d.output eps 2+d.output eps 3 < 1+d.output eps 0 := by
    have hh : 0 < 1+d.output eps 0-d.output eps 2-d.output eps 3 := by
      simpa [constraints,output,bary] using hb0
    linarith
  have hout : d.output eps = ![d.output eps 0,d.output eps 0,d.output eps 2,d.output eps 3] := by
    ext i
    fin_cases i <;> rfl
  have hmem : d.output eps ∈ hull := by
    rw [hout]
    exact hull_of_inequalities _ _ _ h0.le h1.le h2.le hsum.le
  have hopen : ∀ i : Fin 4, d.output eps i ∈ Ioo 0 1 := by
    intro i
    rw [hout]
    fin_cases i <;> simp <;> constructor <;> linarith
  refine ⟨hbase,hmem,hopen,?_⟩
  intro i
  have hg : 0 < insideG d.s d.z d.w d.h1 d.h2 d.hz d.hw i eps := by simpa [constraints] using hp (0,i)
  have hf : 0 < insideF d.s d.z d.w d.h1 d.h2 d.hz d.hw i eps := by simpa [constraints] using hp (1,i)
  have hsquare : 0 < eps^2 := pow_pos he 2
  have hgp := mul_pos hsquare hg
  have hfp := mul_pos hsquare hf
  rw [← ANDRepair.gainG d.s d.z d.w d.h1 d.h2 d.hz d.hw eps i] at hgp
  rw [← ANDRepair.gainF d.s d.z d.w d.h1 d.h2 d.hz d.hw eps i] at hfp
  simp only [scoreG_is_actual_Bregman,scoreF_is_actual_Bregman] at hgp hfp
  constructor
  · exact sub_pos.mp hgp
  · exact sub_pos.mp hfp

end Data

def fromVectors (p h : Vec) : Data :=
  ⟨p 0,p 2,p 3,h 0,h 1,h 2,h 3⟩

lemma fromVectors_valid (p h : Vec) (hp : p ∈ intrinsicInterior ℝ hull)
    (htrans : h 0 ≠ h 1) : (fromVectors p h).valid := by
  obtain ⟨hp01,hs,hz,hw,hsum⟩ := ANDIntrinsic.interior_parameters p hp
  exact ⟨hs,hz,hw,hsum,htrans⟩

/-- Literal intrinsic-interior version with a defined arithmetic radius,
rather than an existential radius selected by continuity. -/
theorem intrinsic_explicit_strict_repair (p h : Vec)
    (hp : p ∈ intrinsicInterior ℝ hull) (htrans : h 0 ≠ h 1) :
    0 < (fromVectors p h).delta ∧
    ∀ eps : ℝ, 0 < eps → eps < (fromVectors p h).delta →
      (∀ i : Fin 4, (p+eps • h) i ∈ Ioo 0 1) ∧
      (fromVectors p h).output eps ∈ hull ∧
      (∀ i : Fin 4, (fromVectors p h).output eps i ∈ Ioo 0 1) ∧
      (∀ i : Fin 4,
        divergence coordG coordDG (truth i) ((fromVectors p h).output eps) <
          divergence coordG coordDG (truth i) (p+eps • h) ∧
        divergence coordF coordDF (truth i) ((fromVectors p h).output eps) <
          divergence coordF coordDF (truth i) (p+eps • h)) := by
  have hd := fromVectors_valid p h hp htrans
  obtain ⟨hdelta,hgain⟩ := (fromVectors p h).explicit_strict_repair hd
  refine ⟨hdelta,?_⟩
  intro eps he hsmall
  have hp01 := (ANDIntrinsic.interior_parameters p hp).1
  have hin : (fromVectors p h).input eps = p+eps • h := by
    ext i
    fin_cases i <;> simp [Data.input,fromVectors,baseline,hp01]
  simpa only [hin] using hgain eps he hsmall

#print axioms intrinsic_explicit_strict_repair
#print axioms Data.explicit_strict_repair
end ExplicitANDScale
