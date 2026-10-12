/- Additive finite serialization for the frozen Joint/E derivation certificate checker.
   This proves checking of supplied finite codes, not computability in a separate machine
   model and not decidability of arbitrary judgment inhabitation. -/
import EncodedCertificatePayloads

namespace JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 32000000

/- A nonnested finite tree representation, with an explicit child-list datatype. -/
mutual
inductive SerialCert where
  | node : Rule → SerialCertList → SerialCert
inductive SerialCertList where
  | nil : SerialCertList
  | cons : SerialCert → SerialCertList → SerialCertList
end

deriving instance Encodable for SerialCert, SerialCertList

mutual
def toSerial : DerivationCertificate → SerialCert
  | .node r cs => .node r (toSerialList cs)
termination_by c => sizeOf c

def toSerialList : List DerivationCertificate → SerialCertList
  | [] => .nil
  | c :: cs => .cons (toSerial c) (toSerialList cs)
termination_by cs => sizeOf cs
end

mutual
def fromSerial : SerialCert → DerivationCertificate
  | .node r cs => .node r (fromSerialList cs)

def fromSerialList : SerialCertList → List DerivationCertificate
  | .nil => []
  | .cons c cs => fromSerial c :: fromSerialList cs
end

mutual
theorem fromSerial_toSerial (c : DerivationCertificate) : fromSerial (toSerial c) = c := by
  cases c with
  | node r cs =>
    rw [toSerial, fromSerial]
    exact congrArg (Certificate.node r) (fromSerialList_toSerialList cs)
termination_by sizeOf c

theorem fromSerialList_toSerialList (cs : List DerivationCertificate) :
    fromSerialList (toSerialList cs) = cs := by
  cases cs with
  | nil => simp only [toSerialList, fromSerialList]
  | cons c cs =>
    rw [toSerialList, fromSerialList]
    exact congrArg₂ List.cons (fromSerial_toSerial c) (fromSerialList_toSerialList cs)
termination_by sizeOf cs
end

mutual
theorem toSerial_fromSerial (c : SerialCert) : toSerial (fromSerial c) = c := by
  cases c with
  | node r cs =>
    rw [fromSerial, toSerial]
    exact congrArg (SerialCert.node r) (toSerialList_fromSerialList cs)

theorem toSerialList_fromSerialList (cs : SerialCertList) :
    toSerialList (fromSerialList cs) = cs := by
  cases cs with
  | nil => simp only [fromSerialList, toSerialList]
  | cons c cs =>
    rw [fromSerialList, toSerialList]
    exact congrArg₂ SerialCertList.cons (toSerial_fromSerial c) (toSerialList_fromSerialList cs)
end

/-- Encode a finite certificate as one natural number. The exact format is opaque. -/
def encodeCertificate (c : DerivationCertificate) : Nat := Encodable.encode (toSerial c)

/-- Total decoder. Malformed finite codes yield none. -/
def decodeCertificate (code : Nat) : Option DerivationCertificate :=
  (Encodable.decode (α := SerialCert) code).map fromSerial

theorem decode_encodeCertificate (c : DerivationCertificate) :
    decodeCertificate (encodeCertificate c) = some c := by
  unfold decodeCertificate encodeCertificate
  rw [Encodable.encodek]
  change some (fromSerial (toSerial c)) = some c
  rw [fromSerial_toSerial]

/-- A supplied natural code is untrusted input; malformed decodings reject. -/
def checkCode (code : Nat) (j : Claim) : Bool :=
  match decodeCertificate code with
  | none => false
  | some c => check c j

theorem checkCode_sound {code : Nat} {j : Claim} (h : checkCode code j = true) : j.denote := by
  unfold checkCode at h
  split at h
  · contradiction
  · exact check_sound h

theorem checkCode_encode (c : DerivationCertificate) (j : Claim) :
    checkCode (encodeCertificate c) j = check c j := by
  simp only [checkCode, decode_encodeCertificate]

/-- Exact soundness and completeness for existence of a supplied finite code. -/
theorem derivable_iff_code (j : Claim) :
    j.denote ↔ ∃ code : Nat, checkCode code j = true := by
  constructor
  · intro h
    obtain ⟨c,hc⟩ := complete h
    exact ⟨encodeCertificate c, by simpa only [checkCode_encode] using hc⟩
  · rintro ⟨code,hcode⟩
    exact checkCode_sound hcode

/-- Both inputs are finite untrusted codes; malformed claims or certificates reject. -/
def checkSerialized (claimCode certificateCode : Nat) : Bool :=
  match Encodable.decode (α := Claim) claimCode with
  | none => false
  | some j => checkCode certificateCode j

theorem checkSerialized_sound {claimCode certificateCode : Nat}
    (h : checkSerialized claimCode certificateCode = true) :
    ∃ j : Claim, Encodable.decode claimCode = some j ∧ j.denote := by
  unfold checkSerialized at h
  split at h
  · contradiction
  · exact ⟨_, ‹_ = some _›, checkCode_sound h⟩

theorem checkSerialized_encode (c : DerivationCertificate) (j : Claim) :
    checkSerialized (Encodable.encode j) (encodeCertificate c) = check c j := by
  simp only [checkSerialized, Encodable.encodek, checkCode_encode]

theorem derivable_iff_serialized (j : Claim) :
    j.denote ↔ ∃ code : Nat, checkSerialized (Encodable.encode j) code = true := by
  simpa only [checkSerialized, Encodable.encodek] using derivable_iff_code j

theorem hasJ_iff_code (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) :
    JointCompletion.HasJ Γ p A ↔ ∃ code : Nat, checkCode code (.hasJ Γ p A) = true :=
  derivable_iff_code (.hasJ Γ p A)

#print axioms decode_encodeCertificate
#print axioms checkCode_sound
#print axioms derivable_iff_code
#print axioms checkSerialized_sound
#print axioms derivable_iff_serialized
end JointCertificates
