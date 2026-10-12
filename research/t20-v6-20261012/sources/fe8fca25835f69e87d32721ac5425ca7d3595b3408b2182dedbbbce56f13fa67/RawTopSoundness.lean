import RawTopTranslation
import JointSoundness

/- Diagnostic interpretation via Raw -> Pi Bottom.Bottom. This is not a
meaning-preserving alternative to the stipulated faithful Raw semantics. -/
namespace JointRawTop
open P01AC P01D FullPER
open OpenTermStandardness (T Conv SatPER)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- The bottom-domain function type denotes the universal relation. -/
theorem top_hereditary {Γ} (hc : FullPER.ContextLaws Γ) : FullPER.Hereditary Γ topTy :=
  ⟨type_pi hc (type_bottom _) (type_bottom _),
    ⟨type_bottom _,trivial⟩,⟨type_bottom _,trivial⟩⟩

theorem top_fundamental {Γ p} : FullPER.Fundamental Γ p topTy := by
  intro ρ η ξ r e x y h
  exact h

theorem lookup_translate {Γ n A} (h : Lookup Γ n A) :
    Lookup (translateTel Γ) n (translate A) := by
  induction h with
  | zero => simpa only [translate_wk] using Lookup.zero
  | succ h ih => simpa only [translate_wk] using Lookup.succ ih

theorem base_form_sound {Γ A} (h : P01AC.ExtensionalRepair.FormE Γ A) :
    FullPER.FormSound (translateTel Γ) (translate A) := by
  induction h using P01AC.ExtensionalRepair.FormE.rec
    (motive_1 := fun Γ _ => FullPER.ContextLaws (translateTel Γ))
    (motive_3 := fun Γ p A _ => FullPER.TermSound (translateTel Γ) p (translate A)) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b =>
        have hb := b.2
        simp only [translateTel_twk] at hb
        exact ⟨c,type_all hb.laws,hb⟩
    | raw hΓ c => exact ⟨c,top_hereditary c⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var (lookup_translate hv)⟩
    | i hA ht a t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_k a.1 a.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_s a.1 c.2.laws⟩
    | finite τ bound hτ hA hf a t =>
        refine ⟨t, ?_⟩
        simpa only [translate_finite_instance] using
          (fundamental_finite (τ := τ.map translate) t.1
            (fun n hn => by
              have v := (a n (by simpa only [List.length_map] using hn)).2.laws
              rw [← congrFun (translate_typeImages τ) n]
              exact v) hf)
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro (by simpa only [translateTel_twk] using p.2)⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,by simpa only [translate_tinst] using fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,top_fundamental⟩
    | rawApp hA hf hx a f x => exact ⟨a,top_fundamental⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,by simpa only [translate_inst] using fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 (by simpa only [translate_inst] using b.2)⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,by simpa only [translate_inst] using fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,top_fundamental⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,by
          have hb := b.2.laws
          have ht := t.2.laws
          have hd := d.2
          simp only [translateTel_theta] at hb
          simp only [translate_motiveAt] at ht hd ⊢
          exact fundamental_j a.1 a.2.laws hb ht e.2 hd⟩
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
        exact ⟨t,fundamental_all_ext p.1.1 (by simpa only [translateTel_twk] using h.2)⟩

theorem base_has_sound {Γ p A} (h : P01AC.ExtensionalRepair.HasE Γ p A) :
    FullPER.TermSound (translateTel Γ) p (translate A) := by
  induction h using P01AC.ExtensionalRepair.HasE.rec
    (motive_1 := fun Γ _ => FullPER.ContextLaws (translateTel Γ))
    (motive_2 := fun Γ A _ => FullPER.FormSound (translateTel Γ) (translate A)) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b =>
        have hb := b.2
        simp only [translateTel_twk] at hb
        exact ⟨c,type_all hb.laws,hb⟩
    | raw hΓ c => exact ⟨c,top_hereditary c⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var (lookup_translate hv)⟩
    | i hA ht a t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_k a.1 a.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_s a.1 c.2.laws⟩
    | finite τ bound hτ hA hf a t =>
        refine ⟨t, ?_⟩
        simpa only [translate_finite_instance] using
          (fundamental_finite (τ := τ.map translate) t.1
            (fun n hn => by
              have v := (a n (by simpa only [List.length_map] using hn)).2.laws
              rw [← congrFun (translate_typeImages τ) n]
              exact v) hf)
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro (by simpa only [translateTel_twk] using p.2)⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,by simpa only [translate_tinst] using fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,top_fundamental⟩
    | rawApp hA hf hx a f x => exact ⟨a,top_fundamental⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,by simpa only [translate_inst] using fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 (by simpa only [translate_inst] using b.2)⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,by simpa only [translate_inst] using fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,top_fundamental⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,by
          have hb := b.2.laws
          have ht := t.2.laws
          have hd := d.2
          simp only [translateTel_theta] at hb
          simp only [translate_motiveAt] at ht hd ⊢
          exact fundamental_j a.1 a.2.laws hb ht e.2 hd⟩
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
        exact ⟨t,fundamental_all_ext p.1.1 (by simpa only [translateTel_twk] using h.2)⟩

theorem base_context_sound {Γ} (h : P01AC.ExtensionalRepair.CtxE Γ) :
    FullPER.ContextLaws (translateTel Γ) := (base_form_sound (.raw h)).1

theorem has_sound {Γ p A} (h : JointCompletion.HasJ Γ p A) :
    FullPER.TermSound (translateTel Γ) p (translate A) := by
  induction h using JointCompletion.HasJ.rec
    (motive_1 := fun Γ _ => FullPER.ContextLaws (translateTel Γ))
    (motive_2 := fun Γ A _ => FullPER.FormSound (translateTel Γ) (translate A)) with
    | ctxBase h => exact base_context_sound h
    | formBase h => exact base_form_sound h
    | hasBase h => exact base_has_sound h
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b =>
        have hb := b.2
        simp only [translateTel_twk] at hb
        exact ⟨c,type_all hb.laws,hb⟩
    | raw hΓ c => exact ⟨c,top_hereditary c⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var (lookup_translate hv)⟩
    | i hA ht a t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_k a.1 a.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,by simpa only [translate_arr] using FullPER.fundamental_s a.1 c.2.laws⟩
    | finite τ bound hτ hA hf a t =>
        refine ⟨t, ?_⟩
        simpa only [translate_finite_instance] using
          (fundamental_finite (τ := τ.map translate) t.1
            (fun n hn => by
              have v := (a n (by simpa only [List.length_map] using hn)).2.laws
              rw [← congrFun (translate_typeImages τ) n]
              exact v) hf)
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro (by simpa only [translateTel_twk] using p.2)⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,by simpa only [translate_tinst] using fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,top_fundamental⟩
    | rawApp hA hf hx a f x => exact ⟨a,top_fundamental⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,by simpa only [translate_inst] using fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 (by simpa only [translate_inst] using b.2)⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,by simpa only [translate_inst] using fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,top_fundamental⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,by
          have hb := b.2.laws
          have ht := t.2.laws
          have hd := d.2
          simp only [translateTel_theta] at hb
          simp only [translate_motiveAt] at ht hd ⊢
          exact fundamental_j a.1 a.2.laws hb ht e.2 hd⟩
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
        exact ⟨t,fundamental_all_ext p.1.1 (by simpa only [translateTel_twk] using h.2)⟩

    | sigmaElim hΓ hA hB hP hd hz c a b p d z =>
        have hd := d.2
        simp only [translate_branchType] at hd
        have hh := JointCompletion.hereditary_inst c p.2 z.2
        have hz := JointCompletion.sigma_elimination c a.2.laws b.2.laws p.2.laws hd z.2
        simpa only [translate_inst] using And.intro (And.intro c hh) hz
    | natInduction hΓ hP hp hs c p seed step =>
        have hP := p.2
        have hp := seed.2
        have hs := step.2
        simp only [translateTel, List.map_cons, translate_N] at hP
        simp only [translate_inst] at hp
        simp only [translate_dependentStepType] at hs
        simpa only [translate, translate_N] using
          And.intro (And.intro c ⟨type_pi c (JointCompletion.nat_laws _) hP.laws,
            JointCompletion.hereditary_nat c,hP⟩)
            (JointCompletion.dependent_induction c hP.laws hp hs)
theorem fundamental {Γ p A} (h : JointCompletion.HasJ Γ p A) :
    FullPER.Fundamental (translateTel Γ) p (translate A) := (has_sound h).2

theorem form_sound {Γ A} (h : JointCompletion.FormJ Γ A) :
    FullPER.FormSound (translateTel Γ) (translate A) := by
  have hf : JointCompletion.FormJ Γ (arr A A) :=
    .pi h (JointCompletion.Structural.form_wk h (JointCompletion.Structural.form_ctx h) h)
  have hh := (has_sound (JointCompletion.HasJ.i h hf)).1
  exact ⟨hh.1,hh.2.2.1⟩

theorem context_sound {Γ} (h : JointCompletion.CtxJ Γ) :
    FullPER.ContextLaws (translateTel Γ) := (form_sound (.raw h)).1

#print axioms base_form_sound
#print axioms base_has_sound
#print axioms form_sound
#print axioms context_sound
#print axioms has_sound
#print axioms fundamental
end JointRawTop
