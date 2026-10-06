#!/usr/bin/env python3
"""Public projection rejection controls; writes only into a new supplied work tree."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys
sys.dont_write_bytecode=True
from verify_artifact import verify, require, digest, json_read
ROOT=Path(__file__).resolve().parent
def write(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')
def reseal(root):
    files=[{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
           for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
    write(root/'MANIFEST.json',{'schema':'ninth-selector-public-v1','files':files})
    return digest(root/'MANIFEST.json')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--expected-manifest-sha256',required=True)
    a=p.parse_args();verify(ROOT,a.expected_manifest_sha256)
    work=a.work.resolve()
    require(not work.exists() and not work.is_relative_to(ROOT), 'Work must be absent and outside the package')
    work.mkdir(parents=True)
    cases=['positive','changed-source','missing-file','extra-file','symlink',
           'omitted-nonnull-destination','required-source-omitted','changed-original-manifest',
           'duplicate-map-entry','incomplete-map','wrong-proof-binding','unbound-Lean-source','host-path']
    results=[]
    for optimized in [False,True]:
        for case in cases:
            tree=work/('optimized' if optimized else 'normal')/case
            shutil.copytree(ROOT,tree)
            expected=a.expected_manifest_sha256
            source=tree/'scientific/A1/FiniteRadixNormalForm.lean'
            mapfile=tree/'projection/A1_SOURCE_MAP.json'
            if case=='changed-source':source.write_text(source.read_text()+'\n-- changed\n')
            elif case=='missing-file':source.unlink()
            elif case=='extra-file':(tree/'extra.txt').write_text('extra')
            elif case=='symlink':(tree/'extra-link').symlink_to('SCIENTIFIC_SCOPE.md')
            elif case in ['omitted-nonnull-destination','required-source-omitted','duplicate-map-entry','incomplete-map']:
                m=json_read(mapfile)
                if case=='omitted-nonnull-destination':
                    row=next(r for r in m['entries'] if r['disposition']=='OMITTED');row['public_path']='SCIENTIFIC_SCOPE.md'
                elif case=='required-source-omitted':
                    row=next(r for r in m['entries'] if r['original_path'].endswith('FiniteRadixNormalForm.lean'))
                    row.update(disposition='OMITTED',public_path=None,public_replacement='SCIENTIFIC_SCOPE.md',reason='Test deletion')
                elif case=='duplicate-map-entry':m['entries'].append(m['entries'][0])
                else:m['entries'].pop()
                write(mapfile,m);expected=reseal(tree)
            elif case=='changed-original-manifest':
                f=tree/'originals/A1/SOURCE_MANIFEST.json';f.write_text(f.read_text()+'\n');expected=reseal(tree)
            elif case=='wrong-proof-binding':
                f=tree/'PROOF_SOURCE_BINDINGS.json';m=json_read(f);m['files'][0]['sha256']='0'*64;write(f,m);expected=reseal(tree)
            elif case=='unbound-Lean-source':
                (tree/'Unbound.lean').write_text('-- not compiled\n');expected=reseal(tree)
            elif case=='host-path':
                (tree/'host.txt').write_text('/'+'workspace/example');expected=reseal(tree)
            cmd=[sys.executable]+(['-O'] if optimized else [])+['-B',str(ROOT/'verify_artifact.py'),
                '--root',str(tree),'--expected-manifest-sha256',expected]
            q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            wanted=case=='positive'
            require((q.returncode==0)==wanted, 'Unexpected artifact test outcome: '+case)
            results.append({'case':case,'optimized':optimized,'accepted':q.returncode==0,'expected_outcome':True})
    result={'status':'PASS_PUBLIC_ARTIFACT_CONTROLS','input_manifest_sha256':a.expected_manifest_sha256,
            'verifier_sha256':digest(ROOT/'verify_artifact.py'),'cases':results,
            'case_count':len(results),'lean_processes_started':False}
    write(work/'RESULT.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
