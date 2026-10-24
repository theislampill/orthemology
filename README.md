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

A tool client must deliver **every record automatically as a separate bounded response**. Do not print the entire stream as one budgeted tool response. Reordered notifications can be reconstructed by sequence; missing, duplicated, altered or substituted records fail verification. Verification establishes the bytes supplied to the verifier, not that a reader saw or understood them. A missing controlling review remains missing.

For ChatGPT code-mode, this is the ordinary named-reading adapter. Set `work` to the title returned by search and use the checkout/cache already selected for the session. This is one deliberate reading request; internal polling and frame notifications are automatic transport events. Any later manual source selection or recovery open is an additional action.

```javascript
const work = "Normal forms and transport for supplied certified selectors";
const root = "/absolute/path/to/orthemology";
const cache = "/absolute/path/to/research-cache";
const spool = "/absolute/path/outside-checkout/new-reading.jsonl";
const metrics = "/absolute/path/outside-checkout/new-reading-metrics.json";
const execution = {}; // Add only the host options authorised for this workspace.
const quote = value => "'" + String(value).replaceAll("'", "'\"'\"'") + "'";
const started = Date.now();
async function invoke(argv) {
  let result = await tools.exec_command({
    ...execution, cmd: argv.map(quote).join(" "), workdir: root,
    max_output_tokens: 60000, yield_time_ms: 1000
  });
  let output = result.output;
  while (result.session_id) {
    result = await tools.write_stdin({
      session_id: result.session_id, chars: "",
      max_output_tokens: 60000, yield_time_ms: 1000
    });
    output += result.output;
  }
  return {output, exit_code: result.exit_code};
}
const prepared = await invoke([
  "python", "-B", "tools/corpus.py", "--cache", cache, "--no-git-source",
  "read", "--work", work, "--spool", spool, "--metrics", metrics
]);
if (prepared.exit_code !== 0 && prepared.exit_code !== 3)
  throw new Error("Reading failed; no complete material may be inferred.");
const descriptor = JSON.parse(prepared.output);
let expectedOffset = 0;
for (const page of descriptor.pages) {
  if (page.offset !== expectedOffset || page.bytes < 1 || page.bytes > 98304)
    throw new Error("Invalid reading page population.");
  expectedOffset += page.bytes;
}
if (expectedOffset !== descriptor.bytes)
  throw new Error("Incomplete reading page index.");
const pages = await Promise.allSettled(descriptor.pages.map(page => invoke([
  "python", "-B", "tools/corpus.py", "reading-page", "--input", spool,
  "--offset", page.offset, "--bytes", page.bytes, "--sha256", page.sha256
])));
const byteLength = text => Array.from(text).reduce((n, c) => {
  const cp = c.codePointAt(0);
  return n + (cp < 128 ? 1 : cp < 2048 ? 2 : cp < 65536 ? 3 : 4);
}, 0);
const frames = [];
for (let i = 0; i < pages.length; i++) {
  const page = pages[i];
  if (page.status !== "fulfilled" || page.value.exit_code !== 0 ||
      byteLength(page.value.output) !== descriptor.pages[i].bytes)
    throw new Error("Missing, failed or truncated page; do not report receipt.");
  const lines = page.value.output.split("\n");
  if (lines.pop() !== "") throw new Error("Incomplete final record.");
  frames.push(...lines.map(line => JSON.parse(line)));
}
if (frames[0].type !== "begin" || frames.at(-1).type !== "end" ||
    frames.at(-1).records !== frames.length || descriptor.records !== frames.length ||
    frames.some((frame, index) => frame.sequence !== index))
  throw new Error("Incomplete reading transport; do not report receipt.");
store("orthemology-reading:" + spool, {descriptor, frames});
const label = frames[0].title + " @ " + frames[0].version;
for (const frame of frames) {
  if (frame.type === "chunk")
    notify(label + " — reading frame " + frame.sequence + "; payload " + frame.payload +
           "; source bytes [" + frame.offset + "," +
           (frame.offset + frame.bytes) + "); SHA-256 " + frame.sha256 +
           "\n" + frame.text);
  else notify(JSON.stringify(frame));
}
text({offered_records: frames.length, complete_sources: frames.at(-1).complete_sources,
      elapsed_to_offer_seconds: (Date.now() - started) / 1000,
      actual_reader_receipt: "AWAITING_READER_ACKNOWLEDGEMENT"});
```

The adapter first writes one new external JSONL spool and receives a small page index. It retrieves whole-record pages in parallel, each at most 98,304 bytes, before offering every frame. This bounds the subprocess response as well as the displayed notifications. Existing files are never overwritten. A failed page, changed source, malformed record or index overflow stops delivery; no partial success is inferred. Spool files are temporary reading outputs, not archives or independent custody. Remove them when the reading and its required evidence retention are finished.

Optional `--metrics NEW_FILE` on `list`, `search` or `read` records verified source routes, received application payload bytes and preflight duration. Use separate metrics files for discovery and reading: a cold query can retrieve source-owner records before the selected document is read, so reading metrics alone do not measure that earlier transfer. It leaves wire/TLS bytes, OS cache state, presentation and comprehension explicitly unmeasured. The adapter separately times source retrieval, bounded captures and notification offers; actual receipt and cold/warm qualification still require the receiving reader's evidence.

The client must retain raw records and the actually presented frames, disclose any omission marker, and acknowledge complete per-source coverage before claiming receipt. The supplied record stream can be checked with `verify-reading`. That check explicitly does not certify scholarly comprehension, review completeness, acceptance, or cold/warm performance. Binary sources require their appropriate full-document reader; `show --output NEW_DIRECTORY` preserves their exact files without pretending to render them as text.

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
