#!/usr/bin/env python3
"""Reconstruct a NEW research directory; never modifies a repository or input."""
from pathlib import Path
import argparse,hashlib,io,json,zipfile
from verify_checkpoint import verify_previous,sha,require
PREFIX='source-main/experiments/orthemology-v5/source/'
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=Path(__file__).resolve().parents[1];out=a.out.expanduser().absolute()
    require(not out.exists(),'Refusing existing workspace')
    data=(root/'inputs/Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0001.zip').read_bytes();verification=verify_previous(data,'P03')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        with zipfile.ZipFile(io.BytesIO(z.read('inputs/Orthemology_Pro_P03_Engine_Refinement.zip'))) as n:
            canonical={p[len(PREFIX):]:n.read(p) for p in n.namelist() if p.startswith(PREFIX)}
        require(len(canonical)==70,'unexpected source count');source=dict(canonical)
        for repo,row in json.loads(z.read('proposal/PATCH_MAP.json')).items():
            rel=repo.removeprefix('experiments/orthemology-v5/source/')
            require(sha(source[rel])==row['preimage_sha256'] and source[rel]==z.read('proposal/preimages/'+rel),'preimage '+rel)
            post=z.read('proposal/postimages/'+rel);require(sha(post)==row['postimage_sha256'],'postimage '+rel);source[rel]=post
    out.mkdir(parents=True)
    for label,tree in [('source',source),('canonical',canonical)]:
        for name,b in tree.items():p=out/label/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    result={'status':'ISOLATED_SOURCE_PREPARED','source_files':len(source),'canonical_files':len(canonical),'source_sha256':{k:sha(v) for k,v in sorted(source.items())},'canonical_sha256':{k:sha(v) for k,v in sorted(canonical.items())},'source_path':str(out/'source'),'canonical_path':str(out/'canonical'),'predecessor':verification,'canonical_effect':False}
    (out/'WORKSPACE_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','canonical_sha256']},indent=2))
if __name__=='__main__':main()
