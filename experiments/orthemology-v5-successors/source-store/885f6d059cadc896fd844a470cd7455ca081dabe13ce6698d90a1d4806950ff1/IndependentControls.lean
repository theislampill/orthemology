import SignedControllerService
import SmallFixtures
import NativeControllerControls
open OrthemicCertificate OrthemicCertificate.Signed OrthemicCertificate.Direct
open OrthemicCertificate.Signed.Fixtures
open HiddenParity.Sufficiency

-- Full actual 49-entry tiny domain checked across valid and malformed row/menu variants.
private def variants : List (Input 1 1 1) :=
  [singleInput 0, singleInput 1, singleInput 2, singleInput 3,
   {evenInput with rows := #[0]}, {evenInput with rows := #[-1]},
   {evenInput with rows := #[2]}, {evenInput with rows := #[]},
   {evenInput with menus := []}, {evenInput with menus := [⟨[0],0,[]⟩]}]
#guard variants.all (fun I => (astDomain 1 1 1).all (fun c =>
  (positiveFormula I c {0} 0).eval Atom.eval == check I c {0} 0))
#guard variants.all (fun I => (astDomain 1 1 1).all (fun c =>
  localReject I {0} 0 c (refutationCandidate Atom.eval (positiveFormula I c {0} 0)) ==
    !(check I c {0} 0)))
#guard (astDomain 1 1 1).all (fun c => !(check evenInput c ∅ 0))

-- Constructor discrimination and exhaustive four-valued truth tables.
private def atom (b : Bool) : Formula Bool := .literal b true
#guard ([false,true].all (fun a => [false,true].all (fun b =>
  rejectCheck id (.disj (atom a) (atom b)) (.both .leaf .leaf) == (!a && !b))))
#guard ([false,true].all (fun a => [false,true].all (fun b =>
  rejectCheck id (.conj (atom a) (atom b)) (.left .leaf) == !a)))
#guard !(rejectCheck id (.disj (atom false) (atom false)) (.left .leaf))
#guard !(rejectCheck id (.conj (atom false) (atom false)) (.both .leaf .leaf))
#guard !(rejectCheck id (atom false) (.right .leaf))
#guard !(rejectCheck id (.constant true : Formula Bool) .leaf)

-- All seven interpretation coordinates are bound, even ones irrelevant to row arithmetic.
private def negOdd := negativeCandidate oddInput {0} 0
private def alteredInterpretations : List Interpretation :=
  let i := oddInput.interpretation
  [{i with modelCoding := ["changed"]}, {i with stateCoding := ["changed"]},
   {i with actionCoding := ["changed"]}, {i with modelRevision := "changed"},
   {i with observation := "changed"}, {i with occurrenceSource := "changed"},
   {i with authority := "changed"}]
#guard alteredInterpretations.all (fun i =>
  !(negativeCheck {oddInput with interpretation := i} {0} 0 negOdd))
-- Local evidence must survive its exact formula, not only an all-false placeholder acceptor.
#guard !(negativeCheck oddInput {0} 0 {negOdd with entries := negOdd.entries.map (fun (i,_) => (i,.leaf))})
#guard !(negativeCheck oddInput {0} 0 {negOdd with entries := negOdd.entries.take 48})
#guard !(negativeCheck oddInput {0} 0 {negOdd with entries := (0,.leaf) :: negOdd.entries})

-- Actual global source reconstruction is tested on a nonconstant observed state trace.
#guard augmentHistory (0 : Fin 3) ([(1,2),(0,1)] : List (Fin 2 × Fin 3)) =
  [((1,1),2),((0,0),1)]
#guard historyVisits (0 : Fin 3) 0 ([(1,2),(0,1)] : List (Fin 2 × Fin 3)) = 1
#guard historyVisits (0 : Fin 3) 1 ([(1,2),(0,1)] : List (Fin 2 × Fin 3)) = 1
#guard historyVisits (0 : Fin 3) 2 ([(1,2),(0,1)] : List (Fin 2 × Fin 3)) = 0
-- Sorted cycle handles arbitrary offsets and emptiness without a selection oracle.
#guard OrthemicCertificate.Direct.cycleAction ({4,1,3} : Finset Nat) 9 0 = 1
#guard OrthemicCertificate.Direct.cycleAction ({4,1,3} : Finset Nat) 9 100 = 3
#guard OrthemicCertificate.Direct.cycleAction (∅ : Finset Nat) 9 100 = 9

-- Every accepted list-order variant, and no normalized representative alone, is covered.
example {q n k : Nat} {I : Input q n k} {c : Body q n k} {B : Support q} {s : Fin n}
    (hc : check I c B s = true) : c ∈ astDomain q n k := accepted_mem_astDomain hc
example {q n k : Nat} {I : Input q n k} {c : Body q n k} {B : Support q} {s : Fin n}
    (hc : check I c.reverse B s = true) : c.reverse ∈ astDomain q n k := accepted_mem_astDomain hc

#eval "Independent discriminating controls passed"

-- Two accepted obligation orders select different literal submitted components.
private def orderInput : Input 2 2 2 :=
  {OrthemicCertificate.Fixtures.latent with
    priorities := OrthemicCertificate.Fixtures.priorities 2 2 2 (fun _ _ _ => 0)}
private def orderNode : Node 2 2 2 :=
  ⟨{0,1},{0,1},Finset.univ,[
    ⟨0,0,.target (OrthemicCertificate.Fixtures.emptyPath 0) (OrthemicCertificate.Fixtures.latentComponent 0) 0⟩,
    ⟨1,0,.target (OrthemicCertificate.Fixtures.emptyPath 1) (OrthemicCertificate.Fixtures.latentComponent 1) 1⟩,
    ⟨0,1,.target (OrthemicCertificate.Fixtures.emptyPath 0) (OrthemicCertificate.Fixtures.latentComponent 0) 0⟩,
    ⟨1,1,.target (OrthemicCertificate.Fixtures.emptyPath 1) (OrthemicCertificate.Fixtures.latentComponent 1) 1⟩]⟩
private def reversedOrderNode : Node 2 2 2 := {orderNode with obligations := orderNode.obligations.reverse}
#guard check orderInput [orderNode] {0,1} 0
#guard check orderInput [reversedOrderNode] {0,1} 0
#guard checkedAction orderInput {0,1} 0 [orderNode] [] = some 0
#guard checkedAction orderInput {0,1} 0 [reversedOrderNode] [] = some 1
example (h : check orderInput [reversedOrderNode] {0,1} 0 = true) :
    [reversedOrderNode] ∈ astDomain 2 2 2 := accepted_mem_astDomain h
