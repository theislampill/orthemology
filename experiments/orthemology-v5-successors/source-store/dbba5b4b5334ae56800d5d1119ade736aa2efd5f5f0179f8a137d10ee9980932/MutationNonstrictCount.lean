import CertificateData
import EmpiricalTestLaw

/-! Exact rational empirical testing and a computed positive separation. -/
namespace OrthemicCertificate.Direct
open HiddenParity HiddenParity.Sufficiency HiddenParity.Empirical HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : ℕ}

/-- Integer acquired count; history is never truncated or reset. -/
def symbolCount (e : Pair n k) (y : Fin n) : History (Pair n k) (Fin n) → ℕ
  | [] => 0
  | (f,z) :: h => (if f = e ∧ z = y then 1 else 0) + symbolCount e y h

def rationalFrequency (e : Pair n k) (y : Fin n) (h : History (Pair n k) (Fin n)) : ℚ :=
  (symbolCount e y h : ℚ) / (actionCount e h : ℚ)

def rationalReject (I : Input q n k) (ε : ℚ) (θ : Fin q) (r : ℕ)
    (h : History (Pair n k) (Fin n)) : Bool :=
  decide (∃ e : Pair n k, ∃ y : Fin n,
    r ≤ actionCount e h ∧ ε ≤ |rationalFrequency e y h - I.row θ e y|)


def mutationInput : Input 2 2 1 where
  rows := #[1,0,0,1,0,1,0,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩

theorem mutant_value : rationalReject mutationInput (1/2) 0 2 [((0,0),0),((0,0),1)] = true := by
  simp only [rationalReject, decide_eq_true_eq]
  refine ⟨(0,0),0,?_⟩
  norm_num [rationalFrequency, symbolCount, actionCount, Input.row, mutationInput]
  exact le_abs_self _
example : rationalReject mutationInput (1/2) 0 2 [((0,0),0),((0,0),1)] = false := by
  rw [mutant_value]
  decide +kernel
end OrthemicCertificate.Direct
