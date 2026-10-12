import Lake
open Lake DSL
package p02Attempt2
require mathlib from git "https://github.com/leanprover-community/mathlib4" @ "c44e0c8ee63ca166450922a373c7409c5d26b00b"
lean_lib P02 where
  srcDir := "Predecessor"
@[default_target]
lean_lib P02A2
