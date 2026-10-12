/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: fc2d875e7af1621bab6d962cc5a5bdda840712af09657bb2642ebdd1c6a03499
def probe96Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 2)))))
def probe96Checked : Checked := (check 0 probe96Certificate).get (by decide)
theorem probe96_erasure : probe96Checked.term = Term.i := by decide
theorem probe96_type : probe96Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))) := by decide
theorem probe96_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))) rho).accepts Term.i := by
  have h := checked_sound probe96Checked rho
  rw [probe96_type, probe96_erasure] at h
  exact h

-- Source JSON SHA256: 85ef4020e20c9cd3581f536241f807730950c05d609d50bda94a3d00e9d6023a
def probe97Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0))))))
def probe97Checked : Checked := (check 0 probe97Certificate).get (by decide)
theorem probe97_erasure : probe97Checked.term = Term.i := by decide
theorem probe97_type : probe97Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe97_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe97Checked rho
  rw [probe97_type, probe97_erasure] at h
  exact h

-- Source JSON SHA256: 3153744ab480ebfd1a8d295a7299f22029195c32d0dee44f25bb53aab473fd70
def probe98Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1))))))
def probe98Checked : Checked := (check 0 probe98Certificate).get (by decide)
theorem probe98_erasure : probe98Checked.term = Term.i := by decide
theorem probe98_type : probe98Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))))) := by decide
theorem probe98_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))))) rho).accepts Term.i := by
  have h := checked_sound probe98Checked rho
  rw [probe98_type, probe98_erasure] at h
  exact h

-- Source JSON SHA256: 1f475fc27e6b2b526951fd61dd3f7b45f2dba47d76c9486ef5d242bc7faee507
def probe99Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 2))))))
def probe99Checked : Checked := (check 0 probe99Certificate).get (by decide)
theorem probe99_erasure : probe99Checked.term = Term.i := by decide
theorem probe99_type : probe99Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2)))))) := by decide
theorem probe99_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2)))))) rho).accepts Term.i := by
  have h := checked_sound probe99Checked rho
  rw [probe99_type, probe99_erasure] at h
  exact h

-- Source JSON SHA256: 0d8f12849123ade0ad81b8cb9b2ec215ce87eba7f14529305f2aca4ee595dfcb
def probe100Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 3))))))
def probe100Checked : Checked := (check 0 probe100Certificate).get (by decide)
theorem probe100_erasure : probe100Checked.term = Term.i := by decide
theorem probe100_type : probe100Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3)))))) := by decide
theorem probe100_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3)))))) rho).accepts Term.i := by
  have h := checked_sound probe100Checked rho
  rw [probe100_type, probe100_erasure] at h
  exact h

-- Source JSON SHA256: cdab01c4b90e053cca212de47e1e7d4feb0569b10681bdebcdb5e3792634b2d0
def probe101Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0)))))))
def probe101Checked : Checked := (check 0 probe101Certificate).get (by decide)
theorem probe101_erasure : probe101Checked.term = Term.i := by decide
theorem probe101_type : probe101Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe101_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.i := by
  have h := checked_sound probe101Checked rho
  rw [probe101_type, probe101_erasure] at h
  exact h

-- Source JSON SHA256: 00d7ca71f4663427edfe463889f6072a4026e0b56d80befff97dec2be9e81302
def probe102Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1)))))))
def probe102Checked : Checked := (check 0 probe102Certificate).get (by decide)
theorem probe102_erasure : probe102Checked.term = Term.i := by decide
theorem probe102_type : probe102Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))))) := by decide
theorem probe102_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))))) rho).accepts Term.i := by
  have h := checked_sound probe102Checked rho
  rw [probe102_type, probe102_erasure] at h
  exact h

-- Source JSON SHA256: 72b5a493b0d8a5c78264155bd6add73d3a9ac3bdb657fdbff90a7666edbac8b0
def probe103Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 2)))))))
def probe103Checked : Checked := (check 0 probe103Certificate).get (by decide)
theorem probe103_erasure : probe103Checked.term = Term.i := by decide
theorem probe103_type : probe103Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))))) := by decide
theorem probe103_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2))))))) rho).accepts Term.i := by
  have h := checked_sound probe103Checked rho
  rw [probe103_type, probe103_erasure] at h
  exact h

-- Source JSON SHA256: 37e3c9166628cbbb2772dc5ccb5ada674893966f5fe48c1c43a2adea5dd36023
def probe104Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 3)))))))
def probe104Checked : Checked := (check 0 probe104Certificate).get (by decide)
theorem probe104_erasure : probe104Checked.term = Term.i := by decide
theorem probe104_type : probe104Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3))))))) := by decide
theorem probe104_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3))))))) rho).accepts Term.i := by
  have h := checked_sound probe104Checked rho
  rw [probe104_type, probe104_erasure] at h
  exact h

-- Source JSON SHA256: 2f0fd4c008f4cf4826d8820f2ad2332067c6bd8b1effb516a8a44382e2c88f10
def probe105Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 4)))))))
def probe105Checked : Checked := (check 0 probe105Certificate).get (by decide)
theorem probe105_erasure : probe105Checked.term = Term.i := by decide
theorem probe105_type : probe105Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4))))))) := by decide
theorem probe105_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4))))))) rho).accepts Term.i := by
  have h := checked_sound probe105Checked rho
  rw [probe105_type, probe105_erasure] at h
  exact h

-- Source JSON SHA256: 98e568d33a130dab6e8780370b69d0cd086c80cc3ed35f7224fe759131264445
def probe106Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0))))))))
def probe106Checked : Checked := (check 0 probe106Certificate).get (by decide)
theorem probe106_erasure : probe106Checked.term = Term.i := by decide
theorem probe106_type : probe106Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))) := by decide
theorem probe106_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))) rho).accepts Term.i := by
  have h := checked_sound probe106Checked rho
  rw [probe106_type, probe106_erasure] at h
  exact h

-- Source JSON SHA256: f896fdd7c00fb96a3952bf558ecf2c0428619bbe44bd661e73181e09e5c9b5c1
def probe107Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1))))))))
def probe107Checked : Checked := (check 0 probe107Certificate).get (by decide)
theorem probe107_erasure : probe107Checked.term = Term.i := by decide
theorem probe107_type : probe107Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))))))) := by decide
theorem probe107_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))))))) rho).accepts Term.i := by
  have h := checked_sound probe107Checked rho
  rw [probe107_type, probe107_erasure] at h
  exact h

-- Source JSON SHA256: 5c6654ec5fa4053a3f807c14a0f57e825718c7ea984c2fac2a1e0e6c87c18502
def probe108Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 2))))))))
def probe108Checked : Checked := (check 0 probe108Certificate).get (by decide)
theorem probe108_erasure : probe108Checked.term = Term.i := by decide
theorem probe108_type : probe108Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2)))))))) := by decide
theorem probe108_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 2) (TypeCode.var 2)))))))) rho).accepts Term.i := by
  have h := checked_sound probe108Checked rho
  rw [probe108_type, probe108_erasure] at h
  exact h

-- Source JSON SHA256: 899688ac46e73836b3d4e842c79ecdceeea4306484145408d24e775b87086b32
def probe109Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 3))))))))
def probe109Checked : Checked := (check 0 probe109Certificate).get (by decide)
theorem probe109_erasure : probe109Checked.term = Term.i := by decide
theorem probe109_type : probe109Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3)))))))) := by decide
theorem probe109_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 3) (TypeCode.var 3)))))))) rho).accepts Term.i := by
  have h := checked_sound probe109Checked rho
  rw [probe109_type, probe109_erasure] at h
  exact h

-- Source JSON SHA256: 67afe9376d3e1406bfec6f1d4aa8d460c2a0277af821b4884f0b5bc78fdd62a2
def probe110Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 4))))))))
def probe110Checked : Checked := (check 0 probe110Certificate).get (by decide)
theorem probe110_erasure : probe110Checked.term = Term.i := by decide
theorem probe110_type : probe110Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4)))))))) := by decide
theorem probe110_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 4) (TypeCode.var 4)))))))) rho).accepts Term.i := by
  have h := checked_sound probe110Checked rho
  rw [probe110_type, probe110_erasure] at h
  exact h

-- Source JSON SHA256: c85579e07e1e7ccbb25b65a96e3ef7412979ccce37b47cb9331be533b5718cbd
def probe111Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 5))))))))
def probe111Checked : Checked := (check 0 probe111Certificate).get (by decide)
theorem probe111_erasure : probe111Checked.term = Term.i := by decide
theorem probe111_type : probe111Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 5) (TypeCode.var 5)))))))) := by decide
theorem probe111_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 5) (TypeCode.var 5)))))))) rho).accepts Term.i := by
  have h := checked_sound probe111Checked rho
  rw [probe111_type, probe111_erasure] at h
  exact h

end OrthemologyV4Exports
