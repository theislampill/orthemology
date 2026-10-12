import SerializedCertificateCodec
namespace ActualSourceEnumerability
open JointCertificates
set_option maxRecDepth 16384
set_option maxHeartbeats 2000000

/- Ordered mutual finite-tree checking, with exactly the retained source rules. -/
mutual
def serialCheck : SerialCert → Claim → Bool
  | .node r cs, j => r.checkSide && decide (r.conclusion = j) && serialCheckList cs r.premises
def serialCheckList : SerialCertList → List Claim → Bool
  | .nil, [] => true
  | .cons c cs, j :: js => serialCheck c j && serialCheckList cs js
  | _, _ => false
end

abbrev coreCheck := Certificate.check Rule.conclusion Rule.premises Rule.checkSide

def coreList (cs : SerialCertList) (js : List Claim) : Bool :=
  decide ((fromSerialList cs).map (fun c => c.rule.conclusion) = js) &&
    (fromSerialList cs).all coreCheck

mutual
theorem serialCheck_exact (c : SerialCert) (j : Claim) :
    serialCheck c j = check (fromSerial c) j := by
  cases c with
  | node r cs =>
    rw [serialCheck, serialCheckList_exact]
    simp only [check, Certificate.checkRoot, fromSerial, Certificate.rule,
      Certificate.check_node, coreList]
    simp only [Bool.and_assoc, Bool.and_left_comm, Bool.and_comm]

theorem serialCheckList_exact (cs : SerialCertList) (js : List Claim) :
    serialCheckList cs js = coreList cs js := by
  cases cs with
  | nil => cases js <;> rfl
  | cons c cs =>
    cases js with
    | nil => simp [serialCheckList, coreList, fromSerialList]
    | cons j js =>
      rw [serialCheckList, serialCheck_exact, serialCheckList_exact]
      simp [coreList, fromSerialList, check, Certificate.checkRoot,
        Bool.and_assoc, Bool.and_left_comm, Bool.and_comm]
end

theorem serialCheck_sound {c : SerialCert} {j : Claim} (h : serialCheck c j = true) : j.denote :=
  check_sound (serialCheck_exact c j ▸ h)

theorem serialCheck_complete (j : Claim) (h : j.denote) : ∃ c, serialCheck c j = true := by
  obtain ⟨c, hc⟩ := complete h
  exact ⟨toSerial c, by simpa only [serialCheck_exact, fromSerial_toSerial] using hc⟩

#print axioms serialCheck_exact
#print axioms serialCheck_sound
#print axioms serialCheck_complete
end ActualSourceEnumerability
