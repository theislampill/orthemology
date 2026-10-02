/-
P03 Q1f graph-only proposal. UNVERIFIED at Lean 4.19.0.
Not the historical VersionCustodyTransport declaration; not VCT/TRC completion.
A finite DAG is encoded by a topological rank, so target acyclicity is not
silently inferred from edge preservation. No authority/semantic truth axiom
is added. Claims are graph transport only, not warrant transport.
-/
import Init
namespace P03Q1f

structure ReasonDAG where
  size : Nat
  Edge : Fin size → Fin size → Prop
  rank : Fin size → Nat
  rising : ∀ {u v}, Edge u v → rank u < rank v

structure Hom (A B : ReasonDAG) where
  node : Fin A.size → Fin B.size
  edge : ∀ {u v}, A.Edge u v → B.Edge (node u) (node v)

def Hom.identity (A : ReasonDAG) : Hom A A where
  node := fun x => x
  edge := fun h => h

def Hom.compose {A B C : ReasonDAG} (f : Hom A B) (g : Hom B C) : Hom A C where
  node := fun x => g.node (f.node x)
  edge := fun h => g.edge (f.edge h)

inductive Chain : ReasonDAG → ReasonDAG → Type where
  | nil (A : ReasonDAG) : Chain A A
  | cons {A B C : ReasonDAG} (head : Hom A B) (tail : Chain B C) : Chain A C

def Chain.composite {A B : ReasonDAG} : Chain A B → Hom A B
  | .nil A => Hom.identity A
  | .cons head tail => Hom.compose head tail.composite

theorem Chain.mapEdge {A B : ReasonDAG} (c : Chain A B)
    {u v : Fin A.size} (h : A.Edge u v) :
    B.Edge (c.composite.node u) (c.composite.node v) :=
  c.composite.edge h

inductive Walk (A : ReasonDAG) : Fin A.size → Fin A.size → Prop where
  | single {u v} : A.Edge u v → Walk A u v
  | join {u v w} : Walk A u v → Walk A v w → Walk A u w

theorem walkRank {A : ReasonDAG} {u v : Fin A.size} (h : Walk A u v) :
    A.rank u < A.rank v := by
  induction h with
  | single h => exact A.rising h
  | join h1 h2 ih1 ih2 => exact Nat.lt_trans ih1 ih2

theorem Hom.mapWalk {A B : ReasonDAG} (f : Hom A B)
    {u v : Fin A.size} (h : Walk A u v) : Walk B (f.node u) (f.node v) := by
  induction h with
  | single h => exact Walk.single (f.edge h)
  | join h1 h2 ih1 ih2 => exact Walk.join ih1 ih2

theorem noClosedWalk {A : ReasonDAG} {u : Fin A.size} : ¬ Walk A u u := by
  intro h
  exact Nat.lt_irrefl (A.rank u) (walkRank h)

theorem Hom.noCollapseOfWalk {A B : ReasonDAG} (f : Hom A B)
    {u v : Fin A.size} (h : Walk A u v) : f.node u ≠ f.node v := by
  intro eq
  have hw := f.mapWalk h
  rw [eq] at hw
  exact noClosedWalk hw

end P03Q1f
