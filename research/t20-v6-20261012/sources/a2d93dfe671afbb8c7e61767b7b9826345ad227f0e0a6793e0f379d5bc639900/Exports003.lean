/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: 2fd88427e9d4f72b5454c1acd9237548c2ee8bec367777a374bb6abfa44e47f2
def probe48Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe48Checked : Checked := (check 0 probe48Certificate).get (by decide)
theorem probe48_erasure : probe48Checked.term = Term.s := by decide
theorem probe48_type : probe48Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe48_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe48Checked rho
  rw [probe48_type, probe48_erasure] at h
  exact h

-- Source JSON SHA256: 0a227763b7950421d4a64b2375f620610b2963ad231b69eba132e3f3356fdb20
def probe49Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe49Checked : Checked := (check 0 probe49Certificate).get (by decide)
theorem probe49_erasure : probe49Checked.term = Term.s := by decide
theorem probe49_type : probe49Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe49_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe49Checked rho
  rw [probe49_type, probe49_erasure] at h
  exact h

-- Source JSON SHA256: 4d1d8e68410dcb793f22c33bbf2cea18c5fb56d07bf7e20d41e7a6acf56218e7
def probe50Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe50Checked : Checked := (check 0 probe50Certificate).get (by decide)
theorem probe50_erasure : probe50Checked.term = Term.k := by decide
theorem probe50_type : probe50Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe50_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.k := by
  have h := checked_sound probe50Checked rho
  rw [probe50_type, probe50_erasure] at h
  exact h

-- Source JSON SHA256: 03af6a49a7e56b8411b5b543793b8ec6f7a433d5ac22b6482d204518dcecd04f
def probe51Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)
def probe51Checked : Checked := (check 0 probe51Certificate).get (by decide)
theorem probe51_erasure : probe51Checked.term = Term.s := by decide
theorem probe51_type : probe51Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) := by decide
theorem probe51_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe51Checked rho
  rw [probe51_type, probe51_erasure] at h
  exact h

-- Source JSON SHA256: c50f8b10a6d44c0a88783bfb510cf09d88bc27023774c6c413d873538a8ed71f
def probe52Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe52Checked : Checked := (check 0 probe52Certificate).get (by decide)
theorem probe52_erasure : probe52Checked.term = Term.s := by decide
theorem probe52_type : probe52Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe52_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe52Checked rho
  rw [probe52_type, probe52_erasure] at h
  exact h

-- Source JSON SHA256: f4862e02d8fe98ee5ff14f6cab3f678e314b870b7c300a3f27ecbed02a51c4b3
def probe53Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe53Checked : Checked := (check 0 probe53Certificate).get (by decide)
theorem probe53_erasure : probe53Checked.term = Term.s := by decide
theorem probe53_type : probe53Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe53_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe53Checked rho
  rw [probe53_type, probe53_erasure] at h
  exact h

-- Source JSON SHA256: 5241c33428c6d6b0d0af4b96464c212d4d919f7a556758eef9f565fba8cdcfd7
def probe54Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)
def probe54Checked : Checked := (check 0 probe54Certificate).get (by decide)
theorem probe54_erasure : probe54Checked.term = Term.k := by decide
theorem probe54_type : probe54Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe54_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.k := by
  have h := checked_sound probe54Checked rho
  rw [probe54_type, probe54_erasure] at h
  exact h

-- Source JSON SHA256: 26355a3044c84de06771c4c97568f9fb3515ccdedffc6f8790d3d25e9c0048ac
def probe55Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom TypeCode.bottom)
def probe55Checked : Checked := (check 0 probe55Certificate).get (by decide)
theorem probe55_erasure : probe55Checked.term = Term.s := by decide
theorem probe55_type : probe55Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) := by decide
theorem probe55_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe55Checked rho
  rw [probe55_type, probe55_erasure] at h
  exact h

-- Source JSON SHA256: 3903e672a30b5148b492dad5bf97b57d1f908f68f6d877060554fe20cac686b6
def probe56Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe56Checked : Checked := (check 0 probe56Certificate).get (by decide)
theorem probe56_erasure : probe56Checked.term = Term.s := by decide
theorem probe56_type : probe56Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe56_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe56Checked rho
  rw [probe56_type, probe56_erasure] at h
  exact h

-- Source JSON SHA256: a010c5dd4511472bd7091a11c981542e9118031a4c375d2c13703fdbd83e314b
def probe57Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe57Checked : Checked := (check 0 probe57Certificate).get (by decide)
theorem probe57_erasure : probe57Checked.term = Term.s := by decide
theorem probe57_type : probe57Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe57_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow TypeCode.bottom (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe57Checked rho
  rw [probe57_type, probe57_erasure] at h
  exact h

-- Source JSON SHA256: 56b1f0292a05876aa2e196c438588d0435eecd067ffedfb0155a7727e4ce4a0f
def probe58Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe58Checked : Checked := (check 0 probe58Certificate).get (by decide)
theorem probe58_erasure : probe58Checked.term = Term.k := by decide
theorem probe58_type : probe58Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe58_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.k := by
  have h := checked_sound probe58Checked rho
  rw [probe58_type, probe58_erasure] at h
  exact h

-- Source JSON SHA256: e58b0c0e9b272b730740e1a3d1b8f31c2149203922a55ba97c4ad8844f5d6ffe
def probe59Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)
def probe59Checked : Checked := (check 0 probe59Certificate).get (by decide)
theorem probe59_erasure : probe59Checked.term = Term.s := by decide
theorem probe59_type : probe59Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) := by decide
theorem probe59_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe59Checked rho
  rw [probe59_type, probe59_erasure] at h
  exact h

-- Source JSON SHA256: 5e3f8bb9df104ac61fe6d26599656fb0085a29f51e65bf5f8319e3fab3e4d767
def probe60Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe60Checked : Checked := (check 0 probe60Certificate).get (by decide)
theorem probe60_erasure : probe60Checked.term = Term.s := by decide
theorem probe60_type : probe60Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe60_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.s := by
  have h := checked_sound probe60Checked rho
  rw [probe60_type, probe60_erasure] at h
  exact h

-- Source JSON SHA256: 96466dab047ee30bc881c42799fbc7197c3f246a3e58f6692c343d2714770178
def probe61Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe61Checked : Checked := (check 0 probe61Certificate).get (by decide)
theorem probe61_erasure : probe61Checked.term = Term.s := by decide
theorem probe61_type : probe61Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) := by decide
theorem probe61_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) rho).accepts Term.s := by
  have h := checked_sound probe61Checked rho
  rw [probe61_type, probe61_erasure] at h
  exact h

-- Source JSON SHA256: 12a983b2ad6cb22bf89e175e6aff46be52d173dce202bb377e4717fcc9774c3d
def probe62Certificate : Cert := (Cert.k (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe62Checked : Checked := (check 0 probe62Certificate).get (by decide)
theorem probe62_erasure : probe62Checked.term = Term.k := by decide
theorem probe62_type : probe62Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe62_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.k := by
  have h := checked_sound probe62Checked rho
  rw [probe62_type, probe62_erasure] at h
  exact h

-- Source JSON SHA256: c5b3216a8bb93292bfd47a241b78774ab86db16a2ec44075e6f1c1da38815890
def probe63Certificate : Cert := (Cert.s (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)
def probe63Checked : Checked := (check 0 probe63Certificate).get (by decide)
theorem probe63_erasure : probe63Checked.term = Term.s := by decide
theorem probe63_type : probe63Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) := by decide
theorem probe63_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom)) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) TypeCode.bottom))) rho).accepts Term.s := by
  have h := checked_sound probe63Checked rho
  rw [probe63_type, probe63_erasure] at h
  exact h

end OrthemologyV4Exports
