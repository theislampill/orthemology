import DirectEndpoint
import CertificateFixtures
open OrthemicCertificate OrthemicCertificate.Fixtures OrthemicCertificate.Direct
open HiddenParity.Sufficiency

-- Execute the actual positive checker to produce erased input-validity evidence.
-- This does not introduce native_decide or any proof-trust extension.
def checkedAction {q n k : ℕ} (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (h : List (Fin k × Fin n)) : Option (Fin k) :=
  if hc : check I c B s = true then
    some (compile I ((check_iff I c B s).mp hc).1.1 B s c () h)
  else none

#guard reveal.inputCheck
#guard latent.inputCheck
#guard choices.inputCheck

-- Different accepted witnesses genuinely change the selected operating action.
#guard checkedAction choices {0} 1 [choicesNode 1 0] [] = some 0
#guard checkedAction choices {0} 1 [choicesNode 2 1] [] = some 1

-- Every positive reveal receipt is handled by its actual submitted child.
#guard checkedAction reveal {0,1,2} 0 revealedBody [] = some 0
#guard checkedAction reveal {0,1,2} 0 revealedBody [(0,1)] = some 1
#guard checkedAction reveal {0,1,2} 0 revealedBody [(0,2)] = some 2

-- Exact initial-support gaps, including the all-identical fallback.
#guard tolerance latent {0,1} = 1/6
#guard tolerance latentEqualRows {0,1} = 1
#guard tolerance choices {0} = 1
#guard rationalFrequency (0,0) 1 ([] : List ((Fin 2 × Fin 2) × Fin 2)) = 0
#guard !(rationalReject latent (1/6) 0 0 [])
#guard rationalReject latent (1/6) 0 0 [((0,0),1)]
#guard !(rationalReject latent (1/6) 0 1 [((0,0),1)])

-- Stale low-count anomalies cannot reject a sufficiently late phase.
#guard !(rationalReject latent (1/6) 0 100 [((0,0),1)])
#guard symbolCount (0,0) 1 ([((0,0),1),((1,1),0),((0,0),1)] : List ((Fin 2 × Fin 2) × Fin 2)) = 2

-- Retention updates use support change, rejection, and component exit in order.
#guard (advanceMemory ({0,1} : Finset (Fin 2)) {1} (0 : Fin 2)
    (⟨7,some {(0,0)}⟩ : PhaseMemory (Fin 2) (Fin 2)) true).index = 0
#guard (advanceMemory ({0,1} : Finset (Fin 2)) {0,1} (0 : Fin 2)
    (⟨7,some {(0,0)}⟩ : PhaseMemory (Fin 2) (Fin 2)) true).index = 8
#guard (advanceMemory ({0,1} : Finset (Fin 2)) {0,1} (1 : Fin 2)
    (⟨7,some {(0,0)}⟩ : PhaseMemory (Fin 2) (Fin 2)) false).index = 8
#guard (advanceMemory ({0,1} : Finset (Fin 2)) {0,1} (0 : Fin 2)
    (⟨7,some {(0,0)}⟩ : PhaseMemory (Fin 2) (Fin 2)) false).index = 7

-- Rejection and candidate advance on the literal acquired receipt history.
#guard checkedAction latent {0,1} 0 [latentNode] [] = some 0
#guard checkedAction latent {0,1} 0 [latentNode] [(0,1)] = some 1
#guard checkedAction latentEqualRows {0,1} 0 [latentNode] [] = none
#guard checkedAction reveal {0,1,2} 0 [child₀,parent] [] = none

-- A submitted two-action component uses global departure counts in operation.
def fairComponent : Component 3 2 :=
  ⟨{(1,0),(1,1)},1,[⟨1,emptyPath 1,emptyPath 1⟩]⟩
def fairNode : Node 1 3 2 :=
  ⟨{0},{1},{(1,0),(1,1)},[⟨1,0,.target (emptyPath 1) fairComponent 1⟩]⟩
#guard check choices [fairNode] {0} 1
#guard checkedAction choices {0} 1 [fairNode] [] = some 0
#guard checkedAction choices {0} 1 [fairNode] [(0,1)] = some 1
#guard checkedAction choices {0} 1 [fairNode] [(1,1),(0,1)] = some 0
#guard !(rationalReject latent (1/6) 0 0 [((0,0),1),((0,0),0),((0,0),0)])
