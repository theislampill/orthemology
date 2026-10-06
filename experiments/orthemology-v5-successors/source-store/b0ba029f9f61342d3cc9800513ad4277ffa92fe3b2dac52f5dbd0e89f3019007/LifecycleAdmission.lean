import LifecycleDelivery

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope path path_card mem_path)

theorem successful_attempt_lands {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    Lands a.config s w.now e requester := by
  have wf := Typed.attempted_path_well_formed w e.val requester badOpen applied
  refine ⟨?_, ?_⟩
  · change (path e).card = a.q
    rw [path_card, wf.2.1, h.quorum]
  · intro i selected good
    have onPath : decide (i.val ∈ e.val.path) = true :=
      decide_eq_true ((mem_path e i).mp selected)
    have actual := attempt_applied_implies_lands w e.val requester badOpen applied
    have opened := actual i.val (by rw [h.root_count]; exact i.isLt) onPath
    have intact := (h.taint i).mpr good
    simp only [gateOpen, intact, Bool.false_eq_true, if_false] at opened
    have above : base ≤ (w.roots i.val).policy.epoch := by
      rw [← (h.roots i).1]
      exact reachable_policy_above a reachable i good
    apply (root_gate_iff s.plant w.now (w.roots i.val) (s.roots i)
      (h.roots i) above e requester).mpr
    simpa only [h.actual_plant] using opened

/-- Current full runtime policy follows from history-alignment, not equal epoch
numbers alone. Actual certify/deliver preservation is proved separately. -/
theorem successful_attempt_current_policy {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    e.val.action.epoch = w.effectivePolicy.epoch ∧
      localStep w.plant w.effectivePolicy w.now e.val.action = some e.val.successor := by
  obtain ⟨raw, step⟩ := finite_history_raw_current a reachable w.now e requester
    (successful_attempt_lands a w s h reachable e requester badOpen applied)
  exact ⟨raw.trans (aligned_raw_epoch h).symm,
    by simpa only [h.actual_plant, h.effective_policy] using step⟩

/-- This rejection includes every raw envelope, not a subtype deleting old
commands. Successful path validation supplies the representation if needed. -/
theorem low_raw_attempt_rejected_from_aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : ComposedExecution.Envelope)
    (requester : String) (badOpen : Bool) (old : e.action.epoch < base) :
    (attempt w e requester badOpen).2 ≠ true := by
  intro applied
  obtain ⟨nodup, _, bounded⟩ := Typed.attempted_path_well_formed w e requester badOpen applied
  let typed : BoundedEnvelope n := ⟨e, nodup, by simpa only [h.root_count] using bounded⟩
  have raw := (successful_attempt_current_policy a w s h reachable typed requester badOpen applied).1
  have current := aligned_raw_epoch h
  change e.action.epoch = w.effectivePolicy.epoch at raw
  omega

theorem successful_attempt_exact_plant {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badOpen : Bool)
    (applied : (attempt w e.val requester badOpen).2 = true) :
    (attempt w e.val requester badOpen).1.plant =
      (land a.config s w.now e requester).plant ∧
    (land a.config s w.now e requester).plant = e.val.successor := by
  have lands := successful_attempt_lands a w s h reachable e requester badOpen applied
  have auth := (admitted_current_authorized (reachable_consistent reachable) w.now e requester lands).2.2
  have safe := Typed.reachable_safe reachable
  have effect : (land a.config s w.now e requester).plant = e.val.successor := by
    have noDamage : ¬(s.damaged = true ∨
        ¬(interface base n).admits s.plant w.now (a.config.source s.epoch) e requester) := by
      simp only [safe, Bool.false_eq_true, false_or, not_not]
      exact auth
    rw [land, if_neg noDamage]
    rfl
  exact ⟨(applied_attempt_exact_successor w e.val requester badOpen applied).trans effect.symm, effect⟩

#print axioms successful_attempt_current_policy
#print axioms low_raw_attempt_rejected_from_aligned
#print axioms successful_attempt_exact_plant
end
end OperationalJoin.Offset
