import LifecycleCertification

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution

/-- A proof-side enumeration of the intact recipients updated by the exact
compiled delivery. This is not information furnished to the actor. -/
def goodIndices {base n} (a : Authority base n) : List (Fin n) :=
  (Finset.univ.filter (fun i => Good a.config i)).toList
@[simp] theorem mem_goodIndices {base n} (a : Authority base n) (i : Fin n) :
    i ∈ goodIndices a ↔ Good a.config i := by simp [goodIndices]

def deliveredWorld (w : ComposedExecution.World) (cert : ComposedExecution.Certificate) :
    ComposedExecution.World :=
  { w with roots := fun i =>
      if !w.tainted i && decide ((w.roots i).policy.epoch < cert.policy.epoch) then
        { w.roots i with policy := cert.policy } else w.roots i }

theorem deliver_exact (w : ComposedExecution.World) (cert : ComposedExecution.Certificate)
    (member : cert ∈ w.completed) : ComposedExecution.deliver w cert = deliveredWorld w cert := by
  unfold ComposedExecution.deliver
  rw [if_pos (decide_eq_true member)]
  rfl

theorem delivery_root_represents {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (index : Nat) (cert : ComposedExecution.Certificate)
    (bound : CertificateAt a s index cert) (i : Fin n) :
    RootRepresents ((deliveredWorld w cert).roots i.val)
      ((deliverMany a.config (index + 1) s (goodIndices a)).roots i) := by
  rw [deliverMany_root]
  obtain ⟨policy, revoked, committed, cancelled⟩ := h.roots i
  by_cases good : Good a.config i
  · have intact := (h.taint i).mpr good
    have above := reachable_policy_above a reachable i good
    have certEpoch : cert.policy.epoch = base + (index + 1) := by
      rw [bound.2.1, a.raw_epoch]
    have rawPolicy : (w.roots i.val).policy.epoch = (s.roots i).descriptor.epoch :=
      congrArg ComposedExecution.Policy.epoch policy.symm
    have test : (w.roots i.val).policy.epoch < cert.policy.epoch ↔
        (interface base n).policyEpoch (s.roots i).descriptor < index + 1 := by
      simp only [interface]
      rw [rawPolicy, certEpoch]
      omega
    by_cases newer : (interface base n).policyEpoch (s.roots i).descriptor < index + 1
    · rw [if_pos ⟨(mem_goodIndices a i).mpr good, newer⟩]
      have rawNewer := test.mpr newer
      simp only [deliveredWorld, intact, Bool.not_false, decide_eq_true rawNewer,
        Bool.and_self, if_true, RootRepresents]
      exact ⟨bound.2.1.symm, revoked, committed, cancelled⟩
    · rw [if_neg (by intro both; exact newer both.2)]
      have rawOld : ¬(w.roots i.val).policy.epoch < cert.policy.epoch := fun new => newer (test.mp new)
      simpa [deliveredWorld, intact, rawOld] using h.roots i
  · rw [if_neg (by intro both; exact good ((mem_goodIndices a i).mp both.1))]
    have faulty : w.tainted i.val = true := by
      cases eq : w.tainted i.val with
      | false => exact False.elim (good ((h.taint i).mp eq))
      | true => rfl
    simpa [deliveredWorld, faulty] using h.roots i

theorem delivery_certificates_aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (index : Nat) (cert : ComposedExecution.Certificate) :
    CertificatesAligned a (deliveredWorld w cert)
      (deliverMany a.config (index + 1) s (goodIndices a)) := by
  constructor
  · intro other member
    obtain ⟨j, old, bound⟩ := h.certificates.sound other member
    exact ⟨j, by simpa using old, by simpa only [CertificateAt, deliverMany_certificates] using bound⟩
  · intro j old
    obtain ⟨other, member, bound⟩ := h.certificates.complete j (by simpa using old)
    exact ⟨other, member, by simpa only [CertificateAt, deliverMany_certificates] using bound⟩
  · exact h.certificates.unique

/-- Actual completed-certificate delivery, including delayed or repeated older
certificates, refines a finite sequence of the exact primitive delivery events.
No pre-base certificate is admitted by the aligned post-boundary source stream. -/
theorem deliver_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (reachable : Reachable a.config s) (cert : ComposedExecution.Certificate)
    (member : cert ∈ w.completed) :
    ∃ index, index < s.epoch ∧ CertificateAt a s index cert ∧
      Aligned a (ComposedExecution.deliver w cert)
        (deliverMany a.config (index + 1) s (goodIndices a)) ∧
      Trace a.config s ((goodIndices a).map (fun i => Event.deliver i (index + 1)))
        (deliverMany a.config (index + 1) s (goodIndices a)) := by
  obtain ⟨index, old, bound⟩ := h.certificates.sound cert member
  refine ⟨index, old, bound, ?_, ?_⟩
  · rw [deliver_exact w cert member]
    refine ⟨h.root_count, h.budget, h.quorum, h.revocation_quorum, ?_, ?_, h.taint,
      delivery_root_represents a w s h reachable index cert bound, ?_,
      delivery_certificates_aligned a w s h index cert⟩
    · simpa [deliveredWorld] using h.actual_plant
    · simpa [deliveredWorld] using h.effective_policy
    · simpa using h.idle
  · apply deliverMany_trace
    omega

#print axioms deliver_exact
#print axioms deliver_preserves_alignment
end
end OperationalJoin.Offset
