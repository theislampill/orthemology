import ExecutableKernel

namespace SharedAlias.Executable.Fixture
open ComposedExecution

def target : TypedCriterionGuard.Target := ("fixture-repository", "pinned-commit", "source.md")
def before : ComposedExecution.Plant :=
  { source := ⟨target, [65,66,67], ["fixture-source"]⟩
    destination := "fixture-A"
    standard := "exact-source-recovery"
    draft := [65,66,67,10]
    draftRevision := 8
    draftHistory := [[88]]
    rule := .normalizedLF
    ruleVersion := 3
    ruleHistory := []
    unrelated := ["retain-custody"] }

def policy (scope : String) (epoch : Nat) : ComposedExecution.Policy :=
  { target, destination := "fixture-A", actor := "A", scope, epoch
    grant := some ⟨"A", "fixture-A", target, epoch, 0, 100, scope⟩ }

def source (epoch : Nat) : ComposedExecution.Policy :=
  policy (if epoch = 0 then "install-criterion" else "replace-derived") epoch

def installCommand : CriterionInstallation.InstallCommand :=
  { actor := "A", destination := "fixture-A", target
    expectedRule := .normalizedLF, expectedVersion := 3, authorizationEpoch := 0
    newRule := .exact, operation := "install-criterion", observedAt := 1, leaseEnd := 90 }

def installed : ComposedExecution.Plant :=
  { before with rule := .exact, ruleVersion := 4, ruleHistory := [.normalizedLF] }
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


def actor : Actor := ⟨source 0, before, "A", 2, 1000⟩
def action : Action := .install installCommand
def start : FiniteState 7 := initial (source 0) before

def withholding : List (Annotation 7) := (List.range 21).map fun n =>
  ⟨2+n, List.replicate 7 true, false, List.replicate 7 true⟩
def worstRouting : Routing 7 := ⟨[0,1], [none], 2,5,5⟩
def goodAliasRouting : Routing 7 := ⟨[0,1], [some 6], 2,5,5⟩

def specs : List (Spec 7) := (compileOrdered actor action sevenOrderedPaths withholding).getD []
def full : Outcome 7 := (runInitial worstRouting actor action sevenOrderedPaths withholding).getD ⟨start, []⟩
def prefix : Outcome 7 :=
  let r := runNative worstRouting actor.identity start (specs.take 20)
  ⟨r.state, List.replicate 7 .hold ++ r.events⟩
def repeated : Outcome 7 := runNative worstRouting actor.identity full.state specs

def installCount {m} : List (ServiceEvent m) → Nat
  | [] => 0
  | .land k _ _ :: rest =>
      (match k.val.action with | .install _ => 1 | .repair _ => 0) + installCount rest
  | _ :: rest => installCount rest

def repairCount {m} : List (ServiceEvent m) → Nat
  | [] => 0
  | .land k _ _ :: rest =>
      (match k.val.action with | .install _ => 0 | .repair _ => 1) + repairCount rest
  | _ :: rest => repairCount rest

def closeCount {m} (events : List (ServiceEvent m)) : Nat :=
  events.countP (fun e => match e with | .close _ => true | _ => false)

def firstLandingNonce {m} : List (ServiceEvent m) → Option Nat
  | [] => none
  | .land k _ _ :: _ => some k.val.nonce
  | _ :: rest => firstLandingNonce rest

def expired : Outcome 7 :=
  (runInitial worstRouting actor action sevenOrderedPaths
    (withholding.map (fun a => { a with time := 90 }))).getD ⟨start, []⟩

def firstCommand : Command 7 := issueOrdered actor action installed 0 ⟨[0,1,2,3,4], by decide⟩
def aliasCancellation : FiniteState 7 := cancelSlot goodAliasRouting start 0 firstCommand "A" false

def checks : List (String × Bool) :=
  [("program_size", decide (specs.length = 21)),
   ("first_twenty", decide (prefix.events.length = 247 ∧ installCount prefix.events = 0 ∧ repairCount prefix.events = 0 ∧ prefix.state.plant = before)),
   ("full_exact_effect", decide (full.events.length = 259 ∧ installCount full.events = 1 ∧ repairCount full.events = 0 ∧ full.state.plant = installed)),
   ("last_path_first_landing", decide (firstLandingNonce full.events = some 1021)),
   ("real_closure_count", decide (closeCount full.events = 21 ∧ closeCount prefix.events = 20)),
   ("failed_prefix_stores", decide (0 < prefix.state.rootRows.length ∧ prefix.state.cancelRows.length = 100)),
   ("repeat_no_effect", decide (installCount repeated.events = 0 ∧ repeated.state.plant = installed)),
   ("expired_no_effect", decide (expired.events.length = 259 ∧ installCount expired.events = 0 ∧ expired.state.plant = before)),
   ("missing_annotations", (runInitial worstRouting actor action sevenOrderedPaths (withholding.take 20)).isNone),
   ("extra_annotations", (runInitial worstRouting actor action sevenOrderedPaths (withholding ++ withholding.take 1)).isNone),
   ("bad_bit_array", (runInitial worstRouting actor action sevenOrderedPaths
      (withholding.modifyHead (fun a => { a with cancelBits := [] }))).isNone),
   ("proposal_none", (runInitial worstRouting { actor with observedTime := 0 } action sevenOrderedPaths withholding).isNone),
   ("shared_veto_single_receipt", decide (firstCommand.val ∈ (rootAt aliasCancellation (rootOf goodAliasRouting 1)).cancelled ∧
      0 ∈ receipts aliasCancellation firstCommand.val ∧ 1 ∉ receipts aliasCancellation firstCommand.val)),
   ("duplicate_receipts", !(closed worstRouting { start with cancelRows := [(firstCommand.val, [0,0,0])] } firstCommand)),
   ("good_alias_world", match runInitial goodAliasRouting actor action sevenOrderedPaths withholding with
      | none => false
      | some r => decide (r.state.plant = installed ∧ installCount r.events = 1 ∧ firstLandingNonce r.events = some 1001)),
   ("bad_cancel_withholding", match runInitial worstRouting actor action sevenOrderedPaths
      (withholding.map (fun a => { a with prepareBits := List.replicate 7 false, cancelBits := List.replicate 7 false })) with
      | none => false
      | some r => decide (r.state.plant = installed ∧ closeCount r.events = 21))]

end SharedAlias.Executable.Fixture
