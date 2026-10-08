import LifecycleModel

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution

def ownerCertificate {base n} (a : Authority base n) (s : State (interface base n))
    (acks : List Nat) : ComposedExecution.Certificate :=
  ⟨base + s.epoch, a.source (s.epoch + 1), acks⟩

def ownerWorld {base n} (a : Authority base n) (w : ComposedExecution.World)
    (s : State (interface base n)) (acks : List Nat) : ComposedExecution.World :=
  { w with effectivePolicy := a.source (s.epoch + 1)
           roots := fun i => if acks.contains i && !w.tainted i then
             { w.roots i with revoked := (base + s.epoch) :: (w.roots i).revoked }
             else w.roots i
           completed := ownerCertificate a s acks :: w.completed }

/-- Consume the actual unchanged runtime branch. The next policy is the full
authentic source record, not merely a number with the right epoch. -/
theorem certifyTransition_exact {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (acks : List Nat) (nodup : acks.Nodup) (length : acks.length = a.r)
    (bounded : ∀ i ∈ acks, i < n) :
    certifyTransition w acks (a.source (s.epoch + 1)) =
      (ownerWorld a w s acks, some (ownerCertificate a s acks)) := by
  have guard : acks.Nodup ∧ acks.length = w.r ∧ (∀ i ∈ acks, i < w.n) ∧
      (a.source (s.epoch + 1)).epoch = w.effectivePolicy.epoch + 1 := by
    refine ⟨nodup, length.trans h.revocation_quorum.symm, ?_, ?_⟩
    · simpa only [h.root_count] using bounded
    · rw [aligned_raw_epoch h, a.raw_epoch]
      omega
  unfold certifyTransition
  rw [if_pos (decide_eq_true guard)]
  simp only [aligned_raw_epoch h, ownerWorld, ownerCertificate]

theorem certificateAt_old_iff {base n} (a : Authority base n)
    (s : State (interface base n)) (is : List (Fin n)) (index : Nat)
    (old : index < s.epoch) (cert : ComposedExecution.Certificate) :
    CertificateAt a (certifyMany a.config s is) index cert ↔ CertificateAt a s index cert := by
  simp only [CertificateAt, certifyMany_certificates,
    Function.update_of_ne (Nat.ne_of_lt old)]

theorem ownerCertificate_at {base n} (a : Authority base n)
    (s : State (interface base n)) (acks : List Nat) (nodup : acks.Nodup)
    (length : acks.length = a.r) (bounded : ∀ i ∈ acks, i < n) :
    CertificateAt a (certifyMany a.config s (rootsOf acks bounded)) s.epoch
      (ownerCertificate a s acks) := by
  refine ⟨rfl, rfl, nodup, length, bounded, ?_⟩
  intro i
  simp [certifyMany_certificates, ownerCertificate]

theorem owner_certificates_aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (acks : List Nat) (nodup : acks.Nodup) (length : acks.length = a.r)
    (bounded : ∀ i ∈ acks, i < n) :
    CertificatesAligned a (ownerWorld a w s acks)
      (certifyMany a.config s (rootsOf acks bounded)) := by
  have newest := ownerCertificate_at a s acks nodup length bounded
  constructor
  · intro cert member
    change cert ∈ ownerCertificate a s acks :: w.completed at member
    rcases List.mem_cons.mp member with eq | old
    · subst cert
      exact ⟨s.epoch, by simp, newest⟩
    · obtain ⟨index, before, bound⟩ := h.certificates.sound cert old
      exact ⟨index, by simp; omega, (certificateAt_old_iff a s _ index before cert).mpr bound⟩
  · intro index before
    have lt : index < s.epoch + 1 := by simpa using before
    by_cases eq : index = s.epoch
    · subst index
      exact ⟨ownerCertificate a s acks, by simp [ownerWorld], newest⟩
    · have old : index < s.epoch := by omega
      obtain ⟨cert, member, bound⟩ := h.certificates.complete index old
      exact ⟨cert, by simp [ownerWorld, member],
        (certificateAt_old_iff a s _ index old cert).mpr bound⟩
  · change ((base + s.epoch) :: w.completed.map ComposedExecution.Certificate.previousEpoch).Nodup
    apply List.nodup_cons.mpr
    refine ⟨?_, h.certificates.unique⟩
    intro member
    obtain ⟨cert, inc, epoch⟩ := List.mem_map.mp member
    obtain ⟨index, old, previous, _⟩ := h.certificates.sound cert inc
    omega

theorem owner_root_represents {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) (i : Fin n) :
    RootRepresents ((ownerWorld a w s acks).roots i.val)
      ((certifyMany a.config s (rootsOf acks bounded)).roots i) := by
  rw [certifyMany_root]
  obtain ⟨policy, revoked, committed, cancelled⟩ := h.roots i
  by_cases good : Good a.config i
  · have intact := (h.taint i).mpr good
    by_cases selected : i.val ∈ acks
    · rw [if_pos ⟨good, (mem_rootsOf acks bounded i).mpr selected⟩]
      simp only [ownerWorld, RootRepresents]
      have contained : acks.contains i.val = true := by simpa using selected
      simp only [contained, intact, Bool.not_false, Bool.and_self, if_true]
      refine ⟨policy, ?_, committed, cancelled⟩
      intro index
      simp only [Finset.mem_insert, List.mem_cons]
      rw [revoked]
      simp
    · rw [if_neg (by intro both; exact selected ((mem_rootsOf acks bounded i).mp both.2))]
      have absent : acks.contains i.val = false := by simpa using selected
      simpa [ownerWorld, absent, selected] using h.roots i
  · have faulty : w.tainted i.val = true := by
      cases eq : w.tainted i.val with
      | false => exact False.elim (good ((h.taint i).mp eq))
      | true => rfl
    rw [if_neg (by intro both; exact good both.1)]
    simpa [ownerWorld, faulty] using h.roots i

/-- The actual aggregate owner operation is simulated by the exact request,
root-close/acknowledge and complete events, and preserves full alignment. -/
theorem certifyTransition_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (acks : List Nat) (nodup : acks.Nodup) (length : acks.length = a.r)
    (bounded : ∀ i ∈ acks, i < n) :
    Aligned a (certifyTransition w acks (a.source (s.epoch + 1))).1
      (certifyMany a.config s (rootsOf acks bounded)) ∧
    Trace a.config s
      (.request :: (rootsOf acks bounded).map Event.acknowledge ++ [.complete])
      (certifyMany a.config s (rootsOf acks bounded)) := by
  rw [certifyTransition_exact a w s h acks nodup length bounded]
  constructor
  · refine ⟨h.root_count, h.budget, h.quorum, h.revocation_quorum, ?_, ?_,
      h.taint, ?_, rfl, owner_certificates_aligned a w s h acks nodup length bounded⟩
    · simpa [ownerWorld] using h.actual_plant
    · simp [ownerWorld]
    · exact owner_root_represents a w s h acks bounded
  · apply certifyMany_trace a.config s (rootsOf acks bounded) h.idle
    rw [rootsOf_card acks bounded nodup]
    exact length

#print axioms certifyTransition_exact
#print axioms certifyTransition_preserves_alignment
end
end OperationalJoin.Offset
