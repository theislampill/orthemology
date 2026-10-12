import SourceCorrectionHistories

namespace FiniteSidecar.IndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive

-- Ragged tables and out-of-range coordinates use the declared fallback.
example : tableValue [[7,8],[9]] 99 0 2 = 99 := by decide
example : tableValue [[7,8],[9]] 99 1 1 = 99 := by decide
example : tableValue [[7,8],[9]] 99 2 0 = 99 := by decide
example : tableValue [[7,8],[9]] 99 0 1 = 8 := by decide

-- An empty represented rectangle still gives a well-typed total source controller.
def emptyTables : Tables := ⟨[],[],[]⟩
theorem empty_controller_has : Has [] (controller emptyTables) (arr State Reply) :=
  controller_has emptyTables

theorem empty_controller_defaults {p : Term} {z k : Nat} (hp : Represents p z k) :
    NatObs (firstTerm (.app (eval (controller emptyTables) zeroEnv) p)) 0 ∧
    Represents (secondTerm (.app (eval (controller emptyTables) zeroEnv) p)) 0 0 := by
  simpa [emptyTables, tableValue, lookupValue] using controller_observes emptyTables hp

-- Numeric typing alone does not prove closure of the declared finite rectangle.
def escaping : Tables := finiteTables 1 1 (fun _ _ => 7) (fun _ _ => 2) (fun _ _ => 0)
theorem escaping_has : Has [] (controller escaping) (arr State Reply) := controller_has escaping
example : runCodes [escaping, escaping] 0 0 = ([7,0], (0,0)) := by decide

theorem escaping_observes :
    NatObs (firstTerm (.app (eval (controller escaping) zeroEnv)
      (eval (encodeState 0 0) zeroEnv))) 7 ∧
    Represents (secondTerm (.app (eval (controller escaping) zeroEnv)
      (eval (encodeState 0 0) zeroEnv))) 2 0 := by
  exact finite_controller_observes (Z := 1) (M := 1)
    (fun _ _ => 7) (fun _ _ => 2) (fun _ _ => 0)
    (by decide) (by decide) (encoded_represents 0 0)

-- The lower bound rejects a hidden typed proof-only distinction.
theorem same_data_no_proof_observer {z k : Nat} {e f : Poly}
    (he : JointCompletion.HasJ [] e Evidence) (hf : JointCompletion.HasJ [] f Evidence) :
    ¬ ObservablyDifferent (withEvidence z k e) (withEvidence z k f) := by
  rintro ⟨observer,j,l,ho,oj,ol,hjl⟩
  exact hjl (observer_identity_counts (withEvidence_has z k he) (withEvidence_has z k hf)
    ho oj ol (proof_slot_cannot_separate z k he hf))

-- Zero counts are legal in the encoding theorem, whereas a nonempty class cannot map to Fin 0.
example (Z : Nat) :
    ∃ tags : (z : Fin Z) → Fin 0 → Fin 0,
      ∃ evidence : (z : Fin Z) → Fin 0 → Poly,
      (∀ z i, JointCompletion.HasJ [] (evidence z i) Evidence) ∧
      (∀ z i j, i ≠ j → ObservablyDifferent
        (withEvidence z.val (tags z i).val (evidence z i))
        (withEvidence z.val (tags z j).val (evidence z j))) := by
  exact (common_alphabet_exact (fun _ : Fin Z => 0)).mpr (fun _ => Nat.le_refl 0)

example (n : Nat) (hn : 0 < n) : ¬ Nonempty (Fin n → Fin 0) := by
  rintro ⟨f⟩
  exact Fin.elim0 (f ⟨0,hn⟩)

#print axioms empty_controller_defaults
#print axioms escaping_observes
#print axioms same_data_no_proof_observer
end FiniteSidecar.IndependentReview
