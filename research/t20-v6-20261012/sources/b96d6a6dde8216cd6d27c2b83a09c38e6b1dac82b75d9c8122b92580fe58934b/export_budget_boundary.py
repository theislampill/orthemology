"""A source-accepted proof for which the actual partial exporter refuses."""
import pathlib,sys,json
src=pathlib.Path('private-locator:73b5d2cdcb4e2bc9b0cc')
sys.path.insert(0,str(src))
import reference,proof_export,boundaries
pid={'rule':'all_i','body':{'rule':'i','A':('v',0)}}
identity=('all',('arr',('v',0),('v',0)))
def balanced_identity(n):
    if n==0:return pid
    child=balanced_identity(n-1)
    return {'rule':'app','function':{'rule':'all_e','polymorphic':child,'type':identity},'argument':child}
proof=balanced_identity(8)
term,ty=reference.check(proof)
assert ty==identity
result={'source_check_accepts':True,'input_nodes':boundaries.bound_tree(proof),'term_nodes':boundaries.bound_tree(term),'expected_certificate_nodes':4*2**8-2}
try:
    proof_export.export('large_balanced_identity',boundaries.dump_json(proof))
    result['export_result']='ACCEPT'
except boundaries.Rejection as ex:
    result.update(export_result='REFUSE',export_reason=str(ex))
assert result['export_reason']=='export: certificate constructor budget'
print(json.dumps(result,indent=2))
