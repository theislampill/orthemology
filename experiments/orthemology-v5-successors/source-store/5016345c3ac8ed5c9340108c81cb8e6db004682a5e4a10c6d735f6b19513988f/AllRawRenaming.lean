/- Raw type-parameter renaming, prior to any formation laws. -/
import AllRawSubstitution
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def renvMap (r : REnv) (f : Nat → Nat) : REnv where
  left := fun n => r.left (f n)
  right := fun n => r.right (f n)
  rel := fun n => r.rel (f n)
  endpoints := fun n => r.endpoints (f n)
  respect := fun n => r.respect (f n)

theorem renvMap_diag (ρ : OEnv) (f : Nat → Nat) :
    renvMap (diagEnv ρ) f = diagEnv (fun n => ρ (f n)) := rfl

theorem cons_liftRen (P : PER) (ρ : OEnv) (f : Nat → Nat) :
    (fun n => cons P ρ (liftRen f n)) = cons P (fun n => ρ (f n)) := by
  funext n; cases n <;> rfl

theorem renvMap_extend {P Q : PER} (R : Link P Q) (r : REnv) (f : Nat → Nat) :
    renvMap (extendEnv R r) (liftRen f) = extendEnv R (renvMap r f) := by
  apply renv_ext
  · exact cons_liftRen _ _ _
  · exact cons_liftRen _ _ _
  · funext n; cases n <;> rfl

theorem FG_trename (A : Ty) :
    (∀ f ρ η t u, F (trename f A) ρ η t u = F A (fun n => ρ (f n)) η t u) ∧
    (∀ f r η ξ t u, G (trename f A) r η ξ t u = G A (renvMap r f) η ξ t u) := by
  induction A with
  | param n => exact ⟨fun _ _ _ _ _ => rfl,fun _ _ _ _ _ _ => rfl⟩
  | bottom => exact ⟨fun _ _ _ _ _ => rfl,fun _ _ _ _ _ _ => rfl⟩
  | raw => exact ⟨fun _ _ _ _ _ => rfl,fun _ _ _ _ _ _ => rfl⟩
  | identity A p q ih =>
      constructor
      · intros; simp only [trename,F_identity,ih.1]
      · intros; simp only [trename,G_identity,ih.1,renvMap]
  | pi A B ha hb =>
      constructor
      · intros; simp only [trename,F_pi,ha.1,hb.1]
      · intros; simp only [trename,G_pi,F_pi,ha.1,hb.1,ha.2,hb.2,renvMap]
  | sigma A B ha hb =>
      constructor
      · intros; simp only [trename,F_sigma,ha.1,hb.1]
      · intros; simp only [trename,G_sigma,F_sigma,ha.1,hb.1,ha.2,hb.2,renvMap]
  | all B ih =>
      constructor
      · intros; simp only [trename,F_all,ih.1,ih.2,renvMap_extend,renvMap_diag,cons_liftRen]
      · intro f r η ξ t u
        simp only [trename,G_all,F_all,ih.1,ih.2,renvMap_extend,renvMap_diag,cons_liftRen]
        rfl

theorem F_trename (A : Ty) (f : Nat → Nat) (ρ : OEnv) (η : Env) (t u : Term) :
    F (trename f A) ρ η t u = F A (fun n => ρ (f n)) η t u := (FG_trename A).1 f ρ η t u

theorem G_trename (A : Ty) (f : Nat → Nat) (r : REnv) (η ξ : Env) (t u : Term) :
    G (trename f A) r η ξ t u = G A (renvMap r f) η ξ t u := (FG_trename A).2 f r η ξ t u

theorem F_twk (A : Ty) (P : PER) (ρ : OEnv) (η : Env) (t u : Term) :
    F (twk A) (cons P ρ) η t u = F A ρ η t u := F_trename A Nat.succ _ η t u

theorem G_twk (A : Ty) {P Q : PER} (R : Link P Q) (r : REnv) (η ξ : Env) (t u : Term) :
    G (twk A) (extendEnv R r) η ξ t u = G A r η ξ t u := by
  rw [twk,G_trename]
  rfl

theorem D_twk (Γ : Tel) (P : PER) (ρ : OEnv) (η : Env) :
    D (twkTel Γ) (cons P ρ) η = D Γ ρ η := by
  induction Γ generalizing η with
  | nil => rfl
  | cons A Γ ih => simp only [twkTel,List.map_cons,D,F_twk]; rw [← twkTel,ih]

theorem E_twk (Γ : Tel) (P : PER) (ρ : OEnv) (η ξ : Env) :
    E (twkTel Γ) (cons P ρ) η ξ = E Γ ρ η ξ := by
  induction Γ generalizing η ξ with
  | nil => rfl
  | cons A Γ ih => simp only [twkTel,List.map_cons,E,F_twk]; rw [← twkTel,ih]

theorem H_twk (Γ : Tel) {P Q : PER} (R : Link P Q) (r : REnv) (η ξ : Env) :
    H (twkTel Γ) (extendEnv R r) η ξ = H Γ r η ξ := by
  induction Γ generalizing η ξ with
  | nil => rfl
  | cons A Γ ih => simp only [twkTel,List.map_cons,H,G_twk]; rw [← twkTel,ih]

end P01AC
