import NativeRefinement
import SharedController

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface rootView)
noncomputable section
open Classical

/-- Raw finite root lists and accepted chosen list representatives give the
same source Boolean for the SAME complete ordered command. -/
theorem rootPermits_reification {m} (p : Plant) (time : Nat) (z : Root)
    (k : BoundedEnvelope m) (who : String) :
    ComposedExecution.rootPermits p time z k.val who =
      ComposedExecution.rootPermits p time (SharedAlias.Typed.rawRoot (rootView (n := m) z)) k.val who := by
  apply Bool.eq_iff_iff.mpr
  exact (OperationalJoin.Typed.root_gate_iff p time z (rootView z)
    (OperationalJoin.Typed.rootView_represents z) k who).symm.trans
      (OperationalJoin.Typed.root_gate_iff p time (SharedAlias.Typed.rawRoot (rootView (n := m) z)) (rootView z)
        (SharedAlias.Typed.rawRoot_represents (rootView z)) k who)

theorem faulty_exact {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (i : Fin m) :
    faulty D i = decide (E.rootOf i ∈ E.actualFaults) := by
  simp only [faulty, rootOf_matches D E matchD, ← matchD.faults, List.mem_toFinset]

/-- Exact live source Boolean equality, for true AND false badOpen, without
reachability or source-authentication assumptions. Those belong to effect safety. -/
theorem applied_exact_reference {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    applied D C k who time badOpen = SharedAlias.Progress.applied E (view C) k who time badOpen := by
  have gates : ∀ j ∈ k.val.path,
      ComposedExecution.gateOpen (gateWorld D C time C.defaultRoot.policy) k.val who badOpen j =
      ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E (view C) time) k.val who badOpen j := by
    intro j member
    have bound := k.property.2 j member
    let i : Fin m := ⟨j,bound⟩
    simp only [ComposedExecution.gateOpen, gateWorld, SharedAlias.Typed.gateWorld,
      dif_pos bound, faulty_exact D E matchD, rootOf_matches D E matchD, view]
    split
    · rfl
    · exact rootPermits_reification C.plant time (rootAt C (E.rootOf i)) k who
  have allEq :
      k.val.path.all (ComposedExecution.gateOpen (gateWorld D C time C.defaultRoot.policy) k.val who badOpen) =
      k.val.path.all (ComposedExecution.gateOpen (SharedAlias.Typed.gateWorld E (view C) time) k.val who badOpen) := by
    apply Bool.eq_iff_iff.mpr
    simp only [List.all_eq_true]
    constructor
    · intro all j member; rw [← gates j member]; exact all j member
    · intro all j member; rw [gates j member]; exact all j member
  have validEq : ComposedExecution.validPath (gateWorld D C time C.defaultRoot.policy) k.val =
      ComposedExecution.validPath (SharedAlias.Typed.gateWorld E (view C) time) k.val := by
    simp only [ComposedExecution.validPath, gateWorld, SharedAlias.Typed.gateWorld, matchD.quorum]
  simp only [applied, SharedAlias.Progress.applied, ComposedExecution.attempt, allEq, validEq]
  split <;> rfl

theorem attempt_exact_reference {m} (D : Routing m) (E : SharedAlias.Environment (interface m))
    (matchD : RoutingMatches D E) (C : FiniteState m) (k : BoundedEnvelope m)
    (who : String) (time : Nat) (badOpen : Bool) :
    view (attemptSlot D C k who time badOpen) =
      SharedAlias.Progress.attemptSlot E (view C) k who time badOpen := by
  cases h : applied D C k who time badOpen with
  | false =>
      have ref : SharedAlias.Progress.applied E (view C) k who time badOpen = false :=
        (applied_exact_reference D E matchD C k who time badOpen).symm.trans h
      simp only [rejected_identity D C k who time badOpen h, SharedAlias.Progress.attemptSlot,
        ref, Bool.false_eq_true, if_false]
  | true =>
      have ref : SharedAlias.Progress.applied E (view C) k who time badOpen = true :=
        (applied_exact_reference D E matchD C k who time badOpen).symm.trans h
      simp only [attempt_success_refines D C k who time badOpen h,
        SharedAlias.Progress.attemptSlot, ref, if_true]

end
end SharedAlias.Native
