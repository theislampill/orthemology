/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
-- Source JSON SHA256: 2a13c0f1dda613654d89559bf0dce2577b29865c3f568af1038593dcbdf9a695
def probe0Certificate : Cert := (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)
def probe0Checked : Checked := (check 0 probe0Certificate).get (by decide)
theorem probe0_erasure : probe0Checked.term = Term.i := by decide
theorem probe0_type : probe0Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe0_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts Term.i := by
  have h := checked_sound probe0Checked rho
  rw [probe0_type, probe0_erasure] at h
  exact h

-- Source JSON SHA256: 014abd0cf9bd60bc0bc59174ae126dbf4395a5a58d87783220aa518896eaf07f
def probe1Certificate : Cert := (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))
def probe1Checked : Checked := (check 0 probe1Certificate).get (by decide)
theorem probe1_erasure : probe1Checked.term = Term.i := by decide
theorem probe1_type : probe1Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe1_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts Term.i := by
  have h := checked_sound probe1Checked rho
  rw [probe1_type, probe1_erasure] at h
  exact h

-- Source JSON SHA256: b2d345a455a1302d1e14fb131530b05ed1b53c25669f3e4fb9675c5cfe8dd1d3
def probe2Certificate : Cert := (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe2Checked : Checked := (check 0 probe2Certificate).get (by decide)
theorem probe2_erasure : probe2Checked.term = Term.i := by decide
theorem probe2_type : probe2Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe2_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe2Checked rho
  rw [probe2_type, probe2_erasure] at h
  exact h

-- Source JSON SHA256: d06d1a084f8c5199df62e84e27e1852c5692a9880349298371113a0cdb26655d
def probe3Certificate : Cert := (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))
def probe3Checked : Checked := (check 0 probe3Certificate).get (by decide)
theorem probe3_erasure : probe3Checked.term = Term.i := by decide
theorem probe3_type : probe3Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe3_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts Term.i := by
  have h := checked_sound probe3Checked rho
  rw [probe3_type, probe3_erasure] at h
  exact h

-- Source JSON SHA256: 02cb8d9f6d54f23e20f806a5b4f63c93ad2b38f0e27bb1e67b112e5b0f1487e5
def probe4Certificate : Cert := (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))
def probe4Checked : Checked := (check 0 probe4Certificate).get (by decide)
theorem probe4_erasure : probe4Checked.term = Term.i := by decide
theorem probe4_type : probe4Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe4_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts Term.i := by
  have h := checked_sound probe4Checked rho
  rw [probe4_type, probe4_erasure] at h
  exact h

-- Source JSON SHA256: fcacf99c75324ecd38264dc368386de4c42cd009c83a1cfeee937681acdeeeb3
def probe5Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom))
def probe5Checked : Checked := (check 0 probe5Certificate).get (by decide)
theorem probe5_erasure : probe5Checked.term = (Term.app Term.i Term.i) := by decide
theorem probe5_type : probe5Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe5_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound probe5Checked rho
  rw [probe5_type, probe5_erasure] at h
  exact h

-- Source JSON SHA256: a732472cac3b0109c136a4f16f435c2f0ddab4e4a01e443a88caec9ede4ff6d9
def probe6Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))
def probe6Checked : Checked := (check 0 probe6Certificate).get (by decide)
theorem probe6_erasure : probe6Checked.term = (Term.app Term.i Term.i) := by decide
theorem probe6_type : probe6Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe6_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound probe6Checked rho
  rw [probe6_type, probe6_erasure] at h
  exact h

-- Source JSON SHA256: 96ff83ea8a2200ee82420f431949ce93d7f7b9465ee16e4e9079465424ac5f71
def probe7Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))
def probe7Checked : Checked := (check 0 probe7Certificate).get (by decide)
theorem probe7_erasure : probe7Checked.term = (Term.app Term.i Term.i) := by decide
theorem probe7_type : probe7Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe7_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound probe7Checked rho
  rw [probe7_type, probe7_erasure] at h
  exact h

-- Source JSON SHA256: 3f27a35f2bce09dcb5dc5cfd578d0ef18459cad4e850874243625c3ea5bc7455
def probe8Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))
def probe8Checked : Checked := (check 0 probe8Certificate).get (by decide)
theorem probe8_erasure : probe8Checked.term = (Term.app Term.i Term.i) := by decide
theorem probe8_type : probe8Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe8_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound probe8Checked rho
  rw [probe8_type, probe8_erasure] at h
  exact h

-- Source JSON SHA256: c28834265211e2ef15b96bc8d3fbd46399ecba5744c8dd492df8daf3464719be
def probe9Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))))
def probe9Checked : Checked := (check 0 probe9Certificate).get (by decide)
theorem probe9_erasure : probe9Checked.term = (Term.app Term.i Term.i) := by decide
theorem probe9_type : probe9Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe9_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts (Term.app Term.i Term.i) := by
  have h := checked_sound probe9Checked rho
  rw [probe9_type, probe9_erasure] at h
  exact h

-- Source JSON SHA256: f194de7ac68ab0bc7e21df14539038714db0fe49712c97d1d4352cc71288f62d
def probe10Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom)))
def probe10Checked : Checked := (check 0 probe10Certificate).get (by decide)
theorem probe10_erasure : probe10Checked.term = (Term.app Term.i (Term.app Term.i Term.i)) := by decide
theorem probe10_type : probe10Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe10_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts (Term.app Term.i (Term.app Term.i Term.i)) := by
  have h := checked_sound probe10Checked rho
  rw [probe10_type, probe10_erasure] at h
  exact h

-- Source JSON SHA256: 4e5ed85d49d2a65165c51ea6cf698f1dd2cd59c636fc87985ec36c76c1ef0e70
def probe11Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))
def probe11Checked : Checked := (check 0 probe11Certificate).get (by decide)
theorem probe11_erasure : probe11Checked.term = (Term.app Term.i (Term.app Term.i Term.i)) := by decide
theorem probe11_type : probe11Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) := by decide
theorem probe11_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) rho).accepts (Term.app Term.i (Term.app Term.i Term.i)) := by
  have h := checked_sound probe11Checked rho
  rw [probe11_type, probe11_erasure] at h
  exact h

-- Source JSON SHA256: 6b8ce0164ea6b9759b913c116f3b122841867dfc0df155aa9c66144a9b8f7dcc
def probe12Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))))
def probe12Checked : Checked := (check 0 probe12Certificate).get (by decide)
theorem probe12_erasure : probe12Checked.term = (Term.app Term.i (Term.app Term.i Term.i)) := by decide
theorem probe12_type : probe12Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) := by decide
theorem probe12_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) rho).accepts (Term.app Term.i (Term.app Term.i Term.i)) := by
  have h := checked_sound probe12Checked rho
  rw [probe12_type, probe12_erasure] at h
  exact h

-- Source JSON SHA256: b2b6b91de0ce2f6b02409e55a986d516a4e8c601976703da76d187d7a1ed5028
def probe13Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))))))
def probe13Checked : Checked := (check 0 probe13Certificate).get (by decide)
theorem probe13_erasure : probe13Checked.term = (Term.app Term.i (Term.app Term.i Term.i)) := by decide
theorem probe13_type : probe13Checked.ty = (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) := by decide
theorem probe13_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))))) (TypeCode.arrow (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0))) (TypeCode.all (TypeCode.arrow (TypeCode.var 0) (TypeCode.arrow (TypeCode.var 0) (TypeCode.var 0)))))) rho).accepts (Term.app Term.i (Term.app Term.i Term.i)) := by
  have h := checked_sound probe13Checked rho
  rw [probe13_type, probe13_erasure] at h
  exact h

-- Source JSON SHA256: ff377b76cd5bac493591da72615cb9f176ba179d2c6560e2204364a69a4701e8
def probe14Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))))))
def probe14Checked : Checked := (check 0 probe14Certificate).get (by decide)
theorem probe14_erasure : probe14Checked.term = (Term.app Term.i (Term.app Term.i Term.i)) := by decide
theorem probe14_type : probe14Checked.ty = (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) := by decide
theorem probe14_sound (rho : Nat → Code) : (interpret (TypeCode.arrow (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0)))) (TypeCode.all (TypeCode.all (TypeCode.arrow (TypeCode.var 1) (TypeCode.var 0))))) rho).accepts (Term.app Term.i (Term.app Term.i Term.i)) := by
  have h := checked_sound probe14Checked rho
  rw [probe14_type, probe14_erasure] at h
  exact h

-- Source JSON SHA256: b7a7de4353c5a8018ba38be7a31ddd41b74b91ac4eeacb51e6ee7dda41d0e4fa
def probe15Certificate : Cert := (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.app (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) (TypeCode.arrow TypeCode.bottom TypeCode.bottom)) (Cert.allE (Cert.allI (Cert.i (TypeCode.var 0))) TypeCode.bottom))))
def probe15Checked : Checked := (check 0 probe15Certificate).get (by decide)
theorem probe15_erasure : probe15Checked.term = (Term.app Term.i (Term.app Term.i (Term.app Term.i Term.i))) := by decide
theorem probe15_type : probe15Checked.ty = (TypeCode.arrow TypeCode.bottom TypeCode.bottom) := by decide
theorem probe15_sound (rho : Nat → Code) : (interpret (TypeCode.arrow TypeCode.bottom TypeCode.bottom) rho).accepts (Term.app Term.i (Term.app Term.i (Term.app Term.i Term.i))) := by
  have h := checked_sound probe15Checked rho
  rw [probe15_type, probe15_erasure] at h
  exact h

end OrthemologyV4Exports
