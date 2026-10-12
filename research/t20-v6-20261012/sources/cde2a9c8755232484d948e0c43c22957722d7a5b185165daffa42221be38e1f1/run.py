from pathlib import Path
import importlib.util,os,sys,subprocess
W=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('v',W/'hase-source-family-computability-20261010/verify.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[R/'validation',W/'hase-coded-scope-computability-20261010/validation',v.V]+v.inherited_paths())))
for a in sys.argv[1:]:
 src=R/a; cmd=[str(v.LEAN),'--trust=0','-o',str(R/'validation'/(src.stem+'.olean')),str(src)]
 p=subprocess.run(cmd,env=env,cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(p.stdout,end=''); (R/'diagnostics'/(src.stem+'.log')).write_text(p.stdout)
 if p.returncode:sys.exit(p.returncode)
