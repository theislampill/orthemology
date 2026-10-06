import LookaheadAdmission

namespace EffectiveRenewal.Lookahead

def horizonCandidates (h : Word → Nat) (n : Nat) : Option Word :=
  boundedSelect (lookaheadCheck h) (binaryWords n)

/-- The fallback is executable but proved unreachable for every finite demand
function. No noncomputable path determines this finite search's output. -/
def lookaheadPlan (h : Word → Nat) (n : Nat) : Word := (horizonCandidates h n).getD []

theorem horizonCandidates_computable (h : Word → Nat) (hc : Computable h) :
    Computable (horizonCandidates h) :=
  (boundedSelect_computable (fun _ : Nat => lookaheadCheck h)
    ((lookaheadCheck_computable h hc).comp Computable.snd)).comp
      (Computable.id.pair binaryWords_primrec.to_comp)

theorem lookaheadPlan_computable (h : Word → Nat) (hc : Computable h) :
    Computable (lookaheadPlan h) :=
  Computable.option_getD (horizonCandidates_computable h hc) (Computable.const [])

theorem horizonCandidates_nonempty (h : Word → Nat) (n : Nat) :
    (horizonCandidates h n).isSome = true := by
  obtain ⟨f, hf⟩ := lookahead_mathematical_path h
  apply (boundedSelect_spec (lookaheadCheck h) (binaryWords n)).2.mpr
  exact ⟨prefixWord f n, (mem_binaryWords_iff _ _).mpr (length_prefixWord _ _), hf n⟩

theorem lookaheadPlan_spec (h : Word → Nat) (n : Nat) :
    (lookaheadPlan h n).length = n ∧ lookaheadTree h (lookaheadPlan h n) := by
  obtain ⟨w, hw⟩ := Option.isSome_iff_exists.mp (horizonCandidates_nonempty h n)
  have hs := (boundedSelect_spec (lookaheadCheck h) (binaryWords n)).1 w hw
  have hp : lookaheadPlan h n = w := by simp only [lookaheadPlan, hw, Option.getD_some]
  rw [hp]
  exact ⟨(mem_binaryWords_iff _ _).mp hs.1, hs.2⟩

theorem lookaheadPlan_prefixes (h : Word → Nat) (n k : Nat) :
    lookaheadTree h ((lookaheadPlan h n).take k) :=
  lookahead_prefix_closed h (List.take_prefix _ _) (lookaheadPlan_spec h n).2

theorem lookaheadPlan_base_admitted (h : Word → Nat) (n : Nat) :
    diagonalTree (lookaheadPlan h n) := lookahead_subset h _ (lookaheadPlan_spec h n).2

theorem supplement_total_of_lookahead (h : Word → Nat) (s : Word)
    (hs : lookaheadTree h s) : ∃ w, supplement h s = some w ∧ BaseWitness h s w := by
  have hl := ((lookaheadTree_iff h s).mp hs).2 s.length (Nat.le_refl _)
  have hsome : (supplement h s).isSome = true := by
    simpa [takeWord_eq_take, lookCheck] using hl
  obtain ⟨w, hw⟩ := Option.isSome_iff_exists.mp hsome
  exact ⟨w, hw, supplement_sound h s w hw⟩

theorem no_computable_lookahead_path (h : Word → Nat) (f : Nat → Bool) (hc : Computable f) :
    ¬ ∀ n, lookaheadTree h (prefixWord f n) := by
  intro hp
  exact no_computable_path f hc ((lookahead_path_iff h f).mp hp)

theorem no_effective_lookahead_commitment (h : Word → Nat) (snap : Nat → Word)
    (hc : Computable snap) (hm : Committed snap) (hs : ∀ n, lookaheadTree h (snap n)) :
    ¬ UnboundedOutput snap :=
  no_effective_committed_renewal snap hc hm (fun n => lookahead_subset h _ (hs n))

theorem no_supported_zero_lookahead (h : Word → Nat) (observer : Contract.Observer)
    (hc : Computable observer)
    (hm : Committed (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero))
    (hs : ∀ n, lookaheadTree h (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero n)) :
    ¬ UnboundedOutput (Contract.controllerSnapshot observer Contract.alwaysAuthorisedZero) :=
  Contract.no_supported_zero_input_renewal observer hc hm (fun n => lookahead_subset h _ (hs n))

theorem lookahead_computably_decidable (h : Word → Nat) (hc : Computable h) :
    Pruning.ComputablyDecidable (lookaheadTree h) :=
  ⟨lookaheadCheck h, lookaheadCheck_computable h hc, fun _ => Iff.rfl⟩

/-- Even after every prescribed finite onward check, the strengthened tree is
not a recursively closed viable region. Supplementary witnesses remain in T. -/
theorem lookahead_not_rooted_pruned (h : Word → Nat) (hc : Computable h) :
    ¬ Pruning.RootedPruned (lookaheadTree h) := by
  intro hp
  obtain ⟨f, hf, hpath⟩ := (Pruning.computable_path_iff_decidable_pruned (lookaheadTree h)).mpr
    ⟨lookaheadTree h, fun _ hs => hs, hp, lookahead_computably_decidable h hc⟩
  exact no_computable_lookahead_path h f hf hpath

theorem admitted_base_capacity_can_lack_lookahead_successor (h : Word → Nat) (hc : Computable h) :
    ∃ s, lookaheadTree h s ∧
      (∃ w, supplement h s = some w ∧ BaseWitness h s w) ∧
      ∀ b : Bool, ¬ lookaheadTree h (s ++ [b]) := by
  classical
  by_contra hnot
  have hprune : ∀ s, lookaheadTree h s → ∃ b : Bool, lookaheadTree h (s ++ [b]) := by
    intro s hs
    by_contra hn
    have hchildren : ∀ b : Bool, ¬ lookaheadTree h (s ++ [b]) := by simpa using hn
    exact hnot ⟨s, hs, supplement_total_of_lookahead h s hs, hchildren⟩
  exact lookahead_not_rooted_pruned h hc
    ⟨lookahead_root h, lookahead_prefix_closed h, hprune⟩

/-- Any finitely admitted base route has the already specified operational lift. -/
theorem admitted_route_run_from (route : Word) (hr : diagonalTree route)
    (inputs : Nat → Bool) (q : Contract.State) (j k : Nat) (hjk : j + k ≤ route.length) :
    Contract.Run (Contract.configurationAt route inputs q j) (Contract.serviceInputs inputs j k)
      (Contract.configurationAt route inputs q (j + k)) := by
  induction k generalizing j with
  | zero => simpa [Contract.serviceInputs] using Contract.Run.nil (Contract.configurationAt route inputs q j)
  | succ k ih =>
    have hj : j < route.length := by omega
    have edge : Contract.RenewalStep true route[j]
        (Contract.execute (Contract.configurationAt route inputs q j) (inputs j))
        (Contract.configurationAt route inputs q (j + 1)) := by
      refine ⟨rfl, rfl, ?_, Contract.configurationAt_next route inputs q hj⟩
      change diagonalTree (route.take j ++ [route[j]])
      rw [← List.take_succ_eq_append_getElem hj]
      exact diagonalTree_prefix_closed (List.take_prefix _ _) hr
    have tail := ih (j + 1) (by omega)
    have run := Contract.Run.service (inputs j) rfl (Contract.Run.renewal edge tail)
    simpa [Contract.serviceInputs, Nat.add_assoc, Nat.add_left_comm, Nat.add_comm] using run

theorem lookahead_plan_contract_run (h : Word → Nat) (n : Nat)
    (inputs : Nat → Bool) (q : Contract.State) :
    Contract.Run (Contract.initial q) (Contract.serviceInputs inputs 0 n)
      (Contract.configurationAt (lookaheadPlan h n) inputs q n) := by
  have hr := admitted_route_run_from (lookaheadPlan h n) (lookaheadPlan_base_admitted h n)
    inputs q 0 n (by simp [(lookaheadPlan_spec h n).1])
  simpa [Contract.configurationAt, Contract.initial, Contract.serviceState, Contract.encoding, Contract.twist] using hr

/-- Central extension theorem. The computability premise is retained exactly;
there is no uniform bound or primitive-recursive restriction on h. -/
theorem finite_lookahead_boundary (h : Word → Nat) (hc : Computable h) :
    Computable (lookaheadCheck h) ∧ lookaheadTree h [] ∧ PrefixClosed (lookaheadTree h) ∧
    (∀ f : Nat → Bool, (∀ n, lookaheadTree h (prefixWord f n)) ↔
      ∀ n, diagonalTree (prefixWord f n)) ∧
    Computable (lookaheadPlan h) ∧
    (∀ n, (lookaheadPlan h n).length = n ∧ lookaheadTree h (lookaheadPlan h n)) ∧
    ¬ Pruning.RootedPruned (lookaheadTree h) :=
  ⟨lookaheadCheck_computable h hc, lookahead_root h, lookahead_prefix_closed h,
    lookahead_path_iff h, lookaheadPlan_computable h hc, lookaheadPlan_spec h,
    lookahead_not_rooted_pruned h hc⟩

theorem zero_lookahead_iff_base (s : Word) :
    lookaheadTree (fun _ => 0) s ↔ diagonalTree s := by
  constructor
  · exact lookahead_subset _ s
  · intro hs
    refine (lookaheadTree_iff _ s).mpr ⟨hs, ?_⟩
    intro k _
    apply (lookCheck_zero (fun _ => 0) (takeWord s k) rfl).mpr
    rw [takeWord_eq_take]
    exact diagonalTree_prefix_closed (List.take_prefix _ _) hs

/-- The h=1 instance supplies a genuine base-T next step at each admitted
handoff, but cannot promise that next step is itself L_1-admitted. -/
theorem one_step_recursive_witness_failure :
    ¬ ∀ s, lookaheadTree (fun _ => 1) s →
      ∃ w, BaseWitness (fun _ => 1) s w ∧ lookaheadTree (fun _ => 1) w := by
  intro h
  apply lookahead_not_rooted_pruned (fun _ => 1) (Computable.const 1)
  refine ⟨lookahead_root _, lookahead_prefix_closed _, ?_⟩
  intro s hs
  obtain ⟨w, ⟨⟨tail, he⟩, hl, _⟩, hw⟩ := h s hs
  change w.length = s.length + 1 at hl
  have hlen : tail.length = 1 := by
    have heLen := congrArg List.length he
    simp only [List.length_append] at heLen
    omega
  obtain ⟨b, hb⟩ := List.length_eq_one_iff.mp hlen
  refine ⟨b, ?_⟩
  have hs : s ++ [b] = w := by simpa only [hb] using he
  rw [hs]
  exact hw

theorem baseWitness_one_immediate {s w : Word} (hw : BaseWitness (fun _ => 1) s w) :
    ∃ b : Bool, w = s ++ [b] := by
  obtain ⟨⟨tail, he⟩, hl, _⟩ := hw
  change w.length = s.length + 1 at hl
  have hlen : tail.length = 1 := by
    have heLen := congrArg List.length he
    simp only [List.length_append] at heLen
    omega
  obtain ⟨b, hb⟩ := List.length_eq_one_iff.mp hlen
  exact ⟨b, by simpa only [hb] using he.symm⟩

/-- The final-prefix check genuinely strengthens base admission: some admitted
base histories have no next base step and therefore fail h=1 at their endpoint. -/
theorem final_prefix_check_is_substantive :
    ∃ s, diagonalTree s ∧ ¬ lookaheadTree (fun _ => 1) s := by
  classical
  by_contra hn
  have hall : ∀ s, diagonalTree s → lookaheadTree (fun _ => 1) s := by simpa using hn
  apply Pruning.diagonal_not_rooted_pruned
  refine ⟨diagonalTree_empty, fun hp ht => diagonalTree_prefix_closed hp ht, ?_⟩
  intro s hs
  obtain ⟨w, _, hw⟩ := supplement_total_of_lookahead (fun _ => 1) s (hall s hs)
  obtain ⟨b, hb⟩ := baseWitness_one_immediate hw
  exact ⟨b, hb ▸ hw.2.2⟩

end EffectiveRenewal.Lookahead
