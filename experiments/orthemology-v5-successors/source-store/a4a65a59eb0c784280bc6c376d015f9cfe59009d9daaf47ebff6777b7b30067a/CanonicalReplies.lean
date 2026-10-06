import OpaqueSearch

namespace CoveringKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

/-- Full authenticated preparation/cancellation content and logical timing are
carried in `control`. A truthful effect receipt is optional. `Payload` is not a
proof of physical authenticity; that remains a retained source premise. -/
structure MacroReply (Payload : Type*) where
  control : Payload
  effectReceipt : Option Bool

/-- Canonical fixed-world observation law: the complete control transcript is
independent of the hidden world. With receipt enabled, precisely the good path
reports an effect. With receipt disabled there is no new observation channel. -/
def canonicalObserve {F : Finset (Finset α)} {Payload : Type*}
    (control : ℕ → Path F → Payload) (receipt : Bool)
    (T : Finset α) (n : ℕ) (P : Path F) : MacroReply Payload :=
  ⟨control n P, if receipt then some (decide (Disjoint P.val T)) else none⟩

def canonicalFailedReply {F : Finset (Finset α)} {Payload : Type*}
    (control : ℕ → Path F → Payload) (receipt : Bool)
    (n : ℕ) (P : Path F) : MacroReply Payload :=
  ⟨control n P, if receipt then some false else none⟩

omit [Fintype α] in
theorem canonical_opaque {F : Finset (Finset α)} {Payload : Type*}
    (control : ℕ → Path F → Payload) (receipt : Bool) (k : ℕ) :
    Opaque k (canonicalObserve control receipt) (canonicalFailedReply control receipt) := by
  intro T _ n P hbad
  simp [canonicalObserve, canonicalFailedReply, hbad]

#print axioms canonical_opaque
end CoveringKernel
