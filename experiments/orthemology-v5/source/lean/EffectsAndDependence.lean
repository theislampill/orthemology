/-
Finite effect typing, positive support soundness, and coherent dependent codes.
STATUS: authored source, NOT kernel-verified here. Probability MASS and Kakutani
are proved in the mathematical document, not asserted as axioms in this file.
-/
import BoundaryResults

namespace OrthemologyV3
open OrthemologyV2

structure Weight where
  num : Nat
  den : Nat
  positiveDen : 0 < den
  bounded : num ≤ den

inductive MExpr where
  | pure : Term → MExpr
  | mix : Weight → MExpr → MExpr → MExpr
  | app : MExpr → MExpr → MExpr

/-- Positive-probability support. Zero-weight branches contribute no outcomes.
Separate app subtrees are sampled independently in the quantitative semantics. -/
inductive Outcome : MExpr → Term → Prop where
  | pure (t) : Outcome (.pure t) t
  | mixL {p l r t} : 0 < p.num → Outcome l t → Outcome (.mix p l r) t
  | mixR {p l r t} : p.num < p.den → Outcome r t → Outcome (.mix p l r) t
  | app {f x g y} : Outcome f g → Outcome x y → Outcome (.app f x) (.app g y)

inductive EffectDerives : MExpr → TypeCode → Prop where
  | pure {t A} : FiniteDerives t A → EffectDerives (.pure t) A
  | mix {l r A} : EffectDerives l A → EffectDerives r A → (p : Weight) →
      EffectDerives (.mix p l r) A
  | app {f x A B} : EffectDerives f (.arrow A B) → EffectDerives x A →
      EffectDerives (.app f x) B
  | allI {e B} : EffectDerives e B → EffectDerives e (.all B)
  | allE {e B} : EffectDerives e (.all B) → (A : TypeCode) →
      EffectDerives e (instantiateType B A)

theorem effect_sound {e A} (h : EffectDerives e A) :
    ∀ ρ t, Outcome e t → (interpret A ρ).accepts t := by
  induction h with
  | pure h =>
      intro ρ t ho
      cases ho
      exact finite_sound h ρ
  | mix hl hr p ihl ihr =>
      intro ρ t ho
      cases ho with
      | mixL _ h => exact ihl ρ t h
      | mixR _ h => exact ihr ρ t h
  | app hf hx ihf ihx =>
      intro ρ t ho
      cases ho with
      | app hg hy => exact ihf ρ _ hg _ (ihx ρ _ hy)
  | allI h ih =>
      intro ρ t ho X
      exact ih (extend X ρ) t ho
  | allE h A ih =>
      intro ρ t ho
      rw [instantiate_sem]
      exact ih ρ t ho (interpret A ρ)

theorem outcome_exists (e : MExpr) : ∃ t, Outcome e t := by
  induction e with
  | pure t => exact ⟨t, .pure t⟩
  | mix p l r ihl ihr =>
      by_cases h : 0 < p.num
      · obtain ⟨t,ht⟩ := ihl
        exact ⟨t,.mixL h ht⟩
      · have hz : p.num = 0 := Nat.eq_zero_of_not_pos h
        have hr : p.num < p.den := by simpa only [hz] using p.positiveDen
        obtain ⟨t,ht⟩ := ihr
        exact ⟨t,.mixR hr ht⟩
  | app f x ihf ihx =>
      obtain ⟨g,hg⟩ := ihf
      obtain ⟨y,hy⟩ := ihx
      exact ⟨.app g y,.app hg hy⟩

theorem no_empty_effect {e} (h : EffectDerives e .bottom) : False := by
  obtain ⟨t,ht⟩ := outcome_exists e
  exact effect_sound h (fun _ => Code.top) t ht

theorem effect_outcomes_free {e A} (h : EffectDerives e A) :
    ∀ t, Outcome e t → MarkerFree t := by
  induction h with
  | pure h =>
      intro t ho
      cases ho
      exact derives_markerFree (finite_translation h (fun _ => Code.top))
  | mix hl hr p ihl ihr =>
      intro t ho
      cases ho with
      | mixL _ h => exact ihl t h
      | mixR _ h => exact ihr t h
  | app hf hx ihf ihx =>
      intro t ho
      cases ho with
      | app hg hy => exact ⟨ihf _ hg,ihx _ hy⟩
  | allI h ih => exact ih
  | allE h A ih => exact ih

theorem probabilistic_boolean_projection {e t}
    (h : EffectDerives e booleanCode) (ho : Outcome e t) :
    (∀ x y, Conv (.app (.app t x) y) x) ∨
    (∀ x y, Conv (.app (.app t x) y) y) :=
  boolean_projection (effect_outcomes_free h t ho)
    (effect_sound h (fun _ => Code.top) t ho)

/-- Actual support/intersection commutation; no finite quantifier restriction. -/
theorem support_all_iff (support : Term → Prop) (B : Code → Code) :
    (∀ t, support t → (Code.all B).accepts t) ↔
    (∀ A t, support t → (B A).accepts t) :=
  ⟨fun h A t ht => h t ht A,fun h t ht A => h A t ht⟩

/- Coherent dependent products and sums. These are semantic constructors, not a
claim of a complete syntactic dependent type theory or decidable conversion. -/
structure CoherentFamily where
  fibre : Term → Code
  coherent : ∀ {x y}, Conv x y → ∀ t,
    (fibre x).accepts t ↔ (fibre y).accepts t

def dependentPi (A : Code) (B : CoherentFamily) : Code where
  accepts := fun f => ∀ x, A.accepts x → (B.fibre x).accepts (.app f x)
  stable := fun h =>
    ⟨fun hf x hx => ((B.fibre x).stable (.left h x)).mp (hf x hx),
     fun hg x hx => ((B.fibre x).stable (.left h x)).mpr (hg x hx)⟩

theorem dependent_application_conversion {A : Code} {B : CoherentFamily}
    {f g x y : Term} (hf : (dependentPi A B).accepts f) (hx : A.accepts x)
    (fg : Conv f g) (xy : Conv x y) : (B.fibre y).accepts (.app g y) := by
  have h := hf x hx
  have hc : Conv (.app f x) (.app g y) :=
    .trans (Conv.left fg x) (Conv.right g xy)
  have ht := (code_conversion (B.fibre x) hc).mp h
  exact (B.coherent xy (.app g y)).mp ht

def pairTerm (x y : Term) : Term :=
  .app (.app .s (.app (.app .s .i) (.app .k x))) (.app .k y)

theorem red_trans {t u v} (h : Red t u) (k : Red u v) : Red t v := by
  induction h with
  | refl => exact k
  | tail h r ih => exact .tail h (ih k)

theorem red_conv {t u} (h : Red t u) : Conv t u := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .trans (.step h) ih

theorem pair_apply (x y f : Term) :
    Red (.app (pairTerm x y) f) (.app (.app f x) y) := by
  have h1 : Step (.app (pairTerm x y) f)
      (.app (.app (.app (.app .s .i) (.app .k x)) f) (.app (.app .k y) f)) :=
    .s (.app (.app .s .i) (.app .k x)) (.app .k y) f
  have h2 : Step
      (.app (.app (.app (.app .s .i) (.app .k x)) f) (.app (.app .k y) f))
      (.app (.app (.app .i f) (.app (.app .k x) f)) (.app (.app .k y) f)) :=
    .left (.s .i (.app .k x) f) _
  have h3 : Step
      (.app (.app (.app .i f) (.app (.app .k x) f)) (.app (.app .k y) f))
      (.app (.app f (.app (.app .k x) f)) (.app (.app .k y) f)) :=
    .left (.left (.i f) _) _
  have h4 : Step
      (.app (.app f (.app (.app .k x) f)) (.app (.app .k y) f))
      (.app (.app f x) (.app (.app .k y) f)) :=
    .left (.right f (.k x f)) _
  have h5 : Step (.app (.app f x) (.app (.app .k y) f)) (.app (.app f x) y) :=
    .right (.app f x) (.k y f)
  exact .tail h1 (.tail h2 (.tail h3 (.tail h4 (.tail h5 (.refl _)))))

def firstTerm (z : Term) : Term := .app z .k
def secondTerm (z : Term) : Term := .app z (.app .k .i)

theorem pair_first (x y : Term) : Conv (firstTerm (pairTerm x y)) x :=
  red_conv (red_trans (pair_apply x y .k) (Red.one (.k x y)))

theorem pair_second (x y : Term) : Conv (secondTerm (pairTerm x y)) y :=
  red_conv (red_trans (pair_apply x y (.app .k .i)) (false_selects x y))

def dependentSigma (A : Code) (B : CoherentFamily) : Code where
  accepts := fun z => ∃ x y, A.accepts x ∧ (B.fibre x).accepts y ∧ Conv z (pairTerm x y)
  stable := fun h =>
    ⟨fun ⟨x,y,hx,hy,hz⟩ => ⟨x,y,hx,hy,.trans (.symm (.step h)) hz⟩,
     fun ⟨x,y,hx,hy,hz⟩ => ⟨x,y,hx,hy,.trans (.step h) hz⟩⟩

theorem sigma_projections {A : Code} {B : CoherentFamily} {z : Term}
    (hz : (dependentSigma A B).accepts z) :
    A.accepts (firstTerm z) ∧ (B.fibre (firstTerm z)).accepts (secondTerm z) := by
  obtain ⟨x,y,hx,hy,hz⟩ := hz
  have hf : Conv (firstTerm z) x := .trans (Conv.left hz .k) (pair_first x y)
  have hs : Conv (secondTerm z) y :=
    .trans (Conv.left hz (.app .k .i)) (pair_second x y)
  exact ⟨(code_conversion A hf).mpr hx,
    (B.coherent hf (secondTerm z)).mpr ((code_conversion (B.fibre x) hs).mpr hy)⟩

def equalityCode (A : Code) (x y : Term) : Code where
  accepts := fun p => A.accepts x ∧ A.accepts y ∧ Conv x y ∧ Conv p .i
  stable := fun h =>
    ⟨fun ⟨hx,hy,hxy,hp⟩ => ⟨hx,hy,hxy,.trans (.symm (.step h)) hp⟩,
     fun ⟨hx,hy,hxy,hp⟩ => ⟨hx,hy,hxy,.trans (.step h) hp⟩⟩

theorem equality_reflexive {A : Code} {x : Term} (hx : A.accepts x) :
    (equalityCode A x x).accepts .i := ⟨hx,hx,.refl x,.refl .i⟩

theorem equality_transport {A : Code} {B : CoherentFamily} {x y p t : Term}
    (h : (equalityCode A x y).accepts p) (ht : (B.fibre x).accepts t) :
    (B.fibre y).accepts t := (B.coherent h.2.2.1 t).mp ht

end OrthemologyV3

#print axioms OrthemologyV3.effect_sound
#print axioms OrthemologyV3.no_empty_effect
#print axioms OrthemologyV3.probabilistic_boolean_projection
#print axioms OrthemologyV3.dependent_application_conversion
#print axioms OrthemologyV3.sigma_projections
#print axioms OrthemologyV3.equality_transport
