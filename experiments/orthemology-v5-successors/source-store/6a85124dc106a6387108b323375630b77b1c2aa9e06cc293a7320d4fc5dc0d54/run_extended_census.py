"""Additional action-dependent numerical census; uses the frozen oracle core."""
import json
from run_census import census, HERE
from oracle import two_state_two_action_state_homogeneous

if __name__=='__main__':
    result=census('two_state_two_action_state_homogeneous',
                  two_state_two_action_state_homogeneous,6561)
    (HERE/'EXTENDED_CENSUS_RESULT_v1.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
