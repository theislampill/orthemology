/- Paired raw term substitution is unconditional; type substitution is deliberately separate. -/
import AllPredicates
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem FG_subst (A : Ty) :
    (∀ σ ρ η t u, F (subst σ A) ρ η t u = F A ρ (fun n => eval (σ n) η) t u) ∧
    (∀ σ r η ξ t u, G (subst σ A) r η ξ t u =
      G A r (fun n => eval (σ n) η) (fun n => eval (σ n) ξ) t u) := by
  induction A with
  | param n => exact ⟨fun _ _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | bottom => exact ⟨fun _ _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | raw => exact ⟨fun _ _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | identity A p q ih =>
      constructor
      · intros; simp only [subst, F_identity, ih.1, eval_sub]
      · intros; simp only [subst, G_identity, ih.1, eval_sub]
  | pi A B ha hb =>
      constructor
      · intros; simp only [subst, F_pi, ha.1, hb.1, eval_pup_env]
      · intros; simp only [subst, G_pi, F_pi, ha.1, hb.1, ha.2, hb.2, eval_pup_env]
  | sigma A B ha hb =>
      constructor
      · intros; simp only [subst, F_sigma, ha.1, hb.1, eval_pup_env]
      · intros; simp only [subst, G_sigma, F_sigma, ha.1, hb.1, ha.2, hb.2, eval_pup_env]
  | all B ih =>
      constructor
      · intros; simp only [subst, F_all, ih.1, ih.2]
      · intros; simp only [subst, G_all, F_all, ih.1, ih.2]

theorem F_subst (A : Ty) (σ : Nat → Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (subst σ A) ρ η t u = F A ρ (fun n => eval (σ n) η) t u := (FG_subst A).1 σ ρ η t u

theorem G_subst (A : Ty) (σ : Nat → Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (subst σ A) r η ξ t u =
      G A r (fun n => eval (σ n) η) (fun n => eval (σ n) ξ) t u := (FG_subst A).2 σ r η ξ t u

theorem F_wk (A : Ty) (ρ : OEnv) (η : Env) (a t u : Term) :
    F (wk A) ρ (cons a η) t u = F A ρ η t u := F_subst A _ ρ _ t u

theorem G_wk (A : Ty) (r : REnv) (η ξ : Env) (a b t u : Term) :
    G (wk A) r (cons a η) (cons b ξ) t u = G A r η ξ t u := G_subst A _ r _ _ t u

theorem F_inst (B : Ty) (a : Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (inst B a) ρ η t u = F B ρ (cons (eval a η) η) t u := by
  simpa only [inst,eval_cons_poly,eval] using F_subst B (cons a Poly.var) ρ η t u

theorem G_inst (B : Ty) (a : Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (inst B a) r η ξ t u = G B r (cons (eval a η) η) (cons (eval a ξ) ξ) t u :=
  by simpa only [inst,eval_cons_poly,eval] using G_subst B (cons a Poly.var) r η ξ t u

theorem F_motiveAt (B : Ty) (y e : Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (motiveAt B y e) ρ η t u = F B ρ (cons (eval e η) (cons (eval y η) η)) t u :=
  by simpa only [motiveAt,eval_cons_poly,eval] using F_subst B (cons e (cons y Poly.var)) ρ η t u

theorem G_motiveAt (B : Ty) (y e : Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (motiveAt B y e) r η ξ t u =
      G B r (cons (eval e η) (cons (eval y η) η)) (cons (eval e ξ) (cons (eval y ξ) ξ)) t u :=
  by simpa only [motiveAt,eval_cons_poly,eval] using G_subst B (cons e (cons y Poly.var)) r η ξ t u

end P01AC
