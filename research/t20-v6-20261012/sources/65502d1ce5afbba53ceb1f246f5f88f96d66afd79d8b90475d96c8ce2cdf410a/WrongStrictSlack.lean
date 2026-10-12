import RationalThresholdControls
import RationalThresholdUniform
open AtomicMembership AtomicMembership.RationalThreshold P02.Codec P02.Codec.UniformComputability

example : lowerCutMatrix (1/2) 0 (Nat.pair 1 2) 0 2 := by decide +kernel
