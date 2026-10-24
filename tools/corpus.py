#!/usr/bin/env python3
"""Read, search and recover Orthemology by substantive work names.

Reading and source restoration do not execute research code. Replay is a separate
explicit operation with its own source, environment and scope checks.
"""
from __future__ import annotations
import argparse
import difflib
import json
import os
import stat
import time
from pathlib import Path
import sys
from source_provider import SourceError, SourceProvider, atomic_bytes, sha256, load_json, _reject_links
from search import (load_works, find_work, metadata_search, fulltext_search,
                    verify_work, work_edition, check_binding, scholarly_sources, source_edition)
from rehydrate import materialise, restore, verify_workspace

def _print_json(value):
    print(json.dumps(value,ensure_ascii=False,indent=2))

def _selected(edition,role,include_status=False):
    sources=edition["sources"]
    if role=="all":selected=sources
    elif role=="status":selected=[s for s in sources if s["role"]=="status"]
    elif role=="historical":
        selected=[s for s in sources if s.get("review_kind")=="historical_source_fidelity"]
    else:
        sources=scholarly_sources(sources)
        roles={role}
        if role=="reading":roles={s["role"] for s in sources}
        elif include_status:roles.update(("support","review","status","currentness"))
        selected=[s for s in sources if s["role"] in roles]
    if not selected and role!="status":
        raise SourceError("UNAVAILABLE",f"no source with role {role} for exact edition {edition['version']}")
    return selected

def show(provider,name,version=None,role="primary",include_status=False,output=None,source_path=None):
    edition=source_edition(provider,source_path,version) if source_path else work_edition(provider,name,version)
    include_status=include_status or role=="status"
    sources=_selected(edition,role,include_status)
    unavailable=[s for s in sources if "path" not in s]
    if any(s["role"]=="primary" for s in unavailable):
        raise SourceError("IDENTITY_ONLY","exact canonical body unavailable; public summary is not its original: "+unavailable[0].get("original_sha256",""))
    bodies=[(s,provider.read_bytes(s["path"],s.get("version"))) for s in sources if "path" in s]
    scientific_reviews=[s for s in sources if s["role"]=="review" and s.get("review_kind")!="historical_source_fidelity"]
    historical_reviews=[s for s in edition["sources"] if s.get("review_kind")=="historical_source_fidelity"]
    status={"scientific_review_binding_identified":bool(scientific_reviews),"historical_fidelity_reviews":len(historical_reviews),"work":edition["work"]["id"],"version":edition["version"],"sources":sources,
            "source_owned_status":edition["status"],"scope":edition["scope"],
            "predecessor":edition["predecessor"],"execution_credit":False,"unavailable_sources":unavailable,"complete":not unavailable}
    if output:
        dest=Path(output)
        if dest.exists():
            raise SourceError("EXISTS",str(dest))
        dest.mkdir(parents=True)
        for number,(source,data) in enumerate(bodies,1):
            atomic_bytes(dest/f"{number:02d}-{source['role']}{Path(source['path']).suffix}",data)
        atomic_bytes(dest/"sources.json",json.dumps(status,ensure_ascii=False,indent=2).encode())
        label="Public reading with unavailable identities" if unavailable else "Complete selected reading"
        print(f"{label} saved to {dest}: {len(bodies)} exact source bodies.")
        return 3 if unavailable else 0
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
        label={"baseline":"Source-owned catalogue status","claim":"Source-owned claim record","source_reading":"Preserved source-owner scope","source":"Source access status"}.get(edition["kind"],"Source-owned edition status")
        print("\n"+label+": "+json.dumps(edition["status"],ensure_ascii=False))
        print(edition["scope"])
        if edition["predecessor"]:
            print("This is the preserved predecessor. The current edition's review is not applied to it.")
        if not scientific_reviews:
            print("Controlling scientific review: NOT IDENTIFIED by this work binding; do not infer scientific acceptance.")
        else:
            print("Scientific review binding identified; inspect its exact target, premises, and scope before drawing conclusions.")
        if historical_reviews:
            print("Historical source-fidelity review is separate. It does not establish controlling scientific review or current adoption. Read it explicitly with --role historical or --role all.")
        if edition["work"].get("reading_links"):
            print("\nSource-owned review/currentness links:")
            print(json.dumps(edition["work"]["reading_links"],ensure_ascii=False,indent=2))
    for source,text in rendered:
        if source.get("review_kind")=="historical_source_fidelity":
            heading="Historical source-fidelity review"
        elif source["role"]=="review" and edition["kind"] in ("current","preserved_current"):
            heading="Source-owned review/adoption decision"
        else:
            heading=source["role"].replace("-"," ").title()
        print("\n## "+heading)
        print("Source: "+source["path"])
        print("Source edition: "+source.get("version",provider.baseline["commit"]))
        print(text,end="" if text.endswith("\n") else "\n")
    for missing in unavailable:
        print("\nUnavailable exact source: "+missing["original_sha256"]+" ("+missing["availability"]+"); no substitute body used.")
    print("\nReading scope: exact selected source bodies; no research code executed.")
    return 3 if unavailable else 0

def _record_bytes(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def _reading_material(provider,name,version=None):
    """Source-owned complete scholarly selection, without a new status decision."""
    edition=work_edition(provider,name,version)
    sources=_selected(edition,"reading",True)
    unavailable=[s for s in sources if "path" not in s]
    if any(s["role"]=="primary" for s in unavailable):
        raise SourceError("IDENTITY_ONLY","exact canonical body unavailable; no public summary substituted")
    bodies=[]
    for source in sources:
        if "path" not in source:continue
        data=provider.read_bytes(source["path"],source.get("version"))
        try:
            text=data.decode("utf-8")
        except UnicodeError as exc:
            raise SourceError("BINARY_SOURCE","this text transport cannot render a binary source; use show --output for exact reading files") from exc
        if "\0" in text:
            raise SourceError("BINARY_SOURCE","binary source requires an appropriate document reader")
        bodies.append((source,data))
    reviews=[s for s in sources if s["role"]=="review" and s.get("review_kind")!="historical_source_fidelity"]
    context={
        "work":{"id":edition["work"]["id"],"title":edition["work"]["title"],
                "source_owned_role":edition["work"].get("role"),
                "record_type":edition["work"].get("record_type","catalogue_work")},
        "version":edition["version"],"kind":edition["kind"],
        "predecessor":edition["predecessor"],"status":edition["status"],
        "scope":edition["scope"],"source_owner_record":edition["metadata"],
        "sources":sources,"reading_links":edition["work"].get("reading_links",[]),
        "unavailable_sources":unavailable,
        "review_availability":"BOUND_SOURCE_REVIEW" if reviews else "NOT_IDENTIFIED",
        "review_scope":"Read the exact target, premises, independence and limits of each bound review; a review role alone does not establish comprehensive controlling review or adoption.",
        "scientific_acceptance_inferred":False,
        "identity_scope":"A research objective, work, manuscript candidate, source, result and published edition are not interchangeable. Relations and status come from the exact source owners, never the newest title, storage or a successful build.",
        "execution_credit":False}
    return context,bodies

def _utf8_parts(data,limit):
    """Bound wire content without losing BOM, CRLF or a split Unicode codepoint."""
    start=0
    while start<len(data):
        end=min(start+limit,len(data))
        while True:
            while end<len(data) and data[end]&0xc0==0x80:end-=1
            if end==start:break
            encoded=json.dumps(data[start:end].decode("utf-8"),ensure_ascii=False).encode("utf-8")
            if len(encoded)<=12000:break
            end=start+max(1,(end-start)//2)
        if end==start:raise SourceError("READING_FRAME","chunk cannot contain a complete Unicode codepoint")
        yield start,data[start:end]
        start=end

def reading_records(provider,name,version=None,chunk_bytes=8192):
    """Preflight first; one named request can automatically deliver bounded frames.

    Consumers must offer every frame independently, retain sequence numbers and
    check complete receipt. An emitter cannot attest what a human/AI has seen.
    """
    if type(chunk_bytes) is not int or not 64<=chunk_bytes<=8192:
        raise SourceError("READING_FRAME","chunk bytes must be between 64 and 8192")
    context,bodies=_reading_material(provider,name,version)
    payloads=[("context",_record_bytes(context),None)]+[("source",data,
        {**{k:source[k] for k in ("path","sha256","git_blob","bytes","mode","role")},
         "version":source.get("version",provider.baseline["commit"])}) for source,data in bodies]
    records=[]
    def append(record):
        framed={"sequence":len(records),**record}
        if len(_record_bytes(framed))>12288:
            raise SourceError("READING_FRAME","serialized record exceeds transport bound")
        records.append(framed)
    append({"type":"begin","format":"orthemology-reading-1","work":context["work"]["id"],
            "title":context["work"]["title"],"version":context["version"],
            "payload_count":len(payloads),"chunk_bytes":chunk_bytes})
    for index,(kind,data,identity) in enumerate(payloads):
        parts=list(_utf8_parts(data,chunk_bytes))
        append({"type":"payload","payload":index,"kind":kind,"bytes":len(data),
                "sha256":sha256(data),"chunks":len(parts),"source":identity})
        for offset,part in parts:
            append({"type":"chunk","payload":index,"offset":offset,"bytes":len(part),
                    "sha256":sha256(part),"text":part.decode("utf-8")})
    digest=sha256(b"".join(_record_bytes(r)+b"\n" for r in records))
    append({"type":"end","records":len(records)+1,"stream_sha256":digest,
            "source_bodies":len(bodies),"source_bytes":sum(len(data) for _,data in bodies),
            "complete_sources":not context["unavailable_sources"],
            "reader_receipt":"NOT_CONFIRMED","execution_credit":False})
    return records

def verify_reading_records(provider,name,records,version=None):
    """Check receiver-supplied frames against exact source owners and full bodies.

    Frames may arrive out of order, but duplicates, holes, substituted bodies,
    versions, status or truncation cannot produce a byte-complete receipt.
    This does not attest actual presentation or scholarly comprehension.
    """
    def reject(detail):
        raise SourceError("READING_RECEIPT",detail)
    if not isinstance(records,list) or not records:reject("no delivered records")
    if any(not isinstance(r,dict) or type(r.get("sequence")) is not int for r in records):
        reject("each record needs an integer sequence")

    fields={
        "begin":{"sequence","type","format","work","title","version","payload_count","chunk_bytes"},
        "payload":{"sequence","type","payload","kind","bytes","sha256","chunks","source"},
        "chunk":{"sequence","type","payload","offset","bytes","sha256","text"},
        "end":{"sequence","type","records","stream_sha256","source_bodies","source_bytes",
               "complete_sources","reader_receipt","execution_credit"}}
    integers={"sequence","payload","bytes","chunks","offset","records","source_bodies","source_bytes","payload_count","chunk_bytes"}
    for record in records:
        if not isinstance(record.get("type"),str) or set(record)!=fields.get(record["type"],set()):
            reject("unknown, missing or misleading record fields")
        if any(type(value) is not int or value<0 for key,value in record.items() if key in integers):
            reject("invalid integer field")
        if any(type(record[key]) is not bool for key in ("complete_sources","execution_credit") if key in record):
            reject("invalid completion/credit field")
        if len(_record_bytes(record))>12288:reject("serialized record exceeds transport bound")
    sequences=[r["sequence"] for r in records]
    if len(set(sequences))!=len(sequences) or set(sequences)!=set(range(len(records))):
        reject("duplicate or missing record sequence")
    ordered=sorted(records,key=lambda r:r["sequence"])
    begin,end=ordered[0],ordered[-1]
    if begin.get("type")!="begin" or begin.get("format")!="orthemology-reading-1" or end.get("type")!="end":
        reject("opening or terminal record missing")
    limit=begin.get("chunk_bytes")
    if type(limit) is not int or not 64<=limit<=8192:reject("invalid chunk bound")
    if end.get("records")!=len(ordered) or end.get("stream_sha256")!=sha256(
            b"".join(_record_bytes(r)+b"\n" for r in ordered[:-1])):
        reject("incomplete or altered stream")
    context,bodies=_reading_material(provider,name,version)
    if (begin.get("work"),begin.get("title"),begin.get("version"))!=(
            context["work"]["id"],context["work"]["title"],context["version"]):
        reject("wrong named work or edition")
    expected=[("context",_record_bytes(context),None)]+[("source",data,
        {**{k:source[k] for k in ("path","sha256","git_blob","bytes","mode","role")},
         "version":source.get("version",provider.baseline["commit"])}) for source,data in bodies]
    if begin.get("payload_count")!=len(expected):reject("source population differs")
    position=1
    for index,(kind,data,identity) in enumerate(expected):
        if position>=len(ordered)-1:reject("missing payload")
        descriptor=ordered[position];position+=1
        if (descriptor.get("type"),descriptor.get("payload"),descriptor.get("kind"),
                descriptor.get("bytes"),descriptor.get("sha256"),descriptor.get("source"))!=("payload",index,kind,len(data),sha256(data),identity):
            reject("payload identity or scientific context differs")
        chunks=descriptor.get("chunks")
        if type(chunks) is not int or chunks<0:reject("invalid chunk population")
        received=bytearray()
        for _ in range(chunks):
            if position>=len(ordered)-1:reject("missing source chunk")
            record=ordered[position];position+=1
            if record.get("type")!="chunk" or record.get("payload")!=index or record.get("offset")!=len(received):
                reject("chunk offset or source differs")
            if not isinstance(record.get("text"),str):reject("chunk text absent")
            raw=record["text"].encode("utf-8")
            if not 0<len(raw)<=limit or record.get("bytes")!=len(raw) or record.get("sha256")!=sha256(raw):
                reject("chunk corrupt or outside advertised bound")
            received.extend(raw)
        if bytes(received)!=data:reject("incomplete or substituted source bytes")
    if position!=len(ordered)-1:reject("unexpected payload or trailing data")
    expected_end={"type":"end","records":len(ordered),"stream_sha256":end["stream_sha256"],
                  "source_bodies":len(bodies),"source_bytes":sum(len(data) for _,data in bodies),
                  "complete_sources":not context["unavailable_sources"],
                  "reader_receipt":"NOT_CONFIRMED","execution_credit":False,"sequence":len(ordered)-1}
    if end!=expected_end:reject("unsupported emitter completion/acceptance claim")
    return {"work":context["work"]["id"],"version":context["version"],
            "records":len(ordered),"stream_sha256":end["stream_sha256"],
            "complete_received_bytes":True,"complete_sources":not context["unavailable_sources"],
            "source_bodies":len(bodies),"source_bytes":end["source_bytes"],
            "review_availability":context["review_availability"],
            "presentation_assessed":False,"scientific_comprehension":"NOT_ASSESSED",
            "scope":"receiver-supplied records match complete exact source-owned reading; actual display and reading require separate evidence",
            "execution_credit":False}

def _regular_read(path):
    """Open only a real regular file, without following links or waiting on FIFOs."""
    path=_reject_links(Path(path).absolute())
    fd=os.open(path,os.O_RDONLY|getattr(os,"O_NONBLOCK",0)|getattr(os,"O_NOFOLLOW",0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise SourceError("READING_RECEIPT","input must be a regular file")
        return os.fdopen(fd,"rb")
    except BaseException:
        os.close(fd)
        raise

def _reading_json(raw):
    try:
        return load_json(raw)
    except RecursionError as exc:
        raise SourceError("READING_RECEIPT","record exceeds supported JSON nesting") from exc

def load_reading_records(provider,name,path,version=None):
    """Bound raw untrusted input before JSON parsing or whole-file allocation."""
    with _regular_read(path) as source:
        context,bodies=_reading_material(provider,name,version)
        sizes=[len(_record_bytes(context))]+[len(data) for _,data in bodies]
        # Smallest allowed chunks contain at least 61 UTF-8 bytes except tails.
        # Bound escaping and descriptor overhead without trusting received counts.
        budget=65536+6*sum(sizes)+1024*sum((size+60)//61+3 for size in sizes)
        if os.fstat(source.fileno()).st_size>budget:
            raise SourceError("READING_RECEIPT","input exceeds complete-work transport budget")
        records=[];total=0
        while True:
            line=source.readline(12290)
            if not line:break
            total+=len(line)
            raw=line[:-1] if line.endswith(b"\n") else line
            if not raw or len(raw)>12288 or total>budget:
                raise SourceError("READING_RECEIPT","empty or oversized raw record")
            records.append(_reading_json(raw))
        return records

def _new_reading_output(provider,path):
    path=_reject_links(Path(path).absolute())
    resolved=path.resolve()
    if resolved==provider.root or provider.root in resolved.parents:
        raise SourceError("OUTPUT_BOUNDARY","reading outputs belong outside the ordinary checkout")
    if path.exists():
        raise SourceError("EXISTS",str(path))
    return path

def _exclusive_reading_bytes(provider,path,data):
    """A failed/partial transport never replaces an existing receiver artifact."""
    path=_new_reading_output(provider,path)
    path.parent.mkdir(parents=True,exist_ok=True)
    _reject_links(path)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o600)
    try:
        with os.fdopen(fd,"wb") as output:
            output.write(data);output.flush();os.fsync(output.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return path

def _reading_index(path,records):
    """Describe canonical records without trusting a received index."""
    lines=[_record_bytes(record)+b"\n" for record in records]
    wire=b"".join(lines);pages=[];offset=0;page=b""
    for line in lines:
        if page and len(page)+len(line)>98304:
            pages.append({"offset":offset,"bytes":len(page),"sha256":sha256(page)})
            offset+=len(page);page=b""
        page+=line
    if page:
        pages.append({"offset":offset,"bytes":len(page),"sha256":sha256(page)})
    result={"format":"orthemology-reading-spool-1","path":str(Path(path).absolute()),
            "bytes":len(wire),"sha256":sha256(wire),"records":len(records),
            "work":records[0]["work"],"title":records[0]["title"],"version":records[0]["version"],
            "complete_sources":records[-1]["complete_sources"],"pages":pages,
            "reader_receipt":"NOT_CONFIRMED","execution_credit":False}
    # Keep the initial tool result bounded too; exceptionally large works need
    # a document reader with its own measured complete-delivery contract.
    if len(_record_bytes(result))>12288:
        raise SourceError("READING_FRAME","reading exceeds this adapter index bound; no partial spool created")
    return result,wire

def reading_spool(provider,path,records,inline_bytes=None):
    """One exact spool; optionally return the complete bounded population inline."""
    if inline_bytes is not None and (type(inline_bytes) is not int or not 0<=inline_bytes<=1048576):
        raise SourceError("READING_FRAME","inline budget must be between 0 and 1048576")
    result,wire=_reading_index(path,records)
    if inline_bytes is not None:
        inline={**result,"inline_frames":records}
        # Count the actual response, not just source/spool bytes: include the
        # envelope, JSON escaping, array separators and final printed newline.
        if len(_record_bytes(inline))+1<=inline_bytes:
            result=inline
        else:
            result={**result,"inline_frames":None,
                    "inline_omitted":"serialized response exceeds inline budget"}
            if len(_record_bytes(result))>12288:
                raise SourceError("READING_FRAME","reading exceeds this adapter index bound; no partial spool created")
    _exclusive_reading_bytes(provider,path,wire)
    return result

def reading_index(provider,name,path,version=None):
    """Recover a bounded index from original selection and authenticated bytes."""
    records=load_reading_records(provider,name,path,version)
    verify_reading_records(provider,name,records,version)
    ordered=sorted(records,key=lambda record:record["sequence"])
    result,expected=_reading_index(path,ordered)
    with _regular_read(path) as source:
        # One bounded reread rejects reordering, omitted final newline and any
        # replacement between parsing and authentication. Page hashes protect
        # later capture; a self-declared spool digest is never an identity root.
        if os.fstat(source.fileno()).st_size!=len(expected) or source.read(len(expected)+1)!=expected:
            raise SourceError("READING_RECEIPT","spool differs from the complete canonical selected reading")
    return result

def reading_page(path,offset,size,digest):
    if type(offset) is not int or offset<0 or type(size) is not int or not 1<=size<=98304:
        raise SourceError("READING_RECEIPT","invalid bounded page range")
    if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
        raise SourceError("READING_RECEIPT","invalid expected page identity")
    with _regular_read(path) as source:
        if offset+size>os.fstat(source.fileno()).st_size:
            raise SourceError("READING_RECEIPT","page extends beyond the received spool")
        if offset:
            source.seek(offset-1)
            if source.read(1)!=b"\n":
                raise SourceError("READING_RECEIPT","page does not start at a record boundary")
        source.seek(offset);data=source.read(size)
    if len(data)!=size or sha256(data)!=digest or not data.endswith(b"\n"):
        raise SourceError("READING_RECEIPT","page is corrupt, incomplete or outside its exact boundary")
    for line in data.splitlines():
        if not line or len(line)>12288:
            raise SourceError("READING_RECEIPT","page contains an invalid record boundary")
        _reading_json(line)
    return data

def query_metrics(provider,path,started,operation,query=None):
    if path is None:return
    record={"operation":operation,"query":query,
            "network_received_payload_bytes":provider.network_bytes,"network_wire_bytes":None,
            "source_routes":provider.sources_used,"preflight_seconds":time.perf_counter()-started,
            "provider_offline":provider.offline,"git_source_enabled":provider.git_repo is not None,
            "os_cache_state":"NOT_MEASURED","reader_receipt":"NOT_CONFIRMED",
            "scope":"query and source-owner received application payload bytes; excludes TLS/wire, presentation, attention and comprehension"}
    _exclusive_reading_bytes(provider,path,_record_bytes(record)+b"\n")

def fetch_named(provider,name,version=None,historical=False):
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
        sources=edition["sources"] if historical else scholarly_sources(edition["sources"])
        unavailable=[source for source in sources if "path" not in source]
        if unavailable:
            raise SourceError("IDENTITY_ONLY","named reading includes unavailable exact source identities; no summary substituted")
        for source in sources:
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

def materialise_context(provider, profile, destination, version=None, context=None, bundle=None, git_repository=None):
    """An explicit reading selection or the complete historical source closure."""
    selected=None
    if profile=="baseline":
        if version and version!=provider.baseline["commit"]:
            raise SourceError("AMBIGUOUS_VERSION","unindexed baseline workspace edition")
    else:
        selected=work_edition(provider,profile,version)
        if selected["version"]!=provider.baseline["commit"] or any(
                s.get("version",provider.baseline["commit"])!=provider.baseline["commit"]
                for s in selected["sources"]):
            raise SourceError("CURRENT_MATERIALISATION_UNSUPPORTED",
                              "current work requires version-aware workspace restoration; no baseline workspace was created")
        if context is None:
            raise SourceError("WORKSPACE_CONTEXT","choose --context reading or --context replay; named reading sources are not an executable closure")
    context=context or "reading"
    sources=_selected(selected,"reading") if selected else None
    if sources and any("path" not in source for source in sources):
        raise SourceError("IDENTITY_ONLY","the selected work has unavailable exact source identities; no complete workspace was created")
    if context=="replay":
        if (bundle is None)==(git_repository is None):
            raise SourceError("HISTORY_REQUIRED","replay context requires one explicit --bundle or --history-from-git")
        if not provider.manifest.get("history"):
            raise SourceError("HISTORY_REQUIRED","verified history identity is not locked")
        if bundle is not None and not Path(bundle).is_file():
            raise SourceError("HISTORY_REQUIRED","explicit history bundle is unavailable")
        if git_repository is not None and not Path(git_repository).is_dir():
            raise SourceError("HISTORY_REQUIRED","explicit historical Git source is unavailable")
        result=restore(provider,destination,True,bundle,git_repository)
        scope="complete public baseline source and Git-history closure; toolchains/external dependencies and scientific execution require separate replay"
    else:
        if bundle is not None or git_repository is not None:
            raise SourceError("WORKSPACE_CONTEXT","history arguments require --context replay")
        result=(materialise(provider,{s["path"] for s in sources},destination)
                if selected else restore(provider,destination))
        scope="exact reading sources only; not an executable dependency closure"
    return {**result,"work":selected["work"]["id"] if selected else "baseline",
            "context":context,"dependency_closure":context=="replay",
            "closure_scope":"public baseline sources and Git history" if context=="replay" else "selected reading",
            "execution_credit":False,"scope":scope}

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
    listing.add_argument("--metrics",type=Path,help="new external file for query payload and source routes")
    searching=sub.add_parser("search",help="metadata or explicit full-text source search")
    searching.add_argument("query");searching.add_argument("--subject")
    searching.add_argument("--full-text",action="store_true");searching.add_argument("--all-versions",action="store_true")
    searching.add_argument("--work");searching.add_argument("--version")
    searching.add_argument("--metrics",type=Path,help="new external file for query payload and source routes")
    reading=sub.add_parser("show",help="complete primary text and source-owned review/status")
    reading_name=reading.add_mutually_exclusive_group(required=True)
    reading_name.add_argument("--work");reading_name.add_argument("--source")
    reading.add_argument("--version")
    reading.add_argument("--role",choices=("primary","support","review","status","currentness","reading","historical","all"),default="primary")
    reading.add_argument("--include-status",action="store_true");reading.add_argument("--output",type=Path)

    framed=sub.add_parser("read",help="complete scholarly reading as bounded, sequenced UTF-8 JSONL frames")
    framed.add_argument("--work",required=True);framed.add_argument("--version")
    framed.add_argument("--chunk-bytes",type=int,default=8192)
    framed.add_argument("--metrics",type=Path,help="new external file for provider payload/routes/preflight metrics")
    framed.add_argument("--spool",type=Path,help="new external JSONL file; return a bounded page index instead of full stdout")
    framed.add_argument("--inline-bytes",type=int,help="with --spool, inline the complete response only within this bounded UTF-8 budget (0..1048576)")
    index=sub.add_parser("reading-index",help="recover an owner-checked bounded index for an existing canonical reading spool")
    index.add_argument("--work",required=True);index.add_argument("--version")
    index.add_argument("--input",type=Path,required=True)
    page=sub.add_parser("reading-page",help="read one authenticated bounded page of an external reading spool")
    page.add_argument("--input",type=Path,required=True);page.add_argument("--offset",type=int,required=True)
    page.add_argument("--bytes",dest="page_bytes",type=int,required=True);page.add_argument("--sha256",required=True)
    received=sub.add_parser("verify-reading",help="verify delivered frames against exact work, edition, status and complete source bytes")
    received.add_argument("--work",required=True);received.add_argument("--version")
    received.add_argument("--input",type=Path,required=True)
    compare=sub.add_parser("compare",help="compare explicitly indexed editions, never nearest versions")
    compare.add_argument("--work",required=True);compare.add_argument("--from",dest="old",required=True)
    compare.add_argument("--to",dest="new",required=True)
    resolving=sub.add_parser("resolve",help="exact historical path/context compatibility")
    resolving.add_argument("--legacy-path",required=True);resolving.add_argument("--context",required=True)
    fetching=sub.add_parser("fetch",help="cache an exact named reading and owner dependencies for offline access")
    choice=fetching.add_mutually_exclusive_group(required=True)
    choice.add_argument("--work");choice.add_argument("--all",action="store_true")
    fetching.add_argument("--version");fetching.add_argument("--historical",action="store_true")
    mat=sub.add_parser("materialise",help="explicit reading bundle or complete historical replay source context")
    mat.add_argument("--profile",required=True);mat.add_argument("--version");mat.add_argument("--dest",type=Path,required=True)
    mat.add_argument("--context",choices=("reading","replay"),help="required for named work; replay restores the complete public baseline/history")
    history=mat.add_mutually_exclusive_group()
    history.add_argument("--bundle",type=Path);history.add_argument("--history-from-git",type=Path)
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
        if args.command=="reading-page":
            sys.stdout.buffer.write(reading_page(args.input,args.offset,args.page_bytes,args.sha256))
            return 0
        provider=SourceProvider(args.root,args.cache,args.offline,git_repo=False if args.no_git_source else None)
        if args.command in ("list","search"):
            if args.metrics:_new_reading_output(provider,args.metrics)
            query_started=time.perf_counter()
            if args.command=="search" and args.full_text:
                result=fulltext_search(provider,args.query,args.all_versions,args.work,args.version)
                query_metrics(provider,args.metrics,query_started,args.command,args.query)
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
            query_metrics(provider,args.metrics,query_started,args.command,getattr(args,"query",None))
            for row in rows:
                print(row["title"]+"\n  "+row["id"]+" @ "+row.get("version",provider.baseline["commit"]))
            claims=sum(row.get("record_type")=="source_owned_claim" for row in rows)
            preserved=sum(row.get("record_type")=="source_owned_reading" for row in rows)
            print(f"{len(rows)-claims-preserved} named work editions; {claims} source-owned claim readings; {preserved} preserved-source readings. Named routes do not enumerate every research work.")
        elif args.command=="show":
            return show(provider,args.work,args.version,args.role,args.include_status,args.output,args.source)

        elif args.command=="read":
            if args.inline_bytes is not None and (args.spool is None or not 0<=args.inline_bytes<=1048576):
                raise SourceError("READING_FRAME","--inline-bytes requires --spool and a budget between 0 and 1048576")
            outputs=[path for path in (args.metrics,args.spool) if path is not None]
            if len({str(path.absolute()) for path in outputs})!=len(outputs):
                raise SourceError("OUTPUT_BOUNDARY","metrics and source spool must have separate destinations")
            for path in outputs:_new_reading_output(provider,path)
            started=time.perf_counter()
            records=reading_records(provider,args.work,args.version,args.chunk_bytes)
            elapsed=time.perf_counter()-started
            if args.metrics:
                metrics={"work":records[0]["work"],"version":records[0]["version"],
                         "network_received_payload_bytes":provider.network_bytes,"network_wire_bytes":None,
                         "source_routes":provider.sources_used,"preflight_seconds":elapsed,
                         "provider_offline":provider.offline,"git_source_enabled":provider.git_repo is not None,
                         "os_cache_state":"NOT_MEASURED","reader_receipt":"NOT_CONFIRMED",
                         "scope":"received application payload bytes and source preflight only; excludes TLS/wire, presentation, attention and comprehension"}
                _exclusive_reading_bytes(provider,args.metrics,_record_bytes(metrics)+b"\n")
            if args.spool:
                print(_record_bytes(reading_spool(provider,args.spool,records,args.inline_bytes)).decode("utf-8"))
            else:
                for record in records:
                    print(_record_bytes(record).decode("utf-8"),flush=True)
            return 0 if records[-1]["complete_sources"] else 3
        elif args.command=="reading-index":
            descriptor=reading_index(provider,args.work,args.input,args.version)
            print(_record_bytes(descriptor).decode("utf-8"))
            return 0 if descriptor["complete_sources"] else 3
        elif args.command=="verify-reading":
            records=load_reading_records(provider,args.work,args.input,args.version)
            receipt=verify_reading_records(provider,args.work,records,args.version)
            _print_json(receipt)
            return 0 if receipt["complete_sources"] else 3
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
                _print_json(fetch_named(provider,args.work,args.version,args.historical))
        elif args.command=="materialise":
            _print_json(materialise_context(provider,args.profile,args.dest,args.version,args.context,args.bundle,args.history_from_git))
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
