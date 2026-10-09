"""Same-path green/red/green checks; fail if rejection is environmental."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

root = Path(__file__).resolve().parent
base = root.parent/'formal-identification'
lean = base/'toolchain/lean-4.19.0-linux/bin/lean'
env = dict(os.environ)
records = {}
cases = {
    'Calibration': ('(5 / 6 : ℚ) ^ c','(1 / 6 : ℚ) ^ c',('unsolved goals','padicValRat p (1 / 6)','padicValRat p (5 / 6)')),
    'HitTransform': ('∑ T : Finset E, if (T ∩ U).Nonempty then n T else 0','∑ T : Finset E, if T.Nonempty then n T else 0',('unsolved goals','if T.Nonempty then n T else 0','(T ∩ U).Nonempty')),
}
for name,(old,new,expected) in cases.items():
    original = (root/'frozen'/f'{name}.lean').read_text()
    assert original.count(old)==1
    path = root/'mutation-controls'/f'{name}Control.lean'
    entry = {}
    for phase,source in (('baseline',original),('mutation',original.replace(old,new)),('restored',original)):
        path.write_text(source)
        args = [str(lean),str(path)]
        if phase!='mutation':
            args.insert(1,'-DwarningAsError=true')
        result = subprocess.run(args,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=base/'mathlib')
        log = root/'results'/f'{name}-{phase}.log'
        log.write_text(result.stdout)
        entry[phase] = {'exit_code':result.returncode,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'log':str(log.relative_to(root))}
        if phase=='mutation':
            assert result.returncode!=0, (name,'mutation accepted')
            assert all(piece in result.stdout for piece in expected), (name,'expected proof-goal rejection missing',result.stdout)
            assert not any(piece in result.stdout.lower() for piece in ('unknown module','unknown package','object file','no such file','failed to load')), (name,'environmental failure')
        else:
            assert result.returncode==0, (name,phase,result.stdout)
    assert path.read_text()==original
    records[name] = entry
(root/'results/INDEPENDENT_MUTATION_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
