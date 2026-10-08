import MarkovSupportAdapter

/-! Independent finite data and shape-first exact-input validation. No semantic
winning proof, retained selector or solver is part of this input language. -/
namespace OrthemicCertificate

abbrev Pair (n k : ℕ) := Fin n × Fin k
abbrev Support (q : ℕ) := Finset (Fin q)

/-- A raw sparse-menu record. Natural keys are checked before interpretation;
duplicated keys or duplicated members are rejected. The default is empty. -/
structure MenuEntry where
  support : List ℕ
  state : ℕ
  actions : List ℕ
  deriving DecidableEq, Repr

structure Interpretation where
  modelCoding : List String
  stateCoding : List String
  actionCoding : List String
  modelRevision : String
  observation : String
  occurrenceSource : String
  authority : String
  deriving DecidableEq, Repr

/-- Dense rows/priorities are explicitly submitted vectors (arrays). Their
lengths are checked before any enumeration of the claimed finite carriers. -/
structure Input (q n k : ℕ) where
  rows : Array ℚ
  priorities : Array ℕ
  menus : List MenuEntry
  interpretation : Interpretation
  deriving DecidableEq, Repr

namespace Input
variable {q n k : ℕ}

def row (I : Input q n k) (σ : Fin q) (e : Pair n k) (y : Fin n) : ℚ :=
  I.rows[((σ.val * n + e.1.val) * k + e.2.val) * n + y.val]?.getD 0

def priority (I : Input q n k) (σ : Fin q) (e : Pair n k) : ℕ :=
  I.priorities[(σ.val * n + e.1.val) * k + e.2.val]?.getD 0

def menuRecord (I : Input q n k) (B : Support q) (s : Fin n) : Option MenuEntry :=
  I.menus.find? (fun e => e.support.toFinset = B.image Fin.val && e.state == s.val)

def menu (I : Input q n k) (B : Support q) (s : Fin n) : Finset (Fin k) :=
  match I.menuRecord B s with
  | none => ∅
  | some entry => Finset.univ.filter (fun a => a.val ∈ entry.actions)

/-- Cheap explicit-length gate: no Fin universe is constructed here. -/
def Shape (I : Input q n k) : Prop :=
  0 < q ∧ 0 < n ∧ 0 < k ∧ I.rows.size = q*n*k*n ∧
  I.priorities.size = q*n*k ∧ I.interpretation.modelCoding.length = q ∧
  I.interpretation.stateCoding.length = n ∧ I.interpretation.actionCoding.length = k
instance (I : Input q n k) : Decidable I.Shape := inferInstanceAs (Decidable (_ ∧ _))

def shapeCheck (I : Input q n k) : Bool := decide I.Shape

def MenuValid (I : Input q n k) : Prop :=
  (I.menus.map (fun e => (e.support.toFinset, e.state))).Nodup ∧
  ∀ e ∈ I.menus, e.support.Nodup ∧ (∀ a ∈ e.support, a < q) ∧
    e.state < n ∧ e.actions.Nodup ∧ (∀ a ∈ e.actions, a < k)
instance (I : Input q n k) : Decidable I.MenuValid := by unfold MenuValid; infer_instance

def RowsValid (I : Input q n k) : Prop :=
  (∀ σ e y, 0 ≤ I.row σ e y) ∧ (∀ σ e, ∑ y, I.row σ e y = 1)
instance (I : Input q n k) : Decidable I.RowsValid := by unfold RowsValid; infer_instance

def Valid (I : Input q n k) : Prop := I.Shape ∧ I.MenuValid ∧ I.RowsValid

/-- The dependent conditional is intentional: neither carrier enumeration nor
row arithmetic is evaluated when the explicit shape gate fails. -/
def inputCheck (I : Input q n k) : Bool :=
  if I.shapeCheck then decide (I.MenuValid ∧ I.RowsValid) else false

@[simp] theorem inputCheck_iff (I : Input q n k) : I.inputCheck = true ↔ I.Valid := by
  simp [inputCheck, shapeCheck, Valid]

def kernel (I : Input q n k) (h : I.Valid) : HiddenParity.RationalKernel (Fin q) (Pair n k) (Fin n) where
  row := I.row
  nonnegative := h.2.2.1
  normalized := h.2.2.2

@[simp] theorem kernel_row (I : Input q n k) (h : I.Valid) : (I.kernel h).row = I.row := rfl

/-- Actual structured equality, including all interpretation fields. -/
def sameInput (I J : Input q n k) : Bool := decide (I = J)
@[simp] theorem sameInput_iff (I J : Input q n k) : I.sameInput J = true ↔ I = J := by simp [sameInput]

/-- Direct finite support computations used by the checker. -/
def live (I : Input q n k) (B : Support q) (e : Pair n k) (y : Fin n) : Support q :=
  B.filter (fun σ => 0 < I.row σ e y)

def internal (I : Input q n k) (B : Support q) (e : Pair n k) : Finset (Fin n) :=
  Finset.univ.filter (fun y => ∀ σ ∈ B, 0 < I.row σ e y)

@[simp] theorem mem_internal (I : Input q n k) (B : Support q) (e : Pair n k) (y : Fin n) :
    y ∈ I.internal B e ↔ ∀ σ ∈ B, 0 < I.row σ e y := by simp [internal]

@[simp] theorem internal_kernel (I : Input q n k) (h : I.Valid) (B : Support q) :
    I.internal B = HiddenParity.internalSuccessors (I.kernel h) B := by
  funext e
  ext y
  simp [HiddenParity.mem_internalSuccessors]
end Input
end OrthemicCertificate
