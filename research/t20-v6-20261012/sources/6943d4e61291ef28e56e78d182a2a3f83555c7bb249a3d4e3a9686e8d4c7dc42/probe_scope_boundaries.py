#!/usr/bin/env python3
"""Two small new scope controls, not a historical acceptance replay."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,os,sys
from test_new_frontier import b,export_module_owned

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--canonical-source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    original=a.canonical_source/'proof_export.py'
    spec=importlib.util.spec_from_file_location('p03_canonical_export_scope_probe',original)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    raw=b.dump_json({'rule':'i','A':['bottom']})
    legacy=module.module([iter(('legacyRow',raw))])
    assert 'legacyRowCertificate' in legacy
    try:export_module_owned([iter(('legacyRow',raw))])
    except b.Rejection as ex:refusal=str(ex)
    else:raise AssertionError('strict adapter accepted arbitrary row iterator')
    immutable=export_module_owned([('legacyRow',raw)])
    assert legacy==immutable
    # Support-level trace equality is strictly weaker than law equality.
    concrete={0:F(1,2),1:F(1,2)};abstract={0:F(3,4),1:F(1,4)}
    assert set(concrete)==set(abstract) and concrete!=abstract
    pair=lambda q:[q.numerator,q.denominator]
    result={'status':'PASS','kernel_credit':False,'checks':[
      {'id':'P03-A2-COMPAT-ITERABLE','canonical_export_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
       'legacy_generator_row_accepted':True,'new_named_strict_entry_refusal':refusal,
       'immutable_row_output_exactly_equal':True,'meaning':'No owner decision to remove legacy behavior was assumed. This is a separately named strict entry.'},
      {'id':'P03-A2-CE-TRACE-LAW','same_trace_support':[0,1],
       'concrete_masses':{str(k):pair(v) for k,v in concrete.items()},
       'abstract_masses':{str(k):pair(v) for k,v in abstract.items()},
       'probability_laws_equal':False,'meaning':'Trace support or trace inclusion does not identify a probability law.'}]}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
