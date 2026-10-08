import CertificateSyntax

namespace IndependentCertificateControls
open OrthemicCertificate

def ep {n k : ℕ} (s : Fin n) : Path (Fin n) (Fin k) := ⟨s,[]⟩
def singletonComponent {n k : ℕ} (s : Fin n) (a : Fin k) : Component n k :=
  ⟨{(s,a)},s,[⟨s,ep s,ep s⟩]⟩

def tiny : Input 1 1 2 :=
  ⟨#[1,1],#[2,4],[⟨[0],0,[0,1]⟩],⟨["m"],["s"],["a","b"],"v1","obs","source","authority"⟩⟩

def tinyNode (a : Fin 2) : Node 1 1 2 :=
  ⟨{0},{0},{(0,0),(0,1)},[⟨0,0,.target (ep 0) (singletonComponent 0 a) 0⟩]⟩

def noStates : Node 1 1 2 := ⟨{0},∅,∅,[]⟩
def noSupport : Node 1 1 2 := ⟨∅,∅,∅,[]⟩

def tinyResults : List (String × Bool) :=
  [("arbitrary_first_component",check tiny [tinyNode 0] {0} 0),
   ("arbitrary_second_component",check tiny [tinyNode 1] {0} 0),
   ("distinct_component_syntax",decide (tinyNode 0 ≠ tinyNode 1)),
   ("empty_state_node_valid",bodyCheck tiny [noStates]),
   ("empty_state_node_no_query",!check tiny [noStates] {0} 0),
   ("empty_body_valid",bodyCheck tiny []),
   ("empty_body_no_query",!check tiny [] {0} 0),
   ("empty_support_rejected",!bodyCheck tiny [noSupport]),
   ("duplicate_node_rejected",!bodyCheck tiny [tinyNode 0,tinyNode 1]),
   ("missing_obligation_rejected",!bodyCheck tiny [{tinyNode 0 with obligations := []}]),
   ("duplicate_obligation_rejected",!bodyCheck tiny [{tinyNode 0 with obligations := (tinyNode 0).obligations ++ (tinyNode 0).obligations}]),
   ("missing_menu_default_empty",!bodyCheck {tiny with menus := []} [tinyNode 0]),
   ("candidate_itself_odd_rejected",!bodyCheck {tiny with priorities := #[1,4]} [tinyNode 0]),
   ("unused_odd_component_alternative_passes",bodyCheck {tiny with priorities := #[1,4]} [tinyNode 1])]
#eval tinyResults
#guard tinyResults.all Prod.snd

-- Complete three-model revealing-action fixture, independently transcribed
-- from the approved design. The exit transition is not an internal path step.
def revealRows : Array ℚ := Array.ofFn fun i : Fin 81 =>
  let m := i.val / 27
  let s := i.val / 9 % 3
  let a := i.val / 3 % 3
  let y := i.val % 3
  if s = 0 ∧ a = 0 then
    if m = 0 then (if y = 1 ∨ y = 2 then 1/2 else 0)
    else if m = 1 then (if y = 1 then 1 else 0)
    else (if y = 2 then 1 else 0)
  else if y = s then 1 else 0

def revealPriorities : Array ℕ := Array.ofFn fun i : Fin 27 =>
  let s := i.val / 3 % 3
  let a := i.val % 3
  if (s = 1 ∧ a = 1) ∨ (s = 2 ∧ a = 2) then 2 else 1

def reveal : Input 3 3 3 :=
  ⟨revealRows,revealPriorities,[⟨[0,1,2],0,[0]⟩,⟨[0,1],1,[1]⟩,⟨[0,2],2,[2]⟩],
    ⟨["alpha","beta","gamma"],["s","t0","t1"],["reveal","a0","a1"],"r1","full state","declared source","declared authority"⟩⟩

def child0 : Node 3 3 3 :=
  ⟨{0,1},{1},{(1,1)},[⟨1,0,.target (ep 1) (singletonComponent 1 1) 1⟩,
                       ⟨1,1,.target (ep 1) (singletonComponent 1 1) 1⟩]⟩
def child1 : Node 3 3 3 :=
  ⟨{0,2},{2},{(2,2)},[⟨2,0,.target (ep 2) (singletonComponent 2 2) 2⟩,
                       ⟨2,2,.target (ep 2) (singletonComponent 2 2) 2⟩]⟩
def parent : Node 3 3 3 :=
  ⟨{0,1,2},{0},{(0,0)},[⟨0,0,.exit (ep 0) (0,0) 1⟩,
                         ⟨0,1,.exit (ep 0) (0,0) 1⟩,
                         ⟨0,2,.exit (ep 0) (0,0) 2⟩]⟩
def parentAlternative : Node 3 3 3 :=
  {parent with obligations := [⟨0,0,.exit (ep 0) (0,0) 2⟩,
                               ⟨0,1,.exit (ep 0) (0,0) 1⟩,
                               ⟨0,2,.exit (ep 0) (0,0) 2⟩]}
def invalidExtra : Node 3 3 3 := ⟨{2},{0},{(0,0)},[]⟩
def harmlessExtra : Node 3 3 3 := ⟨{2},∅,∅,[]⟩

def revealResults : List (String × Bool) :=
  [("reveal_input_valid",reveal.inputCheck),
   ("separate_child0_query",check reveal [child0] {0,1} 1),
   ("separate_child1_query",check reveal [child1] {0,2} 2),
   ("children_body_valid",bodyCheck reveal [child0,child1]),
   ("children_union_no_parent",!check reveal [child0,child1] {0,1,2} 0),
   ("parent_full_body",check reveal [child0,child1,parent] {0,1,2} 0),
   ("alternative_positive_exit",check reveal [child0,child1,parentAlternative] {0,1,2} 0),
   ("missing_child0_rejected",!bodyCheck reveal [child1,parent]),
   ("missing_child1_rejected",!bodyCheck reveal [child0,parent]),
   ("wrong_exact_child_support_rejected",!bodyCheck reveal [{child0 with support := {1,2}},child1,parent]),
   ("parent_before_child_rejected",!bodyCheck reveal [parent,child0,child1]),
   ("invalid_unrelated_node_rejected",!check reveal [invalidExtra,child0,child1,parent] {0,1,2} 0),
   ("valid_unrelated_node_accepted",check reveal [harmlessExtra,child0,child1,parent] {0,1,2} 0),
   ("false_exit_not_internal_step",!decide (Path.Valid parent.pairs (reveal.internal parent.support) 0 1 ⟨0,[(0,1)]⟩)),
   ("used_parent_permission_removed",!check {reveal with menus := [⟨[0,1],1,[1]⟩,⟨[0,2],2,[2]⟩]} [child0,child1,parent] {0,1,2} 0),
   ("shape_mismatch_whole_body_rejected",!bodyCheck {reveal with rows := #[]} [child0,child1,parent])]
#eval revealResults
#guard revealResults.all Prod.snd

-- The semantic universe cannot be allocated before these zero-dimension gates.
def nZero : Input (2^100) 0 (2^100) := ⟨#[],#[],[],⟨[],[],[],"","","",""⟩⟩
def kZero : Input (2^100) (2^100) 0 := ⟨#[],#[],[],⟨[],[],[],"","","",""⟩⟩
#guard !nZero.inputCheck
#guard !kZero.inputCheck

end IndependentCertificateControls

namespace IndependentCertificateControls
open OrthemicCertificate

-- Same transition supports, different full Bernoulli rows. Each candidate has
-- a separate even component; its unmatched rival has odd minimum there.
def latentRows (equalRows : Bool) : Array ℚ := Array.ofFn fun i : Fin 16 =>
  let m := i.val / 8
  let y := i.val % 2
  let p : ℚ := if m = 0 ∨ equalRows then 1/3 else 2/3
  if y = 0 then p else 1-p

def latent : Input 2 2 2 :=
  ⟨latentRows false,#[2,1,2,1,1,2,1,2],[⟨[0,1],0,[0,1]⟩,⟨[0,1],1,[0,1]⟩],
   ⟨["alpha","beta"],["zero","one"],["a","b"],"v1","Bernoulli states","declared","declared"⟩⟩

def latentComponent (a : Fin 2) : Component 2 2 :=
  ⟨{(0,a),(1,a)},0,[⟨0,ep 0,ep 0⟩,⟨1,⟨1,[(a,0)]⟩,⟨0,[(a,1)]⟩⟩]⟩

def latentNode : Node 2 2 2 :=
  ⟨{0,1},{0,1},{(0,0),(0,1),(1,0),(1,1)},
   [⟨0,0,.target (ep 0) (latentComponent 0) 0⟩,
    ⟨1,0,.target (ep 1) (latentComponent 0) 1⟩,
    ⟨0,1,.target (ep 0) (latentComponent 1) 0⟩,
    ⟨1,1,.target (ep 1) (latentComponent 1) 1⟩]⟩

def latentResults : List (String × Bool) :=
  [("unequal_full_rows_same_support_positive",check latent [latentNode] {0,1} 0),
   ("unmatched_odd_rival_component_positive",decide ((latentComponent 0).Valid latent {0,1} 0 latentNode.pairs 0)),
   ("exact_matching_odd_rival_rejected",!check {latent with rows := latentRows true} [latentNode] {0,1} 0),
   ("changed_exact_rows_equality_guard_rejects",!latent.sameInput {latent with rows := latentRows true}),
   ("declared_revision_changes_actual_input",!latent.sameInput {latent with interpretation := {latent.interpretation with modelRevision := "v2"}}),
   ("fresh_revision_recheck_still_valid",check {latent with interpretation := {latent.interpretation with modelRevision := "v2"}} [latentNode] {0,1} 0),
   ("missing_live_candidate_rejected",!bodyCheck latent [{latentNode with obligations := latentNode.obligations.filter (fun o => o.candidate == 0)}]),
   ("component_connection_missing_rejected",!decide (({latentComponent 0 with links := [⟨0,ep 0,ep 0⟩]} : Component 2 2).Valid latent {0,1} 0 latentNode.pairs 0)),
   ("component_internal_successor_omitted_rejected",!decide ((singletonComponent 0 0).Valid latent {0,1} 0 latentNode.pairs 0))]
#eval latentResults
#guard latentResults.all Prod.snd
end IndependentCertificateControls

namespace IndependentCertificateControls
open OrthemicCertificate

-- A valid child under the wrong support cannot discharge the actual receipt.
-- Unlike a malformed-key mutation, the substitute child itself checks.
def wrongChildInput : Input 3 3 3 := {reveal with menus := reveal.menus ++ [⟨[1,2],1,[1]⟩]}
def validWrongChild : Node 3 3 3 :=
  ⟨{1,2},{1},{(1,1)},[⟨1,1,.target (ep 1) (singletonComponent 1 1) 1⟩,
                       ⟨1,2,.target (ep 1) (singletonComponent 1 1) 1⟩]⟩
#guard check wrongChildInput [validWrongChild] {1,2} 1
#guard bodyCheck wrongChildInput [child1,validWrongChild]
#guard !bodyCheck wrongChildInput [child1,validWrongChild,parent]

-- Two distinct actual certificate paths to the same target component.
def routeInput : Input 1 3 2 :=
  ⟨#[0,0,1, 0,1,0, 0,0,1, 0,1,0, 0,0,1, 0,0,1],
   #[1,1,1,1,2,1],[⟨[0],0,[0,1]⟩,⟨[0],1,[0]⟩,⟨[0],2,[0]⟩],
   ⟨["m"],["s","via","target"],["direct","detour"],"v1","states","declared","declared"⟩⟩
def routeNode (detour : Bool) : Node 1 3 2 :=
  ⟨{0},{0,1,2},{(0,0),(0,1),(1,0),(2,0)},
   [⟨0,0,.target (if detour then ⟨0,[(1,1),(0,2)]⟩ else ⟨0,[(0,2)]⟩) (singletonComponent 2 0) 2⟩,
    ⟨1,0,.target ⟨1,[(0,2)]⟩ (singletonComponent 2 0) 2⟩,
    ⟨2,0,.target (ep 2) (singletonComponent 2 0) 2⟩]⟩
#guard check routeInput [routeNode false] {0} 0
#guard check routeInput [routeNode true] {0} 0
#guard routeNode false != routeNode true
-- A same-support successor cannot be redirected into an alleged lower child;
-- retaining only its source without its real same-support successor rejects.
#guard !bodyCheck routeInput [{routeNode false with states := {0}}]

end IndependentCertificateControls
