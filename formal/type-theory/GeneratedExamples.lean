/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: cc86ddf29c1a214f2919234728b818cd18c6cf052f76bf56c3874af698908444
def identityCertificate : Cert := (Cert.allI (Cert.i (TypeCode.var 0)))
def identityChecked : Checked := (check 0 identityCertificate).get (by decide)
theorem identity_erasure : identityChecked.term = Term.i := by decide
theorem identity_type : identityChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
theorem identity_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) rho).accepts Term.i := by
  have h := checked_sound identityChecked rho
  rw [identity_type, identity_erasure] at h
  exact h

-- Source JSON SHA256: 327ae08442ae006088260983d5ef56b280f837939d543b7a0f47cf392bd1cc70
def identitySelfCertificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (Cert.allI (Cert.i (TypeCode.var 0))))
def identitySelfChecked : Checked := (check 0 identitySelfCertificate).get (by decide)
theorem identitySelf_erasure : identitySelfChecked.term = (Term.app Term.i Term.i) := by decide
theorem identitySelf_type : identitySelfChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
theorem identitySelf_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound identitySelfChecked rho
  rw [identitySelf_type, identitySelf_erasure] at h
  exact h

-- Source JSON SHA256: 2cb58b81f018721b7d658d6495e7c9ba7bd33fea1ad1e865834308866f1183b8
def reducedIdentityCertificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (Cert.allI (Cert.i (TypeCode.var 0)))))
def reducedIdentityChecked : Checked := (check 0 reducedIdentityCertificate).get (by decide)
theorem reducedIdentity_erasure : reducedIdentityChecked.term = Term.i := by decide
theorem reducedIdentity_type : reducedIdentityChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
theorem reducedIdentity_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) rho).accepts Term.i := by
  have h := checked_sound reducedIdentityChecked rho
  rw [reducedIdentity_type, reducedIdentity_erasure] at h
  exact h

-- Source JSON SHA256: 8168d31f888c46da067bdb5865830b55b122bf7c193d1cb162bb96a2790abe36
def trueSelectorCertificate : Cert := (Cert.allI (Cert.k (TypeCode.var 0) (TypeCode.var 0)))
def trueSelectorChecked : Checked := (check 0 trueSelectorCertificate).get (by decide)
theorem trueSelector_erasure : trueSelectorChecked.term = Term.k := by decide
theorem trueSelector_type : trueSelectorChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem trueSelector_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.k := by
  have h := checked_sound trueSelectorChecked rho
  rw [trueSelector_type, trueSelector_erasure] at h
  exact h

-- Source JSON SHA256: b9be06bad70e9292b03911c6d520bdf089225055a7dae14ee08aad6d33b0ef0d
def falseSelectorCertificate : Cert := (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)) (TypeCode.var 0)) (Cert.i (TypeCode.var 0))))
def falseSelectorChecked : Checked := (check 0 falseSelectorCertificate).get (by decide)
theorem falseSelector_erasure : falseSelectorChecked.term = (Term.app Term.k Term.i) := by decide
theorem falseSelector_type : falseSelectorChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem falseSelector_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts (Term.app Term.k Term.i) := by
  have h := checked_sound falseSelectorChecked rho
  rw [falseSelector_type, falseSelector_erasure] at h
  exact h

-- Source JSON SHA256: 59fc81f1cd820bfea79e9c92a016f61285638ed2855030a36bd5728f81313b4a
def trueSelfChoiceCertificate : Cert := (Cert.app (Cert.app (Cert.allE (Cert.allI (Cert.k (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allI (Cert.k (TypeCode.var 0) (TypeCode.var 0)))) (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)) (TypeCode.var 0)) (Cert.i (TypeCode.var 0)))))
def trueSelfChoiceChecked : Checked := (check 0 trueSelfChoiceCertificate).get (by decide)
theorem trueSelfChoice_erasure : trueSelfChoiceChecked.term = (Term.app (Term.app Term.k Term.k) (Term.app Term.k Term.i)) := by decide
theorem trueSelfChoice_type : trueSelfChoiceChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem trueSelfChoice_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts (Term.app (Term.app Term.k Term.k) (Term.app Term.k Term.i)) := by
  have h := checked_sound trueSelfChoiceChecked rho
  rw [trueSelfChoice_type, trueSelfChoice_erasure] at h
  exact h

-- Source JSON SHA256: 4d8c16f23262ea9ff6bf4c2ca73361bb086bba100754b6f738fc28cde29a6988
def falseSelfChoiceCertificate : Cert := (Cert.app (Cert.app (Cert.allE (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)) (TypeCode.var 0)) (Cert.i (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allI (Cert.k (TypeCode.var 0) (TypeCode.var 0)))) (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)) (TypeCode.var 0)) (Cert.i (TypeCode.var 0)))))
def falseSelfChoiceChecked : Checked := (check 0 falseSelfChoiceCertificate).get (by decide)
theorem falseSelfChoice_erasure : falseSelfChoiceChecked.term = (Term.app (Term.app (Term.app Term.k Term.i) Term.k) (Term.app Term.k Term.i)) := by decide
theorem falseSelfChoice_type : falseSelfChoiceChecked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem falseSelfChoice_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts (Term.app (Term.app (Term.app Term.k Term.i) Term.k) (Term.app Term.k Term.i)) := by
  have h := checked_sound falseSelfChoiceChecked rho
  rw [falseSelfChoice_type, falseSelfChoice_erasure] at h
  exact h

-- Source JSON SHA256: 68cc2c78809bc25520ddfe3273f1931989a885ed546c661f523a973d7b7130be
def diagonalSelfCertificate : Cert := (Cert.allE (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0))) (Cert.app (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allI (Cert.app (Cert.k (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)) (TypeCode.var 0)) (Cert.i (TypeCode.var 0))))))) (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))
def diagonalSelfChecked : Checked := (check 0 diagonalSelfCertificate).get (by decide)
theorem diagonalSelf_erasure : diagonalSelfChecked.term = (Term.app Term.k (Term.app Term.k (Term.app Term.k Term.i))) := by decide
theorem diagonalSelf_type : diagonalSelfChecked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem diagonalSelf_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.var 0)) (TypeCode.arrow (TypeCode.arrow (TypeCode.var 0) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts (Term.app Term.k (Term.app Term.k (Term.app Term.k Term.i))) := by
  have h := checked_sound diagonalSelfChecked rho
  rw [diagonalSelf_type, diagonalSelf_erasure] at h
  exact h

end OrthemologyV4Exports
