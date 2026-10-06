"""Capture exact original calls and object hashes without changing science."""
from pathlib import Path
import runpy,subprocess,sys
import portable_source as source
import portable_admission as admission
from portable_collector import TRACE_SCHEMA

def capture_calls(api,original_run,trace,plan,state_path):
    api.require(api.canonical(plan['events'])==plan['event_plan_sha256'],'Changed portable event plan')
    capture=api.traced_run(original_run,trace);position=0;child_count=0
    def save():
        row={'schema':TRACE_SCHEMA,'events_observed':position,'children_observed':child_count,'complete':position==len(plan['events']) and child_count==len(plan['children']),'event_plan_sha256':plan['event_plan_sha256']}
        api.write_json(state_path,row);return row
    save()
    def invoke(argv,*args,**kwargs):
        nonlocal position,child_count
        api.require(position<len(plan['events']),'Extra portable original call')
        event=plan['events'][position];source.validate_call(api,event,argv,args,kwargs);position+=1
        if event['readonly']:
            try:return original_run(argv,**kwargs)
            finally:save()
        index=child_count;child_count+=1;rawcode=None
        try:
            result=capture(argv,**kwargs);rawcode=result.returncode
            api.require(type(rawcode) is int,'Original subprocess returned no integer code')
            return result
        finally:
            # Terminal trace is written by the base tracer on completion,
            # TimeoutExpired and KeyboardInterrupt. An abruptly killed tracer
            # may leave RUNNING; the collector refuses it, never inventing an end.
            path=api.path_in(trace,f'{index:04}.json')
            if path.is_file():
                row=api.read_json(path)
                current=api.sha(api.no_symlinks(event['source_path']).read_bytes())
                objects={}
                if event['object_path']:
                    obj=api.no_symlinks(event['object_path'])
                    if obj.is_file():objects[str(obj)]=api.sha(obj.read_bytes())
                row.update(raw_returncode=rawcode,timeout_seconds=event['timeout'],source_sha256_before=event['source_sha256'],source_sha256_after=current,output_absent_before=True,output_hashes_after=objects)
                api.write_json(path,row);save()
                api.require(current==event['source_sha256'],'Original portable source changed during child')
            else:save()
    def finish(require_complete=True):
        row=save()
        if require_complete:api.require(row['complete'],'Original portable call plan did not finish')
        return row
    invoke.finish=finish
    return invoke

def trace_driver(api,driver,trace,state_path,arguments):
    """Called only by separately reviewed family execution admission."""
    api.require(sys.flags.optimize==0,'Original portable assertions must remain enabled')
    api.require(len(arguments)==8 and arguments[::2]==['--review-zip','--lean-bin','--mathlib','--out'],'Portable original argument shape differs')
    driver=api.no_symlinks(driver).absolute();api.require(driver.name==admission.DRIVER['driver_path'] and api.sha(driver.read_bytes())==admission.DRIVER['driver_sha256'],'Portable original wrapper identity differs')
    archive=api.no_symlinks(arguments[1]);lean=(api.no_symlinks(arguments[3])/'lean').resolve();mathlib=api.no_symlinks(arguments[5]).resolve();output=api.no_symlinks(arguments[7]).absolute()
    api.require(output.name=='original' and not output.exists(),'Portable original output must be absent')
    plan=source.build_plan(api,archive,output,lean,mathlib,Path(sys.executable))
    trace=api.no_symlinks(trace);state_path=api.no_symlinks(state_path)
    api.require(not trace.exists() and not state_path.exists(),'Portable capture output already exists');trace.mkdir(parents=True)
    old_run=subprocess.run;old_argv=sys.argv;old_path=sys.path[:];old_bytecode=sys.dont_write_bytecode
    callback=capture_calls(api,old_run,trace,plan,state_path)
    succeeded=False
    try:
        subprocess.run=callback;sys.argv=[str(driver),*arguments];sys.path[0]=str(driver.parent);sys.dont_write_bytecode=True
        runpy.run_path(str(driver),run_name='__main__');succeeded=True
    finally:
        subprocess.run=old_run;sys.argv=old_argv;sys.path[:]=old_path;sys.dont_write_bytecode=old_bytecode
        callback.finish(require_complete=succeeded)
    return 0
