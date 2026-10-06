import LifecycleAdmission
import JoinPreparation

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope path path_card mem_path)

theorem root_eligibility_iff {base n} (p : ComposedExecution.Plant) (time : Nat)
    (r : ComposedExecution.Root) (z : RootState (interface base n))
    (rep : RootRepresents r z) (policyAbove : base ≤ r.policy.epoch)
    (e : BoundedEnvelope n) (requester : String) :
    Envelope p time z e requester ↔ ComposedExecution.Eligible p time r e.val requester := by
  obtain ⟨policy, revoked, _committed, cancelled⟩ := rep
  by_cases above : base ≤ e.val.action.epoch
  · have raw : base + (e.val.action.epoch - base) = e.val.action.epoch := by omega
    simp only [Envelope, interface]
    rw [policy, revoked, raw, cancelled]
    simp [Eligible, and_assoc, and_left_comm, and_comm]
  · have old : e.val.action.epoch < base := by omega
    have rejected := low_raw_epoch_rejected p time r.policy e policyAbove old
    simp [Envelope, interface, policy, Eligible, rejected]

def runtimeSign (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) (i : Nat) : Bool :=
  if w.tainted i then badSign else decide (Eligible w.plant w.now (w.roots i) e requester)

def signers {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (badSign : Bool) : List (Fin n) :=
  (rootsOf e.val.path e.property.2).filter (fun i => runtimeSign w e.val requester badSign i.val)

@[simp] theorem mem_signers {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (badSign : Bool) (i : Fin n) :
    i ∈ signers w e requester badSign ↔
      i.val ∈ e.val.path ∧ runtimeSign w e.val requester badSign i.val = true := by
  simp [signers]

def preparedWorld (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) : ComposedExecution.World :=
  { w with roots := fun i => if e.path.contains i && runtimeSign w e requester badSign i then
      { w.roots i with commitments := e :: (w.roots i).commitments } else w.roots i }

theorem prepare_exact (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) (valid : validPath w e = true) :
    ComposedExecution.prepare w e requester badSign =
      (preparedWorld w e requester badSign, e.path.all (runtimeSign w e requester badSign)) := by
  unfold ComposedExecution.prepare
  rw [if_pos valid]
  rfl

/-- Invalid paths leave the runtime unchanged rather than disappearing from the
comparison. For valid paths, partial commitments survive a false all-signed bit. -/
theorem prepare_invalid_path_identity (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (badSign : Bool) (invalid : validPath w e = false) :
    ComposedExecution.prepare w e requester badSign = (w, false) := by
  simp [ComposedExecution.prepare, invalid]

theorem signer_grant {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n) (requester : String) (badSign : Bool)
    (i : Fin n) (member : i ∈ signers w e requester badSign) :
    i ∈ a.config.faulty ∨ Envelope s.plant w.now (s.roots i) e requester := by
  by_cases bad : i ∈ a.config.faulty
  · exact Or.inl bad
  · right
    have good : Good a.config i := bad
    have intact := (h.taint i).mpr good
    have sign := ((mem_signers w e requester badSign i).mp member).2
    simp only [runtimeSign, intact, Bool.false_eq_true, if_false] at sign
    have eligible : Eligible w.plant w.now (w.roots i.val) e.val requester := of_decide_eq_true sign
    have above : base ≤ (w.roots i.val).policy.epoch := by
      rw [← (h.roots i).1]
      exact reachable_policy_above a reachable i good
    apply (root_eligibility_iff s.plant w.now (w.roots i.val) (s.roots i)
      (h.roots i) above e requester).mpr
    simpa only [h.actual_plant] using eligible

theorem prepared_root_represents {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (badSign : Bool) (i : Fin n) :
    RootRepresents ((preparedWorld w e.val requester badSign).roots i.val)
      ((prepareMany e s (signers w e requester badSign)).roots i) := by
  rw [prepareMany_root]
  obtain ⟨policy, revoked, committed, cancelled⟩ := h.roots i
  by_cases selected : i ∈ signers w e requester badSign
  · rw [if_pos selected]
    obtain ⟨onPath, signs⟩ := (mem_signers w e requester badSign i).mp selected
    have contained : e.val.path.contains i.val = true := by simpa using onPath
    simp only [preparedWorld, contained, signs, Bool.and_self, if_true, RootRepresents]
    refine ⟨policy, revoked, ?_, cancelled⟩
    intro other
    simp only [Finset.mem_insert, List.mem_cons]
    rw [committed]
    exact or_congr Subtype.val_injective.eq_iff.symm Iff.rfl
  · rw [if_neg selected]
    have noSign : ¬(i.val ∈ e.val.path ∧ runtimeSign w e.val requester badSign i.val = true) :=
      fun both => selected ((mem_signers w e requester badSign i).mpr both)
    simpa [preparedWorld, Bool.and_eq_true, noSign] using h.roots i

theorem prepared_certificates_aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (badSign : Bool) :
    CertificatesAligned a (preparedWorld w e.val requester badSign)
      (prepareMany e s (signers w e requester badSign)) := by
  constructor
  · intro cert member
    obtain ⟨index, old, bound⟩ := h.certificates.sound cert member
    exact ⟨index, by simpa using old, by simpa only [CertificateAt, prepareMany_certificates] using bound⟩
  · intro index old
    obtain ⟨cert, member, bound⟩ := h.certificates.complete index (by simpa using old)
    exact ⟨cert, member, by simpa only [CertificateAt, prepareMany_certificates] using bound⟩
  · exact h.certificates.unique

/-- This theorem retains every signed partial preparation even if the runtime
returns false. It quantifies over the one shared badSign Boolean exactly. -/
theorem prepare_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (e : BoundedEnvelope n)
    (requester : String) (badSign : Bool) (valid : validPath w e.val = true) :
    Aligned a (ComposedExecution.prepare w e.val requester badSign).1
      (prepareMany e s (signers w e requester badSign)) ∧
    Trace a.config s ((signers w e requester badSign).map
      (fun i => Event.prepare i e requester w.now))
      (prepareMany e s (signers w e requester badSign)) := by
  rw [prepare_exact w e.val requester badSign valid]
  constructor
  · refine ⟨h.root_count, h.budget, h.quorum, h.revocation_quorum, ?_, ?_, h.taint,
      prepared_root_represents a w s h e requester badSign, ?_,
      prepared_certificates_aligned a w s h e requester badSign⟩
    · simpa [preparedWorld] using h.actual_plant
    · simpa [preparedWorld] using h.effective_policy
    · simpa using h.idle
  · apply prepareMany_trace a.config s _ e requester w.now
    · have wf := of_decide_eq_true valid
      change (path e).card = a.q
      rw [path_card]
      exact wf.2.1.trans h.quorum
    · intro i selected
      exact (mem_path e i).mpr ((mem_signers w e requester badSign i).mp selected).1
    · exact signer_grant a w s h reachable e requester badSign

#print axioms prepare_exact
#print axioms prepare_invalid_path_identity
#print axioms prepare_preserves_alignment
end
end OperationalJoin.Offset
