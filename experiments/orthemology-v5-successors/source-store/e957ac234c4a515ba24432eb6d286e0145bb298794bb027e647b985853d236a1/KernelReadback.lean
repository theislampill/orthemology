/- Independent import/readback of the newly compiled control's exact statements. -/
import InhabitedEndpointControl

open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InhabitedControl

example : Has [] InhabitedControl.H (arr (.pi (.all (.param 0)) .raw) (arr N N)) := H_has
example : Has [] (.app InhabitedControl.H (.app (.atom .k) (.atom .i))) (arr N N) := Fp_has
example : Has [] (.app InhabitedControl.H (.app (.atom .k) (.atom .k))) (arr N N) := Fq_has
example : Scoped 0 InhabitedControl.H ∧ Scoped 0 Fp ∧ Scoped 0 Fq :=
  ⟨H_closed,Fp_closed,Fq_closed⟩
example : Form (theta [] (.pi (.all (.param 0)) .raw)
    (.app (.atom .k) (.atom .i)))
    (.identity (arr N N) (.app InhabitedControl.H (.app (.atom .k) (.atom .i)))
      (.app InhabitedControl.H (.var 1))) := motive_form
example : motiveAt motive p (.atom .i) = .identity (arr N N) Fp Fp := base_substitution
example : motiveAt motive q (.atom .i) = .identity (arr N N) Fp Fq := target_substitution
example : HasE []
    (jPoly (.atom .i) (.app (.atom .k) (.atom .k)) (.atom .i))
    (.identity (arr N N)
      (.app (abstract (abstract (fstPoly
        (.app (.app (.var 0) (.atom .i)) (pairPoly (inputNumeral 0) (.var 1))))))
        (.app (.atom .k) (.atom .i)))
      (.app (abstract (abstract (fstPoly
        (.app (.app (.var 0) (.atom .i)) (pairPoly (inputNumeral 0) (.var 1))))))
        (.app (.atom .k) (.atom .k)))) := inhabited_endpoint_identity
example : Has [] (.atom .i) (arr N N) := Q_inhabited
example : InhabitedControl.H = abstract (abstract (fstPoly
    (.app (.app (.var 0) (.atom .i)) (pairPoly (inputNumeral 0) (.var 1))))) := H_exact
example : Fp = .app InhabitedControl.H (.app (.atom .k) (.atom .i)) ∧
    Fq = .app InhabitedControl.H (.app (.atom .k) (.atom .k)) := endpoints_exact

#print axioms inhabited_endpoint_identity
#print axioms H_has
#print axioms motive_form
#print axioms Q_inhabited
