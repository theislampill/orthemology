import PrunedWitness

/-!
Programme-specific product lift. The bearer, token identity, external grant,
and common support are stipulated model data. No physical provenance,
authority, resources, or numerical identity is derived from these definitions.
-/

namespace EffectiveRenewal.Contract

abbrev State := Bool × Bool
abbrev Config := Word × (State × Bool)

def delayStep (q : State) (i : Bool) : State := (q.2, i)
def readout (q : State) : Bool := q.1

theorem delay_nonvacuous :
    readout (false, false) = readout (false, true) ∧
    readout (delayStep (false, false) false) ≠
      readout (delayStep (false, true) false) := by decide

def twist (b : Bool) (q : State) : State :=
  if b then (!q.1, !q.2) else q

def encoding (generation : Nat) : State → State := twist generation.bodd

@[simp] theorem twist_twist (b : Bool) (q : State) : twist b (twist b q) = q := by
  cases b <;> simp [twist]

@[simp] theorem encoding_inverse (n : Nat) (q : State) : encoding n (encoding n q) = q :=
  twist_twist _ _

def abstractState (c : Config) : State := encoding c.1.length c.2.1

def operativeReadout (c : Config) : Bool := readout (abstractState c)

def initial (q : State) : Config := ([], (q, true))

def execute (c : Config) (i : Bool) : Config :=
  (c.1, (encoding c.1.length (delayStep (abstractState c) i), c.2.2))

def migrate (c : Config) (b : Bool) : Config :=
  (c.1 ++ [b], (encoding (c.1.length + 1) (abstractState c), true))

def terminate (c : Config) : Config := (c.1, (c.2.1, false))

/-- Permission is external input. Invalid admission does not create a successor. -/
def request (permission choice : Bool) (c : Config) : Config :=
  if c.2.2 then
    if permission then
      if treeCheck (c.1 ++ [choice]) then migrate c choice else c
    else terminate c
  else c

/-- Actual transition history; a copied history label alone is not this relation. -/
def RenewalStep (permission choice : Bool) (c d : Config) : Prop :=
  c.2.2 = true ∧ permission = true ∧ diagonalTree (c.1 ++ [choice]) ∧ d = migrate c choice

inductive Support where
  | commonPlatform
  | commonConstructor
  | externalAuthority
  | instanceToken (generation : Nat)
  deriving DecidableEq, Repr

/-- Finite generation tokens are distinct from the retained common support. -/
def operativeSupport (c : Config) : Support → Prop
  | .instanceToken n => c.2.2 = true ∧ n = c.1.length
  | _ => True

@[simp] theorem execute_abstract (c : Config) (i : Bool) :
    abstractState (execute c i) = delayStep (abstractState c) i := by
  simp [execute, abstractState]

@[simp] theorem migrate_abstract (c : Config) (b : Bool) :
    abstractState (migrate c b) = abstractState c := by
  simp [migrate, abstractState]

@[simp] theorem migrate_readout (c : Config) (b : Bool) :
    operativeReadout (migrate c b) = operativeReadout c := by
  simp [operativeReadout]

theorem predecessor_token_excluded (c : Config) (b : Bool) :
    ¬ operativeSupport (migrate c b) (.instanceToken c.1.length) := by
  simp [operativeSupport, migrate]

theorem all_older_tokens_excluded (c : Config) (b : Bool) (k : Nat) (hk : k ≤ c.1.length) :
    ¬ operativeSupport (migrate c b) (.instanceToken k) := by
  simp [operativeSupport, migrate]
  omega

theorem common_support_retained (c : Config) (b : Bool) :
    operativeSupport (migrate c b) .commonPlatform ∧
    operativeSupport (migrate c b) .commonConstructor ∧
    operativeSupport (migrate c b) .externalAuthority := by
  simp [operativeSupport]

theorem renewal_step_executes {p b : Bool} {c d : Config} (h : RenewalStep p b c d) :
    request p b c = d := by
  rcases h with ⟨hc, rfl, ht, rfl⟩
  simp [request, hc, diagonalTree] at ht ⊢
  simp [ht]

theorem revocation_terminates (c : Config) (b : Bool) (hc : c.2.2 = true) :
    request false b c = terminate c ∧ (request false b c).2.2 = false := by
  simp [request, hc, terminate]

theorem revoked_no_renewal (c d : Config) (b : Bool) : ¬ RenewalStep false b c d := by
  simp [RenewalStep]

/-- Finite runs record the actual service-input order; renewals are stuttering. -/
inductive Run : Config → List Bool → Config → Prop
  | nil (c) : Run c [] c
  | service {c d inputs} (i : Bool) (active : c.2.2 = true)
      (tail : Run (execute c i) inputs d) : Run c (i :: inputs) d
  | renewal {c d z inputs p b} (edge : RenewalStep p b c d)
      (tail : Run d inputs z) : Run c inputs z

theorem run_preserves_contract {c d : Config} {inputs : List Bool} (h : Run c inputs d) :
    abstractState d = inputs.foldl delayStep (abstractState c) := by
  induction h with
  | nil => rfl
  | service i active tail ih => simpa using ih
  | renewal edge tail ih =>
    rcases edge with ⟨_, _, _, rfl⟩
    simpa using ih

def serviceState (inputs : Nat → Bool) (q : State) : Nat → State
  | 0 => q
  | n + 1 => delayStep (serviceState inputs q n) (inputs n)

def configurationAt (route : Word) (inputs : Nat → Bool) (q : State) (j : Nat) : Config :=
  (route.take j, (encoding (route.take j).length (serviceState inputs q j), true))

@[simp] theorem configurationAt_abstract (route : Word) (inputs : Nat → Bool) (q : State) (j : Nat) :
    abstractState (configurationAt route inputs q j) = serviceState inputs q j := by
  simp [configurationAt, abstractState]

theorem configurationAt_next (route : Word) (inputs : Nat → Bool) (q : State)
    {j : Nat} (hj : j < route.length) :
    configurationAt route inputs q (j + 1) =
      migrate (execute (configurationAt route inputs q j) (inputs j)) route[j] := by
  have ht : route.take (j + 1) = route.take j ++ [route[j]] := List.take_succ_eq_append_getElem hj
  apply Prod.ext
  · exact ht
  · simp [configurationAt, migrate, execute, abstractState, serviceState,
      List.length_take, Nat.min_eq_left (Nat.le_of_lt hj),
      Nat.min_eq_left (Nat.succ_le_of_lt hj)]

theorem finite_plan_round_correct (n : Nat) (inputs : Nat → Bool) (q : State)
    {j : Nat} (hj : j < n) :
    RenewalStep true ((finitePlan n)[j]'(by simpa using hj))
      (execute (configurationAt (finitePlan n) inputs q j) (inputs j))
      (configurationAt (finitePlan n) inputs q (j + 1)) ∧
    abstractState (configurationAt (finitePlan n) inputs q (j + 1)) =
      delayStep (serviceState inputs q j) (inputs j) ∧
    ¬ operativeSupport (configurationAt (finitePlan n) inputs q (j + 1)) (.instanceToken j) := by
  have hjr : j < (finitePlan n).length := by simpa using hj
  have he := configurationAt_next (finitePlan n) inputs q hjr
  refine ⟨?_, ?_, ?_⟩
  · refine ⟨rfl, rfl, ?_, he⟩
    change diagonalTree ((finitePlan n).take j ++ [(finitePlan n)[j]])
    rw [← List.take_succ_eq_append_getElem hjr]
    exact finitePlan_prefix_admitted n (j + 1)
  · simp [serviceState]
  · rw [he]
    have hg : (execute (configurationAt (finitePlan n) inputs q j) (inputs j)).1.length = j := by
      simp [execute, configurationAt, Nat.min_eq_left (Nat.le_of_lt hj)]
    simpa only [hg] using predecessor_token_excluded
      (execute (configurationAt (finitePlan n) inputs q j) (inputs j)) ((finitePlan n)[j])

def serviceInputs (inputs : Nat → Bool) (start : Nat) : Nat → List Bool
  | 0 => []
  | count + 1 => inputs start :: serviceInputs inputs (start + 1) count

theorem finite_plan_run_from (n : Nat) (inputs : Nat → Bool) (q : State)
    (j k : Nat) (hjk : j + k ≤ n) :
    Run (configurationAt (finitePlan n) inputs q j) (serviceInputs inputs j k)
      (configurationAt (finitePlan n) inputs q (j + k)) := by
  induction k generalizing j with
  | zero => simpa [serviceInputs] using Run.nil (configurationAt (finitePlan n) inputs q j)
  | succ k ih =>
    have hj : j < n := by omega
    have edge := (finite_plan_round_correct n inputs q hj).1
    have tail := ih (j + 1) (by omega)
    have hr := Run.service (inputs j) rfl (Run.renewal edge tail)
    simpa [serviceInputs, Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using hr

theorem finite_plan_whole_run (n : Nat) (inputs : Nat → Bool) (q : State) :
    Run (initial q) (serviceInputs inputs 0 n)
      (configurationAt (finitePlan n) inputs q n) := by
  have h := finite_plan_run_from n inputs q 0 n (by omega)
  simpa [configurationAt, initial, serviceState, encoding, twist] using h

/-- Permission and service input, supplied independently of the controller. -/
abbrev Environment := Nat → Bool × Bool

def alwaysAuthorisedZero : Environment := fun _ => (true, false)

/-- A bounded effective observer sees finite environment observations and time.
Its fixed finite program includes every counted computable technical support. -/
abbrev Observer := ((Word × Word) × Nat) → Word

def controllerSnapshot (observer : Observer) (env : Environment) (time : Nat) : Word :=
  observer ((prefixWord (fun n => (env n).1) time,
    prefixWord (fun n => (env n).2) time), time)

theorem zero_snapshot_computable (observer : Observer) (hc : Computable observer) :
    Computable (controllerSnapshot observer alwaysAuthorisedZero) := by
  have hp : Primrec fun n : Nat => prefixWord (fun _ => true) n :=
    Primrec.list_map Primrec.list_range (Primrec.const true).to₂
  have hi : Primrec fun n : Nat => prefixWord (fun _ => false) n :=
    Primrec.list_map Primrec.list_range (Primrec.const false).to₂
  exact hc.comp ((hp.pair hi).pair Primrec.id).to_comp

theorem no_supported_zero_input_renewal (observer : Observer) (hc : Computable observer)
    (hm : Committed (controllerSnapshot observer alwaysAuthorisedZero))
    (hs : ∀ t, diagonalTree (controllerSnapshot observer alwaysAuthorisedZero t)) :
    ¬ UnboundedOutput (controllerSnapshot observer alwaysAuthorisedZero) :=
  no_effective_committed_renewal _ (zero_snapshot_computable observer hc) hm hs

/-- The negative statement fixes one computable permitted environment. It does
not exclude success when an unrelated noncomputable input stream supplies advice. -/
theorem no_uniform_supported_renewal (observer : Observer) (hc : Computable observer) :
    ¬ ∀ env : Environment, (∀ n, (env n).1 = true) →
      Committed (controllerSnapshot observer env) ∧
      (∀ t, diagonalTree (controllerSnapshot observer env t)) ∧
      UnboundedOutput (controllerSnapshot observer env) := by
  intro h
  obtain ⟨hm, hs, hu⟩ := h alwaysAuthorisedZero (fun _ => rfl)
  exact no_supported_zero_input_renewal observer hc hm hs hu

def lineageConfiguration (f : Nat → Bool) (inputs : Nat → Bool) (q : State) (n : Nat) : Config :=
  (prefixWord f n, (encoding n (serviceState inputs q n), true))

theorem mathematical_lineage_step (f : Nat → Bool)
    (hf : ∀ n, diagonalTree (prefixWord f n)) (inputs : Nat → Bool) (q : State) (n : Nat) :
    RenewalStep true (f n)
      (execute (lineageConfiguration f inputs q n) (inputs n))
      (lineageConfiguration f inputs q (n + 1)) := by
  refine ⟨rfl, rfl, ?_, ?_⟩
  · change diagonalTree (prefixWord f n ++ [f n])
    rw [← Pruning.prefixWord_succ]
    exact hf (n + 1)
  · simp [lineageConfiguration, migrate, execute, abstractState, serviceState,
      Pruning.prefixWord_succ]

theorem exists_mathematical_contract_lineage (inputs : Nat → Bool) (q : State) :
    ∃ (f : Nat → Bool) (c : Nat → Config), c 0 = initial q ∧
      ∀ n, RenewalStep true (f n) (execute (c n) (inputs n)) (c (n + 1)) := by
  obtain ⟨f, hf⟩ := exists_mathematical_path
  refine ⟨f, lineageConfiguration f inputs q, ?_, mathematical_lineage_step f hf inputs q⟩
  simp [lineageConfiguration, initial, prefixWord, encoding, twist, serviceState]

/-- This effective observer copies the externally supplied service-input prefix. -/
def copyInputObserver : Observer := fun p => p.1.2

theorem copyInputObserver_computable : Computable copyInputObserver :=
  Computable.snd.comp Computable.fst

/-- A noncomputable environment may supply path advice. This positive boundary
control is why the negative theorem is stated on the fixed computable zero input. -/
theorem some_environment_supplies_path_advice :
    ∃ env : Environment, (∀ n, (env n).1 = true) ∧
      Committed (controllerSnapshot copyInputObserver env) ∧
      (∀ t, diagonalTree (controllerSnapshot copyInputObserver env t)) ∧
      UnboundedOutput (controllerSnapshot copyInputObserver env) := by
  obtain ⟨f, hf⟩ := exists_mathematical_path
  refine ⟨fun n => (true, f n), fun _ => rfl, ?_, ?_, ?_⟩
  · exact Pruning.prefixWord_committed f
  · exact hf
  · intro n
    exact ⟨n, by simp [controllerSnapshot, copyInputObserver]⟩

end EffectiveRenewal.Contract
