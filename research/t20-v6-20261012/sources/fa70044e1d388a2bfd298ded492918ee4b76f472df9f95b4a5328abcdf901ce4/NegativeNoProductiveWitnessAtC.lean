import ModalKnowledge
import CreativeKnowledge
open Orthemology.Tranche6.ModalKnowledge
set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
example :
    ¬ Orthemology.Tranche5.KnowledgeScope.Complete .c .u .z := by
  simp only [Orthemology.Tranche5.KnowledgeScope.Complete,
    Orthemology.Tranche5.KnowledgeScope.Dep,
    Orthemology.Tranche5.KnowledgeScope.Ex]
  decide
