import NativeOrderedProgram
import FinitePortfolio

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

/-- A finite literal public ordering fixed independently of every hidden world. -/
def sevenOrderedPaths : List (OrderedPath 7) :=
  [⟨[0,1,2,3,4], by decide⟩,
   ⟨[0,1,2,3,5], by decide⟩,
   ⟨[0,1,2,3,6], by decide⟩,
   ⟨[0,1,2,4,5], by decide⟩,
   ⟨[0,1,2,4,6], by decide⟩,
   ⟨[0,1,2,5,6], by decide⟩,
   ⟨[0,1,3,4,5], by decide⟩,
   ⟨[0,1,3,4,6], by decide⟩,
   ⟨[0,1,3,5,6], by decide⟩,
   ⟨[0,1,4,5,6], by decide⟩,
   ⟨[0,2,3,4,5], by decide⟩,
   ⟨[0,2,3,4,6], by decide⟩,
   ⟨[0,2,3,5,6], by decide⟩,
   ⟨[0,2,4,5,6], by decide⟩,
   ⟨[0,3,4,5,6], by decide⟩,
   ⟨[1,2,3,4,5], by decide⟩,
   ⟨[1,2,3,4,6], by decide⟩,
   ⟨[1,2,3,5,6], by decide⟩,
   ⟨[1,2,4,5,6], by decide⟩,
   ⟨[1,3,4,5,6], by decide⟩,
   ⟨[2,3,4,5,6], by decide⟩]

theorem sevenOrderedPaths_length : sevenOrderedPaths.length = 21 := rfl

theorem sevenOrderedPaths_lengths : ∀ p ∈ sevenOrderedPaths, p.val.length = 5 := by
  intro p member
  simp only [sevenOrderedPaths, List.mem_cons, List.not_mem_nil, or_false] at member
  rcases member with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> rfl

/-- Pointwise portfolio support equality preserves the trial index. It does
not identify ordered full commands with predecessor choice-ordered commands. -/
theorem sevenOrderedPaths_supports :
    sevenOrderedPaths.map (fun p => p.val.toFinset) = SharedAlias.Progress.sevenPaths := by rfl

noncomputable section
open Classical

theorem issueOrdered_support {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (p : OrderedPath m) :
    OperationalJoin.Typed.path (issueOrdered actor action next n p) = p.val.toFinset := by
  ext i
  simp only [OperationalJoin.Typed.mem_path, issueOrdered, orderedLabelList, List.mem_toFinset,
    List.mem_map]
  constructor
  · rintro ⟨j, member, same⟩
    have equal : j = i := Fin.ext same
    simpa only [equal] using member
  · intro member; exact ⟨i, member, rfl⟩

theorem orderedCommands_member {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (paths : List (OrderedPath m)) (k : BoundedEnvelope m)
    (member : k ∈ orderedCommands actor action next n paths) :
    ∃ j p, n ≤ j ∧ j < n + paths.length ∧ p ∈ paths ∧ k = issueOrdered actor action next j p := by
  induction paths generalizing n with
  | nil => cases member
  | cons p paths ih =>
      rcases List.mem_cons.mp member with rfl | later
      · exact ⟨n, p, le_rfl, by simp, by simp, rfl⟩
      · obtain ⟨j, q, lower, upper, inPaths, same⟩ := ih (n+1) later
        exact ⟨j, q, by omega, by simp only [List.length_cons]; omega,
          List.mem_cons_of_mem p inPaths, same⟩

theorem orderedCommands_fresh {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (paths : List (OrderedPath m)) :
    (orderedCommands actor action next n paths).Pairwise (fun a b => a ≠ b) := by
  induction paths generalizing n with
  | nil => exact .nil
  | cons p paths ih =>
      apply List.pairwise_cons.mpr
      constructor
      · intro k member same
        obtain ⟨j, q, lower, _, _, command⟩ := orderedCommands_member actor action next (n+1) paths k member
        have nonces := congrArg (fun c : BoundedEnvelope m => c.val.nonce) same
        simp only [command, issueOrdered] at nonces
        omega
      · exact ih (n+1)

theorem orderedCommands_has_path {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (paths : List (OrderedPath m)) (p : OrderedPath m) (member : p ∈ paths) :
    ∃ k ∈ orderedCommands actor action next n paths, OperationalJoin.Typed.path k = p.val.toFinset := by
  induction paths generalizing n with
  | nil => cases member
  | cons q paths ih =>
      rcases List.mem_cons.mp member with rfl | later
      · exact ⟨_, List.mem_cons_self, issueOrdered_support actor action next n p⟩
      · obtain ⟨k, hk, same⟩ := ih (n+1) later
        exact ⟨k, List.mem_cons_of_mem _ hk, same⟩

theorem sevenOrderedPaths_hit (E : SharedAlias.Environment (interface 7)) (q : E.q = 5) :
    ∃ p ∈ sevenOrderedPaths, ∀ i ∈ p.val, OperationalJoin.Good E.labelConfig i := by
  obtain ⟨P, member, good⟩ := SharedAlias.Progress.sevenPaths_hit E q
  rw [← sevenOrderedPaths_supports] at member
  obtain ⟨p, hp, same⟩ := List.mem_map.mp member
  refine ⟨p, hp, ?_⟩
  intro i hi
  apply good i
  rw [← same]
  exact List.mem_toFinset.mpr hi

end
end SharedAlias.Native
