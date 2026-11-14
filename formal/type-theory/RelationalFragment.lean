/-
Binary logical relations for the DECLARED finite pure combinatory fragment.
This fundamental theorem is about FiniteDerives, not every unary semantic
realiser and not arbitrary ambient Lean functions or effectful contexts.
Authored proof source, UNCOMPILED in this runtime. No new axioms.
-/
import FiniteBridge

namespace OrthemologyV4Relations
open OrthemologyV2 OrthemologyV3

structure RelationCode where
  relates : Term → Term → Prop
  leftStable : ∀ {t u}, Step t u → ∀ v, relates t v ↔ relates u v
  rightStable : ∀ {t u}, Step t u → ∀ v, relates v t ↔ relates v u

namespace RelationCode

def bottom : RelationCode where
  relates := fun _ _ => False
  leftStable := fun _ _ => Iff.rfl
  rightStable := fun _ _ => Iff.rfl

def arrow (A B : RelationCode) : RelationCode where
  relates := fun f g => ∀ x y, A.relates x y → B.relates (.app f x) (.app g y)
  leftStable := by
    intro f g h v
    constructor
    · intro hf x y hxy
      exact (B.leftStable (.left h x) (.app v y)).mp (hf x y hxy)
    · intro hg x y hxy
      exact (B.leftStable (.left h x) (.app v y)).mpr (hg x y hxy)
  rightStable := by
    intro f g h v
    constructor
    · intro hf x y hxy
      exact (B.rightStable (.left h y) (.app v x)).mp (hf x y hxy)
    · intro hg x y hxy
      exact (B.rightStable (.left h y) (.app v x)).mpr (hg x y hxy)

def all (B : RelationCode → RelationCode) : RelationCode where
  relates := fun t u => ∀ A, (B A).relates t u
  leftStable := by
    intro t u h v
    exact ⟨fun e A => ((B A).leftStable h v).mp (e A),
           fun e A => ((B A).leftStable h v).mpr (e A)⟩
  rightStable := by
    intro t u h v
    exact ⟨fun e A => ((B A).rightStable h v).mp (e A),
           fun e A => ((B A).rightStable h v).mpr (e A)⟩

theorem alongLeft (A : RelationCode) {t u : Term} (h : Red t u) (v : Term) :
    A.relates t v ↔ A.relates u v := by
  induction h with
  | refl => exact Iff.rfl
  | tail h _ ih => exact (A.leftStable h v).trans ih

theorem alongRight (A : RelationCode) {t u : Term} (h : Red t u) (v : Term) :
    A.relates v t ↔ A.relates v u := by
  induction h with
  | refl => exact Iff.rfl
  | tail h _ ih => exact (A.rightStable h v).trans ih

end RelationCode

def relExtend (X : RelationCode) (rho : Nat → RelationCode) : Nat → RelationCode
  | 0 => X
  | n+1 => rho n

def relInterpret : TypeCode → (Nat → RelationCode) → RelationCode
  | .var n, rho => rho n
  | .bottom, _ => .bottom
  | .arrow A B, rho => .arrow (relInterpret A rho) (relInterpret B rho)
  | .all A, rho => .all (fun X => relInterpret A (relExtend X rho))

theorem relRename (A : TypeCode) : ∀ r rho,
    relInterpret (rename r A) rho = relInterpret A (fun n => rho (r n)) := by
  induction A with
  | var n => intro r rho; rfl
  | bottom => intro r rho; rfl
  | arrow A B ihA ihB =>
      intro r rho
      change RelationCode.arrow (relInterpret (rename r A) rho) (relInterpret (rename r B) rho) = _
      rw [ihA,ihB] <;> rfl
  | all A ih =>
      intro r rho
      change RelationCode.all (fun X => relInterpret (rename (liftRen r) A) (relExtend X rho)) = _
      apply congrArg RelationCode.all
      funext X
      rw [ih]
      apply congrArg (relInterpret A)
      funext n
      cases n <;> rfl

theorem relSubstitute (A : TypeCode) : ∀ sigma rho,
    relInterpret (substitute sigma A) rho =
      relInterpret A (fun n => relInterpret (sigma n) rho) := by
  induction A with
  | var n => intro sigma rho; rfl
  | bottom => intro sigma rho; rfl
  | arrow A B ihA ihB =>
      intro sigma rho
      change RelationCode.arrow (relInterpret (substitute sigma A) rho) (relInterpret (substitute sigma B) rho) = _
      rw [ihA,ihB] <;> rfl
  | all A ih =>
      intro sigma rho
      change RelationCode.all (fun X => relInterpret (substitute (upSub sigma) A) (relExtend X rho)) = _
      apply congrArg RelationCode.all
      funext X
      rw [ih]
      apply congrArg (relInterpret A)
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          change relInterpret (rename Nat.succ (sigma n)) (relExtend X rho) = relInterpret (sigma n) rho
          rw [relRename] <;> rfl

theorem relInstantiate (B A : TypeCode) (rho : Nat → RelationCode) :
    relInterpret (instantiateType B A) rho = relInterpret B (relExtend (relInterpret A rho) rho) := by
  unfold instantiateType
  rw [relSubstitute]
  apply congrArg (relInterpret B)
  funext n
  cases n <;> rfl

theorem relatedI (A : RelationCode) : (RelationCode.arrow A A).relates .i .i := by
  intro x y hxy
  apply (A.leftStable (.i x) (.app .i y)).mpr
  exact (A.rightStable (.i y) x).mpr hxy

theorem relatedK (A B : RelationCode) :
    (RelationCode.arrow A (RelationCode.arrow B A)).relates .k .k := by
  intro x y hxy a b _
  apply (A.leftStable (.k x a) (.app (.app .k y) b)).mpr
  exact (A.rightStable (.k y b) x).mpr hxy

theorem relatedS (A B C : RelationCode) :
    (RelationCode.arrow (RelationCode.arrow A (RelationCode.arrow B C))
      (RelationCode.arrow (RelationCode.arrow A B) (RelationCode.arrow A C))).relates .s .s := by
  intro f f' hf g g' hg x x' hx
  have result := hf x x' hx (.app g x) (.app g' x') (hg x x' hx)
  apply (C.leftStable (.s f g x) (.app (.app (.app .s f') g') x')).mpr
  exact (C.rightStable (.s f' g' x') (.app (.app f x) (.app g x))).mpr result

/-- Finite pure source fundamental theorem. No unary-realiser-to-parametricity
    implication is assumed or concluded. No semantic membership decision oracle. -/
theorem finite_fundamental {t A} (h : FiniteDerives t A) :
    ∀ rho, (relInterpret A rho).relates t t := by
  induction h with
  | i A => intro rho; exact relatedI (relInterpret A rho)
  | k A B => intro rho; exact relatedK (relInterpret A rho) (relInterpret B rho)
  | s A B C => intro rho; exact relatedS (relInterpret A rho) (relInterpret B rho) (relInterpret C rho)
  | app hf hx ihf ihx => intro rho; exact ihf rho _ _ (ihx rho)
  | allI h ih => intro rho X; exact ih (relExtend X rho)
  | allE h A ih =>
      intro rho
      rw [relInstantiate]
      exact ih rho (relInterpret A rho)
  | reduce h r ih =>
      intro rho
      exact ((relInterpret _ rho).alongRight r _).mp (((relInterpret _ rho).alongLeft r _).mp (ih rho))

theorem checked_parametric (v : Checked) (rho : Nat → RelationCode) :
    (relInterpret v.ty rho).relates v.term v.term := finite_fundamental v.valid rho

end OrthemologyV4Relations
