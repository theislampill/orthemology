import Boundary
namespace IndependentSigmaReview
open P01AC P01D P01AC.ExtensionalRepair
open OpenTermStandardness (T Conv SatPER)
open TaggedPER SigmaTagBoundary

theorem sigma_formed {Γ} (hc : CtxE Γ) : FormE Γ SigmaRaw :=
  .sigma (.raw hc) (.raw (.ext hc (.raw hc)))

theorem eta_formed {Γ} (hc : CtxE Γ) : FormE Γ Eta := by
  have hs := sigma_formed hc
  have c := CtxE.ext hc hs
  have hs' := sigma_formed c
  have hz : HasE (SigmaRaw :: Γ) (.var 0) SigmaRaw := .var hs' .zero
  have hf : HasE (SigmaRaw :: Γ) (fstPoly (.var 0)) .raw := .sigmaFst (.raw c) hs' hz
  have hg : HasE (SigmaRaw :: Γ) (sndPoly (.var 0)) .raw := .sigmaSnd hs' (.raw c) hz
  have hp := HasE.sigmaIntro hs' (.raw c) hf hg
  exact .pi hs (.identity hs' hz hp)

theorem conditional_formed : FormE [] (arr SourceRigidity.Rigidity Eta) := by
  have hr := form_inclusion (SourceRigidity.rigidity_formed Ctx.nil)
  exact .pi hr (eta_formed (.ext .nil hr))

theorem pair_inhabited : HasE [] (pairPoly (.atom .k) (.atom .i)) SigmaRaw :=
  .sigmaIntro (sigma_formed .nil) (.raw .nil) (.rawAtom (.raw .nil)) (.rawAtom (.raw .nil))

theorem negation_conditional_formed :
    FormE [] (arr SourceRigidity.Rigidity (arr Eta .bottom)) := by
  have hr := form_inclusion (SourceRigidity.rigidity_formed Ctx.nil)
  have cr := CtxE.ext .nil hr
  have he := eta_formed cr
  exact .pi hr (.pi he (.bottom (.ext cr he)))

theorem raw_exact (ρ η) : TaggedPER.F .raw ρ η = Conv := rfl
theorem all_exact (B ρ η u v) :
    TaggedPER.F (.all B) ρ η u v ↔ ∀ P : SatPER, TaggedPER.F B (cons P.rel ρ) η u v := Iff.rfl

theorem same_projections (ρ η) :
    TaggedPER.F .raw ρ η (first T.i) (first (pair T.k (T.k ⬝ T.i))) ∧
    TaggedPER.F .raw ρ η (second T.i) (second (pair T.k (T.k ⬝ T.i))) :=
  ⟨(Conv.i _).trans (OpenTermStandardness.fst_pair _ _).symm,
   (Conv.i _).trans (OpenTermStandardness.snd_pair _ _).symm⟩

theorem nonetheless_distinct (ρ η) :
    ¬ TaggedPER.F SigmaRaw ρ η T.i (pair T.k (T.k ⬝ T.i)) := by
  intro h
  exact ghost_not_tag (h.2.2.mpr (tag_pair _ _))

theorem canonical_eta (ρ η a b) :
    TaggedPER.F etaBody ρ (cons (pair a b) η) T.i T.i := by
  have h := tag_pair a b
  exact ⟨⟨(OpenTermStandardness.fst_congr h),
    (OpenTermStandardness.snd_congr h),tag_congr h⟩,.refl _,.refl _⟩

theorem old_model_eta_at_ghost (ρ η) :
    FullPER.F etaBody ρ (cons T.i η) T.i T.i :=
  ⟨⟨(OpenTermStandardness.fst_pair _ _).symm,
    (OpenTermStandardness.snd_pair _ _).symm⟩,.refl _,.refl _⟩

theorem pi_all_rigidity_preserved (ρ η) :
    TaggedPER.F SourceRigidity.Rigidity ρ η = FullPER.F SourceRigidity.Rigidity ρ η := rfl

#print axioms pair_inhabited
#print axioms negation_conditional_formed
#print axioms eta_formed
#print axioms conditional_formed
#print axioms canonical_eta
#print axioms old_model_eta_at_ghost
#print axioms TaggedPER.fundamental
#print axioms SigmaTagBoundary.no_rigidity_to_eta
end IndependentSigmaReview
