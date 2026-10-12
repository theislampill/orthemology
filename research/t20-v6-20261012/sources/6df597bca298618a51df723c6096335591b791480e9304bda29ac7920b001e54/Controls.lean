import CompletionSeparation
namespace CompletionSeparation.Controls
open P01AC P01D
open P01AC.ExtensionalRepair (HasE)

-- Negative control: semantic Eta validity cannot be reflected into source typing.
example : True := by
  fail_if_success
    have bad : HasE [] (.app (.atom .k) (.atom .i)) SigmaTagBoundary.Eta :=
      CompletionSeparation.henkin_eta_valid HomogeneousOriginalW.emptyTypes HenkinSoundness.zeroEnv
  trivial

-- Negative control: the same componentwise Raw-pair proof does not validate tagged Eta.
example : True := by
  fail_if_success
    have bad : TaggedPER.F SigmaTagBoundary.Eta SigmaTagBoundary.emptyEnv TaggedPER.zeroEnv
        (OpenTermStandardness.T.k ⬝ OpenTermStandardness.T.i)
        (OpenTermStandardness.T.k ⬝ OpenTermStandardness.T.i) := by
      intro z w zw
      exact ⟨⟨True.intro, True.intro⟩, .k _ _, .k _ _⟩
  trivial

-- Positive controls: the retained opposite edge and new reverse edge both apply to literal types.
example (p : Poly) : ¬ HasE [] p (arr SourceRigidity.Rigidity SigmaTagBoundary.Eta) :=
  SigmaTagBoundary.no_rigidity_to_eta p
example (p : Poly) : ¬ HasE [] p (arr SigmaTagBoundary.Eta SourceRigidity.Rigidity) :=
  CompletionSeparation.no_eta_to_rigidity p

-- A semantic closed environment cannot support both Henkin witnesses.
example (r t : CaseOperational.T)
    (h : HenkinSoundness.F SourceRigidity.Rigidity HomogeneousOriginalW.emptyTypes
      HenkinSoundness.zeroEnv r t) : False := CompletionSeparation.henkin_rigidity_empty r t h

#print axioms CompletionSeparation.reverse_relative_independence
end CompletionSeparation.Controls
