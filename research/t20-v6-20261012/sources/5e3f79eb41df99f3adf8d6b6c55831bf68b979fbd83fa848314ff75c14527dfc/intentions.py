"""Typed intentional-content and factivity controls for frozen-state comparisons."""
from dataclasses import dataclass,asdict
from pathlib import Path
from datetime import datetime,timezone
import json

@dataclass(frozen=True)
class IntrinsicState:
    rigid_bearer:str
    knowing_token:str
    end:int
    command:int
    known_peer_contribution:int
    known_output:int
    mode:str
    peer_manner:int|None=None


def planned_command(end,knowledge):return end-knowledge

def diagnose(state,peer_actual,F=lambda a,b:a+b):
    output=F(state.command,peer_actual)
    return {
        'state':asdict(state),'actual_peer_contribution':peer_actual,'actual_output':output,
        'whole_end_satisfied':output==state.end,
        'partial_command_executed':True,
        'through_peer_content_satisfied':(output==state.end and peer_actual==state.peer_manner) if state.peer_manner is not None else None,
        'peer_knowledge_factive':state.known_peer_contribution==peer_actual,
        'output_knowledge_factive':state.known_output==output,
        'means_end_policy_satisfied':state.command==planned_command(state.end,state.known_peer_contribution) if state.mode=='knowledge_used' else None,
        'productive_relevance_scope':['capacity','end','command']+(['known_peer_contribution'] if state.mode=='knowledge_used' else []),
    }


def run():
    orig=IntrinsicState('A','kA',2,1,1,2,'knowledge_used')
    through=IntrinsicState('A','kA',2,1,1,2,'knowledge_used',1)
    pure=IntrinsicState('A','kA',2,1,1,2,'knowledge_accompaniment')
    changes={
      'actual_whole_end_known_peer_plan':diagnose(orig,1),
      'suppression_freeze_everything':diagnose(orig,0),
      'change_knowledge_freeze_used_command':diagnose(IntrinsicState('A','kA',2,1,0,1,'knowledge_used'),0),
      'replan_preserve_end_change_exercise':diagnose(IntrinsicState('A','kA_new',2,2,0,2,'knowledge_used'),0),
      'through_peer_actual':diagnose(through,1),
      'through_peer_solo_repair':diagnose(IntrinsicState('A','kA_new',2,2,0,2,'knowledge_used',1),0),
      'intrinsic_symmetric_plan_actual':diagnose(pure,1),
      'accompaniment_covaries_productive_state_fixed':diagnose(IntrinsicState('A','kA',2,1,0,1,'knowledge_accompaniment'),0),
      'or_accompaniment_actual':diagnose(IntrinsicState('A','kA',1,1,1,1,'knowledge_accompaniment'),1,lambda a,b:int(bool(a or b))),
      'or_accompaniment_covaries_productive_state_fixed':diagnose(IntrinsicState('A','kA',1,1,0,1,'knowledge_accompaniment'),0,lambda a,b:int(bool(a or b))),
    }
    return {'schema':'intentional-content-factivity/1','run_utc':datetime.now(timezone.utc).isoformat(),'limits':[
      'Every suppression is a diagnostic intervention, not certified source-admissible world.',
      'Same knowing-token identifier with changed content is an explicit identity proposal, not a proof of intrinsic token sameness or external receipt.',
      'Changing known relational content does not by itself change a standing perfection or introduce efficient donation.',
      'When knowledge actually selects the command, changing it while freezing the command violates the displayed choice policy.',
      'When knowledge is accompaniment, it may covary without altering the displayed productive determinants.',
      'The source fixed-condition passage names will, movement and instruments; freezing all omniscient content is an additional test, not attributed to it.',
    ],'cases':changes,'passive_knower_control':{
       'worlds':[{'output':q,'knowledge_of_output':q,'observer_command':None,'observer_productive_support':False} for q in [0,1]],
       'full_factive_knowing_state_entails_output':all(k1!=k2 or o1==o2 for o1,k1 in [(0,0),(1,1)] for o2,k2 in [(0,0),(1,1)]),
       'therefore_entailment_alone_identifies_productive_completion':False,
       'epistemic_accessibility':'identity within each world; metaphysical possibility relation leaves both represented valuations open',
    }}

if __name__=='__main__':
 result=run();p=Path(__file__).resolve().parents[1]/'results/INTENTIONS.json';p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
