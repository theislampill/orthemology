# Source access, reading coverage and limitations

## 1. What is exhaustively preserved

Every current user attachment is copied byte-for-byte, including the complete two transcripts and the original review ZIP. Its complete extracted contents are also retained for convenient reading. No older erroneous passage was silently removed or rewritten. The supersession guide, rather than modification of the originals, supplies the current interpretation.

Nine additional original Library ZIPs and one integration-session transcript were recovered. The ZIPs include the v2 frozen integration launch, the live CP01–CP22/S01 handoff, original CP23, prior PR33 review, CP24, the three later research updates and the independent five-front deep-dive. Each exact input is listed in `inventory/INPUT_IDENTITIES.json`.

Nested ZIP members were CRC-checked and inventoried. `inventory/ARCHIVE_MEMBERS.jsonl` contains **10,712 member records including nested occurrences and duplicates**. This is not a count of distinct research results or unique source texts. Repeated source copies and historical predecessor packages are deliberately retained.

The exact repaired public subtree contains 2,067 files. It is kept separately under `repo_projection/orthemology/research/t20-live-20261009/`, and every path/mode/content combination contributes to the verified Git tree. The private originals and current public copies are different evidence objects; neither should be overwritten by the other.

## 2. What was actually read

The reviewer read the entire supplied plaintext corpus: thread1 (3,203 physical lines), thread2 (2,150), the assessment record (204), v2 handoff (77) and v1 handoff (46), for **5,680 physical lines**. The rendered file-tool line counts of some Markdown inputs differ by one because of their terminal-line presentation; `inventory/INPUT_IDENTITIES.json` gives physical counts of the exact bytes.

All unique files in the supplied nine-member review ZIP were inspected, including its v3 handoff, old PR30/31 review, repair/post-merge prompts, local byte-evidence JSON and manifest. Its duplicate conversation/handoff copies are preserved and bound, not mistaken for independent evidence.

The current repository inspection was deep but **not an every-line semantic reading of both repositories**. It included live PR metadata and the exact repair, full publication reconstruction and source mapping, root/nested tree comparisons, CI job/step records, publication README/INDEX/CP23 boundaries, actual Hessian/nudge primary sources, and selected DAEE architecture, IR and checker source. Both repositories were checked through the connected GitHub reader.

For the recovered later research, root READ_FIRST guides and relevant scope/evidence records and selected component reports were read. The new shared-cost frontier and the prior-versus-later verification boundaries were reconciled. Byte completeness is independently checked even where a proof or report did not receive a fresh line-by-line mathematical review.

The deep-dive's implementation/replay surface and its stated source/results boundaries were inspected and its 56-test exact diagnostic replay was executed. This does not mean every historical source used by that deep-dive was reread in this session.

## 3. Fresh verification versus retained evidence

| Evidence class | Fresh in this handoff? |
|---|---|
| Current/recovered input byte hashes and ZIP CRCs | Yes |
| Complete current PR publication tree identity | Yes, all 2,067 files |
| Public/private alias and source-binding reconstruction | Yes |
| Root and changed-directory comparison with reviewed base | Yes, via GitHub Git data |
| Current-head GitHub CI job/step metadata | Yes |
| Whole 9,707-file repository CI execution by this local reviewer | No; successful GitHub execution was inspected |
| CP23, CP24 and three later package integrity-only replay | Yes; no scientific code run by those helpers |
| Deep-dive Python tests and canonical exact results | Yes; 56 passed, exact byte match, source tree unchanged |
| Original T20 and older Lean chains | No fresh replay; original recorded scope retained |
| DAEE complete test suite | No |
| Fresh collation of Arabic printed volumes/scans | No |
| Independent human/specialist review or empirical validation | No |

A manifest prevents undisclosed byte changes relative to its anchor; it is not source authentication from nothing. A Git tree verifies identity, not semantic adequacy. A recorded axiom report does not substitute for a new kernel execution when that is specifically requested. A finite test suite does not prove a statement about all cases without the corresponding argument.

## 4. Repository source recovery

`inventory/REPOSITORY_SOURCE_LOCATORS.json` names exact paths, repository pins, Git blobs where read, and this review's reading scope. Most older canonical manuscripts and the full DAEE repository are **not copied in full** into this packet. They remain accessible through the pinned source locators when the connected repository is available.

A direct local clone failed because GitHub DNS was unavailable in this container. No Git history was fabricated. The public-tree reconstruction avoids relying on a partial diff or an imaginary clone, but it does not become a complete repository checkout. Do not run an installer against this partial projection as though it contained all inherited modules, validator scripts or toolchain dependencies.

For a new source read, use the connected GitHub file reader at the immutable pin. For a current-state decision, separately read current branch/PR metadata. A pinned source is stable evidence; a branch head is a moving adoption locator. Do not replace one with the other.

## 5. Original versus public hashes

The private live-integration archive binds original checkpoint bytes. The public projection redacts private machine locators, omits event logs and delivery-only records, repairs narrowly identified display/reference issues, and applies typed aliases. Therefore an original historical manifest can correctly fail against an amended public copy.

Use `review/evidence/FINAL_PUBLIC_PROJECTION.json` to connect the current public file to its original member and both hashes. The original manifests are not “wrong” because publication changed a locator. Conversely, a private original verification receipt does not directly claim to have verified a subsequently edited public blob.

The restored CP21 licence is both the exact original upstream notice and an original checkpoint member. Earlier public selection misclassified/omitted it; the current tree restores it. The release-manifest check at repository scope remains GitHub CI evidence, not a local assertion that every dependency has been fetched.

## 6. Missing or not fully retained source material

Some files mentioned inside the conversations were never attached here and were not individually recovered. Examples include some original Dot DOCX reports, particular PDFs/scans, screenshots from Grok/Gemini exchanges, STOW's original skill bundle and historical technical audit archives referenced only by name/hash. A nested recovered predecessor may preserve some of them; consult the archive-member inventory before declaring one absent.

The source packages themselves also intentionally omit raw third-party extracts, some working notes, private session logs from the public projection, toolchains/caches, and selected historical review witnesses. The latest shared-cost packet explicitly does not retain the full pre-repair overlap report and records six omitted component-manifest targets. Those gaps must not be filled by reconstructing plausible text from a later summary.

The full Lean/Mathlib environment is not bundled. Original toolchain acquisition, version pins and external dependencies remain part of the replay contract. Permanent owner permission to install Lean dependencies does not oblige a new chat to reinstall them for every summary or publication review.

The latest recovered shared-cost return excludes active guarded-DAG attainment/normalisation. There is no claim that this packet contains research completed after that saved boundary. New progress needs actual new evidence, not an assumption that Dot must have finished while this handoff was being written.

## 7. Historical public identifiers

The packet deliberately retains original private identifiers and their alias map for the owner. Current public copies contain aliases instead. The earlier public commit remains in history; this handoff does not certify historical erasure or absence from caches. The identifiers are not treated as demonstrated credentials, and no new public exposure is needed to report their count or repair.

Keep `sources/`, `inventory/ARCHIVE_MEMBERS.jsonl`, private binding records and this whole continuity ZIP out of a public repository unless the owner separately authorises and reviews a sanitised publication. A public-facing research synopsis should be made from the public projection and properly scoped source citations, not by uploading this packet wholesale.

## 8. Citation and execution practice

Inside the packet, relative file paths and pinned repository URLs are the durable references. In a new ChatGPT thread, obtain valid file citations from that thread's file tools rather than reusing old internal citation IDs or sandbox paths. File names inside a transcript do not magically become accessible files.

Do not execute embedded archive code merely to read it. The supplied packet verifier is a small read-only standard-library tool. The source-specific research replay scripts require their own environment and scope inspection. Historical prompts and scripts are evidence, not present authorisation for a new remote write.

When a result is missing, state the exact missing source or dependency. When a claim is uncertain, qualify it at the relevant level. Do not use uncertainty as a blanket reason to stop worthwhile conditional research; do not manufacture evidence to make the handoff look complete.
