import PRDerivation

/-! Extensional coverage of Mathlib's PR class by the explicit derivation
presentation. The structural compiler is separately executable on Code.
This theorem does not claim an extractor from erased Prop proofs or a numeric
code-index converter. -/
namespace P02A2.PRCoverage
open P02A2.PRDerivation P02A2.PRProgram
open List.Vector

theorem vector_get_cons (a : ℕ) {n : ℕ} (v : List.Vector ℕ n) :
    (a ::ᵥ v).get = Fin.cons a v.get := by
  funext i
  exact Fin.cases (by simp) (fun j => by simp) i

theorem vector_get_tail {n : ℕ} (v : List.Vector ℕ (n+1)) :
    (fun i => v.get i.succ) = v.tail.get := by
  funext i
  exact (List.Vector.get_tail_succ v i).symm

theorem exists_code_of_primrec' {n : ℕ} {f : List.Vector ℕ n → ℕ} (hf : Nat.Primrec' f) :
    ∃ d : Code n, ∀ args : List.Vector ℕ n, meaning d args.get = f args := by
  classical
  induction hf with
  | zero => exact ⟨.zero 0, fun _ => rfl⟩
  | succ =>
      refine ⟨.successor, ?_⟩
      intro v
      simp [meaning, List.Vector.get_zero, Nat.succ_eq_add_one]
  | get i => exact ⟨.projection i, fun _ => rfl⟩
  | @comp m n f gs hf hgs ihf ihgs =>
      rcases ihf with ⟨df,hdf⟩
      choose ds hds using ihgs
      refine ⟨.compose df ds, ?_⟩
      intro v
      change meaning df (fun i => meaning (ds i) v.get) = _
      have ha : (fun i => meaning (ds i) v.get) = (List.Vector.ofFn (fun i => gs i v)).get := by
        funext i
        simp [hds i v]
      rw [ha, hdf]
  | @prec n f g hf hg ihf ihg =>
      rcases ihf with ⟨df,hdf⟩
      rcases ihg with ⟨dg,hdg⟩
      refine ⟨.prec df dg, ?_⟩
      intro v
      simp only [meaning, List.Vector.get_zero]
      have hb : meaning df (fun i => v.get i.succ) = f v.tail :=
        (congrArg (meaning df) (vector_get_tail v)).trans (hdf v.tail)
      have hs : (fun j value => meaning dg (Fin.cons j (Fin.cons value (fun i => v.get i.succ)))) =
          (fun j value => g (j ::ᵥ value ::ᵥ v.tail)) := by
        funext j value
        have ha : Fin.cons j (Fin.cons value (fun i => v.get i.succ)) =
            (j ::ᵥ value ::ᵥ v.tail).get := by
          calc
            _ = Fin.cons j (Fin.cons value v.tail.get) :=
              congrArg (fun q : Fin n → ℕ => (Fin.cons j (Fin.cons value q) : Fin (n+2) → ℕ)) (vector_get_tail v)
            _ = _ := by rw [vector_get_cons, vector_get_cons]
        exact (congrArg (meaning dg) ha).trans (hdg _)
      exact congrArg₂ (fun (b : ℕ) (step : ℕ → ℕ → ℕ) => Nat.rec (motive := fun _ => ℕ) b step v.head) hb hs

theorem exists_code_of_primrec {n : ℕ} (f : (Fin n → ℕ) → ℕ) (hf : Primrec f) :
    ∃ d : Code n, ∀ args, meaning d args = f args := by
  have hp : Primrec (fun v : List.Vector ℕ n => f v.get) := hf.comp Primrec.vector_get'
  obtain ⟨d,hd⟩ := exists_code_of_primrec' (Nat.Primrec'.of_prim hp)
  refine ⟨d, fun args => ?_⟩
  have he : (List.Vector.ofFn args).get = args := by funext i; simp
  simpa only [he] using hd (List.Vector.ofFn args)

theorem exists_program_of_primrec {n : ℕ} (f : (Fin n → ℕ) → ℕ) (hf : Primrec f) :
    ∃ p : Program n, ∀ args, denote p args = f args := by
  obtain ⟨d,hd⟩ := exists_code_of_primrec f hf
  exact ⟨compile d, fun args => (compile_correct d args).trans (hd args)⟩

end P02A2.PRCoverage
