/- A tracked contextual dependent core over the proposed PERs. Context carriers
   contain valid valuations (a setoid presentation of the domain of a context
   PER). Terms always carry finite Poly syntax; arbitrary ambient sections are
   NOT terms. Intrinsic formation/certificate evidence is distinct from parsing.
   New attempt-0003 authored source, UNCOMPILED at Lean 4.19.0. -/
import P01PER
namespace P01D
open OrthemologyV2 OrthemologyV3
open P01F (cons)

structure Context where
  Val : Type
  eqv : Val → Val → Prop
  refl : ∀ γ, eqv γ γ
  sym : ∀ {γ δ}, eqv γ δ → eqv δ γ
  trans : ∀ {γ δ θ}, eqv γ δ → eqv δ θ → eqv γ θ
  environment : Val → Env

def nilContext : Context where
  Val := Unit
  eqv := fun _ _ => True
  refl := fun _ => True.intro
  sym := id
  trans := fun h _ => h
  environment := fun _ _ => .zero

structure Ty (Γ : Context) where
  obj : Γ.Val → PER
  coherent : ∀ {γ δ}, Γ.eqv γ δ → obj γ = obj δ

structure Tm (Γ : Context) (A : Ty Γ) where
  code : Poly
  valid : ∀ {γ δ}, Γ.eqv γ δ →
    (A.obj γ).rel (eval code (Γ.environment γ)) (eval code (Γ.environment δ))

/-- No arbitrary set-theoretic section can enter by choosing a function: a Tm
    has one finite source polynomial and a proof of its tracking property. -/
theorem tracked (Γ A) (t : Tm Γ A) : ∃p : Poly, p = t.code := ⟨t.code,rfl⟩

def Tm.at {Γ A} (t : Tm Γ A) (γ : Γ.Val) : Term := eval t.code (Γ.environment γ)
theorem Tm.member {Γ A} (t : Tm Γ A) (γ) : (A.obj γ).dom (t.at γ) := t.valid (Γ.refl γ)

def EqTm {Γ A} (t u : Tm Γ A) :=
  ∀γ δ, Γ.eqv γ δ → (A.obj γ).rel (t.at γ) (u.at δ)

theorem eqTm_refl {Γ A} (t : Tm Γ A) : EqTm t t := fun _ _ h => t.valid h

theorem eqTm_sym {Γ A} {t u : Tm Γ A} (h : EqTm t u) : EqTm u t := by
  intro γ δ hγ
  rw [A.coherent hγ]
  exact (A.obj δ).sym (h δ γ (Γ.sym hγ))

theorem eqTm_trans {Γ A} {t u v : Tm Γ A} (h : EqTm t u) (k : EqTm u v) : EqTm t v :=
  fun γ δ hγ => (A.obj γ).trans (h γ γ (Γ.refl γ)) (k γ δ hγ)

structure Sub (Δ Γ : Context) where
  map : Δ.Val → Γ.Val
  respects : ∀ {γ δ}, Δ.eqv γ δ → Γ.eqv (map γ) (map δ)
  code : Nat → Poly
  tracks : ∀γ n, eval (code n) (Δ.environment γ) = Γ.environment (map γ) n

/-- Only finitely many entries of the substitution schema occur in a finite
    Poly. The frontend represents used entries by finite syntax, never functions. -/
def Sub.id (Γ : Context) : Sub Γ Γ where
  map := _root_.id
  respects := _root_.id
  code := Poly.var
  tracks := fun _ _ => rfl

def Sub.comp {Γ Δ Θ} (σ : Sub Δ Γ) (τ : Sub Θ Δ) : Sub Θ Γ where
  map := fun γ => σ.map (τ.map γ)
  respects := fun h => σ.respects (τ.respects h)
  code := fun n => psub τ.code (σ.code n)
  tracks := by
    intro γ n
    rw [eval_sub]
    have e : (fun k => eval (τ.code k) (Θ.environment γ)) = Δ.environment (τ.map γ) :=
      funext (τ.tracks γ)
    rw [e]
    exact σ.tracks (τ.map γ) n

/-- Extensional substitution equality includes both maps and actual trackers. -/
def SubEq {Δ Γ} (σ τ : Sub Δ Γ) := σ.map = τ.map ∧ ∀n, σ.code n = τ.code n

/-- Semantic substitution equality retained from the ordinary contextual
    proposal. SubEq above is the separate stronger code-exact equality. -/
def SubRel {Δ Γ} (σ τ : Sub Δ Γ) : Prop :=
  ∀ γ δ, Δ.eqv γ δ → Γ.eqv (σ.map γ) (τ.map δ)

theorem subrel_refl {Δ Γ} (σ : Sub Δ Γ) : SubRel σ σ :=
  fun _ _ h => σ.respects h

theorem subrel_sym {Δ Γ} {σ τ : Sub Δ Γ} (h : SubRel σ τ) : SubRel τ σ :=
  fun γ δ e => Γ.sym (h δ γ (Δ.sym e))

theorem subrel_trans {Δ Γ} {σ τ υ : Sub Δ Γ}
    (h : SubRel σ τ) (k : SubRel τ υ) : SubRel σ υ :=
  fun γ δ e => Γ.trans (h γ γ (Δ.refl γ)) (k γ δ e)

theorem code_exact_substitution_implies_related {Δ Γ} {σ τ : Sub Δ Γ}
    (h : SubEq σ τ) : SubRel σ τ := by
  intro γ δ e
  have eqδ : σ.map δ = τ.map δ := congrFun h.1 δ
  exact eqδ ▸ σ.respects e

theorem subrel_composition {Γ Δ Θ} {σ σ' : Sub Δ Γ} {τ τ' : Sub Θ Δ}
    (h : SubRel σ σ') (k : SubRel τ τ') : SubRel (σ.comp τ) (σ'.comp τ') :=
  fun γ δ e => h _ _ (k γ δ e)

theorem sub_left_identity {Γ Δ} (σ : Sub Δ Γ) : SubEq ((Sub.id Γ).comp σ) σ := by
  constructor
  · rfl
  · intro n; rfl

theorem sub_right_identity {Γ Δ} (σ : Sub Δ Γ) : SubEq (σ.comp (Sub.id Δ)) σ := by
  constructor
  · rfl
  · intro n; exact psub_id (σ.code n)

theorem sub_associative {Γ Δ Θ Ξ} (σ : Sub Δ Γ) (τ : Sub Θ Δ) (υ : Sub Ξ Θ) :
    SubEq ((σ.comp τ).comp υ) (σ.comp (τ.comp υ)) := by
  constructor
  · rfl
  · intro n; exact psub_comp (σ.code n) τ.code υ.code

def Ty.pull {Γ Δ} (A : Ty Γ) (σ : Sub Δ Γ) : Ty Δ where
  obj := fun γ => A.obj (σ.map γ)
  coherent := fun h => A.coherent (σ.respects h)

def Tm.subst {Γ Δ A} (t : Tm Γ A) (σ : Sub Δ Γ) : Tm Δ (A.pull σ) where
  code := psub σ.code t.code
  valid := by
    intro γ δ hγ
    simp only [eval_sub]
    have eγ := funext (σ.tracks γ)
    have eδ := funext (σ.tracks δ)
    rw [eγ,eδ]
    exact t.valid (σ.respects hγ)

theorem related_substitution_fibres {Γ Δ} (A : Ty Γ) {σ τ : Sub Δ Γ}
    (h : SubRel σ τ) (γ) : (A.pull σ).obj γ = (A.pull τ).obj γ :=
  A.coherent (h γ γ (Δ.refl γ))

/-- The semantic, not merely code-exact, substitution congruence theorem. -/
theorem term_substitution_related {Γ Δ A} (t : Tm Γ A) {σ τ : Sub Δ Γ}
    (h : SubRel σ τ) (γ δ) (e : Δ.eqv γ δ) :
    (A.obj (σ.map γ)).rel ((t.subst σ).at γ) ((t.subst τ).at δ) := by
  change (A.obj (σ.map γ)).rel
    (eval (psub σ.code t.code) (Δ.environment γ))
    (eval (psub τ.code t.code) (Δ.environment δ))
  rw [eval_sub,eval_sub]
  have eγ := funext (σ.tracks γ)
  have eδ := funext (τ.tracks δ)
  rw [eγ,eδ]
  exact t.valid (h γ δ e)

theorem typing_under_substitution {Γ Δ A} (t : Tm Γ A) (σ : Sub Δ Γ) (γ δ) (h : Δ.eqv γ δ) :
    ((A.pull σ).obj γ).rel ((t.subst σ).at γ) ((t.subst σ).at δ) :=
  (t.subst σ).valid h

theorem term_substitution_identity {Γ A} (t : Tm Γ A) :
    (t.subst (Sub.id Γ)).code = t.code := psub_id t.code

theorem term_substitution_composition {Γ Δ Θ A} (t : Tm Γ A)
    (σ : Sub Δ Γ) (τ : Sub Θ Δ) :
    ((t.subst σ).subst τ).code = (t.subst (σ.comp τ)).code := psub_comp t.code σ.code τ.code

def extend (Γ : Context) (A : Ty Γ) : Context where
  Val := {z : Γ.Val × Term // (A.obj z.1).dom z.2}
  eqv := fun γ δ => Γ.eqv γ.val.1 δ.val.1 ∧ (A.obj γ.val.1).rel γ.val.2 δ.val.2
  refl := fun γ => ⟨Γ.refl γ.val.1,γ.property⟩
  sym := by
    intro γ δ h
    refine ⟨Γ.sym h.1,?_⟩
    rw [← A.coherent h.1]
    exact (A.obj γ.val.1).sym h.2
  trans := by
    intro γ δ θ h k
    refine ⟨Γ.trans h.1 k.1,?_⟩
    exact (A.obj γ.val.1).trans h.2 ((A.coherent h.1).symm ▸ k.2)
  environment := fun γ => cons γ.val.2 (Γ.environment γ.val.1)

def weaken (Γ A) : Sub (extend Γ A) Γ where
  map := fun γ => γ.val.1
  respects := fun h => h.1
  code := fun n => .var (n+1)
  tracks := fun _ _ => rfl

def «variable» (Γ A) : Tm (extend Γ A) (A.pull (weaken Γ A)) where
  code := .var 0
  valid := fun h => h.2

def Sub.extend {Γ Δ} (σ : Sub Δ Γ) (A : Ty Γ) (t : Tm Δ (A.pull σ)) :
    Sub Δ (extend Γ A) where
  map := fun γ => ⟨(σ.map γ,t.at γ),t.member γ⟩
  respects := fun h => ⟨σ.respects h,t.valid h⟩
  code := cons t.code σ.code
  tracks := by intro γ n; cases n with
    | zero => rfl
    | succ n => exact σ.tracks γ n

def instanceSub {Γ A} (t : Tm Γ A) : Sub Γ (extend Γ A) := (Sub.id Γ).extend A t

def instanceTy {Γ A} (B : Ty (extend Γ A)) (t : Tm Γ A) : Ty Γ := B.pull (instanceSub t)

noncomputable def fibre {Γ A} (B : Ty (extend Γ A)) (γ : Γ.Val) (x : Term) : PER := by
  classical
  exact if h : (A.obj γ).dom x then B.obj ⟨(γ,x),h⟩ else botPER

theorem fibre_cross {Γ A} (B : Ty (extend Γ A)) {γ δ x y}
    (hγ : Γ.eqv γ δ) (hxy : (A.obj γ).rel x y) : fibre B γ x = fibre B δ y := by
  classical
  have hx : (A.obj γ).dom x := PER.left hxy
  have hy : (A.obj δ).dom y := A.coherent hγ ▸ PER.right hxy
  simp only [fibre,dif_pos hx,dif_pos hy]
  exact B.coherent ⟨hγ,hxy⟩

noncomputable def piTy {Γ A} (B : Ty (extend Γ A)) : Ty Γ where
  obj := fun γ => PiPER (A.obj γ) (fibre B γ) (fibre_cross B (Γ.refl γ))
  coherent := by
    intro γ δ hγ
    apply per_ext
    intro f g
    constructor
    · intro h x y hxy
      have hp : (A.obj γ).rel x y := (A.coherent hγ).symm ▸ hxy
      rw [← fibre_cross B hγ (PER.left hp)]
      exact h x y hp
    · intro h x y hxy
      have hp : (A.obj δ).rel x y := A.coherent hγ ▸ hxy
      rw [fibre_cross B hγ (PER.left hxy)]
      exact h x y hp

noncomputable def lam {Γ A B} (b : Tm (extend Γ A) B) : Tm Γ (piTy B) where
  code := abstract b.code
  valid := by
    classical
    intro γ δ hγ x y hxy
    have hx := PER.left hxy
    have hy : (A.obj δ).dom y := A.coherent hγ ▸ PER.right hxy
    have hb := b.valid (show (extend Γ A).eqv ⟨(γ,x),hx⟩ ⟨(δ,y),hy⟩ from ⟨hγ,hxy⟩)
    simp only [piTy, PiPER, fibre, dif_pos hx]
    exact (B.obj ⟨(γ,x),hx⟩).raw
      (P01Source.red_conv (abstraction_beta b.code (Γ.environment γ) x)).symm
      (P01Source.red_conv (abstraction_beta b.code (Γ.environment δ) y)).symm hb

noncomputable def app {Γ A B} (f : Tm Γ (piTy B)) (a : Tm Γ A) : Tm Γ (instanceTy B a) where
  code := .app f.code a.code
  valid := by
    classical
    intro γ δ hγ
    have h := f.valid hγ (a.at γ) (a.at δ) (a.valid hγ)
    change (fibre B γ (a.at γ)).rel _ _ at h
    rw [fibre, dif_pos (a.member γ)] at h
    exact h

/-- Congruence is proved at Pi equality by related applications, not raw Conv
    of the two abstracted SKI polynomials. -/
theorem abstraction_congruence {Γ A B} {b c : Tm (extend Γ A) B} (h : EqTm b c) :
    EqTm (lam b) (lam c) := by
  classical
  intro γ δ hγ x y hxy
  have hx := PER.left hxy
  have hy : (A.obj δ).dom y := A.coherent hγ ▸ PER.right hxy
  have hb := h ⟨(γ,x),hx⟩ ⟨(δ,y),hy⟩ ⟨hγ,hxy⟩
  simp only [piTy,PiPER,fibre,dif_pos hx]
  exact (B.obj ⟨(γ,x),hx⟩).raw
    (P01Source.red_conv (abstraction_beta b.code (Γ.environment γ) x)).symm
    (P01Source.red_conv (abstraction_beta c.code (Γ.environment δ) y)).symm hb

theorem pi_beta {Γ A B} (b : Tm (extend Γ A) B) (a : Tm Γ A) (γ : Γ.Val) :
    Conv ((app (lam b) a).at γ) ((b.subst (instanceSub a)).at γ) := by
  change Conv (.app (eval (abstract b.code) (Γ.environment γ)) (a.at γ))
    (eval (psub (instanceSub a).code b.code) (Γ.environment γ))
  rw [eval_sub]
  have e : (fun n => eval ((instanceSub a).code n) (Γ.environment γ)) =
      cons (a.at γ) (Γ.environment γ) := by
    funext n
    cases n <;> rfl
  rw [e]
  exact P01Source.red_conv (abstraction_beta b.code (Γ.environment γ) (a.at γ))

noncomputable def sigmaTy {Γ A} (B : Ty (extend Γ A)) : Ty Γ where
  obj := fun γ => SigmaPER (A.obj γ) (fibre B γ) (fibre_cross B (Γ.refl γ))
  coherent := by
    intro γ δ hγ
    apply per_ext
    intro z w
    constructor
    · intro h
      have hp := h.2.2.1
      refine ⟨h.1,h.2.1,A.coherent hγ ▸ hp,?_⟩
      rw [← fibre_cross B hγ (PER.left hp)]
      exact h.2.2.2
    · intro h
      have hp : (A.obj γ).rel (firstTerm z) (firstTerm w) :=
        (A.coherent hγ).symm ▸ h.2.2.1
      refine ⟨h.1,h.2.1,hp,?_⟩
      rw [fibre_cross B hγ (PER.left hp)]
      exact h.2.2.2

noncomputable def pair {Γ A B} (a : Tm Γ A) (b : Tm Γ (instanceTy B a)) : Tm Γ (sigmaTy B) where
  code := pairPoly a.code b.code
  valid := by
    classical
    intro γ δ hγ
    apply sigma_pair (coh := fibre_cross B (Γ.refl γ)) (a.valid hγ)
    change (fibre B γ (a.at γ)).rel _ _
    rw [fibre, dif_pos (a.member γ)]
    exact b.valid hγ

noncomputable def fst {Γ : Context} {A : Ty Γ} {B : Ty (extend Γ A)} (z : Tm Γ (sigmaTy B)) : Tm Γ A where
  code := fstPoly z.code
  valid := fun h => (z.valid h).2.2.1

noncomputable def snd {Γ : Context} {A : Ty Γ} {B : Ty (extend Γ A)} (z : Tm Γ (sigmaTy B)) : Tm Γ (instanceTy B (fst z)) where
  code := sndPoly z.code
  valid := by
    classical
    intro γ δ hγ
    have h := (z.valid hγ).2.2.2
    have hz : (A.obj γ).dom (firstTerm (z.at γ)) := PER.left (z.valid hγ).2.2.1
    change (fibre B γ (firstTerm (z.at γ))).rel _ _ at h
    rw [fibre, dif_pos hz] at h
    exact h

theorem sigma_beta_first {Γ A B} (a : Tm Γ A) (b : Tm Γ (instanceTy B a)) (γ) :
    Conv ((fst (pair a b)).at γ) (a.at γ) := pair_first (a.at γ) (b.at γ)

theorem sigma_beta_second {Γ A B} (a : Tm Γ A) (b : Tm Γ (instanceTy B a)) (γ) :
    Conv ((snd (pair a b)).at γ) (b.at γ) := pair_second (a.at γ) (b.at γ)

theorem sigma_eta_context {Γ : Context} {A : Ty Γ} {B : Ty (extend Γ A)} (z : Tm Γ (sigmaTy B)) (γ) :
    Conv (z.at γ) ((pair (fst z) (snd z)).at γ) :=
  sigma_eta (coh := fibre_cross B (Γ.refl γ)) (z.member γ)

noncomputable def identityTy {Γ A} (x y : Tm Γ A) : Ty Γ where
  obj := fun γ => IdPER (A.obj γ) (x.at γ) (y.at γ)
  coherent := by
    intro γ δ hγ
    apply per_ext
    intro p q
    have hx := x.valid hγ
    have hy := y.valid hγ
    constructor
    · intro h
      refine ⟨?_,h.2.1,h.2.2⟩
      rw [← A.coherent hγ]
      exact (A.obj γ).trans ((A.obj γ).sym hx) ((A.obj γ).trans h.1 hy)
    · intro h
      refine ⟨?_,h.2.1,h.2.2⟩
      have hp : (A.obj γ).rel (x.at δ) (y.at δ) := (A.coherent hγ).symm ▸ h.1
      exact (A.obj γ).trans hx ((A.obj γ).trans hp ((A.obj γ).sym hy))

noncomputable def reflTm {Γ A} (x : Tm Γ A) : Tm Γ (identityTy x x) where
  code := .atom .i
  valid := fun {γ δ} _ => id_intro (x.member γ)

/-- A type-variable context extension changes the code environment but leaves
    the runtime term-variable environment alone. This is the second sort. -/
def typeExtend (Γ : Context) : Context where
  Val := Γ.Val × PER
  eqv := fun γ δ => Γ.eqv γ.1 δ.1 ∧ γ.2 = δ.2
  refl := fun γ => ⟨Γ.refl γ.1,rfl⟩
  sym := fun h => ⟨Γ.sym h.1,h.2.symm⟩
  trans := fun h k => ⟨Γ.trans h.1 k.1,h.2.trans k.2⟩
  environment := fun γ => Γ.environment γ.1

def typeWeaken (Γ) : Sub (typeExtend Γ) Γ where
  map := Prod.fst
  respects := fun h => h.1
  code := Poly.var
  tracks := fun _ _ => rfl

def typeVariable (Γ) : Ty (typeExtend Γ) where
  obj := Prod.snd
  coherent := fun h => h.2

def typeInstance {Γ} (A : Ty Γ) : Sub Γ (typeExtend Γ) where
  map := fun γ => (γ,A.obj γ)
  respects := fun h => ⟨h,A.coherent h⟩
  code := Poly.var
  tracks := fun _ _ => rfl

/-- Explicit parametric interpretation data for a formed body, not a unary-Code
    membership assumption. Uniformity is a *proof obligation*, not a runtime
    annotation allowed to self-attest. See the abstraction theorem preservation
    document for its source-derivation discharge. -/
structure AllFormation {Γ} (B : Ty (typeExtend Γ)) where
  family : Γ.Val → ParamFamily
  body : ∀ γ P, (family γ).obj P = B.obj (γ,P)
  coherent : ∀ {γ δ}, Γ.eqv γ δ → family γ = family δ

noncomputable def allTy {Γ B} (F : @AllFormation Γ B) : Ty Γ where
  obj := fun γ => AllPER (F.family γ)
  coherent := fun h => congrArg AllPER (F.coherent h)

/-- A single finite body tracker is retained for all instantiations. Endpoint
    unary typing alone is intentionally insufficient for this constructor. -/
noncomputable def allIntro {Γ B} (F : @AllFormation Γ B) (b : Tm (typeExtend Γ) B)
    (uniform : ∀ γ, Parametric (F.family γ) (eval b.code (Γ.environment γ))) :
    Tm Γ (allTy F) where
  code := b.code
  valid := by
    intro γ δ hγ
    refine ⟨uniform γ,?_,?_⟩
    · rw [F.coherent hγ]
      exact uniform δ
    · intro P
      rw [F.body γ P]
      exact b.valid (γ := (γ,P)) (δ := (δ,P)) ⟨hγ,rfl⟩

noncomputable def allElim {Γ B} (F : @AllFormation Γ B)
    (t : Tm Γ (allTy F)) (A : Ty Γ) : Tm Γ (B.pull (typeInstance A)) where
  code := t.code
  valid := by
    intro γ δ hγ
    have h := (t.valid hγ).2.2 (A.obj γ)
    simpa only [F.body γ (A.obj γ),Ty.pull,typeInstance] using h

/-- The internal result is itself a legal PER argument. This theorem has no
    same-level Type:Type, decoder, or ambient-section reification conclusion. -/
noncomputable def allSelf {Γ B} (F : @AllFormation Γ B) (t : Tm Γ (allTy F)) :
    Tm Γ (B.pull (typeInstance (allTy F))) := allElim F t (allTy F)

end P01D
