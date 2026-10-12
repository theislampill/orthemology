import Sigma2Compiled
open P02A2.ObserverCore P02A2.Sigma2Compiled
open Lean
namespace IndependentAstComparison
def ej : P02A2.ObserverCore.Expr → Json
  | .constant n => toJson ("c", n)
  | .reg r => toJson ("v", r)
  | .add a b => .arr #[toJson "add", ej a, ej b]
  | .sub a b => .arr #[toJson "sub", ej a, ej b]
  | .mul a b => .arr #[toJson "mul", ej a, ej b]
  | .div a b => .arr #[toJson "div", ej a, ej b]
  | .mod a b => .arr #[toJson "mod", ej a, ej b]
  | .le a b => .arr #[toJson "le", ej a, ej b]
  | .eq a b => .arr #[toJson "eq", ej a, ej b]
  | .pow2 a => .arr #[toJson "pow2", ej a]
def sj : Stmt → List Json
  | .skip => []
  | .seq s t => sj s ++ sj t
  | .set r e => [.arr #[toJson "set", toJson r, ej e]]
  | .loop r e s => [.arr #[toJson "loop", toJson r, ej e, .arr (sj s).toArray]]
  | .branch e s t => [.arr #[toJson "if", ej e, .arr (sj s).toArray, .arr (sj t).toArray]]
#eval IO.println ((Json.arr (sj (compiled (.set 3 (.constant 1)) 3 0)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 3 (.le (.reg 2) (.reg 1))) 3 7)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 0 14)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.set 1 (.constant 9)) (.seq (.set 37 (.add (.reg 0) (.reg 2))) .skip)) 37 21)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.branch (.mul (.le (.reg 37) (.constant 4)) (.div (.reg 17) (.reg 0))) .skip (.branch (.mod (.reg 10) (.reg 17)) (.branch (.add (.eq (.reg 8) (.constant 5)) (.sub (.reg 17) (.constant 4))) (.set 6 (.pow2 (.constant 3))) (.set 0 (.mod (.reg 8) (.reg 5)))) (.loop 5 (.pow2 (.constant 4)) (.set 4 (.mul (.reg 101) (.le (.reg 17) (.constant 0))))))) 7 28)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.loop 17 (.reg 0) .skip) (.seq (.loop 1 (.add (.reg 8) (.reg 10)) .skip) .skip)) 4 35)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.branch (.reg 37) (.loop 5 (.mod (.reg 0) (.reg 10)) (.loop 11 (.add (.reg 4) (.constant 6)) (.set 7 (.mod (.eq (.reg 37) (.constant 0)) (.mod (.reg 9) (.reg 1)))))) (.branch (.mul (.pow2 (.reg 37)) (.add (.constant 2) (.constant 2))) (.set 1 (.pow2 (.constant 2))) (.seq (.set 6 (.eq (.div (.reg 9) (.reg 9)) (.sub (.constant 3) (.reg 9)))) (.seq (.set 9 (.pow2 (.le (.reg 101) (.reg 10)))) .skip)))) 6 42)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 17 49)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 7 56)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.loop 37 (.constant 6) (.branch (.add (.mod (.reg 6) (.constant 6)) (.eq (.reg 2) (.constant 6))) (.seq (.set 0 (.div (.mod (.reg 101) (.constant 1)) (.div (.reg 101) (.reg 9)))) (.seq (.set 11 (.pow2 (.reg 3))) .skip)) (.loop 6 (.constant 3) (.set 37 (.le (.mul (.constant 6) (.reg 11)) (.mod (.reg 1) (.constant 0))))))) 7 63)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 6 (.pow2 (.reg 10))) 1 70)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 9 (.eq (.reg 9) (.sub (.reg 10) (.reg 2)))) 37 77)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 1 84)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 6 91)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.branch (.add (.constant 2) (.mul (.reg 101) (.reg 3))) (.loop 10 (.eq (.constant 4) (.reg 5)) (.set 2 (.sub (.div (.constant 4) (.reg 7)) (.mod (.reg 37) (.reg 2))))) (.set 3 (.reg 37))) (.seq (.set 10 (.pow2 (.mul (.reg 1) (.constant 2)))) .skip)) 8 98)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.loop 2 (.constant 1) (.set 101 (.mod (.le (.constant 4) (.reg 10)) (.reg 1)))) 8 105)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.loop 101 (.constant 3) (.branch (.pow2 (.eq (.reg 9) (.reg 10))) (.branch (.reg 9) (.set 9 (.pow2 (.pow2 (.constant 3)))) (.set 10 (.le (.pow2 (.reg 0)) (.le (.reg 8) (.constant 3))))) (.loop 8 (.reg 3) (.set 1 (.mul (.mul (.reg 37) (.reg 11)) (.le (.reg 1) (.reg 7))))))) 101 112)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.loop 1 (.sub (.reg 8) (.reg 9)) (.branch (.le (.mod (.constant 2) (.constant 1)) (.reg 11)) (.set 11 (.le (.reg 37) (.reg 1))) (.set 10 (.sub (.add (.constant 2) (.reg 4)) (.mod (.reg 3) (.constant 1)))))) (.seq (.seq (.set 6 (.le (.le (.reg 6) (.reg 6)) (.mul (.reg 6) (.reg 7)))) (.seq (.set 7 (.sub (.le (.reg 11) (.reg 3)) (.reg 4))) .skip)) .skip)) 0 119)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.seq (.branch (.mod (.reg 8) (.le (.reg 9) (.reg 101))) (.set 9 (.mod (.constant 1) (.pow2 (.reg 10)))) (.set 10 (.pow2 (.pow2 (.constant 4))))) (.seq (.loop 101 (.le (.reg 2) (.reg 37)) (.set 7 (.le (.mul (.constant 1) (.reg 6)) (.mod (.reg 3) (.reg 0))))) .skip)) (.seq .skip .skip)) 3 126)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.seq (.branch (.sub (.div (.constant 6) (.constant 4)) (.reg 37)) (.set 5 (.sub (.reg 2) (.div (.reg 4) (.constant 3)))) (.set 4 (.pow2 (.le (.reg 5) (.constant 1))))) (.seq (.set 6 (.reg 3)) .skip)) (.seq (.seq .skip (.seq (.set 10 (.eq (.le (.reg 6) (.constant 3)) (.pow2 (.reg 1)))) .skip)) .skip)) 101 133)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 8 140)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 1 (.le (.le (.reg 9) (.reg 4)) (.reg 8))) 9 147)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 4 154)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled .skip 101 161)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.loop 5 (.reg 1) (.loop 0 (.div (.reg 3) (.reg 4)) (.set 5 (.add (.constant 6) (.eq (.reg 10) (.constant 1)))))) (.seq (.branch (.eq (.div (.reg 101) (.constant 3)) (.reg 101)) (.branch (.constant 6) (.set 17 (.sub (.add (.reg 6) (.reg 17)) (.reg 37))) (.set 17 (.mod (.constant 5) (.pow2 (.constant 0))))) (.loop 17 (.constant 3) (.set 101 (.sub (.constant 1) (.mod (.constant 5) (.reg 8)))))) .skip)) 2 168)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.loop 10 (.le (.reg 5) (.reg 2)) (.loop 1 (.mod (.reg 17) (.reg 9)) .skip)) 4 175)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.branch (.reg 4) (.branch (.mod (.reg 0) (.reg 9)) (.loop 17 (.eq (.constant 2) (.constant 4)) (.set 7 (.constant 5))) .skip) .skip) 10 182)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.branch (.sub (.le (.reg 101) (.reg 2)) (.constant 5)) (.loop 1 (.div (.reg 4) (.reg 101)) (.branch (.constant 2) (.set 6 (.pow2 (.eq (.reg 37) (.constant 5)))) (.set 3 (.constant 4)))) (.branch (.pow2 (.le (.reg 7) (.reg 0))) .skip (.branch (.le (.sub (.reg 2) (.reg 8)) (.div (.constant 6) (.reg 3))) (.set 0 (.div (.constant 3) (.mul (.reg 5) (.reg 5)))) (.set 101 (.div (.reg 17) (.sub (.constant 6) (.reg 8))))))) 1 189)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 11 (.mul (.pow2 (.reg 9)) (.reg 4))) 7 196)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.set 37 (.reg 9)) 10 203)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.loop 17 (.mod (.reg 9) (.reg 3)) (.branch (.reg 4) (.seq (.set 11 (.mod (.reg 4) (.reg 9))) (.seq (.set 7 (.eq (.reg 4) (.reg 2))) .skip)) (.seq (.set 8 (.mod (.pow2 (.reg 3)) (.eq (.reg 2) (.constant 2)))) (.seq (.set 8 (.reg 6)) .skip)))) 101 210)).toArray).compress)
#eval IO.println ((Json.arr (sj (compiled (.seq (.branch (.constant 1) (.loop 0 (.reg 10) (.set 101 (.pow2 (.mod (.constant 6) (.reg 3))))) (.set 2 (.add (.constant 3) (.eq (.reg 10) (.constant 3))))) (.seq (.branch (.reg 6) (.loop 7 (.reg 2) (.set 0 (.le (.reg 0) (.mul (.constant 5) (.reg 8))))) (.branch (.div (.reg 8) (.le (.constant 3) (.constant 4))) (.set 10 (.constant 6)) (.set 7 (.eq (.constant 2) (.constant 5))))) .skip)) 10 217)).toArray).compress)
end IndependentAstComparison
