"""Two rejected compiler weakenings, using the scoped source fixture."""
from test_guarded_compiler import source_fixture, prices
from guarded_compiler import compile_exact, exact_step

def run():
    J,E,rules=source_fixture()
    exact,history=compile_exact(J,E,rules)
    old={q:{} for q in J}
    for _ in range(len(J)*(len(E)+1)+2):
        new=exact_step(J,rules,old)
        # Deliberate mutation: discard exact supports by ordinary Pareto order.
        old={q:{s:row for s,row in rows.items()
                if not any(t!=s and t<=s and other[0]<=row[0]
                           for t,other in rows.items())}
             for q,rows in new.items()}
    assert exact['licensed'] and not old['licensed']
    assert not history[len(J)]['licensed']
    return {'intermediate_pareto_mutation_rejected':True,
            'old_judgement_only_round_bound_rejected':True,
            'exact_licensed_price':str(next(iter(exact['licensed'].values()))[0]),
            'mutated_terminal_witnesses':len(old['licensed']),
            'scope':'No arbitrary padding: the second token is a cited matching corroborating report.'}

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
