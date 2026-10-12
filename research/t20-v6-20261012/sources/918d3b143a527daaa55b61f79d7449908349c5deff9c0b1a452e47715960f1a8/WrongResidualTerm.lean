import RationalThresholdControls
import RationalThresholdUniform
open AtomicMembership AtomicMembership.RationalThreshold P02.Codec P02.Codec.UniformComputability

example : heavyCount (programIndex hiddenMixturePacked) 1 4 = 8 := by
  rw [hiddenMixture_count_4]
  decide +kernel
