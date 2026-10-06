import SharedTrial

namespace SharedAlias.Progress
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path)
noncomputable section
open Classical

/-- This premise describes protected service state, never an actor observation.
It mentions full cancellation identity and the command's exact epoch. -/
def Clear {m} {I : Interface m} (E : Environment I) (C : SharedAlias.State I)
    (k : I.Command) (policy : I.Policy) : Prop :=
  ∀ i, Good E.labelConfig i →
    (C.roots (E.rootOf i)).descriptor = policy ∧
    I.commandEpoch k ∉ (C.roots (E.rootOf i)).revoked ∧
    k ∉ (C.roots (E.rootOf i)).cancelled

theorem prepareSlot_clear {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k checked : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Bool) (policy : I.Policy) (clear : Clear E C checked policy) :
    Clear E (prepareSlot E C i k who time badReply) checked policy := by
  intro j good
  unfold prepareSlot
  split
  · by_cases same : E.rootOf j = E.rootOf i
    · simpa [SharedAlias.prepare, SharedAlias.setRoot, same] using clear j good
    · simpa [SharedAlias.prepare, SharedAlias.setRoot, Function.update_of_ne same] using clear j good
  · exact clear j good

theorem cancelSlot_clear_other {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (i : Fin m) (k checked : I.Command) (who : I.Requester)
    (badReply : Bool) (policy : I.Policy) (different : checked ≠ k)
    (clear : Clear E C checked policy) :
    Clear E (cancelSlot E C i k who badReply) checked policy := by
  intro j goodJ
  unfold cancelSlot
  split
  · by_cases goodI : Good E.labelConfig i
    · by_cases same : E.rootOf j = E.rootOf i
      · simpa only [SharedAlias.cancelAck, if_pos goodI, same, Function.update_self, Finset.mem_insert, different, false_or] using clear j goodJ
      · simpa only [SharedAlias.cancelAck, if_pos goodI, Function.update_of_ne same] using clear j goodJ
    · simpa only [SharedAlias.cancelAck, if_neg goodI] using clear j goodJ
  · exact clear j goodJ

theorem preparePath_clear {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k checked : I.Command) (who : I.Requester)
    (time : Nat) (badReply : Fin m → Bool) (policy : I.Policy) (clear : Clear E C checked policy) :
    Clear E (preparePath E C k who time badReply) checked policy :=
  serviceList_invariant _ (fun D => Clear E D checked policy)
    (fun D i h => prepareSlot_clear E D i k checked who time (badReply i) policy h) _ _ clear

theorem cancelPath_clear_other {m} {I : Interface m} (E : Environment I)
    (C : SharedAlias.State I) (k checked : I.Command) (who : I.Requester)
    (badReply : Fin m → Bool) (policy : I.Policy) (different : checked ≠ k)
    (clear : Clear E C checked policy) :
    Clear E (cancelPath E C k who badReply) checked policy :=
  serviceList_invariant _ (fun D => Clear E D checked policy)
    (fun D i h => cancelSlot_clear_other E D i k checked who (badReply i) policy different h) _ _ clear

theorem trial_clear_other {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (k checked : BoundedEnvelope m) (who : String)
    (time : Nat) (bad : Replies m) (policy : ComposedExecution.Policy)
    (different : checked ≠ k) (clear : Clear E C checked policy) :
    Clear E (trial E C k who time bad) checked policy := by
  apply cancelPath_clear_other E _ k checked who bad.cancel policy different
  have prepared := preparePath_clear E C k checked who time bad.prepare policy clear
  unfold attemptSlot
  split
  · exact prepared
  · exact prepared

/-- Public request identity plus environmental time/replies. The actor schedule
is just `command`; neither hidden-world data nor receipts affect its order. -/
structure TrialSpec (m : Nat) where
  command : BoundedEnvelope m
  time : Nat
  replies : Replies m

def run {m} (E : Environment (interface m)) (C : SharedAlias.State (interface m))
    (who : String) : List (TrialSpec m) → SharedAlias.State (interface m)
  | [] => C
  | spec :: rest => run E (trial E C spec.command who spec.time spec.replies) who rest

theorem run_trace {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (who : String) (specs : List (TrialSpec m))
    (valid : ∀ s ∈ specs, ValidPath E.labelConfig s.command)
    (auth : ∀ s ∈ specs, who = s.command.val.action.actor) :
    ∃ events, SharedAlias.Trace E C events (run E C who specs) ∧
      events.length = specs.length * (2 * E.q + 2) := by
  induction specs generalizing C with
  | nil => exact ⟨[], .nil C, by simp⟩
  | cons s specs ih =>
      obtain ⟨first, firstTrace, firstSize⟩ := trial_trace E C s.command who s.time s.replies
        (valid s (by simp)) (auth s (by simp))
      obtain ⟨later, laterTrace, laterSize⟩ := ih
        (trial E C s.command who s.time s.replies)
        (fun x hx => valid x (List.mem_cons_of_mem s hx))
        (fun x hx => auth x (List.mem_cons_of_mem s hx))
      refine ⟨first ++ later, trace_append firstTrace laterTrace, ?_⟩
      simp only [List.length_append, List.length_cons, firstSize, laterSize]
      simp only [Nat.add_mul, Nat.one_mul]
      omega

/-- A run-all controller does not have to recognize its first successful reply. -/
theorem run_preserves_successor {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (who : String) (specs : List (TrialSpec m))
    (next : ComposedExecution.Plant)
    (successors : ∀ s ∈ specs, s.command.val.successor = next) (same : C.plant = next) :
    (run E C who specs).plant = next := by
  induction specs generalizing C with
  | nil => exact same
  | cons s specs ih =>
      apply ih (trial E C s.command who s.time s.replies)
      · intro x hx; exact successors x (List.mem_cons_of_mem s hx)
      · rcases trial_plant_cases E C s.command who s.time s.replies with untouched | landed
        · exact untouched.trans same
        · exact landed.trans (successors s (by simp))

/-- Constructive progress of the actual shared-store interpreter. No successful
trace occurs as a premise. The hit is a combinatorial all-good scheduled path;
its preparation and live landing are derived from local source admission. -/
theorem run_progress {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (who : String) (specs : List (TrialSpec m))
    (policy : ComposedExecution.Policy) (next : ComposedExecution.Plant)
    (valid : ∀ s ∈ specs, ValidPath E.labelConfig s.command)
    (auth : ∀ s ∈ specs, who = s.command.val.action.actor)
    (successors : ∀ s ∈ specs, s.command.val.successor = next)
    (fresh : specs.Pairwise (fun a b => a.command ≠ b.command))
    (clear : ∀ s ∈ specs, Clear E C s.command policy)
    (work : ∀ s ∈ specs,
      ComposedExecution.localStep C.plant policy s.time s.command.val.action = some s.command.val.successor)
    (hit : ∃ s ∈ specs, ∀ i ∈ path s.command, Good E.labelConfig i) :
    (run E C who specs).plant = next := by
  induction specs generalizing C with
  | nil => simp at hit
  | cons s specs ih =>
      let D := trial E C s.command who s.time s.replies
      by_cases done : D.plant = next
      · exact run_preserves_successor E D who specs next
          (fun x hx => successors x (List.mem_cons_of_mem s hx)) done
      · have unchanged : D.plant = C.plant := by
          rcases trial_plant_cases E C s.command who s.time s.replies with old | landed
          · exact old
          · exact False.elim (done (landed.trans (successors s (by simp))))
        have pair := List.pairwise_cons.mp fresh
        have remainingHit : ∃ x ∈ specs, ∀ i ∈ path x.command, Good E.labelConfig i := by
          obtain ⟨x, member, allGood⟩ := hit
          rcases List.mem_cons.mp member with same | later
          · subst x
            have ready : ∀ i, Good E.labelConfig i →
                Envelope C.plant s.time (C.roots (E.rootOf i)) s.command who := by
              intro i good
              obtain ⟨descriptor, revoked, cancelled⟩ := clear s (by simp) i good
              exact ⟨⟨auth s (by simp), by simpa only [descriptor] using work s (by simp)⟩,
                revoked, cancelled⟩
            have actual := trial_all_good E C s.command who s.time s.replies
              (valid s (by simp)) allGood ready
            exact False.elim (done (actual.trans (successors s (by simp))))
          · exact ⟨x, later, allGood⟩
        apply ih D
          (fun x hx => valid x (List.mem_cons_of_mem s hx))
          (fun x hx => auth x (List.mem_cons_of_mem s hx))
          (fun x hx => successors x (List.mem_cons_of_mem s hx)) pair.2
        · intro x hx
          exact trial_clear_other E C s.command x.command who s.time s.replies policy
            (Ne.symm (pair.1 x hx)) (clear x (List.mem_cons_of_mem s hx))
        · intro x hx
          simpa only [unchanged] using work x (List.mem_cons_of_mem s hx)
        · exact remainingHit

end
end SharedAlias.Progress
