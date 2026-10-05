/- A syntax-generated first-order dependent extension. Index equality is raw
   canonical Conv; arbitrary endpoint-aware links are used for type parameters.
   The sealed P01 meanings are imported unchanged. -/
import P01RecursiveModel
import P01ModelWitnesses
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

abbrev IndexRelated (η ξ : Env) := ∀ n, Conv (η n) (ξ n)

theorem index_refl (η : Env) : IndexRelated η η := fun _ => .refl _
theorem index_cons {η ξ : Env} (h : IndexRelated η ξ) {x y : Term}
    (hxy : Conv x y) : IndexRelated (cons x η) (cons y ξ) := by
  intro n; cases n with
  | zero => exact hxy
  | succ n => exact h n

theorem eval_index_related (p : Poly) {η ξ : Env} (h : IndexRelated η ξ) :
    Conv (eval p η) (eval p ξ) := by
  induction p with
  | var n => exact h n
  | atom t => exact .refl _
  | app f x hf hx => exact conv_app hf hx

def rawModel : Model where
  obj := fun _ => rawPER
  rel := fun _ => Conv
  endpoints := by intro r t u h; exact ⟨.refl _,.refl _⟩
  respect := by intro r t t' u u' ht hu h; exact ht.symm.trans (h.trans hu)
  identity := fun _ _ _ => Iff.rfl

def idModel (x y : Term) : Model where
  obj := fun _ => IdPER rawPER x y
  rel := fun _ => (IdPER rawPER x y).rel
  endpoints := by intro r t u h; exact ⟨PER.left h,PER.right h⟩
  respect := by
    intro r p p' q q' hp hq h
    exact (IdPER rawPER x y).trans
      ((IdPER rawPER x y).sym hp) ((IdPER rawPER x y).trans h hq)
  identity := fun _ _ _ => Iff.rfl

theorem idModel_transport {x x' y y' : Term} (hx : Conv x x') (hy : Conv y y') :
    idModel x y = idModel x' y' := by
  have h : Conv x y ↔ Conv x' y' :=
    ⟨fun h => hx.symm.trans (h.trans hy),fun h => hx.trans (h.trans hy.symm)⟩
  apply model_ext
  · intro ρ; apply per_ext; intro t u
    change (Conv x y ∧ Conv t .i ∧ Conv u .i) ↔
      (Conv x' y' ∧ Conv t .i ∧ Conv u .i)
    rw [h]
  · intro r t u
    change (Conv x y ∧ Conv t .i ∧ Conv u .i) ↔
      (Conv x' y' ∧ Conv t .i ∧ Conv u .i)
    rw [h]

/-- Dependent product over the raw-index PER. Its fibre relation is generated
    by the body model, and coherence is used in each required coordinate. -/
def piModel (B : Term → Model) (coh : ∀ {x y}, Conv x y → B x = B y) : Model where
  obj := fun ρ => PiPER rawPER (fun x => (B x).obj ρ)
    (fun h => congrArg (fun M : Model => M.obj ρ) (coh h))
  rel := fun r f g =>
    (PiPER rawPER (fun x => (B x).obj r.left)
      (fun h => congrArg (fun M : Model => M.obj r.left) (coh h))).dom f ∧
    (PiPER rawPER (fun x => (B x).obj r.right)
      (fun h => congrArg (fun M : Model => M.obj r.right) (coh h))).dom g ∧
    ∀ x y, Conv x y → (B x).rel r (.app f x) (.app g y)
  endpoints := by intro r t u h; exact ⟨h.1,h.2.1⟩
  respect := by
    intro r f f' g g' hf hg h
    refine ⟨PER.right hf,PER.right hg,?_⟩
    intro x y hxy
    have hgy : ((B y).obj r.right).rel (.app g y) (.app g' y) := hg y y (Conv.refl y)
    have he := coh hxy
    rw [← he] at hgy
    exact (B x).respect r (hf x x (.refl _)) hgy (h.2.2 x y hxy)
  identity := by
    intro ρ f g
    constructor
    · intro h x y hxy
      exact ((B x).identity ρ _ _).mp (h.2.2 x y hxy)
    · intro h
      refine ⟨PER.left h,PER.right h,?_⟩
      intro x y hxy
      exact ((B x).identity ρ _ _).mpr (h x y hxy)

/-- Represented Sigma uses actual raw pair/projection operations. -/
def sigmaModel (B : Term → Model) (coh : ∀ {x y}, Conv x y → B x = B y) : Model where
  obj := fun ρ => SigmaPER rawPER (fun x => (B x).obj ρ)
    (fun h => congrArg (fun M : Model => M.obj ρ) (coh h))
  rel := fun r z w => Represented z ∧ Represented w ∧
    Conv (firstTerm z) (firstTerm w) ∧
    (B (firstTerm z)).rel r (secondTerm z) (secondTerm w)
  endpoints := by
    intro r z w h
    have hb := (B (firstTerm z)).endpoints r h.2.2.2
    refine ⟨⟨h.1,h.1,Conv.refl _,hb.1⟩,⟨h.2.1,h.2.1,Conv.refl _,?_⟩⟩
    change ((B (firstTerm w)).obj r.right).dom (secondTerm w)
    rw [← coh h.2.2.1]
    exact hb.2
  respect := by
    intro r z z' w w' hz hw h
    have ez := coh hz.2.2.1
    have ew := coh h.2.2.1
    refine ⟨hz.2.1,hw.2.1,hz.2.2.1.symm.trans (h.2.2.1.trans hw.2.2.1),?_⟩
    have hw' : ((B (firstTerm w)).obj r.right).rel (secondTerm w) (secondTerm w') := hw.2.2.2
    rw [← ew] at hw'
    rw [← ez]
    exact (B (firstTerm z)).respect r hz.2.2.2 hw' h.2.2.2
  identity := by
    intro ρ z w
    rw [(B (firstTerm z)).identity]
    rfl

structure IndexFamily where
  run : Env → Model
  coherent : ∀ {η ξ}, IndexRelated η ξ → run η = run ξ

/-- Every constructor is finite syntax. No semantic validity, parametricity,
    arbitrary family, or uniformity evidence can be inserted into this grammar. -/
inductive Ty where
  | param : Nat → Ty
  | bottom : Ty
  | all : Ty → Ty
  | raw : Ty
  | identity : Poly → Poly → Ty
  | arrow : Ty → Ty → Ty
  | pi : Ty → Ty
  | sigma : Ty → Ty
  deriving DecidableEq

def interpret : Ty → IndexFamily
  | .param n => ⟨fun _ => varModel n,fun _ => rfl⟩
  | .bottom => ⟨fun _ => bottomModel,fun _ => rfl⟩
  | .all B => ⟨fun η => allModel ((interpret B).run η),
      fun h => congrArg allModel ((interpret B).coherent h)⟩
  | .raw => ⟨fun _ => rawModel,fun _ => rfl⟩
  | .identity p q => ⟨fun η => idModel (eval p η) (eval q η),
      fun h => idModel_transport (eval_index_related p h) (eval_index_related q h)⟩
  | .arrow A B => ⟨fun η => arrowModel ((interpret A).run η) ((interpret B).run η),
      fun h => congrArg₂ arrowModel ((interpret A).coherent h) ((interpret B).coherent h)⟩
  | .pi B => ⟨fun η => piModel (fun x => (interpret B).run (cons x η))
      (fun h => (interpret B).coherent (index_cons (index_refl η) h)), by
        intro η ξ h
        have e : (fun x => (interpret B).run (cons x η)) =
            (fun x => (interpret B).run (cons x ξ)) := by
          funext x; exact (interpret B).coherent (index_cons h (.refl x))
        simp only [e]⟩
  | .sigma B => ⟨fun η => sigmaModel (fun x => (interpret B).run (cons x η))
      (fun h => (interpret B).coherent (index_cons (index_refl η) h)), by
        intro η ξ h
        have e : (fun x => (interpret B).run (cons x η)) =
            (fun x => (interpret B).run (cons x ξ)) := by
          funext x; exact (interpret B).coherent (index_cons h (.refl x))
        simp only [e]⟩

theorem interpret_index_transport (A : Ty) {η ξ : Env} (h : IndexRelated η ξ) :
    (interpret A).run η = (interpret A).run ξ := (interpret A).coherent h

theorem dependent_identity_extension (A : Ty) (η : Env) (ρ : OEnv) (t u : Term) :
    ((interpret A).run η).rel (diagEnv ρ) t u ↔ (((interpret A).run η).obj ρ).rel t u :=
  ((interpret A).run η).identity ρ t u

theorem dependent_endpoint_restriction (A : Ty) (η : Env) (r : REnv) {t u : Term}
    (h : ((interpret A).run η).rel r t u) :
    (((interpret A).run η).obj r.left).dom t ∧
      (((interpret A).run η).obj r.right).dom u := ((interpret A).run η).endpoints r h

def substIndex (σ : Nat → Poly) : Ty → Ty
  | .param n => .param n
  | .bottom => .bottom
  | .all B => .all (substIndex σ B)
  | .raw => .raw
  | .identity p q => .identity (psub σ p) (psub σ q)
  | .arrow A B => .arrow (substIndex σ A) (substIndex σ B)
  | .pi B => .pi (substIndex (pup σ) B)
  | .sigma B => .sigma (substIndex (pup σ) B)

def subIndexEnv (σ : Nat → Poly) (η : Env) : Env := fun n => eval (σ n) η

theorem subIndexEnv_lift (σ : Nat → Poly) (η : Env) (x : Term) :
    subIndexEnv (pup σ) (cons x η) = cons x (subIndexEnv σ η) := by
  funext n; cases n with
  | zero => rfl
  | succ n => simp only [subIndexEnv,pup,eval_ren]; rfl

theorem interpret_index_substitution (A : Ty) (σ : Nat → Poly) (η : Env) :
    (interpret (substIndex σ A)).run η = (interpret A).run (subIndexEnv σ η) := by
  induction A generalizing σ η with
  | param n => rfl
  | bottom => rfl
  | all B ih => exact congrArg allModel (ih σ η)
  | raw => rfl
  | identity p q => simp only [substIndex,interpret,eval_sub]; rfl
  | arrow A B ha hb =>
      change arrowModel _ _ = arrowModel _ _
      rw [ha,hb]
  | pi B ih =>
      change piModel (fun x => (interpret (substIndex (pup σ) B)).run (cons x η))
        (fun h => (interpret (substIndex (pup σ) B)).coherent (index_cons (index_refl η) h)) = _
      have e : (fun x => (interpret (substIndex (pup σ) B)).run (cons x η)) =
          (fun x => (interpret B).run (cons x (subIndexEnv σ η))) := by
        funext x; rw [ih,subIndexEnv_lift]
      simp only [e,interpret]
  | sigma B ih =>
      change sigmaModel (fun x => (interpret (substIndex (pup σ) B)).run (cons x η))
        (fun h => (interpret (substIndex (pup σ) B)).coherent (index_cons (index_refl η) h)) = _
      have e : (fun x => (interpret (substIndex (pup σ) B)).run (cons x η)) =
          (fun x => (interpret B).run (cons x (subIndexEnv σ η))) := by
        funext x; rw [ih,subIndexEnv_lift]
      simp only [e,interpret]

def instantiate (B : Ty) (p : Poly) : Ty := substIndex (cons p Poly.var) B

theorem interpret_instantiate (B : Ty) (p : Poly) (η : Env) :
    (interpret (instantiate B p)).run η = (interpret B).run (cons (eval p η) η) := by
  rw [instantiate,interpret_index_substitution]
  congr 1
  funext n; cases n <;> rfl

def embedFinite : TypeCode → Ty
  | .var n => .param n
  | .bottom => .bottom
  | .arrow A B => .arrow (embedFinite A) (embedFinite B)
  | .all B => .all (embedFinite B)

theorem interpret_embedFinite (A : TypeCode) (η : Env) :
    (interpret (embedFinite A)).run η = P01R.interpret A := by
  induction A with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => exact congrArg₂ arrowModel ha hb
  | all B ih => exact congrArg allModel ih

end P01DF
