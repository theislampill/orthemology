import RawContextUniformity

/- An isolated syntactic context fragment, with its relational properties proved
   rather than required as context hypotheses. No source rule is changed. -/
namespace StructuredContextUniformity
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody iterationPoly inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv SatPER)
open ImportedOpenTermTransport (interp)
open RawContextUniformity (observe truncate)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Types whose interpretation can only relate Raw-convertible representatives.
    Identity endpoints and their carrier are unrestricted source syntax. -/
inductive Rigid : Ty → Prop
  | raw : Rigid .raw
  | bottom : Rigid .bottom
  | identity (B : Ty) (p q : Poly) : Rigid (.identity B p q)
  | all {B : Ty} : Rigid B → Rigid (.all B)

/-- Types admitting every Raw-convertible pair. The Pi domain is contravariant;
    arbitrary higher-order domains are deliberately not a constructor. -/
inductive Opaque : Ty → Prop
  | raw : Opaque .raw
  | pi {D B : Ty} : Rigid D → Opaque B → Opaque (.pi D B)
  | sigma {D B : Ty} : Opaque D → Opaque B → Opaque (.sigma D B)
  | all {B : Ty} : Opaque B → Opaque (.all B)
  | emptyPi (B : Ty) : Opaque (.pi .bottom B)

theorem rigid_reflects {B : Ty} (hB : Rigid B) (ρ : FullPER.REnv)
    (η : FullPER.Env) {u v : T} (h : FullPER.F B ρ η u v) : Conv u v := by
  induction hB generalizing ρ η u v with
  | raw => exact h
  | bottom => exact False.elim h
  | identity B p q => exact h.2.1.trans h.2.2.symm
  | all hB ih => exact ih _ _ (h (OpenTermStandardness.orbit .i .i))

theorem opaque_admits {B : Ty} (hB : Opaque B) (ρ : FullPER.REnv)
    (η : FullPER.Env) {u v : T} (h : Conv u v) : FullPER.F B ρ η u v := by
  induction hB generalizing ρ η u v with
  | raw => exact h
  | pi hD hB ih =>
    intro x y hxy
    exact ih _ _ (.app h (rigid_reflects hD ρ η hxy))
  | sigma hD hB ihD ihB =>
    exact ⟨ihD _ _ (.app h (.refl _)), ihB _ _ (.app h (.refl _))⟩
  | all hB ih => intro P; exact ih _ _ h
  | emptyPi B => intro x y hxy; exact False.elim hxy

def OpaqueTel (Γ : Tel) : Prop := ∀ B ∈ Γ, Opaque B

theorem truncated_admissible {Γ : Tel} (hΓ : OpaqueTel Γ)
    (η : FullPER.Env) (ρ : FullPER.REnv) :
    FullPER.E Γ ρ (truncate Γ.length η) (truncate Γ.length η) := by
  induction Γ generalizing η with
  | nil =>
    have hz : truncate 0 η = FullPER.zeroEnv := by
      funext j; simp [truncate,FullPER.zeroEnv]
    exact ⟨hz,hz⟩
  | cons B Γ ih =>
    have ht : FullPER.tail (truncate (Γ.length+1) η) =
        truncate Γ.length (fun j => η (j+1)) := by
      funext j; simp [FullPER.tail,truncate]
    exact ⟨by simp only [List.length_cons,ht]; exact ih (fun D hD => hΓ D (by simp [hD])) _,
      opaque_admits (hΓ B (by simp)) _ _ (.refl _)⟩

theorem opaque_church {Γ : Tel} {n : Poly} (hΓ : OpaqueTel Γ)
    (hn : HasE Γ n N) (η : FullPER.Env) : OpenTermStandardness.Church (interp n η) := by
  have hs := ClosedProofCanonicalisation.has_scope hn
  rw [RawContextUniformity.interp_agree hs η (truncate Γ.length η)
    (by intro j hj; simp [truncate,hj])]
  exact FullPER.fundamental hn FullPER.Application.emptyEnv _ _
    FullPER.Application.emptyEnv_admissible (truncated_admissible hΓ η _)

theorem opaque_uniform_iteration {Γ : Tel} {n : Poly}
    (hΓ : OpaqueTel Γ) (hn : HasE Γ n N) :
    ∃ k, PolyConvPlus (observe n) (iterationPoly k) := by
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard _
    (opaque_church hΓ hn (fun j => .var (j+2)))
  refine ⟨k,ClosedScalarInstances.generic_conversion_reflect ?_⟩
  simp only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    ClosedScalarInstances.iteration_interp]
  exact hk (.var 1) (.var 0)

/-- Source formations need only the actual extended context grammar. -/
theorem formEnd {Γ : Tel} (hΓ : CtxE Γ) : FormE Γ End :=
  .pi (.param hΓ) (.param (.ext hΓ (.param hΓ)))
theorem formBody {Γ : Tel} (hΓ : CtxE Γ) : FormE Γ NBody :=
  .pi (formEnd hΓ) (formEnd (.ext hΓ (formEnd hΓ)))
theorem formN {Γ : Tel} (hΓ : CtxE Γ) : FormE Γ N :=
  .all hΓ (formBody (Structural.ctx_twk hΓ))
theorem body_of_N {Γ : Tel} {n : Poly} (hΓ : CtxE Γ) (hn : HasE Γ n N) :
    HasE Γ n NBody :=
  .allElim (formN hΓ) (.param hΓ) (formBody hΓ) hn

def point (n : Poly) : Poly := .app (pren Nat.succ n) (.var 0)

theorem point_has {Γ : Tel} {n : Poly} (hΓ : CtxE Γ) (hn : HasE Γ n N) :
    HasE (End :: Γ) (point n) End := by
  have hE := formEnd hΓ
  have hΓ1 : CtxE (End :: Γ) := .ext hΓ (formEnd hΓ)
  have hw := Structural.has_wk hn hΓ hE
  have hwN : HasE (End :: Γ) (pren Nat.succ n) N := by
    simpa [wk,subst,N,NBody,End,A,arr] using hw
  exact .piElim (formBody hΓ1)
    (formEnd hΓ1) (body_of_N hΓ1 hwN)
    (.var (formEnd hΓ1) .zero)

theorem observation_has {Γ : Tel} {n : Poly} (hΓ : CtxE Γ) (hn : HasE Γ n N) :
    HasE (A :: End :: Γ) (observe n) A := by
  have hΓ1 : CtxE (End :: Γ) := .ext hΓ (formEnd hΓ)
  have hΓ2 : CtxE (A :: End :: Γ) := .ext hΓ1 (.param hΓ1)
  have hw := Structural.has_wk (B := A) (point_has hΓ hn) hΓ1
    (.param hΓ1)
  have hwE : HasE (A :: End :: Γ) (pren Nat.succ (point n)) End := by
    simpa [wk,subst,End,A,arr] using hw
  have hp : HasE (A :: End :: Γ) (.app (pren Nat.succ (point n)) (.var 0)) A :=
    .piElim (formEnd hΓ2) (.param hΓ2) hwE
      (.var (.param hΓ2) .zero)
  simpa only [point,observe,pren,psub] using hp

/-- The two source Pi extensionality steps in any actual CtxE context. -/
theorem body_identity_of_observation {Γ : Tel} {p q : Poly}
    (hΓ : CtxE Γ)
    (hp : HasE Γ p N) (hq : HasE Γ q N)
    (hc : PolyConvPlus (observe p) (observe q)) :
    HasE Γ i (.identity NBody p q) := by
  have hΓ1 : CtxE (End :: Γ) := .ext hΓ (formEnd hΓ)
  have hΓ2 : CtxE (A :: End :: Γ) := .ext hΓ1 (.param hΓ1)
  have sp := ClosedProofCanonicalisation.has_scope hp
  have sq := ClosedProofCanonicalisation.has_scope hq
  have hp1 := point_has hΓ hp
  have hq1 := point_has hΓ hq
  have hp2 := observation_has hΓ hp
  have hq2 := observation_has hΓ hq
  have hf2 : FormE (A :: End :: Γ) (.identity A (observe p) (observe q)) :=
    .identity (.param hΓ2) hp2 hq2
  have hi2 : HasE (A :: End :: Γ) i (.identity A (observe p) (observe q)) :=
    .identityIntro hf2 hp2 hq2 hc
  have ep : .app (pren Nat.succ (point p)) (.var 0) = observe p := rfl
  have eq : .app (pren Nat.succ (point q)) (.var 0) = observe q := rfl
  have hfpi : FormE (End :: Γ) (.pi A (.identity A (observe p) (observe q))) :=
    .pi (.param hΓ1) hf2
  have hhpi : HasE (End :: Γ) (abstract i)
      (.pi A (.identity A (observe p) (observe q))) :=
    .piIntro hfpi hi2 (scoped_abstract trivial)
  have hi1 : HasE (End :: Γ) i (.identity End (point p) (point q)) := by
    apply HasE.piExt (.param hΓ1) (.param hΓ2)
      (formEnd hΓ1) hp1 hq1
    · simpa only [ep,eq] using hf2
    · simpa only [ep,eq] using hfpi
    · simpa only [ep,eq] using hhpi
    · exact .identity (formEnd hΓ1) hp1 hq1
    · exact ClosedProofCanonicalisation.has_scope hp1
    · exact ClosedProofCanonicalisation.has_scope hq1
    · exact scoped_abstract trivial
    · trivial
    · trivial
  have hp0 := body_of_N hΓ hp
  have hq0 := body_of_N hΓ hq
  have hf1 : FormE (End :: Γ) (.identity End (point p) (point q)) :=
    .identity (formEnd hΓ1) hp1 hq1
  have hf0 : FormE Γ (.pi End (.identity End (point p) (point q))) :=
    .pi (formEnd hΓ) hf1
  have hh0 : HasE Γ (abstract i) (.pi End (.identity End (point p) (point q))) :=
    .piIntro hf0 hi1 (scoped_abstract trivial)
  have hi0 : HasE Γ i (.identity NBody p q) := by
    apply HasE.piExt (formEnd hΓ) (formEnd hΓ1)
      (formBody hΓ) hp0 hq0
    · exact hf1
    · exact hf0
    · exact hh0
    · exact .identity (formBody hΓ) hp0 hq0
    · exact sp
    · exact sq
    · exact scoped_abstract trivial
    · exact ⟨trivial,trivial⟩
    · exact ⟨trivial,trivial⟩
  exact hi0

/-- Type weakening, rather than a fixed-telescope premise, discharges allExt.
    No endpoint conversion is inferred from typing alone. -/
theorem identity_of_observation {Γ : Tel} {p q : Poly}
    (hp : HasE Γ p N) (hq : HasE Γ q N)
    (hc : PolyConvPlus (observe p) (observe q)) :
    HasE Γ i (.identity N p q) := by
  have hΓ := Structural.form_ctx (ClosedProofCanonicalisation.formed hp)
  have hΔ := Structural.ctx_twk hΓ
  have hp' : HasE (twkTel Γ) p N := by
    simpa [twk,trename,N,NBody,End,A,arr] using Structural.has_twk hp
  have hq' : HasE (twkTel Γ) q N := by
    simpa [twk,trename,N,NBody,End,A,arr] using Structural.has_twk hq
  exact .allExt (formBody hΔ) (formN hΓ) hp hq
    (.identity (formBody hΔ) (body_of_N hΔ hp') (body_of_N hΔ hq'))
    (body_identity_of_observation hΔ hp' hq' hc)
    (.identity (formN hΓ) hp hq)
    (ClosedProofCanonicalisation.has_scope hp) (ClosedProofCanonicalisation.has_scope hq)
    trivial ⟨⟨trivial,trivial⟩,⟨trivial,trivial⟩⟩

theorem opaque_canonicity_at_count {Γ : Tel} {n : Poly} {k : Nat}
    (hn : HasE Γ n N) (hk : PolyConvPlus (observe n) (iterationPoly k)) :
    HasE Γ i (.identity N n (inputNumeral k)) :=
  identity_of_observation hn
    (Structural.has_closed (has_inclusion (EffectiveCompleteness.inputNumeral_has k))
      (Structural.form_ctx (ClosedProofCanonicalisation.formed hn)))
    (hk.trans (RawContextUniformity.numeral_observation k).symm)

/-- One actual source identity for every source-typed Church term over a
    syntactically opaque structured telescope. No semantic bridge is a premise. -/
theorem opaque_canonicity {Γ : Tel} {n : Poly}
    (hΓ : OpaqueTel Γ) (hn : HasE Γ n N) :
    ∃ k, HasE Γ i (.identity N n (inputNumeral k)) := by
  obtain ⟨k,hk⟩ := opaque_uniform_iteration hΓ hn
  exact ⟨k,opaque_canonicity_at_count hn hk⟩

theorem opaque_uniform_substitutions {Γ : Tel} {n : Poly}
    (hΓ : OpaqueTel Γ) (hn : HasE Γ n N) :
    ∃ k, HasE Γ i (.identity N n (inputNumeral k)) ∧
      ∀ σ : Nat → Poly, PolyConvPlus (observe (psub σ n)) (iterationPoly k) := by
  obtain ⟨k,hk⟩ := opaque_uniform_iteration hΓ hn
  refine ⟨k,opaque_canonicity_at_count hn hk,?_⟩
  intro σ
  simpa only [RawContextUniformity.observe_subst,RawContextUniformity.iteration_subst] using
    Structural.polyConvPlus_subst hk (pup (pup σ))

/-- The same count works at every valuation, even valuations not respecting
    the source structured types. This is an evaluation claim, not new typing. -/
theorem opaque_uniform_evaluation {Γ : Tel} {n : Poly}
    (hΓ : OpaqueTel Γ) (hn : HasE Γ n N) :
    ∃ k, ∀ (η : FullPER.Env) (f a : T),
      Conv ((interp n η).app f |>.app a) (OpenTermStandardness.iter f a k) := by
  obtain ⟨k,hk⟩ := opaque_uniform_iteration hΓ hn
  refine ⟨k,?_⟩
  intro η f a
  have h := ImportedOpenTermTransport.source_plus_sound hk
    (OpenTermStandardness.cons a (OpenTermStandardness.cons f η))
  rw [ClosedChurchIdentity.interp_iteration] at h
  simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    OpenTermStandardness.cons] using h

#print axioms rigid_reflects
#print axioms opaque_admits
#print axioms opaque_uniform_iteration
#print axioms identity_of_observation
#print axioms opaque_canonicity
#print axioms opaque_uniform_substitutions
#print axioms opaque_uniform_evaluation
end StructuredContextUniformity
