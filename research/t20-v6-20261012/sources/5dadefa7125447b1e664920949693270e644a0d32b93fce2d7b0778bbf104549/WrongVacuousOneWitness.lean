import RationalThresholdControls
import RationalThresholdUniform
open AtomicMembership AtomicMembership.RationalThreshold P02.Codec P02.Codec.UniformComputability

example : lowerCutMatrix 0 0 (Nat.pair 1 1) 0 2 := by decide +kernel
