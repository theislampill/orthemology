import UnitTransfer
open P01AC P01D P01AC.ExtensionalRepair RigidityPolymorphicTransfer SourceRigidity
-- This helper deliberately requires original Has evidence before crossing binders.
example {Γ r u} (hc : Ctx Γ) (hr : HasE Γ r Rigidity) (hu : Has Γ u UnitTy) :
    HasE Γ ident (.identity UnitTy u ident) :=
  unit_ext_from_original_rigidity hc hr hu
