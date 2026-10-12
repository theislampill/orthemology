import Executable

namespace GuardedTree.Executable
open Saturation
variable {J E R : Type*} [DecidableEq E] [DecidableEq J]
  (G : Grammar J E R) [Fintype R] [Fintype J]

/-- A materialized finite set of exact-key/rational-price rows. -/
abbrev Stored := Finset ((J × Finset E) × ℚ)

def values (T : Stored (J := J) (E := E)) (q : J) (S : Finset E) : Finset ℚ :=
  (T.filter (fun x => x.1 = (q, S))).image Prod.snd

def read (T : Stored (J := J) (E := E)) : Table (J := J) (E := E) :=
  fun q S => minimum (values T q S)

/-- Computes and stores each reachable key exactly once over the finite
judgement/support universe, with no support-inclusion dominance deletion. -/
def materialize (D : Table (J := J) (E := E)) : Stored (J := J) (E := E) :=
  (Finset.univ ×ˢ (grammarSupport G).powerset).biUnion fun k =>
    (D k.1 k.2).toFinset.image (fun c => (k, c))

theorem mem_materialize (D : Table (J := J) (E := E)) (q : J) (S : Finset E) (c : ℚ) :
    ((q, S), c) ∈ materialize G D ↔ S ⊆ grammarSupport G ∧ D q S = some c := by
  simp [materialize]

theorem values_materialize (D : Table (J := J) (E := E)) (q : J) (S : Finset E) :
    values (materialize G D) q S =
      if S ⊆ grammarSupport G then (D q S).toFinset else ∅ := by
  ext c
  simp only [values, Finset.mem_image, Finset.mem_filter]
  constructor
  · rintro ⟨⟨⟨q', S'⟩, c'⟩, ⟨hm, hk⟩, hc⟩
    simp only [Prod.mk.injEq] at hk
    simp only at hc
    rcases hk with ⟨hq, hS⟩
    subst q'
    subst S'
    subst c'
    obtain ⟨hs, hd⟩ := (mem_materialize G D q S c).mp hm
    simp [hs, hd]
  · intro h
    by_cases hs : S ⊆ grammarSupport G
    · have hd : D q S = some c := by simpa [hs] using h
      exact ⟨((q,S),c), ⟨(mem_materialize G D q S c).mpr ⟨hs,hd⟩,rfl⟩,rfl⟩
    · simp [hs] at h

theorem minimum_toFinset (o : Option ℚ) : minimum o.toFinset = o := by
  cases o <;> simp [minimum]

theorem read_materialize (D : Table (J := J) (E := E)) (q : J) (S : Finset E) :
    read (materialize G D) q S =
      if S ⊆ grammarSupport G then D q S else none := by
  simp only [read, values_materialize]
  split_ifs
  · exact minimum_toFinset _
  · rfl

variable [gd : ∀ r s, Decidable (G.guard r s)]

/-- Each step reads the previous finite table, computes candidates, and
materializes a new finite table. It does not retain nested function thunks. -/
def compileStep (T : Stored (J := J) (E := E)) : Stored (J := J) (E := E) :=
  materialize G (step G (read T))

def compileRounds : ℕ → Stored (J := J) (E := E)
  | 0 => ∅
  | h + 1 => compileStep G (compileRounds h)

omit [DecidableEq J] [Fintype J] gd in
/-- Frozen proof semantics show generated tables never use external supports. -/
theorem round_outside (h : ℕ) (q : J) (S : Finset E)
    (hs : ¬ S ⊆ grammarSupport G) : Saturation.round G h q S = none := by
  cases hc : Saturation.round G h q S with
  | none => rfl
  | some c =>
    obtain ⟨t, _, _, _, ht, _⟩ := (round_correct G h).1 q S c hc
    exact False.elim (hs (ht ▸ support_subset_grammarSupport G t))

/-- The executable stored table has exactly the frozen recurrence's full
numeric semantics, including all keys outside the enumerated universe. -/
theorem compile_round_eq (h : ℕ) :
    read (compileRounds G h) = Saturation.round G h := by
  induction h with
  | zero =>
    funext q S
    simp [compileRounds, read, values, minimum, Saturation.round]
  | succ h ih =>
    funext q S
    simp only [compileRounds, compileStep, read_materialize, ih, step_eq]
    change (if S ⊆ grammarSupport G then Saturation.round G (h+1) q S else none) = _
    by_cases hs : S ⊆ grammarSupport G
    · simp [hs]
    · simp [hs, round_outside G (h+1) q S hs]

/-- Row membership itself, not just a minimum-based lookup, is exact. Thus
no second/dearer row can be hidden by the lookup operation. -/
theorem mem_compileRounds (h : ℕ) (q : J) (S : Finset E) (c : ℚ) :
    ((q,S),c) ∈ compileRounds G h ↔ Saturation.round G h q S = some c := by
  cases h with
  | zero => simp [compileRounds, Saturation.round]
  | succ h =>
    simp only [compileRounds, compileStep, mem_materialize, compile_round_eq, step_eq]
    change (S ⊆ grammarSupport G ∧ Saturation.round G (h+1) q S = some c) ↔ _
    constructor
    · exact And.right
    · intro hc
      obtain ⟨t, _, _, _, ht, _⟩ := (round_correct G (h+1)).1 q S c hc
      exact ⟨ht ▸ support_subset_grammarSupport G t, hc⟩

theorem row_unique (h : ℕ) (q : J) (S : Finset E) (c d : ℚ)
    (hc : ((q,S),c) ∈ compileRounds G h) (hd : ((q,S),d) ∈ compileRounds G h) : c = d := by
  exact Option.some.inj (((mem_compileRounds G h q S c).mp hc).symm.trans
    ((mem_compileRounds G h q S d).mp hd))

/-- Fixed bounded run; finite enumeration and guard decisions are explicit
computational inputs. Nonnegative prices are required by its global theorem. -/
def compile : Stored (J := J) (E := E) := compileRounds G (grammarBound G)

theorem compile_correct (hw : ∀ r, 0 ≤ G.price r) :
    GlobalCorrect G (read (compile G)) := by
  rw [compile, compile_round_eq]
  exact round_global G hw _ le_rfl

theorem compile_stable (hw : ∀ r, 0 ≤ G.price r) (k : ℕ) :
    read (compileRounds G (grammarBound G + k)) = read (compile G) := by
  simp only [compile, compile_round_eq]
  exact round_stable G hw k

/-- The finite row sets themselves are stable, not merely their read function. -/
theorem compile_rows_stable (hw : ∀ r, 0 ≤ G.price r) (k : ℕ) :
    compileRounds G (grammarBound G + k) = compile G := by
  ext ⟨⟨q,S⟩,c⟩
  simp only [compile, mem_compileRounds, round_stable G hw k]

/-- Full finite-table equality is an executable stopping test whose result
transfers to unrestricted correctness. Key-only equality is not used. -/
theorem full_table_stopping (hw : ∀ r, 0 ≤ G.price r) (h : ℕ)
    (heq : compileRounds G (h+1) = compileRounds G h) :
    GlobalCorrect G (read (compileRounds G h)) := by
  rw [compile_round_eq]
  apply early_stopping_global G hw h
  have hr := congrArg read heq
  simpa only [compile_round_eq] using hr

#print axioms mem_compileRounds
#print axioms row_unique
#print axioms full_table_stopping
#print axioms compile_round_eq
#print axioms compile_correct
#print axioms compile_stable
end GuardedTree.Executable
