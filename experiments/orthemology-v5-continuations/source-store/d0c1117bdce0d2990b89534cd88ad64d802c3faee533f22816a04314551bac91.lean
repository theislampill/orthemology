/- Explicit native-tree representation at the validated-AST boundary.
All rule/field/tag strings emitted by these functions are fixed ASCII literals.
Object fields are retained, so dictionary key nodes are counted rather than
forgotten. This is not a UTF-8/JSON text decoder or a CPython semantics. -/
import SourceResources
namespace P03Source
open OrthemologyV2 OrthemologyV3

inductive WireValue where
  | natural : Nat → WireValue
  | negative : Nat → WireValue  -- -(n+1), distinct from natural zero
  | boolean : Bool → WireValue
  | null : WireValue
  | text : String → WireValue
  | array : List WireValue → WireValue
  | object : List (String × WireValue) → WireValue
  deriving Repr

theorem pair_value_size_lt {xs : List (String × WireValue)} {x : String × WireValue}
    (h : x ∈ xs) : sizeOf x.2 < 1 + sizeOf xs := by
  have hm := List.sizeOf_lt_of_mem h
  rcases x with ⟨key, value⟩
  simp only [Prod.mk.sizeOf_spec] at hm
  simp only [Prod.snd]
  omega

def wireNodes : WireValue → Nat
  | .natural _ | .negative _ | .boolean _ | .null | .text _ => 1
  | .array xs => 1 + (xs.map wireNodes).foldl Nat.add 0
  | .object xs => 1 + (xs.map (fun x => 1 + wireNodes x.2)).foldl Nat.add 0

termination_by value => sizeOf value
decreasing_by
  all_goals simp_wf
  all_goals first
    | exact pair_value_size_lt ‹_ ∈ _›
    | have hm := List.sizeOf_lt_of_mem ‹_ ∈ _›; omega

def wireHeight : WireValue → Nat
  | .natural _ | .negative _ | .boolean _ | .null | .text _ => 0
  | .array [] | .object [] => 0
  | .array xs => 1 + (xs.map wireHeight).foldl max 0
  | .object xs => 1 + (xs.map (fun x => wireHeight x.2)).foldl max 0

termination_by value => sizeOf value
decreasing_by
  all_goals simp_wf
  all_goals first
    | exact pair_value_size_lt ‹_ ∈ _›
    | have hm := List.sizeOf_lt_of_mem ‹_ ∈ _›; omega

def wireIntegersFit : WireValue → Bool
  | .natural n => decide (n < 2^256)
  | .negative n => decide (n+1 < 2^256)
  | .boolean _ | .null | .text _ => true
  | .array xs => (xs.map wireIntegersFit).all id
  | .object xs => (xs.map (fun x => wireIntegersFit x.2)).all id

termination_by value => sizeOf value
decreasing_by
  all_goals simp_wf
  all_goals first
    | exact pair_value_size_lt ‹_ ∈ _›
    | have hm := List.sizeOf_lt_of_mem ‹_ ∈ _›; omega

def wireShape (w : WireValue) : Shape := ⟨wireNodes w, wireHeight w, wireIntegersFit w⟩

def typeTree : TypeCode → WireValue
  | .var n => .array [.text "v", .natural n]
  | .bottom => .array [.text "bottom"]
  | .arrow A B => .array [.text "arr", typeTree A, typeTree B]
  | .all A => .array [.text "all", typeTree A]

def termTree : Term → WireValue
  | .i => .array [.text "i"]
  | .k => .array [.text "k"]
  | .s => .array [.text "s"]
  | .zero => .array [.text "zero"]
  | .one => .array [.text "one"]
  | .app f x => .array [.text "app", termTree f, termTree x]

def proofTree : SourceProof → WireValue
  | .i A => .object [("rule", .text "i"), ("A", typeTree A)]
  | .k A B => .object [("rule", .text "k"), ("A", typeTree A), ("B", typeTree B)]
  | .s A B C => .object [("rule", .text "s"), ("A", typeTree A), ("B", typeTree B), ("C", typeTree C)]
  | .app p q => .object [("rule", .text "app"), ("function", proofTree p), ("argument", proofTree q)]
  | .allI p => .object [("rule", .text "all_i"), ("body", proofTree p)]
  | .allE p A => .object [("rule", .text "all_e"), ("polymorphic", proofTree p), ("type", typeTree A)]
  | .reduce p trace => .object [("rule", .text "reduce"), ("proof", proofTree p), ("trace", .array (trace.map termTree))]

-- Componentwise statements keep the recursive proof independent of any
-- theorem asserting that a native Python value already has the right shape.
theorem typeTree_nodes (A : TypeCode) : wireNodes (typeTree A) = (typeShape A).nodes := by
  induction A with
  | var n => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | bottom => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | arrow A B ihA ihB => simp [typeTree, wireNodes, typeShape, ihA, ihB, Nat.add_assoc] <;> omega
  | all A ih => simp [typeTree, wireNodes, typeShape, ih, Nat.add_assoc] <;> omega

theorem typeTree_height (A : TypeCode) : wireHeight (typeTree A) = (typeShape A).height := by
  induction A with
  | var n => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | bottom => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | arrow A B ihA ihB => simp [typeTree, wireHeight, typeShape, ihA, ihB]
  | all A ih => simp [typeTree, wireHeight, typeShape, ih]

theorem typeTree_integers (A : TypeCode) : wireIntegersFit (typeTree A) = (typeShape A).integersFit := by
  induction A with
  | var n => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | bottom => simp [typeTree, wireNodes, wireHeight, wireIntegersFit, typeShape]
  | arrow A B ihA ihB => simp [typeTree, wireIntegersFit, typeShape, ihA, ihB]
  | all A ih => simp [typeTree, wireIntegersFit, typeShape, ih]

theorem termTree_nodes (t : Term) : wireNodes (termTree t) = (termShape t).nodes := by
  induction t <;> simp_all [termTree, wireNodes, termShape, Nat.add_assoc] <;> omega

theorem termTree_height (t : Term) : wireHeight (termTree t) = (termShape t).height := by
  induction t <;> simp_all [termTree, wireHeight, termShape]

theorem termTree_integers (t : Term) : wireIntegersFit (termTree t) = true := by
  induction t <;> simp_all [termTree, wireIntegersFit]

theorem traceTree_nodes (ts : List Term) :
    wireNodes (.array (ts.map termTree)) = (traceShape ts).nodes := by
  simp [wireNodes, traceShape, List.map_map, Function.comp_def, termTree_nodes]

theorem traceTree_height (ts : List Term) :
    wireHeight (.array (ts.map termTree)) = (traceShape ts).height := by
  cases ts <;> simp [wireHeight, traceShape, List.map_map, Function.comp_def, termTree_height]

theorem traceTree_integers (ts : List Term) :
    wireIntegersFit (.array (ts.map termTree)) = true := by
  simp [wireIntegersFit, List.map_map, Function.comp_def, termTree_integers]

theorem proofTree_nodes (p : SourceProof) :
    wireNodes (proofTree p) = (proofShape p).nodes := by
  induction p <;>
    simp_all [proofTree, wireNodes, proofShape, typeTree_nodes, traceTree_nodes,
      traceShape, List.map_map, Function.comp_def, termTree_nodes] <;> omega

theorem proofTree_height (p : SourceProof) :
    wireHeight (proofTree p) = (proofShape p).height := by
  induction p <;>
    simp_all [proofTree, wireHeight, proofShape, typeTree_height, traceTree_height,
      traceShape, List.map_map, termTree_height, Nat.max_assoc]

theorem proofTree_integers (p : SourceProof) :
    wireIntegersFit (proofTree p) = (proofShape p).integersFit := by
  induction p <;>
    simp_all [proofTree, wireIntegersFit, proofShape, typeTree_integers,
      traceTree_integers, List.map_map, termTree_integers, Bool.and_assoc]

theorem proofTree_shape (p : SourceProof) : wireShape (proofTree p) = proofShape p := by
  have hn := proofTree_nodes p
  have hh := proofTree_height p
  have hi := proofTree_integers p
  cases hp : proofShape p
  simp only [hp, Shape.nodes, Shape.height, Shape.integersFit] at hn hh hi
  simp [wireShape, hn, hh, hi]

#print axioms proofTree_shape
end P03Source
