import ImportedCompilerTransport

/- A new unary interpretation on the frozen finite OPEN-term reduct.
No inherited F/G interpretation or soundness theorem is used below. -/
namespace TaggedPER
open P01AC P01D
open OpenTermStandardness (T SatPER Conv Arrow arrowPER churchPER)
open ImportedOpenTermTransport (embed interp)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev Rel := T → T → Prop
abbrev REnv := Nat → Rel
abbrev Env := Nat → T
def cons {α : Type} (a : α) (η : Nat → α) : Nat → α
  | 0 => a
  | n+1 => η n

structure Laws (R : Rel) : Prop where
  sym : ∀ {a b}, R a b → R b a
  trans : ∀ {a b c}, R a b → R b c → R a c
  raw : ∀ {a b a' b'}, Conv a a' → Conv b b' → R a b → R a' b'
def Laws.object {R} (h : Laws R) : SatPER := ⟨R,h.sym,h.trans,h.raw⟩
def admissible (ρ : REnv) := ∀ n, Laws (ρ n)
theorem per_laws (P : SatPER) : Laws P.rel := ⟨P.symm,P.trans,P.saturated⟩
theorem admissible_cons {ρ} (h : admissible ρ) (P : SatPER) : admissible (cons P.rel ρ) := by
  intro n; cases n with
  | zero => exact per_laws P
  | succ n => exact h n

theorem Laws.left {R} (h : Laws R) {a b} (v : R a b) : R a a := h.trans v (h.sym v)
theorem Laws.right {R} (h : Laws R) {a b} (v : R a b) : R b b := h.trans (h.sym v) v

abbrev pair := OpenTermStandardness.pair
abbrev first := OpenTermStandardness.fst
abbrev second := OpenTermStandardness.snd

def tag (z : T) : Prop := Conv z (pair (first z) (second z))
theorem tag_congr {z w : T} (h : Conv z w) : tag z ↔ tag w := by
  have hp := OpenTermStandardness.pair_congr (OpenTermStandardness.fst_congr h) (OpenTermStandardness.snd_congr h)
  exact ⟨fun t => h.symm.trans (t.trans hp), fun t => h.trans (t.trans hp.symm)⟩
theorem tag_pair (a b : T) : tag (pair a b) :=
  (OpenTermStandardness.pair_congr (OpenTermStandardness.fst_pair a b) (OpenTermStandardness.snd_pair a b)).symm

def F : Ty → REnv → Env → Rel
  | .param n, ρ, _ => ρ n
  | .bottom, _, _ => fun _ _ => False
  | .raw, _, _ => Conv
  | .pi A B, ρ, η => fun f g => ∀ x y, F A ρ η x y → F B ρ (cons x η) (f ⬝ x) (g ⬝ y)
  | .sigma A B, ρ, η => fun z w => F A ρ η (first z) (first w) ∧
      F B ρ (cons (first z) η) (second z) (second w) ∧ (tag z ↔ tag w)
  | .identity A p q, ρ, η => fun u v => F A ρ η (interp p η) (interp q η) ∧ Conv u .i ∧ Conv v .i
  | .all B, ρ, η => fun u v => ∀ P : SatPER, F B (cons P.rel ρ) η u v

@[simp] theorem interp_var (n : Nat) (η : Env) : interp (.var n) η = η n := rfl
@[simp] theorem interp_atom (t : OrthemologyV2.Term) (η : Env) : interp (.atom t) η = embed t := rfl
@[simp] theorem interp_app (f a : Poly) (η : Env) : interp (.app f a) η = interp f η ⬝ interp a η := rfl

theorem interp_sub (p : Poly) (σ : Nat → Poly) (η : Env) :
    interp (P01D.psub σ p) η = interp p (fun n => interp (σ n) η) := by
  induction p with
  | var n => rfl
  | atom t => rfl
  | app f a hf ha => simp only [P01D.psub,interp_app,hf,ha]
theorem interp_ren (p : Poly) (r : Nat → Nat) (η : Env) :
    interp (P01D.pren r p) η = interp p (fun n => η (r n)) := interp_sub p _ η
@[simp] theorem interp_pup (σ : Nat → Poly) (η : Env) (a : T) :
    (fun n => interp (P01D.pup σ n) (cons a η)) = cons a (fun n => interp (σ n) η) := by
  funext n; cases n <;> simp [P01D.pup,interp_ren,cons, P01F.cons]
@[simp] theorem interp_cons (a : Poly) (σ : Nat → Poly) (η : Env) :
    (fun n => interp (P01F.cons a σ n) η) = cons (interp a η) (fun n => interp (σ n) η) := by
  funext n; cases n <;> rfl

theorem F_subst (A : Ty) (σ : Nat → Poly) (ρ : REnv) (η : Env) :
    F (P01AC.subst σ A) ρ η = F A ρ (fun n => interp (σ n) η) := by
  induction A generalizing σ ρ η with
  | param n | bottom | raw => rfl
  | pi A B ha hb | sigma A B ha hb => simp only [P01AC.subst,F,ha,hb,interp_pup]
  | identity A p q ha => simp only [P01AC.subst,F,ha,interp_sub]
  | all B hb => simp only [P01AC.subst,F,hb]
@[simp] theorem F_wk (A : Ty) (ρ : REnv) (η : Env) (a : T) :
    F (P01AC.wk A) ρ (cons a η) = F A ρ η := F_subst A _ ρ _
theorem F_inst (B : Ty) (a : Poly) (ρ : REnv) (η : Env) :
    F (P01AC.inst B a) ρ η = F B ρ (cons (interp a η) η) := by
  simpa only [P01AC.inst,interp_cons,interp_var] using F_subst B (P01F.cons a Poly.var) ρ η
theorem F_motiveAt (B : Ty) (y e : Poly) (ρ : REnv) (η : Env) :
    F (motiveAt B y e) ρ η = F B ρ (cons (interp e η) (cons (interp y η) η)) := by
  simpa only [motiveAt,interp_cons,interp_var] using F_subst B (P01F.cons e (P01F.cons y Poly.var)) ρ η
@[simp] theorem F_arr (A B : Ty) (ρ : REnv) (η : Env) :
    F (arr A B) ρ η = Arrow (F A ρ η) (F B ρ η) := by
  funext f g; simp only [arr,F,F_wk,Arrow]

theorem F_trename (A : Ty) (r : Nat → Nat) (ρ : REnv) (η : Env) :
    F (trename r A) ρ η = F A (fun n => ρ (r n)) η := by
  induction A generalizing r ρ η with
  | param n | bottom | raw => rfl
  | pi A B ha hb | sigma A B ha hb => simp only [trename,F,ha,hb]
  | identity A p q ha => simp only [trename,F,ha]
  | all B hb =>
      simp only [trename,F,hb]
      have henv : ∀ P : SatPER, (fun n => cons P.rel ρ (OrthemologyV3.liftRen r n)) = cons P.rel (fun n => ρ (r n)) := by
        intro P; funext n; cases n <;> rfl
      simp only [henv]
@[simp] theorem F_twk (A : Ty) (R : Rel) (ρ : REnv) (η : Env) :
    F (twk A) (cons R ρ) η = F A ρ η := F_trename A _ _ _

theorem F_mixed (B : Ty) (σ : Nat → Poly) (τ : Nat → Ty) (ρ : REnv) (η : Env) :
    F (mixed σ τ B) ρ η = F B (fun n => F (τ n) ρ η) (fun n => interp (σ n) η) := by
  induction B generalizing σ τ ρ η with
  | param n | bottom | raw => rfl
  | identity A p q ha => simp only [mixed,F,ha,interp_sub]
  | pi A B ha hb | sigma A B ha hb => simp only [mixed,F,ha,hb,F_wk,interp_pup]
  | all B hb =>
      simp only [mixed,F,hb]
      have henv : ∀ P : SatPER, (fun n => F (tup τ n) (cons P.rel ρ) η) = cons P.rel (fun n => F (τ n) ρ η) := by
        intro P; funext n; cases n with
        | zero => rfl
        | succ n => exact F_twk _ _ _ _
      simp only [henv]
theorem F_tsubst (B : Ty) (τ : Nat → Ty) (ρ : REnv) (η : Env) :
    F (tsubst τ B) ρ η = F B (fun n => F (τ n) ρ η) η := F_mixed B _ _ _ _
theorem F_tinst (B A : Ty) (ρ : REnv) (η : Env) :
    F (tinst B A) ρ η = F B (cons (F A ρ η) ρ) η := by
  rw [tinst,F_tsubst]
  have henv : (fun n => F (P01F.cons A Ty.param n) ρ η) = cons (F A ρ η) ρ := by
    funext n; cases n <;> rfl
  rw [henv]

def zeroEnv : Env := fun _ => .zero
def tail (η : Env) : Env := fun n => η (n+1)
def D : Tel → REnv → Env → Prop
  | [], _, η => η = zeroEnv
  | A :: Γ, ρ, η => D Γ ρ (tail η) ∧ F A ρ (tail η) (η 0) (η 0)
def E : Tel → REnv → Env → Env → Prop
  | [], _, η, ξ => η = zeroEnv ∧ ξ = zeroEnv
  | A :: Γ, ρ, η, ξ => E Γ ρ (tail η) (tail ξ) ∧ F A ρ (tail η) (η 0) (ξ 0)
@[simp] theorem tail_cons (a : T) (η : Env) : tail (cons a η) = η := rfl
@[simp] theorem cons_head_tail (η : Env) : cons (η 0) (tail η) = η := by funext n; cases n <;> rfl
@[simp] theorem D_twk (Γ : Tel) (R : Rel) (ρ : REnv) (η : Env) :
    D (twkTel Γ) (cons R ρ) η = D Γ ρ η := by
  induction Γ generalizing η with
  | nil => rfl
  | cons A Γ ih => simp only [twkTel,List.map_cons,D,F_twk]; rw [← twkTel,ih]
@[simp] theorem E_twk (Γ : Tel) (R : Rel) (ρ : REnv) (η ξ : Env) :
    E (twkTel Γ) (cons R ρ) η ξ = E Γ ρ η ξ := by
  induction Γ generalizing η ξ with
  | nil => rfl
  | cons A Γ ih => simp only [twkTel,List.map_cons,E,F_twk]; rw [← twkTel,ih]

structure ContextLaws (Γ : Tel) : Prop where
  refl : ∀ {ρ η}, admissible ρ → D Γ ρ η → E Γ ρ η η
  ends : ∀ {ρ η ξ}, admissible ρ → E Γ ρ η ξ → D Γ ρ η ∧ D Γ ρ ξ
  sym : ∀ {ρ η ξ}, admissible ρ → E Γ ρ η ξ → E Γ ρ ξ η
  trans : ∀ {ρ η ξ ζ}, admissible ρ → E Γ ρ η ξ → E Γ ρ ξ ζ → E Γ ρ η ζ
structure TypeLaws (Γ : Tel) (A : Ty) : Prop where
  per : ∀ {ρ η}, admissible ρ → D Γ ρ η → Laws (F A ρ η)
  transport : ∀ {ρ η ξ}, admissible ρ → E Γ ρ η ξ → F A ρ η = F A ρ ξ
def Fundamental (Γ : Tel) (p : Poly) (A : Ty) : Prop :=
  ∀ (ρ : REnv) (η ξ : Env), admissible ρ → E Γ ρ η ξ → F A ρ η (interp p η) (interp p ξ)


theorem context_nil : ContextLaws [] where
  refl := fun _ h => ⟨h,h⟩
  ends := fun _ h => h
  sym := fun _ h => ⟨h.2,h.1⟩
  trans := fun _ h k => ⟨h.1,k.2⟩

theorem context_ext {Γ A} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) : ContextLaws (A :: Γ) where
  refl := fun r h => ⟨hc.refl r h.1,h.2⟩
  ends := by
    intro ρ η ξ r e
    have d := hc.ends r e.1
    exact ⟨⟨d.1,(ha.per r d.1).left e.2⟩,
      ⟨d.2,(ha.transport r e.1) ▸ ((ha.per r d.1).right e.2)⟩⟩
  sym := by
    intro ρ η ξ r e
    exact ⟨hc.sym r e.1,(ha.transport r e.1) ▸ ((ha.per r (hc.ends r e.1).1).sym e.2)⟩
  trans := by
    intro ρ η ξ ζ r e f
    exact ⟨hc.trans r e.1 f.1,(ha.per r (hc.ends r e.1).1).trans e.2 ((ha.transport r e.1).symm ▸ f.2)⟩

theorem type_param (Γ : Tel) (n : Nat) : TypeLaws Γ (.param n) where
  per := fun r _ => r n
  transport := fun _ _ => rfl

theorem type_bottom (Γ : Tel) : TypeLaws Γ .bottom where
  per := fun _ _ => ⟨False.elim,fun h _ => h,fun _ _ h => h⟩
  transport := fun _ _ => rfl

theorem type_raw (Γ : Tel) : TypeLaws Γ .raw where
  per := fun _ _ => ⟨Conv.symm,Conv.trans,fun a b h => a.symm.trans (h.trans b)⟩
  transport := fun _ _ => rfl

theorem type_identity {Γ A p q} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hp : Fundamental Γ p A) (hq : Fundamental Γ q A) : TypeLaws Γ (.identity A p q) where
  per := fun _ _ => {
    sym := fun h => ⟨h.1,h.2.2,h.2.1⟩
    trans := fun h k => ⟨h.1,h.2.1,k.2.2⟩
    raw := fun cp cq h => ⟨h.1,cp.symm.trans h.2.1,cq.symm.trans h.2.2⟩ }
  transport := by
    intro ρ η ξ r e
    have l := ha.per r (hc.ends r e).1
    have pp := hp ρ η ξ r e
    have qq := hq ρ η ξ r e
    have eqv : F A ρ η (interp p η) (interp q η) ↔ F A ρ ξ (interp p ξ) (interp q ξ) := by
      constructor
      · intro v; exact (ha.transport r e) ▸ l.trans (l.sym pp) (l.trans v qq)
      · intro v; exact l.trans pp (l.trans ((ha.transport r e).symm ▸ v) (l.sym qq))
    funext u v
    exact propext (and_congr eqv Iff.rfl)

theorem type_pi {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) : TypeLaws Γ (.pi A B) where
  per := by
    intro ρ η r d
    have la := ha.per r d
    exact {
      sym := by
        intro f g h a b ab
        have da : D (A :: Γ) ρ (cons a η) := ⟨d,la.left ab⟩
        have e : E (A :: Γ) ρ (cons b η) (cons a η) := ⟨hc.refl r d,la.sym ab⟩
        exact (hb.per r da).sym ((hb.transport r e) ▸ (h b a (la.sym ab)))
      trans := by
        intro f g h fg gh a b ab
        exact (hb.per (η := cons a η) r ⟨d,la.left ab⟩).trans (fg a a (la.left ab)) (gh a b ab)
      raw := by
        intro f g f' g' cf cg h a b ab
        exact (hb.per (η := cons a η) r ⟨d,la.left ab⟩).raw (.app cf (.refl _)) (.app cg (.refl _)) (h a b ab) }
  transport := by
    intro ρ η ξ r e
    have ds := hc.ends r e
    funext f g
    apply propext
    constructor
    · intro h a b ab
      have ab' := (ha.transport r e).symm ▸ ab
      exact (hb.transport (η := cons a η) (ξ := cons a ξ) r ⟨e,(ha.per r ds.1).left ab'⟩) ▸ (h a b ab')
    · intro h a b ab
      have ab' := (ha.transport r e) ▸ ab
      exact (hb.transport (η := cons a η) (ξ := cons a ξ) r ⟨e,(ha.per r ds.1).left ab⟩).symm ▸ (h a b ab')

theorem type_sigma {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) : TypeLaws Γ (.sigma A B) where
  per := by
    intro ρ η r d
    have la := ha.per r d
    exact {
      sym := by
        intro z w h
        have e : E (A :: Γ) ρ (cons (first z) η) (cons (first w) η) := ⟨hc.refl r d,h.1⟩
        exact ⟨la.sym h.1,(hb.transport r e) ▸ ((hb.per (η := cons (first z) η) r ⟨d,la.left h.1⟩).sym h.2.1),h.2.2.symm⟩
      trans := by
        intro z w v h k
        have e : E (A :: Γ) ρ (cons (first z) η) (cons (first w) η) := ⟨hc.refl r d,h.1⟩
        exact ⟨la.trans h.1 k.1,
          (hb.per (η := cons (first z) η) r ⟨d,la.left h.1⟩).trans h.2.1 ((hb.transport r e).symm ▸ k.2.1),h.2.2.trans k.2.2⟩
      raw := by
        intro z w z' w' cz cw h
        have fz := OpenTermStandardness.fst_congr cz
        have fw := OpenTermStandardness.fst_congr cw
        have sz := OpenTermStandardness.snd_congr cz
        have sw := OpenTermStandardness.snd_congr cw
        have e : E (A :: Γ) ρ (cons (first z) η) (cons (first z') η) :=
          ⟨hc.refl r d,la.raw (.refl _) fz (la.left h.1)⟩
        exact ⟨la.raw fz fw h.1,(hb.transport r e) ▸ ((hb.per (η := cons (first z) η) r ⟨d,la.left h.1⟩).raw sz sw h.2.1), (tag_congr cz).symm.trans (h.2.2.trans (tag_congr cw))⟩ }
  transport := by
    intro ρ η ξ r e
    have ds := hc.ends r e
    funext z w
    apply propext
    constructor
    · intro h
      have ex : E (A :: Γ) ρ (cons (first z) η) (cons (first z) ξ) := ⟨e,(ha.per r ds.1).left h.1⟩
      exact ⟨(ha.transport r e) ▸ h.1,(hb.transport r ex) ▸ h.2.1,h.2.2⟩
    · intro h
      have hz := (ha.transport r e).symm ▸ h.1
      have ex : E (A :: Γ) ρ (cons (first z) η) (cons (first z) ξ) := ⟨e,(ha.per r ds.1).left hz⟩
      exact ⟨hz,(hb.transport r ex).symm ▸ h.2.1,h.2.2⟩

theorem type_all {Γ B} (hb : TypeLaws (twkTel Γ) B) : TypeLaws Γ (.all B) where
  per := by
    intro ρ η r d
    have bd : ∀ P : SatPER, D (twkTel Γ) (cons P.rel ρ) η := fun P => (D_twk Γ P.rel ρ η).symm ▸ d
    exact {
      sym := fun h P => (hb.per (admissible_cons r P) (bd P)).sym (h P)
      trans := fun h k P => (hb.per (admissible_cons r P) (bd P)).trans (h P) (k P)
      raw := fun ct cu h P => (hb.per (admissible_cons r P) (bd P)).raw ct cu (h P) }
  transport := by
    intro ρ η ξ r e
    have eqv : ∀ P : SatPER, F B (cons P.rel ρ) η = F B (cons P.rel ρ) ξ := by
      intro P
      exact hb.transport (admissible_cons r P) ((E_twk Γ P.rel ρ η ξ).symm ▸ e)
    simp only [F,eqv]


theorem fundamental_var {Γ n A} (v : Lookup Γ n A) : Fundamental Γ (.var n) A := by
  intro ρ η ξ r h
  induction v generalizing η ξ with
  | @zero A Γ =>
      have hh := h.2
      rw [← cons_head_tail η, F_wk]
      exact hh
  | @succ Γ n A B v ih =>
      rw [← cons_head_tail η, F_wk]
      exact ih (tail η) (tail ξ) h.1

theorem fundamental_pi_intro {Γ A B b} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) (ht : Fundamental (A :: Γ) b B) :
    Fundamental Γ (P01D.abstract b) (.pi A B) := by
  intro ρ η ξ r h a a' aa
  have e : E (A :: Γ) ρ (cons a η) (cons a' ξ) := ⟨h,aa⟩
  have cc := context_ext hc ha
  exact (hb.per r (cc.ends r e).1).raw
    (ImportedOpenTermTransport.interp_abstraction_beta b η a).symm
    (ImportedOpenTermTransport.interp_abstraction_beta b ξ a').symm (ht ρ _ _ r e)

theorem fundamental_pi_elim {Γ A B f a} (hf : Fundamental Γ f (.pi A B))
    (ha : Fundamental Γ a A) : Fundamental Γ (.app f a) (inst B a) := by
  intro ρ η ξ r h
  rw [F_inst]
  exact hf ρ η ξ r h _ _ (ha ρ η ξ r h)

theorem fundamental_all_intro {Γ B p} (ht : Fundamental (twkTel Γ) p B) :
    Fundamental Γ p (.all B) := by
  intro ρ η ξ r h P
  exact ht (cons P.rel ρ) η ξ (admissible_cons r P) ((E_twk Γ P.rel ρ η ξ).symm ▸ h)

theorem fundamental_all_elim {Γ B A p} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (ht : Fundamental Γ p (.all B)) : Fundamental Γ p (tinst B A) := by
  intro ρ η ξ r h
  rw [F_tinst]
  exact ht ρ η ξ r h (ha.per r (hc.ends r h).1).object

theorem F_pair {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) {ρ η a a' b b'} (r : admissible ρ) (d : D Γ ρ η)
    (aa : F A ρ η a a') (bb : F B ρ (cons a η) b b') :
    F (.sigma A B) ρ η (pair a b) (pair a' b') := by
  have la := ha.per r d
  have e : E (A :: Γ) ρ (cons a η) (cons (first (pair a b)) η) :=
    ⟨hc.refl r d,la.raw (.refl _) (OpenTermStandardness.fst_pair a b).symm (la.left aa)⟩
  exact ⟨la.raw (OpenTermStandardness.fst_pair a b).symm (OpenTermStandardness.fst_pair a' b').symm aa,
    (hb.transport r e) ▸ ((hb.per (η := cons a η) r ⟨d,la.left aa⟩).raw
      (OpenTermStandardness.snd_pair a b).symm (OpenTermStandardness.snd_pair a' b').symm bb),⟨fun _ => tag_pair _ _,fun _ => tag_pair _ _⟩⟩

theorem fundamental_sigma_intro {Γ A B a b} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) (hta : Fundamental Γ a A) (htb : Fundamental Γ b (inst B a)) :
    Fundamental Γ (P01D.pairPoly a b) (.sigma A B) := by
  intro ρ η ξ r h
  have vb := htb ρ η ξ r h
  rw [F_inst] at vb
  exact F_pair hc ha hb r (hc.ends r h).1 (hta ρ η ξ r h) vb

theorem fundamental_sigma_fst {Γ A B z} (hz : Fundamental Γ z (.sigma A B)) :
    Fundamental Γ (P01D.fstPoly z) A := fun ρ η ξ r h => (hz ρ η ξ r h).1

theorem fundamental_sigma_snd {Γ A B z} (hz : Fundamental Γ z (.sigma A B)) :
    Fundamental Γ (P01D.sndPoly z) (inst B (P01D.fstPoly z)) := by
  intro ρ η ξ r h
  rw [F_inst]
  exact (hz ρ η ξ r h).2.1

theorem fundamental_identity_intro {Γ A p q} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hp : Fundamental Γ p A) (pq : P01AC.Intensional.Plus.PolyConvPlus p q) :
    Fundamental Γ (.atom .i) (.identity A p q) := by
  intro ρ η ξ r h
  have pp := hp ρ η η r (hc.refl r (hc.ends r h).1)
  exact ⟨(ha.per r (hc.ends r h).1).raw (.refl _) (ImportedOpenTermTransport.source_plus_sound pq η) pp,
    .refl _,.refl _⟩

theorem fundamental_proof_erase {Γ A x y p} (hp : Fundamental Γ p (.identity A x y)) :
    Fundamental Γ p .raw := by
  intro ρ η ξ r h
  have v := hp ρ η ξ r h
  exact v.2.1.trans v.2.2.symm

theorem interp_j (d y e : Poly) (η : Env) : Conv (interp (P01D.jPoly d y e) η) (interp d η) :=
  (Conv.app (.k (.k ⬝ interp d η) (interp y η)) (.refl _)).trans (.k _ _)

/-- J transports only across the related endpoint/proof coordinates in its ACTUAL
    theta context. Motive invariance is an induction conclusion, not a premise of HasE. -/
theorem fundamental_j {Γ A B x y e d} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (theta Γ A x) B) (ht : TypeLaws Γ (motiveAt B y e))
    (he : Fundamental Γ e (.identity A x y)) (hd : Fundamental Γ d (motiveAt B x (.atom .i))) :
    Fundamental Γ (P01D.jPoly d y e) (motiveAt B y e) := by
  intro ρ η ξ r h
  have ds := hc.ends r h
  have ep := he ρ η ξ r h
  have el : E (theta Γ A x) ρ (cons .i (cons (interp x η) η))
      (cons (interp e η) (cons (interp y η) η)) := by
    refine ⟨⟨hc.refl r ds.1,ep.1⟩,?_⟩
    change F (wk A) ρ (cons (interp x η) η)
      (interp (P01D.pren Nat.succ x) (cons (interp x η) η)) (interp x η) ∧
      Conv T.i T.i ∧ Conv (interp e η) T.i
    rw [interp_ren,F_wk]
    exact ⟨(ha.per r ds.1).left ep.1,.refl _,ep.2.1⟩
  have db := hd ρ η ξ r h
  rw [F_motiveAt] at db
  have tr := (hb.transport r el) ▸ db
  have goalrel : F (motiveAt B y e) ρ η (interp d η) (interp d ξ) := by
    rw [F_motiveAt]; exact tr
  exact (ht.per r ds.1).raw (interp_j d y e η).symm (interp_j d y e ξ).symm goalrel

theorem fundamental_pi_ext {Γ A B p q h} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) (hq : Fundamental Γ q (.pi A B))
    (hh : Fundamental Γ h (.pi A (.identity B
      (.app (P01D.pren Nat.succ p) (.var 0))
      (.app (P01D.pren Nat.succ q) (.var 0))))) :
    Fundamental Γ (.atom .i) (.identity (.pi A B) p q) := by
  intro ρ η ξ r e
  have d := (hc.ends r e).1
  have qq := hq ρ η η r (hc.refl r d)
  have hh' := hh ρ η η r (hc.refl r d)
  refine ⟨?_,.refl _,.refl _⟩
  intro x y xy
  have pointwise : F B ρ (cons x η) (interp p η ⬝ x) (interp q η ⬝ x) := by
    simpa only [interp_app,interp_ren,interp_var,cons] using (hh' x y xy).1
  exact (hb.per (η := cons x η) r ⟨d,(ha.per r d).left xy⟩).trans pointwise (qq x y xy)

theorem fundamental_all_ext {Γ B p q h} (hc : ContextLaws Γ)
    (hh : Fundamental (twkTel Γ) h (.identity B p q)) :
    Fundamental Γ (.atom .i) (.identity (.all B) p q) := by
  intro ρ η ξ r e
  refine ⟨?_,.refl _,.refl _⟩
  intro P
  have ee : E (twkTel Γ) (cons P.rel ρ) η η :=
    (E_twk Γ P.rel ρ η η).symm ▸ hc.refl r (hc.ends r e).1
  exact (hh (cons P.rel ρ) η η (admissible_cons r P) ee).1


theorem i_related {R : Rel} (h : Laws R) : Arrow R R .i .i :=
  fun x y xy => h.raw (Conv.i x).symm (Conv.i y).symm xy

theorem k_related {R S : Rel} (h : Laws R) : Arrow R (Arrow S R) .k .k :=
  fun x y xy a b _ => h.raw (Conv.k x a).symm (Conv.k y b).symm xy

theorem s_related {R S U : Rel} (h : Laws U) :
    Arrow (Arrow R (Arrow S U)) (Arrow (Arrow R S) (Arrow R U)) .s .s := by
  intro f f' ff g g' gg a a' aa
  exact h.raw (Conv.s f g a).symm (Conv.s f' g' a').symm (ff a a' aa _ _ (gg a a' aa))

theorem fundamental_i {Γ A} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) :
    Fundamental Γ (.atom .i) (arr A A) := by
  intro ρ η ξ r h
  rw [F_arr]
  exact i_related (ha.per r (hc.ends r h).1)

theorem fundamental_k {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) :
    Fundamental Γ (.atom .k) (arr A (arr B A)) := by
  intro ρ η ξ r h
  simp only [F_arr]
  exact k_related (ha.per r (hc.ends r h).1)

theorem fundamental_s {Γ A B C} (hc : ContextLaws Γ) (hcc : TypeLaws Γ C) :
    Fundamental Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) := by
  intro ρ η ξ r h
  simp only [F_arr]
  exact s_related (hcc.per r (hc.ends r h).1)

open OrthemologyV2 (TypeCode)
open OrthemologyV3 (FiniteDerives)
def C : TypeCode → REnv → Rel
  | .var n, ρ => ρ n
  | .bottom, _ => fun _ _ => False
  | .arrow A B, ρ => Arrow (C A ρ) (C B ρ)
  | .all B, ρ => fun u v => ∀ P : SatPER, C B (cons P.rel ρ) u v

theorem C_laws (A : TypeCode) {ρ : REnv} (r : admissible ρ) : Laws (C A ρ) := by
  induction A generalizing ρ with
  | var n => exact r n
  | bottom => exact ⟨False.elim,fun h _ => h,fun _ _ h => h⟩
  | arrow A B ha hb => exact per_laws (arrowPER (ha r).object (hb r).object)
  | all B hb =>
      exact {
        sym := fun h P => (hb (admissible_cons r P)).sym (h P)
        trans := fun h k P => (hb (admissible_cons r P)).trans (h P) (k P)
        raw := fun ct cu h P => (hb (admissible_cons r P)).raw ct cu (h P) }

theorem F_fin (A : TypeCode) (ρ : REnv) (η : Env) : F (fin A) ρ η = C A ρ := by
  induction A generalizing ρ η with
  | var n | bottom => rfl
  | arrow A B ha hb => simp only [fin,F_arr,ha,hb,C]
  | all B hb => simp only [fin,F,hb,C]

theorem C_rename (A : TypeCode) (r : Nat → Nat) (ρ : REnv) :
    C (OrthemologyV3.rename r A) ρ = C A (fun n => ρ (r n)) := by
  induction A generalizing r ρ with
  | var n | bottom => rfl
  | arrow A B ha hb => simp only [OrthemologyV3.rename,C,ha,hb]
  | all B hb =>
      simp only [OrthemologyV3.rename,C,hb]
      have henv : ∀ P : SatPER, (fun n => cons P.rel ρ (OrthemologyV3.liftRen r n)) = cons P.rel (fun n => ρ (r n)) := by
        intro P; funext n; cases n <;> rfl
      simp only [henv]

theorem C_substitute (A : TypeCode) (σ : Nat → TypeCode) (ρ : REnv) :
    C (OrthemologyV3.substitute σ A) ρ = C A (fun n => C (σ n) ρ) := by
  induction A generalizing σ ρ with
  | var n | bottom => rfl
  | arrow A B ha hb => simp only [OrthemologyV3.substitute,C,ha,hb]
  | all B hb =>
      simp only [OrthemologyV3.substitute,C,hb]
      have henv : ∀ P : SatPER, (fun n => C (OrthemologyV3.upSub σ n) (cons P.rel ρ)) = cons P.rel (fun n => C (σ n) ρ) := by
        intro P; funext n; cases n with
        | zero => rfl
        | succ n => exact C_rename _ _ _
      simp only [henv]

theorem C_instantiate (B A : TypeCode) (ρ : REnv) :
    C (OrthemologyV3.instantiateType B A) ρ = C B (cons (C A ρ) ρ) := by
  rw [OrthemologyV3.instantiateType,C_substitute]
  have henv : (fun n => C (OrthemologyV3.singleSub A n) ρ) = cons (C A ρ) ρ := by
    funext n; cases n <;> rfl
  rw [henv]

/-- A fresh induction on the ACTUAL finite grammar, including impredicative
    elimination. This does not reuse the different source semantic theorem. -/
theorem finite_sound {t A} (h : FiniteDerives t A) (ρ : REnv) (r : admissible ρ) :
    C A ρ (embed t) (embed t) := by
  induction h generalizing ρ with
  | i A => exact i_related (C_laws A r)
  | k A B => exact k_related (C_laws A r)
  | s A B C => exact s_related (C_laws C r)
  | app hf hx ihf ihx => exact ihf ρ r _ _ (ihx ρ r)
  | allI ht ih => exact fun P => ih (cons P.rel ρ) (admissible_cons r P)
  | allE ht A ih =>
      rw [C_instantiate]
      exact ih ρ r (C_laws A r).object
  | reduce ht red ih =>
      have cv := ImportedOpenTermTransport.source_conv_sound (P01Source.red_conv red)
      exact (C_laws _ r).raw cv cv (ih ρ r)

theorem fundamental_finite {Γ C t τ} (hc : ContextLaws Γ)
    (h : ∀ n, n < τ.length → TypeLaws Γ (typeImages τ n)) (ht : FiniteDerives t C) :
    Fundamental Γ (.atom t) (tsubst (typeImages τ) (fin C)) := by
  intro ρ η ξ r e
  rw [F_tsubst,F_fin]
  apply finite_sound ht
  intro n
  by_cases hn : n < τ.length
  · exact (h n hn).per r (hc.ends r e).1
  · change Laws (F (typeImages τ n) ρ η)
    rw [P01AC.typeImages_beyond τ (Nat.le_of_not_gt hn)]
    exact (type_bottom Γ).per r (hc.ends r e).1


open P01AC.ExtensionalRepair (CtxE FormE HasE)

/-- These records are conclusions of the actual mutual derivation induction,
    never added premises in the source grammar. -/
def Hereditary (Γ : Tel) (A : Ty) : Prop := TypeLaws Γ A ∧ match A with
  | .pi A B | .sigma A B => Hereditary Γ A ∧ Hereditary (A :: Γ) B
  | .identity A _ _ => Hereditary Γ A
  | .all B => Hereditary (twkTel Γ) B
  | _ => True
abbrev FormSound (Γ : Tel) (A : Ty) := ContextLaws Γ ∧ Hereditary Γ A
abbrev TermSound (Γ : Tel) (p : Poly) (A : Ty) := FormSound Γ A ∧ Fundamental Γ p A

theorem Hereditary.laws {Γ A} (h : Hereditary Γ A) : TypeLaws Γ A := by cases A <;> exact h.1

/- The mutual recursion follows the actual source recursors. Its rule bodies
    invoke only the NEW unary lemmas established above. -/
theorem form_sound {Γ A} (h : FormE Γ A) : FormSound Γ A := by
  induction h using FormE.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_3 := fun Γ p A _ => TermSound Γ p A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b => exact ⟨c,type_all b.2.laws,b.2⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 c.2.laws⟩
    | finite τ bound hτ hA hf a t => exact ⟨t,fundamental_finite t.1 (fun n hn => (a n hn).2.laws) hf⟩
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro p.2⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,fun _ _ _ _ _ => Conv.refl _⟩
    | rawApp hA hf hx a f x => exact ⟨a,fun ρ η ξ r e => Conv.app (f.2 ρ η ξ r e) (x.2 ρ η ξ r e)⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 b.2⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro ρ η ξ r e
        have dd := a.1.ends r e
        exact (a.2.laws.per r dd.1).raw (ImportedOpenTermTransport.source_plus_sound pq η)
          (ImportedOpenTermTransport.source_plus_sound pq ξ) (p.2 ρ η ξ r e)
    | piExt hA hB hPi hp hq hM hPiM hh hTarget sp sq sh sA sB
        a b pi p q m pim h t =>
        exact ⟨t,fundamental_pi_ext a.1 a.2.laws b.2.laws q.2 h.2⟩
    | allExt hB hAll hp hq hN hh hTarget sp sq sh sB
        b all p q n h t =>
        exact ⟨t,fundamental_all_ext p.1.1 h.2⟩


theorem has_sound {Γ p A} (h : HasE Γ p A) : TermSound Γ p A := by
  induction h using HasE.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_2 := fun Γ A _ => FormSound Γ A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b => exact ⟨c,type_all b.2.laws,b.2⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 c.2.laws⟩
    | finite τ bound hτ hA hf a t => exact ⟨t,fundamental_finite t.1 (fun n hn => (a n hn).2.laws) hf⟩
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro p.2⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,fun _ _ _ _ _ => Conv.refl _⟩
    | rawApp hA hf hx a f x => exact ⟨a,fun ρ η ξ r e => Conv.app (f.2 ρ η ξ r e) (x.2 ρ η ξ r e)⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 b.2⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro ρ η ξ r e
        have dd := a.1.ends r e
        exact (a.2.laws.per r dd.1).raw (ImportedOpenTermTransport.source_plus_sound pq η)
          (ImportedOpenTermTransport.source_plus_sound pq ξ) (p.2 ρ η ξ r e)
    | piExt hA hB hPi hp hq hM hPiM hh hTarget sp sq sh sA sB
        a b pi p q m pim h t =>
        exact ⟨t,fundamental_pi_ext a.1 a.2.laws b.2.laws q.2 h.2⟩
    | allExt hB hAll hp hq hN hh hTarget sp sq sh sB
        b all p q n h t =>
        exact ⟨t,fundamental_all_ext p.1.1 h.2⟩



theorem context_sound {Γ} (h : CtxE Γ) : ContextLaws Γ := (form_sound (.raw h)).1

theorem fundamental {Γ p A} (h : HasE Γ p A) : Fundamental Γ p A := (has_sound h).2

theorem formation_per {Γ A} (h : FormE Γ A) {ρ η} (r : admissible ρ) (d : D Γ ρ η) :
    Laws (F A ρ η) := (form_sound h).2.laws.per r d

theorem formation_coherent {Γ A} (h : FormE Γ A) {ρ η ξ} (r : admissible ρ) (e : E Γ ρ η ξ) :
    F A ρ η = F A ρ ξ := (form_sound h).2.laws.transport r e

#print axioms F_mixed
#print axioms finite_sound
#print axioms fundamental_j
#print axioms form_sound
#print axioms has_sound
#print axioms fundamental
#print axioms formation_coherent

end TaggedPER
