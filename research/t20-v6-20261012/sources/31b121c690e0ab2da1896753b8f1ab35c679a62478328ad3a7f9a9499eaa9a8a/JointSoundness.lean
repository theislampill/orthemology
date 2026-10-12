import JointSyntax
namespace JointCompletion
open P01AC P01D FullPER
open OpenTermStandardness (Conv)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000
theorem form_sound {Γ A} (h : FormJ Γ A) : FullPER.FormSound Γ A := by
  induction h using FormJ.rec
    (motive_1 := fun Γ _ => FullPER.ContextLaws Γ)
    (motive_3 := fun Γ p A _ => FullPER.TermSound Γ p A) with
    | ctxBase h => exact FullPER.context_sound h
    | formBase h => exact FullPER.form_sound h
    | hasBase h => exact FullPER.has_sound h
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

    | sigmaElim hΓ hA hB hP hd hz c a b p d z =>
        exact ⟨⟨c,hereditary_inst c p.2 z.2⟩,
          sigma_elimination c a.2.laws b.2.laws p.2.laws d.2 z.2⟩
    | natInduction hΓ hP hp hs c p seed step =>
        exact ⟨⟨c,type_pi c (nat_laws _) p.2.laws,hereditary_nat c,p.2⟩,
          dependent_induction c p.2.laws seed.2 step.2⟩


theorem has_sound {Γ p A} (h : HasJ Γ p A) : FullPER.TermSound Γ p A := by
  induction h using HasJ.rec
    (motive_1 := fun Γ _ => FullPER.ContextLaws Γ)
    (motive_2 := fun Γ A _ => FullPER.FormSound Γ A) with
    | ctxBase h => exact FullPER.context_sound h
    | formBase h => exact FullPER.form_sound h
    | hasBase h => exact FullPER.has_sound h
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



    | sigmaElim hΓ hA hB hP hd hz c a b p d z =>
        exact ⟨⟨c,hereditary_inst c p.2 z.2⟩,
          sigma_elimination c a.2.laws b.2.laws p.2.laws d.2 z.2⟩
    | natInduction hΓ hP hp hs c p seed step =>
        exact ⟨⟨c,type_pi c (nat_laws _) p.2.laws,hereditary_nat c,p.2⟩,
          dependent_induction c p.2.laws seed.2 step.2⟩


theorem context_sound {Γ} (h : CtxJ Γ) : FullPER.ContextLaws Γ :=
  (form_sound (.raw h)).1

theorem fundamental {Γ p A} (h : HasJ Γ p A) : FullPER.Fundamental Γ p A :=
  (has_sound h).2

theorem no_closed_bottom (p : Poly) : ¬ HasJ [] p .bottom := by
  intro h
  exact fundamental h FullPER.Application.emptyEnv FullPER.zeroEnv FullPER.zeroEnv
    FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩

/-- Faithful Raw is unchanged even for the recursively extended calculus. -/
theorem raw_exact (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F .raw ρ η = OpenTermStandardness.Conv := rfl

theorem original_raw_distinct (η : FullPER.Env) :
    ¬ OpenTermStandardness.Conv (ImportedOpenTermTransport.interp FullPER.Application.originalP η)
      (ImportedOpenTermTransport.interp FullPER.Application.originalQ η) :=
  FullPER.Application.original_raw_distinct η

#print axioms form_sound
#print axioms has_sound
#print axioms fundamental
#print axioms no_closed_bottom
#print axioms raw_exact
#print axioms original_raw_distinct
end JointCompletion
