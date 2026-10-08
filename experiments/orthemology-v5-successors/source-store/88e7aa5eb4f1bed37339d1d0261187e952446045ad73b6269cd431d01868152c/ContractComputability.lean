import RenewalContract

namespace EffectiveRenewal.Contract

/-- Primitive-recursive operational data flow, supplementing the semantic
commutation proofs. Inputs here are finite supplied data; no algorithm for
producing an arbitrary external infinite stream is presupposed. -/
theorem delayStep_primrec : Primrec₂ delayStep :=
  (Primrec.snd.comp Primrec.fst).pair Primrec.snd

theorem twist_primrec : Primrec₂ twist :=
  (Primrec.cond Primrec.fst
    ((Primrec.not.comp (Primrec.fst.comp Primrec.snd)).pair
      (Primrec.not.comp (Primrec.snd.comp Primrec.snd))) Primrec.snd).of_eq
    fun p => by cases p.1 <;> rfl

theorem encoding_primrec : Primrec₂ encoding :=
  twist_primrec.comp (Primrec.nat_bodd.comp Primrec.fst) Primrec.snd

theorem abstractState_primrec : Primrec abstractState :=
  encoding_primrec.comp (Primrec.list_length.comp Primrec.fst) (Primrec.fst.comp Primrec.snd)

theorem initial_primrec : Primrec initial :=
  (Primrec.const ([] : Word)).pair (Primrec.id.pair (Primrec.const true))

theorem execute_primrec : Primrec₂ execute := by
  have hist : Primrec fun p : Config × Bool => p.1.1 := Primrec.fst.comp Primrec.fst
  have state : Primrec fun p : Config × Bool => delayStep (abstractState p.1) p.2 :=
    delayStep_primrec.comp (abstractState_primrec.comp Primrec.fst) Primrec.snd
  exact hist.pair ((encoding_primrec.comp (Primrec.list_length.comp hist) state).pair
    (Primrec.snd.comp (Primrec.snd.comp Primrec.fst)))

theorem migrate_primrec : Primrec₂ migrate := by
  have hist : Primrec fun p : Config × Bool => p.1.1 := Primrec.fst.comp Primrec.fst
  exact (Primrec.list_concat.comp hist Primrec.snd).pair
    ((encoding_primrec.comp (Primrec.succ.comp (Primrec.list_length.comp hist))
      (abstractState_primrec.comp Primrec.fst)).pair (Primrec.const true))

theorem terminate_primrec : Primrec terminate :=
  Primrec.fst.pair ((Primrec.fst.comp Primrec.snd).pair (Primrec.const false))

theorem request_primrec : Primrec fun p : Bool × (Bool × Config) => request p.1 p.2.1 p.2.2 := by
  have pc : Primrec fun p : Bool × (Bool × Config) => p.2.2 := Primrec.snd.comp Primrec.snd
  have pb : Primrec fun p : Bool × (Bool × Config) => p.2.1 := Primrec.fst.comp Primrec.snd
  have ht : Primrec fun p : Bool × (Bool × Config) => treeCheck (p.2.2.1 ++ [p.2.1]) :=
    treeCheck_primrec.comp (Primrec.list_concat.comp (Primrec.fst.comp pc) pb)
  exact (Primrec.cond (Primrec.snd.comp (Primrec.snd.comp pc))
    (Primrec.cond Primrec.fst (Primrec.cond ht (migrate_primrec.comp pc pb) pc)
      (terminate_primrec.comp pc)) pc).of_eq fun p => by simp [request, Bool.cond_eq_ite]

def finiteProcess (n : Nat) (inputs : Word) (q : State) : Config :=
  (finitePlan n).foldl
    (fun c b => request true b (execute c (inputs.getD c.1.length false))) (initial q)

theorem finiteProcess_primrec : Primrec fun p : Nat × (Word × State) =>
    finiteProcess p.1 p.2.1 p.2.2 := by
  have hc : Primrec fun p : (Nat × (Word × State)) × (Config × Bool) => p.2.1 :=
    Primrec.fst.comp Primrec.snd
  have hb : Primrec fun p : (Nat × (Word × State)) × (Config × Bool) => p.2.2 :=
    Primrec.snd.comp Primrec.snd
  have inputs : Primrec fun p : (Nat × (Word × State)) × (Config × Bool) => p.1.2.1 :=
    Primrec.fst.comp (Primrec.snd.comp Primrec.fst)
  have hi : Primrec fun p : (Nat × (Word × State)) × (Config × Bool) =>
      p.1.2.1.getD p.2.1.1.length false :=
    (Primrec.list_getD false).comp inputs (Primrec.list_length.comp (Primrec.fst.comp hc))
  exact Primrec.list_foldl (finitePlan_primrec.comp Primrec.fst)
    (initial_primrec.comp (Primrec.snd.comp Primrec.snd))
    (request_primrec.comp ((Primrec.const true).pair (hb.pair (execute_primrec.comp hc hi)))).to₂

theorem finiteProcess_prefix_correct (n : Nat) (inputs : Word) (q : State)
    (j : Nat) (hj : j ≤ n) :
    ((finitePlan n).take j).foldl
      (fun c b => request true b (execute c (inputs.getD c.1.length false))) (initial q) =
    configurationAt (finitePlan n) (fun k => inputs.getD k false) q j := by
  induction j with
  | zero => simp [configurationAt, initial, encoding, twist, serviceState]
  | succ j ih =>
    have hjn : j < n := hj
    have hjr : j < (finitePlan n).length := by simpa using hjn
    rw [List.take_succ_eq_append_getElem hjr, List.foldl_append]
    simp only [List.foldl_cons, List.foldl_nil]
    rw [ih (by omega)]
    have hg : (configurationAt (finitePlan n) (fun k => inputs.getD k false) q j).1.length = j := by
      simp [configurationAt, Nat.min_eq_left (Nat.le_of_lt hjn)]
    rw [hg]
    exact renewal_step_executes (finite_plan_round_correct n (fun k => inputs.getD k false) q hjn).1

theorem finiteProcess_correct (n : Nat) (inputs : Word) (q : State) :
    finiteProcess n inputs q =
      configurationAt (finitePlan n) (fun k => inputs.getD k false) q n := by
  have htake : (finitePlan n).take n = finitePlan n := by
    conv_lhs => arg 2; rw [← length_finitePlan n]
    simp
  simpa only [htake, finiteProcess] using finiteProcess_prefix_correct n inputs q n (Nat.le_refl n)

theorem finiteProcess_run (n : Nat) (inputs : Word) (q : State) :
    Run (initial q) (serviceInputs (fun k => inputs.getD k false) 0 n)
      (finiteProcess n inputs q) := by
  rw [finiteProcess_correct]
  exact finite_plan_whole_run _ _ _

theorem finiteProcess_length (n : Nat) (inputs : Word) (q : State) :
    (finiteProcess n inputs q).1.length = n := by
  simp [finiteProcess_correct, configurationAt]

end EffectiveRenewal.Contract
