/- Fixed-template universal observation. All external representation and halting
   properties remain explicit hypotheses; no evaluator or hierarchy is axiomatized. -/
import EffectiveCanonicalTests

namespace P01AC.IdentityComplexity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness

def numericSucc : Term := .app .s numericB

theorem repeated_step_numeral (n : Nat) :
    Conv (iterateTerm (stepTerm numericSucc) n (numeral 0)) (numeral n) := by
  induction n with
  | zero => exact .refl _
  | succ n ih =>
    exact (Conv.right (stepTerm numericSucc) ih).trans
      (rawStep_application numericSucc (numeral n))

def universalTester (U : Term) (e : Nat) : Poly :=
  tester numericSucc (.app U (numeral e)) (numeral 0)

theorem universalTester_has (U : Term) (e : Nat) : Has [] (universalTester U e) C :=
  tester_has _ _ _

theorem universal_target_formed (U : Term) (e : Nat) :
    Form [] (.identity C (universalTester U e) (constantRaw (numeral 0))) :=
  target_formed numericSucc (.app U (numeral e)) 0

theorem universal_target_closed (U : Term) (e : Nat) :
    Scoped 0 (universalTester U e) ∧ Scoped 0 (constantRaw (numeral 0)) :=
  target_closed numericSucc (.app U (numeral e)) 0

theorem universal_target_scope (U : Term) (e : Nat) :
    TyScoped 0 (.identity C (universalTester U e) (constantRaw (numeral 0))) ∧
    Intensional.TyParamScoped 0
      (.identity C (universalTester U e) (constantRaw (numeral 0))) :=
  target_scope_bundle numericSucc (.app U (numeral e)) 0

theorem universalTester_observation (U : Term) (e n : Nat) (t : Term)
    (ht : ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x)) :
    Conv (.app (eval (universalTester U e) zeroEnv) t)
      (.app (.app U (numeral e)) (numeral n)) := by
  have h := tester_application numericSucc (.app U (numeral e)) (numeral 0) t
  exact h.trans (Conv.right (.app U (numeral e))
    ((ht (stepTerm numericSucc) (numeral 0)).trans (repeated_step_numeral n)))

/-- The relation H is arbitrary; neither its computation nor a representing
    program's existence is proved or added as an axiom here. -/
theorem universal_endpoint_valid_iff_total (U : Term) (H : Nat → Nat → Prop)
    (defined : ∀ e n, H e n →
      Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (undefined : ∀ e n, ¬ H e n →
      ¬ Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (e : Nat) : EndpointValid (universalTester U e) (constantRaw (numeral 0)) ↔
      ∀ n, H e n := by
  have eqtest := endpoint_valid_iff_canonical_tests
    (universalTester_has U e) (constantRaw_has (numeral 0))
  constructor
  · intro hv n
    apply Classical.byContradiction
    intro hn
    have hc := eqtest.mp hv n
    have obs := universalTester_observation U e n (canonical n)
      (fun f x => inputNumeral_applied n f x zeroEnv)
    have hz := constantRaw_application (numeral 0) (canonical n)
    exact undefined e n hn (obs.symm.trans (hc.trans hz))
  · intro total
    apply eqtest.mpr
    intro n
    have obs := universalTester_observation U e n (canonical n)
      (fun f x => inputNumeral_applied n f x zeroEnv)
    exact obs.trans ((defined e n (total n)).trans
      (constantRaw_application (numeral 0) (canonical n)).symm)

theorem original_universal_identity_iff_total (U : Term) (H : Nat → Nat → Prop)
    (defined : ∀ e n, H e n →
      Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (undefined : ∀ e n, ¬ H e n →
      ¬ Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (e : Nat) : IdentityValid (universalTester U e) (constantRaw (numeral 0)) ↔
      ∀ n, H e n :=
  (identity_valid_iff_endpoint_valid _ _).trans
    (universal_endpoint_valid_iff_total U H defined undefined e)

/-- Conversion to the actual normal zero output would supply a raw normal form. -/
theorem raw_no_normal_form_excludes_zero (t : Term)
    (hn : ¬ ∃ z, Red t z ∧ P01Source.Normal z) : ¬ Conv t (numeral 0) := by
  intro hc
  obtain ⟨z, htz, hzz⟩ := P01Source.conv_join hc
  have he := P01Source.normal_red (numeral_normal 0) hzz
  exact hn ⟨numeral 0, he ▸ htz, numeral_normal 0⟩

theorem numeral_marker_free (n : Nat) : MarkerFree (numeral n) := by
  induction n with
  | zero => exact ⟨trivial, trivial⟩
  | succ n ih => exact ⟨⟨trivial, ⟨⟨trivial, ⟨trivial, trivial⟩⟩, trivial⟩⟩, ih⟩

/-- Uses the inherited exact marker-replacement conversion theorem. This
    records the raw-erasure bridge without identifying external languages. -/
theorem erased_no_normal_form_excludes_zero (t : Term)
    (hn : ¬ ∃ z, Red (replaceMarkers .i .i t) z ∧ P01Source.Normal z) :
    ¬ Conv t (numeral 0) := by
  intro h
  apply raw_no_normal_form_excludes_zero (replaceMarkers .i .i t) hn
  simpa only [replace_free (numeral_marker_free 0)] using (conv_replace h .i .i)

theorem pure_universal_observation_erasure (U : Term) (hU : MarkerFree U) (e n : Nat) :
    replaceMarkers .i .i (.app (.app U (numeral e)) (numeral n)) =
      .app (.app U (numeral e)) (numeral n) :=
  replace_free (t := .app (.app U (numeral e)) (numeral n))
    ⟨⟨hU, numeral_marker_free e⟩, numeral_marker_free n⟩ .i .i

/-- Stronger negative evidence may be passed directly. Its existence and its
    match to a particular external representation theorem remain outside Lean. -/
theorem original_universal_identity_iff_total_of_no_normal_form
    (U : Term) (H : Nat → Nat → Prop)
    (defined : ∀ e n, H e n →
      Conv (.app (.app U (numeral e)) (numeral n)) (numeral 0))
    (undefined : ∀ e n, ¬ H e n →
      ¬ ∃ z, Red (replaceMarkers .i .i (.app (.app U (numeral e)) (numeral n))) z ∧
        P01Source.Normal z)
    (e : Nat) : IdentityValid (universalTester U e) (constantRaw (numeral 0)) ↔
      ∀ n, H e n :=
  original_universal_identity_iff_total U H defined
    (fun a b h => erased_no_normal_form_excludes_zero _ (undefined a b h)) e

end P01AC.IdentityComplexity
