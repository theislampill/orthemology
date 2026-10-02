/- Capture avoidance for both type parameters and raw term indices. -/
import P01DependentModel
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def renameType (r : Nat → Nat) : Ty → Ty
  | .param n => .param (r n)
  | .bottom => .bottom
  | .raw => .raw
  | .identity p q => .identity p q
  | .arrow A B => .arrow (renameType r A) (renameType r B)
  | .pi B => .pi (renameType r B)
  | .sigma B => .sigma (renameType r B)
  | .all B => .all (renameType (liftRen r) B)

theorem piModel_congr {B C : Term → Model}
    {hb : ∀ {x y}, Conv x y → B x = B y}
    {hc : ∀ {x y}, Conv x y → C x = C y} (h : ∀ x, B x = C x) :
    piModel B hb = piModel C hc := by
  have e : B = C := funext h
  cases e; rfl

theorem sigmaModel_congr {B C : Term → Model}
    {hb : ∀ {x y}, Conv x y → B x = B y}
    {hc : ∀ {x y}, Conv x y → C x = C y} (h : ∀ x, B x = C x) :
    sigmaModel B hb = sigmaModel C hc := by
  have e : B = C := funext h
  cases e; rfl

theorem piModel_rename (B : Term → Model) (h : ∀ {x y}, Conv x y → B x = B y)
    (r : Nat → Nat) :
    piModel (fun x => (B x).rename r) (fun e => congrArg (fun M : Model => M.rename r) (h e)) =
      (piModel B h).rename r := rfl

theorem sigmaModel_rename (B : Term → Model) (h : ∀ {x y}, Conv x y → B x = B y)
    (r : Nat → Nat) :
    sigmaModel (fun x => (B x).rename r) (fun e => congrArg (fun M : Model => M.rename r) (h e)) =
      (sigmaModel B h).rename r := rfl

theorem interpret_type_rename (A : Ty) (r : Nat → Nat) (η : Env) :
    (interpret (renameType r A)).run η = ((interpret A).run η).rename r := by
  induction A generalizing r η with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb =>
      change arrowModel _ _ = _
      rw [ha,hb]; rfl
  | pi B ih =>
      change piModel (fun x => (interpret (renameType r B)).run (cons x η))
        (fun h => (interpret (renameType r B)).coherent (index_cons (index_refl η) h)) = _
      apply Eq.trans ?_ (piModel_rename (fun x => (interpret B).run (cons x η))
        (fun h => (interpret B).coherent (index_cons (index_refl η) h)) r)
      exact piModel_congr (fun x => ih r (cons x η))
  | sigma B ih =>
      change sigmaModel (fun x => (interpret (renameType r B)).run (cons x η))
        (fun h => (interpret (renameType r B)).coherent (index_cons (index_refl η) h)) = _
      apply Eq.trans ?_ (sigmaModel_rename (fun x => (interpret B).run (cons x η))
        (fun h => (interpret B).coherent (index_cons (index_refl η) h)) r)
      exact sigmaModel_congr (fun x => ih r (cons x η))
  | all B ih =>
      change allModel _ = _
      rw [ih]
      exact rename_all _ r

def liftTypes (σ : Nat → Ty) : Nat → Ty
  | 0 => .param 0
  | n+1 => renameType Nat.succ (σ n)

def liftIndices (σ : Nat → Ty) : Nat → Ty :=
  fun n => substIndex (fun k => .var (k+1)) (σ n)

def substType (σ : Nat → Ty) : Ty → Ty
  | .param n => σ n
  | .bottom => .bottom
  | .raw => .raw
  | .identity p q => .identity p q
  | .arrow A B => .arrow (substType σ A) (substType σ B)
  | .pi B => .pi (substType (liftIndices σ) B)
  | .sigma B => .sigma (substType (liftIndices σ) B)
  | .all B => .all (substType (liftTypes σ) B)

theorem interpret_liftTypes (σ : Nat → Ty) (η : Env) :
    (fun n => (interpret (liftTypes σ n)).run η) =
      liftModels (fun n => (interpret (σ n)).run η) := by
  funext n; cases n with
  | zero => rfl
  | succ n => exact interpret_type_rename _ _ _

theorem interpret_liftIndices (σ : Nat → Ty) (η : Env) (x : Term) :
    (fun n => (interpret (liftIndices σ n)).run (cons x η)) =
      (fun n => (interpret (σ n)).run η) := by
  funext n
  rw [liftIndices,interpret_index_substitution]
  rfl

theorem piModel_substitute (B : Term → Model) (h : ∀ {x y}, Conv x y → B x = B y)
    (σ : Nat → Model) :
    piModel (fun x => (B x).substitute σ)
      (fun e => congrArg (fun M : Model => M.substitute σ) (h e)) =
      (piModel B h).substitute σ := rfl

theorem sigmaModel_substitute (B : Term → Model) (h : ∀ {x y}, Conv x y → B x = B y)
    (σ : Nat → Model) :
    sigmaModel (fun x => (B x).substitute σ)
      (fun e => congrArg (fun M : Model => M.substitute σ) (h e)) =
      (sigmaModel B h).substitute σ := rfl

/-- Substitution of arbitrary dependent types for parameters. Passing through
    an index binder shifts free term indices in every substituted type; passing
    through All shifts its free type parameters. -/
theorem interpret_type_substitution (A : Ty) (σ : Nat → Ty) (η : Env) :
    (interpret (substType σ A)).run η =
      ((interpret A).run η).substitute (fun n => (interpret (σ n)).run η) := by
  induction A generalizing σ η with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | identity p q => rfl
  | arrow A B ha hb =>
      change arrowModel _ _ = _
      rw [ha,hb]; rfl
  | pi B ih =>
      change piModel (fun x => (interpret (substType (liftIndices σ) B)).run (cons x η))
        (fun h => (interpret (substType (liftIndices σ) B)).coherent (index_cons (index_refl η) h)) = _
      apply Eq.trans ?_ (piModel_substitute (fun x => (interpret B).run (cons x η))
        (fun h => (interpret B).coherent (index_cons (index_refl η) h))
        (fun n => (interpret (σ n)).run η))
      apply piModel_congr
      intro x
      rw [ih,interpret_liftIndices]
  | sigma B ih =>
      change sigmaModel (fun x => (interpret (substType (liftIndices σ) B)).run (cons x η))
        (fun h => (interpret (substType (liftIndices σ) B)).coherent (index_cons (index_refl η) h)) = _
      apply Eq.trans ?_ (sigmaModel_substitute (fun x => (interpret B).run (cons x η))
        (fun h => (interpret B).coherent (index_cons (index_refl η) h))
        (fun n => (interpret (σ n)).run η))
      apply sigmaModel_congr
      intro x
      rw [ih,interpret_liftIndices]
  | all B ih =>
      change allModel _ = _
      rw [ih,interpret_liftTypes]
      exact substitute_all _ _

def instantiateType (B A : Ty) : Ty := substType (cons A Ty.param) B

theorem interpret_type_instantiate (B A : Ty) (η : Env) :
    (interpret (instantiateType B A)).run η =
      ((interpret B).run η).substitute (cons ((interpret A).run η) varModel) := by
  rw [instantiateType,interpret_type_substitution]
  congr 1
  funext n; cases n <;> rfl

theorem type_instantiate_rel (B A : Ty) (η : Env) (r : REnv) (t u : Term) :
    ((interpret (instantiateType B A)).run η).rel r t u ↔
      ((interpret B).run η).rel (extendEnv (((interpret A).run η).asLink r) r) t u := by
  rw [interpret_type_instantiate]
  change ((interpret B).run η).rel (r.substitute (cons ((interpret A).run η) varModel)) t u ↔ _
  rw [single_rel_environment]

theorem type_instantiate_obj (B A : Ty) (η : Env) (ρ : OEnv) :
    ((interpret (instantiateType B A)).run η).obj ρ =
      ((interpret B).run η).obj (cons (((interpret A).run η).obj ρ) ρ) := by
  rw [interpret_type_instantiate]
  exact congrArg ((interpret B).run η).obj (single_obj_environment ((interpret A).run η) ρ)

end P01DF
