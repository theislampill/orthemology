import OrderedCycle
open OrthemicCertificate.Direct
#guard cycleAction ({2,0,1} : Finset (Fin 4)) 3 0 = 0
#guard cycleAction ({2,0,1} : Finset (Fin 4)) 3 1 = 1
#guard cycleAction ({2,0,1} : Finset (Fin 4)) 3 2 = 2
#guard cycleAction ({2,0,1} : Finset (Fin 4)) 3 100 = 1
#guard cycleAction (∅ : Finset (Fin 4)) 3 100 = 3
#check cycleAction_mem
#check cycleAction_at_index
#check exists_cycle_barrier
#print axioms cycleAction
#print axioms cycleAction_mem
#print axioms exists_cycle_barrier
