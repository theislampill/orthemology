#!/usr/bin/env python3
"""Original finite cue-acquisition diagnostic; no model of thought or warrant.

Interpretation is fixed globally: x=target appearance; n=noxiousness;
c=x is a sensory signal; p=n is discomfort from a presented taste trial.
No output or state is renamed between mechanisms. Training trials are supplied
independently of the learned test response. All interventions vary physical
exposures or mechanisms, never semantic labels.
"""
import itertools
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Trial:
    x: int
    n: int
    def __post_init__(self):
        assert self.x in (0, 1) and self.n in (0, 1)

TRIALS = tuple(Trial(x, n) for x, n in itertools.product((0, 1), repeat=2))

def acquired(history):
    w = 0
    for t in history:
        c, p = t.x, t.n
        w = int(w or (c and p))
    return w

def sensitized(history):
    return int(any(t.n for t in history))

def disconnected(history):
    return 0

def seeded(history):
    return 1

def response(w, test):
    c = test.x
    return w * c

def encode(h):
    return [[t.x, t.n] for t in h]

H_PLUS = (Trial(1, 1), Trial(0, 0))
H_MINUS = (Trial(1, 0), Trial(0, 1))
histories = [h for length in range(5) for h in itertools.product(TRIALS, repeat=length)]
checks = {}

# General closed form is proved by induction in MODEL_AND_TRANSPORT.md.
assert all(acquired(h) == int(any(t.x and t.n for t in h)) for h in histories)
checks['closed_form_histories'] = len(histories)

assert all(acquired((t,)) == t.x*t.n for t in TRIALS)
assert acquired((Trial(0, 1),)) == 0 and sensitized((Trial(0, 1),)) == 1
checks['single_trial_cases'] = 4
checks['sensitization_mutant_caught_at'] = {'history': [[0, 1]], 'acquired': 0, 'mutant': 1}

assert sum(t.x for t in H_PLUS) == sum(t.x for t in H_MINUS) == 1
assert sum(t.n for t in H_PLUS) == sum(t.n for t in H_MINUS) == 1
assert acquired(H_PLUS) == 1 and acquired(H_MINUS) == 0
assert sensitized(H_PLUS) == sensitized(H_MINUS) == 1
assert disconnected(H_PLUS) == disconnected(H_MINUS) == 0
checks['matched_marginal_pair'] = {'paired': encode(H_PLUS), 'unpaired': encode(H_MINUS),
    'cue_count_each': 1, 'discomfort_count_each': 1, 'acquired_weights': [1, 0],
    'sensitized_weights': [1, 1], 'disconnected_weights': [0, 0]}

# A fixed present W screens history from the deterministic test equation.
# This is interventional mediator clamping, not arbitrary statistical conditioning.
closure_cases = 0
for h in histories:
    for t in TRIALS:
        assert response(acquired(h), t) == acquired(h) * t.x
        for w in (0, 1):
            assert response(w, t) == w * t.x
        closure_cases += 1
checks['history_test_cases'] = closure_cases
checks['mediator_clamp_cases'] = 2*closure_cases

assert all(response(acquired(H_PLUS), t) == response(seeded(H_PLUS), t) for t in TRIALS)
assert response(acquired(H_MINUS), Trial(1, 0)) == 0
assert response(seeded(H_MINUS), Trial(1, 0)) == 1
checks['same_current_map_different_acquisition'] = {
    'all_four_test_inputs_agree_after_paired_history': True,
    'target_response_after_unpaired_history_acquired': 0,
    'target_response_after_unpaired_history_seeded': 1}

harmless = Trial(1, 0)
assert response(acquired(H_PLUS), harmless) == 1 and harmless.n == 0
checks['harmless_lookalike'] = {'x': 1, 'n': 0, 'c': 1, 'w': 1, 'e': 1,
    'claim': 'Target indication and acquired response do not entail noxiousness. No belief or warrant variable exists.'}

# Label-free implementation: no content-label parameter is read anywhere.
assert all(acquired(h) == acquired(tuple(reversed(h))) for h in histories)
checks['order_invariance_histories'] = len(histories)

result = {'status': 'PASS', 'model': 'fixed-cue physical recruitment and provenance',
          'checks': checks, 'general_claim': 'Proof is in MODEL_AND_TRANSPORT.md; finite enumeration is a consistency check.',
          'not_claimed': ['intrinsic intentionality', 'content qua content causation',
                          'rational basing', 'conscious grasp', 'warrant',
                          'metaphysical naturalism or original-source multiplicity']}
print(json.dumps(result, indent=2))
