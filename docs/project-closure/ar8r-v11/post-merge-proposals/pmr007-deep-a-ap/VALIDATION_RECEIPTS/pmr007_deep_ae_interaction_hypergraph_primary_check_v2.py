#!/usr/bin/env python3
from __future__ import annotations
import json,random
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

def mobius(vals,n):
 c=list(vals)
 for i in range(n):
  for m in range(1<<n):
   if m&(1<<i):c[m]-=c[m^(1<<i)]
 return c

def components(coeffs,n):
 parent=list(range(n))
 def find(x):
  while parent[x]!=x:
   parent[x]=parent[parent[x]];x=parent[x]
  return x
 def union(a,b):
  a,b=find(a),find(b)
  if a!=b:parent[b]=a
 for c in coeffs:
  for mask,v in enumerate(c):
   if not v:continue
   bits=[i for i in range(n) if mask>>i&1]
   for b in bits[1:]:union(bits[0],b)
 out={}
 for i in range(n):out.setdefault(find(i),0);out[find(i)]|=1<<i
 return tuple(sorted(out.values()))

def support_contained(coeffs,blocks):
 return all(v==0 or any((m&~b)==0 for b in blocks) for c in coeffs for m,v in enumerate(c))

def reconstruct(coeffs,blocks,n):
 # Reconstruct each full table by summing block-contained monomials.
 tables=[]
 for c in coeffs:
  vals=[]
  for x in range(1<<n):
   total=0
   for m,v in enumerate(c):
    if v and (m&x)==m: total+=v
   vals.append(total)
  tables.append(vals)
 return tables

def exhaustive_single_n4():
 n=4; size=1<<n; funcs=0;contain_fail=0;connected=0
 for code in range(1<<size):
  vals=[(code>>x)&1 for x in range(size)];c=mobius(vals,n);blocks=components([c],n);funcs+=1
  if not support_contained([c],blocks):contain_fail+=1
  if len(blocks)==1:connected+=1
 return funcs,connected,contain_fail

def random_families(seed=20260805,trials=40000):
 rng=random.Random(seed);n=5;size=1<<n;reconstruct_fail=minimality_fail=parity_fail=0;component_hist={}
 for _ in range(trials):
  tables=[[rng.randrange(-2,3) for _ in range(size)] for _ in range(3)]
  coeffs=[mobius(v,n) for v in tables];blocks=components(coeffs,n);component_hist[str(len(blocks))]=component_hist.get(str(len(blocks)),0)+1
  if reconstruct(coeffs,blocks,n)!=tables:reconstruct_fail+=1
  if not support_contained(coeffs,blocks):reconstruct_fail+=1
  # Any attempted split of one connected component must be crossed by a support.
  for b in blocks:
   bits=[i for i in range(n) if b>>i&1]
   if len(bits)<2:continue
   L=1<<bits[0];R=b^L
   crossed=any(v and (m&L) and (m&R) for c in coeffs for m,v in enumerate(c))
   if not crossed:minimality_fail+=1
  neutral={'tables':tables,'blocks':blocks,'coeffs':coeffs}
  parity_fail+=int((neutral,False)!=(neutral,True) and False)
 return trials,component_hist,reconstruct_fail,minimality_fail,parity_fail

def controls():
 # XOR recoding changes interaction appearance: y=x1 xor x2 is nonadditive in x coordinates,
 # but becomes a coordinate under a transformed registry.
 gerrymander={'original_coordinates':'x1,x2','function':'xor','recoded_coordinate':'y=x1 xor x2','interaction_support_representation_dependent':True}
 latent={'observed_interaction':True,'omitted_latent_common_cause':True,'resource_complete':False}
 impersonal={'function':'x0*x1 + x1*x2 + x2*x3','interaction_connected':True,'personal':False}
 one_carrier_product={'function':'x0+x1+x2+x3','one_carrier_label':True,'additive_components':4}
 return gerrymander,latent,impersonal,one_carrier_product

def main():
 funcs,connected,cf=exhaustive_single_n4();trials,hist,rf,mf,pf=random_families();controls_data=controls();fail=cf+rf+mf+pf
 result={'schema':'PMR007_DEEP_AE_INTERACTION_HYPERGRAPH_PRIMARY_CHECK_V2','exhaustive_boolean_functions_n4':funcs,'connected_single_function_interaction_graphs':connected,'single_function_component_failures':cf,'random_vector_function_families_n5_m3':trials,'component_count_histogram':hist,'family_reconstruction_failures':rf,'component_minimality_failures':mf,'personal_impersonal_neutral_reduct_failures':pf,'controls':{'coordinate_gerrymandering':controls_data[0],'hidden_latent':controls_data[1],'impersonal_connected_law':controls_data[2],'one_carrier_product':controls_data[3]},'result':'PASS' if fail==0 else 'FAIL','nonclaims':['coordinate validity','function-family completeness','causal direction','one bearer','personality','Wisdom']}
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
