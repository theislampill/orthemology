import RuntimeCancellationTrace

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution

/-- NEW reference-model operation. The accepted service has no such operation.
It changes only the clock annotation, never the actor's stored observation. -/
def setReferenceTime (w : ComposedExecution.World) (now : Nat) : ComposedExecution.World :=
  { w with now := now }

/-- Structural alignment places no validity-at-now requirement on stored leases
or certificates. This lemma is deliberately unrestricted, even for rollback. -/
theorem setReferenceTime_aligned {base n} {a : Authority base n}
    {w : ComposedExecution.World} {s : State (interface base n)}
    (aligned : Aligned a w s) (now : Nat) : Aligned a (setReferenceTime w now) s := by
  refine ⟨aligned.root_count, aligned.budget, aligned.quorum, aligned.revocation_quorum,
    aligned.actual_plant, aligned.effective_policy, aligned.taint, aligned.roots, aligned.idle, ?_⟩
  exact ⟨aligned.certificates.sound, aligned.certificates.complete, aligned.certificates.unique⟩

theorem setReferenceTime_fields (w : ComposedExecution.World) (now : Nat) :
    (setReferenceTime w now).now = now ∧
    (setReferenceTime w now).plant = w.plant ∧
    (setReferenceTime w now).roots = w.roots ∧
    (setReferenceTime w now).effectivePolicy = w.effectivePolicy ∧
    (setReferenceTime w now).completed = w.completed := by
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

def actionLeaseEnd : ComposedExecution.Action → Nat
  | .install command => command.leaseEnd
  | .repair command => command.leaseEnd

/-- Derived from the exact imported grant predicates, not a new admission law. -/
theorem localStep_before_lease_end (plant : ComposedExecution.Plant) (policy : ComposedExecution.Policy)
    (now : Nat) (action : ComposedExecution.Action) (next : ComposedExecution.Plant)
    (accepted : localStep plant policy now action = some next) : now < actionLeaseEnd action := by
  cases action with
  | install command =>
      have applied := (local_install_refinement plant policy now command next accepted).2.1
      obtain ⟨_, grant, _, valid⟩ :=
        CriterionInstallation.accepted_has_install_specific_grant (ruleState plant policy now) command applied
      exact valid.2.2.2.2.2.2.2.2.1
  | repair command =>
      have applied := (local_repair_refinement plant policy now command next accepted).2.2.2.1
      obtain ⟨_, grant, _, valid⟩ :=
        TypedCriterionGuard.accepted_current_grant (dataState plant policy now) command applied
      exact valid.2.2.2.2.2.2.2.2.1

theorem expired_localStep_is_none (plant : ComposedExecution.Plant) (policy : ComposedExecution.Policy)
    (now : Nat) (action : ComposedExecution.Action) (expired : actionLeaseEnd action ≤ now) :
    localStep plant policy now action = none := by
  cases result : localStep plant policy now action with
  | none => rfl
  | some next => exact False.elim (Nat.not_lt_of_ge expired
      (localStep_before_lease_end plant policy now action next result))

theorem expired_aligned_attempt_rejected {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n))
    (aligned : Aligned a w s) (reachable : Reachable a.config s)
    (e : Typed.BoundedEnvelope n) (requester : String) (badOpen : Bool)
    (expired : actionLeaseEnd e.val.action ≤ w.now) : (attempt w e.val requester badOpen).2 ≠ true := by
  intro applied
  have admitted := (successful_attempt_current_policy a w s aligned reachable e requester badOpen applied).2
  exact Nat.not_lt_of_ge expired
    (localStep_before_lease_end w.plant w.effectivePolicy w.now e.val.action e.val.successor admitted)

#print axioms setReferenceTime_aligned
#print axioms localStep_before_lease_end
#print axioms expired_aligned_attempt_rejected
end
end OperationalJoin.Offset
