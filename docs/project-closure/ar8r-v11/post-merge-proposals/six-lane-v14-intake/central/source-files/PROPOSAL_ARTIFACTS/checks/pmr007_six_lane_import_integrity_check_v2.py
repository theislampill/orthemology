from pathlib import Path
import hashlib,json,re,yaml
ROOT=Path(__file__).resolve().parents[1]
y=ROOT/'synchronization/AR8R_SIX_LANE_IMPORT_ADJUDICATION_AFTER_DEEP_CT_V2.yaml'
d=yaml.safe_load(y.read_text(encoding='utf-8'))
fail=[]
if d['repository_authority']!='9b80f2dfdf73a768ccad6a6ea2f2998c70ebdcf3': fail.append('repo')
if len(d['imports'])!=6: fail.append('lane_count')
for row in d['imports']:
    for k in ['lane','source_artifact','frozen_artifact_sha256','claim_evidence_class','affected_nodes','conflicts','central_adoption']:
        if k not in row: fail.append(f"missing:{row.get('lane')}:{k}")
    h=row['frozen_artifact_sha256']
    if h!='NOT_SURFACED_TO_CENTRAL_RUNTIME' and not re.fullmatch(r'[0-9a-f]{64}',h): fail.append(f"hash:{row['lane']}")
if d['deduplication']['new_independent_theorem_origins_from_imports']!=0: fail.append('multiplicity')
ca=d['central_adjudication']
if ca['integrated_champion']!='NONE' or ca['meniscus']!='MENISCUS_NOT_REACHED' or ca['natural_closure']!='NOT_REACHED': fail.append('closure')
# local current artifacts must match reported hashes
local_expected={
 'deep_ct/PMR-007_DEEP_ROUND_CT_PARTIAL_COMMON_INTERVENTION_DOMAIN_V2.md':'057451541f01369e501ee18470dc11780383819ea8efce03e276f3ad70d8b26e',
 'deep_ct/PMR-007_DEEP_CT_ADMISSION_OVERLAY.yaml':'412593543dd7a13ddf77da5c780125b3b9d47b480176949d5ddc63672050da51',
 'checks/pmr007_deep_ct_distinct_conflict_graph_rereview_results.json':'fa16d66f6c7527eb0164c6f4a1151fb2d0ab8a760159ab1fe62dc71f55b22494'}
for rel,exp in local_expected.items():
 p=ROOT/rel; act=hashlib.sha256(p.read_bytes()).hexdigest()
 if act!=exp: fail.append(f'local_hash:{rel}')
res={'schema':'pmr007-six-lane-import-integrity-v2','pass':not fail,'failures':fail,'imports':len(d['imports']),'new_theorem_origins':d['deduplication']['new_independent_theorem_origins_from_imports'],'local_hashes_checked':len(local_expected)}
out=ROOT/'checks/pmr007_six_lane_import_integrity_check_v2_results.json'
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps(res,indent=2,sort_keys=True))
raise SystemExit(0 if res['pass'] else 1)
