/- New finite shared-seed semantics. It extends actual closed MExpr programs with
   open polynomial leaves admitted only by FiniteDerives or the qualified Curry
   Has theorem; fixed rational weights and independent subtree coordinates are
   retained. This is not a theorem about value-dependent bind or recursion. -/
import P01CurryParametricity
import Mathlib.Data.Fintype.Prod
namespace P01R
open OrthemologyV2 OrthemologyV3 P01D

inductive EExpr where
  | pure : Poly → EExpr
  | mix : Weight → EExpr → EExpr → EExpr
  | app : EExpr → EExpr → EExpr

def Seed : EExpr → Type
  | .pure _ => Unit
  | .mix p l r => Fin p.den × Seed l × Seed r
  | .app f x => Seed f × Seed x

instance seedFintype : (e : EExpr) → Fintype (Seed e)
  | .pure _ => inferInstanceAs (Fintype Unit)
  | .mix p l r => by
      letI := seedFintype l
      letI := seedFintype r
      exact inferInstanceAs (Fintype (Fin p.den × Seed l × Seed r))
  | .app f x => by
      letI := seedFintype f
      letI := seedFintype x
      exact inferInstanceAs (Fintype (Seed f × Seed x))

instance seedInhabited : (e : EExpr) → Inhabited (Seed e)
  | .pure _ => ⟨()⟩
  | .mix p l r => ⟨⟨⟨0,p.positiveDen⟩,(seedInhabited l).default,(seedInhabited r).default⟩⟩
  | .app f x => ⟨(seedInhabited f).default,(seedInhabited x).default⟩

def run : (e : EExpr) → P01D.Env → Seed e → Term
  | .pure p, θ, _ => eval p θ
  | .mix p l r, θ, s => if s.1.val < p.num then run l θ s.2.1 else run r θ s.2.2
  | .app f x, θ, s => .app (run f θ s.1) (run x θ s.2)

def erase : EExpr → P01D.Env → MExpr
  | .pure p, θ => .pure (eval p θ)
  | .mix p l r, θ => .mix p (erase l θ) (erase r θ)
  | .app f x, θ => .app (erase f θ) (erase x θ)

def embed : MExpr → EExpr
  | .pure t => .pure (.atom t)
  | .mix p l r => .mix p (embed l) (embed r)
  | .app f x => .app (embed f) (embed x)

theorem erase_embed (e : MExpr) (θ : P01D.Env) : erase (embed e) θ = e := by
  induction e with
  | pure t => rfl
  | mix p l r ihl ihr => simp only [embed,erase,ihl,ihr]
  | app f x ihf ihx => simp only [embed,erase,ihf,ihx]

theorem seed_outcome (e : EExpr) (θ : P01D.Env) (s : Seed e) : Outcome (erase e θ) (run e θ s) := by
  induction e with
  | pure p => exact .pure _
  | mix p l r ihl ihr =>
      by_cases h : s.1.val < p.num
      · have hp : 0 < p.num := Nat.lt_of_le_of_lt (Nat.zero_le _) h
        simpa only [erase,run,if_pos h] using Outcome.mixL hp (ihl s.2.1)
      · have hp : p.num < p.den := Nat.lt_of_le_of_lt (Nat.le_of_not_lt h) s.1.isLt
        simpa only [erase,run,if_neg h] using Outcome.mixR hp (ihr s.2.2)
  | app f x ihf ihx => exact .app (ihf s.1) (ihx s.2)

theorem outcome_has_seed (e : EExpr) (θ : P01D.Env) {t : Term}
    (h : Outcome (erase e θ) t) : ∃s : Seed e, run e θ s = t := by
  induction e generalizing t with
  | pure p =>
      cases h
      exact ⟨(),rfl⟩
  | mix p l r ihl ihr =>
      cases h with
      | mixL hp hl =>
          obtain ⟨s,hs⟩ := ihl hl
          refine ⟨(⟨0,p.positiveDen⟩,s,default),?_⟩
          simpa only [run,if_pos hp] using hs
      | mixR hp hr =>
          obtain ⟨s,hs⟩ := ihr hr
          refine ⟨(⟨p.num,hp⟩,default,s),?_⟩
          simpa only [run,Nat.lt_irrefl,if_false] using hs
  | app f x ihf ihx =>
      cases h with
      | app hf hx =>
          obtain ⟨sf,rfl⟩ := ihf hf
          obtain ⟨sx,rfl⟩ := ihx hx
          exact ⟨(sf,sx),rfl⟩

theorem seed_support_exact (e : EExpr) (θ : P01D.Env) (t : Term) :
    (∃s : Seed e, run e θ s = t) ↔ Outcome (erase e θ) t := by
  constructor
  · rintro ⟨s,rfl⟩
    exact seed_outcome e θ s
  · exact outcome_has_seed e θ

inductive EHas : P01F.Context → EExpr → TypeCode → Prop where
  | pureFinite {Γ t A} : FiniteDerives t A → EHas Γ (.pure (.atom t)) A
  | pureCurry {Γ t A} : P01F.Has Γ t A → EHas Γ (.pure (compile t)) A
  | mix {Γ l r A} : EHas Γ l A → EHas Γ r A → (p : Weight) → EHas Γ (.mix p l r) A
  | app {Γ f x A B} : EHas Γ f (.arrow A B) → EHas Γ x A → EHas Γ (.app f x) B
  | allI {Γ e B} : EHas (P01F.shiftContext Γ) e B → EHas Γ e (.all B)
  | allE {Γ e B} : EHas Γ e (.all B) → (A : TypeCode) → EHas Γ e (instantiateType B A)

/-- All five actual effect typing rules embed, preserving the literal original
    raw programs and weights, not merely beta-equivalent recompilations. -/
theorem original_effect_embeds {e A} (h : EffectDerives e A) : ∀Γ, EHas Γ (embed e) A := by
  induction h with
  | pure h => intro Γ; exact .pureFinite h
  | mix hl hr p ihl ihr => intro Γ; exact .mix (ihl Γ) (ihr Γ) p
  | app hf hx ihf ihx => intro Γ; exact .app (ihf Γ) (ihx Γ)
  | allI h ih => intro Γ; exact .allI (ih (P01F.shiftContext Γ))
  | allE h A ih => intro Γ; exact .allE (ih Γ) A

/-- One *fixed seed* relates the two runs for every admissible relational
    environment. The seed type and run functions do not depend on that relation. -/
theorem shared_seed_fundamental {Γ e A} (h : EHas Γ e A) :
    ∀ r θ η, ValRelated Γ r θ η → ∀s : Seed e,
      (interpret A).rel r (run e θ s) (run e η s) := by
  induction h with
  | pureFinite h =>
      intro r θ η hv s
      exact finite_fundamental h r
  | pureCurry h =>
      intro r θ η hv s
      exact curry_fundamental h r θ η hv
  | mix hl hr p ihl ihr =>
      intro r θ η hv s
      by_cases h : s.1.val < p.num
      · simpa only [run,if_pos h] using ihl r θ η hv s.2.1
      · simpa only [run,if_neg h] using ihr r θ η hv s.2.2
  | app hf hx ihf ihx =>
      intro r θ η hv s
      exact (ihf r θ η hv s.1).2.2 _ _ (ihx r θ η hv s.2)
  | allI h ih =>
      intro r θ η hv s
      refine ⟨?_,?_,?_⟩
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.left)) θ θ (valuations_shift (valuations_left hv) R) s
      · apply (all_domain _ _).mpr
        intro P Q R
        exact ih (extendEnv R (diagEnv r.right)) η η (valuations_shift (valuations_right hv) R) s
      · intro P Q R
        exact ih (extendEnv R r) θ η (valuations_shift hv R) s
  | @allE Γ e B h A ih =>
      intro r θ η hv s
      apply (instantiate_rel B A r _ _).mpr
      exact (ih r θ η hv s).2.2 ((interpret A).obj r.left) ((interpret A).obj r.right)
        ((interpret A).asLink r)


theorem run_embed_independent (e : MExpr) (θ η : P01D.Env) (s : Seed (embed e)) :
    run (embed e) θ s = run (embed e) η s := by
  induction e with
  | pure t => rfl
  | mix p l r ihl ihr =>
      by_cases h : s.1.val < p.num
      · simpa only [embed,run,if_pos h] using ihl s.2.1
      · simpa only [embed,run,if_neg h] using ihr s.2.2
  | app f x ihf ihx =>
      exact congrArg₂ Term.app (ihf s.1) (ihx s.2)

theorem original_outcome_finite {e A} (h : EffectDerives e A) :
    ∀ t, Outcome e t → FiniteDerives t A := by
  induction h with
  | pure h => intro t ho; cases ho; exact h
  | mix hl hr p ihl ihr =>
      intro t ho
      cases ho with
      | mixL hp ho => exact ihl t ho
      | mixR hp ho => exact ihr t ho
  | app hf hx ihf ihx =>
      intro t ho
      cases ho with
      | app of ox => exact .app (ihf _ of) (ihx _ ox)
  | allI h ih => intro t ho; exact .allI (ih t ho)
  | allE h X ih => intro t ho; exact .allE (ih t ho) X

theorem original_seed_relational {e A} (h : EffectDerives e A)
    (θ η : P01D.Env) (s : Seed (embed e)) (r : REnv) :
    (interpret A).rel r (run (embed e) θ s) (run (embed e) η s) := by
  rw [← run_embed_independent e θ η s]
  have ho : Outcome e (run (embed e) θ s) := by
    simpa only [erase_embed] using seed_outcome (embed e) θ s
  exact finite_fundamental (original_outcome_finite h _ ho) r

end P01R
