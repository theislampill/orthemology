import AliasModel

namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

/-- Concrete first, abstract second. Concrete stores may have additional vetoes.
Only selected commitments may be used by a common path. -/
structure RootRefines {m} (I : Interface m) (i : Fin m)
    (concrete abstract : RootState I) : Prop where
  policy : abstract.descriptor = concrete.descriptor
  commitments : ∀ k, k ∈ abstract.commitments ↔
    k ∈ concrete.commitments ∧ i ∈ I.commandPath k
  revoked : concrete.revoked ⊆ abstract.revoked
  cancelled : abstract.cancelled ⊆ concrete.cancelled

structure Refines {m} {I : Interface m} (E : Environment I)
    (C : State I) (s : OperationalJoin.State I) : Prop where
  epoch : s.epoch = C.epoch
  pending : s.pending = C.pending
  acks : s.acks = C.acks
  certificates : s.certificates = C.certificates
  cancelAcks : s.cancelAcks = C.cancelAcks
  plant : s.plant = C.plant
  safe : s.damaged = false
  roots : ∀ i, Good E.labelConfig i → RootRefines I i (C.roots (E.rootOf i)) (s.roots i)

theorem initial_refines {m} {I : Interface m} (E : Environment I) (p : I.Plant) :
    Refines E (initial E p) (Initial E.labelConfig p) := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, ?_⟩
  intro i good
  refine ⟨rfl, ?_, ?_, ?_⟩
  · intro k; simp [initial, Initial]
  · exact Finset.Subset.refl _
  · exact Finset.Subset.refl _

theorem root_envelope_abstract {m} {I : Interface m} {i : Fin m}
    {z a : RootState I} (h : RootRefines I i z a)
    (p : I.Plant) (time : Nat) (k : I.Command) (who : I.Requester)
    (allowed : Envelope p time z k who) : Envelope p time a k who := by
  refine ⟨?_, ?_, ?_⟩
  · simpa only [h.policy] using allowed.1
  · exact fun revoked => allowed.2.1 (h.revoked revoked)
  · exact fun cancelled => allowed.2.2 (h.cancelled cancelled)

theorem concrete_envelope_abstract {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (good : Good E.labelConfig i) (time : Nat)
    (k : I.Command) (who : I.Requester)
    (allowed : Envelope C.plant time (C.roots (E.rootOf i)) k who) :
    Envelope s.plant time (s.roots i) k who := by
  rw [h.plant]
  exact root_envelope_abstract (h.roots i good) C.plant time k who allowed

theorem concrete_permits_abstract {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (i : Fin m) (good : Good E.labelConfig i) (time : Nat)
    (k : I.Command) (who : I.Requester) (selected : i ∈ I.commandPath k)
    (allowed : Permits C.plant time (C.roots (E.rootOf i)) k who) :
    Permits s.plant time (s.roots i) k who := by
  exact ⟨((h.roots i good).commitments k).mpr ⟨allowed.1, selected⟩,
    concrete_envelope_abstract h i good time k who allowed.2⟩

theorem concrete_lands_abstract {m} {I : Interface m} {E : Environment I}
    {C : State I} {s : OperationalJoin.State I} (h : Refines E C s)
    (time : Nat) (k : I.Command) (who : I.Requester) (allowed : Lands E C time k who) :
    OperationalJoin.Lands E.labelConfig s time k who := by
  refine ⟨allowed.1, ?_⟩
  intro i selected good
  exact concrete_permits_abstract h i good time k who selected (allowed.2 i selected good)

end
end SharedAlias
