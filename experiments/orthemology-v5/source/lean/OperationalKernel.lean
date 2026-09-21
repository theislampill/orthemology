/-
Operational model for the SAME v4 continuation. AUTHORed, NOT kernel-checked.
This is a universe-polymorphic typed operation schema. The Python engine realises
its serialisable interface fragment, with additional resource refusals and an
issued-ticket registry. No arbitrary Lean type is claimed to have a JSON encoding.
The model's licence test is finite and checks BOTH dependency coverage and stamps.
A separate source/refinement argument is required for the actual JSON parser.
-/
import FiniteBridge

namespace OrthemologyV4
open OrthemologyV2 OrthemologyV3
universe u

structure Stamp where
  version : Nat
  enabled : Bool
  deriving DecidableEq, Repr

def Context := Nat → Stamp

def openContext : Context := fun _ => ⟨0, true⟩
def closedContext : Context := fun _ => ⟨0, false⟩

def revise (g : Context) (key : Nat) (permission : Bool) : Context :=
  fun j => if j = key then ⟨Nat.succ (g key).version, permission⟩ else g j

inductive Plan : Type u → Type u → Type (u+1) where
  | identity (A : Type u) : Plan A A
  | copy (A : Type u) : Plan A (A × A)
  | first (A B : Type u) : Plan (A × B) A
  | second (A B : Type u) : Plan (A × B) B
  | succ : Plan (ULift.{u} Nat) (ULift.{u} Nat)
  | isZero : Plan (ULift.{u} Nat) (ULift.{u} Bool)
  | negate : Plan (ULift.{u} Bool) (ULift.{u} Bool)
  | compose {A B C : Type u} : Plan A B → Plan B C → Plan A C
  | parallel {A B C D : Type u} : Plan A B → Plan C D → Plan (A × C) (B × D)
  | source (A B : TypeCode) (v : Checked) (arrow : v.ty = .arrow A B) :
      Plan (ULift.{u} (El (interpret A (fun _ => Code.top))))
        (ULift.{u} (El (interpret B (fun _ => Code.top))))

def dependencies {A B : Type u} : Plan A B → List Nat
  | .identity _ | .copy _ | .first _ _ | .second _ _ => [0]
  | .succ => [1]
  | .isZero => [2]
  | .negate => [3]
  | .source _ _ _ _ => [4]
  | .compose p q | .parallel p q => 0 :: (dependencies p ++ dependencies q)

theorem checked_source_application (A B : TypeCode) (v : Checked)
    (ht : v.ty = .arrow A B) (x : El (interpret A (fun _ => Code.top))) :
    (interpret B (fun _ => Code.top)).accepts (.app v.term x.val) := by
  have h := OrthemologyV3.checked_sound v (fun _ => Code.top)
  rw [ht] at h
  exact h x.val x.property

def evaluate {A B : Type u} : Plan A B → A → B
  | .identity _, x => x
  | .copy _, x => (x,x)
  | .first _ _, x => x.1
  | .second _ _, x => x.2
  | .succ, x => ⟨x.down + 1⟩
  | .isZero, x => ⟨decide (x.down = 0)⟩
  | .negate, x => ⟨!x.down⟩
  | .compose p q, x => evaluate q (evaluate p x)
  | .parallel p q, x => (evaluate p x.1, evaluate q x.2)
  | .source A B v h, x =>
      ⟨⟨.app v.term x.down.val, checked_source_application A B v h x.down⟩⟩

structure Licence (A B : Type u) where
  plan : Plan A B
  bindings : List (Nat × Stamp)

def ticket {A B : Type u} (g : Context) (p : Plan A B) : Licence A B :=
  ⟨p, (dependencies p).map (fun k => (k,g k))⟩

def Good {A B : Type u} (g : Context) (l : Licence A B) : Prop :=
  l.bindings.map Prod.fst = dependencies l.plan ∧
  ∀ p ∈ l.bindings, p.2.enabled = true ∧ g p.1 = p.2

def checkLicence {A B : Type u} (g : Context) (l : Licence A B) : Bool :=
  decide (l.bindings.map Prod.fst = dependencies l.plan) &&
    l.bindings.all (fun p => p.2.enabled && decide (g p.1 = p.2))

theorem checker_sound {A B : Type u} (g : Context) (l : Licence A B) :
    checkLicence g l = true ↔ Good g l := by
  simp [checkLicence, Good, Bool.and_eq_true, List.all_eq_true]

def issue {A B : Type u} (g : Context) (p : Plan A B) : Option (Licence A B) :=
  let l := ticket g p
  if checkLicence g l then some l else none

def execute {A B : Type u} (g : Context) (l : Licence A B) (x : A) : Option B :=
  if checkLicence g l then some (evaluate l.plan x) else none

theorem execution_implies_checked {A B : Type u} (g : Context) (l : Licence A B)
    (x : A) (y : B) (h : execute g l x = some y) : checkLicence g l = true := by
  unfold execute at h
  split at h
  · assumption
  · cases h

theorem ticket_good {A B : Type u} (g : Context) (p : Plan A B)
    (allowed : ∀ k ∈ dependencies p, (g k).enabled = true) : Good g (ticket g p) := by
  constructor
  · simp [ticket, List.map_map]
  · intro x hx
    obtain ⟨k,hk,rfl⟩ := List.mem_map.mp hx
    exact ⟨allowed k hk,rfl⟩

theorem all_open_checked {A B : Type u} (p : Plan A B) :
    checkLicence openContext (ticket openContext p) = true :=
  (checker_sound _ _).mpr (ticket_good _ _ (fun _ _ => rfl))

theorem all_open_execute {A B : Type u} (p : Plan A B) (x : A) :
    execute openContext (ticket openContext p) x = some (evaluate p x) := by
  simp [execute, all_open_checked]

def Agree (g h : Context) (ks : List Nat) : Prop := ∀ k ∈ ks, g k = h k

theorem revision_stability {A B : Type u} (g h : Context) (l : Licence A B)
    (good : Good g l) (same : Agree g h (dependencies l.plan)) : Good h l := by
  refine ⟨good.1, ?_⟩
  intro p hp
  have hk : p.1 ∈ dependencies l.plan := by
    rw [←good.1]
    exact List.mem_map.mpr ⟨p,hp,rfl⟩
  exact ⟨(good.2 p hp).1, (same p.1 hk).symm.trans (good.2 p hp).2⟩

theorem relevant_revision_invalidates {A B : Type u} (g : Context) (l : Licence A B)
    (good : Good g l) (k : Nat) (s : Stamp) (hk : (k,s) ∈ l.bindings) (b : Bool) :
    ¬ Good (revise g k b) l := by
  intro after
  have beforeEq : g k = s := (good.2 (k,s) hk).2
  have afterEq : revise g k b k = s := (after.2 (k,s) hk).2
  have eqStamp : revise g k b k = g k := afterEq.trans beforeEq.symm
  have eqVersion : Nat.succ (g k).version = (g k).version := by
    simpa [revise] using congrArg Stamp.version eqStamp
  exact Nat.succ_ne_self _ eqVersion

/-- Universe-polymorphic SCHEMA reach, not a universal JSON encoding theorem. -/
theorem parametric_reach (A : Type u) (x : A) :
    execute openContext (ticket openContext (Plan.copy A)) x = some (x,x) :=
  all_open_execute _ _

theorem useful_nonidentity :
    execute openContext (ticket openContext Plan.succ) (ULift.up 2) = some (ULift.up 3) := rfl

theorem distinguishable_results :
    execute openContext (ticket openContext Plan.isZero) (ULift.up 0) = some (ULift.up true) ∧
    execute openContext (ticket openContext Plan.isZero) (ULift.up 1) = some (ULift.up false) := ⟨rfl,rfl⟩

theorem composition_works {A B C : Type u} (p : Plan A B) (q : Plan B C) (x : A) :
    execute openContext (ticket openContext (Plan.compose p q)) x =
      some (evaluate q (evaluate p x)) := all_open_execute _ _

theorem source_program_exact (A B : TypeCode) (v : Checked) (ht : v.ty = .arrow A B)
    (x : ULift.{u} (El (interpret A (fun _ => Code.top)))) :
    (evaluate (Plan.source A B v ht) x).down.val = .app v.term x.down.val := rfl

theorem internal_source_self_instantiation (B : Code → Code) (t : El (Code.all B)) :
    (OrthemologyV2.selfInstantiate t).val = t.val := rfl

/-- The API names callable operations independently of any SCUU assertion. -/
structure API where
  State : Type
  Handle : Type u → Type u → Type (u+1)
  check : {A B : Type u} → State → Handle A B → Bool
  invoke : {A B : Type u} → State → Handle A B → A → Option B
  change : State → Nat → Bool → State

def operationalAPI : API.{u} where
  State := Context
  Handle := Licence
  check := checkLicence
  invoke := execute
  change := revise

/-- A positive specification: it requires an actual embedding of EVERY plan in
this declared grammar, including nonidentity, composition and source operations;
a reject-all system cannot satisfy it. It also demands adding and revoking a
concrete authority. It does not assert scope beyond this schema. -/
def OWOU (O : API.{u}) : Prop :=
  (∃ g : O.State, ∃ embed : {A B : Type u} → Plan A B → O.Handle A B,
      (∀ {A B} (p : Plan A B), O.check g (embed p) = true) ∧
      (∀ {A B} (p : Plan A B) (x : A), O.invoke g (embed p) x = some (evaluate p x))) ∧
  (∀ {A B} (g : O.State) (h : O.Handle A B) (x : A) (y : B),
      O.invoke g h x = some y → O.check g h = true) ∧
  (∃ g : O.State, ∃ h : O.Handle (ULift.{u} Nat) (ULift.{u} Nat),
      O.check g h = false ∧
      O.invoke (O.change g 1 true) h (ULift.up 2) = some (ULift.up 3) ∧
      O.check (O.change (O.change g 1 true) 1 false) h = false ∧
      O.check (O.change (O.change (O.change g 1 true) 1 false) 1 true) h = false)

theorem positive_OWOU : OWOU operationalAPI.{u} := by
  refine ⟨?_, ?_, ?_⟩
  · exact ⟨openContext, fun p => ticket openContext p,
      fun p => all_open_checked p, fun p x => all_open_execute p x⟩
  · exact fun g h x y e => execution_implies_checked g h x y e
  · refine ⟨closedContext, ticket (revise closedContext 1 true) Plan.succ, ?_⟩
    decide

end OrthemologyV4
