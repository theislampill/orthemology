import Enumeration

namespace GuardedTree.Witness
open Tree
variable {J E R : Type*} [DecidableEq J] [DecidableEq E]
  (G : Grammar J E R) [gd : ∀ r s, Decidable (G.guard r s)]

/-- Structural checking computes the original grammar validity proposition. -/
def validDecidable : (t : Tree G) → Decidable (Valid G t)
  | .node r child => by
    letI : ∀ i, Decidable (Valid G (child i)) := fun i => validDecidable (child i)
    exact inferInstanceAs (Decidable
      ((∀ i, Valid G (child i) ∧ judgement G (child i) = G.premise r i) ∧
        G.guard r (fun i => support G (child i))))

instance treeValidDecidable (t : Tree G) : Decidable (Valid G t) := validDecidable G t

/-- Standalone executable certificate verifier; recomputes all tree metadata. -/
def accept (q : J) (S : Finset E) (c : ℚ) (t : Tree G) : Bool :=
  decide (Valid G t ∧ judgement G t = q ∧ support G t = S ∧ cost G t ≤ c)

theorem accept_iff (q : J) (S : Finset E) (c : ℚ) (t : Tree G) :
    accept G q S c t = true ↔
      Valid G t ∧ judgement G t = q ∧ support G t = S ∧ cost G t = c := by
  simp only [accept, decide_eq_true_eq]

/-- Deterministic first-match selection. Equal-cost ties use the rule-list order. -/
def search (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E) (c : ℚ) : Option (Tree G) :=
  (trees G rs h).find? (accept G q S c)

theorem search_sound (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E)
    (c : ℚ) (t : Tree G) (ht : search G rs h q S c = some t) :
    Bounded G h t ∧ Valid G t ∧ judgement G t = q ∧ support G t = S ∧ cost G t = c :=
  ⟨(mem_trees G rs h t).mp (List.mem_of_find?_eq_some ht),
    (accept_iff G q S c t).mp (List.find?_some ht)⟩

theorem search_complete (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E) (c : ℚ)
    (hex : ∃ t : Tree G, Bounded G h t ∧ Valid G t ∧
      judgement G t = q ∧ support G t = S ∧ cost G t = c) :
    ∃ t, search G rs h q S c = some t := by
  obtain ⟨t, hb, ht⟩ := hex
  have hi : (search G rs h q S c).isSome := List.find?_isSome.mpr
    ⟨t, (mem_trees G rs h t).mpr hb, (accept_iff G q S c t).mpr ht⟩
  cases he : search G rs h q S c with
  | none => simp [he] at hi
  | some t => exact ⟨t, rfl⟩

variable [Fintype R] [Fintype J]

/-- First compute the separate dynamic-table minimum, then exhaustively search
bounded finite trees at that exact cost. This is not efficient reconstruction. -/
def extractRound (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E) : Option (Tree G) :=
  (Executable.read (Executable.compileRounds G h) q S).bind (search G rs h q S)

theorem extract_sound (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E)
    (t : Tree G) (ht : extractRound G rs h q S = some t) :
    Bounded G h t ∧ Valid G t ∧ judgement G t = q ∧ support G t = S ∧
      Executable.read (Executable.compileRounds G h) q S = some (cost G t) := by
  unfold extractRound at ht
  cases hc : Executable.read (Executable.compileRounds G h) q S with
  | none => simp [hc] at ht
  | some c =>
    have hs : search G rs h q S c = some t := by simpa [hc] using ht
    obtain ⟨hb, hv, hq, hS, hp⟩ := search_sound G rs h q S c t hs
    exact ⟨hb, hv, hq, hS, by simp only [hp]⟩

theorem extract_complete (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E)
    (c : ℚ) (hc : Executable.read (Executable.compileRounds G h) q S = some c) :
    ∃ t, extractRound G rs h q S = some t ∧ cost G t = c := by
  have hr : Saturation.round G h q S = some c := by
    simpa only [Executable.compile_round_eq] using hc
  obtain ⟨t, ht⟩ := search_complete G rs h q S c ((Saturation.round_correct G h).1 q S c hr)
  exact ⟨t, by simp [extractRound, hc, ht], (search_sound G rs h q S c t ht).2.2.2.2⟩

/-- Exact correspondence, including unreachable keys; no existential tree is
chosen by the runtime implementation. -/
theorem extract_cost_eq (rs : RuleList R) (h : ℕ) (q : J) (S : Finset E) :
    (extractRound G rs h q S).map (cost G) =
      Executable.read (Executable.compileRounds G h) q S := by
  cases hc : Executable.read (Executable.compileRounds G h) q S with
  | none => simp [extractRound, hc]
  | some c =>
    obtain ⟨t, ht, hp⟩ := extract_complete G rs h q S c hc
    simp [ht, hp]

/-- Global reference extractor. Nonnegative prices are the correctness theorem's
hypothesis, not an implicit assumption of the bounded implementation. -/
def extract (rs : RuleList R) (q : J) (S : Finset E) : Option (Tree G) :=
  extractRound G rs (grammarBound G) q S

/-- Global output projection is exactly the existing compiled numeric table. -/
theorem extract_global_cost_eq (rs : RuleList R) (q : J) (S : Finset E) :
    (extract G rs q S).map (cost G) = Executable.read (Executable.compile G) q S :=
  extract_cost_eq G rs (grammarBound G) q S

theorem extract_global (rs : RuleList R) (hw : ∀ r, 0 ≤ G.price r)
    (q : J) (S : Finset E) (t : Tree G) (ht : extract G rs q S = some t) :
    Valid G t ∧ judgement G t = q ∧ support G t = S ∧
      (∀ u : Tree G, Valid G u → judgement G u = q → support G u = S →
        cost G t ≤ cost G u) := by
  obtain ⟨_, hv, hq, hs, hc⟩ := extract_sound G rs (grammarBound G) q S t ht
  refine ⟨hv, hq, hs, ?_⟩
  intro u hu huq hus
  obtain ⟨c, huC, hle⟩ := (Executable.compile_correct G hw).2 u hu
  change Executable.read (Executable.compileRounds G (grammarBound G)) _ _ = some c at huC
  rw [huq, hus, hc] at huC
  exact Option.some.inj huC ▸ hle

theorem extract_none_iff (rs : RuleList R) (hw : ∀ r, 0 ≤ G.price r)
    (q : J) (S : Finset E) : extract G rs q S = none ↔
      ¬ ∃ t : Tree G, Valid G t ∧ judgement G t = q ∧ support G t = S := by
  constructor
  · intro hn ⟨t, hv, hq, hs⟩
    obtain ⟨c, hc, _⟩ := (Executable.compile_correct G hw).2 t hv
    rw [hq, hs] at hc
    obtain ⟨u, hu, _⟩ := extract_complete G rs (grammarBound G) q S c hc
    change extract G rs q S = some u at hu
    rw [hn] at hu
    contradiction
  · intro hn
    cases ht : extract G rs q S with
    | none => rfl
    | some t =>
      obtain ⟨hv, hq, hs, _⟩ := extract_global G rs hw q S t ht
      exact False.elim (hn ⟨t, hv, hq, hs⟩)

#print axioms accept_iff
#print axioms extract_cost_eq
#print axioms extract_global_cost_eq
#print axioms extract_global
#print axioms extract_none_iff
end GuardedTree.Witness
