import ModalKnowledge
import CreativeKnowledge
open Orthemology.Tranche6.ModalKnowledge
set_option synthInstance.maxSize 4096
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
open Orthemology.Tranche6.CreativeKnowledge
example : DeterminedBy StandingNature .a (fun v => actualEffect v = .recipient) := by
  simp only [DeterminedBy, StandingNature, actualEffect, actualAct, produce]
  decide
