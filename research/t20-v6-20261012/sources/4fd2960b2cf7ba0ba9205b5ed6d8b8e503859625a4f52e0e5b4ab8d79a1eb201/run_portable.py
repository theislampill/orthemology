"""Derived relocation only; exact mathematical checker and report remain unchanged."""
from pathlib import Path
import runpy
scope=runpy.run_path(str(Path(__file__).with_name('check_exact.py')))
main=scope['main']
main.__globals__['ROOT']=Path(__file__).resolve().parent
main()
