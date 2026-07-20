# Decision 0013 — Source attribution and source-status normalization

**Date:** 2026-07-20 · **Authority:** R4 owner authorization · **Status:** adopted in a **candidate revision requiring independent review** · **Reopens nothing;** the owner's adopted Atharī thesis is unchanged — only evidence status and attribution precision are corrected.

## Problem

1. **Attribution defect.** The corpus attributed the modern "concrete reason / ideal reason" contrast, and its application to Ibn Taymiyyah, to *Evans 2010* and *Turner 2022*. R3 already recorded that the phrase pair could not be found in either. The supplied compilation shows the application in a **different work by different authors**.
2. **Status conflict.** The Atharī paper's front matter said classical loci are `[via compilation]` and "the printed editions were not independently opened", while the R3 sourcing closeout reported work-level verification, verbatim confirmation of the *Majmūʿ* vol-12 formula, and no phantom sources. Both cannot govern the same draft.
3. **No single machine-readable source of source-truth**: prose, two Markdown ledgers, and a claim-source matrix could drift independently.

## Decision

### 1. One machine-readable registry

`references/source-status.yaml` is authoritative; the Markdown ledgers are generated or validated from it (`scripts/validate_source_status.py`, in CI, offline). Each load-bearing claim row carries: claim ID; document/locus; claim level; source; source type; edition/publication metadata; DOI or stable identifier; exact page/volume where available; verification status; verification date; whether wording was **directly** checked; whether the page number is **edition-dependent**; school/tradition flag; support/complication/contradiction; notes.

**Statuses:** `PRIMARY_TEXT_EXACT` · `PRIMARY_WORK_THEME` · `PRIMARY_LOCUS_EDITION_DEPENDENT` · `SECONDARY_VERIFIED` · `SECONDARY_RECONSTRUCTION` · `COMPILATION_MEDIATED` · `INFERENCE_CROSS_SOURCE` · `ORTHEMOLOGICAL_EXTENSION` · `UNVERIFIED_REMOVE_OR_DOWNSCOPE`.

Blanket front-matter source claims are abolished: each Atharī claim carries its own status, and the paper's front matter points to the registry instead of asserting one status for all loci.

### 2. Corrected concrete/ideal-reason attribution chain

Verified this pass:

- **Enis Doko and Jamie B. Turner**, "Islamic Religious Epistemology," ch. 10 in *The Cambridge Handbook of Religious Epistemology*, eds. Fuqua, Greco & McNabb, Cambridge University Press, **2023**, pp. 148–162, DOI `10.1017/9781009047180.013` — **the verified modern application to Ibn Taymiyyah**. `SECONDARY_VERIFIED`. **Doko must be credited**; this is not a Turner-solo claim.
- **C. Stephen Evans**, *Faith Beyond Reason: A Kierkegaardian Account*, 1998 — the reported source of the distinction. Two 1998 editions exist (Edinburgh UP; Eerdmans, Grand Rapids); Doko & Turner cite the **Eerdmans** edition and give "(1998, 94)". **The page locus could not be independently verified** — no accessible copy, snippet, or third-party quotation carrying the page was found, and the two editions may paginate differently. Status `SECONDARY_RECONSTRUCTION`, cited **as reported by Doko & Turner**, with the page never asserted as directly verified. Research residual RR-2 carries the trigger.
- **Turner 2022**, "Ibn Taymiyya on theistic signs and knowledge of God," *Religious Studies* 58(3):583–597, DOI `10.1017/S0034412521000159` — retained **only** for the natural-signs/theistic-signs claims it actually supports, not as the source of the phrase pair.
- **Turner 2023**, "Ibn Taymiyya's 'Common-Sense' Philosophy," in *Pluralizing Philosophy's Past*, Springer, pp. 197–212, DOI `10.1007/978-3-031-13405-0_14` — a **book chapter, 2023** (the corpus's "2022" was wrong).
- **Turner 2021**, "An Islamic Account of Reformed Epistemology," *Philosophy East and West* 71(3):767–792 — distinct record.

### 3. El-Tobgui: three distinct records

- **2013** McGill PhD dissertation (Institute of Islamic Studies).
- **2020** Brill monograph *Ibn Taymiyya on Reason and Revelation*, IPTS 111, ISBN 978-90-04-41285-9 (hbk) / 978-90-04-41286-6 (**open-access** e-book), a substantial revision of the dissertation.
- **2018** "From Legal Theory to *Erkenntnistheorie*: Ibn Taymiyya on *Tawātur* as the Ultimate Guarantor of Human Cognition," *Oriens* 46(1–2):6–61, DOI `10.1163/18778372-04601002` — **independent article**, previously cited via the compilation.

**The uploaded compilation is never cited as though it were one authored monograph or the original publication of any included work.** Its own Section 1 *is* the Doko & Turner chapter; claims read from it are labeled `COMPILATION_MEDIATED` until confirmed against the publisher's version.

### 4. Taymiyyan attributions

Direct claims about `ʿaql ṣarīḥ`, fiṭrah, necessary knowledge, mental universals vs external particulars, tawātur, corruption mechanisms, and objective truth with varied acquisition paths are verified against a primary locus where accessible, else labeled `SECONDARY_RECONSTRUCTION` — with **no paraphrase carrying false precision**. The *Darʾ* locus queue is research residual RR-3.

### 5. Qurʾānic and hadith loci

The corrected 20:11–12 distinction stands and the whole registry is revalidated after any change. For hadith and classical quotations, **exact wording verification is distinguished from work/theme-level verification** by status, and edition-dependent paginations are flagged per row rather than globally.

## Consequences

The Atharī paper's blanket front-matter claim is replaced by a per-claim pointer; no creed position changes. `PRIMARY_TEXT_EXACT` is reserved for loci whose wording was directly checked (the Qurʾānic loci, Muslim 2708, the *Majmūʿ* vol-12 formula). CI validates the registry and the prose-to-registry agreement; no live web request runs in CI.
