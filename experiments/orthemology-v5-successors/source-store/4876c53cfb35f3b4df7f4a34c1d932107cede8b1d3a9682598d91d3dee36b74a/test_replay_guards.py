#!/usr/bin/env python3
"""Test the public core-reuse guard using non-executable minimal fixtures."""
from pathlib import Path
import argparse, json, sys
sys.dont_write_bytecode=True
from replay import check_core_cache
from verify_artifact import require, digest
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    work=a.work.resolve();require(not work.exists(),'Work must be absent');work.mkdir(parents=True)
    cases=['positive','extra-object','missing-object','symlink','wrong-object-digest',
           'wrong-source-digest','duplicate-module','missing-readback','wrong-status']
    results=[]
    for case in cases:
        out=work/case;build=out/'runtime/build';build.mkdir(parents=True)
        sources={};runs=[]
        for i in range(167):
            name='Fixture'+str(i);f=build/(name+'.olean');f.write_bytes(b'Non-executable census fixture\n')
            sources[name]={'sha256':'source-'+name}
            runs.append({'suite':'runtime','module':name,'exit_code':0,'source_sha256':'source-'+name,'object_sha256':digest(f)})
        runs.append({'suite':'runtime','module':'RuntimeReadback','exit_code':0})
        result={'status':'COMPLETED_FRESH_REPLAY','source_manifest_sha256':'bound-manifest','runs':runs,'runtime':{'axiom_readbacks':13}}
        if case=='extra-object':(build/'Extra.olean').write_bytes(b'extra')
        elif case=='missing-object':(build/'Fixture0.olean').unlink()
        elif case=='symlink':(build/'link').symlink_to('Fixture0.olean')
        elif case=='wrong-object-digest':runs[0]['object_sha256']='0'*64
        elif case=='wrong-source-digest':runs[0]['source_sha256']='wrong'
        elif case=='duplicate-module':runs.append(runs[0])
        elif case=='missing-readback':runs.pop()
        elif case=='wrong-status':result['status']='RUNNING'
        write(out/'RESULT.json',result)
        try:check_core_cache(out,sources,'bound-manifest');accepted=True
        except ValueError:accepted=False
        require(accepted==(case=='positive'),'Unexpected core guard outcome: '+case)
        results.append({'case':case,'accepted':accepted,'expected_outcome':True})
    record={'status':'PASS_PUBLIC_CORE_REUSE_GUARDS','optimized_python':bool(sys.flags.optimize),
            'driver_sha256':digest(Path(__file__).parent/'replay.py'),'cases':results,
            'fixtures_are_non_executable':True,'lean_processes_started':False}
    write(work/'RESULT.json',record);print(json.dumps(record,indent=2))
if __name__=='__main__':main()
