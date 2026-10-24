"""Named replay in exact original contexts; no borrowed execution credit."""
from __future__ import annotations
import argparse, importlib.util, json, os, re, signal, subprocess, sys, time
from pathlib import Path
from source_provider import SourceError, SourceProvider, safe_path, sha256
from rehydrate import restore, verify_workspace, tree_identity
BASELINE="a7ff0e33d1a299db640041c46b1af81ca70851f6"
TREE="9cd3f787299b774513f68837112d5f138b093dbd"
FILES=16103

WORKFLOW_SHA256='6239bb5f7f0b78f71e61173465b0f7b1842dc0aaa015f921c8d1301689ed17fc'
CASES_SHA256='d37499c78f15ba9a0146283c17652f59626ab57d6505de261f4bff90150749aa'
INTEGRITY_ROUTES_SHA256='5f631db0bfd69cb6e0e7a8bdc5dffbdff046d9d8da3889b7b78d43f2f51031b7'
GENERATORS_SHA256='bcc19d2c72e5f279e17eeb9eef042553d7eba96601f78b653782605f93679f32'

class Blocked(RuntimeError): pass
class ProcessFailure(RuntimeError): pass

def require(condition,message):
    if not condition: raise ValueError(message)

def write_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")

def load_spec(provider):
    spec=provider.manifest.get("replay")
    require(isinstance(spec,dict),"reviewed replay mapping absent from archive lock")
    canonical=lambda value: sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode())
    require(canonical(spec.get("cases"))==CASES_SHA256,"fixed selection, readback or recipe differs")
    require(canonical(spec.get("integrity_routes"))==INTEGRITY_ROUTES_SHA256,"integrity evaluator mapping differs")
    require(canonical(spec.get("generators"))==GENERATORS_SHA256,"generator recipe mapping differs")
    require(spec.get("workflow",{}).get("path")==".github/workflows/validate.yml" and spec["workflow"].get("sha256")==WORKFLOW_SHA256,"wrong original workflow")
    require(spec.get("schema")=="orthemology-r0002-replay-cases-v1","unknown replay schema")
    require(spec["baseline"]=={"commit":BASELINE,"tree":TREE,"files":FILES},"wrong replay baseline")
    require(provider.baseline["commit"]==BASELINE and provider.baseline["tree"]==TREE,"provider/replay edition mismatch")
    require(len(provider.occurrences)==FILES,"empty or changed original population")
    require(tree_identity(provider.occurrences.values())==TREE,"original tree denominator differs")
    workflow=provider.read_bytes(spec["workflow"]["path"])
    require(sha256(workflow)==spec["workflow"]["sha256"],"workflow identity changed")
    steps=spec["workflow"]["steps"]
    require(len(steps)==71 and len({x["id"] for x in steps})==71,"missing or duplicate CI obligation")
    require(sum(len(x["command"].splitlines()) for x in steps)==158,"CI command denominator changed")
    commands=[]; lines=workflow.decode().splitlines();i=0
    while i<len(lines):
        if lines[i].startswith("        run: "):
            command=lines[i].split(": ",1)[1]
            if command=="|":
                i+=1;body=[]
                while i<len(lines) and (lines[i].startswith("          ") or not lines[i].strip()):
                    body.append(lines[i][10:]);i+=1
                i-=1;command="\n".join(body).rstrip()
            commands.append(command)
        i+=1
    require(commands==[x["command"] for x in steps],"mapped CI commands differ from original workflow")
    for step in steps:
        require(not step.get("retired") and step["route"]=="preserved-original","unreviewed retirement")
        require(sha256(step["command"].encode())==step["command_sha256"],"CI command digest changed")
    require(len(spec["cases"])==8 and len({x["id"] for x in spec["cases"]})==8,"eight fixed cases required")
    for case in spec["cases"]:
        for key in ("descriptor","runner"):
            if key in case:
                item=case[key];raw=provider.read_bytes(item["path"])
                require(len(raw)==item["bytes"] and sha256(raw)==item["sha256"],"wrong runner or descriptor: "+item["path"])
    return spec

def clean_environment(home,tmp,python=None):
    home=Path(home);tmp=Path(tmp)
    home.mkdir(parents=True,exist_ok=True);tmp.mkdir(parents=True,exist_ok=True)
    env={"PATH":os.defpath,"HOME":str(home),"TMPDIR":str(tmp),"LANG":"C.UTF-8","LC_ALL":"C.UTF-8",
         "PYTHONDONTWRITEBYTECODE":"1","RUNNER_TEMP":str(tmp),"GIT_CONFIG_GLOBAL":os.devnull,
         "GIT_CONFIG_SYSTEM":os.devnull,"GIT_TERMINAL_PROMPT":"0"}
    if python is not None: env["PATH"]=str(Path(python).absolute().parent)+os.pathsep+os.defpath
    return env

class Session:
    def __init__(self,out,python=None,timeout=1800):
        self.out=Path(out).absolute()
        require(not self.out.exists(),"output already exists; receipt reuse prohibited")
        self.out.mkdir(parents=True)
        self.env=clean_environment(self.out/"home",self.out/"tmp",python);self.timeout=timeout
        self.receipt={"schema":"orthemology-replay-session-v1","status":"RUNNING","execution_credit":False,"commands":[],"baseline":BASELINE}
        self.save()
    def save(self): write_json(self.out/"RUN.json",self.receipt)
    def run(self,argv,cwd,*,env=None,allowed=(0,),timeout=None):
        log=self.out/("command-%03d.log"%len(self.receipt["commands"]))
        command=list(map(str,argv));start=time.monotonic()
        with log.open("wb") as stream:
            process=subprocess.Popen(command,cwd=cwd,env={**self.env,**(env or {})},stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            timed_out=False
            try: rc=process.wait(timeout=timeout or self.timeout)
            except subprocess.TimeoutExpired:
                timed_out=True;os.killpg(process.pid,signal.SIGKILL);rc=process.wait()
        self.receipt["commands"].append({"argv":command,"cwd":str(cwd),"exit":rc,"seconds":round(time.monotonic()-start,6),"timeout":timed_out,"log":log.name,"log_sha256":sha256(log.read_bytes())});self.save()
        if timed_out: raise TimeoutError("process timeout; no theorem-rejection or PASS credit")
        if rc not in allowed: raise ProcessFailure("original process exit %s; see %s"%(rc,log))
        return log.read_text(errors="replace")

def python_preflight(executable,required=None,expected_hash=None,env=None):
    executable=Path(executable).absolute()
    if not executable.is_file(): raise Blocked("exact Python executable unavailable: "+str(executable))
    raw=subprocess.check_output([str(executable),"-E","-B","-c","import platform; print(platform.python_version())"],timeout=30,env=env)
    version=raw.decode().strip()
    if required and version!=required: raise Blocked("requires Python "+required+"; found "+version)
    digest=sha256(executable.read_bytes())
    if expected_hash and digest!=expected_hash: raise ValueError("Python version matched but executable digest differs")
    return {"version":version,"sha256":digest,"path":str(executable)}

def git(context,*args):
    return subprocess.check_output(["git","-C",str(context),*args],stderr=subprocess.STDOUT,timeout=60).decode().strip()

def assert_history(context,spec):
    require(git(context,"rev-parse","HEAD")==BASELINE,"wrong original-context HEAD")
    require(git(context,"rev-parse","HEAD^{tree}")==TREE,"wrong original-context tree")
    for oid in spec["history_objects"]: require(git(context,"cat-file","-t",oid) in ("commit","tree","blob"),"missing historical object")
    require(not git(context,"status","--porcelain","--untracked-files=no"),"dirty tracked baseline")

def prepare(provider,session,bundle=None,git_repository=None):
    require(not session.out.is_relative_to(provider.root),"outputs must be outside normal checkout")
    context=session.out/"context"
    receipt=restore(provider,context,with_history=True,bundle=Path(bundle) if bundle else None,git_repository=git_repository)
    verify_workspace(provider,context)
    with (context/".git/info/exclude").open("a") as stream: stream.write("\n/.corpus-receipt.json\n")
    session.receipt["restoration"]=receipt;session.save()
    return context

def load_original(context,filename,name):
    require(filename.startswith("scripts/"),"original helper must be in locked scripts closure")
    for dependency in ("validate_research_continuations",):
        loaded=sys.modules.get(dependency)
        if loaded is not None:
            require(Path(getattr(loaded,"__file__","")).resolve()==(context/"scripts"/(dependency+".py")).resolve(),"foreign helper already loaded: "+dependency)
    sys.path.insert(0,str(context/"scripts"))
    try:
        spec=importlib.util.spec_from_file_location(name,context/filename)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module
    finally: sys.path.pop(0)

def graph_population(context):
    resolver=load_original(context,"scripts/resolve_t20_v6_source.py","_original_t20")
    graph=json.loads((context/"research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json").read_text())
    manifest=json.loads((context/"research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json").read_text())
    by_hash={r["source_sha256"]:r for r in manifest["objects"]}
    require(len(graph["nodes"])==233 and len(set(graph["ordinary_sources"]))==23,"current graph denominator changed")
    hashes=[row["source_sha256"] for row in graph["nodes"]]+graph["ordinary_sources"]
    for digest in hashes: resolver.source_bytes(context,by_hash[digest])
    return {"lean":233,"ordinary":23,"verified_bodies":len(hashes)}

def lean_environment(context,session,lean_bin,mathlib,modules):
    if not lean_bin or not mathlib: raise Blocked("exact Lean compiler and official dependency checkout required")
    helper=load_original(context,"scripts/replay_research_continuations.py","_original_continuation")
    desc=json.loads((context/"experiments/orthemology-v5-continuations/suites/c0c3081227ca-hidden-parity-pruning.json").read_text())
    desc["modules"]=[{"module":name} for name in modules]
    logs=session.out/"official-environment";logs.mkdir()
    saved_environment=dict(os.environ)
    try:
        os.environ.clear();os.environ.update(session.env)
        lean,libraries,version,checks=helper.environment(desc,Path(lean_bin),Path(mathlib),logs)
    finally:
        os.environ.clear();os.environ.update(saved_environment)
    session.receipt["official_environment"]={"compiler_version":version,"packages":checks};session.save()
    return helper,lean,libraries

def run_t20(context,case,spec,session,python,lean_bin,mathlib):
    session.receipt["graph"]=graph_population(context);target=session.out/"compiled"
    session.run([python,"-B",case["runner"]["path"],"export-suite",case["selection"],target],context)
    order=(target/"REPLAY_ORDER.txt").read_text().splitlines()
    require(len(order)==case["module_count"] and len(set(order))==len(order),"suite module denominator differs")
    require(not list(target.rglob("*.olean")),"custom objects existed before compilation")
    helper,lean,libraries=lean_environment(context,session,lean_bin,mathlib,order)
    env={"LEAN_PATH":os.pathsep.join(map(str,[target,*libraries]))}
    before={p.relative_to(target).as_posix():sha256(p.read_bytes()) for p in target.rglob("*.lean")}
    for module in order:
        safe_path(module.replace(".","/"))
        output=session.run([lean,"--trust=0","-j1","-o",module+".olean",module+".lean"],target,env=env)
        require(not re.search(r"\berror:|\bPANIC\b|\bsorryAx\b",output),"invalid compiler diagnostic")
        require((target/(module+".olean")).is_file(),"missing custom object")
    audit="\n".join("import "+module for module in order)+"\n"
    for name in case["readbacks"]:
        audit+='#eval IO.println "CONTINUATION_BEGIN '+name+'"\n#check @'+name+'\n#print axioms '+name+'\n#eval IO.println "CONTINUATION_END '+name+'"\n'
    (target/"ReplayReadback.lean").write_text(audit)
    output=session.run([lean,"--trust=0","-j1","ReplayReadback.lean"],target,env=env)
    readbacks=helper.parse_readback(output,case["readbacks"])
    for path,digest in before.items(): require(sha256((target/path).read_bytes())==digest,"compiled source changed")
    write_json(session.out/"READBACKS.json",readbacks)
    session.receipt["objects"]={p.relative_to(target).as_posix():sha256(p.read_bytes()) for p in target.rglob("*.olean")}
    session.receipt.update(status="FRESH_KERNEL_COMPONENTS",execution_credit=True)

def historical_native(context,case,session,python):
    session.run([python,"-B",case["runner"]["path"],"--check"],context,allowed=(0,1))
    revision=case["historical_revision"]
    require(git(context,"cat-file","-t",revision)=="commit","historical composition commit missing")
    entries=git(context,"ls-tree","-r","--name-only",BASELINE,"--","experiments/orthemology-v5/source","experiments/orthemology-v5/formal_project",case["runner"]["path"]).splitlines()
    require(entries,"empty native source closure")
    for path in entries:
        require(git(context,"rev-parse",BASELINE+":"+path)==git(context,"rev-parse",revision+":"+path),"historical native source differs: "+path)
    session.run(["git","checkout","--detach",revision],context)
    require(not git(context,"status","--porcelain","--untracked-files=no"),"dirty historical composition")
    session.receipt["native_edition"]={"revision":revision,"tree":git(context,"rev-parse","HEAD^{tree}"),"scope":"historical composition; current baseline defect remains"}
    return revision


def run_fable(context,case,spec,session,args):
    """Build the repaired formal slice through its original Lake target."""
    import shutil
    if not args.lean_bin or not args.mathlib:
        raise Blocked("Lean 4.32.2, Lake and exact official package checkout required")
    pins=spec["toolchains"]["lean-4.32.2"]
    compiler_hash=pins.get("compiler_sha256");lake_hash=pins.get("lake_sha256")
    if not compiler_hash or not lake_hash:
        raise Blocked("Fable compiler/Lake binary identities need a reviewed acquisition binding in the lock")
    lean=Path(args.lean_bin)/"lean";lake=Path(args.lean_bin)/"lake"
    if not lean.is_file() or not lake.is_file(): raise Blocked("Fable compiler or Lake unavailable")
    require(sha256(lean.read_bytes())==compiler_hash and sha256(lake.read_bytes())==lake_hash,"Fable executable identity differs")
    version=session.run([lean,"--version"],context,timeout=30)
    require(re.search(r"version 4\.32\.2[, ]",version),"wrong Fable compiler version")
    project=session.out/"fable-project"
    shutil.copytree(context/case["project"],project)
    require(not list(project.rglob("*.olean")) and not (project/".lake").exists(),"custom Fable cache existed before build")
    packages=project/".lake/packages";packages.mkdir(parents=True)
    official=[]
    for pin in pins["packages"]:
        repo=Path(args.mathlib) if pin["name"]=="mathlib" else Path(args.mathlib)/".lake/packages"/pin["name"]
        if not repo.is_dir(): raise Blocked("missing Fable package: "+pin["name"])
        require(git(repo,"rev-parse","HEAD")==pin["revision"],"wrong Fable package revision")
        require(not git(repo,"status","--porcelain","--untracked-files=no"),"dirty Fable package")
        require(not (repo/".lake/build/lib/lean/T299.olean").exists(),"custom Fable object in official cache")
        require(not (repo/".lake/build/lib/lean/T299").exists(),"custom Fable module subtree in official cache")
        (packages/pin["name"]).symlink_to(repo.resolve(),target_is_directory=True)
        official.append({"name":pin["name"],"revision":pin["revision"]})
    initial={p.relative_to(project).as_posix():sha256(p.read_bytes()) for p in project.rglob("*.lean") if ".lake" not in p.relative_to(project).parts}
    lock_hash=sha256((project/"lake-manifest.json").read_bytes())
    env={"PATH":str(Path(args.lean_bin).absolute())+os.pathsep+session.env["PATH"]}
    output=session.run([lake,"build","T299"],project,env=env)
    inventories=re.findall(r"^'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[[^\]]*\])\s*$",output,re.M)
    require(len(inventories)==case["axiom_inventory_count"],"incomplete Fable original axiom inventories")
    require(not re.search(r"\bsorryAx\b|\bPANIC\b|\berror:",output),"invalid Fable compiler diagnostic")
    for path,digest in initial.items(): require(sha256((project/path).read_bytes())==digest,"Fable source changed")
    require(sha256((project/"lake-manifest.json").read_bytes())==lock_hash,"Lake changed the reviewed package lock")
    audit="import T299\n"
    for name in case["readbacks"]:
        audit+='#eval IO.println "CONTINUATION_BEGIN '+name+'"\n#check @'+name+'\n#print axioms '+name+'\n#eval IO.println "CONTINUATION_END '+name+'"\n'
    (project/"ReplayReadback.lean").write_text(audit)
    output=session.run([lake,"env","lean","--trust=0","-j1","ReplayReadback.lean"],project,env=env)
    helper=load_original(context,"scripts/replay_research_continuations.py","_fable_readback_parser")
    write_json(session.out/"READBACKS.json",helper.parse_readback(output,case["readbacks"]))
    objects={p.relative_to(project).as_posix():sha256(p.read_bytes()) for p in (project/".lake/build").rglob("*.olean")}
    require(len(objects)>=3,"missing freshly compiled Fable objects")
    for row in official:
        repo=Path(args.mathlib) if row["name"]=="mathlib" else Path(args.mathlib)/".lake/packages"/row["name"]
        require(git(repo,"rev-parse","HEAD")==row["revision"] and not git(repo,"status","--porcelain","--untracked-files=no"),"official Fable source changed")
    session.receipt.update(status="FRESH_REPAIRED_FABLE_KERNEL_SLICE",execution_credit=True,objects=objects,official_packages=official)

def run_case(context,case,spec,session,args):
    py=str(Path(args.python).absolute())
    session.receipt.update(case=case["id"],scope=case["scope"])
    session.receipt["python"]=python_preflight(py,case.get("python"),case.get("python_sha256"),session.env)
    kind=case["kind"]
    if kind=="t20": run_t20(context,case,spec,session,py,args.lean_bin,args.mathlib)
    elif kind=="continuation-lean":
        if not args.lean_bin or not args.mathlib: raise Blocked("Lean 4.19.0 and exact official dependencies unavailable")
        session.run([py,"-B",case["runner"]["path"],"--suite",case["selection"],"--lean-bin",args.lean_bin,"--mathlib",args.mathlib,"--out",session.out/"results"],context)
        result=json.loads((session.out/"results/RECEIPT.json").read_text())
        require(result.get("status")=="FRESH_KERNEL_COMPONENTS" and result.get("kernel_verified") is True,"runner did not grant fresh component scope")
        session.receipt.update(status=result["status"],execution_credit=True)
    elif kind in ("successor-python","finite-controls"):
        command=[py,"-B",case["runner"]["path"]]
        if kind=="successor-python": command+=["--execute","--python",py]
        command+=["--suite",case["selection"],"--out",str(session.out/"results")]
        session.run(command,context);result=json.loads((session.out/"results/RECEIPT.json").read_text())
        if kind=="finite-controls":
            require(result.get("status")=="PASS_NATIVE_CONTROLS" and len(result.get("steps",[]))==21,"incomplete finite control receipt")
            require(all(x["exit_code"]==0 for x in result["steps"]),"failed finite control")
        else:
            require(result.get("outcome")=="FINITE_ONLY" and result.get("proof_scope")=="FINITE" and result.get("exit_code")==0,"wrong successor runtime scope")
        session.receipt.update(status=result.get("status",result.get("outcome")),execution_credit=True)
    elif kind=="native":
        if not args.historical_native:
            session.run([py,"-B",case["runner"]["path"],"--check"],context)
            raise Blocked("current native composition needs reviewed binding before execution")
        historical_native(context,case,session,py)
        if not args.lean_bin: raise Blocked("exact native Lean 4.19.0 toolchain required before full reference/kernel run")
        lean=Path(args.lean_bin)/"lean";lake=Path(args.lean_bin)/"lake"
        if not lean.is_file() or not lake.is_file(): raise Blocked("native Lean/Lake installation incomplete")
        require(sha256(lean.read_bytes())==spec["toolchains"]["lean-4.19.0"]["lean_binary_sha256"],"native compiler identity differs")
        session.receipt["native_toolchain"]={"lean_sha256":sha256(lean.read_bytes()),"lake_sha256":sha256(lake.read_bytes())}
        session.env["PATH"]=str(Path(args.lean_bin).absolute())+os.pathsep+session.env["PATH"]
        if args.mathlib: session.env["MATHLIB_CACHE_DIR"]=str(Path(args.mathlib).parent/"mathlib-cache")
        session.run([py,"-B",case["runner"]["path"],"--output",session.out/"results"],context,allowed=(0,2))
        result=json.loads((session.out/"results/VERIFICATION.json").read_text())
        session.receipt["original_native_receipt"]=result
        if result.get("overall")!="NATIVE_REFERENCE_AND_KERNEL_PASS": raise Blocked("required native kernel remains open")
        session.receipt.update(status=result["overall"],execution_credit=True)
    elif kind=="publication":
        from publication import build
        build(context,case,session,py)
    elif kind=="fable":
        run_fable(context,case,spec,session,args)
    else: raise ValueError("unmapped case")

def snapshot(context):
    result={}
    for base,dirs,files in os.walk(context):
        if Path(base)==Path(context) and ".git" in dirs: dirs.remove(".git")
        for name in dirs+files: require(not (Path(base)/name).is_symlink(),"unapproved generated symlink")
        for name in files:
            p=Path(base)/name;rel=p.relative_to(context).as_posix()
            if rel==".corpus-receipt.json": continue
            result[rel]={"sha256":sha256(p.read_bytes()),"mode":oct(p.stat().st_mode&0o777)}
    return result

def run_ci(context,spec,session,python,selection,keep_going=False):
    session.receipt["python"]=python_preflight(python,"3.11.9",env=session.env)
    steps=spec["workflow"]["steps"];chosen=steps if selection=="all" else [x for x in steps if x["id"]==selection]
    require(chosen,"unknown CI step")
    # Verify the bare python used in unchanged original shell commands is exact.
    resolved=session.run(["/bin/bash","--noprofile","--norc","-c","command -v python"],context).strip()
    require(Path(resolved).resolve()==Path(python).resolve(),"CI PATH selects a different Python")
    path_file=ci_environment(session);failures=[]
    for step in chosen:
        try:
            session.run(["/bin/bash","--noprofile","--norc","-e","-o","pipefail","-c",step["command"]],context)
        except (ProcessFailure,TimeoutError) as exc:
            failures.append({"id":step["id"],"error":str(exc)})
            if not keep_going: raise
        finally:
            apply_ci_paths(session,path_file)
    session.receipt["ci_failures"]=failures
    if failures: raise ProcessFailure(str(len(failures))+" original CI obligations failed; all recorded failures remain blocking")
    session.receipt.update(status="ORIGINAL_CI_COMMANDS_PASS",ci_obligations=[x["id"] for x in chosen],execution_credit=False)

def convergence(context,spec,session,python,selection):
    generators=[x for x in spec["generators"] if x["path"]==selection]
    require(len(generators)==1,"unknown generator");row=generators[0]
    require(sha256((context/row["path"]).read_bytes())==row["sha256"],"generator identity differs")
    before=snapshot(context);previous=None
    for index in range(2):
        session.run([python,"-B",row["path"]],context);current=snapshot(context)
        write_json(session.out/("generation-%d.json"%(index+1)),current)
        if previous is not None: require(previous==current,"generator does not converge")
        previous=current
    require(before==previous,"convergent output differs from reviewed baseline; new edition requires review")
    session.receipt.update(status="GENERATOR_CONVERGENCE_PASS",execution_credit=False)


OFFICIAL_RELEASES={
 "4.19.0":{"file":"lean-4.19.0-linux.tar.zst","bytes":343842845,"sha256":"6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe","lean_sha256":"92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023","lake_sha256":"5111aee5c9434ab05d4265606475ef22e8bda69aaf3a0657b61a7eec6e550bed"},
 "4.32.2":{"file":"lean-4.32.2-linux.tar.zst","bytes":563991635,"sha256":"5f2069e6f5db73780f374ccb49ce8ea649aa20a0cebf0116816744c999ce72aa","lean_sha256":"e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550","lake_sha256":"60330ab6f07dce20f3fa9ebb08e8b984ea9549eac172afeb15d9d2227060e2b3"}}

def download_exact(url,path,identity):
    import urllib.request,urllib.error,hashlib
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    require(not path.exists(),"download destination must be fresh")
    digest=hashlib.sha256();count=0
    try:
        with urllib.request.urlopen(url,timeout=120) as response,path.open("xb") as target:
            while True:
                raw=response.read(1024*1024)
                if not raw:break
                count+=len(raw);require(count<=identity["bytes"],"download exceeds bound")
                digest.update(raw);target.write(raw)
        require(count==identity["bytes"] and digest.hexdigest()==identity["sha256"],"download identity differs")
    except urllib.error.URLError as exc:
        path.unlink(missing_ok=True);raise Blocked("official environment download unavailable: "+url+"; "+str(exc)) from exc
    except BaseException:
        path.unlink(missing_ok=True);raise
    return {"url":url,"bytes":count,"sha256":digest.hexdigest()}

def extract_official_release(archive,destination):
    """Only verified regular/directory/internal-link release members are admitted."""
    import tarfile,posixpath
    dest=Path(destination);require(not dest.exists(),"runtime extraction must be fresh");dest.mkdir()
    process=subprocess.Popen(["zstd","-d","-c",str(archive)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    seen=set()
    try:
        with tarfile.open(fileobj=process.stdout,mode="r|") as source:
            for member in source:
                name=member.name.rstrip("/");safe_path(name)
                require(name not in seen,"duplicate release member");seen.add(name)
                require(member.isfile() or member.isdir() or member.issym() or member.islnk(),"unsupported release member")
                if member.issym() or member.islnk():
                    require(not member.linkname.startswith("/"),"absolute release link")
                    linked=posixpath.normpath(posixpath.join(posixpath.dirname(name),member.linkname)) if member.issym() else posixpath.normpath(member.linkname)
                    safe_path(linked);require(linked.split("/")[0]==name.split("/")[0],"release link escapes runtime")
                source.extract(member,path=dest,set_attrs=True)
        require(process.wait(timeout=30)==0,"release decompression failed")
    finally:
        if process.poll() is None: process.kill();process.wait()
        if process.stdout: process.stdout.close()
        if process.stderr: process.stderr.close()

def ci_environment(session):
    """Emulate the public environment-file contract of original GitHub steps."""
    path=session.out/"GITHUB_PATH";path.touch()
    session.env.update(GITHUB_ACTIONS="true",GITHUB_PATH=str(path))
    return path

def apply_ci_paths(session,path):
    additions=[line for line in path.read_text().splitlines() if line]
    for item in additions:
        location=Path(item)
        require(location.is_absolute() and location.is_dir(),"invalid CI PATH entry")
        require(location.resolve().is_relative_to(session.out.resolve()),"CI provisioned PATH escapes isolated session")
    if additions: session.env["PATH"]=os.pathsep.join(reversed(additions))+os.pathsep+session.env["PATH"]
    path.write_text("")

def provision(provider,spec,case,session,python):
    """Explicit network acquisition into a fresh external directory; no home install."""
    import shutil
    session.env.update(XDG_CACHE_HOME=str(session.out/"cache"),ELAN_HOME=str(session.out/"elan"),
                       LAKE_HOME=str(session.out/"lake-home"),MATHLIB_CACHE_DIR=str(session.out/"mathlib-cache"))
    result={"case":case["id"],"REPLAY_PYTHON":str(Path(python).absolute()),"LEAN_BIN":"","MATHLIB_DIR":"",
            "scope":"acquired exact public environment; no scientific execution credit"}
    if case["kind"]=="successor-python":
        config=spec["toolchains"]["python-3.12.3"]
        root=session.out/"python";root.mkdir()
        downloads=[]
        session.receipt["requested_python_packages"]=config["packages"];session.save()
        for row in config["packages"]:
            package=session.out/"downloads"/row["file"]
            downloads.append(download_exact(row["url"],package,row))
            session.run(["dpkg-deb","-x",package,root],session.out,timeout=60)
        executable=root/config["executable"]
        result["REPLAY_PYTHON"]=str(executable)
        result["python"]=python_preflight(executable,"3.12.3",case["python_sha256"],session.env)
        result["packages"]=downloads
        result["shared_library_scope"]=config["shared_library_scope"]
        session.run([executable,"-E","-B","-c","import json,sys,sysconfig,unittest; print(json.dumps({'prefix':sys.prefix,'paths':sys.path,'platform':sysconfig.get_platform()}))"],session.out)
    elif case.get("lean"):
        version=case["lean"];release=OFFICIAL_RELEASES[version]
        archive=session.out/"downloads"/release["file"]
        url="https://github.com/leanprover/lean4/releases/download/v"+version+"/"+release["file"]
        session.receipt["requested_release"]={"url":url,**release};session.save()
        result["release"]=download_exact(url,archive,release)
        extract_official_release(archive,session.out/"runtime");archive.unlink()
        binary=session.out/"runtime"/("lean-"+version+"-linux")/"bin"
        require(sha256((binary/"lean").read_bytes())==release["lean_sha256"],"official compiler member differs")
        require(sha256((binary/"lake").read_bytes())==release["lake_sha256"],"official Lake member differs")
        session.env["PATH"]=str(binary)+os.pathsep+session.env["PATH"]
        session.run([binary/"lean","--version"],session.out,timeout=30)
        result["LEAN_BIN"]=str(binary)
        lock_path=("experiments/orthemology-v5/formal_project/lake-manifest.json" if version=="4.19.0" else
                   "docs/project-closure/ar8r-v11/fable-research/lean/lake-manifest.json")
        package_lock=json.loads(provider.read_bytes(lock_path))
        wanted={p["name"]:p["revision"] for p in spec["toolchains"]["lean-"+version]["packages"]}
        require({p["name"]:p["rev"] for p in package_lock["packages"]}==wanted,"official dependency pins differ")
        mathlib=session.out/"mathlib"
        ordered=sorted(package_lock["packages"],key=lambda row:row["name"]!="mathlib")
        for row in ordered:
            repo=mathlib if row["name"]=="mathlib" else mathlib/".lake/packages"/row["name"]
            repo.mkdir(parents=True)
            require(row["url"].startswith("https://github.com/"),"unexpected official dependency origin")
            session.run(["git","init","--quiet",repo],session.out)
            session.run(["git","-C",repo,"remote","add","origin",row["url"]],session.out)
            session.run(["git","-C",repo,"fetch","--depth","1","origin",row["rev"]],session.out,timeout=300)
            session.run(["git","-C",repo,"checkout","--quiet","--detach","FETCH_HEAD"],session.out)
            require(git(repo,"rev-parse","HEAD")==row["rev"],"wrong acquired dependency")
        result["MATHLIB_DIR"]=str(mathlib)
        session.run([binary/"lake","exe","cache","get"],mathlib,timeout=3600)
        modules=set()
        graph=json.loads(provider.read_bytes("research/t20-v6-20261012/CURRENT_SOURCE_GRAPH.json"))
        for row in graph["suites"]:modules.update(row["modules"])
        desc=json.loads(provider.read_bytes("experiments/orthemology-v5-continuations/suites/c0c3081227ca-hidden-parity-pruning.json"))
        modules.update(row["module"] for row in desc["modules"])
        native=json.loads(provider.read_bytes("experiments/orthemology-v5/source/formal_targets.json"))
        modules.update(row["name"] for row in native["modules"]);modules.update(["T299","T299.Basic","T299.Receipts"])
        for row in ordered:
            repo=mathlib if row["name"]=="mathlib" else mathlib/".lake/packages"/row["name"]
            require(git(repo,"rev-parse","HEAD")==row["rev"] and not git(repo,"status","--porcelain","--untracked-files=no"),"official dependency source changed")
            for name in modules:
                require(not (repo/".lake/build/lib/lean"/(name.replace(".","/")+".olean")).exists(),"custom module in official dependency cache")
        result["packages"]=[{"name":row["name"],"revision":row["rev"]} for row in ordered]
        result["compiler_sha256"]=release["lean_sha256"];result["lake_sha256"]=release["lake_sha256"]
    else:
        result["python"]=python_preflight(python,case.get("python"),env=session.env)
    write_json(session.out/"ENV.json",result)
    session.receipt.update(status="EXACT_ENVIRONMENT_PROVISIONED",environment=result,execution_credit=False)
    session.save()
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache",type=Path,required=True);parser.add_argument("--bundle",type=Path);parser.add_argument("--history-from-git",type=Path)
    parser.add_argument("--python",default=sys.executable);parser.add_argument("--lean-bin",type=Path);parser.add_argument("--mathlib",type=Path)
    parser.add_argument("--offline",action="store_true");parser.add_argument("--no-git-source",action="store_true")
    parser.add_argument("--historical-native",action="store_true");parser.add_argument("--keep-going",action="store_true");parser.add_argument("--timeout",type=int,default=1800)
    parser.add_argument("--out",type=Path);parser.add_argument("command",choices=["list","integrity","case","export","ci","converge","provision"]);parser.add_argument("selection",nargs="?")
    args=parser.parse_args(argv)
    provider=SourceProvider(args.root,args.cache,offline=args.offline,git_repo=False if args.no_git_source else None)
    spec=load_spec(provider)
    if args.command=="list":
        print(json.dumps({"cases":[x["id"] for x in spec["cases"]],"ci":[x["id"] for x in spec["workflow"]["steps"]],"integrity":list(spec["integrity_routes"]),"generators":[x["path"] for x in spec["generators"]]},indent=2));return 0
    require(args.out is not None,"fresh --out required")
    require(args.command=="provision" or bool(args.bundle)!=bool(args.history_from_git),"one explicit --bundle or --history-from-git required")
    require(not args.out.absolute().is_relative_to(provider.root),"output must be external")
    session=Session(args.out,args.python,args.timeout)
    context=None
    try:
        if args.command=="provision":
            cases=[x for x in spec["cases"] if x["id"]==args.selection]
            require(len(cases)==1,"unknown provision profile")
            provision(provider,spec,cases[0],session,args.python);return 0
        context=prepare(provider,session,args.bundle,args.history_from_git);assert_history(context,spec)
        session.receipt["invocation"]={"command":args.command,"selection":args.selection,"provider_sources":sorted(set(provider.sources_used.values()))}
        if args.command=="integrity":
            require(args.selection in spec["integrity_routes"],"unknown integrity route")
            session.run([args.python,"-B",*spec["integrity_routes"][args.selection]],context)
            if args.selection=="public-source-projection": session.receipt["graph"]=graph_population(context)
            session.receipt["status"]="ORIGINAL_SOURCE_INTEGRITY_PASS"
        elif args.command=="export":
            cases=[x for x in spec["cases"] if x["id"]==args.selection and x["kind"]=="t20"]
            require(len(cases)==1,"unknown export profile");case=cases[0]
            session.receipt["graph"]=graph_population(context)
            session.run([args.python,"-B",case["runner"]["path"],"export-suite",case["selection"],session.out/"exported"],context)
            session.receipt.update(status="EXACT_SOURCES_EXPORTED",executed=False,execution_credit=False)
        elif args.command=="case":
            cases=[x for x in spec["cases"] if x["id"]==args.selection]
            require(len(cases)==1,"unknown fixed replay case");run_case(context,cases[0],spec,session,args)
        elif args.command=="ci": run_ci(context,spec,session,args.python,args.selection,args.keep_going)
        else: convergence(context,spec,session,args.python,args.selection)
        if not session.receipt.get("native_edition"): session.receipt["post_source_verification"]=verify_workspace(provider,context)
        session.save();return 0
    except (Blocked,FileNotFoundError) as exc:
        session.receipt.update(status="BLOCKED",error=str(exc),execution_credit=False);session.save();return 2
    except TimeoutError as exc:
        session.receipt.update(status="RESOURCE_INCONCLUSIVE",error=str(exc),execution_credit=False);session.save();return 1
    except (ValueError,OSError,SourceError,ProcessFailure,subprocess.SubprocessError) as exc:
        session.receipt.update(status="FAILED",error=str(exc),execution_credit=False);session.save();return 1

    finally:
        if context is not None:
            try:
                if session.receipt.get("native_edition"):
                    require(not git(context,"status","--porcelain","--untracked-files=no"),"historical source changed during execution")
                    session.receipt["post_source_verification"]={"revision":git(context,"rev-parse","HEAD"),"tree":git(context,"rev-parse","HEAD^{tree}"),"tracked_clean":True}
                else:
                    session.receipt["post_source_verification"]=verify_workspace(provider,context)
                session.save()
            except (ValueError,OSError,SourceError,subprocess.SubprocessError) as exc:
                session.receipt.update(status="FAILED",source_integrity_error=str(exc),execution_credit=False)
                session.save()
                return 1

if __name__=="__main__": raise SystemExit(main())
