import LocalTests
import DynamicTests
import BatchTests
import RaceTests
import Artifacts
import ClockTests

 def main (args : List String) : IO Unit := do
  let input := args.headD "imports/proper-function-and-candidate-e.md"
  let source ← IO.FS.readBinFile input
  let bytes := source.data.toList.map UInt8.toNat
  IO.println s!"SOURCE_BYTES {bytes.length}"
  LocalTests.runLocal bytes
  DynamicTests.runDynamic bytes
  BatchTests.runBatches bytes
  RaceTests.runRaces bytes
  ClockTests.runClocks bytes
  Artifacts.writeArtifacts bytes (System.FilePath.mk ((args[1]?).getD "."))
  IO.println "TERMINAL PASS"
