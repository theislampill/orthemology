/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: 4af4c82dec4f9a83680b428a1f8cdc02a68682a4e927f4372d769fba4fe20dd6
def probe80Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))))))
def probe80Checked : Checked := (check 0 probe80Certificate).get (by decide)
theorem probe80_erasure : probe80Checked.term = Term.i := by decide
theorem probe80_type : probe80Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe80_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe80Checked rho
  rw [probe80_type, probe80_erasure] at h
  exact h

-- Source JSON SHA256: 7105aab1f828e09e968751cb19c523dfdcfc463b6b8fa0382749858cb438f32f
def probe81Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))))))))
def probe81Checked : Checked := (check 0 probe81Certificate).get (by decide)
theorem probe81_erasure : probe81Checked.term = Term.i := by decide
theorem probe81_type : probe81Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe81_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe81Checked rho
  rw [probe81_type, probe81_erasure] at h
  exact h

-- Source JSON SHA256: 8658aee34ea1d7db784cf63507d497a128ca71d6d4ffea33d5a932dc72c93ef8
def probe82Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))))
def probe82Checked : Checked := (check 0 probe82Certificate).get (by decide)
theorem probe82_erasure : probe82Checked.term = Term.i := by decide
theorem probe82_type : probe82Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe82_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe82Checked rho
  rw [probe82_type, probe82_erasure] at h
  exact h

-- Source JSON SHA256: 0acfad095287d816ccd418b99c8658355a10b29cdd9517f3059470623a1aac5a
def probe83Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))))))))
def probe83Checked : Checked := (check 0 probe83Certificate).get (by decide)
theorem probe83_erasure : probe83Checked.term = Term.i := by decide
theorem probe83_type : probe83Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe83_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe83Checked rho
  rw [probe83_type, probe83_erasure] at h
  exact h

-- Source JSON SHA256: 2dde0bc4201dc738d110c8438ad8ea501901603bc9e6f2701fed74a1d8d71bf9
def probe84Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))))))
def probe84Checked : Checked := (check 0 probe84Certificate).get (by decide)
theorem probe84_erasure : probe84Checked.term = Term.i := by decide
theorem probe84_type : probe84Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe84_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe84Checked rho
  rw [probe84_type, probe84_erasure] at h
  exact h

-- Source JSON SHA256: c98a3bd175cbb68efe89ebb444d1c6bb0bb67dcb64ff24b9e4f8ec3c6c6c5302
def probe85Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))))))))
def probe85Checked : Checked := (check 0 probe85Certificate).get (by decide)
theorem probe85_erasure : probe85Checked.term = Term.i := by decide
theorem probe85_type : probe85Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe85_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe85Checked rho
  rw [probe85_type, probe85_erasure] at h
  exact h

-- Source JSON SHA256: aab708f8c37f7edb559acdd3f3b4cfbb27ff6a6acbd4318263f1f6ad18989cd8
def probe86Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))))))))))
def probe86Checked : Checked := (check 0 probe86Certificate).get (by decide)
theorem probe86_erasure : probe86Checked.term = Term.i := by decide
theorem probe86_type : probe86Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe86_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe86Checked rho
  rw [probe86_type, probe86_erasure] at h
  exact h

-- Source JSON SHA256: 1ce07812a7b4ebe118a45245bce0c87c72405479fd74bb0ecf3864344cd47c19
def probe87Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))))))
def probe87Checked : Checked := (check 0 probe87Certificate).get (by decide)
theorem probe87_erasure : probe87Checked.term = Term.i := by decide
theorem probe87_type : probe87Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe87_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe87Checked rho
  rw [probe87_type, probe87_erasure] at h
  exact h

-- Source JSON SHA256: 283429265b85fd7d785b9904fa5e8e461552f9e4276a5fd4ace94f8500fd1602
def probe88Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))))))))))
def probe88Checked : Checked := (check 0 probe88Certificate).get (by decide)
theorem probe88_erasure : probe88Checked.term = Term.i := by decide
theorem probe88_type : probe88Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe88_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe88Checked rho
  rw [probe88_type, probe88_erasure] at h
  exact h

-- Source JSON SHA256: 3654c1d1ca99b712f23b33d609a93a19edb9687e10df9ec65d7ae5b1c01d92c4
def probe89Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))))))))))
def probe89Checked : Checked := (check 0 probe89Certificate).get (by decide)
theorem probe89_erasure : probe89Checked.term = Term.i := by decide
theorem probe89_type : probe89Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe89_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe89Checked rho
  rw [probe89_type, probe89_erasure] at h
  exact h

-- Source JSON SHA256: 5e13de57adca3e9741f1772ae08d45a899fa3d2a7e42f017c1e2e2a86f761abd
def probe90Certificate : Cert := (Cert.step (Cert.step (Cert.step (Cert.step (Cert.step (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))))))))))
def probe90Checked : Checked := (check 0 probe90Certificate).get (by decide)
theorem probe90_erasure : probe90Checked.term = Term.i := by decide
theorem probe90_type : probe90Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe90_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe90Checked rho
  rw [probe90_type, probe90_erasure] at h
  exact h

-- Source JSON SHA256: cc86ddf29c1a214f2919234728b818cd18c6cf052f76bf56c3874af698908444
def probe91Certificate : Cert := (Cert.allI (Cert.i (TypeCode.var 0)))
def probe91Checked : Checked := (check 0 probe91Certificate).get (by decide)
theorem probe91_erasure : probe91Checked.term = Term.i := by decide
theorem probe91_type : probe91Checked.ty = (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) := by decide
theorem probe91_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) rho).accepts Term.i := by
  have h := checked_sound probe91Checked rho
  rw [probe91_type, probe91_erasure] at h
  exact h

-- Source JSON SHA256: 0f5642c0ac5df2263f7687dbf16d800b2ea7814688e88b61f6f18f2868db2d4e
def probe92Certificate : Cert := (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0))))
def probe92Checked : Checked := (check 0 probe92Certificate).get (by decide)
theorem probe92_erasure : probe92Checked.term = Term.i := by decide
theorem probe92_type : probe92Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe92_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe92Checked rho
  rw [probe92_type, probe92_erasure] at h
  exact h

-- Source JSON SHA256: fc3c0dc5ee45b2504e1c7207f97380163f10a4c3af1aa841202f1b1061f799bd
def probe93Certificate : Cert := (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1))))
def probe93Checked : Checked := (check 0 probe93Certificate).get (by decide)
theorem probe93_erasure : probe93Checked.term = Term.i := by decide
theorem probe93_type : probe93Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))) := by decide
theorem probe93_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1)))) rho).accepts Term.i := by
  have h := checked_sound probe93Checked rho
  rw [probe93_type, probe93_erasure] at h
  exact h

-- Source JSON SHA256: fcfa8b76854329b3ee9816f117cd3c9e43148ef2e3ff1e23f2ae995f8cb353ba
def probe94Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 0)))))
def probe94Checked : Checked := (check 0 probe94Certificate).get (by decide)
theorem probe94_erasure : probe94Checked.term = Term.i := by decide
theorem probe94_type : probe94Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe94_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe94Checked rho
  rw [probe94_type, probe94_erasure] at h
  exact h

-- Source JSON SHA256: 1aff33d10ddecc3c14bee66cf654a27b9dd7b5efc75c9ae4a9cbabf673f8486e
def probe95Certificate : Cert := (Cert.allI (Cert.allI (Cert.allI (Cert.i (TypeCode.var 1)))))
def probe95Checked : Checked := (check 0 probe95Certificate).get (by decide)
theorem probe95_erasure : probe95Checked.term = Term.i := by decide
theorem probe95_type : probe95Checked.ty = (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))) := by decide
theorem probe95_sound (rho : Nat → Code) : (interpret (TypeCode.all (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 1))))) rho).accepts Term.i := by
  have h := checked_sound probe95Checked rho
  rw [probe95_type, probe95_erasure] at h
  exact h

end OrthemologyV4Exports
