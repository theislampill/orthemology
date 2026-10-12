/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: d0fa7c9bc02af1ba7dea1eac347bba4e18f36d753b0e3c2c8d1260fa03e6551d
def probe64Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe64Checked : Checked := (check 0 probe64Certificate).get (by decide)
theorem probe64_erasure : probe64Checked.term = Term.s := by decide
theorem probe64_type : probe64Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe64_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe64Checked rho
  rw [probe64_type, probe64_erasure] at h
  exact h

-- Source JSON SHA256: 69f31311fab42cccbf15ae00e12a3bae47d78239a7c26f7532ae093874cec1d4
def probe65Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe65Checked : Checked := (check 0 probe65Certificate).get (by decide)
theorem probe65_erasure : probe65Checked.term = Term.s := by decide
theorem probe65_type : probe65Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe65_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe65Checked rho
  rw [probe65_type, probe65_erasure] at h
  exact h

-- Source JSON SHA256: 72b5891ab763dcefc116e1b28884c95c927d8afd9246236b4c1a48b6e25371f7
def probe66Certificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))
def probe66Checked : Checked := (check 0 probe66Certificate).get (by decide)
theorem probe66_erasure : probe66Checked.term = Term.i := by decide
theorem probe66_type : probe66Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe66_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe66Checked rho
  rw [probe66_type, probe66_erasure] at h
  exact h

-- Source JSON SHA256: b58d2696667dc036f0e3f6cfd70d5ffb5956e35755b24d62136e8756bb2b2c26
def probe67Certificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))
def probe67Checked : Checked := (check 0 probe67Certificate).get (by decide)
theorem probe67_erasure : probe67Checked.term = Term.i := by decide
theorem probe67_type : probe67Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe67_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe67Checked rho
  rw [probe67_type, probe67_erasure] at h
  exact h

-- Source JSON SHA256: c772c13b3e58d36b9e259d32d61fa85cf37b85b6cb28fb3275aa24772ceec45a
def probe68Certificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))
def probe68Checked : Checked := (check 0 probe68Certificate).get (by decide)
theorem probe68_erasure : probe68Checked.term = Term.i := by decide
theorem probe68_type : probe68Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe68_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe68Checked rho
  rw [probe68_type, probe68_erasure] at h
  exact h

-- Source JSON SHA256: 31d4401baa41764f14fe5a244e56417f5606829f806de0a090257bb50fb5fb01
def probe69Certificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))
def probe69Checked : Checked := (check 0 probe69Certificate).get (by decide)
theorem probe69_erasure : probe69Checked.term = Term.i := by decide
theorem probe69_type : probe69Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe69_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe69Checked rho
  rw [probe69_type, probe69_erasure] at h
  exact h

-- Source JSON SHA256: b3344432474f4d1b5c6b3d7b2435f0f3ee775bbeccb6d8de30688352a078552a
def probe70Certificate : Cert := (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))
def probe70Checked : Checked := (check 0 probe70Certificate).get (by decide)
theorem probe70_erasure : probe70Checked.term = Term.i := by decide
theorem probe70_type : probe70Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe70_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe70Checked rho
  rw [probe70_type, probe70_erasure] at h
  exact h

-- Source JSON SHA256: 2d691e92ff8cfe0377f5da28902dd52ce8a6d9755a66d64ff0dfb1c9712c2aff
def probe71Certificate : Cert := (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))))
def probe71Checked : Checked := (check 0 probe71Certificate).get (by decide)
theorem probe71_erasure : probe71Checked.term = Term.i := by decide
theorem probe71_type : probe71Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe71_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe71Checked rho
  rw [probe71_type, probe71_erasure] at h
  exact h

-- Source JSON SHA256: 89d8af11ad172689731db5203fca9c983830451237d1aa12586a891da4a32418
def probe72Certificate : Cert := (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))
def probe72Checked : Checked := (check 0 probe72Certificate).get (by decide)
theorem probe72_erasure : probe72Checked.term = Term.i := by decide
theorem probe72_type : probe72Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe72_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe72Checked rho
  rw [probe72_type, probe72_erasure] at h
  exact h

-- Source JSON SHA256: f1fc1309f4c53b6b8f7931e0c70a7211cbdf60a025b01606ab1a7c27fe9246d5
def probe73Certificate : Cert := (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))))
def probe73Checked : Checked := (check 0 probe73Certificate).get (by decide)
theorem probe73_erasure : probe73Checked.term = Term.i := by decide
theorem probe73_type : probe73Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe73_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe73Checked rho
  rw [probe73_type, probe73_erasure] at h
  exact h

-- Source JSON SHA256: ae2f20e99c27119e28c1ff85b1778aafca7eef98ac36dfdcad6300fed11be3f3
def probe74Certificate : Cert := (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))
def probe74Checked : Checked := (check 0 probe74Certificate).get (by decide)
theorem probe74_erasure : probe74Checked.term = Term.i := by decide
theorem probe74_type : probe74Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe74_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe74Checked rho
  rw [probe74_type, probe74_erasure] at h
  exact h

-- Source JSON SHA256: d9021d9d3c7a25cb7260a62a5709c9e01755cde9c53ceab8efc02474d2720600
def probe75Certificate : Cert := (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))))
def probe75Checked : Checked := (check 0 probe75Certificate).get (by decide)
theorem probe75_erasure : probe75Checked.term = Term.i := by decide
theorem probe75_type : probe75Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe75_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe75Checked rho
  rw [probe75_type, probe75_erasure] at h
  exact h

-- Source JSON SHA256: 4c4835d3f76f98280378e3a67861ccf9b7d2de4529d2e4239bee96b3fc1b60ea
def probe76Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))))))
def probe76Checked : Checked := (check 0 probe76Certificate).get (by decide)
theorem probe76_erasure : probe76Checked.term = Term.i := by decide
theorem probe76_type : probe76Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe76_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe76Checked rho
  rw [probe76_type, probe76_erasure] at h
  exact h

-- Source JSON SHA256: 26e61c5b137aa4f2f08cd3cee588d9c75b912c47cbbd5c4c30dd160da838494c
def probe77Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))
def probe77Checked : Checked := (check 0 probe77Certificate).get (by decide)
theorem probe77_erasure : probe77Checked.term = Term.i := by decide
theorem probe77_type : probe77Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe77_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe77Checked rho
  rw [probe77_type, probe77_erasure] at h
  exact h

-- Source JSON SHA256: d2ec14d1e125d5e8152b9da08930a9a1f815a984440d3a4343722a8db5d9d5ae
def probe78Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))))))
def probe78Checked : Checked := (check 0 probe78Certificate).get (by decide)
theorem probe78_erasure : probe78Checked.term = Term.i := by decide
theorem probe78_type : probe78Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe78_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe78Checked rho
  rw [probe78_type, probe78_erasure] at h
  exact h

-- Source JSON SHA256: 335d6a7c981eb104297f64734335fcb4c84fe3a080a7d17ccc4943571484b4e5
def probe79Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))))
def probe79Checked : Checked := (check 0 probe79Certificate).get (by decide)
theorem probe79_erasure : probe79Checked.term = Term.i := by decide
theorem probe79_type : probe79Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe79_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe79Checked rho
  rw [probe79_type, probe79_erasure] at h
  exact h

end OrthemologyV4Exports
