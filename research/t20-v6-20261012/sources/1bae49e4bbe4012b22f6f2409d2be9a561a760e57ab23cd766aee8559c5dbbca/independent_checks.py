"""Closed-form replay and semantic mutation controls, independent of output flags."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, subprocess, tempfile
import recovery as r

HERE = Path(__file__).resolve().parent

def check():
    compared = 0
    # Re-derive value differences without utility(), plan(), or expected_outcomes().
    # Crossover, nonstandard utility biases, and false-claim calibration are checked
    # by the separately executed tests rather than this restricted formula.
    for d, a, h, g in product([F(0), F(1, 1000), F(1, 4)],
                               [F(0), F(1, 7)], [F(0), F(1, 9)], [F(0), F(4)]):
        p = r.Policy(decode=d, accept=a, reassure=h, material=g)
        for dm, dg, gift, q in product([F(0), F(1, 3), F(1)], [F(0), F(2, 3), F(1)], [0, 1], [F(0), F(1, 2), F(1)]):
            v = d + q * (a + h)
            scores = {'keep': F(0), 'mantle': v * dm + g * gift - 1,
                      'gesture': v * dg - F(1, 2)}
            for menu in r.menus(('keep', 'mantle', 'gesture')):
                s = r.standard_scene(dm, dg, gift, q, menu)
                optimum = max(scores[x] for x in menu)
                expected = sorted(x for x in menu if scores[x] == optimum)
                actual = sorted(x.name for x in r.optimal(p, s))
                assert expected == actual, (p, s, expected, actual)
                compared += 1
    # Mutation tests run the actual current unittest file in isolated temporary dirs.
    source = (HERE/'recovery.py').read_text()
    tests = (HERE/'test_recovery.py').read_text()
    mutations = {
      'drop_selected_means': ('nodes = ancestors(roots)', 'nodes = set(roots)'),
      'equate_belief_with_actual_decoding': ("if p.channel_belief == 'unaware_of_blocks':\n        return F(1)", "if p.channel_belief == 'unaware_of_blocks':\n        return a.decode_probability"),
      'optimize_uncommitted_appraisals': ('if k in p.commitments), F(0))', 'if True), F(0))'),
      'remove_indication_goal_score': ('return (p.decode, p.accept, p.reassure, p.material, p.repair, p.warmth, p.correction)', 'return (F(0), p.accept, p.reassure, p.material, p.repair, p.warmth, p.correction)'),
      'discard_optimal_action_ties': ('return tuple(a for a, v in zip(s.options, scores) if v == best)', 'return tuple(a for a, v in zip(s.options, scores) if v == best)[:1]'),
      'destroy_channel_crossover': ("Option('y', F(swap), F(1), F(1))", "Option('y', F(not swap), F(1), F(1))"),
    }
    mutation_results = []
    for name, (before, after) in mutations.items():
        assert source.count(before) == 1, (name, source.count(before))
        with tempfile.TemporaryDirectory(prefix='intention-recovery-') as tmp:
            t = Path(tmp)
            (t/'recovery.py').write_text(source.replace(before, after))
            (t/'test_recovery.py').write_text(tests)
            proc = subprocess.run(['python', '-B', '-m', 'unittest', '-v'], cwd=t,
                                  capture_output=True, text=True)
            (HERE/('mutation-'+name+'.txt')).write_text(proc.stdout + proc.stderr)
            mutation_results.append({'mutation': name, 'returncode': proc.returncode,
                                     'rejected': proc.returncode != 0})
            assert proc.returncode != 0, name
    # Earlier author/review/source inputs have not been modified by this continuation.
    cwd = HERE.parents[2]
    rechecks = []
    for row in json.loads((HERE/'INPUT_BINDINGS.json').read_text()):
        path = cwd/row['path']
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == row['sha256'], path
        rechecks.append({'path': row['path'], 'unchanged': True, 'sha256': actual})
    return {'closed_form_argmax_comparisons': compared,
            'semantic_mutations': mutation_results, 'old_input_rechecks': rechecks,
            'scope': 'Author-created independent algebra and mutation replay; not an independent human review.'}

if __name__ == '__main__': print(json.dumps(check(), indent=2))
