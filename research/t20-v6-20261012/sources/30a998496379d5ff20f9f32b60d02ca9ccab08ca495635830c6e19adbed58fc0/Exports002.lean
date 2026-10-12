/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: efb0f1a1c6a0376d1499540c157bd1a47151623a9a86180ac7b4ac23898a2199
def probe32Certificate : Cert := (Cert.s TypeCode.bottom TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe32Checked : Checked := (check 0 probe32Certificate).get (by decide)
theorem probe32_erasure : probe32Checked.term = Term.s := by decide
theorem probe32_type : probe32Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe32_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe32Checked rho
  rw [probe32_type, probe32_erasure] at h
  exact h

-- Source JSON SHA256: aeedfe46fbc56b53cca7f56aa17ceb9173c0a48ea84b89e8b3f4f3c3d0ca3e74
def probe33Certificate : Cert := (Cert.s TypeCode.bottom TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe33Checked : Checked := (check 0 probe33Certificate).get (by decide)
theorem probe33_erasure : probe33Checked.term = Term.s := by decide
theorem probe33_type : probe33Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe33_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom TypeCode.bottom) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe33Checked rho
  rw [probe33_type, probe33_erasure] at h
  exact h

-- Source JSON SHA256: 13eb38cb0b013035d5229d24a38b24677f186c0471a0b04b1b130ab65b3fd81a
def probe34Certificate : Cert := (Cert.k TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe34Checked : Checked := (check 0 probe34Certificate).get (by decide)
theorem probe34_erasure : probe34Checked.term = Term.k := by decide
theorem probe34_type : probe34Checked.ty = (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) := by decide
theorem probe34_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) rho).accepts Term.k := by
  have h := checked_sound probe34Checked rho
  rw [probe34_type, probe34_erasure] at h
  exact h

-- Source JSON SHA256: ce734440243c0145345fd3f36dcc13bfbd6d9163350d717c1de7e3e360f34bd2
def probe35Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)
def probe35Checked : Checked := (check 0 probe35Certificate).get (by decide)
theorem probe35_erasure : probe35Checked.term = Term.s := by decide
theorem probe35_type : probe35Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by decide
theorem probe35_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe35Checked rho
  rw [probe35_type, probe35_erasure] at h
  exact h

-- Source JSON SHA256: 6f008e52f98b5f1b387be483287b633d2dd15e28e48d3f139cfe99a80e93c1e2
def probe36Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe36Checked : Checked := (check 0 probe36Certificate).get (by decide)
theorem probe36_erasure : probe36Checked.term = Term.s := by decide
theorem probe36_type : probe36Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe36_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe36Checked rho
  rw [probe36_type, probe36_erasure] at h
  exact h

-- Source JSON SHA256: 50f81e31664dac2c904666356b32f7c4dd3afbf55a636f6e0df06bbfba4e55c1
def probe37Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe37Checked : Checked := (check 0 probe37Certificate).get (by decide)
theorem probe37_erasure : probe37Checked.term = Term.s := by decide
theorem probe37_type : probe37Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe37_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe37Checked rho
  rw [probe37_type, probe37_erasure] at h
  exact h

-- Source JSON SHA256: ca106e1e82ed574fb843e48c58bdb7927a22b611002803aa686b6930c3b6ad71
def probe38Certificate : Cert := (Cert.k TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe38Checked : Checked := (check 0 probe38Certificate).get (by decide)
theorem probe38_erasure : probe38Checked.term = Term.k := by decide
theorem probe38_type : probe38Checked.ty = (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) := by decide
theorem probe38_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) rho).accepts Term.k := by
  have h := checked_sound probe38Checked rho
  rw [probe38_type, probe38_erasure] at h
  exact h

-- Source JSON SHA256: 2f9e0ea191c94806b15ea0c4d110a0bf8796b296c52d83c48108761ca1254334
def probe39Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)
def probe39Checked : Checked := (check 0 probe39Certificate).get (by decide)
theorem probe39_erasure : probe39Checked.term = Term.s := by decide
theorem probe39_type : probe39Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) := by decide
theorem probe39_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe39Checked rho
  rw [probe39_type, probe39_erasure] at h
  exact h

-- Source JSON SHA256: 2cc2bb2d7ea3eb32ca1d3c45cb7cce113fad776dd1407d090e1c6bb02a2e88fd
def probe40Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe40Checked : Checked := (check 0 probe40Certificate).get (by decide)
theorem probe40_erasure : probe40Checked.term = Term.s := by decide
theorem probe40_type : probe40Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe40_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe40Checked rho
  rw [probe40_type, probe40_erasure] at h
  exact h

-- Source JSON SHA256: 74ea38779fc777197e16916127d97b843dc44cd4ecc39426cae5b710a8d5edb6
def probe41Certificate : Cert := (Cert.s TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe41Checked : Checked := (check 0 probe41Certificate).get (by decide)
theorem probe41_erasure : probe41Checked.term = Term.s := by decide
theorem probe41_type : probe41Checked.ty = (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe41_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe41Checked rho
  rw [probe41_type, probe41_erasure] at h
  exact h

-- Source JSON SHA256: 6c18fa02df1f42e15eb65d60d2ce2e949e1b687e629319102c7f178d5e78314d
def probe42Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)
def probe42Checked : Checked := (check 0 probe42Certificate).get (by decide)
theorem probe42_erasure : probe42Checked.term = Term.k := by decide
theorem probe42_type : probe42Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe42_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.k := by
  have h := checked_sound probe42Checked rho
  rw [probe42_type, probe42_erasure] at h
  exact h

-- Source JSON SHA256: 72bfe6abca5e749f219ef907d5e236f8e7a96757ef37b7c691cac841d25ba0a9
def probe43Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom TypeCode.bottom)
def probe43Checked : Checked := (check 0 probe43Certificate).get (by decide)
theorem probe43_erasure : probe43Checked.term = Term.s := by decide
theorem probe43_type : probe43Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) := by decide
theorem probe43_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe43Checked rho
  rw [probe43_type, probe43_erasure] at h
  exact h

-- Source JSON SHA256: e156de1d94a010788499379a7b4b55119a414b45281ce4ddbf197b2c644db50f
def probe44Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe44Checked : Checked := (check 0 probe44Certificate).get (by decide)
theorem probe44_erasure : probe44Checked.term = Term.s := by decide
theorem probe44_type : probe44Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe44_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe44Checked rho
  rw [probe44_type, probe44_erasure] at h
  exact h

-- Source JSON SHA256: d009d5512944f599cf790e18a3b489bafbc97efe12ed3084f96f90108fc2c7b6
def probe45Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe45Checked : Checked := (check 0 probe45Certificate).get (by decide)
theorem probe45_erasure : probe45Checked.term = Term.s := by decide
theorem probe45_type : probe45Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe45_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe45Checked rho
  rw [probe45_type, probe45_erasure] at h
  exact h

-- Source JSON SHA256: d4ecd72f9c5ae8067bd3b724d33b2e8d6b5a28b4c50e332c950d189b00ba7699
def probe46Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe46Checked : Checked := (check 0 probe46Certificate).get (by decide)
theorem probe46_erasure : probe46Checked.term = Term.k := by decide
theorem probe46_type : probe46Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe46_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.k := by
  have h := checked_sound probe46Checked rho
  rw [probe46_type, probe46_erasure] at h
  exact h

-- Source JSON SHA256: afc3b969c3fe227a1d01ea8d91181e0ec470fa804c8357ec03c2b0fd2068e537
def probe47Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)
def probe47Checked : Checked := (check 0 probe47Certificate).get (by decide)
theorem probe47_erasure : probe47Checked.term = Term.s := by decide
theorem probe47_type : probe47Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) := by decide
theorem probe47_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe47Checked rho
  rw [probe47_type, probe47_erasure] at h
  exact h

end OrthemologyV4Exports
