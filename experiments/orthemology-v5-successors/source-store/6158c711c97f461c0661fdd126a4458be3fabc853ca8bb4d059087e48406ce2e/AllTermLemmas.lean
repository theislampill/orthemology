/- Fundamental-rule lemmas. Inputs are smaller induction conclusions only. -/
import AllSigmaLaws
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem fundamental_var {Γ n A} (v : Lookup Γ n A) : Fundamental Γ (.var n) A := by
  intro r η ξ h
  induction v generalizing η ξ with
  | @zero A Γ =>
      have hh := h.2
      rw [← cons_head_tail η,← cons_head_tail ξ, G_wk]
      exact hh
  | @succ Γ n A B v ih =>
      rw [← cons_head_tail η,← cons_head_tail ξ,G_wk]
      exact ih (tail η) (tail ξ) h.1

theorem fundamental_pi_intro {Γ A B b} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) (ht : Fundamental (A :: Γ) b B) :
    Fundamental Γ (abstract b) (.pi A B) := by
  intro r η ξ h
  have ds := hc.hends h
  have cc := context_ext hc ha
  refine ⟨?_,?_,?_⟩
  · intro a a' aa
    have e : E (A :: Γ) r.left (cons a η) (cons a' η) := ⟨hc.refl ds.1,aa⟩
    have v := ht.unary cc hb e
    exact (hb.per (cc.ends e).1).raw
      (P01Source.red_conv (abstraction_beta b η a)).symm
      (P01Source.red_conv (abstraction_beta b η a')).symm v
  · intro a a' aa
    have e : E (A :: Γ) r.right (cons a ξ) (cons a' ξ) := ⟨hc.refl ds.2,aa⟩
    have v := ht.unary cc hb e
    exact (hb.per (cc.ends e).1).raw
      (P01Source.red_conv (abstraction_beta b ξ a)).symm
      (P01Source.red_conv (abstraction_beta b ξ a')).symm v
  · intro a a' aa
    have he : H (A :: Γ) r (cons a η) (cons a' ξ) := ⟨h,aa⟩
    have dd := cc.hends he
    exact hb.raw dd.1 dd.2
      (P01Source.red_conv (abstraction_beta b η a)).symm
      (P01Source.red_conv (abstraction_beta b ξ a')).symm (ht r _ _ he)

theorem fundamental_pi_elim {Γ A B f a} (hf : Fundamental Γ f (.pi A B))
    (ha : Fundamental Γ a A) : Fundamental Γ (.app f a) (inst B a) := by
  intro r η ξ h
  rw [G_inst]
  exact (hf r η ξ h).2.2 _ _ (ha r η ξ h)

theorem F_pair {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) {ρ η a a' b b'} (d : D Γ ρ η)
    (aa : F A ρ η a a') (bb : F B ρ (cons a η) b b') :
    F (.sigma A B) ρ η (pairTerm a b) (pairTerm a' b') := by
  have la := ha.per d
  have e : E (A :: Γ) ρ (cons a η) (cons (firstTerm (pairTerm a b)) η) :=
    ⟨hc.refl d,la.raw (.refl _) (pair_first a b).symm (la.left aa)⟩
  exact ⟨pair_represented a b,pair_represented a' b',
    la.raw (pair_first a b).symm (pair_first a' b').symm aa,
    (hb.transport e _ _).mp ((hb.per ⟨d,la.left aa⟩).raw (pair_second a b).symm (pair_second a' b').symm bb)⟩

theorem G_pair {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) {r η ξ a a' b b'} (dη : D Γ r.left η) (dξ : D Γ r.right ξ)
    (aa : G A r η ξ a a') (bb : G B r (cons a η) (cons a' ξ) b b') :
    G (.sigma A B) r η ξ (pairTerm a b) (pairTerm a' b') := by
  have da := ha.ends dη dξ aa
  have db := hb.ends ⟨dη,da.1⟩ ⟨dξ,da.2⟩ bb
  have ea : E (A :: Γ) r.left (cons a η) (cons (firstTerm (pairTerm a b)) η) :=
    ⟨hc.refl dη,(ha.per dη).raw (.refl _) (pair_first a b).symm da.1⟩
  have eb : E (A :: Γ) r.right (cons a' ξ) (cons (firstTerm (pairTerm a' b')) ξ) :=
    ⟨hc.refl dξ,(ha.per dξ).raw (.refl _) (pair_first a' b').symm da.2⟩
  exact ⟨F_pair hc ha hb dη da.1 db.1,F_pair hc ha hb dξ da.2 db.2,
    pair_represented a b,pair_represented a' b',
    ha.raw dη dξ (pair_first a b).symm (pair_first a' b').symm aa,
    (hb.invariant ea eb _ _).mp
      (hb.raw ⟨dη,da.1⟩ ⟨dξ,da.2⟩ (pair_second a b).symm (pair_second a' b').symm bb)⟩

theorem fundamental_sigma_intro {Γ A B a b} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) (hta : Fundamental Γ a A) (htb : Fundamental Γ b (inst B a)) :
    Fundamental Γ (pairPoly a b) (.sigma A B) := by
  intro r η ξ h
  have dd := hc.hends h
  have vb := htb r η ξ h
  rw [G_inst] at vb
  exact G_pair hc ha hb dd.1 dd.2 (hta r η ξ h) vb

theorem fundamental_sigma_fst {Γ A B z} (hz : Fundamental Γ z (.sigma A B)) :
    Fundamental Γ (fstPoly z) A := fun r η ξ h => (hz r η ξ h).2.2.2.2.1

theorem fundamental_sigma_snd {Γ A B z} (hz : Fundamental Γ z (.sigma A B)) :
    Fundamental Γ (sndPoly z) (inst B (fstPoly z)) := by
  intro r η ξ h
  rw [G_inst]
  exact (hz r η ξ h).2.2.2.2.2

theorem fundamental_identity_intro {Γ A p q} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hp : Fundamental Γ p A) (pq : P01DF.PolyConv p q) :
    Fundamental Γ (.atom .i) (.identity A p q) := by
  intro r η ξ h
  have dd := hc.hends h
  have pp := ha.ends dd.1 dd.2 (hp r η ξ h)
  exact ⟨(ha.per dd.1).raw (.refl _) (P01DF.polyConv_sound pq η) pp.1,
    (ha.per dd.2).raw (.refl _) (P01DF.polyConv_sound pq ξ) pp.2,.refl _,.refl _⟩

theorem fundamental_proof_erase {Γ A x y p} (hp : Fundamental Γ p (.identity A x y)) :
    Fundamental Γ p .raw := by
  intro r η ξ h
  have v := hp r η ξ h
  exact v.2.2.1.trans v.2.2.2.symm

theorem fundamental_j {Γ A B x y e d} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (theta Γ A x) B) (ht : TypeLaws Γ (motiveAt B y e))
    (he : Fundamental Γ e (.identity A x y)) (hd : Fundamental Γ d (motiveAt B x (.atom .i))) :
    Fundamental Γ (jPoly d y e) (motiveAt B y e) := by
  intro r η ξ h
  have ds := hc.hends h
  have ep := he r η ξ h
  have makeE : ∀ {ρ η}, D Γ ρ η → F A ρ η (eval x η) (eval y η) → Conv (eval e η) .i →
      E (theta Γ A x) ρ (cons .i (cons (eval x η) η)) (cons (eval e η) (cons (eval y η) η)) := by
    intro ρ η dη xy ei
    refine ⟨⟨hc.refl dη,xy⟩,?_⟩
    change F (wk A) ρ (cons (eval x η) η) (eval (pren Nat.succ x) (cons (eval x η) η))
      (eval x η) ∧ Conv Term.i Term.i ∧ Conv (eval e η) Term.i
    rw [eval_ren,F_wk]
    exact ⟨(ha.per dη).left xy,.refl _,ei⟩
  have el := makeE ds.1 ep.1 ep.2.2.1
  have er := makeE ds.2 ep.2.1 ep.2.2.2
  have db := hd r η ξ h
  rw [G_motiveAt] at db
  have tr := (hb.invariant el er _ _).mp db
  have goalrel : G (motiveAt B y e) r η ξ (eval d η) (eval d ξ) := by
    rw [G_motiveAt]; exact tr
  exact ht.raw ds.1 ds.2 (P01Source.red_conv (eval_j d y e η)).symm
    (P01Source.red_conv (eval_j d y e ξ)).symm goalrel

end P01AC
