import PhaseAdvanceSource

/-! Explicit finite-data sources for retained-controller selectors.  These are
callable P02 components.  Their finite certificates bind each table cell to the
actual retained choice; no global controller or law equality is assumed. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource
open P02A2.ObserverCore P02A2.PRProgram
open HiddenParity HiddenParity.Sufficiency

/-- Explicit natural-number literals, supplied independently of the retained
noncomputable selectors.  Values above the used digits are ignored. -/
structure Data where
  cycleTable : ℕ
  targetTable : ℕ
  stageTable : ℕ
  deriving DecidableEq, Repr

/-- The Boolean retained cycle has period two, even if its finite enumeration
order is not the Boolean order. -/
theorem cycle_mod_two (F : Finset Bool) (fallback : Bool) (n : ℕ) :
    cycleAction F fallback (n % 2) = cycleAction F fallback n := by
  classical
  by_cases h : F.Nonempty
  · have hpos : 0 < Fintype.card F := by simpa using Finset.card_pos.mpr h
    have hle : Fintype.card F ≤ 2 := by
      simpa using Fintype.card_le_of_injective (fun a : F => a.val) Subtype.val_injective
    have hc : Fintype.card F = 1 ∨ Fintype.card F = 2 := by omega
    simp only [cycleAction, dif_pos h]
    congr 2
    apply Fin.ext
    rcases hc with hc | hc <;> simp [hc]
  · simp only [cycleAction, dif_neg h]


def cycleDigit (d : Data) (B : Finset Bool) (fallback residue : Bool) : ℕ :=
  d.cycleTable / 2^(4*supportCode B + 2*bitNat fallback + bitNat residue) % 2

def targetDigit (d : Data) (B : Finset Bool) (candidate state : Bool) : ℕ :=
  d.targetTable / 2^(5*(4*supportCode B + 2*bitNat candidate + bitNat state)) % 32

def stageDigit (d : Data) (B : Finset Bool) : ℕ :=
  d.stageTable / 2^(4*supportCode B) % 16

/-- A specification value only.  It is never evaluated by any source compiler. -/
noncomputable def actualTarget (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ)
    (B : Finset Bool) (candidate state : Bool) : Option (Finset (Bool × Bool)) :=
  if state ∈ stageTargets P menu priority B candidate then
    some (chooseTarget P menu priority B candidate state) else none

/-- All three premises quantify over finite carriers only: 16 cycle cells,
16 conditional target cells, and four stage-action cells.  Exact retained choice
is required, not merely membership in a qualifying component. -/
structure Certificate (d : Data) (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool) (priority : Bool → (Bool × Bool) → ℕ) : Prop where
  cycle_eq : ∀ B fallback residue,
    cycleDigit d B fallback residue = bitNat (cycleAction B fallback (bitNat residue))
  target_eq : ∀ B candidate state,
    targetDigit d B candidate state = retainedCode (actualTarget P menu priority B candidate state)
  stage_eq : ∀ B, stageDigit d B = targetCode (stageActions P menu priority B)

variable {d : Data} {P : RationalKernel Bool (Bool × Bool) Bool}
variable {menu : Finset Bool → Bool → Finset Bool} {priority : Bool → (Bool × Bool) → ℕ}

theorem cycle_value_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (fallback : Bool) (n : ℕ) :
    d.cycleTable / 2^(4*supportCode B + 2*bitNat fallback + n % 2) % 2 =
      bitNat (cycleAction B fallback n) := by
  rw [← cycle_mod_two B fallback n]
  have hn : n % 2 = 0 ∨ n % 2 = 1 := by omega
  rcases hn with hn | hn
  · simpa [cycleDigit,bitNat,hn] using cert.cycle_eq B fallback false
  · simpa [cycleDigit,bitNat,hn] using cert.cycle_eq B fallback true

/-- Literal expression: its only table access is division of a supplied numeral. -/
def cycleExpr (d : Data) (support fallback index : Expr) : Expr :=
  .mod (.div (.constant d.cycleTable)
    (.pow2 (.add (.add (.mul (.constant 4) support) (.mul (.constant 2) fallback))
      (.mod index (.constant 2))))) (.constant 2)

def targetExpr (d : Data) (support candidate state : Expr) : Expr :=
  .mod (.div (.constant d.targetTable)
    (.pow2 (.mul (.constant 5)
      (.add (.add (.mul (.constant 4) support) (.mul (.constant 2) candidate)) state))))
    (.constant 32)

def stageExpr (d : Data) (support : Expr) : Expr :=
  .mod (.div (.constant d.stageTable) (.pow2 (.mul (.constant 4) support))) (.constant 16)

/-- Inputs are support mask, fallback bit, and unbounded cycle index. -/
def cycleProgram (d : Data) : Program 3 :=
  ⟨.set 3 (cycleExpr d (.reg 0) (.reg 1) (.reg 2)),3⟩

/-- Inputs are support mask, candidate bit, and observed state bit. -/
def bindProgram (d : Data) : Program 3 :=
  ⟨.set 3 (targetExpr d (.reg 0) (.reg 1) (.reg 2)),3⟩

/-- Inputs are phase index, retained code, support mask, state bit, fallback bit.
The phase index is unchanged by normalization; this component returns the target. -/
def normalizeRetainedProgram (d : Data) : Program 5 :=
  ⟨.branch (.reg 1) (.set 5 (.reg 1))
    (.set 5 (targetExpr d (.reg 2)
      (cycleExpr d (.reg 2) (.reg 4) (.reg 0)) (.reg 3))),5⟩

/-- Inputs are retained code and support mask.  Output is a plain pair-set mask. -/
def activePairsProgram (d : Data) : Program 2 :=
  ⟨.branch (.reg 0) (.set 2 (.sub (.reg 0) (.constant 1)))
    (.set 2 (stageExpr d (.reg 1))),2⟩

theorem cycle_source_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (fallback : Bool) (n : ℕ) :
    denote (cycleProgram d) ![supportCode B,bitNat fallback,n] =
      bitNat (cycleAction B fallback n) := by
  simpa [denote,cycleProgram,cycleExpr,exec,evalExpr,P02A2.LoopPrimrec.extend]
    using cycle_value_exact cert B fallback n

theorem phase_candidate_source_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (fallback : Bool) (m : PhaseMemory Bool Bool) :
    denote (cycleProgram d) ![supportCode B,bitNat fallback,m.index] =
      bitNat (phaseCandidate B fallback m) :=
  cycle_source_exact cert B fallback m.index

theorem bind_source_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (candidate state : Bool) :
    denote (bindProgram d) ![supportCode B,bitNat candidate,bitNat state] =
      retainedCode (actualTarget P menu priority B candidate state) := by
  simpa [denote,bindProgram,targetExpr,targetDigit,exec,evalExpr,P02A2.LoopPrimrec.extend]
    using cert.target_eq B candidate state

theorem normalize_retained_source_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (state fallback : Bool) (m : PhaseMemory Bool Bool) :
    denote (normalizeRetainedProgram d)
      ![m.index,retainedCode m.retained,supportCode B,bitNat state,bitNat fallback] =
      retainedCode (normalizeMemory P menu priority fallback B state m).retained := by
  classical
  rcases m with ⟨n,t⟩
  cases t with
  | some E =>
      simp [denote,normalizeRetainedProgram,exec,evalExpr,P02A2.LoopPrimrec.extend,
        retainedCode,normalizeMemory]
  | none =>
      have hn : (normalizeMemory P menu priority fallback B state ⟨n,none⟩).retained =
          actualTarget P menu priority B (cycleAction B fallback n) state := by
        unfold normalizeMemory actualTarget
        simp only [phaseCandidate]
        split_ifs <;> rfl
      rw [hn]
      have hc := cycle_value_exact cert B fallback n
      simpa [denote,normalizeRetainedProgram,exec,evalExpr,P02A2.LoopPrimrec.extend,
        retainedCode,cycleExpr,targetExpr,hc,targetDigit]
        using cert.target_eq B (cycleAction B fallback n) state

theorem active_pairs_source_exact (cert : Certificate d P menu priority)
    (B : Finset Bool) (m : PhaseMemory Bool Bool) :
    denote (activePairsProgram d) ![retainedCode m.retained,supportCode B] =
      targetCode (activePairs P menu priority B m) := by
  rcases m with ⟨n,t⟩
  cases t with
  | none =>
      simpa [denote,activePairsProgram,stageExpr,stageDigit,exec,evalExpr,
        P02A2.LoopPrimrec.extend,retainedCode,activePairs] using cert.stage_eq B
  | some E =>
      simp [denote,activePairsProgram,exec,evalExpr,P02A2.LoopPrimrec.extend,
        retainedCode,activePairs]


/-- The two state-specific action bits are exactly the retained action menu. -/
theorem retained_actions_code : ∀ (E : Finset (Bool × Bool)) (state : Bool),
    targetCode E / 2^(2*bitNat state) % 4 = supportCode (retainedActions E state) := by decide

/-- Inputs are a pair-set mask, observed state bit, fallback action bit, and
unbounded visit count.  Both candidate and action cycling use the same certified
retained enumeration on Boolean menus. -/
def actionCycleProgram (d : Data) : Program 4 :=
  ⟨.set 4 (cycleExpr d
      (.mod (.div (.reg 0) (.pow2 (.mul (.constant 2) (.reg 1)))) (.constant 4))
      (.reg 2) (.reg 3)),4⟩

theorem action_cycle_source_exact (cert : Certificate d P menu priority)
    (E : Finset (Bool × Bool)) (state fallback : Bool) (visits : ℕ) :
    denote (actionCycleProgram d) ![targetCode E,bitNat state,bitNat fallback,visits] =
      bitNat (cycleAction (retainedActions E state) fallback visits) := by
  simpa [denote,actionCycleProgram,cycleExpr,exec,evalExpr,P02A2.LoopPrimrec.extend,
    retained_actions_code] using cycle_value_exact cert (retainedActions E state) fallback visits

end Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource
