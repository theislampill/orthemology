/- Raw comparison with the unchanged accepted finite interpretation. -/
import AllConstants
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem FG_fin (C : TypeCode) :
    (∀ ρ η t u, F (fin C) ρ η t u = ((P01R.interpret C).obj ρ).rel t u) ∧
    (∀ r η ξ t u, G (fin C) r η ξ t u = (P01R.interpret C).rel r t u) := by
  induction C with
  | var n => exact ⟨fun _ _ _ _ => rfl,fun _ _ _ _ _ => rfl⟩
  | bottom => exact ⟨fun _ _ _ _ => rfl,fun _ _ _ _ _ => rfl⟩
  | arrow A B ha hb =>
      constructor
      · intros; simp only [fin,F_arr,ha.1,hb.1,P01R.interpret,arrowModel,ArrPER,PiPER]
      · intros; simp only [fin,G_arr,ha.1,hb.1,ha.2,hb.2,P01R.interpret,arrowModel,arrowLink,Model.asLink,PER.dom,ArrPER,PiPER]
  | all B ih =>
      have fo : ∀ ρ η t u, F (.all (fin B)) ρ η t u = ((P01R.interpret (.all B)).obj ρ).rel t u := by
        intros; simp only [F_all,ih.1,ih.2,P01R.interpret,allModel,AllPER,Parametric,bodyFamily,Model.asLink]
      refine ⟨fo,?_⟩
      intros; simp only [fin,G_all,fo,ih.2,P01R.interpret,allModel,PER.dom]

theorem F_fin (C : TypeCode) (ρ : OEnv) (η : Env) (t u : Term) :
    F (fin C) ρ η t u = ((P01R.interpret C).obj ρ).rel t u := (FG_fin C).1 ρ η t u

theorem G_fin (C : TypeCode) (r : REnv) (η ξ : Env) (t u : Term) :
    G (fin C) r η ξ t u = (P01R.interpret C).rel r t u := (FG_fin C).2 r η ξ t u

end P01AC
