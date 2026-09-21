#!/usr/bin/env python3
"""Executable positive OWOU witnesses and revision-sensitive law obligations.
This is finite executable evidence, not a Lean proof or arbitrary-law estimator.
"""
import json
from pathlib import Path
import operational as o
import reference as r
from boundaries import Rejection,load_json
import guarded_sampler as gs
import productive_observer as po
ROOT=Path(__file__).resolve().parent

def prim(n):return {'op':'primitive','name':n}
def model(v):return {'space':'tagged-uniform-intervals','law':'demonstration-law','weights':[[1,2],[1,2]],'view':v,'events':'full-measurable'}
def require(ok,why):
 if not ok:raise RuntimeError('demonstration failed: '+why)
def refused(f):
 try:f()
 except Rejection as e:return str(e)
 raise RuntimeError('required refusal did not occur')

def main():
 events=[];e=o.Engine()
 events.append({'test':'unavailable-before-add','refusal':refused(lambda:e.admit(prim('succ')))})
 e.revise_rule('primitive:succ',True);old=e.admit(prim('succ'))
 require(e.dispatch(old,2)==3,'nonidentity')
 events.append({'test':'add-permission-and-nonidentity','input':2,'output':e.dispatch(old,2)})
 e.revise_rule('primitive:succ',False)
 events.append({'test':'revocation','old_refusal':refused(lambda:e.dispatch(old,2)),'new_refusal':refused(lambda:e.admit(prim('succ')))})
 e.revise_rule('primitive:succ',True);new=e.revalidate(old)
 require(e.dispatch(new,4)==5,'revalidation')
 events.append({'test':'ABA-no-revival','old_refusal':refused(lambda:e.dispatch(old,2)),'new_output':e.dispatch(new,4)})
 e=o.Engine.standard();z=e.admit(prim('iszero'));distinct=[e.dispatch(z,0),e.dispatch(z,1)];require(distinct==[True,False],'distinction')
 c=e.admit({'op':'compose','first':prim('iszero'),'second':prim('not')})
 require([e.dispatch(c,0),e.dispatch(c,1)]==[False,True],'composition')
 events.append({'test':'distinguishable-and-composition','iszero':distinct,'composed':[e.dispatch(c,0),e.dispatch(c,1)]})
 p=load_json((ROOT/'examples/identity.json').read_bytes());_,ty=r.check(p)
 source=e.admit({'op':'core','proof':{'rule':'all_e','polymorphic':p,'type':ty}})
 out=e.dispatch(source,{'proof':p});term,result_ty=r.check(out['proof']);require(result_ty==ty,'source type')
 require(r.normalize(term)[0]==('i',),'self application')
 events.append({'test':'internal-source-self-instantiation-and-application','term':term,'type':result_ty,'normal':r.normalize(term)[0]})
 e.set_observation('coarse',[0,0]);edge=e.admit({'op':'edge','size':2,'source':0,'target':1});require(e.dispatch(edge,0)==1,'edge')
 e.set_observation('fine',[0,1]);events.append({'test':'active-invariant-revision','old_refusal':refused(lambda:e.dispatch(edge,0)),'fresh_refusal':refused(lambda:e.admit({'op':'edge','size':2,'source':0,'target':1}))})
 e.set_probability_observation('signal',model([0,0]));e.require_probability('primitive:succ','signal',[1,4]);coarse=e.admit(prim('succ'))
 delta=e.refine_probability_observation('signal',model([0,-1]));require(delta['increment']==[1,2],'exact fibre increment')
 events.append({'test':'quantitative-refinement','identity':delta,'old_refusal':refused(lambda:e.dispatch(coarse,2)),'fresh_refusal':refused(lambda:e.admit(prim('succ')))})
 e.require_probability('primitive:succ','signal',[3,4]);fine=e.admit(prim('succ'));require(e.dispatch(fine,2)==3,'new tolerance admission')
 events.append({'test':'new-evidence','certificate':e.describe(fine),'output':3})
 e.coarsen_probability_observation('signal',model([0,0]));renewed=e.revalidate(fine);require(e.dispatch(renewed,5)==6,'coarsening revalidation')
 events.append({'test':'coarsening-requires-new-authority','old_refusal':refused(lambda:e.dispatch(fine,5)),'new_output':6})
 left=load_json((ROOT/'examples/trueSelector.json').read_bytes());right=load_json((ROOT/'examples/falseSelector.json').read_bytes())
 spec={'kind':'quadratic','left':left,'right':right,'max_bits':8};cert=gs.certificate(gs.check(spec));sampler=e.admit({'op':'sampler_budgeted','source':spec,'max_pending':[1,256]})
 done=e.dispatch(sampler,[0,0]);pending=e.dispatch(sampler,[]);require(done['status']=='done' and pending['status']=='pending','sampler status distinction')
 events.append({'test':'typed-productive-source','certificate':cert,'leaf':done,'pending':pending,'overclaim_refusal':refused(lambda:e.admit({'op':'sampler_budgeted','source':spec,'max_pending':[1,512]}))})
 loop={'kind':'binary-tape-observer','transitions':[[[0,0,1],[0,0,1]]]};obs=e.admit({'op':'observer','source':loop,'invariant':[0]});obsout=e.dispatch(obs,[1,0,1]);require(obsout==[0,0,0],'productive observer certificate')
 events.append({'test':'finite-invariant-full-stream-certificate','certificate':po.certify_constant(loop,[0]),'input':[1,0,1],'output':obsout})
 class RejectAll:
  def admit(self,c):raise Rejection('all rejected')
  def dispatch(self,*_):raise Rejection('all rejected')
 require(not o.positive_probe(RejectAll()),'nonvacuity');require(o.positive_probe(o.Engine.standard()),'positive baseline')
 projection=e.project();require(len(projection)>0,'projection')
 print(json.dumps({'status':'PASS','scope':'FINITE_EXECUTABLE_EVIDENCE','kernel_verified':False,'positive_cases':len(events),'projection_current_entries':len(projection),'reject_all_fails':True,'events':events},indent=2))

if __name__=='__main__':main()
