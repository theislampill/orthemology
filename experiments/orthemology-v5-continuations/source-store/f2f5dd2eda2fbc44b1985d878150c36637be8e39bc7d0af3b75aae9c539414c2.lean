import PrefixPrimrec
import CodecParameter

/-! Cross-lane interface: the actual fair-source tagged-prefix family is
realised by one fixed ternary LOOP program and its literal-specialized numeric
codes. Fixed-family PR coverage is existential; parameterIndex is concrete.
Its numeric Primrec theorem is a separate obligation. -/
namespace P02A2.Pi3Program
open P02A2.ObserverCore P02A2.PRProgram P02A2.Q8Measure P02.Codec

variable (R : ℕ → ℕ → ℕ → ℕ → Prop) [∀ a i, DecidableRel (R a i)]

def family (args : Fin 3 → ℕ) : ℕ := OrthemologyTagged.pi3PrefixValue R (args 0) (args 1) (args 2)

theorem family_primrec
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) : Primrec (family R) := by
  have h0 : Primrec (fun args : Fin 3 → ℕ => args 0) := Primrec.fin_app.comp Primrec.id (Primrec.const 0)
  have h1 : Primrec (fun args : Fin 3 → ℕ => args 1) := Primrec.fin_app.comp Primrec.id (Primrec.const 1)
  have h2 : Primrec (fun args : Fin 3 → ℕ => args 2) := Primrec.fin_app.comp Primrec.id (Primrec.const 2)
  exact (OrthemologyTagged.pi3PrefixValue_primrec R hR).comp (h0.pair h1) h2

theorem exists_fixed_program
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) :
    ∃ p : Program 3, ∀ a n word, denote p ![a,n,word] = OrthemologyTagged.pi3PrefixValue R a n word := by
  obtain ⟨p,hp⟩ := P02A2.PRCoverage.exists_program_of_primrec (family R) (family_primrec R hR)
  exact ⟨p,fun a n word => hp ![a,n,word]⟩

theorem numeric_observer_eq (p : Program 3)
    (hp : ∀ a n word, denote p ![a,n,word] = OrthemologyTagged.pi3PrefixValue R a n word) (a : ℕ) :
    output (evaluateIndex (parameterIndex p a)) = OrthemologyTagged.pi3Observer R a := by
  rw [← OrthemologyTagged.pi3PrefixValue_output]
  funext x n
  unfold output
  rw [parameterIndex_correct, hp, Nat.mod_mod]

theorem numeric_zero_defect_iff (p : Program 3)
    (hp : ∀ a n word, denote p ![a,n,word] = OrthemologyTagged.pi3PrefixValue R a n word) (a : ℕ) :
    defect (fairCantor.map (output (evaluateIndex (parameterIndex p a)))) = 0 ↔
      ∀ i, ∃ s, ∀ t, R a i s t := by
  rw [numeric_observer_eq R p hp]
  exact OrthemologyTagged.pi3_zero_defect_iff R a

theorem exists_numeric_family
    (hR : PrimrecRel (fun p : (ℕ × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) :
    ∃ p : Program 3, ∀ a,
      output (evaluateIndex (parameterIndex p a)) = OrthemologyTagged.pi3Observer R a ∧
      (defect (fairCantor.map (output (evaluateIndex (parameterIndex p a)))) = 0 ↔
        ∀ i, ∃ s, ∀ t, R a i s t) := by
  obtain ⟨p,hp⟩ := exists_fixed_program R hR
  exact ⟨p,fun a => ⟨numeric_observer_eq R p hp a, numeric_zero_defect_iff R p hp a⟩⟩

end P02A2.Pi3Program
