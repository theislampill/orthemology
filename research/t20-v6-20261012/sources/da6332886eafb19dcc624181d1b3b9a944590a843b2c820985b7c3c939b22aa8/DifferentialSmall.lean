import CodecIndexPrimrec
import Pi3IndexReduction
open P02.Codec P02A2.ObserverCore
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
def main : IO Unit := do
  unless (encodeBytes (PackedProgram.mk 2 2 (.set 2 (.add (.reg 0) (.reg 1)))) == [80, 48, 50, 76, 1, 2, 2, 16, 2, 3, 2, 0, 2, 1]) do throw (IO.userError "bytes-0")
  unless (programIndex (PackedProgram.mk 2 2 (.set 2 (.add (.reg 0) (.reg 1)))) == 6818708144761258717208036767695361) do throw (IO.userError "index-0")
  unless (decodeIndex 6818708144761258717208036767695361 == some (PackedProgram.mk 2 2 (.set 2 (.add (.reg 0) (.reg 1))))) do throw (IO.userError "roundtrip-0")
  unless (evaluateIndex 6818708144761258717208036767695361 0 0 == 0) do throw (IO.userError "eval-0-0-0")
  unless (evaluateIndex 6818708144761258717208036767695361 1 2 == 1) do throw (IO.userError "eval-0-1-2")
  unless (evaluateIndex 6818708144761258717208036767695361 9 2 == 1) do throw (IO.userError "eval-0-9-2")
  unless (evaluateIndex 6818708144761258717208036767695361 4 21 == 1) do throw (IO.userError "eval-0-4-21")
  IO.println "SMALL PASS 7"
