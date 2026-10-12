/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: 7ff66fce8d410d856d84217091bed5892ed6bcd45db91be12e47c10fb788c1ad
def probe112Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0)))))))))
def probe112Checked : Checked := (check 0 probe112Certificate).get (by decide)
theorem probe112_erasure : probe112Checked.term = Term.i := by decide
theorem probe112_type : probe112Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))) := by decide
theorem probe112_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))) rho).accepts Term.i := by
  have h := checked_sound probe112Checked rho
  rw [probe112_type, probe112_erasure] at h
  exact h

-- Source JSON SHA256: 3d74fa16381f622f0f3bb4d32aa04077958e71515dc7c3831baf5781cffded4d
def probe113Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1)))))))))
def probe113Checked : Checked := (check 0 probe113Certificate).get (by decide)
theorem probe113_erasure : probe113Checked.term = Term.i := by decide
theorem probe113_type : probe113Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))))))) := by decide
theorem probe113_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))))))) rho).accepts Term.i := by
  have h := checked_sound probe113Checked rho
  rw [probe113_type, probe113_erasure] at h
  exact h

-- Source JSON SHA256: 30f4cad3abee316b4fe7530bdf991feb52829e02b954c092ae1150c20aea62fe
def probe114Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 2)))))))))
def probe114Checked : Checked := (check 0 probe114Certificate).get (by decide)
theorem probe114_erasure : probe114Checked.term = Term.i := by decide
theorem probe114_type : probe114Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))))))) := by decide
theorem probe114_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))))))) rho).accepts Term.i := by
  have h := checked_sound probe114Checked rho
  rw [probe114_type, probe114_erasure] at h
  exact h

-- Source JSON SHA256: af87de5757024d5adc1784e5f1bdb3a49307adf6d07eefc77598f243993a6504
def probe115Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 3)))))))))
def probe115Checked : Checked := (check 0 probe115Certificate).get (by decide)
theorem probe115_erasure : probe115Checked.term = Term.i := by decide
theorem probe115_type : probe115Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3))))))))) := by decide
theorem probe115_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3))))))))) rho).accepts Term.i := by
  have h := checked_sound probe115Checked rho
  rw [probe115_type, probe115_erasure] at h
  exact h

-- Source JSON SHA256: 3ecdfbe6f353fba2c2f759277f075aa81b2ed68255166644e99acc8763fb29ea
def probe116Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 4)))))))))
def probe116Checked : Checked := (check 0 probe116Certificate).get (by decide)
theorem probe116_erasure : probe116Checked.term = Term.i := by decide
theorem probe116_type : probe116Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4))))))))) := by decide
theorem probe116_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4))))))))) rho).accepts Term.i := by
  have h := checked_sound probe116Checked rho
  rw [probe116_type, probe116_erasure] at h
  exact h

-- Source JSON SHA256: bdde120fe5071676fe9a77392b8250512d9e055087a3ababa851c35d630b2789
def probe117Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 5)))))))))
def probe117Checked : Checked := (check 0 probe117Certificate).get (by decide)
theorem probe117_erasure : probe117Checked.term = Term.i := by decide
theorem probe117_type : probe117Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 5) (TypeCode.var 5))))))))) := by decide
theorem probe117_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 5) (TypeCode.var 5))))))))) rho).accepts Term.i := by
  have h := checked_sound probe117Checked rho
  rw [probe117_type, probe117_erasure] at h
  exact h

-- Source JSON SHA256: 7e8a087960e9611a81a0dca992feb94cfbf4d10c14d6c5f53eface453e54015b
def probe118Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 6)))))))))
def probe118Checked : Checked := (check 0 probe118Certificate).get (by decide)
theorem probe118_erasure : probe118Checked.term = Term.i := by decide
theorem probe118_type : probe118Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 6) (TypeCode.var 6))))))))) := by decide
theorem probe118_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 6) (TypeCode.var 6))))))))) rho).accepts Term.i := by
  have h := checked_sound probe118Checked rho
  rw [probe118_type, probe118_erasure] at h
  exact h

end OrthemologyV4Exports
