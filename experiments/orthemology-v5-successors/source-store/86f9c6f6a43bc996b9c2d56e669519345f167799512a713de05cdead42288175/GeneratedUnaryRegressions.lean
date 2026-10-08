/- Expected values produced by an independent finite-tree evaluator. -/
import UnaryWitnesses
import UnaryExpressivity
open P01AC.UnaryIdentity
set_option maxRecDepth 8192
set_option maxHeartbeats 2000000
def regression_0 : Expr := (Expr.constant 0)
example : (List.range 11).map (fun n => (normalise regression_0).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_0 (.constant 0)) regression_0 = true := by decide
example : normalise (Expr.reify (normalise regression_0)) = normalise regression_0 := by decide
def regression_1 : Expr := (Expr.add (Expr.ifEq (Expr.ifEq (Expr.constant 3) (Expr.constant 3) Expr.variable Expr.variable) (Expr.ifEq Expr.variable (Expr.constant 1) (Expr.constant 0) Expr.variable) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 2) (Expr.constant 2)) (Expr.mul Expr.variable (Expr.constant 0))) (Expr.ifEq (Expr.ifEq (Expr.constant 0) (Expr.constant 1) (Expr.constant 1) Expr.variable) (Expr.mul Expr.variable Expr.variable) (Expr.mul Expr.variable (Expr.constant 0)) (Expr.constant 0)))
example : (List.range 11).map (fun n => (normalise regression_1).denote n) = [2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide
example : identityCheck (.add regression_1 (.constant 0)) regression_1 = true := by decide
example : normalise (Expr.reify (normalise regression_1)) = normalise regression_1 := by decide
def regression_2 : Expr := (Expr.mul (Expr.constant 2) (Expr.constant 0))
example : (List.range 11).map (fun n => (normalise regression_2).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_2 (.constant 0)) regression_2 = true := by decide
example : normalise (Expr.reify (normalise regression_2)) = normalise regression_2 := by decide
def regression_3 : Expr := (Expr.mul (Expr.mul (Expr.ifEq (Expr.constant 1) (Expr.constant 3) Expr.variable (Expr.constant 2)) (Expr.mul Expr.variable Expr.variable)) (Expr.add (Expr.mul Expr.variable Expr.variable) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 0) (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_3).denote n) = [0, 2, 32, 162, 512, 1250, 2592, 4802, 8192, 13122, 20000] := by decide
example : identityCheck (.add regression_3 (.constant 0)) regression_3 = true := by decide
example : normalise (Expr.reify (normalise regression_3)) = normalise regression_3 := by decide
def regression_4 : Expr := (Expr.ifEq (Expr.constant 2) (Expr.add (Expr.constant 1) Expr.variable) (Expr.mul Expr.variable (Expr.constant 2)) (Expr.ifEq (Expr.constant 1) (Expr.constant 0) (Expr.ifEq Expr.variable (Expr.constant 2) (Expr.constant 0) (Expr.constant 1)) (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_4).denote n) = [0, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_4 (.constant 0)) regression_4 = true := by decide
example : normalise (Expr.reify (normalise regression_4)) = normalise regression_4 := by decide
def regression_5 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_5).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_5 (.constant 0)) regression_5 = true := by decide
example : normalise (Expr.reify (normalise regression_5)) = normalise regression_5 := by decide
def regression_6 : Expr := (Expr.add (Expr.add Expr.variable (Expr.constant 0)) (Expr.ifEq (Expr.mul (Expr.constant 1) Expr.variable) (Expr.mul Expr.variable Expr.variable) Expr.variable (Expr.constant 3)))
example : (List.range 11).map (fun n => (normalise regression_6).denote n) = [0, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13] := by decide
example : identityCheck (.add regression_6 (.constant 0)) regression_6 = true := by decide
example : normalise (Expr.reify (normalise regression_6)) = normalise regression_6 := by decide
def regression_7 : Expr := (Expr.constant 3)
example : (List.range 11).map (fun n => (normalise regression_7).denote n) = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_7 (.constant 0)) regression_7 = true := by decide
example : normalise (Expr.reify (normalise regression_7)) = normalise regression_7 := by decide
def regression_8 : Expr := (Expr.constant 0)
example : (List.range 11).map (fun n => (normalise regression_8).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_8 (.constant 0)) regression_8 = true := by decide
example : normalise (Expr.reify (normalise regression_8)) = normalise regression_8 := by decide
def regression_9 : Expr := (Expr.constant 2)
example : (List.range 11).map (fun n => (normalise regression_9).denote n) = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide
example : identityCheck (.add regression_9 (.constant 0)) regression_9 = true := by decide
example : normalise (Expr.reify (normalise regression_9)) = normalise regression_9 := by decide
def regression_10 : Expr := (Expr.ifEq (Expr.ifEq (Expr.ifEq (Expr.constant 2) Expr.variable (Expr.constant 1) (Expr.constant 3)) (Expr.ifEq (Expr.constant 2) Expr.variable Expr.variable Expr.variable) (Expr.mul Expr.variable Expr.variable) (Expr.constant 3)) (Expr.ifEq Expr.variable Expr.variable (Expr.ifEq Expr.variable Expr.variable (Expr.constant 2) Expr.variable) (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable Expr.variable)) (Expr.mul (Expr.constant 0) (Expr.add (Expr.constant 1) (Expr.constant 2))) Expr.variable)
example : (List.range 11).map (fun n => (normalise regression_10).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_10 (.constant 0)) regression_10 = true := by decide
example : normalise (Expr.reify (normalise regression_10)) = normalise regression_10 := by decide
def regression_11 : Expr := (Expr.ifEq (Expr.mul (Expr.ifEq (Expr.constant 3) Expr.variable Expr.variable Expr.variable) (Expr.mul (Expr.constant 3) (Expr.constant 1))) (Expr.ifEq Expr.variable (Expr.ifEq (Expr.constant 0) (Expr.constant 3) (Expr.constant 3) (Expr.constant 2)) (Expr.ifEq (Expr.constant 0) Expr.variable Expr.variable (Expr.constant 3)) Expr.variable) (Expr.ifEq (Expr.ifEq (Expr.constant 0) Expr.variable (Expr.constant 1) Expr.variable) (Expr.mul Expr.variable (Expr.constant 0)) Expr.variable (Expr.ifEq Expr.variable (Expr.constant 2) Expr.variable Expr.variable)) (Expr.mul (Expr.mul (Expr.constant 3) (Expr.constant 1)) (Expr.ifEq Expr.variable (Expr.constant 2) Expr.variable (Expr.constant 1))))
example : (List.range 11).map (fun n => (normalise regression_11).denote n) = [0, 3, 6, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_11 (.constant 0)) regression_11 = true := by decide
example : normalise (Expr.reify (normalise regression_11)) = normalise regression_11 := by decide
def regression_12 : Expr := (Expr.ifEq (Expr.mul (Expr.add (Expr.constant 2) Expr.variable) (Expr.add (Expr.constant 0) (Expr.constant 3))) (Expr.ifEq Expr.variable (Expr.add Expr.variable Expr.variable) (Expr.constant 3) (Expr.ifEq (Expr.constant 3) (Expr.constant 3) Expr.variable Expr.variable)) (Expr.mul (Expr.ifEq (Expr.constant 1) Expr.variable (Expr.constant 0) Expr.variable) (Expr.ifEq (Expr.constant 0) (Expr.constant 2) Expr.variable (Expr.constant 3))) (Expr.mul (Expr.mul Expr.variable Expr.variable) (Expr.constant 0)))
example : (List.range 11).map (fun n => (normalise regression_12).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_12 (.constant 0)) regression_12 = true := by decide
example : normalise (Expr.reify (normalise regression_12)) = normalise regression_12 := by decide
def regression_13 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_13).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_13 (.constant 0)) regression_13 = true := by decide
example : normalise (Expr.reify (normalise regression_13)) = normalise regression_13 := by decide
def regression_14 : Expr := (Expr.add (Expr.constant 1) (Expr.constant 1))
example : (List.range 11).map (fun n => (normalise regression_14).denote n) = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide
example : identityCheck (.add regression_14 (.constant 0)) regression_14 = true := by decide
example : normalise (Expr.reify (normalise regression_14)) = normalise regression_14 := by decide
def regression_15 : Expr := (Expr.ifEq (Expr.ifEq Expr.variable (Expr.constant 1) (Expr.ifEq Expr.variable (Expr.constant 2) Expr.variable (Expr.constant 2)) (Expr.ifEq Expr.variable (Expr.constant 1) (Expr.constant 1) (Expr.constant 1))) (Expr.ifEq (Expr.constant 1) (Expr.mul (Expr.constant 2) Expr.variable) (Expr.constant 0) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 1) (Expr.constant 1))) (Expr.ifEq Expr.variable (Expr.ifEq (Expr.constant 3) (Expr.constant 1) (Expr.constant 1) Expr.variable) (Expr.add Expr.variable Expr.variable) (Expr.ifEq (Expr.constant 0) Expr.variable Expr.variable (Expr.constant 1))) (Expr.add (Expr.add (Expr.constant 0) Expr.variable) (Expr.ifEq (Expr.constant 1) Expr.variable (Expr.constant 3) Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_15).denote n) = [0, 4, 4, 6, 8, 10, 12, 14, 16, 18, 20] := by decide
example : identityCheck (.add regression_15 (.constant 0)) regression_15 = true := by decide
example : normalise (Expr.reify (normalise regression_15)) = normalise regression_15 := by decide
def regression_16 : Expr := (Expr.ifEq (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 1)) Expr.variable (Expr.constant 0) (Expr.mul (Expr.constant 0) Expr.variable)) Expr.variable (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable (Expr.constant 1) (Expr.constant 2)) (Expr.ifEq Expr.variable (Expr.constant 2) Expr.variable Expr.variable) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 2) (Expr.constant 2)) (Expr.add (Expr.constant 2) Expr.variable)) (Expr.mul Expr.variable (Expr.ifEq Expr.variable (Expr.constant 1) Expr.variable Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_16).denote n) = [2, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100] := by decide
example : identityCheck (.add regression_16 (.constant 0)) regression_16 = true := by decide
example : normalise (Expr.reify (normalise regression_16)) = normalise regression_16 := by decide
def regression_17 : Expr := (Expr.mul (Expr.add Expr.variable Expr.variable) (Expr.ifEq (Expr.add Expr.variable (Expr.constant 2)) (Expr.add Expr.variable Expr.variable) (Expr.add (Expr.constant 1) Expr.variable) (Expr.mul (Expr.constant 0) Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_17).denote n) = [0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_17 (.constant 0)) regression_17 = true := by decide
example : normalise (Expr.reify (normalise regression_17)) = normalise regression_17 := by decide
def regression_18 : Expr := (Expr.ifEq Expr.variable (Expr.ifEq (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable (Expr.constant 3)) (Expr.mul (Expr.constant 0) Expr.variable) Expr.variable (Expr.ifEq (Expr.constant 2) Expr.variable (Expr.constant 0) Expr.variable)) Expr.variable (Expr.add Expr.variable (Expr.constant 1)))
example : (List.range 11).map (fun n => (normalise regression_18).denote n) = [0, 1, 3, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_18 (.constant 0)) regression_18 = true := by decide
example : normalise (Expr.reify (normalise regression_18)) = normalise regression_18 := by decide
def regression_19 : Expr := (Expr.mul (Expr.add (Expr.constant 1) (Expr.ifEq Expr.variable (Expr.constant 0) (Expr.constant 3) Expr.variable)) (Expr.mul (Expr.ifEq Expr.variable Expr.variable (Expr.constant 3) Expr.variable) (Expr.ifEq (Expr.constant 2) (Expr.constant 1) Expr.variable Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_19).denote n) = [0, 6, 18, 36, 60, 90, 126, 168, 216, 270, 330] := by decide
example : identityCheck (.add regression_19 (.constant 0)) regression_19 = true := by decide
example : normalise (Expr.reify (normalise regression_19)) = normalise regression_19 := by decide
def regression_20 : Expr := (Expr.mul (Expr.constant 0) (Expr.ifEq (Expr.constant 3) Expr.variable (Expr.ifEq Expr.variable (Expr.constant 3) (Expr.constant 1) (Expr.constant 1)) (Expr.add Expr.variable (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_20).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_20 (.constant 0)) regression_20 = true := by decide
example : normalise (Expr.reify (normalise regression_20)) = normalise regression_20 := by decide
def regression_21 : Expr := (Expr.mul (Expr.mul (Expr.mul Expr.variable (Expr.constant 1)) (Expr.ifEq (Expr.constant 3) Expr.variable (Expr.constant 0) (Expr.constant 0))) Expr.variable)
example : (List.range 11).map (fun n => (normalise regression_21).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_21 (.constant 0)) regression_21 = true := by decide
example : normalise (Expr.reify (normalise regression_21)) = normalise regression_21 := by decide
def regression_22 : Expr := (Expr.add (Expr.mul (Expr.constant 1) Expr.variable) Expr.variable)
example : (List.range 11).map (fun n => (normalise regression_22).denote n) = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20] := by decide
example : identityCheck (.add regression_22 (.constant 0)) regression_22 = true := by decide
example : normalise (Expr.reify (normalise regression_22)) = normalise regression_22 := by decide
def regression_23 : Expr := (Expr.ifEq (Expr.add (Expr.ifEq Expr.variable (Expr.constant 1) Expr.variable Expr.variable) (Expr.mul (Expr.constant 0) Expr.variable)) (Expr.add (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable) (Expr.ifEq (Expr.constant 0) Expr.variable Expr.variable (Expr.constant 1))) (Expr.add (Expr.constant 2) (Expr.mul Expr.variable Expr.variable)) (Expr.constant 1))
example : (List.range 11).map (fun n => (normalise regression_23).denote n) = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_23 (.constant 0)) regression_23 = true := by decide
example : normalise (Expr.reify (normalise regression_23)) = normalise regression_23 := by decide
def regression_24 : Expr := (Expr.constant 0)
example : (List.range 11).map (fun n => (normalise regression_24).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_24 (.constant 0)) regression_24 = true := by decide
example : normalise (Expr.reify (normalise regression_24)) = normalise regression_24 := by decide
def regression_25 : Expr := (Expr.mul (Expr.constant 0) (Expr.ifEq (Expr.ifEq (Expr.constant 1) (Expr.constant 3) Expr.variable Expr.variable) (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable (Expr.constant 3)) (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable) (Expr.ifEq (Expr.constant 3) Expr.variable (Expr.constant 1) (Expr.constant 3))))
example : (List.range 11).map (fun n => (normalise regression_25).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_25 (.constant 0)) regression_25 = true := by decide
example : normalise (Expr.reify (normalise regression_25)) = normalise regression_25 := by decide
def regression_26 : Expr := (Expr.ifEq (Expr.ifEq (Expr.constant 1) (Expr.ifEq (Expr.constant 3) (Expr.constant 1) (Expr.constant 0) (Expr.constant 2)) (Expr.add (Expr.constant 2) (Expr.constant 3)) (Expr.constant 3)) (Expr.constant 0) (Expr.mul (Expr.add (Expr.constant 1) (Expr.constant 2)) Expr.variable) (Expr.add Expr.variable Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_26).denote n) = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20] := by decide
example : identityCheck (.add regression_26 (.constant 0)) regression_26 = true := by decide
example : normalise (Expr.reify (normalise regression_26)) = normalise regression_26 := by decide
def regression_27 : Expr := (Expr.add (Expr.constant 1) (Expr.ifEq (Expr.mul (Expr.constant 2) (Expr.constant 0)) Expr.variable (Expr.constant 3) Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_27).denote n) = [4, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] := by decide
example : identityCheck (.add regression_27 (.constant 0)) regression_27 = true := by decide
example : normalise (Expr.reify (normalise regression_27)) = normalise regression_27 := by decide
def regression_28 : Expr := (Expr.constant 0)
example : (List.range 11).map (fun n => (normalise regression_28).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_28 (.constant 0)) regression_28 = true := by decide
example : normalise (Expr.reify (normalise regression_28)) = normalise regression_28 := by decide
def regression_29 : Expr := (Expr.ifEq (Expr.mul (Expr.add (Expr.constant 1) Expr.variable) (Expr.add Expr.variable Expr.variable)) (Expr.ifEq (Expr.ifEq Expr.variable (Expr.constant 1) (Expr.constant 1) (Expr.constant 0)) (Expr.ifEq (Expr.constant 1) (Expr.constant 0) (Expr.constant 0) Expr.variable) Expr.variable (Expr.add (Expr.constant 1) Expr.variable)) (Expr.mul (Expr.ifEq (Expr.constant 1) Expr.variable (Expr.constant 0) Expr.variable) (Expr.constant 3)) (Expr.constant 2))
example : (List.range 11).map (fun n => (normalise regression_29).denote n) = [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide
example : identityCheck (.add regression_29 (.constant 0)) regression_29 = true := by decide
example : normalise (Expr.reify (normalise regression_29)) = normalise regression_29 := by decide
def regression_30 : Expr := (Expr.mul (Expr.constant 1) Expr.variable)
example : (List.range 11).map (fun n => (normalise regression_30).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_30 (.constant 0)) regression_30 = true := by decide
example : normalise (Expr.reify (normalise regression_30)) = normalise regression_30 := by decide
def regression_31 : Expr := (Expr.add (Expr.mul (Expr.constant 3) (Expr.add Expr.variable (Expr.constant 1))) (Expr.constant 3))
example : (List.range 11).map (fun n => (normalise regression_31).denote n) = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36] := by decide
example : identityCheck (.add regression_31 (.constant 0)) regression_31 = true := by decide
example : normalise (Expr.reify (normalise regression_31)) = normalise regression_31 := by decide
def regression_32 : Expr := (Expr.constant 1)
example : (List.range 11).map (fun n => (normalise regression_32).denote n) = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_32 (.constant 0)) regression_32 = true := by decide
example : normalise (Expr.reify (normalise regression_32)) = normalise regression_32 := by decide
def regression_33 : Expr := (Expr.mul Expr.variable (Expr.mul (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 0)) (Expr.constant 1)))
example : (List.range 11).map (fun n => (normalise regression_33).denote n) = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100] := by decide
example : identityCheck (.add regression_33 (.constant 0)) regression_33 = true := by decide
example : normalise (Expr.reify (normalise regression_33)) = normalise regression_33 := by decide
def regression_34 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_34).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_34 (.constant 0)) regression_34 = true := by decide
example : normalise (Expr.reify (normalise regression_34)) = normalise regression_34 := by decide
def regression_35 : Expr := (Expr.constant 0)
example : (List.range 11).map (fun n => (normalise regression_35).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_35 (.constant 0)) regression_35 = true := by decide
example : normalise (Expr.reify (normalise regression_35)) = normalise regression_35 := by decide
def regression_36 : Expr := (Expr.add (Expr.mul (Expr.add Expr.variable Expr.variable) (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable)) (Expr.ifEq (Expr.constant 3) (Expr.mul (Expr.constant 1) Expr.variable) (Expr.add (Expr.constant 1) Expr.variable) (Expr.ifEq (Expr.constant 1) (Expr.constant 3) Expr.variable (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_36).denote n) = [0, 2, 8, 22, 32, 50, 72, 98, 128, 162, 200] := by decide
example : identityCheck (.add regression_36 (.constant 0)) regression_36 = true := by decide
example : normalise (Expr.reify (normalise regression_36)) = normalise regression_36 := by decide
def regression_37 : Expr := (Expr.constant 3)
example : (List.range 11).map (fun n => (normalise regression_37).denote n) = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_37 (.constant 0)) regression_37 = true := by decide
example : normalise (Expr.reify (normalise regression_37)) = normalise regression_37 := by decide
def regression_38 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_38).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_38 (.constant 0)) regression_38 = true := by decide
example : normalise (Expr.reify (normalise regression_38)) = normalise regression_38 := by decide
def regression_39 : Expr := (Expr.constant 1)
example : (List.range 11).map (fun n => (normalise regression_39).denote n) = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_39 (.constant 0)) regression_39 = true := by decide
example : normalise (Expr.reify (normalise regression_39)) = normalise regression_39 := by decide
def regression_40 : Expr := (Expr.ifEq Expr.variable (Expr.mul (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable Expr.variable) (Expr.constant 2)) (Expr.ifEq (Expr.ifEq (Expr.constant 2) Expr.variable (Expr.constant 0) (Expr.constant 2)) Expr.variable (Expr.add (Expr.constant 1) Expr.variable) (Expr.constant 0)) (Expr.ifEq (Expr.ifEq Expr.variable (Expr.constant 1) Expr.variable (Expr.constant 1)) (Expr.add Expr.variable Expr.variable) Expr.variable (Expr.add Expr.variable (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_40).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_40 (.constant 0)) regression_40 = true := by decide
example : normalise (Expr.reify (normalise regression_40)) = normalise regression_40 := by decide
def regression_41 : Expr := (Expr.constant 2)
example : (List.range 11).map (fun n => (normalise regression_41).denote n) = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide
example : identityCheck (.add regression_41 (.constant 0)) regression_41 = true := by decide
example : normalise (Expr.reify (normalise regression_41)) = normalise regression_41 := by decide
def regression_42 : Expr := (Expr.constant 3)
example : (List.range 11).map (fun n => (normalise regression_42).denote n) = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_42 (.constant 0)) regression_42 = true := by decide
example : normalise (Expr.reify (normalise regression_42)) = normalise regression_42 := by decide
def regression_43 : Expr := (Expr.add (Expr.ifEq Expr.variable (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable (Expr.constant 1)) (Expr.mul Expr.variable Expr.variable) (Expr.mul (Expr.constant 1) (Expr.constant 0))) (Expr.add (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable (Expr.constant 2)) (Expr.add (Expr.constant 0) Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_43).denote n) = [2, 4, 4, 6, 6, 7, 8, 9, 10, 11, 12] := by decide
example : identityCheck (.add regression_43 (.constant 0)) regression_43 = true := by decide
example : normalise (Expr.reify (normalise regression_43)) = normalise regression_43 := by decide
def regression_44 : Expr := (Expr.ifEq (Expr.mul (Expr.ifEq (Expr.constant 3) Expr.variable (Expr.constant 2) (Expr.constant 0)) (Expr.add (Expr.constant 1) (Expr.constant 2))) (Expr.mul (Expr.ifEq (Expr.constant 1) Expr.variable (Expr.constant 2) (Expr.constant 0)) (Expr.add (Expr.constant 3) (Expr.constant 0))) (Expr.mul Expr.variable (Expr.constant 0)) (Expr.mul (Expr.constant 2) Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_44).denote n) = [0, 2, 0, 6, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_44 (.constant 0)) regression_44 = true := by decide
example : normalise (Expr.reify (normalise regression_44)) = normalise regression_44 := by decide
def regression_45 : Expr := (Expr.ifEq (Expr.add Expr.variable (Expr.add (Expr.constant 1) Expr.variable)) Expr.variable (Expr.mul Expr.variable (Expr.mul (Expr.constant 1) Expr.variable)) (Expr.ifEq (Expr.ifEq (Expr.constant 3) (Expr.constant 2) (Expr.constant 2) (Expr.constant 2)) (Expr.mul (Expr.constant 3) Expr.variable) (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable Expr.variable) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 3) (Expr.constant 0))))
example : (List.range 11).map (fun n => (normalise regression_45).denote n) = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_45 (.constant 0)) regression_45 = true := by decide
example : normalise (Expr.reify (normalise regression_45)) = normalise regression_45 := by decide
def regression_46 : Expr := (Expr.add (Expr.add (Expr.mul Expr.variable Expr.variable) (Expr.add Expr.variable Expr.variable)) (Expr.constant 1))
example : (List.range 11).map (fun n => (normalise regression_46).denote n) = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121] := by decide
example : identityCheck (.add regression_46 (.constant 0)) regression_46 = true := by decide
example : normalise (Expr.reify (normalise regression_46)) = normalise regression_46 := by decide
def regression_47 : Expr := (Expr.add (Expr.ifEq (Expr.add Expr.variable (Expr.constant 0)) (Expr.ifEq (Expr.constant 2) Expr.variable Expr.variable (Expr.constant 2)) (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable (Expr.constant 0)) (Expr.ifEq Expr.variable (Expr.constant 3) (Expr.constant 3) Expr.variable)) (Expr.mul (Expr.constant 0) Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_47).denote n) = [0, 1, 0, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_47 (.constant 0)) regression_47 = true := by decide
example : normalise (Expr.reify (normalise regression_47)) = normalise regression_47 := by decide
def regression_48 : Expr := (Expr.constant 3)
example : (List.range 11).map (fun n => (normalise regression_48).denote n) = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_48 (.constant 0)) regression_48 = true := by decide
example : normalise (Expr.reify (normalise regression_48)) = normalise regression_48 := by decide
def regression_49 : Expr := (Expr.add (Expr.mul (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable Expr.variable) Expr.variable) (Expr.ifEq (Expr.ifEq (Expr.constant 2) (Expr.constant 1) (Expr.constant 2) Expr.variable) Expr.variable Expr.variable Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_49).denote n) = [0, 2, 6, 12, 20, 30, 42, 56, 72, 90, 110] := by decide
example : identityCheck (.add regression_49 (.constant 0)) regression_49 = true := by decide
example : normalise (Expr.reify (normalise regression_49)) = normalise regression_49 := by decide
def regression_50 : Expr := (Expr.ifEq (Expr.ifEq (Expr.add (Expr.constant 1) (Expr.constant 3)) (Expr.ifEq Expr.variable (Expr.constant 2) (Expr.constant 1) Expr.variable) (Expr.constant 2) (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable)) (Expr.constant 2) (Expr.add (Expr.ifEq (Expr.constant 0) (Expr.constant 0) Expr.variable Expr.variable) Expr.variable) (Expr.ifEq (Expr.ifEq (Expr.constant 2) (Expr.constant 0) (Expr.constant 3) (Expr.constant 2)) (Expr.mul Expr.variable (Expr.constant 0)) (Expr.ifEq (Expr.constant 1) Expr.variable (Expr.constant 1) (Expr.constant 0)) (Expr.constant 3)))
example : (List.range 11).map (fun n => (normalise regression_50).denote n) = [3, 3, 4, 3, 8, 3, 3, 3, 3, 3, 3] := by decide
example : identityCheck (.add regression_50 (.constant 0)) regression_50 = true := by decide
example : normalise (Expr.reify (normalise regression_50)) = normalise regression_50 := by decide
def regression_51 : Expr := (Expr.ifEq (Expr.ifEq (Expr.ifEq (Expr.constant 1) (Expr.constant 0) (Expr.constant 3) Expr.variable) (Expr.mul (Expr.constant 2) (Expr.constant 0)) (Expr.constant 0) (Expr.ifEq Expr.variable Expr.variable (Expr.constant 2) (Expr.constant 0))) Expr.variable (Expr.add (Expr.mul Expr.variable Expr.variable) (Expr.mul (Expr.constant 1) Expr.variable)) (Expr.add (Expr.add Expr.variable (Expr.constant 2)) Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_51).denote n) = [0, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22] := by decide
example : identityCheck (.add regression_51 (.constant 0)) regression_51 = true := by decide
example : normalise (Expr.reify (normalise regression_51)) = normalise regression_51 := by decide
def regression_52 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_52).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_52 (.constant 0)) regression_52 = true := by decide
example : normalise (Expr.reify (normalise regression_52)) = normalise regression_52 := by decide
def regression_53 : Expr := (Expr.ifEq (Expr.add Expr.variable (Expr.mul Expr.variable (Expr.constant 1))) (Expr.mul (Expr.ifEq Expr.variable (Expr.constant 0) (Expr.constant 1) Expr.variable) (Expr.add Expr.variable Expr.variable)) (Expr.mul (Expr.mul Expr.variable (Expr.constant 1)) (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 1))) (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable) (Expr.add (Expr.constant 2) Expr.variable) (Expr.mul Expr.variable Expr.variable) (Expr.add Expr.variable Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_53).denote n) = [0, 1, 4, 6, 8, 10, 12, 14, 16, 18, 20] := by decide
example : identityCheck (.add regression_53 (.constant 0)) regression_53 = true := by decide
example : normalise (Expr.reify (normalise regression_53)) = normalise regression_53 := by decide
def regression_54 : Expr := (Expr.add (Expr.ifEq Expr.variable (Expr.mul Expr.variable (Expr.constant 1)) (Expr.constant 0) (Expr.mul Expr.variable Expr.variable)) (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable (Expr.constant 1) (Expr.constant 3)) (Expr.mul (Expr.constant 1) (Expr.constant 2)) (Expr.constant 2) (Expr.constant 1)))
example : (List.range 11).map (fun n => (normalise regression_54).denote n) = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_54 (.constant 0)) regression_54 = true := by decide
example : normalise (Expr.reify (normalise regression_54)) = normalise regression_54 := by decide
def regression_55 : Expr := (Expr.mul Expr.variable (Expr.mul (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable Expr.variable) (Expr.constant 3)))
example : (List.range 11).map (fun n => (normalise regression_55).denote n) = [0, 3, 12, 27, 48, 75, 108, 147, 192, 243, 300] := by decide
example : identityCheck (.add regression_55 (.constant 0)) regression_55 = true := by decide
example : normalise (Expr.reify (normalise regression_55)) = normalise regression_55 := by decide
def regression_56 : Expr := (Expr.add Expr.variable (Expr.constant 3))
example : (List.range 11).map (fun n => (normalise regression_56).denote n) = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] := by decide
example : identityCheck (.add regression_56 (.constant 0)) regression_56 = true := by decide
example : normalise (Expr.reify (normalise regression_56)) = normalise regression_56 := by decide
def regression_57 : Expr := (Expr.ifEq (Expr.ifEq Expr.variable (Expr.mul Expr.variable Expr.variable) (Expr.constant 0) (Expr.ifEq (Expr.constant 0) (Expr.constant 3) (Expr.constant 0) Expr.variable)) (Expr.constant 2) (Expr.add Expr.variable (Expr.ifEq Expr.variable Expr.variable Expr.variable Expr.variable)) (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 1)) (Expr.mul Expr.variable Expr.variable) (Expr.mul (Expr.constant 0) (Expr.constant 0)) (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable (Expr.constant 1))))
example : (List.range 11).map (fun n => (normalise regression_57).denote n) = [0, 0, 4, 3, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_57 (.constant 0)) regression_57 = true := by decide
example : normalise (Expr.reify (normalise regression_57)) = normalise regression_57 := by decide
def regression_58 : Expr := (Expr.mul (Expr.ifEq (Expr.ifEq (Expr.constant 3) Expr.variable Expr.variable (Expr.constant 0)) (Expr.ifEq (Expr.constant 3) (Expr.constant 1) Expr.variable Expr.variable) Expr.variable (Expr.ifEq (Expr.constant 1) (Expr.constant 2) (Expr.constant 2) (Expr.constant 0))) (Expr.ifEq Expr.variable (Expr.mul (Expr.constant 2) Expr.variable) (Expr.add Expr.variable Expr.variable) Expr.variable))
example : (List.range 11).map (fun n => (normalise regression_58).denote n) = [0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_58 (.constant 0)) regression_58 = true := by decide
example : normalise (Expr.reify (normalise regression_58)) = normalise regression_58 := by decide
def regression_59 : Expr := (Expr.ifEq (Expr.ifEq (Expr.ifEq Expr.variable (Expr.constant 3) Expr.variable Expr.variable) (Expr.add (Expr.constant 3) Expr.variable) Expr.variable (Expr.add Expr.variable (Expr.constant 3))) (Expr.ifEq (Expr.mul Expr.variable (Expr.constant 3)) Expr.variable (Expr.mul (Expr.constant 2) Expr.variable) (Expr.ifEq (Expr.constant 1) Expr.variable Expr.variable (Expr.constant 2))) (Expr.mul (Expr.ifEq Expr.variable Expr.variable (Expr.constant 1) Expr.variable) Expr.variable) Expr.variable)
example : (List.range 11).map (fun n => (normalise regression_59).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_59 (.constant 0)) regression_59 = true := by decide
example : normalise (Expr.reify (normalise regression_59)) = normalise regression_59 := by decide
def regression_60 : Expr := (Expr.ifEq (Expr.constant 0) (Expr.ifEq Expr.variable (Expr.ifEq Expr.variable Expr.variable (Expr.constant 0) Expr.variable) (Expr.ifEq (Expr.constant 0) Expr.variable Expr.variable Expr.variable) (Expr.add Expr.variable Expr.variable)) Expr.variable (Expr.constant 0))
example : (List.range 11).map (fun n => (normalise regression_60).denote n) = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] := by decide
example : identityCheck (.add regression_60 (.constant 0)) regression_60 = true := by decide
example : normalise (Expr.reify (normalise regression_60)) = normalise regression_60 := by decide
def regression_61 : Expr := (Expr.add (Expr.mul (Expr.constant 3) (Expr.constant 1)) (Expr.ifEq Expr.variable (Expr.constant 3) (Expr.ifEq Expr.variable (Expr.constant 2) Expr.variable (Expr.constant 3)) (Expr.ifEq (Expr.constant 2) Expr.variable Expr.variable Expr.variable)))
example : (List.range 11).map (fun n => (normalise regression_61).denote n) = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] := by decide
example : identityCheck (.add regression_61 (.constant 0)) regression_61 = true := by decide
example : normalise (Expr.reify (normalise regression_61)) = normalise regression_61 := by decide
def regression_62 : Expr := Expr.variable
example : (List.range 11).map (fun n => (normalise regression_62).denote n) = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] := by decide
example : identityCheck (.add regression_62 (.constant 0)) regression_62 = true := by decide
example : normalise (Expr.reify (normalise regression_62)) = normalise regression_62 := by decide
def regression_63 : Expr := (Expr.ifEq (Expr.ifEq (Expr.constant 2) Expr.variable (Expr.ifEq Expr.variable Expr.variable (Expr.constant 3) Expr.variable) (Expr.constant 1)) (Expr.add (Expr.mul Expr.variable Expr.variable) Expr.variable) (Expr.constant 1) (Expr.ifEq (Expr.ifEq Expr.variable Expr.variable Expr.variable (Expr.constant 2)) (Expr.ifEq Expr.variable (Expr.constant 0) Expr.variable Expr.variable) (Expr.constant 1) (Expr.constant 3)))
example : (List.range 11).map (fun n => (normalise regression_63).denote n) = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] := by decide
example : identityCheck (.add regression_63 (.constant 0)) regression_63 = true := by decide
example : normalise (Expr.reify (normalise regression_63)) = normalise regression_63 := by decide
