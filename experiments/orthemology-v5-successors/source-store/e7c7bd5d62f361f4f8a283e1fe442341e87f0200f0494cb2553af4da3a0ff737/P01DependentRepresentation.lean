/- Explicit representation into the repaired P01 candidate core and its
   DependentEnvelope interface. This is not a map to canonical unary Code. -/
import P01DependentControls
namespace P01DF
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def indexContext : P01D.Context where
  Val := Env
  eqv := IndexRelated
  refl := index_refl
  sym := fun h n => (h n).symm
  trans := fun h k n => (h n).trans (k n)
  environment := id

def candidateTy (ρ : OEnv) (A : Ty) : P01D.Ty indexContext where
  obj := fun η => ((interpret A).run η).obj ρ
  coherent := fun h => congrArg (fun M : Model => M.obj ρ) (interpret_index_transport A h)

/-- Here validity is the already-derived fundamental theorem, rather than
    a premise of the syntax or its typing judgment. Code identity is literal. -/
def candidateTm {p A} (h : Has p A) (ρ : OEnv) : P01D.Tm indexContext (candidateTy ρ A) where
  code := p
  valid := by
    intro η ξ hη
    exact (((interpret A).run η).identity ρ _ _).mp
      (fundamental h (diagEnv ρ) η ξ hη)

def candidateEnvelope {p A} (h : Has p A) (ρ : OEnv) :
    P01Certificate.DependentEnvelope indexContext (candidateTy ρ A) p :=
  ⟨candidateTm h ρ,rfl⟩

theorem candidate_envelope_code_exact {p A} (h : Has p A) (ρ : OEnv) :
    (candidateEnvelope h ρ).checked.code = p := rfl

theorem candidate_replay_sound {p A} (h : Has p A) (ρ : OEnv)
    {η ξ : Env} (hη : IndexRelated η ξ) :
    ((candidateTy ρ A).obj η).rel (eval p η) (eval p ξ) :=
  P01Certificate.dependent_envelope_sound (candidateEnvelope h ρ) hη

theorem candidate_ty_ext {Γ : P01D.Context} {A B : P01D.Ty Γ}
    (h : ∀ γ, A.obj γ = B.obj γ) : A = B := by
  have he : A.obj = B.obj := funext h
  cases A; cases B; cases he; rfl

def candidateRaw : P01D.Ty indexContext := constantTy indexContext rawPER

theorem candidate_raw_representation (ρ : OEnv) : candidateTy ρ .raw = candidateRaw := rfl

def rawIndexTm (p : Poly) : P01D.Tm indexContext candidateRaw where
  code := p
  valid := by intro η ξ h; exact eval_index_related p h

theorem candidate_identity_representation (ρ : OEnv) (p q : Poly) :
    candidateTy ρ (.identity p q) = identityTy (rawIndexTm p) (rawIndexTm q) := by
  apply candidate_ty_ext
  intro η; rfl

/-- The actual candidate-core context extension is converted back to the
    raw-index environment by cons. It is tracked by the unchanged variables. -/
def candidateBinder : P01D.Sub (P01D.extend indexContext candidateRaw) indexContext where
  map := fun γ => cons γ.val.2 γ.val.1
  respects := by
    intro γ δ h
    exact index_cons h.1 h.2
  code := Poly.var
  tracks := fun _ _ => rfl

def candidateBody (ρ : OEnv) (B : Ty) : P01D.Ty (P01D.extend indexContext candidateRaw) :=
  (candidateTy ρ B).pull candidateBinder

theorem candidate_fibre (ρ : OEnv) (B : Ty) (η : Env) (x : Term) :
    fibre (candidateBody ρ B) η x = ((interpret B).run (cons x η)).obj ρ := by
  have hx : (candidateRaw.obj η).dom x := Conv.refl x
  simp only [fibre,dif_pos hx,candidateBody,P01D.Ty.pull,candidateBinder,candidateTy]

theorem candidate_pi_representation (ρ : OEnv) (B : Ty) :
    candidateTy ρ (.pi B) = piTy (candidateBody ρ B) := by
  apply candidate_ty_ext
  intro η
  apply per_ext
  intro f g
  change (∀ x y, Conv x y → (((interpret B).run (cons x η)).obj ρ).rel (.app f x) (.app g y)) ↔
    (∀ x y, Conv x y → (fibre (candidateBody ρ B) η x).rel (.app f x) (.app g y))
  simp only [candidate_fibre]

theorem candidate_sigma_representation (ρ : OEnv) (B : Ty) :
    candidateTy ρ (.sigma B) = sigmaTy (candidateBody ρ B) := by
  apply candidate_ty_ext
  intro η
  apply per_ext
  intro z w
  change (Represented z ∧ Represented w ∧ Conv (firstTerm z) (firstTerm w) ∧
    (((interpret B).run (cons (firstTerm z) η)).obj ρ).rel (secondTerm z) (secondTerm w)) ↔
    (Represented z ∧ Represented w ∧ Conv (firstTerm z) (firstTerm w) ∧
      (fibre (candidateBody ρ B) η (firstTerm z)).rel (secondTerm z) (secondTerm w))
  rw [candidate_fibre]

theorem candidate_lambda_code {p B} (h : Has p B) (ρ : OEnv) :
    (P01D.lam ((candidateTm h ρ).subst candidateBinder)).code =
      (candidateTm (Has.piIntro h) ρ).code := by
  change abstract (psub Poly.var p) = abstract p
  rw [psub_id]

def candidateIndexSub (σ : Nat → Poly) : P01D.Sub indexContext indexContext where
  map := subIndexEnv σ
  respects := by intro η ξ h n; exact eval_index_related (σ n) h
  code := σ
  tracks := fun _ _ => rfl

theorem candidate_substitution_representation (ρ : OEnv) (A : Ty) (σ : Nat → Poly) :
    candidateTy ρ (substIndex σ A) = (candidateTy ρ A).pull (candidateIndexSub σ) := by
  apply candidate_ty_ext
  intro η
  exact congrArg (fun M : Model => M.obj ρ) (interpret_index_substitution A σ η)

theorem candidate_substitution_code {p A} (h : Has p A) (ρ : OEnv) (σ : Nat → Poly) :
    ((candidateTm h ρ).subst (candidateIndexSub σ)).code = psub σ p := rfl

def candidateAllBody (ρ : OEnv) (B : Ty) : P01D.Ty (typeExtend indexContext) where
  obj := fun γ => ((interpret B).run γ.1).obj (cons γ.2 ρ)
  coherent := by
    intro γ δ h
    have he := interpret_index_transport B h.1
    change ((interpret B).run γ.1).obj (cons γ.2 ρ) =
      ((interpret B).run δ.1).obj (cons δ.2 ρ)
    rw [he,h.2]

def candidateAllFormation (ρ : OEnv) (B : Ty) : AllFormation (candidateAllBody ρ B) where
  family := fun η => bodyFamily ((interpret B).run η) ρ
  body := fun _ _ => rfl
  coherent := fun h => congrArg (fun M : Model => bodyFamily M ρ) (interpret_index_transport B h)

theorem candidate_all_representation (ρ : OEnv) (B : Ty) :
    candidateTy ρ (.all B) = allTy (candidateAllFormation ρ B) := by
  apply candidate_ty_ext
  intro η; rfl

def candidateAllBodyTm {p B} (h : Has p B) (ρ : OEnv) :
    P01D.Tm (typeExtend indexContext) (candidateAllBody ρ B) where
  code := p
  valid := by
    intro γ δ hγ
    exact (((interpret B).run γ.1).identity (cons γ.2 ρ) _ _).mp
      (fundamental h (diagEnv (cons γ.2 ρ)) γ.1 δ.1 hγ.1)

/-- The old candidate core's additional allIntro uniformity premise is now
    discharged for every derivation of this actual finite dependent syntax. -/
theorem candidate_all_uniformity {p B} (h : Has p B) (ρ : OEnv) (η : Env) :
    Parametric ((candidateAllFormation ρ B).family η) (eval p η) := by
  intro P Q R
  exact fundamental h (extendEnv R (diagEnv ρ)) η η (index_refl η)

noncomputable def candidateAllIntro {p B} (h : Has p B) (ρ : OEnv) :
    P01D.Tm indexContext (allTy (candidateAllFormation ρ B)) :=
  P01D.allIntro (candidateAllFormation ρ B) (candidateAllBodyTm h ρ)
    (candidate_all_uniformity h ρ)

theorem candidate_all_intro_code {p B} (h : Has p B) (ρ : OEnv) :
    (candidateAllIntro h ρ).code = (candidateTm (Has.allIntro h) ρ).code := rfl

theorem candidate_type_instantiation_representation (ρ : OEnv) (B A : Ty) :
    candidateTy ρ (instantiateType B A) =
      (candidateAllBody ρ B).pull (typeInstance (candidateTy ρ A)) := by
  apply candidate_ty_ext
  intro η
  exact type_instantiate_obj B A η ρ

def candidateAllTm {p B} (h : Has p (.all B)) (ρ : OEnv) :
    P01D.Tm indexContext (allTy (candidateAllFormation ρ B)) where
  code := p
  valid := (candidateTm h ρ).valid

noncomputable def candidateAllElim {p B} (h : Has p (.all B)) (ρ : OEnv) (A : Ty) :
    P01D.Tm indexContext ((candidateAllBody ρ B).pull (typeInstance (candidateTy ρ A))) :=
  P01D.allElim (candidateAllFormation ρ B) (candidateAllTm h ρ) (candidateTy ρ A)

theorem candidate_all_elim_code {p B} (h : Has p (.all B)) (ρ : OEnv) (A : Ty) :
    (candidateAllElim h ρ A).code = (candidateTm (Has.allElim (A := A) h) ρ).code := rfl

/-- The finite bridge identifies the successor's recursive PER interpretation,
    not canonical unary Code. This exact boundary remains visible in the type. -/
theorem candidate_finite_representation (ρ : OEnv) (A : TypeCode) (η : Env) :
    (candidateTy ρ (embedFinite A)).obj η = (P01R.interpret A).obj ρ :=
  congrArg (fun M : Model => M.obj ρ) (interpret_embedFinite A η)

end P01DF
