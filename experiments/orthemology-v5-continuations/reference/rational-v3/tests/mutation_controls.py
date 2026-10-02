#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys,tempfile
base=Path(__file__).resolve().parents[1]
source=(base/'reference.py').read_text();tests=(base/'tests/test_reference.py').read_bytes()
mutations={
 'strict_head_equality':('if centre > (epsilon - delta) / (2 * epsilon):','if centre >= (epsilon - delta) / (2 * epsilon):'),
 'restore_guard_sensitive_parser':('numerator = _decimal_input(pieces[0])','numerator = int(pieces[0])'),
 'boundary_equality':('if floor > boundary:','if floor >= boundary:'),
 'remove_positive_floor':('floor = max(mean, Fraction(1, n))','floor = mean'),
 'reverse_local_tie':('if mean <= centre:','if mean < centre:')}
results={}
for name,(old,new) in mutations.items():
 assert source.count(old)==1,name
 with tempfile.TemporaryDirectory(prefix='rational-policy-mutation-') as directory:
  path=Path(directory);(path/'tests').mkdir();(path/'reference.py').write_text(source.replace(old,new,1));(path/'tests/test_reference.py').write_bytes(tests)
  result=subprocess.run([sys.executable,'-B',str(path/'tests/test_reference.py')],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert result.returncode!=0,('mutation survived',name)
  results[name]={'detected':True,'returncode':result.returncode,'failure_kind':result.stdout.splitlines()[-1].split(':',1)[0]}
print(json.dumps(results,indent=2))
