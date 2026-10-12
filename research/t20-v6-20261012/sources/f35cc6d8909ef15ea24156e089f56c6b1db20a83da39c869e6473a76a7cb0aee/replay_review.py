"""Portable independent-control replay against one exact source ZIP.
The companion binds the source archive, not its own eventual ZIP hash.
"""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,math,os,re,signal,stat,subprocess,sys,time,zipfile
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
SOURCE_ZIP_SHA='19f90a7bfd9bd2840c71c972029447533e9f5985281c275c5c0979ff8597f906'
SOURCE_ZIP_BYTES=2438940
SOURCE_PUBLIC_SHA='6acd4dc584cb37c7c9e168dd71f912f96cd31fedc9f408fdb8742450462dc9fa'
SCIENCE_SHA='186281d14d0ea41e7ac49aa7a392a6cf05cb92047670f7d639420720785ecf0e'
REVIEW_ORDER_SHA='b3caf1d93d2d96566d46442f1fac185b8ac9772a8eb12bc3b0a6099e382a9c43'
RECEIPTS={
 'ACTUAL_BATCH_V1_RECEIPT.json':'1e88d4cb552b09d41804bec43c8ac0cb1941656112e4a0eecd004cfccd700b2c',
 'ACTUAL_BATCH_V3_RECEIPT.json':'d38077d680cf8d038be2dd05fc1fcfa388d0abcf753d0d9c8b0a6a2aa531e476',
 'ACTUAL_BATCH_V4_RECEIPT.json':'98165df6e71d72ab167f66dc27a617a6e31b1d67ee417bb54965a208801aa1c9',
 'BATCH_RETRY_CORRIGENDUM_V1_RECEIPT.json':'b6a9bf294ab6abbc1bcecb34b85604ce4c296275f5c8da03dd50e6baa26d4eca'}
SOURCE_FOLDER='Eighth_Actual_Batch_Controller_Source'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest()

def canonical(relative):
    path=Path(relative)
    require(not path.is_absolute() and path.parts and str(path)==relative and '\\' not in relative and
        all(p not in ('','.','..') for p in path.parts),f'Unsafe relative path: {relative}')
    return path

def regular(base,relative):
    path=base
    for part in canonical(relative).parts:
        path=path/part;require(not path.is_symlink(),f'Symlink in input: {relative}')
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode),f'Not a regular input: {relative}')
    return path

def verify_record(base,row):
    p=regular(base,row['path'])
    require(p.stat().st_size==row.get('bytes',row.get('size')) and digest(p)==row['sha256'],f'Identity mismatch: {row["path"]}')

def fresh_output(path,protected):
    require(not path.exists() and not path.is_symlink(),'Output must be absent')
    path=path.resolve()
    for base in protected:
        base=base.resolve();require(path!=base and base not in path.parents,'Output is inside a protected input/dependency tree')
    return path

def safe_extract(archive,destination):
    require(not destination.exists() and not destination.is_symlink(),'Extraction destination must be absent')
    with zipfile.ZipFile(archive) as z:
        rows=z.infolist();names=[r.filename for r in rows]
        require(len(names)==len(set(names)),'Duplicate archive member')
        require(sum(r.file_size for r in rows)<=64*1024*1024,'Unexpected archive expansion')
        for r in rows:
            path=canonical(r.filename)
            require(path.parts[0]==SOURCE_FOLDER and len(path.parts)>1,'Wrong source archive root')
            require(not r.is_dir() and stat.S_IFMT(r.external_attr>>16) in (0,stat.S_IFREG),'Nonregular archive entry')
        destination.mkdir(parents=True,exist_ok=False)
        for r in rows:
            p=destination/canonical(r.filename);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(r))
    return destination/SOURCE_FOLDER

def verify_companion():
    manifest=json.loads(regular(ROOT,'ACCEPTANCE_MANIFEST.json').read_text())
    paths=[r['path'] for r in manifest['files']];require(len(paths)==len(set(paths)),'Duplicate companion member')
    expected=set(paths)|{'ACCEPTANCE_MANIFEST.json'};observed=set()
    directories={str(p) for name in expected for p in Path(name).parents if str(p)!='.'}
    for p in ROOT.rglob('*'):
        name=str(p.relative_to(ROOT));require(not p.is_symlink(),'Companion symlink')
        if p.is_dir():require(name in directories,'Unlisted companion directory')
        else:require(p.is_file(),'Nonregular companion member');observed.add(name)
    require(observed==expected,'Companion inventory mismatch')
    for row in manifest['files']:verify_record(ROOT,row)
    require(digest(regular(ROOT,'records/REVIEW_SOURCE_ORDER_V4.json'))==REVIEW_ORDER_SHA,'Reviewer source order changed')
    order=json.loads((ROOT/'records/REVIEW_SOURCE_ORDER_V4.json').read_text())
    require(order['candidate_manifest_sha256']==SCIENCE_SHA and len(order['modules'])==9,'Wrong review scope')
    for name,sha in RECEIPTS.items():
        p=regular(ROOT,'records/'+name);require(digest(p)==sha,'A sealed scientific receipt changed')
        receipt=json.loads(p.read_text())
        for row in receipt.get('bound_review_artifacts',[]):verify_record(ROOT/'records',row)
    for row in order['modules']:verify_record(ROOT/'records',row)
    binding=json.loads(regular(ROOT,'SOURCE_ARCHIVE.json').read_text())
    require(binding['sha256']==SOURCE_ZIP_SHA and binding['bytes']==SOURCE_ZIP_BYTES and
        binding['public_manifest_sha256']==SOURCE_PUBLIC_SHA and binding['scientific_manifest_sha256']==SCIENCE_SHA,
        'Source archive binding changed')
    return digest(ROOT/'ACCEPTANCE_MANIFEST.json'),order

def run_source_command(command,env,log,timeout,cwd):
    started=time.monotonic();p=subprocess.Popen(command,env=env,cwd=cwd,stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,text=True,start_new_session=True)
    timed_out=False
    try:text=p.communicate(timeout=timeout)[0];code=p.returncode
    except subprocess.TimeoutExpired:
        timed_out=True
        try:os.killpg(p.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:text=p.communicate(timeout=5)[0]
        except subprocess.TimeoutExpired:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            text=p.communicate()[0]
        text+=f'\nREPLAY_TIMEOUT after {timeout} seconds\n';code=None
    except BaseException:
        if p.poll() is None:
            try:os.killpg(p.pid,signal.SIGTERM)
            except ProcessLookupError:pass
            try:p.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                p.communicate()
        raise
    log.write_text(text)
    return {'exit_code':code,'timed_out':timed_out,'text':text,'seconds':round(time.monotonic()-started,3),
        'command':command,'compiler_cwd':str(cwd),'log_sha256':digest(log)}

def propagated_source_failure(science_output,fallback):
    failure=science_output/'REPLAY_FAILURE.json'
    if not failure.exists() or failure.is_symlink() or (science_output/'RECEIPT.json').exists():return fallback
    try:record=json.loads(failure.read_text())
    except (OSError,ValueError):return fallback
    if (isinstance(record,dict) and record.get('public_manifest_sha256')==SOURCE_PUBLIC_SHA and
        record.get('no_success_receipt') is True and record.get('status') in ('FAIL','INCONCLUSIVE')):
        return record['status']
    return fallback

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-zip',type=Path,required=True)
    parser.add_argument('--lean-root',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage-timeout',type=float,default=300)
    args=parser.parse_args()
    require(math.isfinite(args.stage_timeout) and 0<args.stage_timeout<=600,'Invalid per-stage timeout')
    leanroot,mathlib,archive=args.lean_root.resolve(),args.mathlib.resolve(),args.source_zip.resolve()
    output=fresh_output(args.output,[ROOT,leanroot,mathlib,archive])
    identity,order=verify_companion()
    require(archive.is_file() and archive.stat().st_size==SOURCE_ZIP_BYTES and digest(archive)==SOURCE_ZIP_SHA,'Wrong source ZIP bytes')
    output.mkdir(parents=True,exist_ok=False);(output/'logs').mkdir();stages=[];status='FAIL'
    try:
        source=safe_extract(archive,output/'extracted source')
        helper_spec=importlib.util.spec_from_file_location('bound_source_replay',source/'replay.py')
        helper=importlib.util.module_from_spec(helper_spec);helper_spec.loader.exec_module(helper)
        source_identity,index=helper.verify_checkpoint();require(source_identity==SOURCE_PUBLIC_SHA,'Wrong extracted public component')
        cachepin=json.loads((source/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
        env=helper.sanitized_env([],mathlib,cachepin)
        science_output=output/'fresh science'
        command=[sys.executable,'-B',str(source/'replay.py'),'--lean-root',str(leanroot),'--mathlib',str(mathlib),
            '--output',str(science_output),'--stage-timeout',str(args.stage_timeout)]
        result=run_source_command(command,env,output/'logs/source-component.log',args.stage_timeout*63+180,ROOT)
        status=helper.failure_classification(result)
        if not helper.clean_positive_result(result):status=propagated_source_failure(science_output,status)
        require(helper.clean_positive_result(result),'Fresh source-component replay failed')
        scientific=json.loads(regular(science_output,'RECEIPT.json').read_text())
        require(scientific['status']=='PASS' and scientific['public_manifest_sha256']==SOURCE_PUBLIC_SHA and
            scientific['scientific_manifest_sha256']==SCIENCE_SHA and scientific['prior_custom_objects_reused']==0,
            'Unexpected source replay receipt')
        science_objects={row['module']+'.olean':row['object_sha256'] for row in scientific['stages'] if 'object_sha256' in row}
        helper.verified_build_inventory(science_output/'build',science_objects)
        build=output/'fresh review';build.mkdir();objects={};env=helper.sanitized_env([build,science_output/'build'],mathlib,cachepin)
        names=[];theorems=[];sources=[]
        for row in order['modules']:
            require(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',row['module']) is not None,'Invalid reviewer module name')
            path=regular(ROOT,'records/'+row['path']);declarations=helper.named_declarations(path.read_text(),row['namespace'])
            require(declarations==row['named_explicit_declarations'],'Reviewer declaration inventory differs')
            names += [r['name'] for r in declarations];theorems += [r['name'] for r in declarations if r['kind']=='theorem']
            sources.append((row['module'],path))
        require(len(names)==len(set(names))==78 and len(theorems)==47,'Wrong reviewer audit count')
        audit=output/'ReviewerNamedDeclarations.lean'
        audit.write_text('\n'.join(['import '+name for name,_ in sources]+['#print axioms '+name for name in names])+'\n')
        sources.append(('ReviewerNamedDeclarations',audit))
        for name,path in sources:
            helper.verified_build_inventory(science_output/'build',science_objects);helper.verified_build_inventory(build,objects)
            result=helper.run_compiler_stage([str(leanroot/'bin/lean'),'-j1','-s65536',f'--root={path.parent}',
                '-o',str(build/f'{name}.olean'),str(path)],env,output/'logs'/f'{name}.log',args.stage_timeout)
            status=helper.failure_classification(result)
            require(helper.clean_positive_result(result),f'Reviewer source stage failed: {name}')
            objects[name+'.olean']=digest(regular(build,name+'.olean'))
            stages.append({'module':name,'source_sha256':digest(path),'object_sha256':objects[name+'.olean'],
                **{k:v for k,v in result.items() if k!='text'}})
        axioms=helper.audit_axioms((output/'logs/ReviewerNamedDeclarations.log').read_text(),names)
        helper.verified_build_inventory(science_output/'build',science_objects);helper.verified_build_inventory(build,objects)
        require(verify_companion()[0]==identity and helper.verify_checkpoint()[0]==SOURCE_PUBLIC_SHA,'A verified component changed')
        helper.verify_dependencies(leanroot,mathlib)
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source_zip_sha256':SOURCE_ZIP_SHA,'source_public_manifest_sha256':SOURCE_PUBLIC_SHA,
            'scientific_manifest_sha256':SCIENCE_SHA,'companion_manifest_sha256':identity,
            'source_replay_receipt_sha256':digest(science_output/'RECEIPT.json'),'fresh_source_modules':61,
            'source_named_declarations':902,'author_theorems':476,'fresh_reviewer_modules':9,
            'reviewer_named_declarations':78,'reviewer_theorems':47,'prior_scientific_objects_reused':0,
            'review_source_order_sha256':REVIEW_ORDER_SHA,'scientific_receipt_sha256':RECEIPTS,
            'reviewer_axioms':axioms,'stages':stages,'dependencies_mutated':False,
            'claim':'Independent source-control replay against exact accepted batch source ZIP; no self-certification of the eventual companion ZIP.'}
        (output/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps({k:receipt[k] for k in ['status','source_zip_sha256','source_named_declarations','reviewer_named_declarations']},indent=2))
    except BaseException as error:
        if isinstance(error,(KeyboardInterrupt,OSError,subprocess.TimeoutExpired)):status='INCONCLUSIVE'
        (output/'RECEIPT.json').unlink(missing_ok=True)
        (output/'REPLAY_FAILURE.json').write_text(json.dumps({'status':status,'error':str(error),'stages':stages,
            'source_zip_sha256':SOURCE_ZIP_SHA,'no_success_receipt':True},indent=2)+'\n')
        raise

if __name__=='__main__':main()
