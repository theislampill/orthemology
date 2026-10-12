from pathlib import Path
import subprocess,sys,json,hashlib,time,datetime
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[2]
LEAN=ROOT/'tranche20/hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux/bin/lean'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
commands=[('python-results',[sys.executable,str(BASE/'src/provision_semantics.py')]),
          ('python-tests',[sys.executable,str(BASE/'src/test_provision_semantics.py')]),
          ('trace-tests',[sys.executable,str(BASE/'src/trace_reduction.py')]),
          ('preservation-tests',[sys.executable,str(BASE/'src/preservation_modes.py')]),
          ('lean-version',[str(LEAN),'--version']),
          ('lean-kernel',[str(LEAN),'-o',str(BASE/'results/ProvisionIdentity.olean'),str(BASE/'src/ProvisionIdentity.lean')]),
          ('trace-lean-kernel',[str(LEAN),'-o',str(BASE/'results/TraceReduction.olean'),str(BASE/'src/TraceReduction.lean')])]
inputs=[BASE/'src'/p for p in ['provision_semantics.py','test_provision_semantics.py','ProvisionIdentity.lean','trace_reduction.py','preservation_modes.py','TraceReduction.lean']]
before={str(p.relative_to(BASE)):sha(p) for p in inputs}
results=[]
for label,cmd in commands:
    start=now(); tick=time.monotonic()
    r=subprocess.run(cmd,cwd=BASE,capture_output=True,text=True)
    elapsed=time.monotonic()-tick; end=now()
    log=BASE/'receipts'/('verified-'+label+'.log')
    log.write_text(r.stdout+r.stderr)
    results.append({'label':label,'command':cmd,'start_utc':start,'end_utc':end,
                    'process_elapsed_seconds':elapsed,'exit_code':r.returncode,
                    'log':str(log.relative_to(BASE)),'log_sha256':sha(log)})
    print(label, r.returncode, elapsed)
    if r.returncode: print(r.stdout+r.stderr)
after={str(p.relative_to(BASE)):sha(p) for p in inputs}
kernel=(BASE/'receipts/verified-lean-kernel.log').read_text()+(BASE/'receipts/verified-trace-lean-kernel.log').read_text()
report={'utc':now(),'commands':results,'input_sha256_before':before,'input_sha256_after':after,
        'inputs_unchanged':before==after,'no_sorry_in_successful_axiom_report':'sorryAx' not in kernel,
        'verified':all(r['exit_code']==0 for r in results) and before==after and 'sorryAx' not in kernel,
        'scope':'Only new provision-identity lane. Process times are tool execution, not research-active-time estimates.',
        'development_logs':'Earlier failing Lean probes and compilations are retained with no proof credit.'}
(BASE/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
if not report['verified']: sys.exit(1)
