import PhaseSourceFixtures
import UniformComputabilityMachine

/-! Numeric parser and retained explicit-stack execution for callable arity-k
components. This separate API does not change the retained binary observer's
wrong-arity convention and never converts rejection/fuel failure to zero. -/
namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram
open P02.Codec P02.Codec.UniformComputability

def inputRegs {k : ℕ} (args : Fin k → ℕ) : RegFile := List.ofFn (fun i => (i.val,args i))

theorem readRegs_missing (rs : RegFile) (r : ℕ) (h : r ∉ rs.map Prod.fst) : readRegs rs r = 0 := by
  induction rs with
  | nil => rfl
  | cons z rs ih =>
      have hn : r ≠ z.1 := by intro he; apply h; simp [he]
      have ht : r ∉ rs.map Prod.fst := fun hm => h (by simp [hm])
      simpa [readRegs,hn] using ih ht

theorem readRegs_member (rs : RegFile) (r v : ℕ) (hn : (rs.map Prod.fst).Nodup) (hm : (r,v) ∈ rs) :
    readRegs rs r = v := by
  induction rs with
  | nil => simp at hm
  | cons z rs ih =>
      rcases List.mem_cons.mp hm with he | ht
      · subst z
        simp [readRegs]
      · have hn' := List.nodup_cons.mp hn
        have hr : r ≠ z.1 := by
          intro he
          apply hn'.1
          exact he ▸ List.mem_map.mpr ⟨(r,v),ht,rfl⟩
        simpa [readRegs,hr] using ih hn'.2 ht

theorem readRegs_inputs {k : ℕ} (args : Fin k → ℕ) : readRegs (inputRegs args) = P02A2.LoopPrimrec.extend args := by
  funext r
  have hn : ((inputRegs args).map Prod.fst).Nodup := by
    rw [inputRegs,List.map_ofFn]
    exact List.nodup_ofFn.mpr (fun i j h => Fin.ext h)
  by_cases hr : r < k
  · simp only [P02A2.LoopPrimrec.extend,hr,↓reduceDIte]
    exact readRegs_member _ _ _ hn (List.mem_ofFn.mpr ⟨⟨r,hr⟩,rfl⟩)
  · simp only [P02A2.LoopPrimrec.extend,hr,↓reduceDIte]
    apply readRegs_missing
    intro hm
    rcases List.mem_map.mp hm with ⟨z,hz,he⟩
    rcases List.mem_ofFn.mp hz with ⟨i,hi⟩
    subst z
    have hi' := i.isLt
    simp only at he
    omega

def callFuel {k : ℕ} (fuel index : ℕ) (args : Fin k → ℕ) : Option ℕ :=
  match decodeIndex index with
  | none => none
  | some p => if p.arity = k then
      (runFuel fuel [.stmt p.body] (inputRegs args)).map (fun rs => readRegs rs p.output)
    else none

/-- The actual parser/stack engine produces the callable source value with
sufficient fuel. No arbitrary timeout fallback is introduced. -/
theorem callFuel_complete {k : ℕ} (p : Program k) (args : Fin k → ℕ) :
    ∃ fuel, callFuel fuel (programIndex (pack p)) args = some (denote p args) := by
  obtain ⟨fuel,hf⟩ := runFuel_complete p.body (inputRegs args)
  refine ⟨fuel,?_⟩
  simp only [callFuel,decodeIndex_programIndex,pack,↓reduceIte,hf,Option.map_some]
  change some (readRegs (execRegs p.body (inputRegs args)) p.output) = some (denote p args)
  rw [execRegs_correct,readRegs_inputs]
  rfl

theorem callFuel_sound {k : ℕ} (p : Program k) (args : Fin k → ℕ) (fuel value : ℕ)
    (h : callFuel fuel (programIndex (pack p)) args = some value) : value = denote p args := by
  simp only [callFuel,decodeIndex_programIndex,pack,↓reduceIte] at h
  obtain ⟨rs,hf,hv⟩ := Option.map_eq_some_iff.mp h
  have hs := runFuel_sound fuel p.body (inputRegs args) rs hf
  rw [readRegs_inputs] at hs
  rw [← hv,hs]
  rfl

/-- A full literal arity-six phase update on the actual decoded stack engine. -/
theorem actual_phase_update (B C : Finset Bool) (y : Bool) (m : HiddenParity.Sufficiency.PhaseMemory Bool Bool) (reject : Bool) :
    ∃ fuel, callFuel fuel (programIndex (pack phaseProgram)) (args B C y m reject) =
      some (HiddenParity.Sufficiency.advanceMemory B C y m reject).index := by
  obtain ⟨fuel,hf⟩ := callFuel_complete phaseProgram (args B C y m reject)
  exact ⟨fuel,by simpa only [phase_source_exact] using hf⟩

/-- The complete actual empirical guard, including exact tolerance equality. -/
theorem actual_fixture_empirical (θ : Bool) (k : ℕ) (h : Orthemology.Tranche2.PolicyEmbedding.History (Bool × Bool) Bool) :
    ∃ fuel, callFuel fuel (programIndex (pack (Fixture.empiricalFixture θ))) (statisticInputs k h) =
      some (bitNat (HiddenParity.Sufficiency.empiricalReject Controller.Fixture.kernel (1/6) θ k h)) := by
  obtain ⟨fuel,hf⟩ := callFuel_complete (Fixture.empiricalFixture θ) (statisticInputs k h)
  exact ⟨fuel,by simpa only [Fixture.fixture_empirical_exact] using hf⟩

end Orthemology.RuntimeBridge.PhaseUpdate
