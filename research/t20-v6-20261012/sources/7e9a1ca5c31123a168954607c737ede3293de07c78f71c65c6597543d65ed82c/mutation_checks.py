"""In-memory semantic mutations, with each original restored; no author-file edits."""
from dataclasses import replace
import json
from independent_checks import load, occurrence_oracle, actual_endpoint_checks, nonmonotone_control

occ=load('occurrence_model');cont=load('continuation_model')
results=[]

def reject(name, invoke):
    try: invoke()
    except AssertionError:
        results.append({'mutation':name,'detected':True,'failure_type':'AssertionError'})
    else:
        raise AssertionError('Independent check failed to detect '+name)

original=occ.resolve
try:
    occ.resolve=lambda formula,context: original(formula,replace(context,time=0))
    reject('erase_original_time_binding',lambda: occurrence_oracle(occ))
finally: occ.resolve=original

original=cont.World.migrate
try:
    def omit_source_state(world,parent,encoding,available):
        child=original(world,parent,encoding,available)
        child.data=cont.encode(0,encoding)
        return child
    cont.World.migrate=omit_source_state
    reject('replace_migrated_state_with_constant_zero',lambda: actual_endpoint_checks(cont))
finally: cont.World.migrate=original

original=cont.World.step
try:
    def stale_write(world,token,request,available):
        if request=='toggle': return ('value',world.read_state(token,available))
        return original(world,token,request,available)
    cont.World.step=stale_write
    reject('drop_state_changing_effect',lambda: actual_endpoint_checks(cont))
finally: cont.World.step=original

original=cont.World.migrate
try:
    def preserve_parent(world,parent,encoding,available):
        data=parent.data
        child=original(world,parent,encoding,available)
        parent.live=True;parent.data=data
        return child
    cont.World.migrate=preserve_parent
    reject('retain_parent_as_live_operative_token',lambda: actual_endpoint_checks(cont))
finally: cont.World.migrate=original

# Fresh green checks after restoration ensure no mutation leaked.
occurrence_oracle(occ);actual_endpoint_checks(cont)
print(json.dumps({'semantic_mutations':results,'restored_checks_pass':True,'nonmonotone_control':nonmonotone_control()},indent=2))
