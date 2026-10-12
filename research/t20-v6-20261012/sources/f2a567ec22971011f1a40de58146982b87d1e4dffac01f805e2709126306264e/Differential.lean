import NumericMembership
open P02A2.FiniteOutputTable AtomicMembership

def testHeavy (e k n : ℕ) : ℚ≥0 :=
  rationalHeavyMass (indexTable e) k n

def batch0 : IO Nat := do
  let mut passed := 0
  if indexTable 406426676795557660890104064 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/word")
  if testHeavy 406426676795557660890104064 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy0")
  if testHeavy 406426676795557660890104064 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy1")
  if testHeavy 406426676795557660890104064 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy2")
  if testHeavy 406426676795557660890104064 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy3")
  if testHeavy 406426676795557660890104064 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy4")
  if testHeavy 406426676795557660890104064 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N0/heavy5")
  if indexTable 406426676795557660890104064 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/word0")
  if indexTable 406426676795557660890104064 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/word1")
  if testHeavy 406426676795557660890104064 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy0")
  if testHeavy 406426676795557660890104064 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy1")
  if testHeavy 406426676795557660890104064 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy2")
  if testHeavy 406426676795557660890104064 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy3")
  if testHeavy 406426676795557660890104064 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy4")
  if testHeavy 406426676795557660890104064 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N1/heavy5")
  if indexTable 406426676795557660890104064 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/word00")
  if indexTable 406426676795557660890104064 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/word01")
  if indexTable 406426676795557660890104064 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/word10")
  if indexTable 406426676795557660890104064 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/word11")
  if testHeavy 406426676795557660890104064 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy0")
  if testHeavy 406426676795557660890104064 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy1")
  if testHeavy 406426676795557660890104064 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy2")
  if testHeavy 406426676795557660890104064 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy3")
  if testHeavy 406426676795557660890104064 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy4")
  if testHeavy 406426676795557660890104064 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N2/heavy5")
  if indexTable 406426676795557660890104064 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word000")
  if indexTable 406426676795557660890104064 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word001")
  if indexTable 406426676795557660890104064 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word010")
  if indexTable 406426676795557660890104064 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word011")
  if indexTable 406426676795557660890104064 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word100")
  if indexTable 406426676795557660890104064 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word101")
  if indexTable 406426676795557660890104064 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word110")
  if indexTable 406426676795557660890104064 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/word111")
  if testHeavy 406426676795557660890104064 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy0")
  if testHeavy 406426676795557660890104064 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy1")
  if testHeavy 406426676795557660890104064 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy2")
  if testHeavy 406426676795557660890104064 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy3")
  if testHeavy 406426676795557660890104064 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy4")
  if testHeavy 406426676795557660890104064 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N3/heavy5")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0000")
  return passed

def batch1 : IO Nat := do
  let mut passed := 0
  if indexTable 406426676795557660890104064 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0001")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0010")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0011")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0100")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0101")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0110")
  if indexTable 406426676795557660890104064 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word0111")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1000")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1001")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1010")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1011")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1100")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1101")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1110")
  if indexTable 406426676795557660890104064 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/word1111")
  if testHeavy 406426676795557660890104064 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/0-1/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-2/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-4/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-1/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-2/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/4-0/k0")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/2-4/k0")
  if testHeavy 406426676795557660890104064 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/0-1/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-2/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-4/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-1/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-2/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/4-0/k1")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/2-4/k1")
  if testHeavy 406426676795557660890104064 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy2")
  if testHeavy 406426676795557660890104064 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy3")
  if testHeavy 406426676795557660890104064 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/0-1/k4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-2/k4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-4/k4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/1-1/k4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/3-2/k4")
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/4-0/k4")
  return passed

def batch2 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 406426676795557660890104064 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/matrix/2-4/k4")
  if testHeavy 406426676795557660890104064 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero/N4/heavy5")
  if indexTable 406426676795557660890104065 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/word")
  if testHeavy 406426676795557660890104065 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy0")
  if testHeavy 406426676795557660890104065 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy1")
  if testHeavy 406426676795557660890104065 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy2")
  if testHeavy 406426676795557660890104065 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy3")
  if testHeavy 406426676795557660890104065 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy4")
  if testHeavy 406426676795557660890104065 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N0/heavy5")
  if indexTable 406426676795557660890104065 1 (fun i => #[false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/word0")
  if indexTable 406426676795557660890104065 1 (fun i => #[true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/word1")
  if testHeavy 406426676795557660890104065 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy0")
  if testHeavy 406426676795557660890104065 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy1")
  if testHeavy 406426676795557660890104065 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy2")
  if testHeavy 406426676795557660890104065 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy3")
  if testHeavy 406426676795557660890104065 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy4")
  if testHeavy 406426676795557660890104065 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N1/heavy5")
  if indexTable 406426676795557660890104065 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/word00")
  if indexTable 406426676795557660890104065 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/word01")
  if indexTable 406426676795557660890104065 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/word10")
  if indexTable 406426676795557660890104065 2 (fun i => #[true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/word11")
  if testHeavy 406426676795557660890104065 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy0")
  if testHeavy 406426676795557660890104065 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy1")
  if testHeavy 406426676795557660890104065 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy2")
  if testHeavy 406426676795557660890104065 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy3")
  if testHeavy 406426676795557660890104065 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy4")
  if testHeavy 406426676795557660890104065 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N2/heavy5")
  if indexTable 406426676795557660890104065 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word000")
  if indexTable 406426676795557660890104065 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word001")
  if indexTable 406426676795557660890104065 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word010")
  if indexTable 406426676795557660890104065 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word011")
  if indexTable 406426676795557660890104065 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word100")
  if indexTable 406426676795557660890104065 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word101")
  if indexTable 406426676795557660890104065 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word110")
  if indexTable 406426676795557660890104065 3 (fun i => #[true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/word111")
  if testHeavy 406426676795557660890104065 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy0")
  if testHeavy 406426676795557660890104065 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy1")
  if testHeavy 406426676795557660890104065 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy2")
  if testHeavy 406426676795557660890104065 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy3")
  if testHeavy 406426676795557660890104065 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy4")
  return passed

def batch3 : IO Nat := do
  let mut passed := 0
  if testHeavy 406426676795557660890104065 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N3/heavy5")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0000")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0001")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0010")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0011")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0100")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0101")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0110")
  if indexTable 406426676795557660890104065 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word0111")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1000")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1001")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1010")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1011")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1100")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1101")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1110")
  if indexTable 406426676795557660890104065 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/word1111")
  if testHeavy 406426676795557660890104065 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/0-1/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-2/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-4/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-1/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-2/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/4-0/k0")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/2-4/k0")
  if testHeavy 406426676795557660890104065 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/0-1/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-2/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-4/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-1/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-2/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/4-0/k1")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/2-4/k1")
  if testHeavy 406426676795557660890104065 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy2")
  if testHeavy 406426676795557660890104065 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy3")
  if testHeavy 406426676795557660890104065 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/0-1/k4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-2/k4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-4/k4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/1-1/k4")
  return passed

def batch4 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/3-2/k4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/4-0/k4")
  if decide (membershipMatrix 406426676795557660890104065 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/matrix/2-4/k4")
  if testHeavy 406426676795557660890104065 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL one/N4/heavy5")
  if indexTable 6201578930596277719296 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/word")
  if testHeavy 6201578930596277719296 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy0")
  if testHeavy 6201578930596277719296 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy1")
  if testHeavy 6201578930596277719296 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy2")
  if testHeavy 6201578930596277719296 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy3")
  if testHeavy 6201578930596277719296 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy4")
  if testHeavy 6201578930596277719296 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N0/heavy5")
  if indexTable 6201578930596277719296 1 (fun i => #[false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/word0")
  if indexTable 6201578930596277719296 1 (fun i => #[true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/word1")
  if testHeavy 6201578930596277719296 0 1 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy0")
  if testHeavy 6201578930596277719296 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy1")
  if testHeavy 6201578930596277719296 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy2")
  if testHeavy 6201578930596277719296 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy3")
  if testHeavy 6201578930596277719296 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy4")
  if testHeavy 6201578930596277719296 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N1/heavy5")
  if indexTable 6201578930596277719296 2 (fun i => #[false, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/word00")
  if indexTable 6201578930596277719296 2 (fun i => #[false, true][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/word01")
  if indexTable 6201578930596277719296 2 (fun i => #[true, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/word10")
  if indexTable 6201578930596277719296 2 (fun i => #[true, true][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/word11")
  if testHeavy 6201578930596277719296 0 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy0")
  if testHeavy 6201578930596277719296 1 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy1")
  if testHeavy 6201578930596277719296 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy2")
  if testHeavy 6201578930596277719296 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy3")
  if testHeavy 6201578930596277719296 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy4")
  if testHeavy 6201578930596277719296 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N2/heavy5")
  if indexTable 6201578930596277719296 3 (fun i => #[false, false, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word000")
  if indexTable 6201578930596277719296 3 (fun i => #[false, false, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word001")
  if indexTable 6201578930596277719296 3 (fun i => #[false, true, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word010")
  if indexTable 6201578930596277719296 3 (fun i => #[false, true, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word011")
  if indexTable 6201578930596277719296 3 (fun i => #[true, false, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word100")
  if indexTable 6201578930596277719296 3 (fun i => #[true, false, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word101")
  if indexTable 6201578930596277719296 3 (fun i => #[true, true, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word110")
  if indexTable 6201578930596277719296 3 (fun i => #[true, true, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/word111")
  if testHeavy 6201578930596277719296 0 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy0")
  if testHeavy 6201578930596277719296 1 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy1")
  if testHeavy 6201578930596277719296 2 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy2")
  return passed

def batch5 : IO Nat := do
  let mut passed := 0
  if testHeavy 6201578930596277719296 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy3")
  if testHeavy 6201578930596277719296 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy4")
  if testHeavy 6201578930596277719296 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N3/heavy5")
  if indexTable 6201578930596277719296 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0000")
  if indexTable 6201578930596277719296 4 (fun i => #[false, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0001")
  if indexTable 6201578930596277719296 4 (fun i => #[false, false, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0010")
  if indexTable 6201578930596277719296 4 (fun i => #[false, false, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0011")
  if indexTable 6201578930596277719296 4 (fun i => #[false, true, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0100")
  if indexTable 6201578930596277719296 4 (fun i => #[false, true, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0101")
  if indexTable 6201578930596277719296 4 (fun i => #[false, true, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0110")
  if indexTable 6201578930596277719296 4 (fun i => #[false, true, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word0111")
  if indexTable 6201578930596277719296 4 (fun i => #[true, false, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1000")
  if indexTable 6201578930596277719296 4 (fun i => #[true, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1001")
  if indexTable 6201578930596277719296 4 (fun i => #[true, false, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1010")
  if indexTable 6201578930596277719296 4 (fun i => #[true, false, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1011")
  if indexTable 6201578930596277719296 4 (fun i => #[true, true, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1100")
  if indexTable 6201578930596277719296 4 (fun i => #[true, true, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1101")
  if indexTable 6201578930596277719296 4 (fun i => #[true, true, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1110")
  if indexTable 6201578930596277719296 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/word1111")
  if testHeavy 6201578930596277719296 0 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/0-1/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 2) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-2/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-4/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-1/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-2/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/4-0/k0")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 2 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/2-4/k0")
  if testHeavy 6201578930596277719296 1 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/0-1/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 2) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-2/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-4/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-1/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-2/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/4-0/k1")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 2 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/2-4/k1")
  if testHeavy 6201578930596277719296 2 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy2")
  if testHeavy 6201578930596277719296 3 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy3")
  if testHeavy 6201578930596277719296 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/0-1/k4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-2/k4")
  return passed

def batch6 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-4/k4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/1-1/k4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/3-2/k4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/4-0/k4")
  if decide (membershipMatrix 6201578930596277719296 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/matrix/2-4/k4")
  if testHeavy 6201578930596277719296 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_bit/N4/heavy5")
  if indexTable 1745589285058882231605260711082197504 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/word")
  if testHeavy 1745589285058882231605260711082197504 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy0")
  if testHeavy 1745589285058882231605260711082197504 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy1")
  if testHeavy 1745589285058882231605260711082197504 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy2")
  if testHeavy 1745589285058882231605260711082197504 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy3")
  if testHeavy 1745589285058882231605260711082197504 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy4")
  if testHeavy 1745589285058882231605260711082197504 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N0/heavy5")
  if indexTable 1745589285058882231605260711082197504 1 (fun i => #[false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/word0")
  if indexTable 1745589285058882231605260711082197504 1 (fun i => #[true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/word1")
  if testHeavy 1745589285058882231605260711082197504 0 1 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy0")
  if testHeavy 1745589285058882231605260711082197504 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy1")
  if testHeavy 1745589285058882231605260711082197504 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy2")
  if testHeavy 1745589285058882231605260711082197504 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy3")
  if testHeavy 1745589285058882231605260711082197504 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy4")
  if testHeavy 1745589285058882231605260711082197504 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N1/heavy5")
  if indexTable 1745589285058882231605260711082197504 2 (fun i => #[false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/word00")
  if indexTable 1745589285058882231605260711082197504 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/word01")
  if indexTable 1745589285058882231605260711082197504 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/word10")
  if indexTable 1745589285058882231605260711082197504 2 (fun i => #[true, true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/word11")
  if testHeavy 1745589285058882231605260711082197504 0 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy0")
  if testHeavy 1745589285058882231605260711082197504 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy1")
  if testHeavy 1745589285058882231605260711082197504 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy2")
  if testHeavy 1745589285058882231605260711082197504 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy3")
  if testHeavy 1745589285058882231605260711082197504 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy4")
  if testHeavy 1745589285058882231605260711082197504 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N2/heavy5")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[false, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word000")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word001")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word010")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word011")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word100")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word101")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word110")
  if indexTable 1745589285058882231605260711082197504 3 (fun i => #[true, true, true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/word111")
  if testHeavy 1745589285058882231605260711082197504 0 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy0")
  return passed

def batch7 : IO Nat := do
  let mut passed := 0
  if testHeavy 1745589285058882231605260711082197504 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy1")
  if testHeavy 1745589285058882231605260711082197504 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy2")
  if testHeavy 1745589285058882231605260711082197504 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy3")
  if testHeavy 1745589285058882231605260711082197504 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy4")
  if testHeavy 1745589285058882231605260711082197504 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N3/heavy5")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0000")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0001")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0010")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0011")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0100")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0101")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0110")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word0111")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1000")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1001")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1010")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1011")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1100")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1101")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1110")
  if indexTable 1745589285058882231605260711082197504 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/word1111")
  if testHeavy 1745589285058882231605260711082197504 0 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/0-1/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 2) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-2/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-4/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-1/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-2/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/4-0/k0")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 2 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/2-4/k0")
  if testHeavy 1745589285058882231605260711082197504 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/0-1/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-2/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-4/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-1/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-2/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/4-0/k1")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/2-4/k1")
  if testHeavy 1745589285058882231605260711082197504 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy2")
  if testHeavy 1745589285058882231605260711082197504 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy3")
  if testHeavy 1745589285058882231605260711082197504 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy4")
  return passed

def batch8 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/0-1/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-2/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-4/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/1-1/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/3-2/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/4-0/k4")
  if decide (membershipMatrix 1745589285058882231605260711082197504 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/matrix/2-4/k4")
  if testHeavy 1745589285058882231605260711082197504 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL first_bit/N4/heavy5")
  if indexTable 6201578930596277653760 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/word")
  if testHeavy 6201578930596277653760 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy0")
  if testHeavy 6201578930596277653760 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy1")
  if testHeavy 6201578930596277653760 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy2")
  if testHeavy 6201578930596277653760 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy3")
  if testHeavy 6201578930596277653760 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy4")
  if testHeavy 6201578930596277653760 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N0/heavy5")
  if indexTable 6201578930596277653760 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/word0")
  if indexTable 6201578930596277653760 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/word1")
  if testHeavy 6201578930596277653760 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy0")
  if testHeavy 6201578930596277653760 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy1")
  if testHeavy 6201578930596277653760 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy2")
  if testHeavy 6201578930596277653760 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy3")
  if testHeavy 6201578930596277653760 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy4")
  if testHeavy 6201578930596277653760 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N1/heavy5")
  if indexTable 6201578930596277653760 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/word00")
  if indexTable 6201578930596277653760 2 (fun i => #[false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/word01")
  if indexTable 6201578930596277653760 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/word10")
  if indexTable 6201578930596277653760 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/word11")
  if testHeavy 6201578930596277653760 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy0")
  if testHeavy 6201578930596277653760 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy1")
  if testHeavy 6201578930596277653760 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy2")
  if testHeavy 6201578930596277653760 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy3")
  if testHeavy 6201578930596277653760 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy4")
  if testHeavy 6201578930596277653760 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N2/heavy5")
  if indexTable 6201578930596277653760 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word000")
  if indexTable 6201578930596277653760 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word001")
  if indexTable 6201578930596277653760 3 (fun i => #[false, true, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word010")
  if indexTable 6201578930596277653760 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word011")
  if indexTable 6201578930596277653760 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word100")
  if indexTable 6201578930596277653760 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word101")
  if indexTable 6201578930596277653760 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word110")
  return passed

def batch9 : IO Nat := do
  let mut passed := 0
  if indexTable 6201578930596277653760 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/word111")
  if testHeavy 6201578930596277653760 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy0")
  if testHeavy 6201578930596277653760 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy1")
  if testHeavy 6201578930596277653760 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy2")
  if testHeavy 6201578930596277653760 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy3")
  if testHeavy 6201578930596277653760 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy4")
  if testHeavy 6201578930596277653760 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N3/heavy5")
  if indexTable 6201578930596277653760 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0000")
  if indexTable 6201578930596277653760 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0001")
  if indexTable 6201578930596277653760 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0010")
  if indexTable 6201578930596277653760 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0011")
  if indexTable 6201578930596277653760 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0100")
  if indexTable 6201578930596277653760 4 (fun i => #[false, true, false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0101")
  if indexTable 6201578930596277653760 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0110")
  if indexTable 6201578930596277653760 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word0111")
  if indexTable 6201578930596277653760 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1000")
  if indexTable 6201578930596277653760 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1001")
  if indexTable 6201578930596277653760 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1010")
  if indexTable 6201578930596277653760 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1011")
  if indexTable 6201578930596277653760 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1100")
  if indexTable 6201578930596277653760 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1101")
  if indexTable 6201578930596277653760 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1110")
  if indexTable 6201578930596277653760 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/word1111")
  if testHeavy 6201578930596277653760 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/0-1/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-2/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-4/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-1/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-2/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/4-0/k0")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/2-4/k0")
  if testHeavy 6201578930596277653760 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/0-1/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-2/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-4/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-1/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-2/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/4-0/k1")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/2-4/k1")
  if testHeavy 6201578930596277653760 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy2")
  return passed

def batch10 : IO Nat := do
  let mut passed := 0
  if testHeavy 6201578930596277653760 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy3")
  if testHeavy 6201578930596277653760 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/0-1/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-2/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-4/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/1-1/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/3-2/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/4-0/k4")
  if decide (membershipMatrix 6201578930596277653760 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/matrix/2-4/k4")
  if testHeavy 6201578930596277653760 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL stage_parity/N4/heavy5")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/word")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy0")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy2")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy3")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy4")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N0/heavy5")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 (fun i => #[false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/word0")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 (fun i => #[true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/word1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 1 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy0")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy2")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy3")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy4")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N1/heavy5")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 (fun i => #[false, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/word00")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 (fun i => #[false, true][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/word01")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 (fun i => #[true, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/word10")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 (fun i => #[true, true][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/word11")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy0")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy2")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy3")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy4")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N2/heavy5")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[false, false, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word000")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[false, false, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word001")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[false, true, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word010")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[false, true, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word011")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[true, false, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word100")
  return passed

def batch11 : IO Nat := do
  let mut passed := 0
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[true, false, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word101")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[true, true, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word110")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 (fun i => #[true, true, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/word111")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy0")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy2")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy3")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy4")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N3/heavy5")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0000")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0001")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, false, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0010")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, false, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0011")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, true, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0100")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, true, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0101")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, true, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0110")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[false, true, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word0111")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, false, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1000")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1001")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, false, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1010")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, false, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1011")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, true, false, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1100")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, true, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1101")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, true, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1110")
  if indexTable 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/word1111")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 0 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/0-1/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 2) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-2/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-4/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-1/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-2/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/4-0/k0")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 2 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/2-4/k0")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 1 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/0-1/k1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 2) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-2/k1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-4/k1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-1/k1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-2/k1")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/4-0/k1")
  return passed

def batch12 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 2 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/2-4/k1")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 2 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy2")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 3 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy3")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/0-1/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-2/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-4/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/1-1/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/3-2/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/4-0/k4")
  if decide (membershipMatrix 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/matrix/2-4/k4")
  if testHeavy 9965553118050143013272257897974807602869150761025950146592543765339435077032149250 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL prefix_parity/N4/heavy5")
  if indexTable 114398939385618905930482293903871677890818 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/word")
  if testHeavy 114398939385618905930482293903871677890818 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy0")
  if testHeavy 114398939385618905930482293903871677890818 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy1")
  if testHeavy 114398939385618905930482293903871677890818 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy2")
  if testHeavy 114398939385618905930482293903871677890818 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy3")
  if testHeavy 114398939385618905930482293903871677890818 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy4")
  if testHeavy 114398939385618905930482293903871677890818 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N0/heavy5")
  if indexTable 114398939385618905930482293903871677890818 1 (fun i => #[false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/word0")
  if indexTable 114398939385618905930482293903871677890818 1 (fun i => #[true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/word1")
  if testHeavy 114398939385618905930482293903871677890818 0 1 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy0")
  if testHeavy 114398939385618905930482293903871677890818 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy1")
  if testHeavy 114398939385618905930482293903871677890818 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy2")
  if testHeavy 114398939385618905930482293903871677890818 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy3")
  if testHeavy 114398939385618905930482293903871677890818 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy4")
  if testHeavy 114398939385618905930482293903871677890818 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N1/heavy5")
  if indexTable 114398939385618905930482293903871677890818 2 (fun i => #[false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/word00")
  if indexTable 114398939385618905930482293903871677890818 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/word01")
  if indexTable 114398939385618905930482293903871677890818 2 (fun i => #[true, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/word10")
  if indexTable 114398939385618905930482293903871677890818 2 (fun i => #[true, true][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/word11")
  if testHeavy 114398939385618905930482293903871677890818 0 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy0")
  if testHeavy 114398939385618905930482293903871677890818 1 2 == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy1")
  if testHeavy 114398939385618905930482293903871677890818 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy2")
  if testHeavy 114398939385618905930482293903871677890818 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy3")
  if testHeavy 114398939385618905930482293903871677890818 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy4")
  if testHeavy 114398939385618905930482293903871677890818 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N2/heavy5")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[false, false, false][i.val]!) == (3 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word000")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[false, false, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word001")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word010")
  return passed

def batch13 : IO Nat := do
  let mut passed := 0
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word011")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[true, false, false][i.val]!) == (1 / 4 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word100")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word101")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[true, true, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word110")
  if indexTable 114398939385618905930482293903871677890818 3 (fun i => #[true, true, true][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/word111")
  if testHeavy 114398939385618905930482293903871677890818 0 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy0")
  if testHeavy 114398939385618905930482293903871677890818 1 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy1")
  if testHeavy 114398939385618905930482293903871677890818 2 3 == (5 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy2")
  if testHeavy 114398939385618905930482293903871677890818 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy3")
  if testHeavy 114398939385618905930482293903871677890818 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy4")
  if testHeavy 114398939385618905930482293903871677890818 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N3/heavy5")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, false, false, false][i.val]!) == (5 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0000")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0001")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, false, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0010")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, false, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0011")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0100")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0101")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0110")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word0111")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, false, false, false][i.val]!) == (3 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1000")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, false, false, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1001")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1010")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1011")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, true, false, false][i.val]!) == (1 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1100")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1101")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, true, true, false][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1110")
  if indexTable 114398939385618905930482293903871677890818 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/word1111")
  if testHeavy 114398939385618905930482293903871677890818 0 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/0-1/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 2) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-2/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-4/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-1/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-2/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/4-0/k0")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 2 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/2-4/k0")
  if testHeavy 114398939385618905930482293903871677890818 1 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/0-1/k1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 2) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-2/k1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-4/k1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-1/k1")
  return passed

def batch14 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-2/k1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/4-0/k1")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 2 4) 1 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/2-4/k1")
  if testHeavy 114398939385618905930482293903871677890818 2 4 == (5 / 16 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy2")
  if testHeavy 114398939385618905930482293903871677890818 3 4 == (5 / 8 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy3")
  if testHeavy 114398939385618905930482293903871677890818 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/0-1/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-2/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-4/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/1-1/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/3-2/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/4-0/k4")
  if decide (membershipMatrix 114398939385618905930482293903871677890818 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/matrix/2-4/k4")
  if testHeavy 114398939385618905930482293903871677890818 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL fresh_and_previous/N4/heavy5")
  if indexTable 406426676795556561378476289 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/word")
  if testHeavy 406426676795556561378476289 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy0")
  if testHeavy 406426676795556561378476289 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy1")
  if testHeavy 406426676795556561378476289 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy2")
  if testHeavy 406426676795556561378476289 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy3")
  if testHeavy 406426676795556561378476289 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy4")
  if testHeavy 406426676795556561378476289 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N0/heavy5")
  if indexTable 406426676795556561378476289 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/word0")
  if indexTable 406426676795556561378476289 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/word1")
  if testHeavy 406426676795556561378476289 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy0")
  if testHeavy 406426676795556561378476289 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy1")
  if testHeavy 406426676795556561378476289 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy2")
  if testHeavy 406426676795556561378476289 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy3")
  if testHeavy 406426676795556561378476289 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy4")
  if testHeavy 406426676795556561378476289 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N1/heavy5")
  if indexTable 406426676795556561378476289 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/word00")
  if indexTable 406426676795556561378476289 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/word01")
  if indexTable 406426676795556561378476289 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/word10")
  if indexTable 406426676795556561378476289 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/word11")
  if testHeavy 406426676795556561378476289 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy0")
  if testHeavy 406426676795556561378476289 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy1")
  if testHeavy 406426676795556561378476289 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy2")
  if testHeavy 406426676795556561378476289 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy3")
  if testHeavy 406426676795556561378476289 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy4")
  if testHeavy 406426676795556561378476289 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N2/heavy5")
  if indexTable 406426676795556561378476289 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word000")
  return passed

def batch15 : IO Nat := do
  let mut passed := 0
  if indexTable 406426676795556561378476289 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word001")
  if indexTable 406426676795556561378476289 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word010")
  if indexTable 406426676795556561378476289 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word011")
  if indexTable 406426676795556561378476289 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word100")
  if indexTable 406426676795556561378476289 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word101")
  if indexTable 406426676795556561378476289 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word110")
  if indexTable 406426676795556561378476289 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/word111")
  if testHeavy 406426676795556561378476289 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy0")
  if testHeavy 406426676795556561378476289 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy1")
  if testHeavy 406426676795556561378476289 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy2")
  if testHeavy 406426676795556561378476289 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy3")
  if testHeavy 406426676795556561378476289 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy4")
  if testHeavy 406426676795556561378476289 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N3/heavy5")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0000")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0001")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0010")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0011")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0100")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0101")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0110")
  if indexTable 406426676795556561378476289 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word0111")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1000")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1001")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1010")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1011")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1100")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1101")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1110")
  if indexTable 406426676795556561378476289 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/word1111")
  if testHeavy 406426676795556561378476289 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/0-1/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-2/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-4/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-1/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-2/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/4-0/k0")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/2-4/k0")
  if testHeavy 406426676795556561378476289 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/0-1/k1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-2/k1")
  return passed

def batch16 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-4/k1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-1/k1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-2/k1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/4-0/k1")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/2-4/k1")
  if testHeavy 406426676795556561378476289 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy2")
  if testHeavy 406426676795556561378476289 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy3")
  if testHeavy 406426676795556561378476289 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/0-1/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-2/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-4/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/1-1/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/3-2/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/4-0/k4")
  if decide (membershipMatrix 406426676795556561378476289 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/matrix/2-4/k4")
  if testHeavy 406426676795556561378476289 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL wrong_arity/N4/heavy5")
  if indexTable 406426676795555461866848513 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/word")
  if testHeavy 406426676795555461866848513 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy0")
  if testHeavy 406426676795555461866848513 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy1")
  if testHeavy 406426676795555461866848513 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy2")
  if testHeavy 406426676795555461866848513 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy3")
  if testHeavy 406426676795555461866848513 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy4")
  if testHeavy 406426676795555461866848513 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N0/heavy5")
  if indexTable 406426676795555461866848513 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/word0")
  if indexTable 406426676795555461866848513 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/word1")
  if testHeavy 406426676795555461866848513 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy0")
  if testHeavy 406426676795555461866848513 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy1")
  if testHeavy 406426676795555461866848513 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy2")
  if testHeavy 406426676795555461866848513 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy3")
  if testHeavy 406426676795555461866848513 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy4")
  if testHeavy 406426676795555461866848513 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N1/heavy5")
  if indexTable 406426676795555461866848513 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/word00")
  if indexTable 406426676795555461866848513 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/word01")
  if indexTable 406426676795555461866848513 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/word10")
  if indexTable 406426676795555461866848513 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/word11")
  if testHeavy 406426676795555461866848513 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy0")
  if testHeavy 406426676795555461866848513 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy1")
  if testHeavy 406426676795555461866848513 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy2")
  if testHeavy 406426676795555461866848513 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy3")
  if testHeavy 406426676795555461866848513 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy4")
  return passed

def batch17 : IO Nat := do
  let mut passed := 0
  if testHeavy 406426676795555461866848513 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N2/heavy5")
  if indexTable 406426676795555461866848513 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word000")
  if indexTable 406426676795555461866848513 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word001")
  if indexTable 406426676795555461866848513 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word010")
  if indexTable 406426676795555461866848513 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word011")
  if indexTable 406426676795555461866848513 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word100")
  if indexTable 406426676795555461866848513 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word101")
  if indexTable 406426676795555461866848513 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word110")
  if indexTable 406426676795555461866848513 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/word111")
  if testHeavy 406426676795555461866848513 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy0")
  if testHeavy 406426676795555461866848513 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy1")
  if testHeavy 406426676795555461866848513 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy2")
  if testHeavy 406426676795555461866848513 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy3")
  if testHeavy 406426676795555461866848513 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy4")
  if testHeavy 406426676795555461866848513 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N3/heavy5")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0000")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0001")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0010")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0011")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0100")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0101")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0110")
  if indexTable 406426676795555461866848513 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word0111")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1000")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1001")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1010")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1011")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1100")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1101")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1110")
  if indexTable 406426676795555461866848513 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/word1111")
  if testHeavy 406426676795555461866848513 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/0-1/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-2/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-4/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-1/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-2/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/4-0/k0")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/2-4/k0")
  if testHeavy 406426676795555461866848513 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy1")
  return passed

def batch18 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/0-1/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-2/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-4/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-1/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-2/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/4-0/k1")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/2-4/k1")
  if testHeavy 406426676795555461866848513 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy2")
  if testHeavy 406426676795555461866848513 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy3")
  if testHeavy 406426676795555461866848513 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/0-1/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-2/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-4/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/1-1/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/3-2/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/4-0/k4")
  if decide (membershipMatrix 406426676795555461866848513 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/matrix/2-4/k4")
  if testHeavy 406426676795555461866848513 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL zero_arity/N4/heavy5")
  if indexTable 6201578930596279554304 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/word")
  if testHeavy 6201578930596279554304 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy0")
  if testHeavy 6201578930596279554304 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy1")
  if testHeavy 6201578930596279554304 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy2")
  if testHeavy 6201578930596279554304 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy3")
  if testHeavy 6201578930596279554304 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy4")
  if testHeavy 6201578930596279554304 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N0/heavy5")
  if indexTable 6201578930596279554304 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/word0")
  if indexTable 6201578930596279554304 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/word1")
  if testHeavy 6201578930596279554304 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy0")
  if testHeavy 6201578930596279554304 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy1")
  if testHeavy 6201578930596279554304 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy2")
  if testHeavy 6201578930596279554304 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy3")
  if testHeavy 6201578930596279554304 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy4")
  if testHeavy 6201578930596279554304 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N1/heavy5")
  if indexTable 6201578930596279554304 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/word00")
  if indexTable 6201578930596279554304 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/word01")
  if indexTable 6201578930596279554304 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/word10")
  if indexTable 6201578930596279554304 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/word11")
  if testHeavy 6201578930596279554304 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy0")
  if testHeavy 6201578930596279554304 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy1")
  if testHeavy 6201578930596279554304 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy2")
  return passed

def batch19 : IO Nat := do
  let mut passed := 0
  if testHeavy 6201578930596279554304 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy3")
  if testHeavy 6201578930596279554304 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy4")
  if testHeavy 6201578930596279554304 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N2/heavy5")
  if indexTable 6201578930596279554304 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word000")
  if indexTable 6201578930596279554304 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word001")
  if indexTable 6201578930596279554304 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word010")
  if indexTable 6201578930596279554304 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word011")
  if indexTable 6201578930596279554304 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word100")
  if indexTable 6201578930596279554304 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word101")
  if indexTable 6201578930596279554304 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word110")
  if indexTable 6201578930596279554304 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/word111")
  if testHeavy 6201578930596279554304 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy0")
  if testHeavy 6201578930596279554304 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy1")
  if testHeavy 6201578930596279554304 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy2")
  if testHeavy 6201578930596279554304 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy3")
  if testHeavy 6201578930596279554304 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy4")
  if testHeavy 6201578930596279554304 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N3/heavy5")
  if indexTable 6201578930596279554304 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0000")
  if indexTable 6201578930596279554304 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0001")
  if indexTable 6201578930596279554304 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0010")
  if indexTable 6201578930596279554304 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0011")
  if indexTable 6201578930596279554304 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0100")
  if indexTable 6201578930596279554304 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0101")
  if indexTable 6201578930596279554304 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0110")
  if indexTable 6201578930596279554304 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word0111")
  if indexTable 6201578930596279554304 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1000")
  if indexTable 6201578930596279554304 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1001")
  if indexTable 6201578930596279554304 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1010")
  if indexTable 6201578930596279554304 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1011")
  if indexTable 6201578930596279554304 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1100")
  if indexTable 6201578930596279554304 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1101")
  if indexTable 6201578930596279554304 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1110")
  if indexTable 6201578930596279554304 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/word1111")
  if testHeavy 6201578930596279554304 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/0-1/k0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-2/k0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-4/k0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-1/k0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-2/k0")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/4-0/k0")
  return passed

def batch20 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/2-4/k0")
  if testHeavy 6201578930596279554304 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/0-1/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-2/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-4/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-1/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-2/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/4-0/k1")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/2-4/k1")
  if testHeavy 6201578930596279554304 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy2")
  if testHeavy 6201578930596279554304 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy3")
  if testHeavy 6201578930596279554304 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/0-1/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-2/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-4/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/1-1/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/3-2/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/4-0/k4")
  if decide (membershipMatrix 6201578930596279554304 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/matrix/2-4/k4")
  if testHeavy 6201578930596279554304 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL oversized_output_register/N4/heavy5")
  if indexTable 6818708144761258717208049652662528 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/word")
  if testHeavy 6818708144761258717208049652662528 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy0")
  if testHeavy 6818708144761258717208049652662528 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy1")
  if testHeavy 6818708144761258717208049652662528 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy2")
  if testHeavy 6818708144761258717208049652662528 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy3")
  if testHeavy 6818708144761258717208049652662528 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy4")
  if testHeavy 6818708144761258717208049652662528 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N0/heavy5")
  if indexTable 6818708144761258717208049652662528 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/word0")
  if indexTable 6818708144761258717208049652662528 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/word1")
  if testHeavy 6818708144761258717208049652662528 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy0")
  if testHeavy 6818708144761258717208049652662528 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy1")
  if testHeavy 6818708144761258717208049652662528 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy2")
  if testHeavy 6818708144761258717208049652662528 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy3")
  if testHeavy 6818708144761258717208049652662528 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy4")
  if testHeavy 6818708144761258717208049652662528 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N1/heavy5")
  if indexTable 6818708144761258717208049652662528 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/word00")
  if indexTable 6818708144761258717208049652662528 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/word01")
  if indexTable 6818708144761258717208049652662528 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/word10")
  if indexTable 6818708144761258717208049652662528 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/word11")
  if testHeavy 6818708144761258717208049652662528 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy0")
  return passed

def batch21 : IO Nat := do
  let mut passed := 0
  if testHeavy 6818708144761258717208049652662528 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy1")
  if testHeavy 6818708144761258717208049652662528 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy2")
  if testHeavy 6818708144761258717208049652662528 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy3")
  if testHeavy 6818708144761258717208049652662528 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy4")
  if testHeavy 6818708144761258717208049652662528 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N2/heavy5")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word000")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word001")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word010")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word011")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word100")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word101")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word110")
  if indexTable 6818708144761258717208049652662528 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/word111")
  if testHeavy 6818708144761258717208049652662528 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy0")
  if testHeavy 6818708144761258717208049652662528 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy1")
  if testHeavy 6818708144761258717208049652662528 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy2")
  if testHeavy 6818708144761258717208049652662528 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy3")
  if testHeavy 6818708144761258717208049652662528 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy4")
  if testHeavy 6818708144761258717208049652662528 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N3/heavy5")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0000")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0001")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0010")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0011")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0100")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0101")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0110")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word0111")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1000")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1001")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1010")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1011")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1100")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1101")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1110")
  if indexTable 6818708144761258717208049652662528 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/word1111")
  if testHeavy 6818708144761258717208049652662528 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/0-1/k0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-2/k0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-4/k0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-1/k0")
  return passed

def batch22 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-2/k0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/4-0/k0")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/2-4/k0")
  if testHeavy 6818708144761258717208049652662528 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/0-1/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-2/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-4/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-1/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-2/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/4-0/k1")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/2-4/k1")
  if testHeavy 6818708144761258717208049652662528 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy2")
  if testHeavy 6818708144761258717208049652662528 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy3")
  if testHeavy 6818708144761258717208049652662528 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/0-1/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-2/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-4/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/1-1/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/3-2/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/4-0/k4")
  if decide (membershipMatrix 6818708144761258717208049652662528 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/matrix/2-4/k4")
  if testHeavy 6818708144761258717208049652662528 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL division_by_zero/N4/heavy5")
  if indexTable 6818708144761258717208041062662657 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/word")
  if testHeavy 6818708144761258717208041062662657 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy0")
  if testHeavy 6818708144761258717208041062662657 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy1")
  if testHeavy 6818708144761258717208041062662657 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy2")
  if testHeavy 6818708144761258717208041062662657 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy3")
  if testHeavy 6818708144761258717208041062662657 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy4")
  if testHeavy 6818708144761258717208041062662657 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N0/heavy5")
  if indexTable 6818708144761258717208041062662657 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/word0")
  if indexTable 6818708144761258717208041062662657 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/word1")
  if testHeavy 6818708144761258717208041062662657 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy0")
  if testHeavy 6818708144761258717208041062662657 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy1")
  if testHeavy 6818708144761258717208041062662657 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy2")
  if testHeavy 6818708144761258717208041062662657 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy3")
  if testHeavy 6818708144761258717208041062662657 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy4")
  if testHeavy 6818708144761258717208041062662657 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N1/heavy5")
  if indexTable 6818708144761258717208041062662657 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/word00")
  if indexTable 6818708144761258717208041062662657 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/word01")
  if indexTable 6818708144761258717208041062662657 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/word10")
  return passed

def batch23 : IO Nat := do
  let mut passed := 0
  if indexTable 6818708144761258717208041062662657 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/word11")
  if testHeavy 6818708144761258717208041062662657 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy0")
  if testHeavy 6818708144761258717208041062662657 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy1")
  if testHeavy 6818708144761258717208041062662657 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy2")
  if testHeavy 6818708144761258717208041062662657 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy3")
  if testHeavy 6818708144761258717208041062662657 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy4")
  if testHeavy 6818708144761258717208041062662657 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N2/heavy5")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word000")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word001")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word010")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word011")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word100")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word101")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word110")
  if indexTable 6818708144761258717208041062662657 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/word111")
  if testHeavy 6818708144761258717208041062662657 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy0")
  if testHeavy 6818708144761258717208041062662657 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy1")
  if testHeavy 6818708144761258717208041062662657 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy2")
  if testHeavy 6818708144761258717208041062662657 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy3")
  if testHeavy 6818708144761258717208041062662657 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy4")
  if testHeavy 6818708144761258717208041062662657 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N3/heavy5")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0000")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0001")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0010")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0011")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0100")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0101")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0110")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word0111")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1000")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1001")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1010")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1011")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1100")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1101")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1110")
  if indexTable 6818708144761258717208041062662657 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/word1111")
  if testHeavy 6818708144761258717208041062662657 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/0-1/k0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-2/k0")
  return passed

def batch24 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-4/k0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-1/k0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-2/k0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/4-0/k0")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/2-4/k0")
  if testHeavy 6818708144761258717208041062662657 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/0-1/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-2/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-4/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-1/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-2/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/4-0/k1")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/2-4/k1")
  if testHeavy 6818708144761258717208041062662657 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy2")
  if testHeavy 6818708144761258717208041062662657 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy3")
  if testHeavy 6818708144761258717208041062662657 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/0-1/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-2/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-4/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/1-1/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/3-2/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/4-0/k4")
  if decide (membershipMatrix 6818708144761258717208041062662657 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/matrix/2-4/k4")
  if testHeavy 6818708144761258717208041062662657 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL subtraction_truncation/N4/heavy5")
  if indexTable 29286128482718439918203559835646890061332740 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/word")
  if testHeavy 29286128482718439918203559835646890061332740 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy0")
  if testHeavy 29286128482718439918203559835646890061332740 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy1")
  if testHeavy 29286128482718439918203559835646890061332740 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy2")
  if testHeavy 29286128482718439918203559835646890061332740 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy3")
  if testHeavy 29286128482718439918203559835646890061332740 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy4")
  if testHeavy 29286128482718439918203559835646890061332740 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N0/heavy5")
  if indexTable 29286128482718439918203559835646890061332740 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/word0")
  if indexTable 29286128482718439918203559835646890061332740 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/word1")
  if testHeavy 29286128482718439918203559835646890061332740 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy0")
  if testHeavy 29286128482718439918203559835646890061332740 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy1")
  if testHeavy 29286128482718439918203559835646890061332740 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy2")
  if testHeavy 29286128482718439918203559835646890061332740 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy3")
  if testHeavy 29286128482718439918203559835646890061332740 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy4")
  if testHeavy 29286128482718439918203559835646890061332740 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N1/heavy5")
  if indexTable 29286128482718439918203559835646890061332740 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/word00")
  return passed

def batch25 : IO Nat := do
  let mut passed := 0
  if indexTable 29286128482718439918203559835646890061332740 2 (fun i => #[false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/word01")
  if indexTable 29286128482718439918203559835646890061332740 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/word10")
  if indexTable 29286128482718439918203559835646890061332740 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/word11")
  if testHeavy 29286128482718439918203559835646890061332740 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy0")
  if testHeavy 29286128482718439918203559835646890061332740 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy1")
  if testHeavy 29286128482718439918203559835646890061332740 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy2")
  if testHeavy 29286128482718439918203559835646890061332740 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy3")
  if testHeavy 29286128482718439918203559835646890061332740 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy4")
  if testHeavy 29286128482718439918203559835646890061332740 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N2/heavy5")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word000")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word001")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word010")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[false, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word011")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word100")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word101")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word110")
  if indexTable 29286128482718439918203559835646890061332740 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/word111")
  if testHeavy 29286128482718439918203559835646890061332740 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy0")
  if testHeavy 29286128482718439918203559835646890061332740 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy1")
  if testHeavy 29286128482718439918203559835646890061332740 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy2")
  if testHeavy 29286128482718439918203559835646890061332740 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy3")
  if testHeavy 29286128482718439918203559835646890061332740 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy4")
  if testHeavy 29286128482718439918203559835646890061332740 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N3/heavy5")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0000")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0001")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0010")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0011")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0100")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0101")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0110")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[false, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word0111")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1000")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1001")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1010")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1011")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1100")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1101")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1110")
  if indexTable 29286128482718439918203559835646890061332740 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/word1111")
  if testHeavy 29286128482718439918203559835646890061332740 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy0")
  return passed

def batch26 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/0-1/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-2/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-4/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-1/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-2/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/4-0/k0")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/2-4/k0")
  if testHeavy 29286128482718439918203559835646890061332740 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/0-1/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-2/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-4/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-1/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-2/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/4-0/k1")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/2-4/k1")
  if testHeavy 29286128482718439918203559835646890061332740 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy2")
  if testHeavy 29286128482718439918203559835646890061332740 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy3")
  if testHeavy 29286128482718439918203559835646890061332740 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/0-1/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-2/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-4/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/1-1/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/3-2/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/4-0/k4")
  if decide (membershipMatrix 29286128482718439918203559835646890061332740 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/matrix/2-4/k4")
  if testHeavy 29286128482718439918203559835646890061332740 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_0/N4/heavy5")
  if indexTable 29286128482718439918203559835646881471463684 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/word")
  if testHeavy 29286128482718439918203559835646881471463684 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy0")
  if testHeavy 29286128482718439918203559835646881471463684 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy1")
  if testHeavy 29286128482718439918203559835646881471463684 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy2")
  if testHeavy 29286128482718439918203559835646881471463684 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy3")
  if testHeavy 29286128482718439918203559835646881471463684 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy4")
  if testHeavy 29286128482718439918203559835646881471463684 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N0/heavy5")
  if indexTable 29286128482718439918203559835646881471463684 1 (fun i => #[false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/word0")
  if indexTable 29286128482718439918203559835646881471463684 1 (fun i => #[true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/word1")
  if testHeavy 29286128482718439918203559835646881471463684 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy0")
  if testHeavy 29286128482718439918203559835646881471463684 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy1")
  if testHeavy 29286128482718439918203559835646881471463684 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy2")
  if testHeavy 29286128482718439918203559835646881471463684 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy3")
  if testHeavy 29286128482718439918203559835646881471463684 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy4")
  return passed

def batch27 : IO Nat := do
  let mut passed := 0
  if testHeavy 29286128482718439918203559835646881471463684 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N1/heavy5")
  if indexTable 29286128482718439918203559835646881471463684 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/word00")
  if indexTable 29286128482718439918203559835646881471463684 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/word01")
  if indexTable 29286128482718439918203559835646881471463684 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/word10")
  if indexTable 29286128482718439918203559835646881471463684 2 (fun i => #[true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/word11")
  if testHeavy 29286128482718439918203559835646881471463684 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy0")
  if testHeavy 29286128482718439918203559835646881471463684 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy1")
  if testHeavy 29286128482718439918203559835646881471463684 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy2")
  if testHeavy 29286128482718439918203559835646881471463684 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy3")
  if testHeavy 29286128482718439918203559835646881471463684 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy4")
  if testHeavy 29286128482718439918203559835646881471463684 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N2/heavy5")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word000")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word001")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word010")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word011")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word100")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word101")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word110")
  if indexTable 29286128482718439918203559835646881471463684 3 (fun i => #[true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/word111")
  if testHeavy 29286128482718439918203559835646881471463684 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy0")
  if testHeavy 29286128482718439918203559835646881471463684 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy1")
  if testHeavy 29286128482718439918203559835646881471463684 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy2")
  if testHeavy 29286128482718439918203559835646881471463684 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy3")
  if testHeavy 29286128482718439918203559835646881471463684 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy4")
  if testHeavy 29286128482718439918203559835646881471463684 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N3/heavy5")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0000")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0001")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0010")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0011")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0100")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0101")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0110")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word0111")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1000")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1001")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1010")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1011")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1100")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1101")
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1110")
  return passed

def batch28 : IO Nat := do
  let mut passed := 0
  if indexTable 29286128482718439918203559835646881471463684 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/word1111")
  if testHeavy 29286128482718439918203559835646881471463684 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/0-1/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-2/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-4/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-1/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-2/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/4-0/k0")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/2-4/k0")
  if testHeavy 29286128482718439918203559835646881471463684 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/0-1/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-2/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-4/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-1/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-2/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/4-0/k1")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/2-4/k1")
  if testHeavy 29286128482718439918203559835646881471463684 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy2")
  if testHeavy 29286128482718439918203559835646881471463684 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy3")
  if testHeavy 29286128482718439918203559835646881471463684 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/0-1/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-2/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-4/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/1-1/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/3-2/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/4-0/k4")
  if decide (membershipMatrix 29286128482718439918203559835646881471463684 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/matrix/2-4/k4")
  if testHeavy 29286128482718439918203559835646881471463684 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_1/N4/heavy5")
  if indexTable 1919295716243435678479382462075317872304941367809 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/word")
  if testHeavy 1919295716243435678479382462075317872304941367809 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy0")
  if testHeavy 1919295716243435678479382462075317872304941367809 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy1")
  if testHeavy 1919295716243435678479382462075317872304941367809 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy2")
  if testHeavy 1919295716243435678479382462075317872304941367809 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy3")
  if testHeavy 1919295716243435678479382462075317872304941367809 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy4")
  if testHeavy 1919295716243435678479382462075317872304941367809 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N0/heavy5")
  if indexTable 1919295716243435678479382462075317872304941367809 1 (fun i => #[false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/word0")
  if indexTable 1919295716243435678479382462075317872304941367809 1 (fun i => #[true][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/word1")
  if testHeavy 1919295716243435678479382462075317872304941367809 0 1 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy0")
  if testHeavy 1919295716243435678479382462075317872304941367809 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy1")
  if testHeavy 1919295716243435678479382462075317872304941367809 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy2")
  return passed

def batch29 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479382462075317872304941367809 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy3")
  if testHeavy 1919295716243435678479382462075317872304941367809 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy4")
  if testHeavy 1919295716243435678479382462075317872304941367809 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N1/heavy5")
  if indexTable 1919295716243435678479382462075317872304941367809 2 (fun i => #[false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/word00")
  if indexTable 1919295716243435678479382462075317872304941367809 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/word01")
  if indexTable 1919295716243435678479382462075317872304941367809 2 (fun i => #[true, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/word10")
  if indexTable 1919295716243435678479382462075317872304941367809 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/word11")
  if testHeavy 1919295716243435678479382462075317872304941367809 0 2 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy0")
  if testHeavy 1919295716243435678479382462075317872304941367809 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy1")
  if testHeavy 1919295716243435678479382462075317872304941367809 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy2")
  if testHeavy 1919295716243435678479382462075317872304941367809 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy3")
  if testHeavy 1919295716243435678479382462075317872304941367809 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy4")
  if testHeavy 1919295716243435678479382462075317872304941367809 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N2/heavy5")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[false, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word000")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word001")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word010")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word011")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[true, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word100")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word101")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word110")
  if indexTable 1919295716243435678479382462075317872304941367809 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/word111")
  if testHeavy 1919295716243435678479382462075317872304941367809 0 3 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy0")
  if testHeavy 1919295716243435678479382462075317872304941367809 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy1")
  if testHeavy 1919295716243435678479382462075317872304941367809 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy2")
  if testHeavy 1919295716243435678479382462075317872304941367809 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy3")
  if testHeavy 1919295716243435678479382462075317872304941367809 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy4")
  if testHeavy 1919295716243435678479382462075317872304941367809 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N3/heavy5")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0000")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0001")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0010")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0011")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0100")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0101")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0110")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word0111")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, false, false, false][i.val]!) == (1 / 2 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1000")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1001")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1010")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1011")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1100")
  return passed

def batch30 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1101")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1110")
  if indexTable 1919295716243435678479382462075317872304941367809 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/word1111")
  if testHeavy 1919295716243435678479382462075317872304941367809 0 4 == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 2) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 2 4) 0 4) == false then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/2-4/k0")
  if testHeavy 1919295716243435678479382462075317872304941367809 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/2-4/k1")
  if testHeavy 1919295716243435678479382462075317872304941367809 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy2")
  if testHeavy 1919295716243435678479382462075317872304941367809 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy3")
  if testHeavy 1919295716243435678479382462075317872304941367809 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479382462075317872304941367809 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/matrix/2-4/k4")
  if testHeavy 1919295716243435678479382462075317872304941367809 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_2/N4/heavy5")
  if indexTable 1919295716243435678479386088834618483952721199360 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/word")
  if testHeavy 1919295716243435678479386088834618483952721199360 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy0")
  if testHeavy 1919295716243435678479386088834618483952721199360 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy1")
  if testHeavy 1919295716243435678479386088834618483952721199360 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy2")
  if testHeavy 1919295716243435678479386088834618483952721199360 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy3")
  if testHeavy 1919295716243435678479386088834618483952721199360 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy4")
  if testHeavy 1919295716243435678479386088834618483952721199360 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N0/heavy5")
  if indexTable 1919295716243435678479386088834618483952721199360 1 (fun i => #[false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/word0")
  if indexTable 1919295716243435678479386088834618483952721199360 1 (fun i => #[true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/word1")
  if testHeavy 1919295716243435678479386088834618483952721199360 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy0")
  return passed

def batch31 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479386088834618483952721199360 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy1")
  if testHeavy 1919295716243435678479386088834618483952721199360 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy2")
  if testHeavy 1919295716243435678479386088834618483952721199360 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy3")
  if testHeavy 1919295716243435678479386088834618483952721199360 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy4")
  if testHeavy 1919295716243435678479386088834618483952721199360 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N1/heavy5")
  if indexTable 1919295716243435678479386088834618483952721199360 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/word00")
  if indexTable 1919295716243435678479386088834618483952721199360 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/word01")
  if indexTable 1919295716243435678479386088834618483952721199360 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/word10")
  if indexTable 1919295716243435678479386088834618483952721199360 2 (fun i => #[true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/word11")
  if testHeavy 1919295716243435678479386088834618483952721199360 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy0")
  if testHeavy 1919295716243435678479386088834618483952721199360 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy1")
  if testHeavy 1919295716243435678479386088834618483952721199360 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy2")
  if testHeavy 1919295716243435678479386088834618483952721199360 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy3")
  if testHeavy 1919295716243435678479386088834618483952721199360 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy4")
  if testHeavy 1919295716243435678479386088834618483952721199360 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N2/heavy5")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word000")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word001")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word010")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word011")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word100")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word101")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word110")
  if indexTable 1919295716243435678479386088834618483952721199360 3 (fun i => #[true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/word111")
  if testHeavy 1919295716243435678479386088834618483952721199360 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy0")
  if testHeavy 1919295716243435678479386088834618483952721199360 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy1")
  if testHeavy 1919295716243435678479386088834618483952721199360 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy2")
  if testHeavy 1919295716243435678479386088834618483952721199360 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy3")
  if testHeavy 1919295716243435678479386088834618483952721199360 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy4")
  if testHeavy 1919295716243435678479386088834618483952721199360 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N3/heavy5")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0000")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0001")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0010")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0011")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0100")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0101")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0110")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word0111")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1000")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1001")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1010")
  return passed

def batch32 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1011")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1100")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1101")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1110")
  if indexTable 1919295716243435678479386088834618483952721199360 4 (fun i => #[true, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/word1111")
  if testHeavy 1919295716243435678479386088834618483952721199360 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/2-4/k0")
  if testHeavy 1919295716243435678479386088834618483952721199360 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/2-4/k1")
  if testHeavy 1919295716243435678479386088834618483952721199360 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy2")
  if testHeavy 1919295716243435678479386088834618483952721199360 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy3")
  if testHeavy 1919295716243435678479386088834618483952721199360 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479386088834618483952721199360 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/matrix/2-4/k4")
  if testHeavy 1919295716243435678479386088834618483952721199360 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_3/N4/heavy5")
  if indexTable 1919295716243435678479386079389741405250147975680 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/word")
  if testHeavy 1919295716243435678479386079389741405250147975680 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy0")
  if testHeavy 1919295716243435678479386079389741405250147975680 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy1")
  if testHeavy 1919295716243435678479386079389741405250147975680 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy2")
  if testHeavy 1919295716243435678479386079389741405250147975680 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy3")
  if testHeavy 1919295716243435678479386079389741405250147975680 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy4")
  if testHeavy 1919295716243435678479386079389741405250147975680 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N0/heavy5")
  if indexTable 1919295716243435678479386079389741405250147975680 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/word0")
  return passed

def batch33 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479386079389741405250147975680 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/word1")
  if testHeavy 1919295716243435678479386079389741405250147975680 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy0")
  if testHeavy 1919295716243435678479386079389741405250147975680 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy1")
  if testHeavy 1919295716243435678479386079389741405250147975680 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy2")
  if testHeavy 1919295716243435678479386079389741405250147975680 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy3")
  if testHeavy 1919295716243435678479386079389741405250147975680 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy4")
  if testHeavy 1919295716243435678479386079389741405250147975680 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N1/heavy5")
  if indexTable 1919295716243435678479386079389741405250147975680 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/word00")
  if indexTable 1919295716243435678479386079389741405250147975680 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/word01")
  if indexTable 1919295716243435678479386079389741405250147975680 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/word10")
  if indexTable 1919295716243435678479386079389741405250147975680 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/word11")
  if testHeavy 1919295716243435678479386079389741405250147975680 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy0")
  if testHeavy 1919295716243435678479386079389741405250147975680 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy1")
  if testHeavy 1919295716243435678479386079389741405250147975680 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy2")
  if testHeavy 1919295716243435678479386079389741405250147975680 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy3")
  if testHeavy 1919295716243435678479386079389741405250147975680 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy4")
  if testHeavy 1919295716243435678479386079389741405250147975680 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N2/heavy5")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word000")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word001")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word010")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word011")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word100")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word101")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word110")
  if indexTable 1919295716243435678479386079389741405250147975680 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/word111")
  if testHeavy 1919295716243435678479386079389741405250147975680 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy0")
  if testHeavy 1919295716243435678479386079389741405250147975680 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy1")
  if testHeavy 1919295716243435678479386079389741405250147975680 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy2")
  if testHeavy 1919295716243435678479386079389741405250147975680 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy3")
  if testHeavy 1919295716243435678479386079389741405250147975680 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy4")
  if testHeavy 1919295716243435678479386079389741405250147975680 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N3/heavy5")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0000")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0001")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0010")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0011")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0100")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0101")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0110")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word0111")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1000")
  return passed

def batch34 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1001")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1010")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1011")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1100")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1101")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1110")
  if indexTable 1919295716243435678479386079389741405250147975680 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/word1111")
  if testHeavy 1919295716243435678479386079389741405250147975680 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/2-4/k0")
  if testHeavy 1919295716243435678479386079389741405250147975680 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/2-4/k1")
  if testHeavy 1919295716243435678479386079389741405250147975680 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy2")
  if testHeavy 1919295716243435678479386079389741405250147975680 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy3")
  if testHeavy 1919295716243435678479386079389741405250147975680 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479386079389741405250147975680 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/matrix/2-4/k4")
  if testHeavy 1919295716243435678479386079389741405250147975680 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_4/N4/heavy5")
  if indexTable 1919295716243435678479384861019044710767331901954 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/word")
  if testHeavy 1919295716243435678479384861019044710767331901954 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy0")
  if testHeavy 1919295716243435678479384861019044710767331901954 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy1")
  if testHeavy 1919295716243435678479384861019044710767331901954 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy2")
  if testHeavy 1919295716243435678479384861019044710767331901954 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy3")
  if testHeavy 1919295716243435678479384861019044710767331901954 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy4")
  return passed

def batch35 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479384861019044710767331901954 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N0/heavy5")
  if indexTable 1919295716243435678479384861019044710767331901954 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/word0")
  if indexTable 1919295716243435678479384861019044710767331901954 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/word1")
  if testHeavy 1919295716243435678479384861019044710767331901954 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy0")
  if testHeavy 1919295716243435678479384861019044710767331901954 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy1")
  if testHeavy 1919295716243435678479384861019044710767331901954 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy2")
  if testHeavy 1919295716243435678479384861019044710767331901954 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy3")
  if testHeavy 1919295716243435678479384861019044710767331901954 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy4")
  if testHeavy 1919295716243435678479384861019044710767331901954 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N1/heavy5")
  if indexTable 1919295716243435678479384861019044710767331901954 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/word00")
  if indexTable 1919295716243435678479384861019044710767331901954 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/word01")
  if indexTable 1919295716243435678479384861019044710767331901954 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/word10")
  if indexTable 1919295716243435678479384861019044710767331901954 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/word11")
  if testHeavy 1919295716243435678479384861019044710767331901954 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy0")
  if testHeavy 1919295716243435678479384861019044710767331901954 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy1")
  if testHeavy 1919295716243435678479384861019044710767331901954 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy2")
  if testHeavy 1919295716243435678479384861019044710767331901954 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy3")
  if testHeavy 1919295716243435678479384861019044710767331901954 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy4")
  if testHeavy 1919295716243435678479384861019044710767331901954 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N2/heavy5")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word000")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word001")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word010")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word011")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word100")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word101")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word110")
  if indexTable 1919295716243435678479384861019044710767331901954 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/word111")
  if testHeavy 1919295716243435678479384861019044710767331901954 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy0")
  if testHeavy 1919295716243435678479384861019044710767331901954 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy1")
  if testHeavy 1919295716243435678479384861019044710767331901954 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy2")
  if testHeavy 1919295716243435678479384861019044710767331901954 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy3")
  if testHeavy 1919295716243435678479384861019044710767331901954 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy4")
  if testHeavy 1919295716243435678479384861019044710767331901954 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N3/heavy5")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0000")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0001")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0010")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0011")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0100")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0101")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0110")
  return passed

def batch36 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word0111")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1000")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1001")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1010")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1011")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1100")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1101")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1110")
  if indexTable 1919295716243435678479384861019044710767331901954 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/word1111")
  if testHeavy 1919295716243435678479384861019044710767331901954 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/2-4/k0")
  if testHeavy 1919295716243435678479384861019044710767331901954 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/2-4/k1")
  if testHeavy 1919295716243435678479384861019044710767331901954 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy2")
  if testHeavy 1919295716243435678479384861019044710767331901954 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy3")
  if testHeavy 1919295716243435678479384861019044710767331901954 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479384861019044710767331901954 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/matrix/2-4/k4")
  if testHeavy 1919295716243435678479384861019044710767331901954 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_5/N4/heavy5")
  if indexTable 1919295716243435678479380015871105344131167289856 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/word")
  if testHeavy 1919295716243435678479380015871105344131167289856 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy0")
  if testHeavy 1919295716243435678479380015871105344131167289856 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy1")
  if testHeavy 1919295716243435678479380015871105344131167289856 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy2")
  return passed

def batch37 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479380015871105344131167289856 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy3")
  if testHeavy 1919295716243435678479380015871105344131167289856 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy4")
  if testHeavy 1919295716243435678479380015871105344131167289856 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N0/heavy5")
  if indexTable 1919295716243435678479380015871105344131167289856 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/word0")
  if indexTable 1919295716243435678479380015871105344131167289856 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/word1")
  if testHeavy 1919295716243435678479380015871105344131167289856 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy0")
  if testHeavy 1919295716243435678479380015871105344131167289856 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy1")
  if testHeavy 1919295716243435678479380015871105344131167289856 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy2")
  if testHeavy 1919295716243435678479380015871105344131167289856 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy3")
  if testHeavy 1919295716243435678479380015871105344131167289856 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy4")
  if testHeavy 1919295716243435678479380015871105344131167289856 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N1/heavy5")
  if indexTable 1919295716243435678479380015871105344131167289856 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/word00")
  if indexTable 1919295716243435678479380015871105344131167289856 2 (fun i => #[false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/word01")
  if indexTable 1919295716243435678479380015871105344131167289856 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/word10")
  if indexTable 1919295716243435678479380015871105344131167289856 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/word11")
  if testHeavy 1919295716243435678479380015871105344131167289856 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy0")
  if testHeavy 1919295716243435678479380015871105344131167289856 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy1")
  if testHeavy 1919295716243435678479380015871105344131167289856 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy2")
  if testHeavy 1919295716243435678479380015871105344131167289856 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy3")
  if testHeavy 1919295716243435678479380015871105344131167289856 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy4")
  if testHeavy 1919295716243435678479380015871105344131167289856 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N2/heavy5")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word000")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word001")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word010")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[false, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word011")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word100")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word101")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word110")
  if indexTable 1919295716243435678479380015871105344131167289856 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/word111")
  if testHeavy 1919295716243435678479380015871105344131167289856 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy0")
  if testHeavy 1919295716243435678479380015871105344131167289856 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy1")
  if testHeavy 1919295716243435678479380015871105344131167289856 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy2")
  if testHeavy 1919295716243435678479380015871105344131167289856 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy3")
  if testHeavy 1919295716243435678479380015871105344131167289856 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy4")
  if testHeavy 1919295716243435678479380015871105344131167289856 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N3/heavy5")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0000")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0001")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0010")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0011")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0100")
  return passed

def batch38 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0101")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0110")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[false, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word0111")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1000")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1001")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1010")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1011")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1100")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1101")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1110")
  if indexTable 1919295716243435678479380015871105344131167289856 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/word1111")
  if testHeavy 1919295716243435678479380015871105344131167289856 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/2-4/k0")
  if testHeavy 1919295716243435678479380015871105344131167289856 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/2-4/k1")
  if testHeavy 1919295716243435678479380015871105344131167289856 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy2")
  if testHeavy 1919295716243435678479380015871105344131167289856 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy3")
  if testHeavy 1919295716243435678479380015871105344131167289856 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479380015871105344131167289856 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/matrix/2-4/k4")
  if testHeavy 1919295716243435678479380015871105344131167289856 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_6/N4/heavy5")
  if indexTable 1919295716243435678479386084130410233327131885824 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/word")
  if testHeavy 1919295716243435678479386084130410233327131885824 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy0")
  return passed

def batch39 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479386084130410233327131885824 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy1")
  if testHeavy 1919295716243435678479386084130410233327131885824 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy2")
  if testHeavy 1919295716243435678479386084130410233327131885824 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy3")
  if testHeavy 1919295716243435678479386084130410233327131885824 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy4")
  if testHeavy 1919295716243435678479386084130410233327131885824 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N0/heavy5")
  if indexTable 1919295716243435678479386084130410233327131885824 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/word0")
  if indexTable 1919295716243435678479386084130410233327131885824 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/word1")
  if testHeavy 1919295716243435678479386084130410233327131885824 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy0")
  if testHeavy 1919295716243435678479386084130410233327131885824 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy1")
  if testHeavy 1919295716243435678479386084130410233327131885824 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy2")
  if testHeavy 1919295716243435678479386084130410233327131885824 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy3")
  if testHeavy 1919295716243435678479386084130410233327131885824 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy4")
  if testHeavy 1919295716243435678479386084130410233327131885824 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N1/heavy5")
  if indexTable 1919295716243435678479386084130410233327131885824 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/word00")
  if indexTable 1919295716243435678479386084130410233327131885824 2 (fun i => #[false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/word01")
  if indexTable 1919295716243435678479386084130410233327131885824 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/word10")
  if indexTable 1919295716243435678479386084130410233327131885824 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/word11")
  if testHeavy 1919295716243435678479386084130410233327131885824 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy0")
  if testHeavy 1919295716243435678479386084130410233327131885824 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy1")
  if testHeavy 1919295716243435678479386084130410233327131885824 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy2")
  if testHeavy 1919295716243435678479386084130410233327131885824 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy3")
  if testHeavy 1919295716243435678479386084130410233327131885824 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy4")
  if testHeavy 1919295716243435678479386084130410233327131885824 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N2/heavy5")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word000")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word001")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word010")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[false, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word011")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word100")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word101")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word110")
  if indexTable 1919295716243435678479386084130410233327131885824 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/word111")
  if testHeavy 1919295716243435678479386084130410233327131885824 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy0")
  if testHeavy 1919295716243435678479386084130410233327131885824 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy1")
  if testHeavy 1919295716243435678479386084130410233327131885824 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy2")
  if testHeavy 1919295716243435678479386084130410233327131885824 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy3")
  if testHeavy 1919295716243435678479386084130410233327131885824 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy4")
  if testHeavy 1919295716243435678479386084130410233327131885824 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N3/heavy5")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0000")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0001")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0010")
  return passed

def batch40 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0011")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0100")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0101")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0110")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[false, true, true, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word0111")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1000")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1001")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1010")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1011")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1100")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1101")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1110")
  if indexTable 1919295716243435678479386084130410233327131885824 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/word1111")
  if testHeavy 1919295716243435678479386084130410233327131885824 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/2-4/k0")
  if testHeavy 1919295716243435678479386084130410233327131885824 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/2-4/k1")
  if testHeavy 1919295716243435678479386084130410233327131885824 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy2")
  if testHeavy 1919295716243435678479386084130410233327131885824 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy3")
  if testHeavy 1919295716243435678479386084130410233327131885824 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479386084130410233327131885824 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/matrix/2-4/k4")
  if testHeavy 1919295716243435678479386084130410233327131885824 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_7/N4/heavy5")
  return passed

def batch41 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479384861019260880259500933378 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/word")
  if testHeavy 1919295716243435678479384861019260880259500933378 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy0")
  if testHeavy 1919295716243435678479384861019260880259500933378 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy1")
  if testHeavy 1919295716243435678479384861019260880259500933378 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy2")
  if testHeavy 1919295716243435678479384861019260880259500933378 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy3")
  if testHeavy 1919295716243435678479384861019260880259500933378 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy4")
  if testHeavy 1919295716243435678479384861019260880259500933378 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N0/heavy5")
  if indexTable 1919295716243435678479384861019260880259500933378 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/word0")
  if indexTable 1919295716243435678479384861019260880259500933378 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/word1")
  if testHeavy 1919295716243435678479384861019260880259500933378 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy0")
  if testHeavy 1919295716243435678479384861019260880259500933378 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy1")
  if testHeavy 1919295716243435678479384861019260880259500933378 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy2")
  if testHeavy 1919295716243435678479384861019260880259500933378 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy3")
  if testHeavy 1919295716243435678479384861019260880259500933378 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy4")
  if testHeavy 1919295716243435678479384861019260880259500933378 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N1/heavy5")
  if indexTable 1919295716243435678479384861019260880259500933378 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/word00")
  if indexTable 1919295716243435678479384861019260880259500933378 2 (fun i => #[false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/word01")
  if indexTable 1919295716243435678479384861019260880259500933378 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/word10")
  if indexTable 1919295716243435678479384861019260880259500933378 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/word11")
  if testHeavy 1919295716243435678479384861019260880259500933378 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy0")
  if testHeavy 1919295716243435678479384861019260880259500933378 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy1")
  if testHeavy 1919295716243435678479384861019260880259500933378 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy2")
  if testHeavy 1919295716243435678479384861019260880259500933378 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy3")
  if testHeavy 1919295716243435678479384861019260880259500933378 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy4")
  if testHeavy 1919295716243435678479384861019260880259500933378 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N2/heavy5")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word000")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word001")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[false, true, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word010")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word011")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word100")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word101")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word110")
  if indexTable 1919295716243435678479384861019260880259500933378 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/word111")
  if testHeavy 1919295716243435678479384861019260880259500933378 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy0")
  if testHeavy 1919295716243435678479384861019260880259500933378 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy1")
  if testHeavy 1919295716243435678479384861019260880259500933378 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy2")
  if testHeavy 1919295716243435678479384861019260880259500933378 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy3")
  if testHeavy 1919295716243435678479384861019260880259500933378 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy4")
  if testHeavy 1919295716243435678479384861019260880259500933378 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N3/heavy5")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0000")
  return passed

def batch42 : IO Nat := do
  let mut passed := 0
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0001")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0010")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0011")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0100")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, true, false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0101")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0110")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word0111")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1000")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1001")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1010")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1011")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1100")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1101")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1110")
  if indexTable 1919295716243435678479384861019260880259500933378 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/word1111")
  if testHeavy 1919295716243435678479384861019260880259500933378 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/2-4/k0")
  if testHeavy 1919295716243435678479384861019260880259500933378 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/2-4/k1")
  if testHeavy 1919295716243435678479384861019260880259500933378 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy2")
  if testHeavy 1919295716243435678479384861019260880259500933378 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy3")
  if testHeavy 1919295716243435678479384861019260880259500933378 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/4-0/k4")
  return passed

def batch43 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1919295716243435678479384861019260880259500933378 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/matrix/2-4/k4")
  if testHeavy 1919295716243435678479384861019260880259500933378 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_8/N4/heavy5")
  if indexTable 1919295716243435678479386069945152552478435377667 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/word")
  if testHeavy 1919295716243435678479386069945152552478435377667 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy0")
  if testHeavy 1919295716243435678479386069945152552478435377667 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy1")
  if testHeavy 1919295716243435678479386069945152552478435377667 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy2")
  if testHeavy 1919295716243435678479386069945152552478435377667 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy3")
  if testHeavy 1919295716243435678479386069945152552478435377667 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy4")
  if testHeavy 1919295716243435678479386069945152552478435377667 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N0/heavy5")
  if indexTable 1919295716243435678479386069945152552478435377667 1 (fun i => #[false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/word0")
  if indexTable 1919295716243435678479386069945152552478435377667 1 (fun i => #[true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/word1")
  if testHeavy 1919295716243435678479386069945152552478435377667 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy0")
  if testHeavy 1919295716243435678479386069945152552478435377667 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy1")
  if testHeavy 1919295716243435678479386069945152552478435377667 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy2")
  if testHeavy 1919295716243435678479386069945152552478435377667 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy3")
  if testHeavy 1919295716243435678479386069945152552478435377667 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy4")
  if testHeavy 1919295716243435678479386069945152552478435377667 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N1/heavy5")
  if indexTable 1919295716243435678479386069945152552478435377667 2 (fun i => #[false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/word00")
  if indexTable 1919295716243435678479386069945152552478435377667 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/word01")
  if indexTable 1919295716243435678479386069945152552478435377667 2 (fun i => #[true, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/word10")
  if indexTable 1919295716243435678479386069945152552478435377667 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/word11")
  if testHeavy 1919295716243435678479386069945152552478435377667 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy0")
  if testHeavy 1919295716243435678479386069945152552478435377667 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy1")
  if testHeavy 1919295716243435678479386069945152552478435377667 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy2")
  if testHeavy 1919295716243435678479386069945152552478435377667 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy3")
  if testHeavy 1919295716243435678479386069945152552478435377667 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy4")
  if testHeavy 1919295716243435678479386069945152552478435377667 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N2/heavy5")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word000")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word001")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word010")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word011")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[true, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word100")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word101")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word110")
  if indexTable 1919295716243435678479386069945152552478435377667 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/word111")
  if testHeavy 1919295716243435678479386069945152552478435377667 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy0")
  if testHeavy 1919295716243435678479386069945152552478435377667 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy1")
  if testHeavy 1919295716243435678479386069945152552478435377667 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy2")
  if testHeavy 1919295716243435678479386069945152552478435377667 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy3")
  if testHeavy 1919295716243435678479386069945152552478435377667 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy4")
  return passed

def batch44 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479386069945152552478435377667 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N3/heavy5")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0000")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0001")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0010")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0011")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0100")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0101")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0110")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word0111")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1000")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1001")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1010")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1011")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1100")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1101")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1110")
  if indexTable 1919295716243435678479386069945152552478435377667 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/word1111")
  if testHeavy 1919295716243435678479386069945152552478435377667 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/2-4/k0")
  if testHeavy 1919295716243435678479386069945152552478435377667 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/2-4/k1")
  if testHeavy 1919295716243435678479386069945152552478435377667 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy2")
  if testHeavy 1919295716243435678479386069945152552478435377667 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy3")
  if testHeavy 1919295716243435678479386069945152552478435377667 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/1-1/k4")
  return passed

def batch45 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479386069945152552478435377667 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/matrix/2-4/k4")
  if testHeavy 1919295716243435678479386069945152552478435377667 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_9/N4/heavy5")
  if indexTable 1919295716243435678479383647370858331797847015939 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/word")
  if testHeavy 1919295716243435678479383647370858331797847015939 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy0")
  if testHeavy 1919295716243435678479383647370858331797847015939 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy1")
  if testHeavy 1919295716243435678479383647370858331797847015939 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy2")
  if testHeavy 1919295716243435678479383647370858331797847015939 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy3")
  if testHeavy 1919295716243435678479383647370858331797847015939 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy4")
  if testHeavy 1919295716243435678479383647370858331797847015939 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N0/heavy5")
  if indexTable 1919295716243435678479383647370858331797847015939 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/word0")
  if indexTable 1919295716243435678479383647370858331797847015939 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/word1")
  if testHeavy 1919295716243435678479383647370858331797847015939 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy0")
  if testHeavy 1919295716243435678479383647370858331797847015939 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy1")
  if testHeavy 1919295716243435678479383647370858331797847015939 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy2")
  if testHeavy 1919295716243435678479383647370858331797847015939 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy3")
  if testHeavy 1919295716243435678479383647370858331797847015939 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy4")
  if testHeavy 1919295716243435678479383647370858331797847015939 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N1/heavy5")
  if indexTable 1919295716243435678479383647370858331797847015939 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/word00")
  if indexTable 1919295716243435678479383647370858331797847015939 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/word01")
  if indexTable 1919295716243435678479383647370858331797847015939 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/word10")
  if indexTable 1919295716243435678479383647370858331797847015939 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/word11")
  if testHeavy 1919295716243435678479383647370858331797847015939 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy0")
  if testHeavy 1919295716243435678479383647370858331797847015939 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy1")
  if testHeavy 1919295716243435678479383647370858331797847015939 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy2")
  if testHeavy 1919295716243435678479383647370858331797847015939 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy3")
  if testHeavy 1919295716243435678479383647370858331797847015939 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy4")
  if testHeavy 1919295716243435678479383647370858331797847015939 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N2/heavy5")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word000")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word001")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word010")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word011")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word100")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word101")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word110")
  if indexTable 1919295716243435678479383647370858331797847015939 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/word111")
  if testHeavy 1919295716243435678479383647370858331797847015939 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy0")
  if testHeavy 1919295716243435678479383647370858331797847015939 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy1")
  if testHeavy 1919295716243435678479383647370858331797847015939 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy2")
  return passed

def batch46 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479383647370858331797847015939 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy3")
  if testHeavy 1919295716243435678479383647370858331797847015939 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy4")
  if testHeavy 1919295716243435678479383647370858331797847015939 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N3/heavy5")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0000")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0001")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0010")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0011")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0100")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0101")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0110")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word0111")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1000")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1001")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1010")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1011")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1100")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1101")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1110")
  if indexTable 1919295716243435678479383647370858331797847015939 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/word1111")
  if testHeavy 1919295716243435678479383647370858331797847015939 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/2-4/k0")
  if testHeavy 1919295716243435678479383647370858331797847015939 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/2-4/k1")
  if testHeavy 1919295716243435678479383647370858331797847015939 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy2")
  if testHeavy 1919295716243435678479383647370858331797847015939 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy3")
  if testHeavy 1919295716243435678479383647370858331797847015939 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-2/k4")
  return passed

def batch47 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479383647370858331797847015939 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/matrix/2-4/k4")
  if testHeavy 1919295716243435678479383647370858331797847015939 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_10/N4/heavy5")
  if indexTable 1919295716243435678479386065222714012036210360834 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/word")
  if testHeavy 1919295716243435678479386065222714012036210360834 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy0")
  if testHeavy 1919295716243435678479386065222714012036210360834 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy1")
  if testHeavy 1919295716243435678479386065222714012036210360834 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy2")
  if testHeavy 1919295716243435678479386065222714012036210360834 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy3")
  if testHeavy 1919295716243435678479386065222714012036210360834 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy4")
  if testHeavy 1919295716243435678479386065222714012036210360834 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N0/heavy5")
  if indexTable 1919295716243435678479386065222714012036210360834 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/word0")
  if indexTable 1919295716243435678479386065222714012036210360834 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/word1")
  if testHeavy 1919295716243435678479386065222714012036210360834 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy0")
  if testHeavy 1919295716243435678479386065222714012036210360834 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy1")
  if testHeavy 1919295716243435678479386065222714012036210360834 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy2")
  if testHeavy 1919295716243435678479386065222714012036210360834 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy3")
  if testHeavy 1919295716243435678479386065222714012036210360834 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy4")
  if testHeavy 1919295716243435678479386065222714012036210360834 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N1/heavy5")
  if indexTable 1919295716243435678479386065222714012036210360834 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/word00")
  if indexTable 1919295716243435678479386065222714012036210360834 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/word01")
  if indexTable 1919295716243435678479386065222714012036210360834 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/word10")
  if indexTable 1919295716243435678479386065222714012036210360834 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/word11")
  if testHeavy 1919295716243435678479386065222714012036210360834 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy0")
  if testHeavy 1919295716243435678479386065222714012036210360834 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy1")
  if testHeavy 1919295716243435678479386065222714012036210360834 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy2")
  if testHeavy 1919295716243435678479386065222714012036210360834 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy3")
  if testHeavy 1919295716243435678479386065222714012036210360834 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy4")
  if testHeavy 1919295716243435678479386065222714012036210360834 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N2/heavy5")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word000")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word001")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word010")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word011")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word100")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word101")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word110")
  if indexTable 1919295716243435678479386065222714012036210360834 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/word111")
  if testHeavy 1919295716243435678479386065222714012036210360834 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy0")
  return passed

def batch48 : IO Nat := do
  let mut passed := 0
  if testHeavy 1919295716243435678479386065222714012036210360834 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy1")
  if testHeavy 1919295716243435678479386065222714012036210360834 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy2")
  if testHeavy 1919295716243435678479386065222714012036210360834 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy3")
  if testHeavy 1919295716243435678479386065222714012036210360834 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy4")
  if testHeavy 1919295716243435678479386065222714012036210360834 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N3/heavy5")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0000")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, false, false, true][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0001")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0010")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0011")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0100")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0101")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0110")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word0111")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1000")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1001")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1010")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1011")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1100")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1101")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1110")
  if indexTable 1919295716243435678479386065222714012036210360834 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/word1111")
  if testHeavy 1919295716243435678479386065222714012036210360834 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/0-1/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-2/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-4/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-1/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-2/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/4-0/k0")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/2-4/k0")
  if testHeavy 1919295716243435678479386065222714012036210360834 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/0-1/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-2/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-4/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-1/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-2/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/4-0/k1")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/2-4/k1")
  if testHeavy 1919295716243435678479386065222714012036210360834 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy2")
  if testHeavy 1919295716243435678479386065222714012036210360834 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy3")
  if testHeavy 1919295716243435678479386065222714012036210360834 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy4")
  return passed

def batch49 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/0-1/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-2/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-4/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/1-1/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/3-2/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/4-0/k4")
  if decide (membershipMatrix 1919295716243435678479386065222714012036210360834 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/matrix/2-4/k4")
  if testHeavy 1919295716243435678479386065222714012036210360834 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL random_11/N4/heavy5")
  if indexTable 0 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/word")
  if testHeavy 0 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy0")
  if testHeavy 0 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy1")
  if testHeavy 0 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy2")
  if testHeavy 0 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy3")
  if testHeavy 0 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy4")
  if testHeavy 0 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N0/heavy5")
  if indexTable 0 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/word0")
  if indexTable 0 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/word1")
  if testHeavy 0 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy0")
  if testHeavy 0 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy1")
  if testHeavy 0 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy2")
  if testHeavy 0 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy3")
  if testHeavy 0 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy4")
  if testHeavy 0 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N1/heavy5")
  if indexTable 0 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/word00")
  if indexTable 0 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/word01")
  if indexTable 0 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/word10")
  if indexTable 0 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/word11")
  if testHeavy 0 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy0")
  if testHeavy 0 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy1")
  if testHeavy 0 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy2")
  if testHeavy 0 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy3")
  if testHeavy 0 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy4")
  if testHeavy 0 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N2/heavy5")
  if indexTable 0 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word000")
  if indexTable 0 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word001")
  if indexTable 0 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word010")
  if indexTable 0 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word011")
  if indexTable 0 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word100")
  if indexTable 0 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word101")
  if indexTable 0 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word110")
  return passed

def batch50 : IO Nat := do
  let mut passed := 0
  if indexTable 0 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/word111")
  if testHeavy 0 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy0")
  if testHeavy 0 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy1")
  if testHeavy 0 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy2")
  if testHeavy 0 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy3")
  if testHeavy 0 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy4")
  if testHeavy 0 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N3/heavy5")
  if indexTable 0 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0000")
  if indexTable 0 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0001")
  if indexTable 0 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0010")
  if indexTable 0 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0011")
  if indexTable 0 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0100")
  if indexTable 0 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0101")
  if indexTable 0 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0110")
  if indexTable 0 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word0111")
  if indexTable 0 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1000")
  if indexTable 0 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1001")
  if indexTable 0 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1010")
  if indexTable 0 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1011")
  if indexTable 0 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1100")
  if indexTable 0 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1101")
  if indexTable 0 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1110")
  if indexTable 0 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/word1111")
  if testHeavy 0 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy0")
  if decide (membershipMatrix 0 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/0-1/k0")
  if decide (membershipMatrix 0 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-2/k0")
  if decide (membershipMatrix 0 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-4/k0")
  if decide (membershipMatrix 0 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-1/k0")
  if decide (membershipMatrix 0 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-2/k0")
  if decide (membershipMatrix 0 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/4-0/k0")
  if decide (membershipMatrix 0 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/2-4/k0")
  if testHeavy 0 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy1")
  if decide (membershipMatrix 0 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/0-1/k1")
  if decide (membershipMatrix 0 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-2/k1")
  if decide (membershipMatrix 0 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-4/k1")
  if decide (membershipMatrix 0 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-1/k1")
  if decide (membershipMatrix 0 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-2/k1")
  if decide (membershipMatrix 0 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/4-0/k1")
  if decide (membershipMatrix 0 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/2-4/k1")
  if testHeavy 0 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy2")
  return passed

def batch51 : IO Nat := do
  let mut passed := 0
  if testHeavy 0 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy3")
  if testHeavy 0 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy4")
  if decide (membershipMatrix 0 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/0-1/k4")
  if decide (membershipMatrix 0 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-2/k4")
  if decide (membershipMatrix 0 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-4/k4")
  if decide (membershipMatrix 0 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/1-1/k4")
  if decide (membershipMatrix 0 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/3-2/k4")
  if decide (membershipMatrix 0 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/4-0/k4")
  if decide (membershipMatrix 0 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/matrix/2-4/k4")
  if testHeavy 0 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_index/N4/heavy5")
  if indexTable 2 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/word")
  if testHeavy 2 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy0")
  if testHeavy 2 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy1")
  if testHeavy 2 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy2")
  if testHeavy 2 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy3")
  if testHeavy 2 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy4")
  if testHeavy 2 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N0/heavy5")
  if indexTable 2 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/word0")
  if indexTable 2 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/word1")
  if testHeavy 2 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy0")
  if testHeavy 2 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy1")
  if testHeavy 2 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy2")
  if testHeavy 2 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy3")
  if testHeavy 2 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy4")
  if testHeavy 2 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N1/heavy5")
  if indexTable 2 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/word00")
  if indexTable 2 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/word01")
  if indexTable 2 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/word10")
  if indexTable 2 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/word11")
  if testHeavy 2 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy0")
  if testHeavy 2 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy1")
  if testHeavy 2 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy2")
  if testHeavy 2 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy3")
  if testHeavy 2 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy4")
  if testHeavy 2 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N2/heavy5")
  if indexTable 2 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word000")
  if indexTable 2 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word001")
  if indexTable 2 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word010")
  if indexTable 2 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word011")
  if indexTable 2 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word100")
  return passed

def batch52 : IO Nat := do
  let mut passed := 0
  if indexTable 2 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word101")
  if indexTable 2 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word110")
  if indexTable 2 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/word111")
  if testHeavy 2 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy0")
  if testHeavy 2 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy1")
  if testHeavy 2 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy2")
  if testHeavy 2 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy3")
  if testHeavy 2 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy4")
  if testHeavy 2 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N3/heavy5")
  if indexTable 2 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0000")
  if indexTable 2 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0001")
  if indexTable 2 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0010")
  if indexTable 2 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0011")
  if indexTable 2 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0100")
  if indexTable 2 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0101")
  if indexTable 2 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0110")
  if indexTable 2 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word0111")
  if indexTable 2 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1000")
  if indexTable 2 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1001")
  if indexTable 2 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1010")
  if indexTable 2 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1011")
  if indexTable 2 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1100")
  if indexTable 2 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1101")
  if indexTable 2 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1110")
  if indexTable 2 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/word1111")
  if testHeavy 2 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy0")
  if decide (membershipMatrix 2 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/0-1/k0")
  if decide (membershipMatrix 2 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-2/k0")
  if decide (membershipMatrix 2 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-4/k0")
  if decide (membershipMatrix 2 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-1/k0")
  if decide (membershipMatrix 2 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-2/k0")
  if decide (membershipMatrix 2 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/4-0/k0")
  if decide (membershipMatrix 2 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/2-4/k0")
  if testHeavy 2 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy1")
  if decide (membershipMatrix 2 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/0-1/k1")
  if decide (membershipMatrix 2 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-2/k1")
  if decide (membershipMatrix 2 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-4/k1")
  if decide (membershipMatrix 2 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-1/k1")
  if decide (membershipMatrix 2 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-2/k1")
  if decide (membershipMatrix 2 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/4-0/k1")
  return passed

def batch53 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 2 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/2-4/k1")
  if testHeavy 2 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy2")
  if testHeavy 2 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy3")
  if testHeavy 2 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy4")
  if decide (membershipMatrix 2 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/0-1/k4")
  if decide (membershipMatrix 2 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-2/k4")
  if decide (membershipMatrix 2 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-4/k4")
  if decide (membershipMatrix 2 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/1-1/k4")
  if decide (membershipMatrix 2 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/3-2/k4")
  if decide (membershipMatrix 2 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/4-0/k4")
  if decide (membershipMatrix 2 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/matrix/2-4/k4")
  if testHeavy 2 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL invalid_sentinel/N4/heavy5")
  if indexTable 1 0 (fun i => #[][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/word")
  if testHeavy 1 0 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy0")
  if testHeavy 1 1 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy1")
  if testHeavy 1 2 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy2")
  if testHeavy 1 3 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy3")
  if testHeavy 1 4 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy4")
  if testHeavy 1 5 0 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N0/heavy5")
  if indexTable 1 1 (fun i => #[false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/word0")
  if indexTable 1 1 (fun i => #[true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/word1")
  if testHeavy 1 0 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy0")
  if testHeavy 1 1 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy1")
  if testHeavy 1 2 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy2")
  if testHeavy 1 3 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy3")
  if testHeavy 1 4 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy4")
  if testHeavy 1 5 1 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N1/heavy5")
  if indexTable 1 2 (fun i => #[false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/word00")
  if indexTable 1 2 (fun i => #[false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/word01")
  if indexTable 1 2 (fun i => #[true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/word10")
  if indexTable 1 2 (fun i => #[true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/word11")
  if testHeavy 1 0 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy0")
  if testHeavy 1 1 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy1")
  if testHeavy 1 2 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy2")
  if testHeavy 1 3 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy3")
  if testHeavy 1 4 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy4")
  if testHeavy 1 5 2 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N2/heavy5")
  if indexTable 1 3 (fun i => #[false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word000")
  if indexTable 1 3 (fun i => #[false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word001")
  if indexTable 1 3 (fun i => #[false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word010")
  return passed

def batch54 : IO Nat := do
  let mut passed := 0
  if indexTable 1 3 (fun i => #[false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word011")
  if indexTable 1 3 (fun i => #[true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word100")
  if indexTable 1 3 (fun i => #[true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word101")
  if indexTable 1 3 (fun i => #[true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word110")
  if indexTable 1 3 (fun i => #[true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/word111")
  if testHeavy 1 0 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy0")
  if testHeavy 1 1 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy1")
  if testHeavy 1 2 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy2")
  if testHeavy 1 3 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy3")
  if testHeavy 1 4 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy4")
  if testHeavy 1 5 3 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N3/heavy5")
  if indexTable 1 4 (fun i => #[false, false, false, false][i.val]!) == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0000")
  if indexTable 1 4 (fun i => #[false, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0001")
  if indexTable 1 4 (fun i => #[false, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0010")
  if indexTable 1 4 (fun i => #[false, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0011")
  if indexTable 1 4 (fun i => #[false, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0100")
  if indexTable 1 4 (fun i => #[false, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0101")
  if indexTable 1 4 (fun i => #[false, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0110")
  if indexTable 1 4 (fun i => #[false, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word0111")
  if indexTable 1 4 (fun i => #[true, false, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1000")
  if indexTable 1 4 (fun i => #[true, false, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1001")
  if indexTable 1 4 (fun i => #[true, false, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1010")
  if indexTable 1 4 (fun i => #[true, false, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1011")
  if indexTable 1 4 (fun i => #[true, true, false, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1100")
  if indexTable 1 4 (fun i => #[true, true, false, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1101")
  if indexTable 1 4 (fun i => #[true, true, true, false][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1110")
  if indexTable 1 4 (fun i => #[true, true, true, true][i.val]!) == (0 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/word1111")
  if testHeavy 1 0 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy0")
  if decide (membershipMatrix 1 (Nat.pair 0 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/0-1/k0")
  if decide (membershipMatrix 1 (Nat.pair 1 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-2/k0")
  if decide (membershipMatrix 1 (Nat.pair 3 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-4/k0")
  if decide (membershipMatrix 1 (Nat.pair 1 1) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-1/k0")
  if decide (membershipMatrix 1 (Nat.pair 3 2) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-2/k0")
  if decide (membershipMatrix 1 (Nat.pair 4 0) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/4-0/k0")
  if decide (membershipMatrix 1 (Nat.pair 2 4) 0 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/2-4/k0")
  if testHeavy 1 1 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy1")
  if decide (membershipMatrix 1 (Nat.pair 0 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/0-1/k1")
  if decide (membershipMatrix 1 (Nat.pair 1 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-2/k1")
  if decide (membershipMatrix 1 (Nat.pair 3 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-4/k1")
  if decide (membershipMatrix 1 (Nat.pair 1 1) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-1/k1")
  return passed

def batch55 : IO Nat := do
  let mut passed := 0
  if decide (membershipMatrix 1 (Nat.pair 3 2) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-2/k1")
  if decide (membershipMatrix 1 (Nat.pair 4 0) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/4-0/k1")
  if decide (membershipMatrix 1 (Nat.pair 2 4) 1 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/2-4/k1")
  if testHeavy 1 2 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy2")
  if testHeavy 1 3 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy3")
  if testHeavy 1 4 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy4")
  if decide (membershipMatrix 1 (Nat.pair 0 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/0-1/k4")
  if decide (membershipMatrix 1 (Nat.pair 1 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-2/k4")
  if decide (membershipMatrix 1 (Nat.pair 3 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-4/k4")
  if decide (membershipMatrix 1 (Nat.pair 1 1) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/1-1/k4")
  if decide (membershipMatrix 1 (Nat.pair 3 2) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/3-2/k4")
  if decide (membershipMatrix 1 (Nat.pair 4 0) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/4-0/k4")
  if decide (membershipMatrix 1 (Nat.pair 2 4) 4 4) == true then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/matrix/2-4/k4")
  if testHeavy 1 5 4 == (1 / 1 : ℚ≥0) then
    passed := passed + 1
  else
    throw (IO.userError "FAIL sentinel_only/N4/heavy5")
  return passed

def main : IO Unit := do
  let mut passed := 0
  passed := passed + (← batch0)
  passed := passed + (← batch1)
  passed := passed + (← batch2)
  passed := passed + (← batch3)
  passed := passed + (← batch4)
  passed := passed + (← batch5)
  passed := passed + (← batch6)
  passed := passed + (← batch7)
  passed := passed + (← batch8)
  passed := passed + (← batch9)
  passed := passed + (← batch10)
  passed := passed + (← batch11)
  passed := passed + (← batch12)
  passed := passed + (← batch13)
  passed := passed + (← batch14)
  passed := passed + (← batch15)
  passed := passed + (← batch16)
  passed := passed + (← batch17)
  passed := passed + (← batch18)
  passed := passed + (← batch19)
  passed := passed + (← batch20)
  passed := passed + (← batch21)
  passed := passed + (← batch22)
  passed := passed + (← batch23)
  passed := passed + (← batch24)
  passed := passed + (← batch25)
  passed := passed + (← batch26)
  passed := passed + (← batch27)
  passed := passed + (← batch28)
  passed := passed + (← batch29)
  passed := passed + (← batch30)
  passed := passed + (← batch31)
  passed := passed + (← batch32)
  passed := passed + (← batch33)
  passed := passed + (← batch34)
  passed := passed + (← batch35)
  passed := passed + (← batch36)
  passed := passed + (← batch37)
  passed := passed + (← batch38)
  passed := passed + (← batch39)
  passed := passed + (← batch40)
  passed := passed + (← batch41)
  passed := passed + (← batch42)
  passed := passed + (← batch43)
  passed := passed + (← batch44)
  passed := passed + (← batch45)
  passed := passed + (← batch46)
  passed := passed + (← batch47)
  passed := passed + (← batch48)
  passed := passed + (← batch49)
  passed := passed + (← batch50)
  passed := passed + (← batch51)
  passed := passed + (← batch52)
  passed := passed + (← batch53)
  passed := passed + (← batch54)
  passed := passed + (← batch55)
  IO.println s!"PASS {passed} exact table, heavy-mass, and numerical matrix differential checks"
