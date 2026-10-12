import ModalKnowledge
import CreativeKnowledge
open Orthemology.Tranche6.ModalKnowledge
set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
example : StandingKnowledge := by
  simp only [StandingKnowledge, HasKnowledge, Knows,
    Orthemology.Tranche5.KnowledgeScope.Knows,
    Orthemology.Tranche5.KnowledgeScope.Truth, Active]
  decide
