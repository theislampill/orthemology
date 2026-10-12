"""Read-only inherited-engine probes: original roots versus derived participants.
This adds no full model of subordinate cognition, will, or moral responsibility.
"""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'provision-identity/src'))
from provision_semantics import Event,rule,run,created_rules
m=Event('m','created-means')
u=Event('u','created-secondary-activity')
p=rule('A-originates-means','A',output=m)
q=rule('means-produces-secondary-activity',(),inputs=['m'],output=u)
r=rule('secondary-activity-produces-e',(),inputs=['u'])
positive=run((p,q,r),'A')
negative=run(created_rules('A_created_mechanism'),'AB')
results={
 'sole_original_through_created_means':{
  'created_history':positive.history(),
  'root_supports':{e:sorted(positive.productive_roots(e)) for e in positive.events},
  'exhaustive_original_providers':sorted(positive.exhaustive_providers()),
  'actual_derivation_rules':{e:sorted(p.rule for p in ps) for e,ps in positive.proofs.items()},
 },
 'created_means_plus_independent_peer':{
  'created_history':negative.history(),
  'root_supports':{e:sorted(negative.productive_roots(e)) for e in negative.events},
  'exhaustive_original_providers':sorted(negative.exhaustive_providers()),
 },
 'limits':'Root support concerns stipulated independent original bearers A/B, not every participating entity. Proof propagation permits real derived causes. Full source-agent cognition, will, completeness of causal inventory, and metaphysical original adequacy are not proved.'
}
assert positive.productive_roots('e')==frozenset('A')
assert positive.exhaustive_providers()==frozenset('A')
assert len(positive.events)==3
assert negative.productive_roots('m')==frozenset('A')
assert negative.productive_roots('e')==frozenset('AB')
assert negative.exhaustive_providers()==frozenset()
print(json.dumps(results,indent=2))
