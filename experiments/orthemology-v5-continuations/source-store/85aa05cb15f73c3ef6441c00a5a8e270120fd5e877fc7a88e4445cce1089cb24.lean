import ExecutableAuditRepair

open MeasureTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2

namespace Orthemology.Tranche3

noncomputable section

/-- One realised contract charge. The selector chooses which complementary
coordinate is charged, while truth is held fixed. -/
def auditCharge (b₁ b₂ : ℝ) (truth selector : Bool) : ℝ :=
  if selector then (b₁-(if truth then 1 else 0))^2
  else (b₂-(if truth then 0 else 1))^2

def expectedAuditCharge (a b₁ b₂ : ℝ) (truth : Bool) : ℝ :=
  ∑ selector : Bool, coinMass a selector*auditCharge b₁ b₂ truth selector

/-- The same selector distribution that generates the observed receipts
induces the weighted expected score. This is a model identity, not a proof
that an external service implements this contract. -/
theorem selector_score_identity (a b₁ b₂ : ℝ) (truth : Bool) :
    expectedAuditCharge a b₁ b₂ truth =
      a*(b₁-(if truth then 1 else 0))^2+(1-a)*(b₂-(if truth then 0 else 1))^2 := by
  simp [expectedAuditCharge,coinMass,auditCharge,add_comm]

lemma expectedAuditCharge_coherent (a q : ℝ) (truth : Bool) :
    expectedAuditCharge a q (1-q) truth = (q-(if truth then 1 else 0))^2 := by
  rw [selector_score_identity]
  cases truth <;> norm_num <;> ring

/-- The exact regret certificate has the intended contract semantics. -/
theorem contract_regret_identity (a e q : ℝ) :
    expectedAuditCharge a q (1-q) false-expectedAuditCharge a (1/2+e) (1/2) false = excessZero a e q ∧
    expectedAuditCharge a q (1-q) true-expectedAuditCharge a (1/2+e) (1/2) true = excessOne a e q := by
  rw [expectedAuditCharge_coherent,expectedAuditCharge_coherent,
    selector_score_identity,selector_score_identity]
  norm_num
  unfold excessZero excessOne
  constructor <;> ring

/-- A fresh next selector and the acquired word have their derived joint law.
This is stronger than merely postulating a marginal Bernoulli sensor. -/
theorem auditSource_next_joint (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (n : ℕ) (w : Bits n) (b : Bool) :
    auditSourceLaw a ha0 ha1 {ω | observedPrefix n ω=w ∧ ω n=b} =
      ENNReal.ofReal (bernoulliMass n a w)*ENNReal.ofReal (coinMass a b) := by
  have hs : {ω | observedPrefix n ω=w ∧ ω n=b} = observedPrefix (n+1) ⁻¹' {(b,w)} := by
    ext ω
    change (observedPrefix n ω=w ∧ ω n=b) ↔ (ω n,observedPrefix n ω)=(b,w)
    constructor
    · rintro ⟨h1,h2⟩
      exact Prod.ext h2 h1
    · intro h
      exact ⟨(Prod.mk.inj h).2,(Prod.mk.inj h).1⟩
  rw [hs,← Measure.map_apply (observedPrefix_measurable (n+1)) (measurableSet_singleton _),
    auditSource_prefix_mass]
  change ENNReal.ofReal (coinMass a b*bernoulliMass n a w) = _
  rw [ENNReal.ofReal_mul (coinMass_nonneg a ha0 ha1 b)]
  exact mul_comm _ _

/-- Every accepted interval certificate protects expected contract charge
at each truth state, provided the true selector is inside the interval. -/
theorem accepted_contract_score (l u e eta q : ℚ) (a : ℝ)
    (hout : rationalCertificate l u e eta=some q) (hla : (l:ℝ) ≤ a) (hau : a ≤ (u:ℝ))
    (truth : Bool) :
    expectedAuditCharge a q (1-q) truth-expectedAuditCharge a (1/2+e) (1/2) truth ≤ eta := by
  have hg := (rationalCertificate_sound l u e eta q hout).2.2 a hla hau
  cases truth
  · rw [(contract_regret_identity a e q).1]
    exact hg.1
  · rw [(contract_regret_identity a e q).2]
    exact hg.2

/-- Expected improvement need not hold on every realised selector draw. -/
theorem expected_not_realised_control :
    expectedAuditCharge (1/2) (5/8) (3/8) false <
      expectedAuditCharge (1/2) (3/4) (1/2) false ∧
    auditCharge (5/8) (3/8) false false > auditCharge (3/4) (1/2) false false := by
  norm_num [expectedAuditCharge,auditCharge,coinMass]

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.selector_score_identity
#print axioms Orthemology.Tranche3.auditSource_next_joint
#print axioms Orthemology.Tranche3.accepted_contract_score
#print axioms Orthemology.Tranche3.expected_not_realised_control
