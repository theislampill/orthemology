/-
P03 attempt-0002 NEW PROPOSAL. UNVERIFIED: no compiler was acquired here.
Target Lean 4.19.0. Core-only formalisation; not historical declaration recovery.
The model carries local target-indexed evidence and retains authority/root paths.
It does NOT assume a field asserting the desired whole-path warrant conclusion.
Exact-image graph carriers are an explicit emitted-certificate representation.
Semantic truth, actual authority and currentness require their own local witnesses.
-/
import P03GuardedGraph
namespace P03A2
universe u

structure EvidenceState (O : Type) where
  required : O → Prop
  discharged : O → Prop
  valid : O → Prop

def Sound {O : Type} (s : EvidenceState O) : Prop :=
  ∀ o, s.discharged o → s.valid o

def Closed {O : Type} (s : EvidenceState O) : Prop :=
  ∀ o, s.required o → s.valid o

structure EvidenceHop {O : Type} (a b : EvidenceState O) where
  preserved : O → Prop
  revalidated : O → Prop
  kept : ∀ o, preserved o → a.discharged o
  carry : ∀ o, preserved o → a.valid o → b.valid o
  fresh : ∀ o, revalidated o → b.valid o
  outExact : ∀ o, b.discharged o ↔ preserved o ∨ revalidated o
  coverage : ∀ o, b.required o → preserved o ∨ revalidated o

theorem EvidenceHop.sound {O : Type} {a b : EvidenceState O}
    (h : EvidenceHop a b) (hs : Sound a) : Sound b := by
  intro o ho
  cases (h.outExact o).mp ho with
  | inl hp => exact h.carry o hp (hs o (h.kept o hp))
  | inr hr => exact h.fresh o hr

theorem EvidenceHop.closed {O : Type} {a b : EvidenceState O}
    (h : EvidenceHop a b) (hs : Sound a) : Closed b := by
  intro o ho
  cases h.coverage o ho with
  | inl hp => exact h.carry o hp (hs o (h.kept o hp))
  | inr hr => exact h.fresh o hr

structure SemanticState where
  World : Type
  meaning : World → Prop

structure SemanticHop (a b : SemanticState) where
  map : a.World → b.World
  square : ∀ w, b.meaning (map w) ↔ a.meaning w

def SemanticHop.comp {a b c : SemanticState}
    (f : SemanticHop a b) (g : SemanticHop b c) : SemanticHop a c where
  map := fun w => g.map (f.map w)
  square := fun w => (g.square (f.map w)).trans (f.square w)

theorem SemanticHop.composite_square {a b c : SemanticState}
    (f : SemanticHop a b) (g : SemanticHop b c) (w : a.World) :
    c.meaning ((SemanticHop.comp f g).map w) ↔ a.meaning w :=
  (SemanticHop.comp f g).square w

structure Frame (O V R C : Type) where
  graph : P03Q1f.ReasonDAG
  reasons : EvidenceState O
  semantics : SemanticState
  version : V
  root : R
  claim : C

structure Policy (O V R C : Type) where
  epoch : Nat
  authority : Frame O V R C → Frame O V R C → Prop
  redelegate : Frame O V R C → Prop
  versionAllowed : V → Prop
  invalidatorsClosed : Frame O V R C → Prop
  rootStep : R → R → Prop

structure Hop {O V R C : Type} (p : Policy O V R C)
    (a b : Frame O V R C) where
  graphMap : P03Q1f.Hom a.graph b.graph
  onto : ∀ v, ∃ u, graphMap.node u = v
  reasons : EvidenceHop a.reasons b.reasons
  semantics : SemanticHop a.semantics b.semantics
  authority : p.authority a b
  targetVersion : p.versionAllowed b.version
  noOpenInvalidator : p.invalidatorsClosed b
  rootCustody : p.rootStep a.root b.root

/-- Indexed adjacency enforces the entire prior/output frame, not only version. -/
inductive Path {O V R C : Type} (p : Policy O V R C) :
    Frame O V R C → Frame O V R C → Type 1 where
  | one {a b} (h : Hop p a b) : Path p a b
  | cons {a b c} (h : Hop p a b) (rest : Path p b c)
      (allowMiddle : p.redelegate b) : Path p a c

inductive Via {α : Sort u} (rel : α → α → Prop) : α → α → Prop where
  | one {a b} : rel a b → Via rel a b
  | comp {a b c} : Via rel a b → Via rel b c → Via rel a c

/-- Permission is composable only with explicit intermediate re-delegation.
This is not transitive closure of pairwise authority with the guard erased. -/
inductive AuthorityPath {O V R C : Type} (p : Policy O V R C) :
    Frame O V R C → Frame O V R C → Prop where
  | one {a b} : p.authority a b → AuthorityPath p a b
  | cons {a b c} : p.authority a b → p.redelegate b →
      AuthorityPath p b c → AuthorityPath p a c

variable {O V R C : Type} {p : Policy O V R C}
variable {a b c : Frame O V R C}

def Path.graph {a b : Frame O V R C} : Path p a b → P03Q1f.Hom a.graph b.graph
  | .one h => h.graphMap
  | .cons h rest _ => P03Q1f.Hom.compose h.graphMap (Path.graph rest)

def Path.preimage {a b : Frame O V R C} : (q : Path p a b) →
    ∀ v : Fin b.graph.size, ∃ u : Fin a.graph.size, (Path.graph q).node u = v
  | .one h, v => h.onto v
  | .cons h rest _, v => by
      obtain ⟨mid, hm⟩ := Path.preimage rest v
      obtain ⟨src, hs⟩ := h.onto mid
      refine ⟨src, ?_⟩
      change (Path.graph rest).node (h.graphMap.node src) = v
      rw [hs]
      exact hm

def Path.semantics {a b : Frame O V R C} : Path p a b → SemanticHop a.semantics b.semantics
  | .one h => h.semantics
  | .cons h rest _ => SemanticHop.comp h.semantics (Path.semantics rest)

def Path.transportSound {a b : Frame O V R C} : (q : Path p a b) → Sound a.reasons → Sound b.reasons
  | .one h, hs => h.reasons.sound hs
  | .cons h rest _, hs => Path.transportSound rest (h.reasons.sound hs)

def Path.closeTarget {a b : Frame O V R C} : (q : Path p a b) → Sound a.reasons → Closed b.reasons
  | .one h, hs => h.reasons.closed hs
  | .cons h rest _, hs => Path.closeTarget rest (h.reasons.sound hs)

def Path.finalVersion {a b : Frame O V R C} : (q : Path p a b) → p.versionAllowed b.version
  | .one h => h.targetVersion
  | .cons _ rest _ => Path.finalVersion rest

def Path.finalInvalidators {a b : Frame O V R C} : (q : Path p a b) → p.invalidatorsClosed b
  | .one h => h.noOpenInvalidator
  | .cons _ rest _ => Path.finalInvalidators rest

def Path.rootTrace {a b : Frame O V R C} : (q : Path p a b) → Via p.rootStep a.root b.root
  | .one h => .one h.rootCustody
  | .cons h rest _ => .comp (.one h.rootCustody) (Path.rootTrace rest)

def Path.authorityTrace {a b : Frame O V R C} : (q : Path p a b) → AuthorityPath p a b
  | .one h => .one h.authority
  | .cons h rest allowMiddle => .cons h.authority allowMiddle (Path.authorityTrace rest)

theorem Path.mapEdge (q : Path p a b) {u v : Fin a.graph.size}
    (h : a.graph.Edge u v) : b.graph.Edge ((Path.graph q).node u) ((Path.graph q).node v) :=
  (Path.graph q).edge h

/-- The new conclusion is constructed from local evidence; it is not a Hop field.
Authority is a path witness, NOT an assumed transitive direct permission.
Currentness is at p.epoch only; changing Policy does not inherit this theorem.
-/
theorem guarded_reason_version_composition (q : Path p a b) (hs : Sound a.reasons) :
    Sound b.reasons ∧ Closed b.reasons ∧
    (∀ w, b.semantics.meaning ((Path.semantics q).map w) ↔ a.semantics.meaning w) ∧
    p.versionAllowed b.version ∧ p.invalidatorsClosed b ∧
    Via p.rootStep a.root b.root ∧ AuthorityPath p a b :=
  ⟨Path.transportSound q hs, Path.closeTarget q hs,
   (Path.semantics q).square, Path.finalVersion q,
   Path.finalInvalidators q, Path.rootTrace q, Path.authorityTrace q⟩

theorem Path.semantic_truth_transport (q : Path p a b) (w : a.semantics.World)
    (hw : a.semantics.meaning w) :
    b.semantics.meaning ((Path.semantics q).map w) :=
  ((Path.semantics q).square w).mpr hw

theorem Via.eq_endpoints {α : Sort u} {x y : α} (h : Via (fun a b => a = b) x y) : x = y := by
  induction h with
  | one e => exact e
  | comp _ _ ih₁ ih₂ => exact ih₁.trans ih₂

/-- A nonempty graph walk cannot collapse under the composed graph map. -/
theorem Path.no_collapse {u v : Fin a.graph.size} (q : Path p a b)
    (h : P03Q1f.Walk a.graph u v) : (Path.graph q).node u ≠ (Path.graph q).node v :=
  P03Q1f.Hom.noCollapseOfWalk (Path.graph q) h

end P03A2
