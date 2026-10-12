import RationalThresholdControls
import RationalThresholdUniform
open AtomicMembership AtomicMembership.RationalThreshold P02.Codec P02.Codec.UniformComputability

example : rationalOfCode (complementCode (Nat.pair 7 0)) = 0 := by decide +kernel
