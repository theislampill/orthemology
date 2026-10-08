import NativePrimitives

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)

/-- An explicit public ordering, not Finset.toList and not a root-map query. -/
abbrev OrderedPath (m : Nat) := { labels : List (Fin m) // labels.Nodup }

def orderedLabelList {m} (path : OrderedPath m) : List Nat := path.val.map Fin.val

theorem orderedLabelList_nodup {m} (path : OrderedPath m) : (orderedLabelList path).Nodup :=
  path.property.map Fin.val_injective

theorem orderedLabelList_bounded {m} (path : OrderedPath m) : ∀ i ∈ orderedLabelList path, i < m := by
  intro i member
  obtain ⟨j, _, rfl⟩ := List.mem_map.mp member
  exact j.isLt

def issueOrdered {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (path : OrderedPath m) : BoundedEnvelope m :=
  ⟨⟨action, next, actor.nonce + n + 1, orderedLabelList path⟩,
    orderedLabelList_nodup path, orderedLabelList_bounded path⟩

/-- Actor-only computation. No hidden environment, actual state, clock,
service response or acknowledgement is accepted by this function. -/
def orderedCommands {m} (actor : Actor) (action : Action) (next : Plant) :
    Nat → List (OrderedPath m) → List (BoundedEnvelope m)
  | _, [] => []
  | n, path :: rest => issueOrdered actor action next n path :: orderedCommands actor action next (n+1) rest

def orderedProgram {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m)) :
    Option (List (BoundedEnvelope m)) :=
  (ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action).map
    (fun next => orderedCommands actor action next 0 paths)

/-- Explicit finite service data. The checked annotation constructor below
requires exactly m prepare bits and m cancel bits at every trial. -/
structure Annotation (m : Nat) where
  time : Nat
  prepareBits : List Bool
  openGate : Bool
  cancelBits : List Bool

def annotationValid {m} (a : Annotation m) : Bool :=
  decide (a.prepareBits.length = m ∧ a.cancelBits.length = m)

def prepareReply {m} (a : Annotation m) (i : Fin m) : Bool := a.prepareBits.getD i.val false
def cancelReply {m} (a : Annotation m) (i : Fin m) : Bool := a.cancelBits.getD i.val false

structure NativeSpec (m : Nat) where
  command : BoundedEnvelope m
  annotation : Annotation m

/-- Exact-length consumption. BOTH missing and excess annotations reject;
no zip/truncation or fabricated clock sample changes the public program. -/
def annotate {m} : List (BoundedEnvelope m) → List (Annotation m) → Option (List (NativeSpec m))
  | [], [] => some []
  | k :: commands, a :: annotations =>
      if annotationValid a then (annotate commands annotations).map (fun rest => ⟨k,a⟩ :: rest)
      else none
  | _, _ => none

def compileOrdered {m} (actor : Actor) (action : Action) (paths : List (OrderedPath m))
    (annotations : List (Annotation m)) : Option (List (NativeSpec m)) := do
  let commands ← orderedProgram actor action paths
  annotate commands annotations

@[simp] theorem orderedCommands_length {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (paths : List (OrderedPath m)) :
    (orderedCommands actor action next n paths).length = paths.length := by
  induction paths generalizing n with
  | nil => rfl
  | cons path rest ih => simp only [orderedCommands, List.length_cons, ih]

theorem issueOrdered_source_proposal {m} (actor : Actor) (action : Action) (next : Plant)
    (n : Nat) (path : OrderedPath m)
    (proposal : ComposedExecution.localStep actor.observedPlant actor.policy actor.observedTime action = some next) :
    ComposedExecution.propose { actor with nonce := actor.nonce+n } action (orderedLabelList path) =
      some (issueOrdered actor action next n path).val := by
  simp [ComposedExecution.propose, proposal, issueOrdered]

theorem annotate_erases {m} (commands : List (BoundedEnvelope m)) (annotations : List (Annotation m))
    (specs : List (NativeSpec m)) (success : annotate commands annotations = some specs) :
    specs.map NativeSpec.command = commands := by
  induction commands generalizing annotations specs with
  | nil =>
      cases annotations with
      | nil => cases success; rfl
      | cons a rest => cases success
  | cons k commands ih =>
      cases annotations with
      | nil => cases success
      | cons a annotations =>
          simp only [annotate] at success
          split at success
          · cases rest : annotate commands annotations with
            | none => simp only [rest, Option.map_none] at success; cases success
            | some later =>
                have same : { command := k, annotation := a } :: later = specs := by
                  rw [rest] at success
                  exact Option.some.inj success
                subst specs
                simp only [List.map_cons, ih annotations later rest]
          · cases success

theorem annotate_exact_length {m} (commands : List (BoundedEnvelope m)) (annotations : List (Annotation m))
    (specs : List (NativeSpec m)) (success : annotate commands annotations = some specs) :
    annotations.length = commands.length := by
  induction commands generalizing annotations specs with
  | nil => cases annotations <;> simp_all [annotate]
  | cons k commands ih =>
      cases annotations with
      | nil => cases success
      | cons a annotations =>
          simp only [annotate] at success
          split at success
          · cases rest : annotate commands annotations with
            | none => simp only [rest, Option.map_none] at success; cases success
            | some later =>
                have h := ih annotations later rest
                simpa only [List.length_cons] using congrArg Nat.succ h
          · cases success

theorem annotate_mismatch_rejects {m} (commands : List (BoundedEnvelope m))
    (annotations : List (Annotation m)) (wrong : annotations.length ≠ commands.length) :
    annotate commands annotations = none := by
  cases h : annotate commands annotations with
  | none => rfl
  | some specs => exact False.elim (wrong (annotate_exact_length commands annotations specs h))

theorem annotate_complete {m} (commands : List (BoundedEnvelope m))
    (annotations : List (Annotation m)) (lengths : annotations.length = commands.length)
    (valid : ∀ a ∈ annotations, annotationValid a = true) :
    ∃ specs, annotate commands annotations = some specs := by
  induction commands generalizing annotations with
  | nil =>
      have empty : annotations = [] := List.length_eq_zero_iff.mp lengths
      subst annotations
      exact ⟨[], rfl⟩
  | cons k commands ih =>
      cases annotations with
      | nil => simp at lengths
      | cons a annotations =>
          have remaining : annotations.length = commands.length := Nat.succ.inj lengths
          obtain ⟨specs, later⟩ := ih annotations remaining
            (fun x member => valid x (List.mem_cons_of_mem a member))
          refine ⟨⟨k,a⟩ :: specs, ?_⟩
          simp only [annotate, valid a (by simp), if_true, later]
          rfl

theorem annotate_pairwise {m} (commands : List (BoundedEnvelope m))
    (annotations : List (Annotation m)) (specs : List (NativeSpec m))
    (success : annotate commands annotations = some specs)
    (fresh : commands.Pairwise (fun a b => a ≠ b)) :
    specs.Pairwise (fun a b => a.command ≠ b.command) := by
  rw [← annotate_erases commands annotations specs success] at fresh
  exact List.pairwise_map.mp fresh

theorem annotate_member_annotation {m} (commands : List (BoundedEnvelope m))
    (annotations : List (Annotation m)) (specs : List (NativeSpec m))
    (success : annotate commands annotations = some specs) :
    specs.map NativeSpec.annotation = annotations := by
  induction commands generalizing annotations specs with
  | nil =>
      cases annotations with
      | nil => cases success; rfl
      | cons a rest => cases success
  | cons k commands ih =>
      cases annotations with
      | nil => cases success
      | cons a annotations =>
          simp only [annotate] at success
          split at success
          · cases later : annotate commands annotations with
            | none => simp only [later] at success; cases success
            | some rest =>
                have same : { command := k, annotation := a } :: rest = specs := by
                  rw [later] at success
                  exact Option.some.inj success
                subst specs
                simp only [List.map_cons, ih annotations rest later]
          · cases success

/-- Service decorations cannot change any complete command emitted by the
actor. This is public-program independence, not transcript opacity. -/
theorem compileOrdered_public_program {m} (actor : Actor) (action : Action)
    (paths : List (OrderedPath m)) (annotations : List (Annotation m)) (specs : List (NativeSpec m))
    (success : compileOrdered actor action paths annotations = some specs) :
    orderedProgram actor action paths = some (specs.map NativeSpec.command) := by
  unfold compileOrdered at success
  cases program : orderedProgram actor action paths with
  | none => simp only [program, Option.bind_none] at success; cases success
  | some commands =>
      simp only [program, Option.bind_some] at success
      rw [annotate_erases commands annotations specs success]

/-- Two arbitrary successful service decorations expose exactly the same
complete actor command list. This says nothing about visible service replies. -/
theorem annotation_noninterference {m} (actor : Actor) (action : Action)
    (paths : List (OrderedPath m)) (first second : List (Annotation m))
    (xs ys : List (NativeSpec m))
    (hx : compileOrdered actor action paths first = some xs)
    (hy : compileOrdered actor action paths second = some ys) :
    xs.map NativeSpec.command = ys.map NativeSpec.command := by
  have x := compileOrdered_public_program actor action paths first xs hx
  have y := compileOrdered_public_program actor action paths second ys hy
  exact Option.some.inj (x.symm.trans y)

end SharedAlias.Native
