"""Independent repeat of five supplied runtime mutants plus the observed clock regression.
The accepted freeze is read-only; all intentionally broken sources live in mutants-v2.
"""
import importlib.util
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate_mutations',HERE/'freeze-v2/check_mutations.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.MUTATIONS['restore_actor_world_clock_oracle']=(
    'match propose trialActor a path with',
    'match propose { trialActor with observedTime := current.now } a path with',
    'FAIL stale actor time still proposes without a current-time oracle')
sys.argv=[str(HERE/'run_v2_mutants.py'),'--clean-build',str(HERE/'replay-v2/build'),'--output-dir',str(HERE/'mutants-v2'),'--lean','private-locator:cb50f30cfa35bdf3a0cf']
m.main()
