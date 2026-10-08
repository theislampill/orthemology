import SelectorTableNormalForm
set_option autoImplicit false

/-! A2 domain derivation. The domains come from the actual source-history fold
and its protected parallel inputs. They are not assumptions about arbitrary
natural component inputs, which A1 showed can distinguish unused high bits. -/
namespace Orthemology.Ninth.SelectorTransport
open HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.Eighth.SemanticControls
open Orthemology.Ninth.SelectorExtraction
open P02A2.ObserverCore P02A2.PRProgram

/-- The source's stored selector-relevant sufficient-statistic slots. -/
def StateDomain (v : Fin 18 → ℕ) : Prop :=
  v 2 < 4 ∧ v 3 < 2 ∧ v 1 ≤ 16

/-- The parallel step adds one actual Boolean action and receipt. -/
def StepDomain (v : Fin 20 → ℕ) : Prop :=
  v 2 < 4 ∧ v 3 < 2 ∧ v 1 ≤ 16 ∧ v 18 < 2 ∧ v 19 < 2

theorem stateData_domain (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : History (Bool × Bool) Bool) :
    StateDomain (stateData m B s vf vt h) := by
  change supportCode B < 4 ∧ bitNat s < 2 ∧ retainedCode m.retained ≤ 16
  exact ⟨supportCode_lt B, bitNat_lt s, retained_encoding_le_sixteen _⟩

theorem inputs_domain (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool)
    (vf vt : ℕ) (h : History (Bool × Bool) Bool) (a y : Bool) :
    StepDomain (inputs m B s vf vt h a y) := by
  change supportCode B < 4 ∧ bitNat s < 2 ∧ retainedCode m.retained ≤ 16 ∧
    bitNat a < 2 ∧ bitNat y < 2
  exact ⟨supportCode_lt B, bitNat_lt s, retained_encoding_le_sixteen _, bitNat_lt a, bitNat_lt y⟩

theorem represented_state_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (h : HistoryFold.History) :
    StateDomain (rep c menu priority h) := by
  unfold rep
  exact stateData_domain _ _ _ _ _ _

theorem represented_step_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (h : HistoryFold.History) (e : Bool × Bool) :
    StepDomain (HistoryFold.stepInputs (rep c menu priority h) e) := by
  unfold rep
  exact inputs_domain _ _ _ _ _ _ e.1 e.2

/-- The data view at the actual raw policy's source-register boundary. -/
def dataView (σ : Store) : Fin 18 → ℕ := fun j => σ (3+j.val)

theorem matched_state_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (code : ℕ)
    (remaining accumulated : HistoryFold.History) (σ : Store)
    (hm : HistoryFold.Matches (rep c menu priority) code remaining accumulated σ) :
    StateDomain (dataView σ) := by
  have hv : dataView σ = rep c menu priority accumulated := funext hm.2.2
  rw [hv]
  exact represented_state_domain c menu priority accumulated

/-- Every parallel component sees the protected old state and the current
accepted digit, as derived from the compiler's actual expression arguments. -/
theorem actual_step_arguments_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (code : ℕ) (e : Bool × Bool)
    (remaining accumulated : HistoryFold.History) (σ : Store)
    (hm : HistoryFold.Matches (rep c menu priority) code (e::remaining) accumulated σ) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j) σ) := by
  rw [HistoryFold.step_args_value (rep c menu priority) code e remaining accumulated σ hm]
  exact represented_step_domain c menu priority accumulated e

/-- This is literally the reverse-call prefix of rawPolicyProgram's compiler. -/
def reversePrefix (h : HistoryFold.History) : Store :=
  exec (call HistoryFold.reverseProgram 22 HistoryFold.reverseArgs 1)
    (P02A2.LoopPrimrec.extend ![Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h])

theorem reverse_prefix_registers (h : HistoryFold.History) :
    reversePrefix h 0 = Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h ∧
    reversePrefix h 1 = Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h.reverse := by
  constructor
  · unfold reversePrefix
    rw [call_frame _ _ _ _ (HistoryFold.reverse_args_fresh 18) 0 (by decide) (by decide)]
    simp [P02A2.LoopPrimrec.extend]
  · unfold reversePrefix
    rw [call_value _ _ _ _ (HistoryFold.reverse_args_fresh 18)]
    have ha : (fun i => evalExpr (HistoryFold.reverseArgs i)
        (P02A2.LoopPrimrec.extend ![Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h])) =
        ![Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h] := by
      funext i
      fin_cases i
      rfl
    rw [ha, HistoryFold.reverse_source_exact]

/-- The actual state at entry to the history-fold loop. -/
def foldStart (c : Config) (h : HistoryFold.History) : Store := exec (initialStmt c) (reversePrefix h)

def controllerStep (c : Config) : Stmt :=
  HistoryFold.parallelStep (nextPrograms c) (HistoryFold.stepArgs 18)

theorem foldStart_matches (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (h : HistoryFold.History) :
    HistoryFold.Matches (rep c menu priority)
      (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h) h.reverse [] (foldStart c h) :=
  initial_exact c menu priority _ _ _ (reverse_prefix_registers h).1 (reverse_prefix_registers h).2

theorem controllerStep_implements (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    HistoryFold.StepImplements (controllerStep c) (rep c menu priority) :=
  HistoryFold.parallel_implements (nextPrograms c) (rep c menu priority)
    (next_rep_exact c menu priority hc)

/-- No arbitrary-store validity premise remains: initialization from an encoded
history and the exact source step derive the invariant at every loop index. -/
theorem actual_fold_iteration_matches (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) :
    HistoryFold.Matches (rep c menu priority)
      (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h)
      ((HistoryFold.consume^[n]) (h.reverse,[])).1 ((HistoryFold.consume^[n]) (h.reverse,[])).2
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) :=
  HistoryFold.loop_exact (controllerStep c) (rep c menu priority)
    (controllerStep_implements c menu priority hc) _ _ _ (foldStart_matches c menu priority h) n

theorem actual_fold_iteration_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) :
    StateDomain (dataView
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h))) :=
  matched_state_domain c menu priority _ _ _ _ (actual_fold_iteration_matches c menu priority hc h n)

/-- When the actual loop has a digit to consume, every component's evaluated
parallel argument vector is in the certified finite domain. -/
theorem actual_fold_call_arguments_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (e : Bool × Bool) (remaining : HistoryFold.History)
    (hr : ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h))) := by
  have hm := actual_fold_iteration_matches c menu priority hc h n
  rw [hr] at hm
  exact actual_step_arguments_domain c menu priority _ e remaining _ _ hm

/-- Sentinel padding contains no source step and hence no selector access. -/
theorem empty_fold_body_noop (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (code : ℕ) (acc : HistoryFold.History) (σ : Store)
    (hm : HistoryFold.Matches (rep c menu priority) code [] acc σ) :
    exec (HistoryFold.foldBody (controllerStep c)) σ = σ := by
  have h1 := hm.2.1
  simp [HistoryFold.foldBody, exec, evalExpr, h1,
    Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory]

theorem actual_fold_padding_noop (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (hn : h.length ≤ n) :
    let σ := runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)
    exec (HistoryFold.foldBody (controllerStep c)) σ = σ := by
  have hm := actual_fold_iteration_matches c menu priority hc h n
  rw [HistoryFold.consume_complete h.reverse [] n (by simpa using hn)] at hm
  exact empty_fold_body_noop c menu priority _ _ _ hm

/-- The exact address used by cycleExpr, including the unbounded index's residue. -/
def cycleAddress (B : Finset Bool) (fallback : Bool) (n : ℕ) : ℕ :=
  4*supportCode B + 2*bitNat fallback + n%2

def targetAddress (B : Finset Bool) (candidate state : Bool) : ℕ :=
  4*supportCode B + 2*bitNat candidate + bitNat state

theorem cycle_address_in_domain (B : Finset Bool) (fallback : Bool) (n : ℕ) :
    cycleAddress B fallback n < 16 := by
  have hB := supportCode_lt B
  have hf := bitNat_lt fallback
  have hn : n%2 < 2 := Nat.mod_lt _ (by decide)
  unfold cycleAddress
  omega

theorem target_address_in_domain (B : Finset Bool) (candidate state : Bool) :
    targetAddress B candidate state < 16 :=
  (cellIndex B candidate state).isLt

/-- The action-call support is exactly a finite row menu, not an unchecked mask. -/
theorem action_menu_code_exact (E : Finset (Bool × Bool)) (s : Bool) :
    targetCode E / 2^(2*bitNat s) % 4 = supportCode (retainedActions E s) :=
  FiniteSelectorSource.retained_actions_code E s

theorem action_menu_code_in_domain (E : Finset (Bool × Bool)) (s : Bool) :
    targetCode E / 2^(2*bitNat s) % 4 < 4 := by
  rw [action_menu_code_exact]
  exact supportCode_lt _

/-- The source candidate returned to targetExpr is a genuine encoded Boolean. -/
theorem source_candidate_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) (a y : Bool) :
    denote (candidateProgram c) (inputs m B s vf vt h a y) < 2 := by
  rw [candidate_source c menu priority hc]
  exact bitNat_lt _

/-- The normalized optional-target payload stays in the 17 valid codes. -/
theorem source_normalize_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) (a y : Bool) :
    denote (normalizeProgram c 20) (inputs m B s vf vt h a y) ≤ 16 := by
  rw [normalize_source c menu priority hc]
  exact retained_encoding_le_sixteen _

/-- The final action source receives an actual finite active-pair mask. -/
theorem source_active_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) :
    denote (activeProgram c) (stateData m B s vf vt h) < 16 := by
  rw [active_source c menu priority hc]
  exact targetCode_lt _

theorem source_action_menu_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) :
    denote (activeProgram c) (stateData m B s vf vt h) / 2^(2*bitNat s) % 4 =
      supportCode (retainedActions (activePairs c.kernel menu priority B
        (normalizeMemory c.kernel menu priority c.fallbackModel B s m)) s) := by
  rw [active_source c menu priority hc, action_menu_code_exact]


/-- A source-level domain property with no assumed valid raw-call arguments.
It quantifies the actual compiled loop from every encoded acquired history. -/
def DerivedCallDomains (c : Config) : Prop :=
  ∀ (h : HistoryFold.History) (n : ℕ),
    StateDomain (dataView
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h))) ∧
    (∀ (e : Bool × Bool) (remaining : HistoryFold.History),
      ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining →
      StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
        (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)))) ∧
    (h.length ≤ n →
      let σ := runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)
      exec (HistoryFold.foldBody (controllerStep c)) σ = σ)

theorem derived_call_domains (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    DerivedCallDomains c := by
  intro h n
  exact ⟨actual_fold_iteration_domain c menu priority hc h n,
    fun e remaining hr => actual_fold_call_arguments_domain c menu priority hc h n e remaining hr,
    fun hn => actual_fold_padding_noop c menu priority hc h n hn⟩


/-- At the real final readout boundary, the compiler's argument expressions
recover the whole represented acquired history, not merely some valid slots. -/
theorem actual_readout_arguments_exact (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    (fun j => evalExpr (HistoryFold.dataArgs 18 j)
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2
        (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h) (foldStart c h))) =
      rep c menu priority h := by
  have hm := actual_fold_iteration_matches c menu priority hc h
    (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h)
  rw [HistoryFold.consume_complete h.reverse [] _ (by simpa using HistoryFold.length_le_code h)] at hm
  simp only [List.reverse_reverse, List.append_nil] at hm
  exact funext hm.2.2

theorem actual_readout_arguments_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) :
    StateDomain (fun j => evalExpr (HistoryFold.dataArgs 18 j)
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2
        (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h) (foldStart c h))) := by
  rw [actual_readout_arguments_exact c menu priority hc]
  exact represented_state_domain c menu priority h

/-- The concrete source-computed candidate, rather than an assumed Boolean
oracle, gives an address among the sixteen target cells. -/
theorem source_target_address_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) (a y : Bool) :
    4*supportCode B + 2*denote (candidateProgram c) (inputs m B s vf vt h a y) + bitNat s < 16 := by
  rw [candidate_source c menu priority hc]
  exact target_address_in_domain B (phaseCandidate B c.fallbackModel m) s

/-- This is the final actionCycleProgram's actual address expression. Its menu
comes from the source-computed active mask and its visit count may be unbounded. -/
theorem source_action_address_in_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (m : PhaseMemory Bool Bool) (B : Finset Bool) (s : Bool) (vf vt : ℕ)
    (h : History (Bool × Bool) Bool) :
    4*(denote (activeProgram c) (stateData m B s vf vt h) / 2^(2*bitNat s) % 4) +
      2*bitNat c.fallbackAction + (if s then vt else vf)%2 < 16 := by
  rw [source_action_menu_in_domain c menu priority hc]
  exact cycle_address_in_domain _ c.fallbackAction (if s then vt else vf)


/-- The LOOP interpreter writes register 2 immediately before the body.
That write preserves every component of the actual history representation. -/
theorem matches_loop_index_update (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (code : ℕ)
    (remaining accumulated : HistoryFold.History) (σ : Store) (n : ℕ)
    (hm : HistoryFold.Matches (rep c menu priority) code remaining accumulated σ) :
    HistoryFold.Matches (rep c menu priority) code remaining accumulated (Function.update σ 2 n) := by
  refine ⟨?_, ?_, ?_⟩
  · simpa using hm.1
  · simpa using hm.2.1
  · intro j
    rw [Function.update_of_ne (by omega : 3+j.val ≠ 2)]
    exact hm.2.2 j

/-- Exact actual body-entry argument bounds, including the interpreter's fresh
loop-index write. The index is not silently omitted from the concrete store. -/
theorem actual_body_entry_arguments_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (e : Bool × Bool) (remaining : HistoryFold.History)
    (hr : ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n)) := by
  have hm := matches_loop_index_update c menu priority _ _ _ _ n
    (actual_fold_iteration_matches c menu priority hc h n)
  rw [hr] at hm
  exact actual_step_arguments_domain c menu priority _ e remaining _ _ hm

theorem actual_body_entry_padding_noop (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (hn : h.length ≤ n) :
    let σ := Function.update
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n
    exec (HistoryFold.foldBody (controllerStep c)) σ = σ := by
  have hm := matches_loop_index_update c menu priority _ _ _ _ n
    (actual_fold_iteration_matches c menu priority hc h n)
  rw [HistoryFold.consume_complete h.reverse [] n (by simpa using hn)] at hm
  exact empty_fold_body_noop c menu priority _ _ _ hm


/-- After every partial collection of parallel components, the old argument
registers are still protected. Thus later component calls retain the same
valid domain; this is not merely a statement about the first call. -/
theorem parallel_prefix_arguments_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (code : ℕ) (e : Bool × Bool)
    (remaining accumulated : HistoryFold.History) (σ : Store)
    (hm : HistoryFold.Matches (rep c menu priority) code (e::remaining) accumulated σ)
    (order : List (Fin 18)) (hn : order.Nodup) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18) order) σ)) := by
  have hp := (HistoryFold.collect_correct (nextPrograms c) (HistoryFold.stepArgs 18)
    (HistoryFold.step_args_fresh 18) order hn σ).1
  have he : (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18) order) σ)) =
      (fun j => evalExpr (HistoryFold.stepArgs 18 j) σ) := by
    funext j
    apply P02A2.LoopRenaming.evalExpr_congr
    intro r hr
    exact hp r (HistoryFold.step_args_fresh 18 j r hr)
  rw [he]
  exact actual_step_arguments_domain c menu priority code e remaining accumulated σ hm

theorem actual_body_parallel_prefix_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (e : Bool × Bool) (remaining : HistoryFold.History)
    (hr : ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining)
    (order : List (Fin 18)) (hn : order.Nodup) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18) order)
        (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n))) := by
  have hm := matches_loop_index_update c menu priority _ _ _ _ n
    (actual_fold_iteration_matches c menu priority hc h n)
  rw [hr] at hm
  exact parallel_prefix_arguments_domain c menu priority _ e remaining _ _ hm order hn


/-- In particular, every prefix of the compiler's actual eighteen-component
order has valid arguments; its no-duplicate premise is discharged internally. -/
theorem actual_ordered_component_domain (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority)
    (h : HistoryFold.History) (n : ℕ) (e : Bool × Bool) (remaining : HistoryFold.History)
    (hr : ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining) (k : ℕ) :
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18) ((List.finRange 18).take k))
        (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n))) :=
  actual_body_parallel_prefix_domain c menu priority hc h n e remaining hr _
    (List.Nodup.sublist (List.take_sublist k _) (List.nodup_finRange 18))


/-- Bundled actual call-boundary domains: the derived fold invariant, every
ordered component entry after the LOOP write, and the final readout arguments. -/
def CompiledCallDomains (c : Config) : Prop :=
  DerivedCallDomains c ∧
  (∀ (h : HistoryFold.History) (n : ℕ) (e : Bool × Bool) (remaining : HistoryFold.History),
    ((HistoryFold.consume^[n]) (h.reverse,[])).1 = e::remaining → ∀ k : ℕ,
    StepDomain (fun j => evalExpr (HistoryFold.stepArgs 18 j)
      (exec (HistoryFold.collect (nextPrograms c) (HistoryFold.stepArgs 18) ((List.finRange 18).take k))
        (Function.update (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2 n (foldStart c h)) 2 n)))) ∧
  (∀ h : HistoryFold.History,
    StateDomain (fun j => evalExpr (HistoryFold.dataArgs 18 j)
      (runLoop (exec (HistoryFold.foldBody (controllerStep c))) 2
        (Orthemology.RuntimeBridge.HistoryRuntime.encodeHistory h) (foldStart c h))))

theorem compiled_call_domains (c : Config) (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ) (hc : Certificate c menu priority) :
    CompiledCallDomains c :=
  ⟨derived_call_domains c menu priority hc,
    actual_ordered_component_domain c menu priority hc,
    actual_readout_arguments_domain c menu priority hc⟩

end Orthemology.Ninth.SelectorTransport
