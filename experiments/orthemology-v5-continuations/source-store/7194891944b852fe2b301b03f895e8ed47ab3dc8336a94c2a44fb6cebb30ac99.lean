import SourceResources
namespace P03Source
open OrthemologyV2 OrthemologyV3

/-- Resource checking cannot convert any semantic refusal into acceptance. -/
theorem semantic_refusal_preserved {p : SourceProof} {d : Nat}
    (h : sourceCheckCore d p = none) : sourceCheck d p = none := by
  cases hs : sourceCheck d p with
  | none => rfl
  | some out =>
      have hc := sourceCheck_refines_core hs
      rw [h] at hc
      contradiction

theorem empty_trace_is_refused (start : Term) : sourceTrace start [] = none := rfl

theorem singleton_trace_exact (start first : Term) :
    sourceTrace start [first] = if first = start then some start else none := by
  simp only [sourceTrace, sourceTraceTail]

theorem semantic_singleton_trace {p : SourceProof} {d : Nat} {t : Term} {A : TypeCode}
    (h : sourceCheckCore d p = some (t,A)) :
    sourceCheckCore d (.reduce p [t]) = some (t,A) := by
  simp [sourceCheckCore, h, sourceTrace, sourceTraceTail, Option.map]

-- These exact values select less/equal/greater binder cases and prevent a
-- capture-incorrect substitution implementation from satisfying the fixtures.
theorem capture_equal_under_one_binder :
    sourceSubstitute (.all (.arrow (.var 1) (.var 0))) (.var 0) 0 =
      .all (.arrow (.var 1) (.var 0)) := by decide

theorem capture_greater_under_one_binder :
    sourceSubstitute (.all (.arrow (.var 2) (.var 0))) (.var 0) 0 =
      .all (.arrow (.var 1) (.var 0)) := by decide

theorem capture_equal_under_two_binders :
    sourceSubstitute (.all (.all (.arrow (.var 2) (.var 0)))) (.var 1) 0 =
      .all (.all (.arrow (.var 3) (.var 0))) := by decide

theorem capture_less_under_two_binders :
    sourceSubstitute (.all (.all (.arrow (.var 1) (.var 0)))) (.var 9) 0 =
      .all (.all (.arrow (.var 1) (.var 0))) := by decide

namespace BranchFixtures
def pid : SourceProof := .allI (.i (.var 0))
def selfApp : SourceProof := .app (.allE pid identityCode) pid

theorem singleton_reduction_accepted :
    sourceCheck 0 (.reduce selfApp [.app .i .i]) = some (.app .i .i, identityCode) := by decide

theorem i_scope_refusal : sourceCheck 0 (.i (.var 0)) = none := by decide

theorem k_first_scope_refusal : sourceCheck 0 (.k (.var 0) .bottom) = none := by decide

theorem k_second_scope_refusal : sourceCheck 0 (.k .bottom (.var 0)) = none := by decide

theorem s_first_scope_refusal : sourceCheck 0 (.s (.var 0) .bottom .bottom) = none := by decide

theorem s_second_scope_refusal : sourceCheck 0 (.s .bottom (.var 0) .bottom) = none := by decide

theorem s_third_scope_refusal : sourceCheck 0 (.s .bottom .bottom (.var 0)) = none := by decide

theorem app_function_refusal : sourceCheck 0 (.app (.i (.var 0)) pid) = none := by decide

theorem app_argument_refusal : sourceCheck 0 (.app (.i .bottom) (.i (.var 0))) = none := by decide

theorem app_nonarrow_refusal : sourceCheck 0 (.app pid pid) = none := by decide

theorem allI_body_scope_refusal : sourceCheck 0 (.allI (.i (.var 1))) = none := by decide

theorem allE_argument_scope_refusal : sourceCheck 0 (.allE pid (.var 0)) = none := by decide

theorem allE_body_refusal : sourceCheck 0 (.allE (.i (.var 0)) .bottom) = none := by decide

theorem allE_nonpoly_refusal : sourceCheck 0 (.allE (.i .bottom) .bottom) = none := by decide

theorem reduce_body_refusal : sourceCheck 0 (.reduce (.i (.var 0)) [.i]) = none := by decide

theorem reduce_empty_refusal : sourceCheck 0 (.reduce pid []) = none := by decide

theorem reduce_wrong_start_refusal : sourceCheck 0 (.reduce pid [.k]) = none := by decide

theorem reduce_normal_step_refusal : sourceCheck 0 (.reduce pid [.i,.i]) = none := by decide

theorem reduce_wrong_successor_refusal :
    sourceCheck 0 (.reduce selfApp [.app .i .i,.k]) = none := by decide

end BranchFixtures
#print axioms semantic_refusal_preserved
#print axioms semantic_singleton_trace
#print axioms capture_equal_under_two_binders
#print axioms BranchFixtures.singleton_reduction_accepted
end P03Source
