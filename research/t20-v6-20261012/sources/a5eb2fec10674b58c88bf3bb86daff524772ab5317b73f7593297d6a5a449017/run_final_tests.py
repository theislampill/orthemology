#!/usr/bin/env python3
"""Durable new-proposal test evidence with exact code and output bindings."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys
R=Path(__file__).resolve().parents[1]
def H(b):return hashlib.sha256(b).hexdigest()
def identity(b):return {'bytes':len(b),'sha256':H(b)}
source={p.relative_to(R).as_posix():identity(p.read_bytes())
        for folder in ['executable','handoff'] for p in sorted((R/folder).glob('*.py'))}
rows=[]
for mode,flags in [('normal',[]),('optimised',['-O'])]:
    cmd=[sys.executable,*flags,'-B','-m','unittest','discover','-v']
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(cmd,cwd=R/'executable',capture_output=True,timeout=120,env=env)
    text=(p.stdout+p.stderr).decode();counts=re.findall(r'^Ran ([0-9]+) tests? in .+$',text,re.M)
    row={'mode':mode,'command':cmd,'cwd':'executable','exit_code':p.returncode,
         'test_count':int(counts[0]) if len(counts)==1 else 0,'source_bindings':source,
         'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'python':sys.version,'new_tests_not_recovered_attempt2':True,'kernel_credit':False}
    for label,b in [('stdout',p.stdout),('stderr',p.stderr)]:
        rel='evidence/final_tests_'+mode+'.'+label;(R/rel).write_bytes(b)
        row[label]={'path':rel,**identity(b)}
    (R/('evidence/final_tests_'+mode+'.exit')).write_text(str(p.returncode)+'\n')
    rows.append(row)
    if p.returncode or row['test_count']<=0 or not re.search(r'^OK\s*$',text,re.M):
        (R/'evidence/FINAL_TEST_RUNS.json').write_text(json.dumps(rows,indent=2)+'\n')
        raise SystemExit('FAILED '+mode+'\n'+text)
for name,b in source.items():
    if identity((R/name).read_bytes())!=b:raise SystemExit('source changed during tests: '+name)
(R/'evidence/FINAL_TEST_RUNS.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'runs':[{'mode':r['mode'],'tests':r['test_count'],'exit':r['exit_code']} for r in rows],
                  'source_files_bound':len(source),'kernel_credit':False},indent=2))
