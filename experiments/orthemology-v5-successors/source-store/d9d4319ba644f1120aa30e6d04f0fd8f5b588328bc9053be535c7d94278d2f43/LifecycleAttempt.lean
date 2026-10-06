import LifecyclePreparation

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope)

theorem attempt_success_effect (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) (applied : (attempt w e requester badOpen).2 = true) :
    (attempt w e requester badOpen).1 = { w with plant := e.successor } := by
  unfold attempt at applied ⊢
  split
  · rfl
  · split at applied <;> simp_all

theorem attempt_invalid_path_identity (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) (invalid : validPath w e = false) :
    attempt w e requester badOpen = (w, false) := by
  simp [attempt, invalid]

theorem admitted_land_exact {base n} (a : Authority base n)
    (s : State (interface base n)) (reachable : Reachable a.config s)
    (time : Nat) (e : BoundedEnvelope n) (requester : String)
    (admitted : Lands a.config s time e requester) :
    land a.config s time e requester = { s with plant := e.val.successor } := by
  have auth := (admitted_current_authorized (reachable_consistent reachable) time e requester admitted).2.2
  have safe := Typed.reachable_safe reachable
  have noDamage : ¬(s.damaged = true ∨
      ¬(interface base n).admits s.plant time (a.config.source s.epoch) e requester) := by
    simp only [safe, Bool.false_eq_true, false_or, not_not]
    exact auth
  rw [land, if_neg noDamage]
  rfl

/-- The complete runtime World update matches one admitted primitive effect;
control policies, thresholds and certificate history remain aligned. -/
theorem successful_attempt_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    Aligned a (attempt w e.val requester badOpen).1 (land a.config s w.now e requester) ∧
      Step a.config s (.land e requester w.now) (land a.config s w.now e requester) := by
  have admitted := successful_attempt_lands a w s h reachable e requester badOpen applied
  constructor
  · rw [attempt_success_effect w e.val requester badOpen applied,
        admitted_land_exact a s reachable w.now e requester admitted]
    exact ⟨h.root_count, h.budget, h.quorum, h.revocation_quorum, rfl,
      h.effective_policy, h.taint, h.roots, h.idle,
      ⟨h.certificates.sound, h.certificates.complete, h.certificates.unique⟩⟩
  · exact Step.land s e requester w.now admitted

/-- Both outcomes of the exact shared badOpen call are covered. A rejected
attempt is full World identity and a zero-event common stutter. -/
theorem attempt_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool) :
    ∃ next events, Aligned a (attempt w e.val requester badOpen).1 next ∧
      Trace a.config s events next ∧
      (events = [] ∨ events = [.land e requester w.now]) := by
  cases applied : (attempt w e.val requester badOpen).2 with
  | false =>
      refine ⟨s, [], ?_, Trace.nil s, Or.inl rfl⟩
      rw [rejected_attempt_full_identity w e.val requester badOpen applied]
      exact h
  | true =>
      obtain ⟨alignment, step⟩ := successful_attempt_preserves_alignment a w s h reachable e requester badOpen applied
      exact ⟨land a.config s w.now e requester, [.land e requester w.now], alignment,
        Trace.cons step (Trace.nil _), Or.inr rfl⟩

#print axioms attempt_success_effect
#print axioms successful_attempt_preserves_alignment
#print axioms attempt_preserves_alignment
end
end OperationalJoin.Offset
