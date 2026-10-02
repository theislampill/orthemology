/- Partial constructor-export boundary. This models proof_export._cert's
512-unit construction work guard after successful checking. It intentionally
is not the full textual exporter: identifier/row/byte/host guards remain separate. -/
import SourceResources
namespace P03Source
open OrthemologyV2 OrthemologyV3

def exportWork : SourceProof → Nat
  | .i _ | .k _ _ | .s _ _ _ => 1
  | .app p q => 1 + exportWork p + exportWork q
  | .allI p | .allE p _ => 1 + exportWork p
  | .reduce p trace => 1 + (trace.length-1) + exportWork p

def certNodes : Cert → Nat
  | .i _ | .k _ _ | .s _ _ _ => 1
  | .app p q => 1 + certNodes p + certNodes q
  | .allI p | .allE p _ | .step p => 1 + certNodes p

theorem certSteps_nodes (n : Nat) (c : Cert) :
    certNodes (certSteps n c) = n + certNodes c := by
  induction n with
  | zero => simp [certSteps]
  | succ n ih => simp [certSteps, certNodes, ih]; omega

/-- Reduce wrappers consume one source work unit in addition to emitted steps,
so source expansion work is a conservative bound on actual Cert nodes. -/
theorem encoded_nodes_le_export_work (p : SourceProof) :
    certNodes (encode p) ≤ exportWork p := by
  induction p <;> simp_all [encode, certNodes, exportWork, certSteps_nodes] <;> omega

def partialConstructorExport (p : SourceProof) : Option (Cert × (Term × TypeCode)) :=
  match sourceCheck 0 p with
  | none => none
  | some out => if exportWork p ≤ 512 then some (encode p, out) else none

theorem partial_constructor_export_square {p : SourceProof} {c : Cert}
    {out : Term × TypeCode} (h : partialConstructorExport p = some (c,out)) :
    ∃ v, check 0 c = some v ∧ v.term = out.1 ∧ v.ty = out.2 ∧ certNodes c ≤ 512 := by
  unfold partialConstructorExport at h
  cases hs : sourceCheck 0 p with
  | none => simp [hs] at h
  | some result =>
      simp only [hs] at h
      split at h
      next hb =>
        cases h
        obtain ⟨v,hv,ht,ha⟩ := source_checker_constructor_erasure_square p 0 out hs
        exact ⟨v,hv,ht,ha,Nat.le_trans (encoded_nodes_le_export_work p) hb⟩
      next hn => contradiction

/-- An explicitly partial export square. Both source acceptance and the
constructor-export success gate are required; no total textual export claim. -/
theorem source_checker_export_square {p : SourceProof} {c : Cert} {out : Term × TypeCode}
    (_sourceAccepted : sourceCheck 0 p = some out)
    (exportSucceeded : partialConstructorExport p = some (c,out)) :
    ∃ v, check 0 c = some v ∧ v.term = out.1 ∧ v.ty = out.2 ∧ certNodes c ≤ 512 :=
  partial_constructor_export_square exportSucceeded

def balancedIdentity : Nat → SourceProof
  | 0 => .allI (.i (.var 0))
  | n+1 => .app (.allE (balancedIdentity n) identityCode) (balancedIdentity n)

theorem balanced_expansion_work : exportWork (balancedIdentity 8) = 1022 := by decide

theorem balanced_input_nodes : (proofShape (balancedIdentity 8)).nodes = 7916 := by decide

theorem balanced_checker_accepts : (sourceCheck 0 (balancedIdentity 8)).isSome = true := by decide

theorem balanced_export_refuses : partialConstructorExport (balancedIdentity 8) = none := by
  unfold partialConstructorExport
  split <;> simp [balanced_expansion_work]

/-- Checker acceptance cannot license bypassing the independent exporter guard. -/
theorem checker_acceptance_not_total_export :
    (sourceCheck 0 (balancedIdentity 8)).isSome = true ∧
      partialConstructorExport (balancedIdentity 8) = none :=
  ⟨balanced_checker_accepts, balanced_export_refuses⟩

#print axioms partial_constructor_export_square
#print axioms checker_acceptance_not_total_export
end P03Source
