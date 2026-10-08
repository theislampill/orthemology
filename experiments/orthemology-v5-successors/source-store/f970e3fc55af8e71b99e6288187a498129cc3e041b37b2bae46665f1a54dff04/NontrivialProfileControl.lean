import SourceAttemptTransport

namespace SharedAlias.OrderTransport.Controls
open OperationalJoin.Typed (BoundedEnvelope)
noncomputable section
open Classical

/-- Two distinct explicit orders ensure a nonidentity control without guessing
which ordering Classical Finset.toList happens to select. -/
def sampleSupport : Finset (Fin 7) := {0,1,2,3,4}

def nontrivialProfile : Profile 7 where
  selected := {sampleSupport}
  order P := if same : P = sampleSupport then
    if Progress.labelList P = [0,1,2,3,4] then
      ⟨[4,3,2,1,0], by
        constructor
        · decide
        · rw [same]; decide⟩
    else
      ⟨[0,1,2,3,4], by
        constructor
        · decide
        · rw [same]; decide⟩
    else ⟨P.toList, P.nodup_toList, Finset.toList_toFinset P⟩

theorem profile_is_nontrivial : newLabels nontrivialProfile sampleSupport ≠ Progress.labelList sampleSupport := by
  by_cases h : Progress.labelList sampleSupport = [0,1,2,3,4]
  · simp [newLabels, nontrivialProfile, h]
  · simpa [newLabels, nontrivialProfile, h] using Ne.symm h

theorem selected_command_can_change (actor : ComposedExecution.Actor)
    (action : ComposedExecution.Action) (next : ComposedExecution.Plant) (n : Nat) :
    selected nontrivialProfile (Progress.issue actor action next n sampleSupport) ≠
      Progress.issue actor action next n sampleSupport := by
  intro same
  have pathEq := congrArg (fun k : BoundedEnvelope 7 => k.val.path) same
  -- Use the source issue-support law; the actual old chosen order stays abstract.
  have changed : newLabels nontrivialProfile sampleSupport = Progress.labelList sampleSupport := by
    have exchange' := selected_old_to_new nontrivialProfile
      (Progress.issue actor action next n sampleSupport)
      (by simp [nontrivialProfile]) (by rw [Progress.issue_path]; rfl)
    have combined := exchange'.symm.trans pathEq
    rw [Progress.issue_path] at combined
    exact combined
  exact profile_is_nontrivial changed

end
end SharedAlias.OrderTransport.Controls
