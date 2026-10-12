import OpenDevelopments
import ScalarCertificates
import DomainControls
namespace CompleteDevelopmentReview
open OpenTermStandardness OpenDevelopments

-- The strategy theorem quantifies over the actual open carrier and actual Conv.
theorem actual_open_conversion {t z : T} (hn : OpenDevelopments.Normal z)
    (hc : Conv t z) : ∃ r, OpenDevelopments.run r t = z :=
  OpenDevelopments.development_complete hn hc

-- Every actual conversion constructor is usable without a closedness premise.
example (n : Nat) : Conv (.var n) (.var n) := .refl _
example (f a b : T) (h : Conv a b) :
    Conv (.app f a) (.app f b) := .app (.refl _) h
example (f a b : T) (h : Conv a b) :
    Conv (.app a f) (.app b f) := .app h (.refl _)

-- Do not contract a newly created root redex in the same development round.
example : dev (.app (.app .i .i) (.var 0)) = .app .i (.var 0) := rfl
example : run 2 (.app (.app .i .i) (.var 0)) = .var 0 := rfl
example : dev (.app (.app .k (.var 42)) (.app .i (.var 7))) = .var 42 := rfl
example : dev (.app (.app (.app .s (.var 2)) (.var 3)) (.var 7)) =
    .app (.app (.var 2) (.var 7)) (.app (.var 3) (.var 7)) := rfl

-- Normality and count readback retain generic variable indices exactly.
example : OpenDevelopments.Normal (.var 42) := by
  intro u h
  cases h
  rfl
example : readIteration (.var 0) = some ⟨0, rfl⟩ := rfl
example : (readIteration (.var 1)).isSome = false := rfl
example : (readIteration (.app (.var 0) (.var 1))).isSome = false := rfl
example : (readIteration (.app (.var 1) (.var 0))).isSome = true := rfl
example : (readIteration (.app .i (.var 0))).isSome = false := rfl

-- Count uniqueness is an actual open conversion theorem.
theorem actual_count_unique {m n : Nat}
    (h : Conv (iter (.var 1) (.var 0) m) (iter (.var 1) (.var 0) n)) : m = n :=
  OpenDevelopments.iter_conv_injective h

-- Exact input constructor preservation includes packed application atoms.
example (f a : OrthemologyV2.Term) :
    ImportedOpenTermTransport.interp (.atom (.app f a)) T.var =
      .app (ImportedOpenTermTransport.embed f) (ImportedOpenTermTransport.embed a) := rfl
example (j : Nat) : ImportedOpenTermTransport.interp (.var j) T.var = .var j := rfl

-- A certificate's proposition binds to the actual original source endpoints.
theorem literal_checked_scalar (n : P01D.Poly) (k : Nat)
    (l r : List P01Certificate.Address)
    (h : (ScalarCertificates.checkScalar n k l r).isSome = true) :
    P01AC.Intensional.Plus.PolyConvPlus
      (.app (.app n (.var 1)) (.var 0))
      (.app (.app (.app FullPER.Application.originalQ n) (.var 1)) (.var 0)) :=
  ScalarCertificates.checkedScalar n k l r h

-- Universal quantification here is external and keeps actual closed HasE.
theorem actual_closed_input {n : P01D.Poly}
    (h : P01AC.ExtensionalRepair.HasE [] n P01AC.EffectiveCompleteness.N) :
    ∃ k l r,
      run l (ImportedOpenTermTransport.interp (ClosedScalarInstances.scalarLeft n) T.var) =
        iter (.var 1) (.var 0) k ∧
      run r (ImportedOpenTermTransport.interp (ClosedScalarInstances.scalarRight n) T.var) =
        iter (.var 1) (.var 0) k :=
  closed_HasE_development_terminates h

-- The source-typed discarded divergence also cycles in the exact open Step.
private theorem open_three_cycle {a b c : T}
    (ab : OpenDevelopments.Step a b) (bc : OpenDevelopments.Step b c)
    (ca : OpenDevelopments.Step c a) :
    ¬ Acc (fun u t => OpenDevelopments.Step t u) a := by
  intro h
  have aux : ∀ a, Acc (fun u t => OpenDevelopments.Step t u) a →
      ∀ b c, OpenDevelopments.Step a b → OpenDevelopments.Step b c →
        OpenDevelopments.Step c a → False := by
    intro a ha
    induction ha with
    | intro a next ih =>
      intro b c ab bc ca
      exact ih b ab c a bc ca ab
  exact aux a h b c ab bc ca

def openDelta : T := .app (.app .s .i) .i

theorem padded_not_open_SN (k : Nat) :
    ¬ Acc (fun u t => OpenDevelopments.Step t u)
      (ImportedOpenTermTransport.interp (OpenDevelopments.DomainControls.padded k) T.var) := by
  apply open_three_cycle
    (OpenDevelopments.Step.right _ (OpenDevelopments.Step.s .i .i openDelta))
    (OpenDevelopments.Step.right _ (OpenDevelopments.Step.left
      (OpenDevelopments.Step.i openDelta) _))
    (OpenDevelopments.Step.right _ (OpenDevelopments.Step.right openDelta
      (OpenDevelopments.Step.i openDelta)))

#print axioms padded_not_open_SN
#print axioms actual_open_conversion
#print axioms actual_count_unique
#print axioms literal_checked_scalar
#print axioms actual_closed_input
end CompleteDevelopmentReview
