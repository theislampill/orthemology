#!/usr/bin/env python3
"""Bounded read-only replay against the actual accepted Python source.
This corroborates correspondence; it is not a mechanized language-refinement proof.
"""
from pathlib import Path
import importlib.util, sys, json
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parent
source=root.parents[2]/'tranche7-restart/delivery/unknown-root-attribution-accepted-v1/base-v2/dynamic_interlock.py'
spec=importlib.util.spec_from_file_location('accepted_dynamic_v2',source)
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)

def check(condition, message):
    if not condition: raise RuntimeError(message)

def world():
    d=m.Descriptor(0,'7',4,'11','3',(0,1))
    w=m.World(4,1,3,3,d,frozenset({0}))
    k=m.Command.for_descriptor(d,{0,1,2},5)
    check(w.prepare(k,requester='11'),'preparation unexpectedly rejected')
    return w,k

def revoked():
    w,k=world()
    cert=w.revoke({1,2,3},m.Descriptor(1,'7',4,'11','3',(0,1),False))
    return w,k,cert

results=[]
w,k,cert=revoked()
check(w.roots[1].local.epoch==0 and 0 in w.roots[1].revoked,'delayed local history mismatch')
check(w.attempt(k,requester='11')=='NO_EFFECT','live stale write landed')
check(w.attempt(k,requester='11',cached_votes=True)=='UNSAFE','cached-vote deletion did not fail')
results.append({'case':'stale_local_after_revocation','baseline':'NO_EFFECT','cached_votes':'UNSAFE'})

w,k,cert=revoked(); w.deliver(cert)
check(w.attempt(k,requester='11')=='NO_EFFECT','permission-only transition failed')
check(w.attempt(k,requester='11',omit_authorization_epoch=True)=='UNSAFE','target-only deletion did not fail')
results.append({'case':'permission_only_epoch','baseline':'NO_EFFECT','target_only':'UNSAFE'})

w,k=world()
check(w.cancel_with_acknowledgers(k,{0,1},requester='11'),'B+1 cancellation failed')
check(w.attempt(k,requester='11')=='NO_EFFECT','cancelled command landed')
check(not w.roots[1].prepare(k,'11'),'late preparation reopened cancelled nonce')
fresh=m.Command.for_descriptor(w.descriptor,{0,1,2},6)
check(w.prepare(fresh,requester='11'),'fresh nonce blocked by unrelated tombstone')
check(w.attempt(fresh,requester='11')=='APPLIED','fresh authorized nonce failed')
results.append({'case':'durable_cancellation','late':'NO_EFFECT','reprepare':False,'fresh_nonce':'APPLIED'})

w,k=world()
check(w.cancel_with_acknowledgers(k,{0},requester='11',threshold=1),'weak certificate did not form')
check(w.attempt(k,requester='11')=='APPLIED','weak cancellation counterexample missing')
results.append({'case':'too_small_cancel_threshold','late':'APPLIED'})

w,k,cert=revoked(); w.unmediated_write(0)
check(w.unsafe,'charged bypass failed to damage')
results.append({'case':'same_budget_bypass','unsafe':True})

w,k=world(); bad=m.replace(k,table=(1,0))
check(w.attempt(bad,requester='11')=='NO_EFFECT','actual tuple binding failed')
check(w.attempt(bad,requester='11',checked_command=k)=='UNSAFE','post-check substitution counterexample missing')
results.append({'case':'same_command_binding','baseline':'NO_EFFECT','substitution':'UNSAFE'})

w,k=world()
c1=w.revoke({1,2,3},m.Descriptor(1,'7',5,'11','3',(1,0)))
c2=w.revoke({1,2,3},m.Descriptor(2,'7',6,'11','3',(0,1)))
w.deliver(c2); w.deliver(c1)
check(all(w.roots[i].local.epoch==2 for i in (1,2,3)),'stale delivery rewound root')
k2=m.Command.for_descriptor(w.descriptor,{0,1,2},8)
check(w.prepare(k2,requester='11'),'current multi-epoch preparation failed')
check(w.attempt(k2,requester='11')=='APPLIED','current multi-epoch landing failed')
check(w.table==(0,1) and not w.unsafe,'multi-epoch target not restored')
results.append({'case':'two_epochs_reordered_delivery','final_epoch':2,'landing':'APPLIED'})
print(json.dumps({'status':'PASS','source':str(source),'cases':results,
 'scope':'bounded source correspondence corroboration only'},indent=2))
