import CertificateData
import CertificatePath
import CertificateOrder

namespace OrthemicCertificate

structure Link (n k : ℕ) where
  state : Fin n
  toRoot : Path (Fin n) (Fin k)
  fromRoot : Path (Fin n) (Fin k)
  deriving DecidableEq

structure Component (n k : ℕ) where
  pairs : Finset (Pair n k)
  root : Fin n
  links : List (Link n k)
  deriving DecidableEq

inductive Witness (n k : ℕ) where
  | exit (path : Path (Fin n) (Fin k)) (pair : Pair n k) (receipt : Fin n)
  | target (path : Path (Fin n) (Fin k)) (component : Component n k) (entry : Fin n)
  deriving DecidableEq

structure Obligation (q n k : ℕ) where
  state : Fin n
  candidate : Fin q
  witness : Witness n k
  deriving DecidableEq

structure Node (q n k : ℕ) where
  support : Support q
  states : Finset (Fin n)
  pairs : Finset (Pair n k)
  obligations : List (Obligation q n k)
  deriving DecidableEq

abbrev Body (q n k : ℕ) := List (Node q n k)

namespace Component
variable {q n k : ℕ}
def used (c : Component n k) : Finset (Fin n) := c.pairs.image Prod.fst

def Valid (I : Input q n k) (B : Support q) (θ : Fin q)
    (A : Finset (Pair n k)) (c : Component n k) (entry : Fin n) : Prop :=
  c.pairs.Nonempty ∧ c.pairs ⊆ A ∧ c.root ∈ c.used ∧ entry ∈ c.used ∧
  (c.links.map Link.state).Nodup ∧ (c.links.map Link.state).toFinset = c.used ∧
  (∀ link ∈ c.links, Path.Valid c.pairs (I.internal B) link.state c.root link.toRoot ∧
    Path.Valid c.pairs (I.internal B) c.root link.state link.fromRoot) ∧
  (∀ e ∈ c.pairs, (I.internal B e).Nonempty ∧ I.internal B e ⊆ c.used ∧
    ∀ y, 0 < I.row θ e y → y ∈ I.internal B e) ∧
  ∀ σ ∈ B, (∀ e ∈ c.pairs, ∀ y, I.row σ e y = I.row θ e y) →
    ∃ e ∈ c.pairs, I.priority σ e % 2 = 0 ∧ ∀ f ∈ c.pairs, I.priority σ e ≤ I.priority σ f

instance (I : Input q n k) (B : Support q) (θ : Fin q)
    (A : Finset (Pair n k)) (c : Component n k) (entry : Fin n) :
    Decidable (Valid I B θ A c entry) := by
  haveI : Decidable (∀ link ∈ c.links, Path.Valid c.pairs (I.internal B) link.state c.root link.toRoot ∧
    Path.Valid c.pairs (I.internal B) c.root link.state link.fromRoot) := by infer_instance
  haveI : Decidable (∀ e ∈ c.pairs, (I.internal B e).Nonempty ∧ I.internal B e ⊆ c.used ∧
    ∀ y, 0 < I.row θ e y → y ∈ I.internal B e) := by infer_instance
  haveI : Decidable (∀ σ ∈ B, (∀ e ∈ c.pairs, ∀ y, I.row σ e y = I.row θ e y) →
    ∃ e ∈ c.pairs, I.priority σ e % 2 = 0 ∧ ∀ f ∈ c.pairs, I.priority σ e ≤ I.priority σ f) := by infer_instance
  unfold Valid
  infer_instance
end Component

namespace Witness
variable {q n k : ℕ}
def Valid (I : Input q n k) (B : Support q) (A : Finset (Pair n k))
    (s : Fin n) (θ : Fin q) : Witness n k → Prop
  | .exit p e y => Path.Valid A (I.internal B) s e.1 p ∧ e ∈ A ∧
      0 < I.row θ e y ∧ I.live B e y ⊂ B
  | .target p c entry => Path.Valid A (I.internal B) s entry p ∧ c.Valid I B θ A entry

instance (I : Input q n k) (B : Support q) (A : Finset (Pair n k))
    (s : Fin n) (θ : Fin q) (w : Witness n k) : Decidable (Valid I B A s θ w) := by
  cases w <;> unfold Valid <;> infer_instance
end Witness

namespace Node
variable {q n k : ℕ}
def KeysValid (N : Node q n k) : Prop :=
  (N.obligations.map (fun o => (o.state,o.candidate))).Nodup ∧
  (N.obligations.map (fun o => (o.state,o.candidate))).toFinset = N.states ×ˢ N.support
instance (N : Node q n k) : Decidable N.KeysValid := by unfold KeysValid; infer_instance

def PairsValid (I : Input q n k) (c : Body q n k) (N : Node q n k) : Prop :=
  ∀ e ∈ N.pairs, e.1 ∈ N.states ∧ e.2 ∈ I.menu N.support e.1 ∧
    ∀ y, (I.live N.support e y).Nonempty →
      if I.live N.support e y = N.support then y ∈ N.states
      else I.live N.support e y ⊂ N.support ∧
        ∃ child ∈ c, child.support = I.live N.support e y ∧ y ∈ child.states
instance (I : Input q n k) (c : Body q n k) (N : Node q n k) :
    Decidable (PairsValid I c N) := by unfold PairsValid; infer_instance

def Valid (I : Input q n k) (c : Body q n k) (N : Node q n k) : Prop :=
  N.support.Nonempty ∧ N.KeysValid ∧ N.PairsValid I c ∧
    ∀ o ∈ N.obligations, o.witness.Valid I N.support N.pairs o.state o.candidate
instance (I : Input q n k) (c : Body q n k) (N : Node q n k) :
    Decidable (Valid I c N) := by unfold Valid; infer_instance
end Node

/-- Nondecreasing canonical keys plus no repeated support is exactly strict key
ordering. No unlisted support is enumerated for this check. -/
def Layout {q n k : ℕ} (c : Body q n k) : Prop :=
  (c.map Node.support).Pairwise supportLE ∧ (c.map Node.support).Nodup
instance {q n k : ℕ} (c : Body q n k) : Decidable (Layout c) := by unfold Layout; infer_instance

def BodyValid {q n k : ℕ} (I : Input q n k) (c : Body q n k) : Prop :=
  I.Valid ∧ Layout c ∧ ∀ N ∈ c, N.Valid I c

/-- Input gate is short-circuiting; every submitted node is then checked. -/
def bodyCheck {q n k : ℕ} (I : Input q n k) (c : Body q n k) : Bool :=
  if I.inputCheck then decide (Layout c ∧ ∀ N ∈ c, N.Valid I c) else false

def queryLookup {q n k : ℕ} (c : Body q n k) (B : Support q) (s : Fin n) : Bool :=
  decide (B.Nonempty ∧ ∃ N ∈ c, N.support = B ∧ s ∈ N.states)

def check {q n k : ℕ} (I : Input q n k) (c : Body q n k) (B : Support q) (s : Fin n) : Bool :=
  bodyCheck I c && queryLookup c B s

@[simp] theorem bodyCheck_iff {q n k : ℕ} (I : Input q n k) (c : Body q n k) :
    bodyCheck I c = true ↔ BodyValid I c := by
  simp [bodyCheck, BodyValid]

@[simp] theorem queryLookup_iff {q n k : ℕ} (c : Body q n k) (B : Support q) (s : Fin n) :
    queryLookup c B s = true ↔ B.Nonempty ∧ ∃ N ∈ c, N.support = B ∧ s ∈ N.states := by
  simp [queryLookup]

@[simp] theorem check_iff {q n k : ℕ} (I : Input q n k) (c : Body q n k)
    (B : Support q) (s : Fin n) : check I c B s = true ↔
      BodyValid I c ∧ B.Nonempty ∧ ∃ N ∈ c, N.support = B ∧ s ∈ N.states := by
  simp [check]
end OrthemicCertificate
