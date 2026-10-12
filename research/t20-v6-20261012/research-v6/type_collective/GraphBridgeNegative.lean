import GraphBridgeAssembly
import OriginalWNoninhabitation

open P01AC.ExtensionalRepair

/-- The later Henkin obstruction rules out simultaneous exact projection bridges.
It does not choose which bridge is uninhabited. -/
theorem graph_projection_bridges_not_jointly_inhabited :
    ¬ (∃ stateEvidence scalarEvidence,
      HasE InternalGraph.scalarContext stateEvidence InternalGraph.stateTransport ∧
      HasE InternalGraph.scalarContext scalarEvidence InternalGraph.scalarTransport) := by
  rintro ⟨s, x, hs, hx⟩
  exact HomogeneousOriginalW.original_c3_not_W
    (InternalGraph.BridgeAssembly.scalar_fusion_from_bridges hs hx)
