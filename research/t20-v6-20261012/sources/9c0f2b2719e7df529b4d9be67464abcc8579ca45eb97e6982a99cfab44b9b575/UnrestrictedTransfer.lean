import GenericAuditControls
open MeasureTheory
open Orthemology.Tranche2.FiniteAlphabetQuery GenericAuditControls
example :
    traceLaw (fun _ => true) (fun (_ : Bool) y => y) (Measure.dirac false)
      (Measure.dirac (fun _ : ℕ => true)) ≪
    traceLaw (fun _ => true) (fun (_ : Bool) y => y) (Measure.dirac false)
      (iidOracle fairBit) :=
  finite_query_domination_by_iid_rival (fun _ => true) (fun (_ : Bool) y => y)
    measurable_const (fun _ => measurable_const) (Measure.dirac false)
    (Measure.dirac (fun _ : ℕ => true)) fairBit fairBit_full
