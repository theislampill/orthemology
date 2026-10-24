#!/usr/bin/env python3
"""Read, search and recover Orthemology by substantive work names.

Reading and source restoration do not execute research code. Replay is a separate
explicit operation with its own source, environment and scope checks.
"""
from __future__ import annotations
import argparse
import difflib
import json
from pathlib import Path
import sys
from source_provider import SourceError, SourceProvider, atomic_bytes
from search import (load_works, find_work, metadata_search, fulltext_search,
                    verify_work, work_edition, check_binding)
from rehydrate import materialise, restore, verify_workspace

def _print_json(value):
    print(json.dumps(value,ensure_ascii=False,indent=2))

def _selected(edition,role,include_status=False):
    sources=edition["sources"]
    roles={role}
    if role=="all":
        roles={s["role"] for s in sources}
    elif include_status:
        roles.update(("review","status"))
    selected=[s for s in sources if s["role"] in roles]
    if not selected:
        raise SourceError("UNAVAILABLE",f"no source with role {role} for exact edition {edition['version']}")
    return selected

def show(provider,name,version=None,role="primary",include_status=False,output=None):
    edition=work_edition(provider,name,version)
    sources=_selected(edition,role,include_status)
    bodies=[(s,provider.read_bytes(s["path"],s.get("version"))) for s in sources]
    scientific_reviews=[s for s in sources if s["role"]=="review" and s.get("review_kind")!="historical_source_fidelity"]
    historical_reviews=[s for s in sources if s.get("review_kind")=="historical_source_fidelity"]
    status={"scientific_review_binding_identified":bool(scientific_reviews),"historical_fidelity_reviews":len(historical_reviews),"work":edition["work"]["id"],"version":edition["version"],"sources":sources,
            "source_owned_status":edition["status"],"scope":edition["scope"],
            "predecessor":edition["predecessor"],"execution_credit":False}
    if output:
        dest=Path(output)
        if dest.exists():
            raise SourceError("EXISTS",str(dest))
        dest.mkdir(parents=True)
        for number,(source,data) in enumerate(bodies,1):
            atomic_bytes(dest/f"{number:02d}-{source['role']}{Path(source['path']).suffix}",data)
        atomic_bytes(dest/"sources.json",json.dumps(status,ensure_ascii=False,indent=2).encode())
        print(f"Complete reading saved to {dest}: {len(bodies)} exact source bodies.")
        return
    # Decode all selected forms before printing a complete textual reading.
    rendered=[]
    for source,data in bodies:
        try:text=data.decode("utf-8-sig")
        except UnicodeError as exc:
            raise SourceError("BINARY_SOURCE","use --output NEW_DIRECTORY for complete binary reading forms") from exc
        if "\0" in text:
            raise SourceError("BINARY_SOURCE","use --output NEW_DIRECTORY for binary reading forms")
        rendered.append((source,text))
    print("# "+edition["work"]["title"])
    print("\nExact edition: "+edition["version"])
    if include_status:
        label="Source-owned catalogue status" if edition["kind"]=="baseline" else "Source-owned edition status"
        print("\n"+label+": "+json.dumps(edition["status"],ensure_ascii=False))
        print(edition["scope"])
        if edition["predecessor"]:
            print("This is the preserved predecessor. The current edition's review is not applied to it.")
        if not scientific_reviews:
            print("Controlling scientific review: NOT IDENTIFIED by this work binding; do not infer scientific acceptance.")
        else:
            print("Scientific review binding identified; inspect its exact target, premises, and scope before drawing conclusions.")
        if historical_reviews:
            print("Historical source-fidelity review is separate. It does not establish controlling scientific review or current adoption.")
    for source,text in rendered:
        if source.get("review_kind")=="historical_source_fidelity":
            heading="Historical source-fidelity review"
        elif source["role"]=="review" and edition["kind"] in ("current","preserved_current"):
            heading="Source-owned review/adoption decision"
        else:
            heading=source["role"].replace("-"," ").title()
        print("\n## "+heading)
        print("Source edition: "+source.get("version",provider.baseline["commit"]))
        print(text,end="" if text.endswith("\n") else "\n")
    print("\nReading scope: exact indexed source bodies; no research code executed.")

def fetch_named(provider,name,version=None):
    """Cache complete verified reading and exact source-owner dependency reads."""
    reads={}
    original=provider.read_bytes
    def tracked(path,context=None):
        data=original(path,context)
        row=provider.resolve(path,context)
        edition=context or provider.baseline["commit"]
        identity={k:row[k] for k in ("path","sha256","git_blob","bytes","mode")}
        identity["version"]=edition
        reads[(path,edition)]=(identity,data)
        return data
    provider.read_bytes=tracked
    try:
        edition=work_edition(provider,name,version)
        for source in edition["sources"]:
            check_binding(provider,source)
            provider.read_bytes(source["path"],source.get("version"))
        # verify_work/authority helpers read exact owners, appointments,
        # review evidence and predecessor dependencies through tracked().
    finally:
        provider.read_bytes=original
    for identity,data in reads.values():
        atomic_bytes(provider.cache/"objects"/identity["sha256"],data)
    return {"work":edition["work"]["id"],"version":edition["version"],"source_occurrences":len(reads),
            "distinct_byte_objects":len({identity["sha256"] for identity,_ in reads.values()}),
            "logical_bytes":sum(identity["bytes"] for identity,_ in reads.values()),
            "network_bytes":provider.network_bytes,
            "sources":[identity for identity,_ in reads.values()],
            "scope":"exact named reading plus source-owner verification dependencies; no execution or scientific adoption"}

def _replay_parse(argv):
    """Keep replay child arguments in their original order, including options."""
    argv=list(argv)
    i=0
    while i<len(argv):
        value=argv[i]
        if value in ("--root","--cache"):
            i+=2
        elif value.startswith("--root=") or value.startswith("--cache=") or value in ("--offline","--no-git-source"):
            i+=1
        else:
            break
    if i<len(argv) and argv[i]=="replay":
        tail=argv[i+1:]
        if tail[:1]==["--"]:tail=tail[1:]
        return argv[:i+1],tail
    return argv,None

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache",type=Path,help="explicit source cache outside ordinary checkout")
    parser.add_argument("--offline",action="store_true")
    parser.add_argument("--no-git-source",action="store_true",help="deny even pinned local Git object fallback")
    sub=parser.add_subparsers(dest="command",required=True)
    listing=sub.add_parser("list",help="substantive work names and exact selected editions")
    listing.add_argument("--subject")
    searching=sub.add_parser("search",help="metadata or explicit full-text source search")
    searching.add_argument("query");searching.add_argument("--subject")
    searching.add_argument("--full-text",action="store_true");searching.add_argument("--all-versions",action="store_true")
    searching.add_argument("--work");searching.add_argument("--version")
    reading=sub.add_parser("show",help="complete primary text and source-owned review/status")
    reading.add_argument("--work",required=True);reading.add_argument("--version")
    reading.add_argument("--role",choices=("primary","review","status","all"),default="primary")
    reading.add_argument("--include-status",action="store_true");reading.add_argument("--output",type=Path)
    compare=sub.add_parser("compare",help="compare explicitly indexed editions, never nearest versions")
    compare.add_argument("--work",required=True);compare.add_argument("--from",dest="old",required=True)
    compare.add_argument("--to",dest="new",required=True)
    resolving=sub.add_parser("resolve",help="exact historical path/context compatibility")
    resolving.add_argument("--legacy-path",required=True);resolving.add_argument("--context",required=True)
    fetching=sub.add_parser("fetch",help="cache an exact named reading and owner dependencies for offline access")
    choice=fetching.add_mutually_exclusive_group(required=True)
    choice.add_argument("--work");choice.add_argument("--all",action="store_true")
    fetching.add_argument("--version")
    mat=sub.add_parser("materialise",help="create an exact baseline source editing/replay workspace")
    mat.add_argument("--profile",required=True);mat.add_argument("--version");mat.add_argument("--dest",type=Path,required=True)
    recovery=sub.add_parser("restore",help="restore every original source occurrence")
    recovery.add_argument("--baseline");recovery.add_argument("--dest",type=Path,required=True)
    recovery.add_argument("--with-history",action="store_true");recovery.add_argument("--bundle",type=Path)
    recovery.add_argument("--history-from-git",type=Path)
    verify=sub.add_parser("verify",help="reread all restored bytes/modes/tree; a receipt alone is insufficient")
    verify.add_argument("--workspace",type=Path,required=True);verify.add_argument("--exact-tree")
    replay=sub.add_parser("replay",help="explicit scientific replay with inherited root/cache/offline options")
    replay.add_argument("args",nargs=argparse.REMAINDER)
    parse_args,replay_tail=_replay_parse(sys.argv[1:] if argv is None else argv)
    args=parser.parse_args(parse_args)
    try:
        provider=SourceProvider(args.root,args.cache,args.offline,git_repo=False if args.no_git_source else None)
        if args.command in ("list","search"):
            if args.command=="search" and args.full_text:
                result=fulltext_search(provider,args.query,args.all_versions,args.work,args.version)
                for match in result["matches"]:
                    print(f"{match['path']}@{match['version']}:{match['line']}: {match['text']}")
                print(f"Coverage: selected={result['selected']} searched={result['searched']} binary={result['binary']} unavailable={len(result['unavailable'])}")
                print(result["scope"])
                for missing in result["unavailable"]:
                    print(f"{missing['state']}: {missing['path']}@{missing['version']}",file=sys.stderr)
                return 0 if result["complete"] else 3
            if args.command=="search" and (args.version or args.all_versions or args.work):
                raise SourceError("SEARCH_MODE","--version, --work and --all-versions require --full-text")
            rows=metadata_search(provider,getattr(args,"query",""),args.subject)
            for row in rows:
                print(row["title"]+"\n  "+row["id"]+" @ "+row.get("version",provider.baseline["commit"]))
            print(f"{len(rows)} named work editions.")
        elif args.command=="show":
            show(provider,args.work,args.version,args.role,args.include_status,args.output)
        elif args.command=="compare":
            def edition(version):
                selected=work_edition(provider,args.work,version)
                return "\n".join(provider.read_bytes(s["path"],s.get("version")).decode("utf-8") for s in _selected(selected,"primary"))
            print("".join(difflib.unified_diff(edition(args.old).splitlines(True),edition(args.new).splitlines(True),fromfile=args.old,tofile=args.new)),end="")
        elif args.command=="resolve":
            _print_json(provider.resolve_legacy(args.legacy_path,args.context))
        elif args.command=="fetch":
            if args.all:
                if args.version and args.version!=provider.baseline["commit"]:
                    raise SourceError("AMBIGUOUS_VERSION","--all fetches the indexed original baseline; use --work --version for current editions")
                _print_json({**provider.fetch(),"scope":"all exact baseline occurrences; current editions require named fetch"})
            else:
                _print_json(fetch_named(provider,args.work,args.version))
        elif args.command=="materialise":
            if args.profile=="baseline":
                if args.version and args.version!=provider.baseline["commit"]:
                    raise SourceError("AMBIGUOUS_VERSION","unindexed baseline workspace edition")
                _print_json(restore(provider,args.dest))
            else:
                selected=work_edition(provider,args.profile,args.version)
                if selected["version"]!=provider.baseline["commit"] or any(s.get("version",provider.baseline["commit"])!=provider.baseline["commit"] for s in selected["sources"]):
                    raise SourceError("CURRENT_MATERIALISATION_UNSUPPORTED","current work requires version-aware workspace restoration; no baseline workspace was created")
                _print_json(materialise(provider,{s["path"] for s in selected["sources"]},args.dest))
        elif args.command=="restore":
            if args.baseline and args.baseline!=provider.baseline["commit"]:
                raise SourceError("AMBIGUOUS_VERSION","unindexed restoration baseline")
            _print_json(restore(provider,args.dest,args.with_history,args.bundle,args.history_from_git))
        elif args.command=="verify":
            result=verify_workspace(provider,args.workspace)
            if args.exact_tree and args.exact_tree!=result["tree"]:
                raise SourceError("CORRUPT","explicit tree expectation differs")
            _print_json(result)
        elif args.command=="replay":
            from replay import main as replay_main
            forwarded=["--root",str(args.root),"--cache",str(provider.cache)]
            if args.offline:forwarded.append("--offline")
            if args.no_git_source:forwarded.append("--no-git-source")
            return replay_main(forwarded+(replay_tail if replay_tail is not None else args.args))
        return 0
    except (SourceError,OSError,ValueError) as exc:
        print(str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
