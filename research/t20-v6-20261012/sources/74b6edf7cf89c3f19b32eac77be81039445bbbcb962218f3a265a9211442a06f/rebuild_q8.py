import pathlib,json,os,subprocess,hashlib,datetime,re
R=pathlib.Path('private-locator:4bb2f72cdc070f304a86');E=R/'evidence';F=pathlib.Path('private-locator:4b06887cf6b87610e5b8');T=F/'lean-4.19.0-linux/bin';P=pathlib.Path('private-locator:6e1cdd2685640ba2eef0');M=pathlib.Path('private-locator:67a0368f452b0a176f36');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseenv={**os.environ,'PATH':str(T)+':'+os.environ['PATH']};baseenv.pop('LEAN_SYSROOT',None);baseenv.pop('LEAN_PATH',None)
paths=json.loads((E/'EXTENSION_REPLAY.json').read_text())['external_lean_path'];p02=str(P/'.lake/build/lib/lean')
result={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Q8 structural compiler addendum','modules':[]}
def compile(src,b,name,libs,expected=0):
 local=b/(name+'.lean');local.write_bytes(src.read_bytes());assert not (b/(name+'.olean')).exists()
 p=subprocess.run([str(T/'lean'),'-j1','-o',name+'.olean',name+'.lean'],cwd=b,env={**baseenv,'LEAN_PATH':':'.join(libs+paths)},capture_output=True,timeout=240)
 label='addendum-'+name;(E/(label+'.stdout')).write_bytes(p.stdout);(E/(label+'.stderr')).write_bytes(p.stderr)
 row={'module':name,'origin':str(src),'source_sha256':sha(src),'exit_code':p.returncode,'expected_exit':expected,'stdout_sha256':sha(E/(label+'.stdout')),'stderr_sha256':sha(E/(label+'.stderr'))}
 result['modules'].append(row);print(name,p.returncode,flush=True);assert p.returncode==expected,(name,p.stdout.decode())
 if expected==0:assert (b/(name+'.olean')).stat().st_size>0;row['artifact_sha256']=sha(b/(name+'.olean'))
 else:assert "proved that the proposition" in p.stdout.decode() and 'is false' in p.stdout.decode()
try:
 b=R/'q8-fresh';b.mkdir(exist_ok=True)
 seal=json.loads((P/'Q8_SEAL.json').read_text());assert all(sha(P/f)==h for f,h in seal['files'].items())
 q=json.loads((P/'receipts/q8-20260930T141007Z/Q8_RESULT.json').read_text());assert len(q['axioms'])==51
 assert all(sha(P/(f+'.lean'))==h for f,h in q['source_sha256'].items())
 for n in ['Q8Measure','Q8Machine','Q8Compiler','Q8Witnesses','Q8Audit']:compile(P/(n+'.lean'),b,n,[str(b),p02])
 text=(E/'addendum-Q8Audit.stdout').read_text();seen={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)};seen.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",text)});assert seen==q['axioms'];result['q8_51_axioms_exactly_match']=True
 for n,expected in [('Baseline',0),('WrongBoundMustFail',1),('WrongSnapshotMustFail',1)]:compile(P/'negative-controls'/(n+'.lean'),b,n,[str(b),p02],expected)
 result['status']='PASS_BOUNDED_ADDENDA_REPLAY'
except Exception as e:result['status']='FAIL_CLOSED';result['failure']=repr(e);raise
finally:result['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(E/'Q8_INDEPENDENT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
