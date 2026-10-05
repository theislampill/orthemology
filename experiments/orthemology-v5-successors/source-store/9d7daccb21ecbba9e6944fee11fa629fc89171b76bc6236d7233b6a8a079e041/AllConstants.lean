/- Exact finite-leaf and nondependent combinator bridge. -/
import AllBinderLaws
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def objectOf {Γ A ρ η} (h : TypeLaws Γ A) (d : D Γ ρ η) : PER := (h.per d).per

def linkOf {Γ A} {r : REnv} {η ξ} (h : TypeLaws Γ A) (dη : D Γ r.left η) (dξ : D Γ r.right ξ) :
    Link (objectOf h dη) (objectOf h dξ) where
  rel := G A r η ξ
  endpoints := h.ends dη dξ
  respect := h.respect dη dξ

theorem F_arr (A B : Ty) (ρ : OEnv) (η : Env) (f g : Term) :
    F (arr A B) ρ η f g = (∀ a b, F A ρ η a b → F B ρ η (.app f a) (.app g b)) := by
  simp only [arr,F_pi,F_wk]

theorem G_arr (A B : Ty) (r : REnv) (η ξ : Env) (f g : Term) :
    G (arr A B) r η ξ f g =
      ((∀ a b, F A r.left η a b → F B r.left η (.app f a) (.app f b)) ∧
       (∀ a b, F A r.right ξ a b → F B r.right ξ (.app g a) (.app g b)) ∧
       ∀ a b, G A r η ξ a b → G B r η ξ (.app f a) (.app g b)) := by
  simp only [arr,G_pi,F_pi,F_wk,G_wk]

theorem fundamental_i {Γ A} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) :
    Fundamental Γ (.atom .i) (arr A A) := by
  intro r η ξ h
  have ds := hc.hends h
  have v := identity_link (linkOf ha ds.1 ds.2)
  simpa only [G_arr,arrowLink,ArrPER,PiPER,linkOf,objectOf,RelLaws.per,PER.dom,eval] using v

theorem fundamental_k {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A) (hb : TypeLaws Γ B) :
    Fundamental Γ (.atom .k) (arr A (arr B A)) := by
  intro r η ξ h
  have ds := hc.hends h
  have v := k_link (linkOf ha ds.1 ds.2) (linkOf hb ds.1 ds.2)
  simpa only [G_arr,F_arr,arrowLink,ArrPER,PiPER,linkOf,objectOf,RelLaws.per,PER.dom,eval] using v

theorem fundamental_s {Γ A B C} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws Γ B) (hcc : TypeLaws Γ C) :
    Fundamental Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) := by
  intro r η ξ h
  have ds := hc.hends h
  have v := s_link (linkOf ha ds.1 ds.2) (linkOf hb ds.1 ds.2) (linkOf hcc ds.1 ds.2)
  simpa only [G_arr,F_arr,arrowLink,ArrPER,PiPER,linkOf,objectOf,RelLaws.per,PER.dom,eval] using v


end P01AC
