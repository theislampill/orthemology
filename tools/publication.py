"""Bounded all-six publication route with unchanged reviewed-source provenance."""
from pathlib import Path, PurePosixPath
import io, json, shutil, tarfile
from source_provider import sha256, safe_path

def package_members(context, artifact="orthemma-ortheme-systems-draft"):
    """Verify the complete four-member source package without extracting it."""
    from replay import require
    root=Path(context);base=root/"artifacts"
    manifest=json.loads((base/(artifact+".source-manifest.json")).read_text())
    require(manifest["source_commit"]=="1db15916a3965ccbba101969341bad4cb44ba22b","wrong reviewed publication commit")
    require(manifest["source_tree"]=="7c7a22d83b9dd86702978bae00c1e3f15d826195","wrong reviewed publication tree")
    archive=(base/(artifact+".source.tar.gz")).read_bytes()
    require(sha256(archive)==manifest["archive"]["sha256"],"publication archive digest differs")
    expected={r["path"]:r for r in manifest["members"]}
    require(len(expected)==len(manifest["members"])==4,"incomplete or duplicate source package")
    require(manifest["entry_point"] in expected,"entry point missing")
    require(str(PurePosixPath(manifest["entry_point"]).parent)==manifest["build_workdir"],"build directory differs")
    found={}
    with tarfile.open(fileobj=io.BytesIO(archive),mode="r:gz") as tar:
        for member in tar:
            safe_path(member.name)
            require(member.isfile() and member.name in expected and member.name not in found,"unsafe/extra/duplicate package member")
            row=expected[member.name]
            require(member.size==row["bytes"] and member.mode==int(row["mode"],8),"source package size/mode differs")
            raw=tar.extractfile(member).read(row["bytes"]+1)
            require(len(raw)==row["bytes"] and sha256(raw)==row["sha256"],"source package body differs")
            found[member.name]=row
    require(set(found)==set(expected),"missing complete source-package member")
    return {"artifact":artifact,"archive_sha256":sha256(archive),"members":list(found.values()),
            "source_commit":manifest["source_commit"],"source_tree":manifest["source_tree"],
            "scope":"source-package integrity only; no PDF rebuild credit"}

def build(context,case,session,python):
    from replay import Blocked, require, git, ci_environment, apply_ci_paths
    session.receipt["source_package"]=package_members(context,case["selection"]);session.save()
    require(git(context,"rev-parse",case["source_commit"]+"^{tree}")==case["source_tree"],
            "reviewed historical tree missing or different")
    if shutil.which("docker",path=session.env["PATH"]) is None:
        raise Blocked("locked TeX Live container requires Docker; host latexmk/pdflatex cannot substitute")
    path_file=ci_environment(session)
    session.run([python,"-B","scripts/provision_ci_infrastructure.py"],context)
    apply_ci_paths(session,path_file)
    session.run([python,"-m","pip","install","--quiet","-r","requirements-ci.lock.txt"],context)
    # Original script enforces image/config/tools, two builds, source package,
    # bibliography, PDF byte equality, text structure and committed sidecars.
    session.run([python,"-B",case["runner"]["path"],"--check","--source-commit",case["source_commit"]],context)
    session.run([python,"-B","scripts/validate_arxiv_source_package.py"],context)
    render=session.out/"render-review"
    session.run([python,"-B",case["runner"]["path"],"--render-committed",case["selection"],"--output-dir",render],context)
    pages=sorted(render.glob("page-*.png"))
    require(bool(pages),"rendered manuscript pages absent")
    from replay import write_json
    write_json(session.out/"RENDER_MANIFEST.json",{"artifact":case["selection"],"pdf_sha256":sha256((Path(context)/"artifacts"/(case["selection"]+".pdf")).read_bytes()),"pages":[{"file":p.name,"bytes":p.stat().st_size,"sha256":sha256(p.read_bytes())} for p in pages],"scope":"Rasterized committed PDF after exact all-six rebuilt-byte equality; scholarly render review remains separate"})
    session.receipt["render_review"]="AWAITING_SCHOLARLY_REVIEW"
    session.receipt.update(status="ALL_SIX_GOVERNED_PUBLICATIONS_PASS",execution_credit=True,
                           hosted_publication=False)
