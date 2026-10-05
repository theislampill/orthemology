/-
The separating witness of the accepted intensional-identity argument, §8.
These are statements about the unchanged P01AC syntax and its full inherited
F/G interpretation. No new identity rule or semantic admission is used.
-/
import AllNucleusSyntax
import AllFiniteComparison
import P01ModelWitnesses

namespace P01AC.Intensional
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- The closed finite polymorphic identity type. -/
def separationA : Ty := fin OrthemologyV2.identityCode

def separationP : Poly := .atom .i
def separationQ : Poly := .atom P01R.skk
def separationE : Poly := .atom .i

/-- Forming this identity does not require a proof of its endpoints' identity. -/
def separationB : Ty := .identity separationA separationP separationQ

theorem separationA_form : P01AC.Form [] separationA :=
  form_fin OrthemologyV2.identityCode .nil

theorem separationP_has : P01AC.Has [] separationP separationA :=
  finite_import .nil P01R.finite_polymorphic_I

theorem separationQ_has : P01AC.Has [] separationQ separationA :=
  finite_import .nil P01R.finite_polymorphic_skk

theorem separationB_form : P01AC.Form [] separationB :=
  .identity separationA_form separationP_has separationQ_has

theorem separationP_scoped : P01AC.Scoped 0 separationP := True.intro
theorem separationQ_scoped : P01AC.Scoped 0 separationQ := True.intro
theorem separationE_scoped : P01AC.Scoped 0 separationE := True.intro

theorem separationA_scoped : P01AC.TyScoped 0 separationA :=
  tyScoped_fin OrthemologyV2.identityCode 0

theorem separationB_scoped : P01AC.TyScoped 0 separationB :=
  ⟨separationA_scoped, separationP_scoped, separationQ_scoped⟩

/-- The independent type-parameter scope. Pi and Sigma bind only terms;
    All binds exactly one type parameter. The inherited `TyScoped` checks
    free term variables instead, so both predicates are recorded below. -/
def TyParamScoped (n : Nat) : Ty → Prop
  | .param k => k < n
  | .bottom | .raw => True
  | .all B => TyParamScoped (n + 1) B
  | .pi A B | .sigma A B => TyParamScoped n A ∧ TyParamScoped n B
  | .identity A _ _ => TyParamScoped n A

theorem separationA_type_scoped : TyParamScoped 0 separationA := by
  change 0 < 1 ∧ 0 < 1
  exact ⟨Nat.zero_lt_succ 0, Nat.zero_lt_succ 0⟩

theorem separationB_type_scoped : TyParamScoped 0 separationB :=
  separationA_type_scoped

/-- This uses the inherited *full* recursive polymorphic theorem, its identity
    extension, and finite comparison. In particular it includes the uniformity
    clauses, rather than merely the pointwise action of I and SKK. -/
theorem separation_endpoints_F (ρ : OEnv) (η : Env) :
    P01AC.F separationA ρ η .i P01R.skk := by
  rw [separationA, F_fin]
  exact (P01R.recursive_identity_extension OrthemologyV2.identityCode ρ
    .i P01R.skk).mp (P01R.recursive_polymorphic_I_skk (diagEnv ρ))

/-- Unary validity in every inherited object environment, at any valuation. -/
theorem separation_F (ρ : OEnv) (η : Env) :
    P01AC.F separationB ρ η (eval separationE η) (eval separationE η) := by
  change P01AC.F separationA ρ η .i P01R.skk ∧ Conv .i .i ∧ Conv .i .i
  exact ⟨separation_endpoints_F ρ η, Conv.refl .i, Conv.refl .i⟩

/-- Full heterogeneous validity, for every inherited lawful relational
    environment and independently chosen left and right term valuations. -/
theorem separation_G (r : REnv) (η ξ : Env) :
    P01AC.G separationB r η ξ (eval separationE η) (eval separationE ξ) := by
  change P01AC.F separationA r.left η .i P01R.skk ∧
    P01AC.F separationA r.right ξ .i P01R.skk ∧ Conv .i .i ∧ Conv .i .i
  exact ⟨separation_endpoints_F r.left η, separation_endpoints_F r.right ξ,
    Conv.refl .i, Conv.refl .i⟩

/-- The exact closed positive witness used by the separation theorem. -/
theorem separation_closed_positive :
    P01AC.Form [] separationB ∧
    P01AC.Has [] separationP separationA ∧
    P01AC.Has [] separationQ separationA ∧
    P01AC.Scoped 0 separationE ∧
    P01AC.TyScoped 0 separationB ∧
    TyParamScoped 0 separationB ∧
    (∀ ρ : OEnv, P01AC.F separationB ρ zeroEnv
      (eval separationE zeroEnv) (eval separationE zeroEnv)) ∧
    (∀ r : REnv, P01AC.G separationB r zeroEnv zeroEnv
      (eval separationE zeroEnv) (eval separationE zeroEnv)) :=
  ⟨separationB_form, separationP_has, separationQ_has, separationE_scoped,
    separationB_scoped, separationB_type_scoped,
    fun ρ => separation_F ρ zeroEnv, fun r => separation_G r zeroEnv zeroEnv⟩

/-- Raw conversion cannot identify the two endpoints. This independent lemma
    is the contradiction used after closed-identity reflection is established. -/
theorem separation_endpoints_not_convertible (η : Env) :
    ¬ Conv (eval separationP η) (eval separationQ η) :=
  P01Source.I_SKK_not_convertible

theorem separation_contradiction
    (h : Conv (eval separationP zeroEnv) (eval separationQ zeroEnv)) : False :=
  separation_endpoints_not_convertible zeroEnv h

end P01AC.Intensional
