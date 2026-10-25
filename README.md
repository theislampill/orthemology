# Orthemology

Orthemology investigates the conditions of correct judgement, adequate reasoning and production, warranted recognition, objective standards, and source-grounded correction. Its philosophical arguments, mathematical results, formal proofs and applications retain their own premises and evidence scopes.

## Read the research

| Question | Start with the primary source |
|---|---|
| How do correctness, evidence and correction fit together? | [The main paper](papers/correctness-reasoning-and-systems.md) |
| What makes things intelligible and genuinely evaluable? | [Orthability and the ground of intelligibility](foundations/orthability-and-the-ground-of-intelligibility.md) · [current foundational arguments](foundations/current-arguments.md) |
| What follows about necessary being, productive adequacy and divine attributes? | [Modal grounding](foundations/modal-grounding/orthability-and-modal-grounding.md) · [attributes and speech](foundations/orthability-divine-attributes-and-speech-athari.md) |
| How do proper function, recognition, warrant and correction relate? | [Concrete and sound reason](foundations/concrete-and-sound-reason.md) · [dynamic orthing and noetic learning](foundations/dynamic-orthing-noetic-learning-and-orthability.md) |
| What must representations retain for future inquiry? | [Continuation-complete inquiry](mathematics/continuation/continuation-complete-inquiry.md) · [information, composition and revision](mathematics/information-and-revision/information-composition-and-self-revision.pdf) |
| How are collective judgement and formal reasoning governed? | [Formal core](mathematics/formal-foundations/core-formalization.md) · [collective inquiry](mathematics/collective-inquiry/conflict-and-shared-standards.md) |
| What are the substantive applications? | [DAEE epistemics](applications/daee-epistemics/README.md) |

The [reading guide](docs/reader/START_HERE.md) covers the programme's twelve avenues. [Current science](docs/reader/CURRENT_SCIENCE.md) presents affirmative arguments with their premises and qualifications; [research frontiers](docs/reader/RESEARCH_FRONTIERS.md) distinguishes established results from genuine open questions.

These guides are generated from existing scientific owners. A preserved source, a correct file hash, an ordinary mathematical argument, a finite control, a kernel-checked theorem and a scientific adoption decision are different forms of evidence. See [status](STATUS.md).

## Find a complete work and its review

Python 3.11 or later is sufficient for ordinary source reading; no proof toolchain is needed.

```sh
python tools/corpus.py list --subject geometry
python tools/corpus.py search "necessary being"
python tools/corpus.py show --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold" --include-status
```

The last command reads the complete selected primary texts and identified review, with the source-owned status. Use `--role reading` for the scholarly selection or `--output NEW_DIRECTORY` to save complete reading forms, including PDFs. Historical source-fidelity reports are available explicitly with `--role historical` or `--role all`. A missing controlling review is disclosed; it does not confer acceptance.

Source access verifies the exact edition against SHA-256 and Git blob identities. It can read retained Git history, an explicitly supplied verified cache, or the existing public source at its pinned commit. Reading does not silently reconstruct the old repository.

For deliberate offline reading, cache a named work:

```sh
python tools/corpus.py --cache ../research-cache fetch --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold"
python tools/corpus.py --cache ../research-cache --offline show --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold" --include-status
```

`search --full-text` reports the actual searched and unavailable populations. `fetch --all` deliberately caches the full public baseline (310,686,293 logical bytes); it is separate from an ordinary reading session. Source caches and restored proof environments live outside the ordinary checkout. Named `materialise` requires `--context reading` for a reading bundle or `--context replay` plus an explicit verified history source for a complete historical source workspace; neither choice executes a proof.

### Complete delivery to an AI reader

A long terminal response can be truncated by the receiving interface even when the source file was saved correctly. The `read` route emits the complete scholarly selection and its source-owned identity/status as bounded UTF-8 JSONL records. It preserves BOMs, line endings and every source byte. Each record has a sequence number; each source has byte offsets and hashes. No proof toolchain is needed.

```sh
python tools/corpus.py read --work "Normal forms and transport for supplied certified selectors"
python tools/corpus.py verify-reading --work "Normal forms and transport for supplied certified selectors" --input RECEIVED_RECORDS.jsonl
```

A tool client must deliver **every logical record automatically in bounded source notifications**. Consecutive whole records may share one bounded group; each record retains its sequence and exact content. Do not print the entire stream as one budgeted tool response. Reordered notifications can be reconstructed by sequence; missing, duplicated, altered or substituted records fail verification. Verification establishes the bytes supplied to the verifier, not that a reader saw or understood them. A missing controlling review remains missing.

For ChatGPT code-mode, this is the ordinary named-reading adapter. Set `work` to the title returned by search and use the checkout/cache already selected for the session. This is one deliberate reading request; internal polling and frame notifications are automatic transport events. Any later manual source selection or recovery open is an additional action.

```javascript
const work = "Normal forms and transport for supplied certified selectors"; // Exact listed title or ID.
const version = null; // Or an explicitly selected indexed edition.
const repeat = false; // True reoffers this session's same verified edition; it does not refresh currentness.
const root = "/absolute/path/to/orthemology";
const cache = "/absolute/path/to/research-cache";
const spool = "/absolute/path/outside-checkout/new-reading.jsonl";
const metrics = "/absolute/path/outside-checkout/new-reading-metrics.json";
const execution = {}; // Add only the host options authorised for this workspace.
const quote = value => "'" + String(value).replaceAll("'", "'\"'\"'") + "'";
const started = Date.now();
async function invoke(argv, budget=60000) {
  let result = await tools.exec_command({
    ...execution, cmd: argv.map(quote).join(" "), workdir: root,
    max_output_tokens: budget, yield_time_ms: 1000
  });
  let output = result.output;
  while (result.session_id) {
    result = await tools.write_stdin({
      session_id: result.session_id, chars: "",
      max_output_tokens: budget, yield_time_ms: 1000
    });
    output += result.output;
  }
  return {output, exit_code: result.exit_code};
}
const utf8 = text => {
  const bytes = [];
  for (const c of text) {
    const n = c.codePointAt(0);
    if (n >= 0xd800 && n <= 0xdfff) throw new Error("Invalid Unicode.");
    if (n < 128) bytes.push(n);
    else if (n < 2048) bytes.push(192 | n >> 6, 128 | n & 63);
    else if (n < 65536) bytes.push(224 | n >> 12, 128 | n >> 6 & 63, 128 | n & 63);
    else bytes.push(240 | n >> 18, 128 | n >> 12 & 63, 128 | n >> 6 & 63, 128 | n & 63);
  }
  return bytes;
};
// SHA-256 is a transport check here, not a substitute for the source provider.
const sha256 = input => {
  const bytes = [...input], bits = bytes.length * 8;
  bytes.push(128);
  while (bytes.length % 64 !== 56) bytes.push(0);
  for (let i = 7; i >= 0; i--) bytes.push(Math.floor(bits / 2 ** (8 * i)) & 255);
  const k = [
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
  ];
  const h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const rotate = (n, b) => n >>> b | n << (32 - b);
  for (let offset = 0; offset < bytes.length; offset += 64) {
    const w = new Uint32Array(64);
    for (let i = 0; i < 16; i++) w[i] = bytes[offset+4*i]<<24 | bytes[offset+4*i+1]<<16 | bytes[offset+4*i+2]<<8 | bytes[offset+4*i+3];
    for (let i = 16; i < 64; i++) {
      const x=w[i-15], y=w[i-2];
      w[i]=(rotate(x,7)^rotate(x,18)^x>>>3)+w[i-16]+(rotate(y,17)^rotate(y,19)^y>>>10)+w[i-7];
    }
    let [a,b,c,d,e,f,g,j]=h;
    for (let i = 0; i < 64; i++) {
      const t1=(j+(rotate(e,6)^rotate(e,11)^rotate(e,25))+((e&f)^(~e&g))+k[i]+w[i])>>>0;
      const t2=((rotate(a,2)^rotate(a,13)^rotate(a,22))+((a&b)^(a&c)^(b&c)))>>>0;
      j=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;
    }
    [a,b,c,d,e,f,g,j].forEach((v,i)=>{h[i]=(h[i]+v)>>>0;});
  }
  return h.map(n=>n.toString(16).padStart(8,"0")).join("");
};
const canonical = value => {
  if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
  if (value && typeof value === "object")
    return "{" + Object.keys(value).sort().map(k=>JSON.stringify(k)+":"+canonical(value[k])).join(",") + "}";
  if (typeof value === "number" && !Number.isSafeInteger(value)) throw new Error("Invalid integer.");
  return JSON.stringify(value);
};
const digest = text => sha256(utf8(text));
const ensure = (condition, detail) => { if (!condition) throw new Error(detail); };
const integer = value => Number.isSafeInteger(value) && value >= 0;
const hash = value => typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
const sameFields = (record, fields) => record && !Array.isArray(record) &&
  Object.keys(record).sort().join(",") === fields.split(" ").sort().join(",");
function validateIndex(d, selection, spool, version) {
  const fields = "format path bytes sha256 records work title version complete_sources pages reader_receipt execution_credit";
  let extra = "";
  if (Object.hasOwn(d, "inline_frames")) extra += " inline_frames";
  if (Object.hasOwn(d, "inline_omitted")) extra += " inline_omitted";
  ensure(sameFields(d, fields + extra), "Invalid index fields.");
  ensure(d.format === "orthemology-reading-spool-1" && d.path === spool &&
    (d.work === selection || d.title === selection) && (!version || d.version === version) &&
    typeof d.work === "string" && typeof d.title === "string" && typeof d.version === "string" &&
    integer(d.bytes) && integer(d.records) && d.records >= 3 && hash(d.sha256) &&
    typeof d.complete_sources === "boolean" && d.reader_receipt === "NOT_CONFIRMED" &&
    d.execution_credit === false && Array.isArray(d.pages), "Wrong reading identity or unsupported claim.");
  let offset = 0;
  for (const page of d.pages) {
    ensure(sameFields(page,"offset bytes sha256") && page.offset === offset &&
      integer(page.bytes) && page.bytes > 0 && page.bytes <= 98304 && hash(page.sha256), "Invalid page index.");
    offset += page.bytes;
  }
  ensure(offset === d.bytes, "Incomplete page population.");
}
function validateFrames(d, frames) {
  ensure(Array.isArray(frames) && frames.length === d.records, "Incomplete frame population.");
  const fields = {
    begin:"sequence type format work title version payload_count chunk_bytes",
    payload:"sequence type payload kind bytes sha256 chunks source",
    chunk:"sequence type payload offset bytes sha256 text",
    end:"sequence type records stream_sha256 source_bodies source_bytes complete_sources reader_receipt execution_credit"
  };
  frames.forEach((r,i)=>ensure(r && sameFields(r,fields[r.type] || "") &&
    r.sequence === i && utf8(canonical(r)).length <= 12288, "Invalid frame sequence or fields."));
  const begin=frames[0], end=frames.at(-1);
  ensure(begin.type === "begin" && begin.format === "orthemology-reading-1" &&
    begin.work === d.work && begin.title === d.title && begin.version === d.version &&
    integer(begin.payload_count) && begin.payload_count > 0 &&
    integer(begin.chunk_bytes) && begin.chunk_bytes >= 64 && begin.chunk_bytes <= 8192 &&
    end.type === "end" && end.records === frames.length && end.complete_sources === d.complete_sources &&
    end.reader_receipt === "NOT_CONFIRMED" && end.execution_credit === false, "Incomplete identity/completion record.");
  const lines=frames.map(canonical), wire=lines.join("\n")+"\n", raw=utf8(wire);
  ensure(raw.length === d.bytes && sha256(raw) === d.sha256 &&
    digest(lines.slice(0,-1).join("\n")+"\n") === end.stream_sha256, "Altered or truncated reading stream.");
  for (const page of d.pages)
    ensure(sha256(raw.slice(page.offset,page.offset+page.bytes)) === page.sha256, "Changed page binding.");
  let position=1, sourceBytes=0, context;
  for (let i=0; i<begin.payload_count; i++) {
    const p=frames[position++];
    ensure(p && p.type === "payload" && p.payload === i && p.kind === (i ? "source" : "context") &&
      integer(p.bytes) && integer(p.chunks) && hash(p.sha256), "Invalid source population.");
    let body="", bytes=0;
    for (let j=0; j<p.chunks; j++) {
      const c=frames[position++];
      ensure(c && c.type === "chunk" && c.payload === i && c.offset === bytes &&
        typeof c.text === "string" && integer(c.bytes) && c.bytes > 0 &&
        c.bytes <= begin.chunk_bytes && utf8(c.text).length === c.bytes &&
        digest(c.text) === c.sha256, "Corrupt or missing source chunk.");
      body += c.text; bytes += c.bytes;
    }
    ensure(bytes === p.bytes && digest(body) === p.sha256, "Incomplete source body.");
    if (i) {
      ensure(sameFields(p.source,"path sha256 git_blob bytes mode role version") &&
        p.source.sha256 === p.sha256 && p.source.bytes === p.bytes, "Source identity differs.");
      sourceBytes += bytes;
    } else {
      ensure(p.source === null, "Unexpected context source.");
      context=JSON.parse(body);
    }
  }
  ensure(position === frames.length-1 && end.source_bodies === begin.payload_count-1 &&
    end.source_bytes === sourceBytes && context.work.id === d.work && context.work.title === d.title &&
    context.version === d.version && Array.isArray(context.unavailable_sources) &&
    (context.unavailable_sources.length === 0) === d.complete_sources, "Scientific context or source population differs.");
  return frames;
}

const selected = ["--work",work,...(version ? ["--version",version] : [])];
const base = ["python","-B","tools/corpus.py","--cache",cache,"--no-git-source"];
const protocol = "orthemology-reading-client-2";
ensure([root,cache,work,spool].every(x=>typeof x==="string" && x.length>0) &&
  (version === null || typeof version === "string" && version.length>0), "Invalid reading request.");
const request = {root,cache,work,version,spool};
const sessionKey = "orthemology-reading-session:"+canonical([root,cache,work,version]);
const admissionKey = sessionKey+":admission";
let saved, admission;
try {
  ensure(typeof repeat === "boolean", "Invalid reading mode.");
  if (repeat) {
    ensure(typeof load === "function", "This client cannot reopen a session snapshot.");
    saved=load(sessionKey); admission=load(admissionKey);
  }
} finally {
  // No new failed/interrupted attempt may borrow an earlier complete offer.
  store(sessionKey,null); store(admissionKey,null);
}
let descriptor, frames, fallback=null, origin;
if (repeat) {
  ensure(sameFields(admission,"format state protocol request resolved_version origin snapshot_sha256") &&
    admission.format==="orthemology-reading-session-admission-1" &&
    admission.state==="OFFERED_NOT_RECEIVED" && admission.protocol===protocol &&
    canonical(admission.request)===canonical(request) && hash(admission.snapshot_sha256),
    "No compatible completed-offer admission; request a fresh source read.");
  ensure(sameFields(saved,"format state protocol request origin descriptor frames") &&
    saved.format==="orthemology-reading-session-1" && saved.state==="OFFERED_NOT_RECEIVED" &&
    saved.protocol===protocol && canonical(saved.request)===canonical(request) &&
    digest(canonical(saved))===admission.snapshot_sha256,
    "Changed or missing session snapshot; no source offer is permitted.");
  origin=saved.origin;
  ensure(sameFields(origin,"source_read_started_ms source_delivery initial_fallback resolved_version source_exit_code") &&
    integer(origin.source_read_started_ms) &&
    ["INLINE","PAGES","RECOVERED_PAGES"].includes(origin.source_delivery) &&
    (origin.initial_fallback===null ||
      sameFields(origin.initial_fallback,"event reason") &&
      origin.initial_fallback.event==="INITIAL_CAPTURE_REJECTED" &&
      typeof origin.initial_fallback.reason==="string") &&
    ((origin.initial_fallback!==null)===(origin.source_delivery==="RECOVERED_PAGES")) &&
    canonical(origin)===canonical(admission.origin),
    "Missing or unsupported original provider provenance.");
  descriptor=saved.descriptor;
  validateIndex(descriptor,work,spool,version);
  frames=validateFrames(descriptor,saved.frames);
  ensure(descriptor.version===admission.resolved_version && descriptor.version===origin.resolved_version &&
    origin.source_exit_code===(descriptor.complete_sources ? 0 : 3),
    "Session edition or original completeness differs.");
  // Original fallback evidence remains in origin; it is not a new recovery event.
} else {
  const sourceReadStarted=Date.now();
  const prepared = await invoke([...base,"read",...selected,"--spool",spool,
    "--metrics",metrics,"--inline-bytes","1048576"],300000);
  store("orthemology-reading-capture:"+spool,prepared);
  ensure(prepared.exit_code === 0 || prepared.exit_code === 3,
    "Source read failed; preserve the error. No complete material may be inferred.");
  try {
    descriptor=JSON.parse(prepared.output);
    validateIndex(descriptor,work,spool,version);
    if (Array.isArray(descriptor.inline_frames)) {
      ensure(utf8(prepared.output).length <= 1048576, "Inline response exceeds its bound.");
      frames=validateFrames(descriptor,descriptor.inline_frames);
    } else {
      ensure(descriptor.inline_frames === null &&
        descriptor.inline_omitted === "serialized response exceeds inline budget" &&
        utf8(prepared.output).length <= 12289, "Malformed inline omission.");
    }
  } catch (error) {
    fallback={event:"INITIAL_CAPTURE_REJECTED",reason:String(error)};
    store("orthemology-reading-recovery:"+spool,{prepared,fallback});
    // Authenticate the known spool against the original name/edition, not fields
    // taken from the rejected response. There is one recovery, never recursive retry.
    const recovered=await invoke([...base,"reading-index",...selected,"--input",spool],12000);
    ensure(recovered.exit_code === 0 || recovered.exit_code === 3, "Owner-checked recovery failed.");
    ensure(utf8(recovered.output).length <= 12289, "Recovered index exceeds its bound.");
    descriptor=JSON.parse(recovered.output);
    validateIndex(descriptor,work,spool,version);
    store("orthemology-reading-recovery:"+spool,{prepared,fallback,recovered});
  }
  if (!frames) {
    const pages=await Promise.allSettled(descriptor.pages.map(page=>invoke([
      "python","-B","tools/corpus.py","reading-page","--input",spool,
      "--offset",page.offset,"--bytes",page.bytes,"--sha256",page.sha256
    ])));
    store("orthemology-reading-pages:"+spool,pages);
    frames=[];
    for (let i=0; i<pages.length; i++) {
      const page=pages[i], expected=descriptor.pages[i];
      ensure(page.status === "fulfilled" && page.value.exit_code === 0 &&
        utf8(page.value.output).length === expected.bytes &&
        digest(page.value.output) === expected.sha256, "Missing, corrupt or truncated page.");
      const lines=page.value.output.split("\n");
      ensure(lines.pop() === "", "Incomplete final record.");
      frames.push(...lines.map(line=>JSON.parse(line)));
    }
    validateFrames(descriptor,frames);
  }
  ensure((prepared.exit_code === 0) === descriptor.complete_sources, "Exit/completeness mismatch.");
  origin={source_read_started_ms:sourceReadStarted,
    source_delivery:fallback ? "RECOVERED_PAGES" : Array.isArray(descriptor.inline_frames) ? "INLINE" : "PAGES",
    initial_fallback:fallback,resolved_version:descriptor.version,source_exit_code:prepared.exit_code};
}
store("orthemology-reading:"+spool,{descriptor,frames,fallback,origin});
function renderReadingFrame(frame, label) {
  return frame.type === "chunk" ?
    label+" — reading frame "+frame.sequence+"; payload "+frame.payload+
      "; source bytes ["+frame.offset+","+(frame.offset+frame.bytes)+"); SHA-256 "+frame.sha256+
      "\n"+frame.text : JSON.stringify(frame);
}
function groupReadingFrames(frames, label) {
  const limit=12288, groups=[];
  const items=frames.map(frame=>({sequence:frame.sequence,text:renderReadingFrame(frame,label)}));
  function pack(members, index) {
    let text="Orthemology reading group "+index+"; logical frames "+
      members[0].sequence+"–"+members.at(-1).sequence+"\n";
    const bindings=[];
    for (const member of members) {
      const bytes=utf8(member.text).length;
      text+="[reading frame "+member.sequence+"; "+bytes+" UTF-8 bytes]\n";
      const offset=utf8(text).length;
      text+=member.text+"\n[/reading frame "+member.sequence+"]\n";
      bindings.push({sequence:member.sequence,offset,bytes});
    }
    return {index,text,members:bindings,bytes:utf8(text).length};
  }
  let pending=[];
  for (const item of items) {
    const extended=pack([...pending,item],groups.length);
    if (extended.bytes<=limit) { pending.push(item); continue; }
    ensure(pending.length>0,"Rendered reading frame exceeds the notification limit.");
    groups.push(pack(pending,groups.length));
    pending=[item];
    ensure(pack(pending,groups.length).bytes<=limit,
      "Rendered reading frame exceeds the notification limit.");
  }
  if (pending.length) groups.push(pack(pending,groups.length));
  const sequences=groups.flatMap(group=>group.members.map(member=>member.sequence));
  ensure(sequences.length===frames.length && sequences.every((n,i)=>n===frames[i].sequence) &&
    groups.every(group=>group.bytes<=limit),"Incomplete or oversized reading delivery.");
  return groups.map(group=>({...group,sha256:digest(group.text)}));
}
const label=frames[0].title+" @ "+frames[0].version;
const groups=groupReadingFrames(frames,label); // Preflight every complete rendered message.
const compactDescriptor={...descriptor};
delete compactDescriptor.inline_frames; delete compactDescriptor.inline_omitted;
const snapshot={format:"orthemology-reading-session-1",state:"OFFERED_NOT_RECEIVED",
  protocol,request,origin,descriptor:compactDescriptor,frames};
const snapshotDigest=digest(canonical(snapshot));
store("orthemology-reading-delivery:"+spool,{
  format:"orthemology-reading-delivery-1",state:"DELIVERY_PLAN_NOT_RECEIPT",
  max_source_group_bytes:12288,
  logical_records:frames.length,groups
});
if (fallback) notify(fallback);
for (const group of groups) notify(group.text);
// This admission is written only after every offer returned, never from a capture or plan.
store(sessionKey,snapshot);
store(admissionKey,{format:"orthemology-reading-session-admission-1",state:"OFFERED_NOT_RECEIVED",
  protocol,request,resolved_version:descriptor.version,origin,snapshot_sha256:snapshotDigest});
text({offered_records:frames.length,offered_source_groups:groups.length,
  offered_diagnostic_events:fallback ? 1 : 0,offered_notifications:groups.length+(fallback ? 1 : 0),
  delivery_format:"BOUNDED_WHOLE_FRAME_GROUPS",
  complete_sources:frames.at(-1).complete_sources,
  elapsed_to_offer_seconds:(Date.now()-started)/1000,
  delivery:repeat ? "VERIFIED_SESSION_EDITION" : origin.source_delivery,
  fresh_provider_check:!repeat,currentness:repeat ? "PRIOR_FETCH_ONLY" : "PROVIDER_CHECKED_THIS_REQUEST",
  origin,source_completeness_exit:origin.source_exit_code,
  actual_reader_receipt:"AWAITING_READER_ACKNOWLEDGEMENT"});
```

The adapter first writes one new external JSONL spool. If the complete serialized response fits 1,048,576 UTF-8 bytes, it validates and offers every frame from that single capture. Otherwise it retrieves authenticated whole-record pages in parallel, each at most 98,304 bytes. The limit includes the envelope, JSON escaping and final newline. An incomplete or malformed initial capture is retained and permits one explicit source-owner-checked reading-index recovery using the original title/ID, edition and spool path. It cannot select a replacement work from corrupt response fields. Complete frame, source, context and hash checks precede every source notification. The adapter then groups consecutive complete rendered frame messages into source notifications of at most 12,288 UTF-8 bytes, including every header and separator. It preflights all groups before offering any source text. An oversized single rendered frame stops the offer; no text is split or shortened. The stored delivery plan binds each member by sequence and exact UTF-8 offset/length, so source text that resembles a frame header is not a parsing authority. Logical records, source groups and recovery diagnostic events are counted separately; the source-group byte cap does not claim to bound a separate diagnostic event. A delivery plan records intended output. Only the final summary after every notification call returns records a complete offer, and neither establishes actual reader receipt. Existing files are never overwritten. A failed page, changed source, failed owner check or index overflow stops delivery; no partial success is inferred. Spool files are temporary reading outputs, not archives or independent custody. Remove them when the reading and its required evidence retention are finished.


To read the **same authenticated edition again in this client session**, set `repeat = true` and rerun the same named-reading adapter with the same root, cache, work, requested version and spool values. Every frame is revalidated, regrouped and newly offered; a previous display or ACK is not reused as receipt. This route reads no new process or source payload. Its admission is tied to the original provider fetch, selected edition and complete snapshot, and is stored only after all notification calls returned. The original fallback, if any, remains provenance and is not reported as a new recovery. An identifiable selection invalidates its previous admission before mode/snapshot validation or delivery; missing, changed or interrupted session state fails explicitly. Set `repeat = false` and choose new spool/metrics paths for a fresh provider/currentness check. A null requested version in repeat mode stays pinned to the edition resolved by the original fetch. The session snapshot is trusted data from this originating client, not an independently authenticated archive or protection against a compromised client rewriting its admission. It carries the original source-owned status and review scope with **prior-fetch-only currentness**. It confers no new entitlement, scientific acceptance, actual receipt or timing qualification. All lookup, validation, hashing, grouping and offers still count within a measured repeat request.

Optional `--metrics NEW_FILE` on `list`, `search` or `read` records verified source routes, received application payload bytes and preflight duration. Use separate metrics files for discovery and reading: a cold query can retrieve source-owner records before the selected document is read, so reading metrics alone do not measure that earlier transfer. The source-route map records the last successful route for each logical path, not every transfer event; a cached reread cannot erase earlier bytes from the cumulative payload total. Metrics leave wire/TLS bytes, OS cache state, presentation and comprehension explicitly unmeasured. The adapter times the combined source-retrieval, bounded-capture and notification-offer interval; source preflight is recorded separately in the metrics file. Actual receipt and cold/warm qualification still require the receiving reader's evidence.

The client must retain raw records, the source-group delivery plan and the actually presented groups/frames, disclose any omission marker, and acknowledge complete per-source coverage before claiming receipt. The supplied record stream can be checked with `verify-reading`. That check explicitly does not certify scholarly comprehension, review completeness, acceptance, or cold/warm performance. Binary sources require their appropriate full-document reader; `show --output NEW_DIRECTORY` preserves their exact files without pretending to render them as text.

Research objectives, works, manuscript revisions, results, source occurrences and rendered editions remain distinct. The full source-owned record accompanies named readings. Governed manuscript routes separately expose their artifact/input commit, dated candidate snapshot and publication qualifications. Proposal routes carry the existing external adoption boundary; a newer candidate, equal-byte copy or successful build cannot promote it to accepted theory.

## Edit, reproduce and preserve

[Contributing](CONTRIBUTING.md) explains source ownership, new editions and review. The [reproducibility guide](docs/reader/REPRODUCIBILITY.md) separates reading, exact restoration, actual proof/experiment execution and publication.

```sh
python tools/corpus.py --help
python tools/replay.py --help
python tools/authority.py validate --root .
```

Historic paths and research labels remain resolvable as exact citations and replay inputs. Ordinary navigation uses the subject and argument. Original manuscripts, proofs, reviews, negative findings and historical source identities remain preserved.

The repository consolidation is being implemented and qualified through [R-0002](https://github.com/theislampill/orthemology/issues/38) and its [draft implementation PR](https://github.com/theislampill/orthemology/pull/39). That work reuses the completed reader refactor; it does not change scientific acceptance.
