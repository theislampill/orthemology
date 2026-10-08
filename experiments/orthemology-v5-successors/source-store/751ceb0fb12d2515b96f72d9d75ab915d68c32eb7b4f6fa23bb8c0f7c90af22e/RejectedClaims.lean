import BridgeControls
open Orthemology.Tranche20.OriginalBearerBridge
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open Orthemology.Tranche3.SourceIdentity

-- Each false target below must be rejected. Controls prove the universally
-- quantified failure, so these are compiler sanity checks, not model searches.
example : ∃ g, ActualWholeOriginal withoutCompletion g := by
  exact ⟨0, trivial, by change ¬ True; decide⟩

example : ∃ g, ActualWholeOriginal withoutRealisation g := by
  exact ⟨0, trivial, by change ¬ True; decide⟩

example : ∃ g, ActualWholeOriginal withoutSupport g := by
  exact ⟨0, trivial, by change ¬ True; decide⟩

example : Necessary withoutNeed.existsAt false := by
  simp only [Necessary, withoutNeed, positive]
  decide

example : UniformRoot withoutConstitution.existsAt withoutConstitution.dep false := by
  simp only [UniformRoot, Root, Received, withoutConstitution, positive]
  decide
