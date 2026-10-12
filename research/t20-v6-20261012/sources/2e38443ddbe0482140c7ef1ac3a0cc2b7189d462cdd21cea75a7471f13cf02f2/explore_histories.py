#!/usr/bin/env python3
"""Finite new operational exploration, not a universal proof.

Independent small abstract oracle; line-prefix fault injection; forced actual
thread interleavings. Every refusal is a recorded outcome, not discarded data.
"""
from pathlib import Path
from itertools import product
from unittest.mock import patch
from threading import Thread,Event,Lock
import argparse,hashlib,json,sys
from test_new_frontier import AtomicEngine,op,b,logical_state,before_line,BASE

class Nonces:
    def __init__(self):self.n=0
    def __call__(self,n):
        if n!=24:raise AssertionError('unexpected nonce request')
        self.n+=1;return format(self.n,'048x')

def model(view=None,space='finite-programs'):
    return {'space':space,'law':'P03-A2-law','events':'full-measurable',
            'weights':[[1,2],[1,2]],'view':[0,1] if view is None else view}

class Oracle:
    def __init__(self):
        self.ver=0;self.enabled=True;self.need=0;self.required=False;self.mv=0;self.epoch=10
        self.records=[(0,0,None)];self.last=0
    def current(self):
        v,n,m=self.records[self.last]
        return self.enabled and self.ver==v and self.need==n and (m is None or m==self.mv)
    def step(self,a):
        if a in ('admit','revalidate'):
            if not self.enabled:return 'Rejection'
            self.records.append((self.ver,self.need,self.mv if self.required else None));self.last=len(self.records)-1
            return 'Licence'
        if a=='dispatch':return 1 if self.current() else 'Rejection'
        if a in ('disable','enable'):
            self.ver+=1;self.enabled=(a=='enable');self.epoch+=1;return None
        if a=='require':self.required=True;self.need+=1;self.epoch+=1;return None
        if a=='remove':
            if not self.required:return 'Rejection'
            self.required=False;self.need+=1;self.epoch+=1;return None
        if a=='model':self.mv+=1;self.epoch+=1;return None
        raise AssertionError(a)

def oracle_census(dest):
    alphabet=('admit','dispatch','disable','enable','require','remove','model','revalidate')
    rows=[];transitions=0;outcomes={'success':0,'refusal':0}
    with (dest/'serial_histories.jsonl').open('w') as out:
        for length in range(1,5):
            for word in product(alphabet,repeat=length):
                with patch.object(op.secrets,'token_hex',Nonces()):
                    engine=AtomicEngine.standard();engine.set_probability_observation('m',model())
                    last=engine.admit({'op':'primitive','name':'succ'});q=Oracle();trace=[]
                    for action in word:
                        expected=q.step(action)
                        try:
                            if action=='admit':last=engine.admit({'op':'primitive','name':'succ'});actual='Licence'
                            elif action=='revalidate':last=engine.revalidate(last);actual='Licence'
                            elif action=='dispatch':actual=engine.dispatch(last,0)
                            elif action in ('disable','enable'):actual=engine.revise_rule('primitive:succ',action=='enable')
                            elif action=='require':actual=engine.require_probability('primitive:succ','m',[0,1])
                            elif action=='remove':actual=engine.remove_probability_requirement('primitive:succ')
                            else:actual=engine.set_probability_observation('m',model())
                        except b.Rejection:actual='Rejection'
                        if expected!=actual:raise AssertionError((word,action,expected,actual))
                        e=engine._engine
                        got=(e._rules['primitive:succ'],e._stamp('need:primitive:succ')[0],e._rules['probobs:m'][0],e._epoch,len(e._issued),engine.describe(last)['current'])
                        want=((q.ver,q.enabled),q.need,q.mv,q.epoch,len(q.records),q.current())
                        if got!=want:raise AssertionError(('state',word,action,got,want))
                        trace.append({'action':action,'outcome':actual,'epoch':q.epoch,'current':q.current(),'records':len(q.records)})
                        transitions+=1;outcomes['refusal' if actual=='Rejection' else 'success']+=1
                out.write(json.dumps({'actions':word,'trace':trace},separators=(',',':'))+'\n')
                rows.append(1)
    return {'histories':len(rows),'transitions':transitions,'alphabet':alphabet,'max_length':4,'outcomes':outcomes,'mismatches':0,'oracle':'independently written complete-state fragment equations; controlled nonces, no statistical randomness claim'}

def prepare_case(name):
    e=AtomicEngine.standard();e.set_observation('v',[0,0])
    coarse=model([0,2],'tagged-uniform-intervals');fine=model([-1,4],'tagged-uniform-intervals')
    e.set_probability_observation('m',coarse);e.require_probability('primitive:succ','m',[1,1])
    lic=e.admit({'op':'primitive','name':'succ'})
    if name=='coarsen':e.set_probability_observation('m',fine)
    if name=='revalidate':e.revise_rule('primitive:succ',True)
    actions={
       'revise':lambda:e.revise_rule('primitive:succ',False),
       'set_observation':lambda:e.set_observation('v',[1,1]),
       'remove_observation':lambda:e.remove_observation('v'),
       'set_probability':lambda:e.set_probability_observation('m',fine),
       'refine':lambda:e.refine_probability_observation('m',fine),
       'coarsen':lambda:e.coarsen_probability_observation('m',coarse),
       'require':lambda:e.require_probability('primitive:succ','m',[1,2]),
       'remove_requirement':lambda:e.remove_probability_requirement('primitive:succ'),
       'admit':lambda:e.admit({'op':'primitive','name':'succ'}),
       'admit_json':lambda:e.admit_json(b.dump_json({'op':'primitive','name':'succ'})),
       'revalidate':lambda:e.revalidate(lic),
       'describe':lambda:e.describe(lic),
       'dispatch':lambda:e.dispatch(lic,0),
       'project':lambda:e.project()}
    return e,actions[name]

def trace_run(fn,index=None):
    seen=[];previous=sys.gettrace();filename=op.Engine._compile.__code__.co_filename
    def trace(frame,event,arg):
        if event=='line' and frame.f_code.co_filename==filename:
            seen.append((frame.f_code.co_name,frame.f_lineno))
            if index==len(seen)-1:raise MemoryError('P03 finite line-prefix fault')
        return trace
    sys.settrace(trace)
    try:fn()
    finally:sys.settrace(previous)
    return seen

def faults(dest):
    names=('revise','set_observation','remove_observation','set_probability','refine','coarsen','require','remove_requirement','admit','admit_json','revalidate','describe','dispatch','project')
    records=[]
    for name in names:
        e,fn=prepare_case(name);points=trace_run(fn)
        for i,point in enumerate(points):
            e,fn=prepare_case(name);before=logical_state(e);raised=False
            try:trace_run(fn,i)
            except MemoryError:raised=True
            unchanged=before==logical_state(e)
            if not raised or not unchanged or e._active:raise AssertionError((name,i,point,raised,unchanged,e._active))
            records.append({'operation':name,'prefix_index':i,'function':point[0],'line':point[1],'outcome':'MemoryError','state_unchanged':True,'active_cleared':True})
    (dest/'fault_prefixes.json').write_text(json.dumps(records,indent=2)+'\n')
    return {'operations':len(names),'injected_prefixes':len(records),'bad_state_changes':0,'scope':'Every operational.py line event along each of 14 chosen successful call paths, not every opcode or all inputs.'}

def concurrency(dest):
    all_rows=[]
    for first,second in [('dispatch','disable'),('disable','dispatch'),('bad_dispatch','disable'),('disable','bad_dispatch'),('admit','admit')]:
        e=AtomicEngine.standard();lic=e.admit({'op':'primitive','name':'succ'})
        entered=Event();release=Event();invoked=Event();events=[];lock=Lock();failures=[];results={}
        def log(w,kind,value=None):
            with lock:events.append({'n':len(events),'thread':w,'event':kind,'value':value})
        def call(action):
            if action=='dispatch':return e.dispatch(lic,0)
            if action=='bad_dispatch':return e.dispatch(lic,-1)
            if action=='disable':return e.revise_rule('primitive:succ',False)
            return e.admit({'op':'primitive','name':'succ'})
        def pause(frame):
            entered.set()
            if not release.wait(3):raise RuntimeError('scheduler release timeout')
        def worker(w,action,paused):
            log(w,'invoke',action)
            if not paused:invoked.set()
            try:
                if paused:
                    with before_line(AtomicEngine._call,'result = getattr(private',action=pause):r=call(action)
                else:r=call(action)
                r=('Licence:'+r.ticket) if type(r) is op.Licence else r
            except b.Rejection:r='Rejection'
            except BaseException as ex:failures.append(repr(ex));r='UNEXPECTED'
            results[w]=r;log(w,'response',r)
        a=Thread(target=worker,args=('A',first,True));a.start()
        if not entered.wait(3):raise RuntimeError('scheduler entry timeout')
        c=Thread(target=worker,args=('B',second,False));c.start()
        if not invoked.wait(3):raise RuntimeError('second invocation timeout')
        release.set();a.join(3);c.join(3)
        if a.is_alive() or c.is_alive() or failures:raise AssertionError(failures or 'join timeout')
        wantA=1 if first=='dispatch' else 'Rejection' if first=='bad_dispatch' else None
        wantB='Rejection' if second in ('dispatch','bad_dispatch') else None
        if first=='admit':
            if results['A']==results['B'] or not all(str(x).startswith('Licence:') for x in results.values()):raise AssertionError(results)
        elif results!={'A':wantA,'B':wantB}:raise AssertionError((first,second,results))
        all_rows.append({'first_lock_owner':first,'second_invocation':second,'linearisation_order':['A','B'],'events':events,'matches_abstract_history':True})
    # Mutator is interrupted after a provisional write while dispatch waits.
    e=AtomicEngine.standard();e.set_observation('v',[0,0]);lic=e.admit({'op':'edge','size':2,'source':0,'target':1})
    entered=Event();release=Event();invoked=Event();results={};events=[]
    def pause_fault(frame):
        entered.set()
        if not release.wait(3):raise RuntimeError('fault schedule timeout')
    def mutator():
        try:
            with before_line(op.Engine.set_observation,"for key in ['vocabulary'",MemoryError,pause_fault):e.set_observation('v',[0,1])
        except MemoryError:results['mutation']='MemoryError'
    def reader():
        invoked.set();results['dispatch']=e.dispatch(lic,0)
    a=Thread(target=mutator);a.start()
    if not entered.wait(3):raise RuntimeError('fault schedule entry')
    c=Thread(target=reader);c.start()
    if not invoked.wait(3):raise RuntimeError('fault schedule second invoke')
    release.set();a.join(3);c.join(3)
    if a.is_alive() or c.is_alive() or results!={'mutation':'MemoryError','dispatch':1} or e._engine._observations['v']!=(0,0):raise AssertionError(results)
    all_rows.append({'scenario':'provisional observation write -> synchronous fault while dispatch waits','results':results,'committed_observation':[0,0],'matches_abstract_history':True})
    (dest/'actual_concurrent_histories.json').write_text(json.dumps(all_rows,indent=2)+'\n')
    return {'forced_actual_thread_histories':len(all_rows),'mismatches':0,'fairness_or_all_schedule_claim':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    summary={'serial':oracle_census(args.out),'faults':faults(args.out),'concurrent':concurrency(args.out)}
    summary['files']=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(args.out.iterdir()) if p.is_file()]
    (args.out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
