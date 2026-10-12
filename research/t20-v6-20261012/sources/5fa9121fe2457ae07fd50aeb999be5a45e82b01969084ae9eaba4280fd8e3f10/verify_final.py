#!/usr/bin/env python3
"""Repeat frozen source replay while also checking telescope handoff objects.
The original source replay/pins/receipt remain unchanged; this run has its own V.
"""
from pathlib import Path
import importlib.util,json,tempfile
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rule_source_verify',R/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
supp=json.loads((R/'validation/TRANSPORT_OBJECT_PINS.json').read_text())
freeze=json.loads((R/'validation/FINAL_REPLAY_FREEZE.json').read_text())['files']
v.b.check(supp);v.b.check(freeze)
source_pins=R/'validation/INPUT_PINS.json';v.b.check(json.loads(source_pins.read_text()))
v.V=Path(tempfile.mkdtemp(prefix='final-replay-',dir=R/'validation'))
(v.V/'INPUT_PINS.json').write_bytes(source_pins.read_bytes())
v.main()
v.b.check(supp);v.b.check(freeze)
(v.V/'TRANSPORT_PIN_CHECK.json').write_text(json.dumps(dict(status='PASS',source_replay=str(v.V/'AUTHOR_REPLAY.json'),supplement=supp),indent=2)+'\n')
print('PASS transport handoff objects; receipt '+str(v.V/'TRANSPORT_PIN_CHECK.json'))
