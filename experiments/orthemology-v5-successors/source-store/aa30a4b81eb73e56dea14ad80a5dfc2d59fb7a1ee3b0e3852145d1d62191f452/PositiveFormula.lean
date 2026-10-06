import CertificateSyntax
import Refutation
import FiniteLists

namespace OrthemicCertificate.Signed

/-- Closed finite atomic language. No Boolean, arbitrary proposition, positive
checker, semantic winning predicate, reachability or solver can be stored here.
All leaves are exact equality, order or finite membership calculations. -/
inductive Atom (q n k : Nat) where
  | natEq (a b : Nat)
  | natLE (a b : Nat)
  | natLT (a b : Nat)
  | ratEq (a b : Rat)
  | ratLE (a b : Rat)
  | ratLT (a b : Rat)
  | natMem (a : Nat) (xs : List Nat)
  | menuKeyEq (a b : Finset Nat × Nat)
  | supportEq (a b : Support q)
  | supportOrder (a b : Support q)
  | stateEq (a b : Fin n)
  | stateSetEq (a b : Finset (Fin n))
  | stateModelEq (a b : Fin n × Fin q)
  | stateModelSetEq (a b : Finset (Fin n × Fin q))
  | modelMem (a : Fin q) (s : Support q)
  | stateMem (a : Fin n) (s : Finset (Fin n))
  | actionMem (a : Fin k) (s : Finset (Fin k))
  | pairMem (a : Pair n k) (s : Finset (Pair n k))
  deriving DecidableEq

namespace Atom
variable {q n k : Nat}
def eval : Atom q n k → Bool
  | .natEq a b => decide (a = b)
  | .natLE a b => decide (a ≤ b)
  | .natLT a b => decide (a < b)
  | .ratEq a b => decide (a = b)
  | .ratLE a b => decide (a ≤ b)
  | .ratLT a b => decide (a < b)
  | .natMem a xs => decide (a ∈ xs)
  | .menuKeyEq a b => decide (a = b)
  | .supportEq a b => decide (a = b)
  | .supportOrder a b => decide (supportLE a b)
  | .stateEq a b => decide (a = b)
  | .stateSetEq a b => decide (a = b)
  | .stateModelEq a b => decide (a = b)
  | .stateModelSetEq a b => decide (a = b)
  | .modelMem a s => decide (a ∈ s)
  | .stateMem a s => decide (a ∈ s)
  | .actionMem a s => decide (a ∈ s)
  | .pairMem a s => decide (a ∈ s)
end Atom

abbrev CheckedFormula (q n k : Nat) := Formula (Atom q n k)
variable {q n k : Nat}

private def lit (a : Atom q n k) : CheckedFormula q n k := .literal a true
private def allF := @Formula.all (Atom q n k)
private def everyF {α : Type} := @Formula.every (Atom q n k) α
private def someF {α : Type} := @Formula.someOf (Atom q n k) α
private def impliesF := @Formula.implies (Atom q n k)

private def allPairs (n k : Nat) : List (Pair n k) :=
  productList (List.finRange n) (List.finRange k)

private theorem allPairs_complete (e : Pair n k) : e ∈ allPairs n k := by simp [allPairs]

private def supportNonempty (B : Support q) : CheckedFormula q n k :=
  someF (List.finRange q) (fun σ => lit (.modelMem σ B))

private def pairNonempty (A : Finset (Pair n k)) : CheckedFormula q n k :=
  someF (allPairs n k) (fun e => lit (.pairMem e A))

private def stateNonempty (W : Finset (Fin n)) : CheckedFormula q n k :=
  someF (List.finRange n) (fun y => lit (.stateMem y W))

private def supportSubset (B C : Support q) : CheckedFormula q n k :=
  everyF (List.finRange q) (fun σ => impliesF (lit (.modelMem σ B)) (lit (.modelMem σ C)))

private def supportStrictSubset (B C : Support q) : CheckedFormula q n k :=
  .conj (supportSubset B C) (lit (.supportEq B C)).neg

private def pairSubset (A D : Finset (Pair n k)) : CheckedFormula q n k :=
  everyF (allPairs n k) (fun e => impliesF (lit (.pairMem e A)) (lit (.pairMem e D)))

private def stateSubset (W V : Finset (Fin n)) : CheckedFormula q n k :=
  everyF (List.finRange n) (fun y => impliesF (lit (.stateMem y W)) (lit (.stateMem y V)))

/-- Finite pairwise inequalities expose every duplicate-key test structurally. -/
private def nodupF {α : Type} (eq : α → α → Atom q n k) (xs : List α) : CheckedFormula q n k :=
  Formula.pairwise (fun a b => (lit (eq a b)).neg) xs

private theorem lit_eval (a : Atom q n k) : (lit a).eval Atom.eval = Atom.eval a := by
  simp [lit, Formula.eval]

private theorem nodupF_eval {α : Type} [DecidableEq α]
    (eq : α → α → Atom q n k) (heq : ∀ a b, Atom.eval (eq a b) = decide (a = b))
    (xs : List α) : (nodupF eq xs).eval Atom.eval = true ↔ xs.Nodup := by
  simp only [nodupF, Formula.eval_pairwise_true, Formula.eval_neg, lit_eval, heq,
    Bool.not_eq_true', decide_eq_false_iff_not]
  rfl

private theorem supportNonempty_eval (B : Support q) :
    (supportNonempty (n := n) (k := k) B).eval Atom.eval = true ↔ B.Nonempty := by
  simp [supportNonempty, someF, lit, Formula.eval, Atom.eval, Finset.Nonempty]

private theorem pairNonempty_eval (A : Finset (Pair n k)) :
    (pairNonempty (q := q) A).eval Atom.eval = true ↔ A.Nonempty := by
  simp [pairNonempty, someF, lit, Formula.eval, Atom.eval, allPairs, Finset.Nonempty]

private theorem stateNonempty_eval (W : Finset (Fin n)) :
    (stateNonempty (q := q) (k := k) W).eval Atom.eval = true ↔ W.Nonempty := by
  simp [stateNonempty, someF, lit, Formula.eval, Atom.eval, Finset.Nonempty]

private theorem supportSubset_eval (B C : Support q) :
    (supportSubset (n := n) (k := k) B C).eval Atom.eval = true ↔ B ⊆ C := by
  simp [supportSubset, everyF, impliesF, lit_eval, Atom.eval, Finset.subset_iff]

private theorem supportStrictSubset_eval (B C : Support q) :
    (supportStrictSubset (n := n) (k := k) B C).eval Atom.eval = true ↔ B ⊂ C := by
  simp [supportStrictSubset, Formula.eval, supportSubset_eval, lit_eval, Atom.eval,
    Finset.ssubset_iff_subset_ne]

private theorem pairSubset_eval (A D : Finset (Pair n k)) :
    (pairSubset (q := q) A D).eval Atom.eval = true ↔ A ⊆ D := by
  simp [pairSubset, everyF, impliesF, lit_eval, Atom.eval, allPairs, Finset.subset_iff]

private theorem stateSubset_eval (W V : Finset (Fin n)) :
    (stateSubset (q := q) (k := k) W V).eval Atom.eval = true ↔ W ⊆ V := by
  simp [stateSubset, everyF, impliesF, lit_eval, Atom.eval, Finset.subset_iff]

/-- All original shape branches are separate exact length/dimension atoms. -/
def shapeFormula (I : Input q n k) : CheckedFormula q n k :=
  allF [lit (.natLT 0 q), lit (.natLT 0 n), lit (.natLT 0 k),
    lit (.natEq I.rows.size (q*n*k*n)), lit (.natEq I.priorities.size (q*n*k)),
    lit (.natEq I.interpretation.modelCoding.length q),
    lit (.natEq I.interpretation.stateCoding.length n),
    lit (.natEq I.interpretation.actionCoding.length k)]

def menuFormula (I : Input q n k) : CheckedFormula q n k :=
  .conj (nodupF Atom.menuKeyEq (I.menus.map (fun e => (e.support.toFinset, e.state))))
    (everyF I.menus (fun e => allF [
      nodupF Atom.natEq e.support,
      everyF e.support (fun a => lit (.natLT a q)), lit (.natLT e.state n),
      nodupF Atom.natEq e.actions, everyF e.actions (fun a => lit (.natLT a k))]))

def rowsFormula (I : Input q n k) : CheckedFormula q n k :=
  .conj (everyF (List.finRange q) (fun σ => everyF (allPairs n k) (fun e =>
    everyF (List.finRange n) (fun y => lit (.ratLE 0 (I.row σ e y))))))
    (everyF (List.finRange q) (fun σ => everyF (allPairs n k) (fun e =>
      lit (.ratEq (∑ y, I.row σ e y) 1))))

def inputFormula (I : Input q n k) : CheckedFormula q n k :=
  allF [shapeFormula I, menuFormula I, rowsFormula I]

@[simp] theorem shapeFormula_eval (I : Input q n k) :
    (shapeFormula I).eval Atom.eval = true ↔ I.Shape := by
  simp [shapeFormula, allF, lit, Formula.eval, Atom.eval, Input.Shape, and_assoc]

@[simp] theorem menuFormula_eval (I : Input q n k) :
    (menuFormula I).eval Atom.eval = true ↔ I.MenuValid := by
  simp [menuFormula, allF, everyF, Formula.eval, nodupF_eval, lit_eval,
    Atom.eval, Input.MenuValid, and_assoc]

@[simp] theorem rowsFormula_eval (I : Input q n k) :
    (rowsFormula I).eval Atom.eval = true ↔ I.RowsValid := by
  simp [rowsFormula, everyF, Formula.eval, lit_eval, Atom.eval, allPairs, Input.RowsValid]

@[simp] theorem inputFormula_eval (I : Input q n k) :
    (inputFormula I).eval Atom.eval = true ↔ I.Valid := by
  simp [inputFormula, allF, Input.Valid, and_assoc]

/-- Stored edges are traversed recursively with reconstructed source state. -/
def edgesFormula (I : Input q n k) (B : Support q) (A : Finset (Pair n k))
    (s : Fin n) : List (Fin k × Fin n) → CheckedFormula q n k
  | [] => .constant true
  | (a,t) :: rest => allF [lit (.pairMem (s,a) A),
      lit (.stateMem t (I.internal B (s,a))), edgesFormula I B A t rest]

def pathFormula (I : Input q n k) (B : Support q) (A : Finset (Pair n k))
    (s t : Fin n) (p : Path (Fin n) (Fin k)) : CheckedFormula q n k :=
  allF [lit (.stateEq p.start s), lit (.stateEq p.endpoint t),
    edgesFormula I B A p.start p.steps, lit (.natLE p.steps.length (n-1))]

@[simp] theorem edgesFormula_eval (I : Input q n k) (B : Support q)
    (A : Finset (Pair n k)) (s : Fin n) (steps : List (Fin k × Fin n)) :
    (edgesFormula I B A s steps).eval Atom.eval = true ↔ Path.Edges A (I.internal B) s steps := by
  induction steps generalizing s with
  | nil => simp [edgesFormula, Formula.eval, Path.Edges]
  | cons step steps ih =>
    rcases step with ⟨a,t⟩
    simp [edgesFormula, allF, lit_eval, Atom.eval, Path.Edges, ih, and_assoc]

@[simp] theorem pathFormula_eval (I : Input q n k) (B : Support q)
    (A : Finset (Pair n k)) (s t : Fin n) (p : Path (Fin n) (Fin k)) :
    (pathFormula I B A s t p).eval Atom.eval = true ↔ Path.Valid A (I.internal B) s t p := by
  simp [pathFormula, allF, lit_eval, Atom.eval, Path.Valid, and_assoc]

/-- Full-row match and attained even minimum are separate finite quantifier
subtrees. In particular, there is no aggregate qualification leaf. -/
def componentFormula (I : Input q n k) (B : Support q) (θ : Fin q)
    (A : Finset (Pair n k)) (c : Component n k) (entry : Fin n) : CheckedFormula q n k :=
  allF [pairNonempty c.pairs, pairSubset c.pairs A, lit (.stateMem c.root c.used),
    lit (.stateMem entry c.used),
    nodupF Atom.stateEq (c.links.map Link.state),
    lit (.stateSetEq (c.links.map Link.state).toFinset c.used),
    everyF c.links (fun link => .conj
      (pathFormula I B c.pairs link.state c.root link.toRoot)
      (pathFormula I B c.pairs c.root link.state link.fromRoot)),
    everyF (allPairs n k) (fun e => impliesF (lit (.pairMem e c.pairs))
      (allF [stateNonempty (I.internal B e), stateSubset (I.internal B e) c.used,
        everyF (List.finRange n) (fun y => impliesF (lit (.ratLT 0 (I.row θ e y)))
          (lit (.stateMem y (I.internal B e))))])),
    everyF (List.finRange q) (fun σ => impliesF (lit (.modelMem σ B))
      (impliesF (everyF (allPairs n k) (fun e => impliesF (lit (.pairMem e c.pairs))
        (everyF (List.finRange n) (fun y => lit (.ratEq (I.row σ e y) (I.row θ e y))))))
        (someF (allPairs n k) (fun e => allF [lit (.pairMem e c.pairs),
          lit (.natEq (I.priority σ e % 2) 0),
          everyF (allPairs n k) (fun f => impliesF (lit (.pairMem f c.pairs))
            (lit (.natLE (I.priority σ e) (I.priority σ f))))]))))]

@[simp] theorem componentFormula_eval (I : Input q n k) (B : Support q) (θ : Fin q)
    (A : Finset (Pair n k)) (c : Component n k) (entry : Fin n) :
    (componentFormula I B θ A c entry).eval Atom.eval = true ↔ c.Valid I B θ A entry := by
  simp [componentFormula, allF, everyF, someF, impliesF, Formula.eval,
    pairNonempty_eval, pairSubset_eval, stateNonempty_eval, stateSubset_eval,
    nodupF_eval, lit_eval, Atom.eval, allPairs, Component.Valid, and_assoc,
    forall_and]

/-- The exact submitted witness constructor selects its own local formula. -/
def witnessFormula (I : Input q n k) (B : Support q) (A : Finset (Pair n k))
    (s : Fin n) (θ : Fin q) : Witness n k → CheckedFormula q n k
  | .exit p e y => allF [pathFormula I B A s e.1 p, lit (.pairMem e A),
      lit (.ratLT 0 (I.row θ e y)), supportStrictSubset (I.live B e y) B]
  | .target p c entry => .conj (pathFormula I B A s entry p) (componentFormula I B θ A c entry)

@[simp] theorem witnessFormula_eval (I : Input q n k) (B : Support q)
    (A : Finset (Pair n k)) (s : Fin n) (θ : Fin q) (w : Witness n k) :
    (witnessFormula I B A s θ w).eval Atom.eval = true ↔ w.Valid I B A s θ := by
  cases w <;> simp [witnessFormula, allF, Formula.eval, lit_eval, Atom.eval,
    supportStrictSubset_eval, Witness.Valid, and_assoc]

def keysFormula (N : Node q n k) : CheckedFormula q n k :=
  .conj (nodupF Atom.stateModelEq (N.obligations.map (fun o => (o.state,o.candidate))))
    (lit (.stateModelSetEq (N.obligations.map (fun o => (o.state,o.candidate))).toFinset
      (N.states ×ˢ N.support)))

/-- A proper-support child test is a finite existential over the literal body;
refuting it therefore covers every submitted child, including unused nodes. -/
def pairsFormula (I : Input q n k) (c : Body q n k) (N : Node q n k) : CheckedFormula q n k :=
  everyF (allPairs n k) (fun e => impliesF (lit (.pairMem e N.pairs))
    (allF [lit (.stateMem e.1 N.states), lit (.actionMem e.2 (I.menu N.support e.1)),
      everyF (List.finRange n) (fun y =>
        impliesF (supportNonempty (I.live N.support e y))
          (.conj
            (impliesF (lit (.supportEq (I.live N.support e y) N.support)) (lit (.stateMem y N.states)))
            (impliesF (lit (.supportEq (I.live N.support e y) N.support)).neg
              (.conj (supportStrictSubset (I.live N.support e y) N.support)
                (someF c (fun child => .conj
                  (lit (.supportEq child.support (I.live N.support e y)))
                  (lit (.stateMem y child.states))))))))]))

@[simp] theorem keysFormula_eval (N : Node q n k) :
    (keysFormula N).eval Atom.eval = true ↔ N.KeysValid := by
  simp [keysFormula, Formula.eval, nodupF_eval, lit_eval, Atom.eval, Node.KeysValid]

private theorem guarded_branches (p q r : Prop) [Decidable p] :
    ((p → q) ∧ (¬p → r)) ↔ (if p then q else r) := by
  by_cases hp : p <;> simp [hp]

@[simp] theorem pairsFormula_eval (I : Input q n k) (c : Body q n k) (N : Node q n k) :
    (pairsFormula I c N).eval Atom.eval = true ↔ N.PairsValid I c := by
  simp [pairsFormula, everyF, someF, allF, impliesF, Formula.eval,
    lit_eval, Atom.eval, allPairs, Node.PairsValid, supportNonempty_eval,
    supportStrictSubset_eval, guarded_branches]

def nodeFormula (I : Input q n k) (c : Body q n k) (N : Node q n k) : CheckedFormula q n k :=
  allF [supportNonempty N.support, keysFormula N, pairsFormula I c N,
    everyF N.obligations (fun o => witnessFormula I N.support N.pairs o.state o.candidate o.witness)]

def layoutFormula (c : Body q n k) : CheckedFormula q n k :=
  .conj (Formula.pairwise (fun B C => lit (.supportOrder B C)) (c.map Node.support))
    (nodupF Atom.supportEq (c.map Node.support))

def bodyFormula (I : Input q n k) (c : Body q n k) : CheckedFormula q n k :=
  allF [inputFormula I, layoutFormula c, everyF c (nodeFormula I c)]

def queryFormula (c : Body q n k) (B : Support q) (s : Fin n) : CheckedFormula q n k :=
  .conj (supportNonempty B) (someF c (fun N =>
    .conj (lit (.supportEq N.support B)) (lit (.stateMem s N.states))))

def positiveFormula (I : Input q n k) (c : Body q n k) (B : Support q) (s : Fin n) : CheckedFormula q n k :=
  .conj (bodyFormula I c) (queryFormula c B s)

@[simp] theorem nodeFormula_eval (I : Input q n k) (c : Body q n k) (N : Node q n k) :
    (nodeFormula I c N).eval Atom.eval = true ↔ N.Valid I c := by
  simp [nodeFormula, allF, everyF, supportNonempty_eval, Node.Valid, and_assoc]

@[simp] theorem layoutFormula_eval (c : Body q n k) :
    (layoutFormula c).eval Atom.eval = true ↔ Layout c := by
  simp [layoutFormula, Formula.eval, nodupF_eval, lit_eval, Atom.eval, Layout]

@[simp] theorem bodyFormula_eval (I : Input q n k) (c : Body q n k) :
    (bodyFormula I c).eval Atom.eval = true ↔ BodyValid I c := by
  simp [bodyFormula, allF, everyF, BodyValid, and_assoc]

@[simp] theorem queryFormula_eval (c : Body q n k) (B : Support q) (s : Fin n) :
    (queryFormula c B s).eval Atom.eval = true ↔
      B.Nonempty ∧ ∃ N ∈ c, N.support = B ∧ s ∈ N.states := by
  simp [queryFormula, someF, Formula.eval, supportNonempty_eval, lit_eval, Atom.eval]

/-- Exact reflection of the unchanged inherited positive checker, including input
validation, every submitted node and the precise nonempty query lookup. -/
theorem positiveFormula_eval (I : Input q n k) (c : Body q n k) (B : Support q) (s : Fin n) :
    (positiveFormula I c B s).eval Atom.eval = check I c B s := by
  have h : (positiveFormula I c B s).eval Atom.eval = true ↔ check I c B s = true := by
    simp [positiveFormula, Formula.eval]
  exact Bool.eq_iff_iff.mpr h

end OrthemicCertificate.Signed
