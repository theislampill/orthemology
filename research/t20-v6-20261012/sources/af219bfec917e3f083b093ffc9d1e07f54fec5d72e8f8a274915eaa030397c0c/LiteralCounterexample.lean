import SourceTransport

/- Concrete computation of the ACTUAL original q on the semantic value nu.
   No HasE noninhabitation claim is made in this module. -/
namespace HomogeneousCounterexample
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
open CaseOperational HenkinSourceTransport
abbrev OT := OpenTermStandardness.T

def defaultEnv : Nat → T := fun _ => .a0

theorem fold_closed (t : OT) (ht : OpenTermStandardness.bound t = 0) (η ξ : Nat → T) :
    fold η t = fold ξ t := by
  induction t with
  | var n => simp [OpenTermStandardness.bound] at ht
  | i | k | s | zero | one => rfl
  | app f a hf ha =>
    have h : OpenTermStandardness.bound f = 0 ∧ OpenTermStandardness.bound a = 0 := by
      change max (OpenTermStandardness.bound f) (OpenTermStandardness.bound a) = 0 at ht
      exact ⟨Nat.eq_zero_of_le_zero (ht ▸ Nat.le_max_left _ _),
        Nat.eq_zero_of_le_zero (ht ▸ Nat.le_max_right _ _)⟩
    exact congrArg₂ T.app (hf h.1) (ha h.2)

def pair (a b : T) := T.s ⬝ (T.s ⬝ T.i ⬝ (T.k ⬝ a)) ⬝ (T.k ⬝ b)
def first (z : T) := z ⬝ T.k
def second (z : T) := z ⬝ (T.k ⬝ T.i)
def zeroTerm := fold defaultEnv OpenTermStandardness.zeroTerm
def succTerm := fold defaultEnv OpenTermStandardness.succTerm
def delta := fold defaultEnv OpenTermStandardness.delta
def z0 := pair zeroTerm zeroTerm
def q := fold defaultEnv OpenTermStandardness.q

theorem fold_pair (η) (a b : OT) :
    fold η (OpenTermStandardness.pair a b) = pair (fold η a) (fold η b) := rfl

theorem fold_zero (η) : fold η OpenTermStandardness.zeroTerm = zeroTerm :=
  fold_closed _ (by
    simp [OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
      OpenTermStandardness.delta, OpenTermStandardness.q, OpenTermStandardness.qPoly,
      OpenTermStandardness.literalPairStateBody, OpenTermStandardness.diagonalStep,
      OpenTermStandardness.diagonalStepBody, OpenTermStandardness.diagonalZero,
      OpenTermStandardness.pairPoly, OpenTermStandardness.fstPoly, OpenTermStandardness.sndPoly,
      OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
      OpenTermStandardness.succPoly, OpenTermStandardness.succBody, OpenTermStandardness.abstract,
      OpenTermStandardness.freeZero, OpenTermStandardness.drop, OpenTermStandardness.pren,
      OpenTermStandardness.psub, OpenTermStandardness.eval, OpenTermStandardness.bound,
      OpenTermStandardness.zeroEnv]) _ _
theorem fold_succ (η) : fold η OpenTermStandardness.succTerm = succTerm :=
  fold_closed _ (by
    simp [OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
      OpenTermStandardness.delta, OpenTermStandardness.q, OpenTermStandardness.qPoly,
      OpenTermStandardness.literalPairStateBody, OpenTermStandardness.diagonalStep,
      OpenTermStandardness.diagonalStepBody, OpenTermStandardness.diagonalZero,
      OpenTermStandardness.pairPoly, OpenTermStandardness.fstPoly, OpenTermStandardness.sndPoly,
      OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
      OpenTermStandardness.succPoly, OpenTermStandardness.succBody, OpenTermStandardness.abstract,
      OpenTermStandardness.freeZero, OpenTermStandardness.drop, OpenTermStandardness.pren,
      OpenTermStandardness.psub, OpenTermStandardness.eval, OpenTermStandardness.bound,
      OpenTermStandardness.zeroEnv]) _ _
theorem fold_delta (η) : fold η OpenTermStandardness.delta = delta :=
  fold_closed _ (by
    simp [OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
      OpenTermStandardness.delta, OpenTermStandardness.q, OpenTermStandardness.qPoly,
      OpenTermStandardness.literalPairStateBody, OpenTermStandardness.diagonalStep,
      OpenTermStandardness.diagonalStepBody, OpenTermStandardness.diagonalZero,
      OpenTermStandardness.pairPoly, OpenTermStandardness.fstPoly, OpenTermStandardness.sndPoly,
      OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
      OpenTermStandardness.succPoly, OpenTermStandardness.succBody, OpenTermStandardness.abstract,
      OpenTermStandardness.freeZero, OpenTermStandardness.drop, OpenTermStandardness.pren,
      OpenTermStandardness.psub, OpenTermStandardness.eval, OpenTermStandardness.bound,
      OpenTermStandardness.zeroEnv]) _ _
theorem fold_z0 (η) : fold η OpenTermStandardness.z0 = z0 := by
  simp only [OpenTermStandardness.z0, fold_pair, fold_zero, z0]
theorem fold_q (η) : fold η OpenTermStandardness.q = q :=
  fold_closed _ (by
    simp [OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
      OpenTermStandardness.delta, OpenTermStandardness.q, OpenTermStandardness.qPoly,
      OpenTermStandardness.literalPairStateBody, OpenTermStandardness.diagonalStep,
      OpenTermStandardness.diagonalStepBody, OpenTermStandardness.diagonalZero,
      OpenTermStandardness.pairPoly, OpenTermStandardness.fstPoly, OpenTermStandardness.sndPoly,
      OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
      OpenTermStandardness.succPoly, OpenTermStandardness.succBody, OpenTermStandardness.abstract,
      OpenTermStandardness.freeZero, OpenTermStandardness.drop, OpenTermStandardness.pren,
      OpenTermStandardness.psub, OpenTermStandardness.eval, OpenTermStandardness.bound,
      OpenTermStandardness.zeroEnv]) _ _

theorem q_application (n : T) : Conv (q ⬝ n) (second (n ⬝ delta ⬝ z0)) := by
  have h := fold_conv (OpenTermStandardness.q_application (.var 0)) (fun _ => n)
  simpa only [fold, OpenTermStandardness.snd, fold_q, fold_delta, fold_z0, second] using h

theorem delta_pair (a b : T) :
    Conv (delta ⬝ pair a b) (pair (succTerm ⬝ a) (succTerm ⬝ b)) := by
  have h := fold_conv (OpenTermStandardness.delta_pair (.var 0) (.var 1))
    (fun n => if n = 0 then a else b)
  simpa only [fold, fold_delta, fold_pair, fold_succ, ↓reduceIte, Nat.one_ne_zero] using h

theorem second_pair (a b : T) : Conv (second (pair a b)) b := by
  have h := fold_conv (OpenTermStandardness.snd_pair (.var 0) (.var 1))
    (fun n => if n = 0 then a else b)
  simpa only [fold, OpenTermStandardness.snd, fold_pair, second, ↓reduceIte, Nat.one_ne_zero] using h

theorem zero_application (f a : T) : Conv (zeroTerm ⬝ f ⬝ a) a := by
  have h := fold_conv (OpenTermStandardness.zero_application (.var 0) (.var 1))
    (fun n => if n = 0 then f else a)
  simpa only [fold, fold_zero, ↓reduceIte, Nat.one_ne_zero] using h

theorem succ_zero_application (f a : T) :
    Conv (succTerm ⬝ zeroTerm ⬝ f ⬝ a) (f ⬝ a) := by
  have h := fold_conv (OpenTermStandardness.succ_application OpenTermStandardness.zeroTerm
    (.var 0) (.var 1)) (fun n => if n = 0 then f else a)
  have h' : Conv (succTerm ⬝ zeroTerm ⬝ f ⬝ a) (f ⬝ (zeroTerm ⬝ f ⬝ a)) := by
    simpa only [fold, fold_succ, fold_zero, ↓reduceIte, Nat.one_ne_zero] using h
  exact h'.trans (.app (.refl _) (zero_application f a))

theorem nu_q_is_one : Conv (q ⬝ T.nu) (succTerm ⬝ zeroTerm) := by
  have hz : FunVal z0 := raw_fun_val (.s2 _ _)
  exact (q_application T.nu).trans
    ((Conv.app (nu_fun delta hz) (.refl _)).trans
      ((Conv.app (delta_pair zeroTerm zeroTerm) (.refl _)).trans (second_pair _ _)))

def scalarStep : T := T.k ⬝ T.a1

theorem scalar_left : Conv (T.nu ⬝ scalarStep ⬝ T.a0) T.a0 := nu_atom0 _

theorem scalar_right : Conv (q ⬝ T.nu ⬝ scalarStep ⬝ T.a0) T.a1 :=
  ((Conv.app (Conv.app nu_q_is_one (.refl _)) (.refl _)).trans
    (succ_zero_application scalarStep T.a0)).trans (.k _ _)

theorem scalar_not_convertible :
    ¬ Conv (T.nu ⬝ scalarStep ⬝ T.a0) (q ⬝ T.nu ⬝ scalarStep ⬝ T.a0) := by
  intro h
  exact atom_distinct (scalar_left.symm.trans (h.trans scalar_right))

theorem original_q_eval (η : Nat → T) :
    interp P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed η = q := by
  have h := fold_interp P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed OpenTermStandardness.T.var η
  have he : (fun n => fold η (OpenTermStandardness.T.var n)) = η := rfl
  rw [he] at h
  rw [← h]
  unfold ImportedOpenTermTransport.interp
  rw [ImportedOpenTermTransport.original_q_poly_exact, ImportedOpenTermTransport.q_eval_independent]
  exact fold_q η

theorem original_scalar_right (η : Nat → T) :
    Conv (interp P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed η
      ⬝ T.nu ⬝ scalarStep ⬝ T.a0) T.a1 := by
  rw [original_q_eval]
  exact scalar_right

#print axioms nu_q_is_one
#print axioms scalar_not_convertible
#print axioms original_q_eval
#print axioms original_scalar_right
end HomogeneousCounterexample
