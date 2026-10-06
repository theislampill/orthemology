import ParallelHistorySource
import FiniteSelectorSource
import CompleteEmpiricalSource

/-! Compositional P02 source for the retained phase/support/target/statistic
controller on Boolean finite carriers. Classical selectors occur solely in the
finite binding certificate; source syntax contains explicit table numerals. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate.FullController
open P02A2.ObserverCore P02A2.PRProgram P02A2.PRComposition
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Stage HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
set_option maxHeartbeats 2000000

structure Config where
  selectors : FiniteSelectorSource.Data
  kernel : RationalKernel Bool (Bool × Bool) Bool
  toleranceNumerator : ℕ
  toleranceDenominator : ℕ
  rowDenominator : ℕ
  rowNumerator : Bool → (Bool × Bool) → Bool → ℕ
  initialSupport : Finset Bool
  initialState : Bool
  fallbackModel : Bool
  fallbackAction : Bool

structure Certificate (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) : Prop where
  selectors : FiniteSelectorSource.Certificate c.selectors c.kernel menu priority
  toleranceDenominator_pos : 0 < c.toleranceDenominator
  rowDenominator_pos : 0 < c.rowDenominator
  row_exact : ∀ θ e y, c.kernel.row θ e y = (c.rowNumerator θ e y : ℚ)/c.rowDenominator

def exprProgram (n : ℕ) (e : Expr) : Program n := ⟨.set n e,n⟩
@[simp] theorem denote_exprProgram (n : ℕ) (e : Expr) (xs : Fin n → ℕ) :
    denote (exprProgram n e) xs = evalExpr e (P02A2.LoopPrimrec.extend xs) := by
  simp [denote,exprProgram,exec]

def substProgram {k l : ℕ} (p : Program l) (args : Fin l → Expr) : Program k :=
  composeProgram p (fun j => exprProgram k (args j))
@[simp] theorem denote_substProgram {k l : ℕ} (p : Program l) (args : Fin l → Expr)
    (xs : Fin k → ℕ) : denote (substProgram p args) xs =
      denote p (fun j => evalExpr (args j) (P02A2.LoopPrimrec.extend xs)) := by
  simp [substProgram,composeProgram_correct]

def chooseProgram : Program 3 :=
  ⟨.branch (.reg 0) (.set 3 (.reg 1)) (.set 3 (.reg 2)),3⟩
theorem choose_exact (b : Bool) (x y : ℕ) :
    denote chooseProgram ![bitNat b,x,y] = if b then x else y := by
  cases b <;> simp [denote,chooseProgram,exec,evalExpr,P02A2.LoopPrimrec.extend,bitNat]

def projection (n r : ℕ) : Program n := exprProgram n (.reg r)
def literal (n v : ℕ) : Program n := exprProgram n (.constant v)

def normalizeProgram (c : Config) (n : ℕ) : Program n :=
  substProgram (FiniteSelectorSource.normalizeRetainedProgram c.selectors)
    ![.reg 0,.reg 1,.reg 2,.reg 3,.constant (bitNat c.fallbackModel)]

def candidateProgram (c : Config) : Program 20 :=
  substProgram (FiniteSelectorSource.cycleProgram c.selectors)
    ![.reg 2,.constant (bitNat c.fallbackModel),.reg 0]

def newSupportProgram (c : Config) : Program 20 :=
  substProgram (supportProgram c.kernel) ![.reg 2,.reg 3,.reg 18,.reg 19]

def newPair : Expr := .add (.mul (.constant 2) (.reg 3)) (.reg 18)
def newCountProgram (j : Fin 4) : Program 20 :=
  exprProgram 20 (.add (.reg (6+j.val)) (.eq (.constant j.val) newPair))
def newSymbolProgram (j : Fin 8) : Program 20 :=
  exprProgram 20 (.add (.reg (10+j.val))
    (.mul (.eq (.constant (j.val/2)) newPair) (.eq (.constant (j.val%2)) (.reg 19))))

def guardArgs : Fin 13 → Program 20 := fun i =>
  if i.val = 0 then projection 20 0
  else if h : i.val < 5 then newCountProgram ⟨i.val-1,by omega⟩
  else newSymbolProgram ⟨i.val-5,by omega⟩

def fixedGuardProgram (c : Config) (θ : Bool) : Program 20 :=
  composeProgram (empiricalProgram c.toleranceNumerator c.toleranceDenominator
    c.rowDenominator c.rowNumerator θ) guardArgs

def guardProgram (c : Config) : Program 20 :=
  composeProgram chooseProgram ![candidateProgram c,fixedGuardProgram c true,fixedGuardProgram c false]

def advanceArgs (c : Config) : Fin 6 → Program 20 :=
  ![projection 20 0,normalizeProgram c 20,projection 20 2,newSupportProgram c,projection 20 19,guardProgram c]

def newPhaseProgram (c : Config) : Program 20 := composeProgram phaseProgram (advanceArgs c)
def newTargetProgram (c : Config) : Program 20 := composeProgram targetProgram (advanceArgs c)

def visitProgram (s : Bool) : Program 20 :=
  exprProgram 20 (.add (.reg (4+bitNat s)) (.eq (.reg 3) (.constant (bitNat s))))

def nextPrograms (c : Config) : Fin 18 → Program 20 := fun j =>
  if j.val = 0 then newPhaseProgram c
  else if j.val = 1 then newTargetProgram c
  else if j.val = 2 then newSupportProgram c
  else if j.val = 3 then projection 20 19
  else if j.val = 4 then visitProgram false
  else if j.val = 5 then visitProgram true
  else if h : j.val < 10 then newCountProgram ⟨j.val-6,by omega⟩
  else newSymbolProgram ⟨j.val-10,by omega⟩

def activeProgram (c : Config) : Program 18 :=
  composeProgram (FiniteSelectorSource.activePairsProgram c.selectors) ![normalizeProgram c 18,projection 18 2]

def currentVisitsProgram : Program 18 :=
  composeProgram chooseProgram ![projection 18 3,projection 18 5,projection 18 4]

def actionProgram (c : Config) : Program 18 :=
  composeProgram (FiniteSelectorSource.actionCycleProgram c.selectors)
    ![activeProgram c,projection 18 3,literal 18 (bitNat c.fallbackAction),currentVisitsProgram]

/-- Sufficient statistics. The input history is the acquired pair history;
phase memory and live support are explicit independent components. -/
def stateData (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) : Fin 18 → ℕ :=
  ![m.index,retainedCode m.retained,supportCode B,bitNat s,vf,vt,
    actionCount (false,false) h,actionCount (false,true) h,
    actionCount (true,false) h,actionCount (true,true) h,
    RationalGate.symbolCount (false,false) false h,RationalGate.symbolCount (false,false) true h,
    RationalGate.symbolCount (false,true) false h,RationalGate.symbolCount (false,true) true h,
    RationalGate.symbolCount (true,false) false h,RationalGate.symbolCount (true,false) true h,
    RationalGate.symbolCount (true,true) false h,RationalGate.symbolCount (true,true) true h]

def inputs (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) : Fin 20 → ℕ :=
  HistoryFold.stepInputs (stateData m B s vf vt h) (a,y)

def pairAt (j : Fin 4) : Bool × Bool := (decide (2 ≤ j.val),decide (j.val%2=1))

theorem pairAt_code (j : Fin 4) : pairCode (pairAt j) = j.val := by
  fin_cases j <;> rfl

theorem count_source (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) (j : Fin 4) :
    denote (newCountProgram j) (inputs m B s vf vt h a y) = actionCount (pairAt j) (((s,a),y)::h) := by
  have he := pair_code_injective (pairAt j) (s,a)
  rw [pairAt_code] at he
  fin_cases j <;> cases s <;> cases a <;>
    simp [newCountProgram,denote_exprProgram,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,
      stateData,newPair,pairAt,actionCount,List.countP_cons,bitNat,Orthemology.RuntimeBridge.bitNat]

theorem symbol_source (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) (j : Fin 8) :
    denote (newSymbolProgram j) (inputs m B s vf vt h a y) =
      RationalGate.symbolCount (coordPair j) (coordReceipt j) (((s,a),y)::h) := by
  fin_cases j <;> cases s <;> cases a <;> cases y <;>
    simp [newSymbolProgram,denote_exprProgram,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,
      stateData,newPair,coordPair,coordReceipt,RationalGate.symbolCount,List.countP_cons,
      bitNat,Orthemology.RuntimeBridge.bitNat]

theorem normalize_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (normalizeProgram c 20) (inputs m B s vf vt h a y) =
      retainedCode (normalizeMemory c.kernel menu priority c.fallbackModel B s m).retained := by
  rw [normalizeProgram,denote_substProgram]
  convert FiniteSelectorSource.normalize_retained_source_exact hc.selectors B s c.fallbackModel m using 1
  congr 1
  funext i
  fin_cases i <;> simp [evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData]

theorem candidate_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (candidateProgram c) (inputs m B s vf vt h a y) = bitNat (phaseCandidate B c.fallbackModel m) := by
  rw [candidateProgram,denote_substProgram]
  convert FiniteSelectorSource.phase_candidate_source_exact hc.selectors B c.fallbackModel m using 1

theorem support_source (c : Config) (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (newSupportProgram c) (inputs m B s vf vt h a y) = supportCode (liveUpdate c.kernel B (s,a) y) := by
  rw [newSupportProgram,denote_substProgram]
  convert support_source_exact c.kernel B s a y using 1
  congr 1
  funext i
  fin_cases i <;> simp [evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData,bitNat,Orthemology.RuntimeBridge.bitNat]

theorem guard_args_source (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    (fun i => denote (guardArgs i) (inputs m B s vf vt h a y)) =
      statisticInputs m.index (((s,a),y)::h) := by
  funext i
  fin_cases i
  · simp [guardArgs,projection,statisticInputs,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData]
  · exact count_source m B s vf vt h a y 0
  · exact count_source m B s vf vt h a y 1
  · exact count_source m B s vf vt h a y 2
  · exact count_source m B s vf vt h a y 3
  · exact symbol_source m B s vf vt h a y 0
  · exact symbol_source m B s vf vt h a y 1
  · exact symbol_source m B s vf vt h a y 2
  · exact symbol_source m B s vf vt h a y 3
  · exact symbol_source m B s vf vt h a y 4
  · exact symbol_source m B s vf vt h a y 5
  · exact symbol_source m B s vf vt h a y 6
  · exact symbol_source m B s vf vt h a y 7

theorem fixed_guard_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y θ : Bool) :
    denote (fixedGuardProgram c θ) (inputs m B s vf vt h a y) =
      bitNat (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
        θ m.index (((s,a),y)::h)) := by
  rw [fixedGuardProgram,composeProgram_correct,guard_args_source]
  exact empirical_source_exact c.kernel _ _ _ hc.toleranceDenominator_pos hc.rowDenominator_pos
    c.rowNumerator hc.row_exact θ m.index (((s,a),y)::h)

theorem guard_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (guardProgram c) (inputs m B s vf vt h a y) =
      bitNat (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
        (phaseCandidate B c.fallbackModel m) m.index (((s,a),y)::h)) := by
  rw [guardProgram,composeProgram_correct]
  have he : (fun i => denote
      (![candidateProgram c,fixedGuardProgram c true,fixedGuardProgram c false] i)
      (inputs m B s vf vt h a y)) =
      ![bitNat (phaseCandidate B c.fallbackModel m),
        bitNat (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
          true m.index (((s,a),y)::h)),
        bitNat (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
          false m.index (((s,a),y)::h))] := by
    funext i
    fin_cases i
    · exact candidate_source c menu priority hc m B s vf vt h a y
    · exact fixed_guard_source c menu priority hc m B s vf vt h a y true
    · exact fixed_guard_source c menu priority hc m B s vf vt h a y false
  rw [he,choose_exact]
  cases phaseCandidate B c.fallbackModel m <;> rfl

noncomputable def newMemory (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) : PhaseMemory Bool Bool :=
  let nm := normalizeMemory c.kernel menu priority c.fallbackModel B s m
  advanceMemory B (liveUpdate c.kernel B (s,a) y) y nm
    (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
      (phaseCandidate B c.fallbackModel nm) nm.index (((s,a),y)::h))

theorem advance_args_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    (fun i => denote (advanceArgs c i) (inputs m B s vf vt h a y)) =
      args B (liveUpdate c.kernel B (s,a) y) y
        (normalizeMemory c.kernel menu priority c.fallbackModel B s m)
        (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)
          (phaseCandidate B c.fallbackModel (normalizeMemory c.kernel menu priority c.fallbackModel B s m))
          m.index (((s,a),y)::h)) := by
  funext i
  fin_cases i
  · simp [advanceArgs,projection,args,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData]
  · exact normalize_source c menu priority hc m B s vf vt h a y
  · simp [advanceArgs,projection,args,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData]
  · exact support_source c m B s vf vt h a y
  · simp [advanceArgs,projection,args,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,stateData,
      bitNat,Orthemology.RuntimeBridge.bitNat]
  · simpa only [phaseCandidate,normalizeMemory_index] using guard_source c menu priority hc m B s vf vt h a y

theorem phase_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (newPhaseProgram c) (inputs m B s vf vt h a y) = (newMemory c menu priority m B s h a y).index := by
  rw [newPhaseProgram,composeProgram_correct,advance_args_source c menu priority hc,phase_source_exact]
  simp only [newMemory,normalizeMemory_index]

theorem target_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) :
    denote (newTargetProgram c) (inputs m B s vf vt h a y) =
      retainedCode (newMemory c menu priority m B s h a y).retained := by
  rw [newTargetProgram,composeProgram_correct,advance_args_source c menu priority hc,target_source_exact]
  simp only [newMemory,normalizeMemory_index]

theorem next_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) (a y : Bool) (j : Fin 18) :
    denote (nextPrograms c j) (inputs m B s vf vt h a y) =
      stateData (newMemory c menu priority m B s h a y) (liveUpdate c.kernel B (s,a) y) y
        (vf+if s=false then 1 else 0) (vt+if s=true then 1 else 0) (((s,a),y)::h) j := by
  fin_cases j
  · exact phase_source c menu priority hc m B s vf vt h a y
  · exact target_source c menu priority hc m B s vf vt h a y
  · exact support_source c m B s vf vt h a y
  · simp [nextPrograms,projection,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,
      stateData,bitNat,Orthemology.RuntimeBridge.bitNat]
  · cases s <;> simp [nextPrograms,visitProgram,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,
      stateData,bitNat,Orthemology.RuntimeBridge.bitNat]
  · cases s <;> simp [nextPrograms,visitProgram,evalExpr,P02A2.LoopPrimrec.extend,inputs,HistoryFold.stepInputs,
      stateData,bitNat,Orthemology.RuntimeBridge.bitNat]
  · exact count_source m B s vf vt h a y 0
  · exact count_source m B s vf vt h a y 1
  · exact count_source m B s vf vt h a y 2
  · exact count_source m B s vf vt h a y 3
  · exact symbol_source m B s vf vt h a y 0
  · exact symbol_source m B s vf vt h a y 1
  · exact symbol_source m B s vf vt h a y 2
  · exact symbol_source m B s vf vt h a y 3
  · exact symbol_source m B s vf vt h a y 4
  · exact symbol_source m B s vf vt h a y 5
  · exact symbol_source m B s vf vt h a y 6
  · exact symbol_source m B s vf vt h a y 7

theorem normalize_state_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) :
    denote (normalizeProgram c 18) (stateData m B s vf vt h) =
      retainedCode (normalizeMemory c.kernel menu priority c.fallbackModel B s m).retained := by
  rw [normalizeProgram,denote_substProgram]
  convert FiniteSelectorSource.normalize_retained_source_exact hc.selectors B s c.fallbackModel m using 1
  congr 1
  funext i
  fin_cases i <;> simp [evalExpr,P02A2.LoopPrimrec.extend,stateData]

theorem active_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) :
    denote (activeProgram c) (stateData m B s vf vt h) =
      targetCode (activePairs c.kernel menu priority B
        (normalizeMemory c.kernel menu priority c.fallbackModel B s m)) := by
  rw [activeProgram,composeProgram_correct]
  have ha : (fun i => denote (![normalizeProgram c 18,projection 18 2] i) (stateData m B s vf vt h)) =
      ![retainedCode (normalizeMemory c.kernel menu priority c.fallbackModel B s m).retained,supportCode B] := by
    funext i
    fin_cases i
    · exact normalize_state_source c menu priority hc m B s vf vt h
    · simp [projection,evalExpr,P02A2.LoopPrimrec.extend,stateData]
  rw [ha,FiniteSelectorSource.active_pairs_source_exact hc.selectors]

theorem current_visits_source (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) :
    denote currentVisitsProgram (stateData m B s vf vt h) = if s then vt else vf := by
  rw [currentVisitsProgram,composeProgram_correct]
  cases s <;> simp [chooseProgram,projection,exprProgram,
    denote,exec,evalExpr,P02A2.LoopPrimrec.extend,stateData,bitNat]

theorem action_source (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) :
    denote (actionProgram c) (stateData m B s vf vt h) =
      bitNat (cycleAction (retainedActions (activePairs c.kernel menu priority B
        (normalizeMemory c.kernel menu priority c.fallbackModel B s m)) s)
        c.fallbackAction (if s then vt else vf)) := by
  rw [actionProgram,composeProgram_correct]
  have ha : (fun i => denote
      (![activeProgram c,projection 18 3,literal 18 (bitNat c.fallbackAction),currentVisitsProgram] i)
      (stateData m B s vf vt h)) =
      ![targetCode (activePairs c.kernel menu priority B
          (normalizeMemory c.kernel menu priority c.fallbackModel B s m)),
        bitNat s,bitNat c.fallbackAction,if s then vt else vf] := by
    funext i
    fin_cases i
    · exact active_source c menu priority hc m B s vf vt h
    · simp [projection,evalExpr,P02A2.LoopPrimrec.extend,stateData]
    · simp [literal,evalExpr]
    · exact current_visits_source m B s vf vt h
  rw [ha,FiniteSelectorSource.action_cycle_source_exact hc.selectors]

noncomputable def rep (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (h : HistoryFold.History) : Fin 18 → ℕ :=
  stateData
    (phaseMemory c.kernel menu priority c.initialSupport c.initialState c.fallbackModel
      (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)) h)
    (liveHistory c.kernel c.initialSupport (augmentHistory c.initialState h))
    (observedState c.initialState h)
    (historyVisits c.initialState false h) (historyVisits c.initialState true h)
    (augmentHistory c.initialState h)

noncomputable def policy (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) : HistoryFold.History → Bool :=
  generatedPhasePolicy c.kernel menu priority c.initialSupport c.initialState c.fallbackModel c.fallbackAction
    (RationalGate.reject c.kernel ((c.toleranceNumerator : ℚ)/c.toleranceDenominator)) ()

theorem next_rep_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (e : Bool × Bool) (h : HistoryFold.History) (j : Fin 18) :
    denote (nextPrograms c j) (HistoryFold.stepInputs (rep c menu priority h) e) =
      rep c menu priority (e::h) j := by
  change denote (nextPrograms c j) (inputs _ _ _ _ _ _ e.1 e.2) = _
  rw [next_source c menu priority hc]
  simp only [rep,phaseMemory,augmentHistory,liveHistory_cons,observedState,historyVisits,newMemory]

theorem action_rep_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    denote (actionProgram c) (rep c menu priority h) = bitNat (policy c menu priority h) := by
  rw [rep,action_source c menu priority hc]
  have hv : (if observedState c.initialState h then historyVisits c.initialState true h
      else historyVisits c.initialState false h) = historyVisits c.initialState (observedState c.initialState h) h := by
    cases observedState c.initialState h <;> rfl
  rw [hv]
  rfl

def initialStmt (c : Config) : Stmt :=
  P02A2.PRProgram.sequence [
    .set 3 (.constant (0)),
    .set 4 (.constant (0)),
    .set 5 (.constant (supportCode c.initialSupport)),
    .set 6 (.constant (bitNat c.initialState)),
    .set 7 (.constant (0)),
    .set 8 (.constant (0)),
    .set 9 (.constant (0)),
    .set 10 (.constant (0)),
    .set 11 (.constant (0)),
    .set 12 (.constant (0)),
    .set 13 (.constant (0)),
    .set 14 (.constant (0)),
    .set 15 (.constant (0)),
    .set 16 (.constant (0)),
    .set 17 (.constant (0)),
    .set 18 (.constant (0)),
    .set 19 (.constant (0)),
    .set 20 (.constant (0))]

theorem initial_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) :
    HistoryFold.InitImplements (initialStmt c) (rep c menu priority) := by
  intro code remaining σ h0 h1
  refine ⟨?_,?_,?_⟩
  · simpa [initialStmt,P02A2.PRProgram.sequence,exec] using h0
  · simpa [initialStmt,P02A2.PRProgram.sequence,exec] using h1
  · intro j
    fin_cases j <;>
      simp [initialStmt,P02A2.PRProgram.sequence,exec,evalExpr,rep,stateData,
        phaseMemory,augmentHistory,observedState,historyVisits,actionCount,RationalGate.symbolCount,retainedCode]

/-- The complete arity-one history-policy source. All eighteen sufficient-state
components are generated locally and replayed in acquired chronological order. -/
def rawPolicyProgram (c : Config) : Program 1 :=
  HistoryFold.compiled (initialStmt c)
    (HistoryFold.parallelStep (nextPrograms c) (HistoryFold.stepArgs 18)) (actionProgram c)

/-- Exact full phase-controller extraction from finite selector and rational
coefficient certificates. No whole-history or probability-law premise occurs. -/
theorem raw_policy_source_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    denote (rawPolicyProgram c) ![HistoryRuntime.encodeHistory h] = bitNat (policy c menu priority h) := by
  exact HistoryFold.compiled_history_exact (initialStmt c) _ (actionProgram c)
    (rep c menu priority) (policy c menu priority) (initial_exact c menu priority)
    (HistoryFold.parallel_implements (nextPrograms c) (rep c menu priority)
      (next_rep_exact c menu priority hc)) (action_rep_exact c menu priority hc) h

/-- Boolean normalization gives a total contract even for malformed natural
history codes. It does not synthesize receipts on a rejected input tape. -/
def policyProgram (c : Config) : Program 1 :=
  composeProgram (exprProgram 1 (.mod (.reg 0) (.constant 2))) (fun _ : Fin 1 => rawPolicyProgram c)

def sourcePolicy (c : Config) (code : ℕ) : Bool :=
  decide (denote (rawPolicyProgram c) ![code] % 2 = 1)

theorem policy_program_implements (c : Config) :
    HistoryRuntime.PolicyImplements (policyProgram c) (sourcePolicy c) := by
  intro code
  rw [policyProgram,composeProgram_correct,denote_exprProgram]
  simp only [evalExpr,P02A2.LoopPrimrec.extend,show (0:ℕ)<1 by decide,↓reduceDIte]
  exact (HistoryRuntime.bitNat_mod _).symm

theorem source_policy_retained_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    sourcePolicy c (HistoryRuntime.encodeHistory h) = policy c menu priority h := by
  unfold sourcePolicy
  rw [raw_policy_source_exact c menu priority hc h]
  cases policy c menu priority h <;> rfl

theorem policy_program_retained_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    denote (policyProgram c) ![HistoryRuntime.encodeHistory h] = bitNat (policy c menu priority h) := by
  rw [policy_program_implements c,source_policy_retained_exact c menu priority hc]
  rfl

end Orthemology.RuntimeBridge.PhaseUpdate.FullController
