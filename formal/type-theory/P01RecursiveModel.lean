/- New recursive U10 finite interpretation. The heterogeneous environment
   explicitly bundles both object endpoints and its respectful relations.
   No canonical Conv or checkpoint definition is changed. -/
import P01Examples
namespace P01R
open OrthemologyV2 OrthemologyV3 P01D
open P01F (cons)

abbrev OEnv := Nat → PER

structure REnv where
  left : OEnv
  right : OEnv
  rel : Nat → Term → Term → Prop
  endpoints : ∀ n {t u}, rel n t u → (left n).dom t ∧ (right n).dom u
  respect : ∀ n {t t' u u'}, (left n).rel t t' → (right n).rel u u' →
    rel n t u → rel n t' u'

@[ext] theorem renv_ext {r s : REnv}
    (hl : r.left = s.left) (hr : r.right = s.right) (hp : r.rel = s.rel) : r = s := by
  cases r; cases s; cases hl; cases hr; cases hp; rfl

def diagEnv (ρ : OEnv) : REnv where
  left := ρ
  right := ρ
  rel := fun n => (ρ n).rel
  endpoints := by intro n t u h; exact ⟨PER.left h,PER.right h⟩
  respect := by intro n t t' u u' ht hu h; exact (ρ n).trans ((ρ n).sym ht) ((ρ n).trans h hu)

def REnv.at (r : REnv) (n : Nat) : Link (r.left n) (r.right n) where
  rel := r.rel n
  endpoints := r.endpoints n
  respect := r.respect n

def extendEnv {P Q : PER} (R : Link P Q) (r : REnv) : REnv where
  left := cons P r.left
  right := cons Q r.right
  rel := cons R.rel r.rel
  endpoints := by
    intro n t u h
    cases n with
    | zero => exact R.endpoints h
    | succ n => exact r.endpoints n h
  respect := by
    intro n t t' u u' ht hu h
    cases n with
    | zero => exact R.respect ht hu h
    | succ n => exact r.respect n ht hu h

theorem extend_diag (ρ : OEnv) (P : PER) :
    extendEnv (diagonal P) (diagEnv ρ) = diagEnv (cons P ρ) := by
  apply renv_ext
  · rfl
  · rfl
  · funext n
    cases n <;> rfl

@[ext] theorem link_ext {P Q : PER} {R S : Link P Q}
    (h : ∀ t u, R.rel t u ↔ S.rel t u) : R = S := by
  have e : R.rel = S.rel := funext fun t => funext fun u => propext (h t u)
  cases R; cases S; cases e; rfl

structure Model where
  obj : OEnv → PER
  rel : REnv → Term → Term → Prop
  endpoints : ∀ r {t u}, rel r t u → (obj r.left).dom t ∧ (obj r.right).dom u
  respect : ∀ r {t t' u u'}, (obj r.left).rel t t' → (obj r.right).rel u u' →
    rel r t u → rel r t' u'
  identity : ∀ ρ t u, rel (diagEnv ρ) t u ↔ (obj ρ).rel t u

def Model.asLink (M : Model) (r : REnv) : Link (M.obj r.left) (M.obj r.right) where
  rel := M.rel r
  endpoints := M.endpoints r
  respect := M.respect r

theorem Model.asLink_diag (M : Model) (ρ : OEnv) :
    M.asLink (diagEnv ρ) = diagonal (M.obj ρ) := link_ext (M.identity ρ)

@[ext] theorem model_ext {M N : Model}
    (ho : ∀ρ, M.obj ρ = N.obj ρ)
    (hr : ∀ r t u, M.rel r t u ↔ N.rel r t u) : M = N := by
  have eo : M.obj = N.obj := funext ho
  have er : M.rel = N.rel := funext fun r => funext fun t => funext fun u => propext (hr r t u)
  cases M; cases N; cases eo; cases er; rfl

def varModel (n : Nat) : Model where
  obj := fun ρ => ρ n
  rel := fun r => r.rel n
  endpoints := fun r => r.endpoints n
  respect := fun r => r.respect n
  identity := fun _ _ _ => Iff.rfl

def bottomModel : Model where
  obj := fun _ => botPER
  rel := fun _ _ _ => False
  endpoints := by intro r t u h; exact False.elim h
  respect := by intro r t t' u u' ht hu h; exact h
  identity := fun _ _ _ => Iff.rfl

def arrowModel (A B : Model) : Model where
  obj := fun ρ => ArrPER (A.obj ρ) (B.obj ρ)
  rel := fun r => (arrowLink (A.asLink r) (B.asLink r)).rel
  endpoints := fun r => (arrowLink (A.asLink r) (B.asLink r)).endpoints
  respect := fun r => (arrowLink (A.asLink r) (B.asLink r)).respect
  identity := by
    intro ρ t u
    rw [A.asLink_diag, B.asLink_diag]
    exact arrow_identity (A.obj ρ) (B.obj ρ) t u

def bodyFamily (B : Model) (ρ : OEnv) : ParamFamily where
  obj := fun P => B.obj (cons P ρ)
  link := fun R => B.asLink (extendEnv R (diagEnv ρ))
  identity := by
    intro P t u
    change B.rel (extendEnv (diagonal P) (diagEnv ρ)) t u ↔ _
    rw [extend_diag]
    exact B.identity (cons P ρ) t u

def allModel (B : Model) : Model where
  obj := fun ρ => AllPER (bodyFamily B ρ)
  rel := fun r t u =>
    (AllPER (bodyFamily B r.left)).dom t ∧ (AllPER (bodyFamily B r.right)).dom u ∧
    ∀ (P Q : PER) (R : Link P Q), B.rel (extendEnv R r) t u
  endpoints := by intro r t u h; exact ⟨h.1,h.2.1⟩
  respect := by
    intro r t t' u u' ht hu h
    refine ⟨PER.right ht, PER.right hu, ?_⟩
    intro P Q R
    exact B.respect (extendEnv R r) (ht.2.2 P) (hu.2.2 Q) (h.2.2 P Q R)
  identity := fun ρ t u => all_identity_extension (bodyFamily B ρ) t u

def interpret : TypeCode → Model
  | .var n => varModel n
  | .bottom => bottomModel
  | .arrow A B => arrowModel (interpret A) (interpret B)
  | .all B => allModel (interpret B)

theorem recursive_identity_extension (A : TypeCode) (ρ : OEnv) (t u : Term) :
    (interpret A).rel (diagEnv ρ) t u ↔ ((interpret A).obj ρ).rel t u :=
  (interpret A).identity ρ t u

theorem recursive_endpoint_restriction (A : TypeCode) (r : REnv) {t u}
    (h : (interpret A).rel r t u) :
    ((interpret A).obj r.left).dom t ∧ ((interpret A).obj r.right).dom u :=
  (interpret A).endpoints r h

theorem recursive_respectfulness (A : TypeCode) (r : REnv) {t t' u u'}
    (ht : ((interpret A).obj r.left).rel t t') (hu : ((interpret A).obj r.right).rel u u')
    (h : (interpret A).rel r t u) : (interpret A).rel r t' u' :=
  (interpret A).respect r ht hu h

theorem recursive_raw_compatibility (A : TypeCode) (r : REnv) {t t' u u'}
    (ct : Conv t t') (cu : Conv u u') (h : (interpret A).rel r t u) :
    (interpret A).rel r t' u' := (interpret A).asLink r |>.raw ct cu h

def renEnv (r : Nat → Nat) (ρ : OEnv) : OEnv := fun n => ρ (r n)

def REnv.rename (r : REnv) (s : Nat → Nat) : REnv where
  left := renEnv s r.left
  right := renEnv s r.right
  rel := fun n => r.rel (s n)
  endpoints := fun n => r.endpoints (s n)
  respect := fun n => r.respect (s n)

def Model.rename (M : Model) (s : Nat → Nat) : Model where
  obj := fun ρ => M.obj (renEnv s ρ)
  rel := fun r => M.rel (r.rename s)
  endpoints := fun r => M.endpoints (r.rename s)
  respect := fun r => M.respect (r.rename s)
  identity := fun ρ => M.identity (renEnv s ρ)

theorem renEnv_cons (s : Nat → Nat) (ρ : OEnv) (P : PER) :
    renEnv (liftRen s) (cons P ρ) = cons P (renEnv s ρ) := by
  funext n
  cases n <;> rfl

theorem rename_extend (s : Nat → Nat) (r : REnv) {P Q} (R : Link P Q) :
    (extendEnv R r).rename (liftRen s) = extendEnv R (r.rename s) := by
  apply renv_ext (renEnv_cons s r.left P) (renEnv_cons s r.right Q)
  funext n
  cases n <;> rfl

theorem rename_diag (s : Nat → Nat) (ρ : OEnv) :
    (diagEnv ρ).rename s = diagEnv (renEnv s ρ) := rfl


theorem rename_all (M : Model) (s : Nat → Nat) :
    allModel (M.rename (liftRen s)) = (allModel M).rename s := by
  apply model_ext
  · intro ρ
    apply per_ext
    intro t u
    simp only [allModel, Model.rename, AllPER, Parametric, bodyFamily, Model.asLink,
      rename_extend, rename_diag, renEnv_cons]
  · intro r t u
    simp only [allModel, Model.rename, AllPER, PER.dom, Parametric, bodyFamily, Model.asLink,
      rename_extend, rename_diag, renEnv_cons]
    rfl

theorem interpret_rename (A : TypeCode) (s : Nat → Nat) :
    interpret (rename s A) = (interpret A).rename s := by
  induction A generalizing s with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb =>
      simp only [rename, interpret, ha, hb]
      rfl
  | all B ih =>
      simp only [rename, interpret, ih]
      exact rename_all (interpret B) s


def subEnv (s : Nat → Model) (ρ : OEnv) : OEnv := fun n => (s n).obj ρ

def REnv.substitute (r : REnv) (s : Nat → Model) : REnv where
  left := subEnv s r.left
  right := subEnv s r.right
  rel := fun n => (s n).rel r
  endpoints := fun n => (s n).endpoints r
  respect := fun n => (s n).respect r

theorem substitute_diag (s : Nat → Model) (ρ : OEnv) :
    (diagEnv ρ).substitute s = diagEnv (subEnv s ρ) := by
  apply renv_ext
  · rfl
  · rfl
  · funext n t u
    exact propext ((s n).identity ρ t u)

def Model.substitute (M : Model) (s : Nat → Model) : Model where
  obj := fun ρ => M.obj (subEnv s ρ)
  rel := fun r => M.rel (r.substitute s)
  endpoints := fun r => M.endpoints (r.substitute s)
  respect := fun r => M.respect (r.substitute s)
  identity := by
    intro ρ t u
    rw [substitute_diag]
    exact M.identity (subEnv s ρ) t u

def liftModels (s : Nat → Model) : Nat → Model
  | 0 => varModel 0
  | n+1 => (s n).rename Nat.succ

theorem subEnv_cons (s : Nat → Model) (ρ : OEnv) (P : PER) :
    subEnv (liftModels s) (cons P ρ) = cons P (subEnv s ρ) := by
  funext n
  cases n <;> rfl

theorem rename_succ_extend (r : REnv) {P Q} (R : Link P Q) :
    (extendEnv R r).rename Nat.succ = r := rfl

theorem substitute_extend (s : Nat → Model) (r : REnv) {P Q} (R : Link P Q) :
    (extendEnv R r).substitute (liftModels s) = extendEnv R (r.substitute s) := by
  apply renv_ext (subEnv_cons s r.left P) (subEnv_cons s r.right Q)
  funext n
  cases n <;> rfl

theorem substitute_all (M : Model) (s : Nat → Model) :
    allModel (M.substitute (liftModels s)) = (allModel M).substitute s := by
  apply model_ext
  · intro ρ
    apply per_ext
    intro t u
    simp only [allModel, Model.substitute, AllPER, Parametric, bodyFamily, Model.asLink,
      substitute_extend, substitute_diag, subEnv_cons]
  · intro r t u
    simp only [allModel, Model.substitute, AllPER, PER.dom, Parametric, bodyFamily, Model.asLink,
      substitute_extend, substitute_diag, subEnv_cons]
    rfl

theorem interpret_lift (s : Nat → TypeCode) :
    (fun n => interpret (upSub s n)) = liftModels (fun n => interpret (s n)) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact interpret_rename (s n) Nat.succ

theorem interpret_substitute (A : TypeCode) (s : Nat → TypeCode) :
    interpret (substitute s A) = (interpret A).substitute (fun n => interpret (s n)) := by
  induction A generalizing s with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb =>
      simp only [substitute, interpret, ha, hb]
      rfl
  | all B ih =>
      simp only [substitute, interpret, ih, interpret_lift]
      exact substitute_all (interpret B) (fun n => interpret (s n))

theorem interpret_single (A : TypeCode) :
    (fun n => interpret (singleSub A n)) = cons (interpret A) varModel := by
  funext n
  cases n <;> rfl

theorem single_obj_environment (M : Model) (ρ : OEnv) :
    subEnv (cons M varModel) ρ = cons (M.obj ρ) ρ := by
  funext n
  cases n <;> rfl

theorem single_rel_environment (M : Model) (r : REnv) :
    r.substitute (cons M varModel) = extendEnv (M.asLink r) r := by
  apply renv_ext (single_obj_environment M r.left) (single_obj_environment M r.right)
  funext n
  cases n <;> rfl

theorem instantiate_obj (B A : TypeCode) (ρ : OEnv) :
    (interpret (instantiateType B A)).obj ρ =
      (interpret B).obj (cons ((interpret A).obj ρ) ρ) := by
  simp only [instantiateType, interpret_substitute, interpret_single,
    Model.substitute, single_obj_environment]

theorem instantiate_rel (B A : TypeCode) (r : REnv) (t u : Term) :
    (interpret (instantiateType B A)).rel r t u ↔
      (interpret B).rel (extendEnv ((interpret A).asLink r) r) t u := by
  simp only [instantiateType, interpret_substitute, interpret_single,
    Model.substitute, single_rel_environment]


theorem k_per (P Q : PER) : (ArrPER P (ArrPER Q P)).dom .k := by
  intro x x' hx y y' hy
  exact P.raw (.symm (.step (.k x y))) (.symm (.step (.k x' y'))) hx

theorem k_link {P P' Q Q' : PER} (R : Link P P') (S : Link Q Q') :
    (arrowLink R (arrowLink S R)).rel .k .k := by
  refine ⟨k_per P Q, k_per P' Q', ?_⟩
  intro x x' hx
  refine ⟨k_per P Q x x (R.endpoints hx).1,
    k_per P' Q' x' x' (R.endpoints hx).2, ?_⟩
  intro y y' hy
  exact R.raw (.symm (.step (.k x y))) (.symm (.step (.k x' y'))) hx

theorem s_per (P Q R : PER) :
    (ArrPER (ArrPER P (ArrPER Q R)) (ArrPER (ArrPER P Q) (ArrPER P R))).dom .s := by
  intro f f' hf g g' hg x x' hx
  exact R.raw (.symm (.step (.s f g x))) (.symm (.step (.s f' g' x')))
    (hf x x' hx (.app g x) (.app g' x') (hg x x' hx))

theorem s_link {P P' Q Q' R R' : PER}
    (Ra : Link P P') (Rb : Link Q Q') (Rc : Link R R') :
    (arrowLink (arrowLink Ra (arrowLink Rb Rc))
      (arrowLink (arrowLink Ra Rb) (arrowLink Ra Rc))).rel .s .s := by
  refine ⟨s_per P Q R, s_per P' Q' R', ?_⟩
  intro f f' hf
  refine ⟨s_per P Q R f f hf.1, s_per P' Q' R' f' f' hf.2.1, ?_⟩
  intro g g' hg
  refine ⟨s_per P Q R f f hf.1 g g hg.1,
    s_per P' Q' R' f' f' hf.2.1 g' g' hg.2.1, ?_⟩
  intro x x' hx
  exact Rc.raw (.symm (.step (.s f g x))) (.symm (.step (.s f' g' x')))
    ((hf.2.2 x x' hx).2.2 (.app g x) (.app g' x') (hg.2.2 x x' hx))

/-- Full relational fundamental theorem for all seven rules of the actual
    unchanged closed FiniteDerives calculus. All uniformity is derived by the
    induction hypothesis at explicit endpoint/relation extensions. -/
theorem finite_fundamental {t A} (h : FiniteDerives t A) :
    ∀ r : REnv, (interpret A).rel r t t := by
  induction h with
  | i A =>
      intro r
      exact identity_link ((interpret A).asLink r)
  | k A B =>
      intro r
      exact k_link ((interpret A).asLink r) ((interpret B).asLink r)
  | s A B C =>
      intro r
      exact s_link ((interpret A).asLink r) ((interpret B).asLink r) ((interpret C).asLink r)
  | app hf hx ihf ihx =>
      intro r
      exact (ihf r).2.2 _ _ (ihx r)
  | allI h ih =>
      intro r
      refine ⟨?_, ?_, ?_⟩
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.left))
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.right))
      · intro P Q R
        exact ih (extendEnv R r)
  | @allE t B h A ih =>
      intro r
      apply (instantiate_rel B A r t t).mpr
      exact (ih r).2.2 ((interpret A).obj r.left) ((interpret A).obj r.right)
        ((interpret A).asLink r)
  | reduce h red ih =>
      intro r
      exact recursive_raw_compatibility _ r (P01Source.red_conv red)
        (P01Source.red_conv red) (ih r)

theorem finite_new_model_member {t A} (h : FiniteDerives t A) (ρ : OEnv) :
    ((interpret A).obj ρ).dom t :=
  ((interpret A).identity ρ t t).mp (finite_fundamental h (diagEnv ρ))

/-- The interpreted All object is a legitimate internal PER argument. This does
    not reify the universe of PERs or all ambient sections as a raw term. -/
theorem recursive_all_self_instance {t B} (h : FiniteDerives t (.all B)) (ρ : OEnv) :
    ((interpret B).obj (cons ((interpret (.all B)).obj ρ) ρ)).dom t :=
  all_self_eliminate (finite_new_model_member h ρ)

end P01R
