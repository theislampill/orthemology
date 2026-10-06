import PathEdgesMutant

/-! Executable finite-path controls. These are authored before CertificatePath.
The direct and detour witnesses must both pass; the checker must reconstruct
sources rather than accepting a free source annotation at each step. -/
namespace OrthemicCertificate.PathControls

abbrev State := Fin 3
abbrev Action := Fin 2

def allowed : Finset (State × Action) := {(0, 0), (0, 1), (1, 0), (2, 0)}

def succ (e : State × Action) : Finset State :=
  if e = (0, 0) then {2}
  else if e = (0, 1) then {1}
  else if e = (1, 0) then {2}
  else if e = (2, 0) then {0}
  else ∅

def direct : Path State Action := ⟨0, [(0, 2)]⟩
def detour : Path State Action := ⟨0, [(1, 1), (0, 2)]⟩
def wrongSource : Path State Action := ⟨1, [(1, 1), (0, 2)]⟩
def tooLong : Path State Action := ⟨0, [(0, 2), (0, 0), (0, 2)]⟩

def results : List (String × Bool) :=
  [("direct_route", decide (Path.Valid allowed succ 0 2 direct)),
   ("distinct_detour", decide (Path.Valid allowed succ 0 2 detour)),
   ("reconstructed_source_rejects", !decide (Path.Valid allowed succ 1 2 wrongSource)),
   ("length_bound_rejects", !decide (Path.Valid allowed succ 0 2 tooLong)),
   ("wrong_endpoint_rejects", !decide (Path.Valid allowed succ 0 1 direct)),
   ("wrong_declared_start_rejects", !decide (Path.Valid allowed succ 1 2 direct)),
   ("used_edge_removal_rejects", !decide (Path.Valid (allowed.erase (0, 0)) succ 0 2 direct)),
   ("empty_singleton_accepts", decide (Path.Valid (∅ : Finset (Fin 1 × Fin 1))
      (fun _ => ∅) 0 0 ⟨0, []⟩)),
   ("singleton_nonempty_rejects", !decide (Path.Valid ({(0, 0)} : Finset (Fin 1 × Fin 1))
      (fun _ => {0}) 0 0 ⟨0, [(0, 0)]⟩))]

#eval results
#guard results.all Prod.snd


end OrthemicCertificate.PathControls
