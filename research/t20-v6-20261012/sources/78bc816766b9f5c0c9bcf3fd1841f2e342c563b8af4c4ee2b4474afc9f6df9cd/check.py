from pathlib import Path
import os,subprocess,sys
p=Path('private-locator:480e48aae3b59d70a43f'); math=Path('private-locator:41bd9f979012c8bbc235'); libs=[Path('private-locator:096fa1962179cf1aeebf'),Path('private-locator:41bb551746702dbd66a7'),Path('private-locator:6e1cdd2685640ba2eef0'),math/'.lake/build/lib/lean']+[x/'.lake/build/lib/lean' for x in sorted((math/'.lake/packages').iterdir()) if (x/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'LEAN_PATH':':'.join(map(str,libs))};r=subprocess.run(['private-locator:4211d241978f643cb623','-j1',str(p/'BoundaryControls.lean')],env=env,capture_output=True,text=True);(p/f'development/BoundaryControls.{sys.argv[1]}.log').write_text(r.stdout+r.stderr);print(r.returncode);print(r.stdout+r.stderr)
