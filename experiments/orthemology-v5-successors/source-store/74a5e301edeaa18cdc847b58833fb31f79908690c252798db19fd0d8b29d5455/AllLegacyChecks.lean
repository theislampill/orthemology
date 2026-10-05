/- Exact recovered controls and the displayed-support boundary. -/
import AllLegacyComparison
namespace P01AC.Legacy
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- The inherited D is recursively translated, retaining all dependent Id indices. -/
theorem dependent_type_readback : translate P01DF.dependentPolyType =
    .all (.pi .raw (arr (.param 0) (arr (.identity .raw (.var 0) (.atom .i)) (.param 0)))) := rfl

theorem open_replacement_embedding :
    Has (rawTel 1) (.atom .i)
      (arr (.identity .raw (.var 0) (.atom .i)) (.identity .raw (.var 0) (.atom .i))) :=
  openIdentityInstance_supported.raw_embed

/-- A closed conclusion can hide an unsupported, unused All replacement. -/
def hiddenOpenReplacementTree : Derivation (.atom .i) .raw :=
  .allElim (A := .identity (.var 1) (.atom .i)) (.allIntro (.raw (.atom .i)))

theorem hidden_replacement_old_judgment : P01DF.Has (.atom .i) .raw := erase hiddenOpenReplacementTree

theorem hidden_replacement_closed : Scoped 0 (.atom .i) := trivial

theorem hidden_replacement_not_supported : ¬ Supported 0 hiddenOpenReplacementTree := by
  intro hs
  have hp : Scoped 0 (.var 1) := hs.2.2.1.1
  exact Nat.not_lt_zero 1 hp

/-- Conversion may erase a displayed unscoped premise; support must still reject it. -/
def hiddenOpenPremiseTree : Derivation (.atom .i) .raw :=
  .conv (.raw (.app (.app (.atom .k) (.atom .i)) (.var 37)))
    (.k (.atom .i) (.var 37))

theorem hidden_premise_not_supported : ¬ Supported 0 hiddenOpenPremiseTree := by
  intro hs
  have hp : Scoped 0 (.var 37) := hs.2.2.1.2
  exact Nat.not_lt_zero 37 hp

/-- In contrast, hidden proof-internal conversion witnesses are outside the census.
Both displayed endpoints and the sole displayed premise are exactly the closed I. -/
def conversionInternalTree : Derivation (.atom .i) .raw :=
  .conv (.raw (.atom .i))
    (.trans (.symm (.k (.atom .i) (.var 37))) (.k (.atom .i) (.var 37)))

theorem conversion_internal_supported : Supported 0 conversionInternalTree := by
  simp [conversionInternalTree,Supported,Scoped,TypeSupported]

theorem conversion_internal_embedding : Has [] (.atom .i) .raw :=
  conversion_internal_supported.raw_embed

/-- The old restriction remains an actual restriction; it was not renamed or relaxed. -/
theorem nucleus_still_excludes_all_intro {n : Nat} {A' : P01TC.Ty} :
    ¬ P01TC.Legacy.Restricted n identityTree A' := P01TC.Legacy.no_allIntro

theorem nucleus_still_excludes_dependent_type {n : Nat} {A' : P01TC.Ty} :
    ¬ P01TC.Legacy.Translation n P01DF.dependentPolyType A' := P01TC.Legacy.no_dependentPolyType

end P01AC.Legacy

#print axioms P01AC.Legacy.supported_embed
#print axioms P01AC.Legacy.FG_agrees
#print axioms P01AC.Legacy.TypeSupported.theta_form
#print axioms P01AC.Legacy.dependent_polymorphic_typed
#print axioms P01AC.Legacy.dependent_polymorphic_self_typed
#print axioms P01AC.Legacy.open_replacement_embedding
#print axioms P01AC.Legacy.hidden_replacement_not_supported
#print axioms P01AC.Legacy.nucleus_still_excludes_dependent_type

#print axioms P01AC.Legacy.hidden_premise_not_supported
#print axioms P01AC.Legacy.conversion_internal_embedding
