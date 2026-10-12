from pathlib import Path
import runpy
s=runpy.run_path(str(Path(__file__).with_name('verify.py')))
f=s['main']
f.__globals__['CAT']=Path(__file__).resolve().parent/'inputs'
f()
