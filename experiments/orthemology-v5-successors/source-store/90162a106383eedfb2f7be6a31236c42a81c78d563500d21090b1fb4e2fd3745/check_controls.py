#!/usr/bin/env python3
"""Compile independently false claims and require Lean to reject each.

These are claim mutations against the actual concrete histories, not syntax
errors or postulated bad gates. The positive witness theorems live in
NegativeControls.lean and are always compiled first.
"""
from pathlib import Path
import os, subprocess, sys, json
root = Path(__file__).resolve().parent
out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
claims = {
    'revocation_omission_is_safe':
        '¬ BrokenLands revoked NoRevocation command 11',
    'target_only_checks_preserve_permission':
        '¬ BrokenLands delivered TargetOnly command 11',
    'cancellation_guard_is_redundant':
        '¬ BrokenLands cancelled NoCancellation command 11',
    'B_replies_are_enough':
        '¬ Lands cfg falselyClosed command 11',
    'mediation_is_redundant':
        '(bypass revoked).damaged = false',
    'approved_label_binds_substituted_bytes':
        '(land cfg prepared substituted 11).damaged = false',
    'old_action_still_authorized':
        'Authorized command (cfg.source revoked.epoch)',
}
results=[]
for name, claim in claims.items():
    p=out/(name+'.lean')
    p.write_text('import NegativeControls\nopen InterlockHistory InterlockHistory.Controls\n'
                 +'example : '+claim+' := by decide\n')
    r=subprocess.run([str(root/'lean.sh'), '-j1', str(p)], capture_output=True, text=True)
    text=r.stdout+r.stderr
    (out/(name+'.log')).write_text(text)
    okay=r.returncode != 0 and "tactic 'decide' proved that the proposition" in text and 'is false' in text
    results.append({'control':name,'expected':'kernel_rejection_of_false_claim',
                    'exit_code':r.returncode,'passed':okay})
    if not okay:
        print(text)
        raise SystemExit(f'Control {name} did not produce the required false-claim rejection')
(out/'RESULTS.json').write_text(json.dumps({'status':'PASS','controls':results}, indent=2)+'\n')
print(f'PASS: {len(results)} false safety claims rejected by kernel reduction.')
