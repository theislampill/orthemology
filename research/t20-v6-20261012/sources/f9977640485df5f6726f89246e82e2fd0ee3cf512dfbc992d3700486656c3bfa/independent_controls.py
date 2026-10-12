import copy,importlib.util,json,sys
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
pin=root/'replay/interpretation-repair-transport-20261010/pinned'
s=importlib.util.spec_from_file_location('review_validator',pin/'scripts/validate_corrective_transition.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
rows=[]
for f in yaml.safe_load((pin/'applications/daee-epistemics/CORRECTIVE-TRANSITION-FIXTURES.yaml').read_text())['fixtures']:
 actual,reason=v.transition_ok(f['transition']);assert actual==f['expected_valid']
 if not actual: assert reason==f['violates']
 rows.append({'id':f['id'],'actual':actual,'reason':reason,'matches_fixture':True})
doc=json.loads((root/'replay/interpretation-repair-transport-20261010/PROBE_DOCUMENTS.json').read_text())['honest-fixed-content-repair']
missing=copy.deepcopy(doc)
missing['transitions'][0]['state_before']='nonexistent-state-before'
missing['transitions'][0]['state_after']='nonexistent-state-after'
assert v.document_ok(missing)==(True,None)
# Isolate declared authorization handling independently of the author's snapshots.
checks=[]
for requested,authorized,ref,expected in [(False,False,None,True),(True,False,None,False),(True,True,'not-authenticated',True),(False,True,'not-authenticated',False),(True,True,None,False)]:
 d=copy.deepcopy(doc); d['transitions'][0]['global_revision']={'requested':requested,'authorized':authorized,'authorization_ref':ref}
 actual,reason=v.document_ok(d);assert actual==expected
 checks.append({'requested':requested,'authorized':authorized,'reference':ref,'accepted':actual,'reason':reason})
print(json.dumps({'inherited_transition_fixtures':rows,'nonexistent_state_references_still_accepted':True,'isolated_declared_authorization_controls':checks,'scope':'The unchanged imported functions check record fields, not state existence, source interpretation, or real authorization.'},indent=2))
