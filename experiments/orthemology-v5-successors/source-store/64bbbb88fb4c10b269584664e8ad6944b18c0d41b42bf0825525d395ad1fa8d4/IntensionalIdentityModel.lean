/- Fresh Conv-saturated unary interpretation of the unchanged P01AC syntax.
   Sat is transparently the inherited step-stable Code, with its precise
   equivalence to Conv-saturated predicates proved below. -/
import AllPredicates
namespace P01AC.Intensional
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

abbrev Sat := Code
abbrev SEnv := Nat → Sat

def Saturated (P : Term → Prop) : Prop :=
  ∀ {t u}, Conv t u → (P t ↔ P u)

def ofSaturated (P : Term → Prop) (h : Saturated P) : Sat :=
  ⟨P, fun s => h (.step s)⟩

theorem sat_saturated (X : Sat) : Saturated X.accepts :=
  fun h => code_conversion X h

theorem saturated_iff_code (P : Term → Prop) :
    Saturated P ↔ ∃ X : Sat, X.accepts = P := by
  constructor
  · intro h; exact ⟨ofSaturated P h, rfl⟩
  · rintro ⟨X, rfl⟩; exact sat_saturated X

theorem code_ext {A B : Code} (h : ∀ t, A.accepts t ↔ B.accepts t) : A = B := by
  cases A with
  | mk a ha =>
    cases B with
    | mk b hb =>
      have e : a = b := funext (fun t => propext (h t))
      cases e
      rfl

def piCode (A : Sat) (B : Term → Sat) : Sat where
  accepts f := ∀ a, A.accepts a → (B a).accepts (.app f a)
  stable h := ⟨fun hf a ha => ((B a).stable (.left h a)).mp (hf a ha),
    fun hg a ha => ((B a).stable (.left h a)).mpr (hg a ha)⟩

def sigmaCode (A : Sat) (B : Term → Sat) : Sat where
  accepts z := ∃ a b, A.accepts a ∧ (B a).accepts b ∧ Conv z (pairTerm a b)
  stable h := ⟨fun ⟨a,b,ha,hb,hz⟩ => ⟨a,b,ha,hb,.trans (.symm (.step h)) hz⟩,
    fun ⟨a,b,ha,hb,hz⟩ => ⟨a,b,ha,hb,.trans (.step h) hz⟩⟩

def identityCode (A : Sat) (p q : Term) : Sat where
  accepts e := A.accepts p ∧ A.accepts q ∧ Conv p q ∧ Conv e .i
  stable h := ⟨fun ⟨hp,hq,pq,he⟩ => ⟨hp,hq,pq,.trans (.symm (.step h)) he⟩,
    fun ⟨hp,hq,pq,he⟩ => ⟨hp,hq,pq,.trans (.step h) he⟩⟩

def interp : Ty → SEnv → Env → Sat
  | .param n, ρ, _ => ρ n
  | .bottom, _, _ => Code.bottom
  | .raw, _, _ => Code.top
  | .pi A B, ρ, η => piCode (interp A ρ η) (fun a => interp B ρ (cons a η))
  | .sigma A B, ρ, η => sigmaCode (interp A ρ η) (fun a => interp B ρ (cons a η))
  | .identity A p q, ρ, η => identityCode (interp A ρ η) (eval p η) (eval q η)
  | .all B, ρ, η => Code.all (fun X => interp B (cons X ρ) η)

abbrev mem (A : Ty) (ρ : SEnv) (η : Env) (t : Term) : Prop := (interp A ρ η).accepts t

theorem interp_saturated (A : Ty) (ρ : SEnv) (η : Env) :
    Saturated (mem A ρ η) := sat_saturated _

def EnvConv (η ξ : Env) : Prop := ∀ n, Conv (η n) (ξ n)

theorem envConv_cons {η ξ : Env} (h : EnvConv η ξ) {a b} (ab : Conv a b) :
    EnvConv (cons a η) (cons b ξ) := by
  intro n; cases n with
  | zero => exact ab
  | succ n => exact h n

theorem eval_coherent (p : Poly) {η ξ : Env} (h : EnvConv η ξ) :
    Conv (eval p η) (eval p ξ) := by
  induction p with
  | var n => exact h n
  | atom t => exact .refl _
  | app f a hf ha => exact conv_app hf ha

theorem interp_coherent (A : Ty) (ρ : SEnv) (η ξ : Env) (h : EnvConv η ξ) :
    interp A ρ η = interp A ρ ξ := by
  induction A generalizing ρ η ξ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb =>
    simp only [interp]
    rw [ha ρ η ξ h]
    congr 1
    funext a
    exact hb ρ _ _ (envConv_cons h (.refl a))
  | sigma A B ha hb =>
    simp only [interp]
    rw [ha ρ η ξ h]
    congr 1
    funext a
    exact hb ρ _ _ (envConv_cons h (.refl a))
  | all B hb =>
    simp only [interp]
    congr 1
    funext X
    exact hb (cons X ρ) η ξ h
  | identity A p q ha =>
    simp only [interp]
    rw [ha ρ η ξ h]
    apply code_ext
    intro e
    have hp := eval_coherent p h
    have hq := eval_coherent q h
    change (_ ∧ _ ∧ _ ∧ _) ↔ (_ ∧ _ ∧ _ ∧ _)
    constructor
    · rintro ⟨ap,aq,pq,he⟩
      exact ⟨(code_conversion _ hp).mp ap, (code_conversion _ hq).mp aq,
        .trans (.symm hp) (.trans pq hq), he⟩
    · rintro ⟨ap,aq,pq,he⟩
      exact ⟨(code_conversion _ hp).mpr ap, (code_conversion _ hq).mpr aq,
        .trans hp (.trans pq (.symm hq)), he⟩

theorem eval_pup (σ : Nat → Poly) (η : Env) (a : Term) :
    (fun n => eval (pup σ n) (cons a η)) = cons a (fun n => eval (σ n) η) := by
  funext n
  cases n <;> simp only [pup, eval_ren, eval, cons]

theorem interp_subst (A : Ty) (σ : Nat → Poly) (ρ : SEnv) (η : Env) :
    interp (subst σ A) ρ η = interp A ρ (fun n => eval (σ n) η) := by
  induction A generalizing σ ρ η with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb =>
    simp only [subst, interp, ha]
    congr 1
    funext a
    rw [hb, eval_pup]
  | sigma A B ha hb =>
    simp only [subst, interp, ha]
    congr 1
    funext a
    rw [hb, eval_pup]
  | identity A p q ha => simp only [subst, interp, ha, eval_sub]
  | all B hb =>
    simp only [subst, interp]
    congr 1
    funext X
    exact hb σ (cons X ρ) η

theorem interp_wk (A : Ty) (ρ : SEnv) (η : Env) (a : Term) :
    interp (wk A) ρ (cons a η) = interp A ρ η := by
  unfold wk
  rw [interp_subst]
  rfl

theorem interp_inst (B : Ty) (a : Poly) (ρ : SEnv) (η : Env) :
    interp (inst B a) ρ η = interp B ρ (cons (eval a η) η) := by
  unfold inst
  rw [interp_subst]
  congr 1
  funext n; cases n <;> rfl

theorem interp_motiveAt (B : Ty) (y e : Poly) (ρ : SEnv) (η : Env) :
    interp (motiveAt B y e) ρ η = interp B ρ (cons (eval e η) (cons (eval y η) η)) := by
  unfold motiveAt
  rw [interp_subst]
  congr 1
  funext n; cases n with
  | zero => rfl
  | succ n => cases n <;> rfl

theorem interp_arr (A B : Ty) (ρ : SEnv) (η : Env) :
    interp (arr A B) ρ η = Code.arrow (interp A ρ η) (interp B ρ η) := by
  apply code_ext
  intro t
  change (∀ a, _ → _) ↔ (∀ a, _ → _)
  simp only [interp_wk]

theorem interp_trename (A : Ty) (r : Nat → Nat) (ρ : SEnv) (η : Env) :
    interp (trename r A) ρ η = interp A (fun n => ρ (r n)) η := by
  induction A generalizing r ρ η with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb => simp only [trename, interp, ha, hb]
  | sigma A B ha hb => simp only [trename, interp, ha, hb]
  | identity A p q ha => simp only [trename, interp, ha]
  | all B hb =>
    simp only [trename, interp]
    congr 1
    funext X
    rw [hb]
    congr 1
    funext n; cases n <;> rfl

theorem interp_twk (A : Ty) (ρ : SEnv) (η : Env) (X : Sat) :
    interp (twk A) (cons X ρ) η = interp A ρ η := by
  unfold twk
  rw [interp_trename]
  rfl

/-- The replacement type interpretations are frozen at the original outer η.
    Term and type binder lifting is exactly the source mixed operation. -/
theorem interp_mixed (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) (ρ : SEnv) (η : Env) :
    interp (mixed σ τ A) ρ η =
      interp A (fun n => interp (τ n) ρ η) (fun n => eval (σ n) η) := by
  induction A generalizing σ τ ρ η with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | pi A B ha hb =>
    simp only [mixed, interp, ha]
    congr 1
    funext a
    rw [hb, eval_pup]
    simp only [interp_wk]
  | sigma A B ha hb =>
    simp only [mixed, interp, ha]
    congr 1
    funext a
    rw [hb, eval_pup]
    simp only [interp_wk]
  | identity A p q ha => simp only [mixed, interp, ha, eval_sub]
  | all B hb =>
    simp only [mixed, interp]
    congr 1
    funext X
    rw [hb]
    congr 1
    funext n
    cases n with
    | zero => rfl
    | succ n => exact interp_twk (τ n) ρ η X

theorem interp_tsubst (A : Ty) (τ : Nat → Ty) (ρ : SEnv) (η : Env) :
    interp (tsubst τ A) ρ η = interp A (fun n => interp (τ n) ρ η) η := by
  exact interp_mixed A Poly.var τ ρ η

theorem interp_tinst (B A : Ty) (ρ : SEnv) (η : Env) :
    interp (tinst B A) ρ η = interp B (cons (interp A ρ η) ρ) η := by
  unfold tinst
  rw [interp_tsubst]
  congr 1
  funext n; cases n <;> rfl

theorem interp_fin (C : TypeCode) (ρ : SEnv) (η : Env) :
    interp (fin C) ρ η = OrthemologyV2.interpret C ρ := by
  induction C generalizing ρ η with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [fin, interp_arr, ha, hb, OrthemologyV2.interpret]
  | all B hb =>
    simp only [fin, interp, OrthemologyV2.interpret]
    congr 1
    funext X
    exact hb (cons X ρ) η

/-- The finite fragment is checked over every one of its seven actual rules.
    This uses the inherited finite type substitution theorem for allE. -/
theorem finite_code_sound {t C} (h : FiniteDerives t C) (ρ : SEnv) :
    (OrthemologyV2.interpret C ρ).accepts t := by
  induction h generalizing ρ with
  | i A => exact i_realises _
  | k A B => exact k_realises _ _
  | s A B C => exact s_realises _ _ _
  | app hf hx ihf ihx => exact ihf ρ _ (ihx ρ)
  | allI h ih => exact fun X => ih (extend X ρ)
  | allE h A ih =>
    rw [instantiate_sem]
    exact ih ρ (OrthemologyV2.interpret A ρ)
  | reduce h red ih => exact (Code.along _ red).mp (ih ρ)

/-- Exact finite import; every image, including Bottom-default images, is
    interpreted at the frozen outer environment. FiniteDerives is unchanged. -/
theorem finite_mem {t C} (h : FiniteDerives t C) (τ : List Ty) (ρ : SEnv) (η : Env) :
    mem (tsubst (typeImages τ) (fin C)) ρ η t := by
  unfold mem
  rw [interp_tsubst, interp_fin]
  exact finite_code_sound h _

/-- The fresh relation refines raw conversion uniformly, even at Pi and All. -/
def R (A : Ty) (ρ : SEnv) (η : Env) (t u : Term) : Prop :=
  mem A ρ η t ∧ mem A ρ η u ∧ Conv t u

theorem R_refines {A ρ η t u} (h : R A ρ η t u) : Conv t u := h.2.2

theorem R_symm {A ρ η t u} (h : R A ρ η t u) : R A ρ η u t :=
  ⟨h.2.1, h.1, .symm h.2.2⟩

theorem R_trans {A ρ η t u v} (h : R A ρ η t u) (k : R A ρ η u v) :
    R A ρ η t v := ⟨h.1, k.2.1, .trans h.2.2 k.2.2⟩

theorem R_domain {A ρ η t} : R A ρ η t t ↔ mem A ρ η t :=
  ⟨fun h => h.1, fun h => ⟨h,h,.refl _⟩⟩

theorem R_saturated {A ρ η t t' u u'} (ht : Conv t t') (hu : Conv u u') :
    R A ρ η t u ↔ R A ρ η t' u' := by
  constructor
  · intro h
    exact ⟨(code_conversion _ ht).mp h.1, (code_conversion _ hu).mp h.2.1,
      .trans (.symm ht) (.trans h.2.2 hu)⟩
  · intro h
    exact ⟨(code_conversion _ ht).mpr h.1, (code_conversion _ hu).mpr h.2.1,
      .trans ht (.trans h.2.2 (.symm hu))⟩

theorem R_coherent {A ρ η ξ t u} (h : EnvConv η ξ) :
    R A ρ η t u ↔ R A ρ ξ t u := by
  unfold R mem
  rw [interp_coherent A ρ η ξ h]

end P01AC.Intensional
