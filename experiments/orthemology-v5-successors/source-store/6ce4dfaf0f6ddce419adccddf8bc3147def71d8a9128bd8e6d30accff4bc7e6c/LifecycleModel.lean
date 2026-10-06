import EpochOffset
import JoinBatches

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope path path_card mem_path)

def rootsOf {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) : List (Fin n) :=
  xs.attach.map (fun i => ⟨i.val, bounded i.val i.property⟩)

@[simp] theorem rootsOf_values {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) :
    (rootsOf xs bounded).map Fin.val = xs := by
  simp [rootsOf, List.map_map, Function.comp_def]

@[simp] theorem rootsOf_length {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) :
    (rootsOf xs bounded).length = xs.length := by simp [rootsOf]

@[simp] theorem mem_rootsOf {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) (i : Fin n) :
    i ∈ rootsOf xs bounded ↔ i.val ∈ xs := by
  constructor
  · intro member
    have val : i.val ∈ (rootsOf xs bounded).map Fin.val := List.mem_map.mpr ⟨i, member, rfl⟩
    simpa using val
  · intro member
    apply List.mem_map.mpr
    refine ⟨⟨i.val, member⟩, List.mem_attach _ _, ?_⟩
    apply Fin.ext
    rfl

theorem rootsOf_nodup {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) (nodup : xs.Nodup) :
    (rootsOf xs bounded).Nodup := by
  have mapped : ((rootsOf xs bounded).map Fin.val).Nodup := by simpa using nodup
  exact List.Nodup.of_map _ mapped

theorem rootsOf_card {n} (xs : List Nat) (bounded : ∀ i ∈ xs, i < n) (nodup : xs.Nodup) :
    (rootsOf xs bounded).toFinset.card = xs.length := by
  rw [List.toFinset_card_of_nodup (rootsOf_nodup xs bounded nodup), rootsOf_length]

/-- Full stored Policy and original ordered acknowledger list remain in the
certificate. The common certificate set tracks their root membership only. -/
def CertificateAt {base n} (a : Authority base n) (s : State (interface base n))
    (index : Nat) (cert : ComposedExecution.Certificate) : Prop :=
  cert.previousEpoch = base + index ∧ cert.policy = a.source (index + 1) ∧
  cert.acknowledgers.Nodup ∧ cert.acknowledgers.length = a.r ∧
  (∀ i ∈ cert.acknowledgers, i < n) ∧
  (∀ i : Fin n, i ∈ s.certificates index ↔ i.val ∈ cert.acknowledgers)

structure CertificatesAligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) : Prop where
  sound : ∀ cert ∈ w.completed, ∃ index, index < s.epoch ∧ CertificateAt a s index cert
  complete : ∀ index, index < s.epoch → ∃ cert ∈ w.completed, CertificateAt a s index cert
  unique : (w.completed.map ComposedExecution.Certificate.previousEpoch).Nodup

/-- Alignment is a refinement relation, not an input to the compiled gate.
It intentionally requires an idle macro boundary and the entire authentic
post-base certificate stream. It certifies no pre-base history. -/
structure Aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) : Prop where
  root_count : w.n = n
  budget : w.budget = a.budget
  quorum : w.q = a.q
  revocation_quorum : w.r = a.r
  actual_plant : w.plant = s.plant
  effective_policy : w.effectivePolicy = a.source s.epoch
  taint : ∀ i : Fin n, w.tainted i.val = false ↔ Good a.config i
  roots : ∀ i : Fin n, RootRepresents (w.roots i.val) (s.roots i)
  idle : s.pending = false
  certificates : CertificatesAligned a w s

theorem aligned_raw_epoch {base n} {a : Authority base n}
    {w : ComposedExecution.World} {s : State (interface base n)} (h : Aligned a w s) :
    w.effectivePolicy.epoch = base + s.epoch := by
  rw [h.effective_policy, a.raw_epoch]

/-- Exact unchanged initialWorld, with explicit four-root configuration. The
source can start at raw base=2 just as the accepted native fixture does. -/
theorem initial_aligned {base} (a : Authority base 4) (p : ComposedExecution.Plant)
    (bad : List Nat) (budget : a.budget = 1) (q : a.q = 3) (r : a.r = 3)
    (taint : ∀ i : Fin 4, bad.contains i.val = false ↔ i ∉ a.faulty) :
    Aligned a (initialWorld p (a.source 0) bad) (Initial a.config p) := by
  refine ⟨rfl, budget.symm, q.symm, r.symm, rfl, rfl, ?_, ?_, rfl, ?_⟩
  · intro i
    exact taint i
  · intro i
    refine ⟨rfl, ?_, ?_, ?_⟩ <;> simp [Initial, initialWorld]
  · constructor
    · intro cert member
      cases member
    · intro index before
      exact False.elim (Nat.not_lt_zero index before)
    · simp [initialWorld]

/-- No message predating the explicit base can be drawn from an aligned
post-boundary completed-certificate list. -/
theorem aligned_certificate_not_prebase {base n} {a : Authority base n}
    {w : ComposedExecution.World} {s : State (interface base n)} (h : Aligned a w s)
    (cert : ComposedExecution.Certificate) (member : cert ∈ w.completed) :
    base ≤ cert.previousEpoch ∧ base < cert.policy.epoch := by
  obtain ⟨index, _, old, policy, _⟩ := h.certificates.sound cert member
  rw [old, policy, a.raw_epoch]
  omega

#print axioms initial_aligned
#print axioms aligned_certificate_not_prebase
end
end OperationalJoin.Offset
