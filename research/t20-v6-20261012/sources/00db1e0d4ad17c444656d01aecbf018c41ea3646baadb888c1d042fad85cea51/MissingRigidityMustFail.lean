import UnitTransfer
open P01AC P01D P01AC.ExtensionalRepair RigidityPolymorphicTransfer
-- A conditional implication cannot be mistaken for an unconditional UnitEta proof.
example : HasE [] (abstract (abstract (.atom .i))) UnitEta :=
  rigidity_implies_unit_eta
