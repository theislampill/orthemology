import JointRegularity

/- Additive syntax-only translation for a bounded rival-model diagnostic.
   This file makes no source-derivability or semantic-faithfulness claim. -/
namespace JointRawTop
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness
open SigmaCompletion RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def topTy : Ty := .pi .bottom .bottom

def translate : Ty → Ty
  | .param n => .param n
  | .bottom => .bottom
  | .raw => topTy
  | .all B => .all (translate B)
  | .pi A B => .pi (translate A) (translate B)
  | .sigma A B => .sigma (translate A) (translate B)
  | .identity A p q => .identity (translate A) p q

def translateTel (Γ : Tel) : Tel := Γ.map translate

theorem translate_subst (A : Ty) (σ : Nat → Poly) :
    translate (subst σ A) = subst σ (translate A) := by
  induction A generalizing σ with
  | param n | bottom | raw => rfl
  | all B ih => simp only [subst, translate, ih]
  | pi A B ia ib | sigma A B ia ib => simp only [subst, translate, ia, ib]
  | identity A p q ia => simp only [subst, translate, ia]

theorem translate_wk (A : Ty) : translate (wk A) = wk (translate A) :=
  translate_subst A _

theorem translate_inst (B : Ty) (a : Poly) :
    translate (inst B a) = inst (translate B) a := translate_subst B _

theorem translate_trename (A : Ty) (r : Nat → Nat) :
    translate (trename r A) = trename r (translate A) := by
  induction A generalizing r with
  | param n | bottom | raw => rfl
  | all B ih => simp only [trename, translate, ih]
  | pi A B ia ib | sigma A B ia ib => simp only [trename, translate, ia, ib]
  | identity A p q ia => simp only [trename, translate, ia]

theorem translate_twk (A : Ty) : translate (twk A) = twk (translate A) :=
  translate_trename A _

theorem translateTel_twk (Γ : Tel) : translateTel (twkTel Γ) = twkTel (translateTel Γ) := by
  simp only [translateTel, twkTel, List.map_map]
  congr 1
  funext A
  exact translate_twk A

theorem translate_tup (τ : Nat → Ty) :
    (fun n => translate (tup τ n)) = tup (fun n => translate (τ n)) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact translate_twk (τ n)

theorem translate_mixed (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    translate (mixed σ τ A) = mixed σ (fun n => translate (τ n)) (translate A) := by
  induction A generalizing σ τ with
  | param n | bottom | raw => rfl
  | all B ih => simp only [mixed, translate, ih, translate_tup]
  | pi A B ia ib | sigma A B ia ib =>
      simp only [mixed, translate, ia, ib, translate_wk]
  | identity A p q ia => simp only [mixed, translate, ia]

theorem translate_tsubst (A : Ty) (τ : Nat → Ty) :
    translate (tsubst τ A) = tsubst (fun n => translate (τ n)) (translate A) :=
  translate_mixed A Poly.var τ

theorem translate_tinst (B A : Ty) :
    translate (tinst B A) = tinst (translate B) (translate A) := by
  simp only [tinst, translate_tsubst]
  congr 1
  funext n
  cases n <;> rfl

theorem translate_arr (A B : Ty) :
    translate (arr A B) = arr (translate A) (translate B) := by
  simp only [arr, translate, translate_wk]

theorem translate_motiveAt (B : Ty) (y e : Poly) :
    translate (motiveAt B y e) = motiveAt (translate B) y e := translate_subst B _

theorem translateTel_theta (Γ : Tel) (A : Ty) (x : Poly) :
    translateTel (theta Γ A x) = theta (translateTel Γ) (translate A) x := by
  simp only [translateTel, theta, List.map_cons, translate, translate_wk]

theorem translate_fin (C : TypeCode) : translate (fin C) = fin C := by
  induction C with
  | var n | bottom => rfl
  | arrow A B ia ib => simp only [fin, translate_arr, ia, ib]
  | all B ih => simp only [fin, translate, ih]

theorem translate_typeImages (υ : List Ty) :
    (fun n => translate (typeImages υ n)) = typeImages (υ.map translate) := by
  induction υ with
  | nil => rfl
  | cons A υ ih =>
      funext n
      cases n with
      | zero => rfl
      | succ n => exact congrFun ih n

theorem translate_finite_instance (C : TypeCode) (υ : List Ty) :
    translate (tsubst (typeImages υ) (fin C)) =
      tsubst (typeImages (υ.map translate)) (fin C) := by
  rw [translate_tsubst, translate_fin, translate_typeImages]

theorem translate_N : translate N = N := rfl

theorem translate_branchType (P : Ty) :
    translate (branchType P) = branchType (translate P) := translate_subst P _

theorem translate_successorFamily (P : Ty) :
    translate (successorFamily P) = successorFamily (translate P) := translate_subst P _

theorem translate_dependentStepType (P : Ty) :
    translate (dependentStepType P) = dependentStepType (translate P) := by
  simp only [dependentStepType, translate, translate_N, translate_arr, translate_successorFamily]

#print axioms translate_subst
#print axioms translate_mixed
#print axioms translate_tinst
#print axioms translate_finite_instance
#print axioms translate_branchType
#print axioms translate_dependentStepType
end JointRawTop
