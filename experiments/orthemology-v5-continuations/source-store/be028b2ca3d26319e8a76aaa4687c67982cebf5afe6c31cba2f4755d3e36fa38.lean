import SourceResources
namespace P03SourceControls
open P03Source OrthemologyV2 OrthemologyV3

def pid : SourceProof := .allI (.i (.var 0))
def selfApp : SourceProof := .app (.allE pid identityCode) pid

theorem identity_accepted : sourceCheck 0 pid = some (.i, identityCode) := by decide

theorem self_application_accepted :
    sourceCheck 0 selfApp = some (.app .i .i, identityCode) := by decide

theorem explicit_trace_accepted :
    sourceCheck 0 (.reduce selfApp [.app .i .i, .i]) = some (.i, identityCode) := by decide

theorem empty_trace_refused : sourceCheck 0 (.reduce pid []) = none := by decide

theorem wrong_start_refused : sourceCheck 0 (.reduce pid [.k]) = none := by decide

theorem invalid_step_refused :
    sourceCheck 0 (.reduce selfApp [.app .i .i, .k]) = none := by decide

theorem free_type_refused : sourceCheck 0 (.i (.var 0)) = none := by decide

theorem nonpolymorphic_elimination_refused :
    sourceCheck 0 (.allE (.i .bottom) .bottom) = none := by decide

theorem application_type_mismatch_refused :
    sourceCheck 0 (.app (.i .bottom) pid) = none := by decide

theorem initial_depth_limit_refused : sourceCheck 101 pid = none := by decide

/-- This catches the circular alternative of defining source acceptance to be
exactly target checking: source traces contain information erased by export. -/
theorem malformed_trace_can_erase_to_accepted_cert :
    sourceCheck 0 (.reduce pid [.k]) = none ∧
      (check 0 (encode (.reduce pid [.k]))).isSome = true := by decide

theorem erased_checker_acceptance_is_not_source_acceptance :
    ¬ (∀ p : SourceProof, (check 0 (encode p)).isSome = true → (sourceCheck 0 p).isSome = true) := by
  intro h
  have hbad := h (.reduce pid [.k]) (by decide)
  have hf : (sourceCheck 0 (.reduce pid [.k])).isSome = false := by decide
  rw [hf] at hbad
  contradiction

#print axioms malformed_trace_can_erase_to_accepted_cert
#print axioms erased_checker_acceptance_is_not_source_acceptance
#print axioms explicit_trace_accepted
end P03SourceControls
