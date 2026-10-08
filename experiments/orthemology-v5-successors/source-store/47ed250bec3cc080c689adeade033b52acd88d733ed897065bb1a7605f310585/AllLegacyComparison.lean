/- Full unary and heterogeneous old-model comparison, jointly structural through All. -/
import AllLegacyDerivations
import AllSoundness
namespace P01AC.Legacy
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- Unary agreement holds at every valuation; heterogeneous agreement uses the
actual pointwise-Conv-related pair. All uniformity invokes the smaller G result. -/
theorem FG_agrees (A : P01DF.Ty) :
    (∀ ρ η t u, F (translate A) ρ η t u = (((P01DF.interpret A).run η).obj ρ).rel t u) ∧
    (∀ r η ξ, P01DF.IndexRelated η ξ → ∀ t u,
      G (translate A) r η ξ t u = ((P01DF.interpret A).run η).rel r t u) := by
  induction A with
  | param n => exact ⟨fun _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | bottom => exact ⟨fun _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | raw => exact ⟨fun _ _ _ _ => rfl, fun _ _ _ _ _ _ => rfl⟩
  | identity p q =>
      refine ⟨fun _ _ _ _ => rfl, ?_⟩
      intro r η ξ hc t u
      apply propext
      change (Conv (eval p η) (eval q η) ∧ Conv (eval p ξ) (eval q ξ) ∧
        Conv t .i ∧ Conv u .i) ↔ (Conv (eval p η) (eval q η) ∧ Conv t .i ∧ Conv u .i)
      constructor
      · intro h; exact ⟨h.1,h.2.2⟩
      · intro h
        exact ⟨h.1,(P01DF.eval_index_related p hc).symm.trans
          (h.1.trans (P01DF.eval_index_related q hc)),h.2⟩
  | arrow A B ha hb =>
      constructor
      · intros; simp only [translate,F_arr,ha.1,hb.1,P01DF.interpret,arrowModel,ArrPER,PiPER]
      · intro r η ξ hc t u
        simp only [translate,G_arr,ha.1,hb.1,ha.2 r η ξ hc,hb.2 r η ξ hc,
          P01DF.interpret,arrowModel,arrowLink,Model.asLink,PER.dom,ArrPER,PiPER]
        rw [← P01DF.interpret_index_transport A hc,← P01DF.interpret_index_transport B hc]
  | pi B ih =>
      have fo : ∀ ρ η t u, F (translate (.pi B)) ρ η t u =
          (((P01DF.interpret (.pi B)).run η).obj ρ).rel t u := by
        intros; simp only [translate,F_pi,F_raw,ih.1,P01DF.interpret,P01DF.piModel,PiPER,rawPER]
      refine ⟨fo, ?_⟩
      intro r η ξ hc t u
      change G (.pi .raw (translate B)) r η ξ t u = _
      rw [G_pi]
      rw [show F (.pi .raw (translate B)) r.left η t t =
        (((P01DF.interpret (.pi B)).run η).obj r.left).rel t t from fo _ _ _ _]
      rw [show F (.pi .raw (translate B)) r.right ξ u u =
        (((P01DF.interpret (.pi B)).run ξ).obj r.right).rel u u from fo _ _ _ _]
      rw [← P01DF.interpret_index_transport (.pi B) hc]
      apply propext
      constructor
      · intro h
        refine ⟨h.1,h.2.1,?_⟩
        intro a b hab
        exact (ih.2 r (cons a η) (cons b ξ) (P01DF.index_cons hc hab) _ _) ▸ h.2.2 a b hab
      · intro h
        refine ⟨h.1,h.2.1,?_⟩
        intro a b hab
        exact (ih.2 r (cons a η) (cons b ξ) (P01DF.index_cons hc hab) _ _).symm ▸ h.2.2 a b hab
  | sigma B ih =>
      have fo : ∀ ρ η t u, F (translate (.sigma B)) ρ η t u =
          (((P01DF.interpret (.sigma B)).run η).obj ρ).rel t u := by
        intros; simp only [translate,F_sigma,F_raw,ih.1,P01DF.interpret,P01DF.sigmaModel,SigmaPER,rawPER]
      refine ⟨fo, ?_⟩
      intro r η ξ hc t u
      change G (.sigma .raw (translate B)) r η ξ t u = _
      rw [G_sigma]
      rw [show F (.sigma .raw (translate B)) r.left η t t =
        (((P01DF.interpret (.sigma B)).run η).obj r.left).rel t t from fo _ _ _ _]
      rw [show F (.sigma .raw (translate B)) r.right ξ u u =
        (((P01DF.interpret (.sigma B)).run ξ).obj r.right).rel u u from fo _ _ _ _]
      rw [← P01DF.interpret_index_transport (.sigma B) hc]
      apply propext
      constructor
      · intro h
        refine ⟨h.2.2.1,h.2.2.2.1,h.2.2.2.2.1,?_⟩
        exact (ih.2 r (cons (firstTerm t) η) (cons (firstTerm u) ξ)
          (P01DF.index_cons hc h.2.2.2.2.1) _ _) ▸ h.2.2.2.2.2
      · intro h
        have he := ((P01DF.interpret (.sigma B)).run η).endpoints r h
        refine ⟨he.1,he.2,h.1,h.2.1,h.2.2.1,?_⟩
        exact (ih.2 r (cons (firstTerm t) η) (cons (firstTerm u) ξ)
          (P01DF.index_cons hc h.2.2.1) _ _).symm ▸ h.2.2.2
  | all B ih =>
      have fo : ∀ ρ η t u, F (translate (.all B)) ρ η t u =
          (((P01DF.interpret (.all B)).run η).obj ρ).rel t u := by
        intro ρ η t u
        simp only [translate,F_all,ih.1,ih.2 _ η η (P01DF.index_refl η),
          P01DF.interpret,allModel,AllPER,Parametric,bodyFamily,Model.asLink]
      refine ⟨fo, ?_⟩
      intro r η ξ hc t u
      change G (.all (translate B)) r η ξ t u = _
      rw [G_all]
      rw [show F (.all (translate B)) r.left η t t =
        (((P01DF.interpret (.all B)).run η).obj r.left).rel t t from fo _ _ _ _]
      rw [show F (.all (translate B)) r.right ξ u u =
        (((P01DF.interpret (.all B)).run ξ).obj r.right).rel u u from fo _ _ _ _]
      rw [← P01DF.interpret_index_transport (.all B) hc]
      simp only [ih.2 _ η ξ hc,P01DF.interpret,allModel,PER.dom]

theorem F_agrees (A : P01DF.Ty) (ρ : OEnv) (η : Env) (t u : Term) :
    F (translate A) ρ η t u = (((P01DF.interpret A).run η).obj ρ).rel t u :=
  (FG_agrees A).1 ρ η t u

theorem G_agrees (A : P01DF.Ty) (r : REnv) (η ξ : Env) (hc : P01DF.IndexRelated η ξ) (t u : Term) :
    G (translate A) r η ξ t u = ((P01DF.interpret A).run η).rel r t u :=
  (FG_agrees A).2 r η ξ hc t u

theorem Supported.object_agrees {n p A} {h : Derivation p A} (hs : Supported n h)
    {ρ : OEnv} {η : Env} (d : D (rawTel n) ρ η) :
    objectOf (form_sound (has_form hs.raw_embed)).2.laws d = ((P01DF.interpret A).run η).obj ρ := by
  apply per_ext
  intro t u
  exact Iff.of_eq (F_agrees A ρ η t u)

theorem Supported.heterogeneous_agrees {n p A} {h : Derivation p A} (_hs : Supported n h)
    (r : REnv) (η ξ : Env) (hc : P01DF.IndexRelated η ξ) (t u : Term) :
    G (translate A) r η ξ t u = ((P01DF.interpret A).run η).rel r t u :=
  G_agrees A r η ξ hc t u

end P01AC.Legacy
