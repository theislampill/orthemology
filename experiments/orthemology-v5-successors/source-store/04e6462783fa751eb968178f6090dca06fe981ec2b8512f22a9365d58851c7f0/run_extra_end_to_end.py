"""Full operator/body follow-through for the 503 supplemental component models."""
import json
from pathlib import Path
from run_campaign import census
from run_extra_campaign import three_state_supports,sparse_seeded
if __name__=='__main__':
    results=[census('three_state_all_equal_mode_support_graphs',three_state_supports,343),
             census('three_state_two_action_seeded_sparse',sparse_seeded,160)]
    (Path(__file__).resolve().parent/'EXTRA_END_TO_END_v1.json').write_text(json.dumps(results,indent=2)+'\n')
