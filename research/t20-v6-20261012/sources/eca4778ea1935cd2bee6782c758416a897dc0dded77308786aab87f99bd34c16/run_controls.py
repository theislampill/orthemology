from pathlib import Path
import os,subprocess,json,hashlib
r=Path('private-locator:d7baf990504d056c9053'); rec=r/'receipts/20260930T164838Z'; lib=rec/'lib'; math=Path('private-locator:41bd9f979012c8bbc235');tool='private-locator:d97af50b47918e94879b'
paths=[lib,math/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in sorted((math/'.lake/packages').iterdir()) if (p/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'LEAN_PATH':':'.join(map(str,paths)),'PATH':tool+':'+os.environ['PATH']};env.pop('LEAN_NUM_THREADS',None)
f=r/'BoundaryControls.lean';cmd=['lean','-j1','--root='+str(r),'-o',str(lib/'BoundaryControls.olean'),str(f)]
p=subprocess.run(cmd,env=env,cwd=r,capture_output=True,text=True);(r/'BoundaryControls.log').write_text(p.stdout+p.stderr);print(p.stdout+p.stderr);print('EXIT',p.returncode)
(r/'CONTROLS_RESULT.json').write_text(json.dumps({'exit':p.returncode,'command':cmd,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'log_sha256':hashlib.sha256((r/'BoundaryControls.log').read_bytes()).hexdigest()},indent=2))
