"""Reproducible structural counters; no timings are used as a complexity proof."""
from fractions import Fraction
import json
import platform
from time import perf_counter
from unittest.mock import patch
from tests.support import graph_model
import efficient
import mec


def measure(n, large=False):
    a=2; m=n*a; offset=(1<<8192) if large else 0
    rows=[[[int(s==t) for t in range(n)] for _ in range(a)] for s in range(n)]
    priorities=[[[offset+2*(s*a+i+1) for i in range(a)] for s in range(n)],
                [[offset+2*(m-s*a-i) for i in range(a)] for s in range(n)]]
    model=graph_model(rows,priorities=priorities)
    pairs=tuple((s,i) for s in range(n) for i in range(a))
    calls=[]; original=mec.maximal_components
    def counted(*args):
        with patch.object(mec,'_strongly_connected',wraps=mec._strongly_connected) as count:
            result=original(*args)
            calls.append(count.call_count)
            assert count.call_count <= 2*n-1
            return result
    started=perf_counter()
    with patch.object(efficient,'maximal_components',side_effect=counted):
        known=efficient.known_components(model,pairs)
        known_calls=len(calls)
        uncertain=efficient.uncertain_components(model,0,pairs)
    uncertain_calls=len(calls)-known_calls
    assert known_calls==m and uncertain_calls==m+m*m
    return dict(n=n,m_full_carrier=m,large_8193_bit_thresholds=large,
        known_mec_calls=known_calls,uncertain_mec_calls=uncertain_calls,
        largest_scc_worklist_items=max(calls),scc_items_bound=2*n-1,
        total_scc_worklist_items=sum(calls),known_representatives=len(known),
        uncertain_representatives=len(uncertain),illustrative_seconds=perf_counter()-started)

if __name__=='__main__':
    print(json.dumps(dict(python=platform.python_version(),
        meaning='Structural counters corroborate the source proof; timings prove no asymptotic bound.',
        rows=[measure(n) for n in (1,2,4,8,16)]+[measure(2,True)]),indent=2))
