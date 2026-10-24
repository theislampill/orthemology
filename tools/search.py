"""Named metadata and exact-version full-text access with coverage reporting."""
from pathlib import Path
from source_provider import SourceError, load_json

def load_works(provider):
    path=provider.root/"corpus/works.jsonl"
    rows=[load_json(line) for line in path.read_bytes().splitlines() if line.strip()]
    if not rows:
        raise SourceError("POPULATION","empty work projection")
    keys=[(r["id"],r.get("version",provider.baseline["commit"])) for r in rows]
    if len(keys)!=len(set(keys)):
        raise SourceError("DUPLICATE_KEY","work and exact edition identity")
    # Preserve current rows exactly for source-owned regeneration checks.
    # Baseline records remain without row.version; its effective edition is
    # always the exact baseline commit, never a newest-current fallback.
    for work in rows:
        for source in work["sources"]:
            source.setdefault("version",provider.baseline["commit"])
    return rows

def _named(rows,name):
    exact=[r for r in rows if name==r["id"]]
    return exact or [r for r in rows if name.casefold()==r["title"].casefold() or name in r.get("aliases",[])]

def find_work(provider,name,version=None):
    matches=_named(load_works(provider),name)
    if version is not None:
        chosen=[r for r in matches if r.get("version",provider.baseline["commit"])==version]
    else:
        chosen=matches
    if len(chosen)!=1:
        raise SourceError("AMBIGUOUS_VERSION" if matches else "UNAVAILABLE",
                          f"named work: {name}; specify an exact --version when several editions are selected")
    return chosen[0]

def check_binding(provider,source):
    row=provider.resolve(source["path"],source.get("version"))
    for key in ("sha256","git_blob","bytes","mode"):
        if source.get(key)!=row[key]:
            raise SourceError("CORRUPT",f"work/source binding: {source['path']} ({key})")
    return row

def verify_work(provider,work,owner_cache=None):
    if work.get("version") and work["version"]!=provider.baseline["commit"]:
        from authority import verify_current_work
        verify_current_work(provider,work)
        for source in work["sources"]:
            check_binding(provider,source)
        return work["original_record"]
    owner=work.get("owner",{})
    if not owner.get("path") or not owner.get("json_pointer"):
        raise SourceError("UNAVAILABLE","work has no source-owned status binding")
    owner_record=provider.resolve(owner["path"],owner.get("version"))
    check_binding(provider,{**owner_record,**owner})
    owner_key=(owner["path"],owner.get("version",provider.baseline["commit"]),owner_record["sha256"])
    if owner_cache is not None and owner_key in owner_cache:
        obj=owner_cache[owner_key]
    else:
        obj=load_json(provider.read_bytes(owner["path"],owner.get("version")))
        if owner_cache is not None:owner_cache[owner_key]=obj
    try:
        for part in owner["json_pointer"].lstrip("/").split("/"):
            part=part.replace("~1","/").replace("~0","~")
            obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    except (KeyError,IndexError,ValueError,TypeError) as exc:
        raise SourceError("CORRUPT","work owner pointer") from exc
    if obj!=work["original_record"]:
        raise SourceError("CORRUPT","unsupported work/status edit; change its source owner")
    projected=work.get("source_owned_status",{}).get("catalogue_review_status")
    if projected is not None and projected!=obj.get("review_status"):
        raise SourceError("CORRUPT","unsupported scientific status promotion")
    for source in work["sources"]:
        check_binding(provider,source)
    return obj

def work_edition(provider,name,version=None):
    """Resolve selected exact edition, or a verified same-work predecessor."""
    matches=_named(load_works(provider),name)
    if not matches:
        raise SourceError("UNAVAILABLE",f"named work: {name}")
    selected=[w for w in matches if version is None or w.get("version",provider.baseline["commit"])==version]
    if len(selected)>1:
        raise SourceError("AMBIGUOUS_VERSION",f"{name}: specify --version; no newest fallback")
    if selected:
        work=selected[0]
        original=verify_work(provider,work)
        is_current=work.get("version",provider.baseline["commit"])!=provider.baseline["commit"]
        return {"work":work,"version":work.get("version",provider.baseline["commit"]),"sources":work["sources"],
                "metadata":original,"kind":"current" if is_current else "baseline","predecessor":False,
                "status":work["source_owned_status"] if is_current else {"catalogue_review_status":original.get("review_status","UNSPECIFIED")},
                "scope":"exact source-owned current declaration; external actor authentication not performed" if is_current else "historical catalogue curation; no new scientific adoption"}
    # No selected row has that edition. A current work may bind it as its
    # preserved predecessor; the source-owned helper verifies same-work linkage.
    candidates=[w for w in matches if w.get("version") and any(s.get("role")=="predecessor" and s.get("version")==version for s in w["sources"])]
    if not candidates:
        raise SourceError("AMBIGUOUS_VERSION","requested edition is not selected or bound as a same-work predecessor")
    from authority import predecessor_sources
    resolved=[(w,predecessor_sources(provider,w,version)) for w in candidates]
    signatures={tuple((s["path"],s.get("version"),s["sha256"],s["role"]) for s in item["sources"]) for _,item in resolved}
    if len(signatures)!=1:
        raise SourceError("AMBIGUOUS_VERSION","several differing predecessor readings are bound; choose an explicit source owner")
    carrier,prior=resolved[0]
    baseline=prior.get("baseline_work")
    if baseline:
        metadata=verify_work(provider,baseline)
        status={"catalogue_review_status":metadata.get("review_status","UNSPECIFIED")}
        kind="baseline"
    else:
        metadata=prior["source_metadata"]
        decision=prior.get("prior_review_and_adoption")
        status={"source_declared_status":metadata.get("status","UNSPECIFIED"),
                "prior_review_and_adoption":decision,"review_availability":prior.get("review_availability"),
                "current_review_applied":False}
        kind="preserved_current"
    for source in prior["sources"]:
        check_binding(provider,source)
    return {"work":baseline or carrier,"version":version,"sources":prior["sources"],"metadata":metadata,
            "kind":kind,"predecessor":True,"status":status,"scope":prior["scope"]}

def metadata_search(provider,query="",subject=None):
    terms=query.casefold().split()
    found=[]
    for work in load_works(provider):
        public=" ".join([work["title"],work["id"],*work.get("subjects",[])]).casefold()
        original=work.get("original_record",{})
        searchable=public+" "+original.get("explanation","").casefold()+" "+original.get("statement","").casefold()
        if all(term in searchable for term in terms) and (subject is None or subject.casefold() in public):
            found.append(work)
    return found

def fulltext_search(provider,query,all_versions=False,work=None,version=None):
    if not query:
        raise SourceError("EMPTY_QUERY","full-text query is required")
    if work:
        if all_versions and version is None:
            matches=_named(load_works(provider),work)
            if not matches:raise SourceError("UNAVAILABLE",f"named work: {work}")
            contexts={w.get("version",provider.baseline["commit"]) for w in matches}
            contexts.update(s["version"] for w in matches for s in w["sources"] if s.get("role")=="predecessor")
            readings=[work_edition(provider,work,context) for context in sorted(contexts)]
        else:
            readings=[work_edition(provider,work,version)]
        bindings={(s["path"],s.get("version",provider.baseline["commit"])) for edition in readings for s in edition["sources"]}
    elif all_versions:
        bindings={(path,provider.baseline["commit"]) for path in provider.occurrences}
        bindings.update((row["path"],row["version"]) for row in provider.manifest.get("current_sources",[]))
        if version is not None:
            bindings={item for item in bindings if item[1]==version}
    else:
        # Search all explicitly selected editions without choosing one by date.
        # Include preserved predecessor bodies as separately labelled editions.
        rows=load_works(provider)
        owner_cache={}
        for row in rows:verify_work(provider,row,owner_cache)
        bindings={(s["path"],s.get("version",provider.baseline["commit"])) for w in rows for s in w["sources"]
                  if s["role"] in ("primary","review","status","predecessor")}
        if version is not None:
            bindings={item for item in bindings if item[1]==version}
    if not bindings:
        raise SourceError("AMBIGUOUS_VERSION","no sources at requested explicit edition")
    matches=[];unavailable=[];decoded=binary=0
    for path,context in sorted(bindings):
        try:
            raw=provider.read_bytes(path,context)
        except SourceError as exc:
            if exc.code in ("NOT_CACHED","UNAVAILABLE","RESTRICTED","IDENTITY_ONLY"):
                unavailable.append({"path":path,"version":context,"state":exc.code})
                continue
            raise
        try:
            text=raw.decode("utf-16") if raw.startswith((b"\xff\xfe",b"\xfe\xff")) else raw.decode("utf-8-sig")
            if "\0" in text:raise UnicodeError()
        except UnicodeError:
            binary+=1;continue
        decoded+=1
        for number,line in enumerate(text.splitlines(),1):
            if query.casefold() in line.casefold():
                matches.append({"path":path,"version":context,"line":number,"text":line})
    return {"matches":matches,"selected":len(bindings),"searched":decoded,"binary":binary,"unavailable":unavailable,
            "scope":"decoded exact-version full source text; PDF/images/binary require their ordinary reading form",
            "complete":not unavailable}
