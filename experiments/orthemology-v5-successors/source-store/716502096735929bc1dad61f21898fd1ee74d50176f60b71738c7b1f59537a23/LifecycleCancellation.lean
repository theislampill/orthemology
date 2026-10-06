import RuntimeTrace
import JoinCancellation

namespace OperationalJoin.Offset
noncomputable section
open Classical
open ComposedExecution
open Typed (BoundedEnvelope path mem_path)

def cancelResponders {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) : List (Fin n) :=
  (rootsOf acks bounded).filter (fun i => w.tainted i.val || requester == e.val.action.actor)

@[simp] theorem mem_cancelResponders {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) (i : Fin n) :
    i ∈ cancelResponders w e requester acks bounded ↔
      i.val ∈ acks ∧ (w.tainted i.val = true ∨ requester = e.val.action.actor) := by
  simp [cancelResponders, Bool.or_eq_true]

/-- This retains the exact runtime list of this call's replies, in order. -/
theorem cancelResponders_values {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) :
    (cancelResponders w e requester acks bounded).map Fin.val =
      acks.filter (fun i => w.tainted i || requester == e.val.action.actor) := by
  unfold cancelResponders
  change ((rootsOf acks bounded).filter
    ((fun i : Nat => w.tainted i || requester == e.val.action.actor) ∘ Fin.val)).map Fin.val = _
  rw [← List.filter_map, rootsOf_values]

theorem cancelResponders_length {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) :
    (cancelResponders w e requester acks bounded).length =
      (acks.filter (fun i => w.tainted i || requester == e.val.action.actor)).length := by
  have lengths := congrArg List.length (cancelResponders_values w e requester acks bounded)
  simpa only [List.length_map] using lengths

theorem cancelResponders_nodup {n} (w : ComposedExecution.World) (e : BoundedEnvelope n)
    (requester : String) (acks : List Nat) (bounded : ∀ i ∈ acks, i < n) (nodup : acks.Nodup) :
    (cancelResponders w e requester acks bounded).Nodup :=
  (rootsOf_nodup acks bounded nodup).filter _

def cancelledWorld (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat) : ComposedExecution.World :=
  { w with roots := fun i => if acks.contains i && !w.tainted i && requester == e.action.actor then
      { w.roots i with cancelled := e :: (w.roots i).cancelled } else w.roots i }

theorem cancelWith_exact (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat) (valid : validPath w e = true)
    (nodup : acks.Nodup) (selected : ∀ i ∈ acks, i ∈ e.path) :
    cancelWith w e requester acks = (cancelledWorld w e requester acks,
      decide (w.budget + 1 ≤ (acks.filter (fun i => w.tainted i || requester == e.action.actor)).length)) := by
  unfold cancelWith
  rw [if_pos (by simp only [valid, Bool.true_and]; exact decide_eq_true ⟨nodup, selected⟩)]
  rfl

theorem cancelWith_invalid_identity (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat)
    (invalid : ¬(validPath w e = true ∧ acks.Nodup ∧ ∀ i ∈ acks, i ∈ e.path)) :
    cancelWith w e requester acks = (w, false) := by
  unfold cancelWith
  rw [if_neg]
  intro guard
  have both : validPath w e = true ∧ decide (acks.Nodup ∧ ∀ i ∈ acks, i ∈ e.path) = true := by
    simpa only [Bool.and_eq_true] using guard
  exact invalid ⟨both.1, of_decide_eq_true both.2⟩

theorem true_cancel_outer_guards (w : ComposedExecution.World) (e : ComposedExecution.Envelope)
    (requester : String) (acks : List Nat) (closed : (cancelWith w e requester acks).2 = true) :
    validPath w e = true ∧ acks.Nodup ∧ ∀ i ∈ acks, i ∈ e.path := by
  unfold cancelWith at closed
  split at closed
  · rename_i guard
    have both : validPath w e = true ∧ decide (acks.Nodup ∧ ∀ i ∈ acks, i ∈ e.path) = true := by
      simpa only [Bool.and_eq_true] using guard
    exact ⟨both.1, of_decide_eq_true both.2⟩
  · cases closed

theorem cancel_responder_auth {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (bounded : ∀ i ∈ acks, i < n) (i : Fin n)
    (member : i ∈ cancelResponders w e requester acks bounded) :
    i ∈ a.config.faulty ∨ requester = (interface base n).recipient e := by
  by_cases bad : i ∈ a.config.faulty
  · exact Or.inl bad
  · right
    have intact := (h.taint i).mpr bad
    have response := ((mem_cancelResponders w e requester acks bounded i).mp member).2
    rcases response with faulty | owner
    · rw [intact] at faulty
      cases faulty
    · exact owner

theorem cancelled_root_represents {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (bounded : ∀ i ∈ acks, i < n) (i : Fin n) :
    RootRepresents ((cancelledWorld w e.val requester acks).roots i.val)
      ((cancelMany a.config e s (cancelResponders w e requester acks bounded)).roots i) := by
  rw [cancelMany_root]
  obtain ⟨policy, revoked, committed, cancelled⟩ := h.roots i
  by_cases good : Good a.config i
  · have intact := (h.taint i).mpr good
    by_cases active : i.val ∈ acks ∧ requester = e.val.action.actor
    · have member : i ∈ cancelResponders w e requester acks bounded := by
        exact (mem_cancelResponders w e requester acks bounded i).mpr ⟨active.1, Or.inr active.2⟩
      rw [if_pos ⟨good, member⟩]
      have contained : acks.contains i.val = true := by simpa using active.1
      simp only [cancelledWorld, contained, intact, Bool.not_false, Bool.and_self,
        active.2, beq_self_eq_true, if_true, RootRepresents]
      refine ⟨policy, revoked, committed, ?_⟩
      intro other
      simp only [Finset.mem_insert, List.mem_cons]
      rw [cancelled]
      exact or_congr Subtype.val_injective.eq_iff.symm Iff.rfl
    · have notMember : i ∉ cancelResponders w e requester acks bounded := by
        intro member
        have both := (mem_cancelResponders w e requester acks bounded i).mp member
        simp only [intact, Bool.false_eq_true, false_or] at both
        exact active both
      rw [if_neg (by intro both; exact notMember both.2)]
      simpa [cancelledWorld, intact, Bool.and_eq_true, active] using h.roots i
  · rw [if_neg (by intro both; exact good both.1)]
    have faulty : w.tainted i.val = true := by
      cases eq : w.tainted i.val with
      | false => exact False.elim (good ((h.taint i).mp eq))
      | true => rfl
    simpa [cancelledWorld, faulty] using h.roots i

theorem cancelled_certificates_aligned {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (bounded : ∀ i ∈ acks, i < n) :
    CertificatesAligned a (cancelledWorld w e.val requester acks)
      (cancelMany a.config e s (cancelResponders w e requester acks bounded)) := by
  constructor
  · intro cert member
    obtain ⟨index, old, bound⟩ := h.certificates.sound cert member
    exact ⟨index, by simpa using old, by simpa only [CertificateAt, cancelMany_certificates] using bound⟩
  · intro index old
    obtain ⟨cert, member, bound⟩ := h.certificates.complete index (by simpa using old)
    exact ⟨cert, member, by simpa only [CertificateAt, cancelMany_certificates] using bound⟩
  · exact h.certificates.unique

/-- Valid calls preserve every partial tombstone, independently of whether the
current-call reply count reaches the threshold. No new fault-response flag is added. -/
theorem cancelWith_preserves_alignment {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (valid : validPath w e.val = true) (nodup : acks.Nodup)
    (selected : ∀ i ∈ acks, i ∈ e.val.path) :
    let bounded := fun i hi => e.property.2 i (selected i hi)
    Aligned a (cancelWith w e.val requester acks).1
      (cancelMany a.config e s (cancelResponders w e requester acks bounded)) ∧
    Trace a.config s ((cancelResponders w e requester acks bounded).map
      (fun i => Event.cancelAck i e requester))
      (cancelMany a.config e s (cancelResponders w e requester acks bounded)) := by
  dsimp only
  rw [cancelWith_exact w e.val requester acks valid nodup selected]
  constructor
  · refine ⟨h.root_count, h.budget, h.quorum, h.revocation_quorum, ?_, ?_, h.taint,
      cancelled_root_represents a w s h e requester acks _, ?_,
      cancelled_certificates_aligned a w s h e requester acks _⟩
    · simpa [cancelledWorld] using h.actual_plant
    · simpa [cancelledWorld] using h.effective_policy
    · simpa using h.idle
  · apply cancelMany_trace
    · intro i member
      exact (mem_path e i).mpr (selected i.val ((mem_cancelResponders w e requester acks _ i).mp member).1)
    · exact cancel_responder_auth a w s h e requester acks _

/-- One-way only: the actual Boolean counts this call's replies, whereas the
common certificate accumulates distinct replies across all prior calls. -/
theorem true_cancel_implies_certificate {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (valid : validPath w e.val = true) (nodup : acks.Nodup)
    (selected : ∀ i ∈ acks, i ∈ e.val.path) (closed : (cancelWith w e.val requester acks).2 = true) :
    let bounded := fun i hi => e.property.2 i (selected i hi)
    Cancelled a.config (cancelMany a.config e s (cancelResponders w e requester acks bounded)) e := by
  dsimp only
  rw [cancelWith_exact w e.val requester acks valid nodup selected] at closed
  have enough := of_decide_eq_true closed
  rw [h.budget] at enough
  let bounded := fun i hi => e.property.2 i (selected i hi)
  let replies := cancelResponders w e requester acks bounded
  have distinct : replies.Nodup := cancelResponders_nodup w e requester acks bounded nodup
  have card : replies.toFinset.card =
      (acks.filter (fun i => w.tainted i || requester == e.val.action.actor)).length := by
    rw [List.toFinset_card_of_nodup distinct]
    exact cancelResponders_length w e requester acks bounded
  have sub : replies.toFinset ⊆ replies.toFinset ∪ s.cancelAcks e := Finset.subset_union_left
  have count := Finset.card_le_card sub
  unfold Cancelled
  rw [cancelMany_cancelAcks, if_pos rfl]
  change a.budget < (replies.toFinset ∪ s.cancelAcks e).card
  omega

/-- The B+1 count also forces this model's authenticated requester field to
match the original actor; bad acknowledgements alone cannot produce true. -/
theorem true_cancel_requester_matches {base n} (a : Authority base n)
    (w : ComposedExecution.World) (s : State (interface base n)) (h : Aligned a w s)
    (e : BoundedEnvelope n) (requester : String) (acks : List Nat)
    (closed : (cancelWith w e.val requester acks).2 = true) :
    requester = e.val.action.actor := by
  obtain ⟨valid, nodup, selected⟩ := true_cancel_outer_guards w e.val requester acks closed
  rw [cancelWith_exact w e.val requester acks valid nodup selected] at closed
  have enough := of_decide_eq_true closed
  rw [h.budget] at enough
  let bounded := fun i hi => e.property.2 i (selected i hi)
  let replies := cancelResponders w e requester acks bounded
  have distinct : replies.Nodup := cancelResponders_nodup w e requester acks bounded nodup
  have card : replies.toFinset.card =
      (acks.filter (fun i => w.tainted i || requester == e.val.action.actor)).length := by
    rw [List.toFinset_card_of_nodup distinct]
    exact cancelResponders_length w e requester acks bounded
  have large : a.config.budget < replies.toFinset.card := by
    change a.budget < replies.toFinset.card
    omega
  obtain ⟨i, member, good⟩ := good_member a.config replies.toFinset large
  rcases cancel_responder_auth a w s h e requester acks bounded i
      (List.mem_toFinset.mp member) with bad | owner
  · exact False.elim (good bad)
  · exact owner

#print axioms cancelWith_exact
#print axioms cancelWith_invalid_identity
#print axioms cancelWith_preserves_alignment
#print axioms true_cancel_implies_certificate
#print axioms true_cancel_requester_matches
end
end OperationalJoin.Offset
