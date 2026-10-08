/- Independent literal import and genuinely varying mixed-image controls. -/
import AllJoinedControls
import AllMixedRepresentation
import AllNucleus

namespace P01AC.IndependentMixed
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def varyingMap : MixedSub [.raw] [] [] [rawFibreType] := by
  refine ⟨.nil (.ext .nil (.raw .nil)),?_⟩
  intro n hn
  cases n with
  | zero => exact raw_fibre_form
  | succ n => simp only [List.length_cons,List.length_nil] at hn; omega

theorem raw_valid (ρ : OEnv) (x : Term) : D [.raw] ρ (cons x zeroEnv) :=
  ⟨rfl,.refl _⟩

/-- The parameter environment installed by the mixed map actually changes
    with the target term valuation; this is stronger than syntactic openness. -/
theorem image_objects_really_vary (ρ : OEnv) :
    varyingMap.imageObjects ρ (cons .i zeroEnv) (raw_valid ρ .i) ≠
    varyingMap.imageObjects ρ (cons P01DF.skk zeroEnv) (raw_valid ρ P01DF.skk) := by
  intro h
  have he := congrArg (fun env : OEnv => (env 0).rel (pairTerm .i .i) (pairTerm .i .i)) h
  exact (raw_fibres_nonempty_and_vary ρ).2.2 (Eq.mp he (raw_fibres_nonempty_and_vary ρ).1)

theorem mixed_intrinsic_tracks_every_index (ρ : OEnv)
    (η : (representedContext [.raw] ρ (context_sound varyingMap.target)).Val) (n : Nat) :
    (jointContext [] (context_sound varyingMap.source)).environment
      ((representedMixedSub varyingMap ρ).map η) n = .zero := rfl

def applicationProof : FiniteDerives (.app .i .i) (.arrow (.var 0) (.var 0)) :=
  .app (.i (.arrow (.var 0) (.var 0))) (.i (.var 0))

/-- The finite proof's opaque source application remains a single atom. -/
theorem literal_application_atom_import :
    Has [] (.atom (.app .i .i)) (arr (.param 0) (.param 0)) :=
  finite_import .nil applicationProof

/-- Open contextual type substitution preserves that same opaque atom. -/
theorem literal_application_atom_open_instance :
    Has [.raw] (.atom (.app .i .i)) (arr rawFibreType rawFibreType) := by
  have hh := varyingMap.has literal_application_atom_import
  simpa only [mixed_arr,mixed,images,psub,typeImages,cons] using hh

theorem exact_nucleus_import (h : P01TC.Has [] (.atom (.app .i .i))
    (P01TC.arr (.param 0) (.param 0))) :
    Has [] (.atom (.app .i .i)) (arr (.param 0) (.param 0)) := Nucleus.has h

def unequalEndpoints : H [alpha] Negative.rightSeparating
    (cons P01DF.skk zeroEnv) (cons .i zeroEnv) := ⟨⟨rfl,rfl⟩,trivial⟩

theorem nonempty_unequal_endpoint_replacement :
    G typedPairType Negative.rightSeparating (cons P01DF.skk zeroEnv) (cons .i zeroEnv)
      (pairTerm P01DF.skk .i) (pairTerm .i .i) :=
  fundamental typed_pair_has _ _ _ unequalEndpoints

theorem unequal_endpoint_replacement_really_differs :
    F typedPairType Negative.rightSeparating.left (cons P01DF.skk zeroEnv)
      (pairTerm P01DF.skk .i) (pairTerm P01DF.skk .i) ∧
    ¬ F typedPairType Negative.rightSeparating.right (cons .i zeroEnv)
      (pairTerm P01DF.skk .i) (pairTerm P01DF.skk .i) := by
  refine ⟨nonempty_unequal_endpoint_replacement.1,?_⟩
  intro h
  exact P01Source.I_SKK_not_convertible (h.2.2.2.1.trans (pair_first _ _))

/-- The actual polymorphic elimination result acts on the nonempty Link with
    unequal replacement endpoint PERs; it is not a same-endpoint-only test. -/
theorem joined_instantiation_at_unequal_endpoints :
    G typedPairType Negative.rightSeparating (cons P01DF.skk zeroEnv) (cons .i zeroEnv)
      (.app .i (pairTerm P01DF.skk .i)) (.app .i (pairTerm .i .i)) := by
  have h := fundamental open_sigma_replacement_instance _ _ _ unequalEndpoints
  exact h.2.2 _ _ nonempty_unequal_endpoint_replacement

end P01AC.IndependentMixed
