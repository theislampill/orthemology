import MatrixEndpointChecks
open P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit
example : outputList (programIndex echoProgram) [true,false] = [false,false] := by
  rw [echo_prefix_stream]
