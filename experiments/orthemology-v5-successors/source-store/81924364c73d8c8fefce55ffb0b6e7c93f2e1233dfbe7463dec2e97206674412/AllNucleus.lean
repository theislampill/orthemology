/- Full accepted-nucleus derivation translation, preserving literal source polynomials. -/
import AllNucleusSyntax
import AllSoundness
import TypedSoundness
namespace P01AC.Nucleus
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem form {Γ A} (h : P01TC.Form Γ A) : Form (telescope Γ) (translate A) := by
  induction h using P01TC.Form.rec
    (motive_1 := fun Γ _ => Ctx (telescope Γ))
    (motive_3 := fun Γ p A _ => Has (telescope Γ) p (translate A)) with
  | nil => exact .nil
  | ext hΓ hA c a => exact .ext c a
  | param hΓ c => exact .param c
  | bottom hΓ c => exact .bottom c
  | allFinite hΓ c => exact .all c (form_fin _ (ctx_twk c))
  | raw hΓ c => exact .raw c
  | pi hA hB a b => exact .pi a b
  | sigma hA hB a b => exact .sigma a b
  | identity hA hp hq a p q => exact .identity a p q
  | var hA hv a => exact .var a (lookup hv)
  | i hA ht a t => simpa only [translate_arr] using Has.i a (by simpa only [translate_arr] using t)
  | k hA hB ht a b t => simpa only [translate_arr] using Has.k a b (by simpa only [translate_arr] using t)
  | s hA hB hC ht a b c t => simpa only [translate_arr] using Has.s a b c (by simpa only [translate_arr] using t)
  | finite hA hf a => simpa only [translate_fin] using finite_import (form_ctx a) hf
  | rawAtom hA a => exact .rawAtom a
  | rawApp hA hf hx a f x => exact .rawApp a f x
  | piIntro hA hb hs a b =>
      apply Has.piIntro a b
      simpa only [telescope,List.length_map] using (scoped_agrees _ _).mp hs
  | piElim hPi ht hf ha pi t f a =>
      simpa only [translate_inst] using Has.piElim pi (by simpa only [translate_inst] using t) f a
  | sigmaIntro hSigma ht ha hb s t a b =>
      exact Has.sigmaIntro s (by simpa only [translate_inst] using t) a (by simpa only [translate_inst] using b)
  | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
  | sigmaSnd hSigma ht hz s t z =>
      simpa only [translate_inst] using Has.sigmaSnd s (by simpa only [translate_inst] using t) z
  | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
  | proofErase hRaw hId hp a i p => exact .proofErase a i p
  | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
      simpa only [translate_motiveAt] using Has.j a (by simpa only [telescope_theta] using b) i
        (by simpa only [translate_motiveAt] using base) (by simpa only [translate_motiveAt] using t)
        x y e (by simpa only [translate_motiveAt] using d)
  | conv hA hp pq hs a p =>
      exact .conv a p pq (by simpa only [telescope,List.length_map] using (scoped_agrees _ _).mp hs)

theorem has {Γ p A} (h : P01TC.Has Γ p A) : Has (telescope Γ) p (translate A) := by
  induction h using P01TC.Has.rec
    (motive_1 := fun Γ _ => Ctx (telescope Γ))
    (motive_2 := fun Γ A _ => Form (telescope Γ) (translate A)) with
  | nil => exact .nil
  | ext hΓ hA c a => exact .ext c a
  | param hΓ c => exact .param c
  | bottom hΓ c => exact .bottom c
  | allFinite hΓ c => exact .all c (form_fin _ (ctx_twk c))
  | raw hΓ c => exact .raw c
  | pi hA hB a b => exact .pi a b
  | sigma hA hB a b => exact .sigma a b
  | identity hA hp hq a p q => exact .identity a p q
  | var hA hv a => exact .var a (lookup hv)
  | i hA ht a t => simpa only [translate_arr] using Has.i a (by simpa only [translate_arr] using t)
  | k hA hB ht a b t => simpa only [translate_arr] using Has.k a b (by simpa only [translate_arr] using t)
  | s hA hB hC ht a b c t => simpa only [translate_arr] using Has.s a b c (by simpa only [translate_arr] using t)
  | finite hA hf a => simpa only [translate_fin] using finite_import (form_ctx a) hf
  | rawAtom hA a => exact .rawAtom a
  | rawApp hA hf hx a f x => exact .rawApp a f x
  | piIntro hA hb hs a b =>
      apply Has.piIntro a b
      simpa only [telescope,List.length_map] using (scoped_agrees _ _).mp hs
  | piElim hPi ht hf ha pi t f a =>
      simpa only [translate_inst] using Has.piElim pi (by simpa only [translate_inst] using t) f a
  | sigmaIntro hSigma ht ha hb s t a b =>
      exact Has.sigmaIntro s (by simpa only [translate_inst] using t) a (by simpa only [translate_inst] using b)
  | sigmaFst hA hSigma hz a s z => exact .sigmaFst a s z
  | sigmaSnd hSigma ht hz s t z =>
      simpa only [translate_inst] using Has.sigmaSnd s (by simpa only [translate_inst] using t) z
  | identityIntro hId hp hq pq a p q => exact .identityIntro a p q pq
  | proofErase hRaw hId hp a i p => exact .proofErase a i p
  | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
      simpa only [translate_motiveAt] using Has.j a (by simpa only [telescope_theta] using b) i
        (by simpa only [translate_motiveAt] using base) (by simpa only [translate_motiveAt] using t)
        x y e (by simpa only [translate_motiveAt] using d)
  | conv hA hp pq hs a p =>
      exact .conv a p pq (by simpa only [telescope,List.length_map] using (scoped_agrees _ _).mp hs)

theorem context {Γ} (h : P01TC.Ctx Γ) : Ctx (telescope Γ) := form_ctx (form (.raw h))

theorem F_agrees (A : P01TC.Ty) (ρ : OEnv) (η : Env) (t u : Term) :
    F (translate A) ρ η t u = P01TC.F A ρ η t u := by
  induction A generalizing η t u with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | allFinite C => exact F_fin (.all C) ρ η t u
  | pi A B ha hb => simp only [translate,F_pi,P01TC.F,ha,hb]
  | sigma A B ha hb => simp only [translate,F_sigma,P01TC.F,ha,hb]
  | identity A p q ha => simp only [translate,F_identity,P01TC.F,ha]

theorem G_agrees (A : P01TC.Ty) (r : REnv) (η ξ : Env) (t u : Term) :
    G (translate A) r η ξ t u = P01TC.G A r η ξ t u := by
  induction A generalizing η ξ t u with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | allFinite C => exact G_fin (.all C) r η ξ t u
  | pi A B ha hb =>
      change (F (translate (.pi A B)) r.left η t t ∧ F (translate (.pi A B)) r.right ξ u u ∧
        ∀ a b, G (translate A) r η ξ a b → G (translate B) r (cons a η) (cons b ξ) (.app t a) (.app u b)) = _
      simp only [F_agrees,P01TC.G,ha,hb]
  | sigma A B ha hb =>
      change (F (translate (.sigma A B)) r.left η t t ∧ F (translate (.sigma A B)) r.right ξ u u ∧
        Represented t ∧ Represented u ∧ G (translate A) r η ξ (firstTerm t) (firstTerm u) ∧
        G (translate B) r (cons (firstTerm t) η) (cons (firstTerm u) ξ) (secondTerm t) (secondTerm u)) = _
      simp only [F_agrees,P01TC.G,ha,hb]
  | identity A p q ha => simp only [translate,G_identity,P01TC.G,F_agrees]

theorem D_agrees (Γ : P01TC.Tel) (ρ : OEnv) (η : Env) : D (telescope Γ) ρ η = P01TC.D Γ ρ η := by
  induction Γ generalizing η with
  | nil => rfl
  | cons A Γ ih => simp only [telescope,List.map_cons,D,P01TC.D,F_agrees]; rw [← telescope,ih]; rfl

theorem E_agrees (Γ : P01TC.Tel) (ρ : OEnv) (η ξ : Env) : E (telescope Γ) ρ η ξ = P01TC.E Γ ρ η ξ := by
  induction Γ generalizing η ξ with
  | nil => rfl
  | cons A Γ ih => simp only [telescope,List.map_cons,E,P01TC.E,F_agrees]; rw [← telescope,ih]; rfl

theorem H_agrees (Γ : P01TC.Tel) (r : REnv) (η ξ : Env) : H (telescope Γ) r η ξ = P01TC.H Γ r η ξ := by
  induction Γ generalizing η ξ with
  | nil => rfl
  | cons A Γ ih => simp only [telescope,List.map_cons,H,P01TC.H,G_agrees]; rw [← telescope,ih]; rfl

end P01AC.Nucleus
