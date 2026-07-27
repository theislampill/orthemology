#!/usr/bin/env python3
"""Unit tests for the R7B math pipeline (Decision 0023): the strict LaTeX-subset
-> Typst-math translator and the md_to_typst wiring. Runnable: `python
tests/test_math_pipeline.py`. Deterministic, offline."""
import os
import sys
import tempfile
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from latex_to_typst_math import translate_inline, translate_display, MathConvertError
import md_to_typst
import build_pdfs
import validate_pdf_math
from validate_math_source import extract_inline_code_occurrences

for diagnostic_stream in (sys.stdout, sys.stderr):
    reconfigure = getattr(diagnostic_stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="backslashreplace")

FAILS = []


def eq(name, got, want):
    ok = got == want
    print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        print("      got : %r\n      want: %r" % (got, want))
        FAILS.append(name)


def ok(name, cond, detail=""):
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name, "" if cond else " — " + detail))
    if not cond:
        FAILS.append(name)


# --- translation exactness (meaning preservation is the whole point) ----------
eq("O-star", translate_inline(r"O^*(m; A)"), "O^*(m; A)")
eq("Inst subscript", translate_inline(r"\operatorname{Inst}_A"), 'op("Inst")_A')
eq("hat + subscript group", translate_inline(r"\hat p_{A,\alpha,t}"),
   "hat(p)_(A,alpha ,t)")
eq("bar mu", translate_inline(r"\bar\mu_{e,j}"), "macron(mu)_(e,j)")
eq("vec mu", translate_inline(r"\vec\mu"), "arrow(mu)")
eq("Pi partial", translate_inline(r"\Pi_A^\partial"), "Pi _A^(partial)")
eq("calligraphic", translate_inline(r"\mathcal{Q}_e"), "cal(Q)_e")
eq("angle brackets literal", translate_inline(r"\langle a, b \rangle"), "⟨ a, b ⟩")
eq("labeled arrow", translate_inline(r"m_t \xrightarrow{a_t} m"),
   "m_t arrow.r.long^(a_t) m")
eq("underbrace with label", translate_inline(r"\underbrace{x}_{y}"),
   "underbrace(x, y)")
eq("operatorname underscore", translate_inline(r"\operatorname{hand\_in}"),
   'op("hand_in")')

# --- strict contract: unknown commands raise, never pass through --------------
for bad in [r"\frobnicate", r"\sqrt{x}", r"\begin{matrix}a\end{matrix}"]:
    try:
        translate_inline(bad)
        ok("strict: rejects %s" % bad, False, "did not raise")
    except MathConvertError:
        ok("strict: rejects %s" % bad, True)

# unbalanced braces raise
for bad in [r"\hat{p", r"a}b"]:
    try:
        translate_inline(bad)
        ok("strict: rejects unbalanced %r" % bad, False, "did not raise")
    except MathConvertError:
        ok("strict: rejects unbalanced %r" % bad, True)

# --- display / aligned --------------------------------------------------------
d = translate_display(r"\begin{aligned} a &\to b \\ c &\to d \end{aligned}")
ok("aligned has two rows", d.count("&") == 2 and "\\" in d, repr(d))

# --- md_to_typst wiring: $...$ inline, ```math fence, backticks unchanged ------
out = md_to_typst.convert("Belief $\\hat p$ is not $O^*(m;A)$.")
ok("inline $...$ -> typst math", "$hat(p)$" in out and "$O^*(m;A)$" in out, out)

out2 = md_to_typst.convert("```math\n\\vec\\mu = (\\mu_1; \\preceq)\n```\n")
ok("```math fence -> display", "$ arrow(mu)" in out2, out2)

out3 = md_to_typst.convert("Identifier `Inst_A` stays code.")
ok("backtick identifier stays #raw", '#raw("Inst_A")' in out3, out3)

out4 = md_to_typst.convert(
    "Literal `python --version` and registry ID `V1` stay code."
)
ok(
    "literal command and semantic registry ID stay #raw",
    '#raw("python --version")' in out4 and '#raw("V1")' in out4,
    out4,
)

inventory_probe = extract_inline_code_occurrences(
    "Keep `V1` and classify `V1(e)`.\n```\n`fenced` is not inline\n```\n"
)
eq(
    "inventory extractor is locus-sensitive and fence-aware",
    [
        (
            row["locus"]["line"],
            row["locus"]["column"],
            row["occurrence"],
            row["text"],
        )
        for row in inventory_probe
    ],
    [(1, 6, 1, "V1"), (1, 24, 2, "V1(e)")],
)

# a math translation failure inside convert() surfaces as ConversionError
try:
    md_to_typst.convert("bad $\\nope$ math")
    ok("convert surfaces math errors", False, "did not raise")
except md_to_typst.ConversionError:
    ok("convert surfaces math errors", True)

# --- Task 13 PDFLaTeX publication pipeline -----------------------------------
ok(
    "Task 13 builder exposes the digest-pinned toolchain loader",
    hasattr(build_pdfs, "load_toolchain_lock"),
)
ok(
    "Task 13 builder exposes explicit candidate-status loading",
    hasattr(build_pdfs, "load_candidate_status"),
)
ok(
    "Task 13 builder exposes provenance-complete sidecar construction",
    hasattr(build_pdfs, "build_sidecar_record"),
)
ok(
    "Task 13 builder exposes stale-safe committed-PDF render preparation",
    hasattr(build_pdfs, "prepare_render_directory"),
)
ok(
    "Task 13 builder exposes exact six-artifact profile specs",
    hasattr(build_pdfs, "artifact_specs"),
)
ok(
    "Task 13 builder exposes offline digest-pinned Docker command construction",
    hasattr(build_pdfs, "docker_build_command"),
)
ok(
    "Task 13 builder exposes log hard-failure classification",
    hasattr(build_pdfs, "build_log_issues"),
)
ok(
    "Task 13 builder exposes declared package-local compatibility inputs",
    hasattr(build_pdfs, "compatibility_input_bytes"),
)
ok(
    "Task 13 builder exposes fail-closed Unicode inventory validation",
    hasattr(build_pdfs, "unicode_mapping_issues"),
)
ok(
    "Task 13 builder exposes compiled UTF-8 verbatim compatibility probing",
    hasattr(build_pdfs, "probe_utf8_verbatim_compatibility"),
)
ok(
    "Task 13 builder exposes compiled empty/nonempty bibliography probing",
    hasattr(build_pdfs, "probe_bibliography_compatibility"),
)
ok(
    "Task 13 builder exposes typed bibliography-run evidence classification",
    hasattr(build_pdfs, "classify_bibliography_run"),
)
ok(
    "Task 13 builder exposes a bounded latexmk execution timeout",
    hasattr(build_pdfs, "latexmk_timeout_seconds"),
)
ok(
    "Task 13 builder exposes an explicit runaway page guard",
    hasattr(build_pdfs, "latex_page_guard_pages"),
)
ok(
    "Task 13 builder exposes explicit UTF-8 diagnostic configuration",
    hasattr(build_pdfs, "configure_utf8_diagnostics"),
)

heading_normalize = getattr(
    build_pdfs, "normalize_heading_text", lambda _text: ""
)
heading_sequence_issues = getattr(
    build_pdfs,
    "heading_sequence_issues",
    lambda _text, _headings: ["heading matching helper unavailable"],
)
markdown_headings = getattr(
    build_pdfs,
    "_markdown_headings",
    lambda _sources: [],
)
fitrah_source = "4. Fiṭrah and proper function"
fitrah_pypdf = "4 4. Fit .rah and proper function"
fitrah_poppler = "4. Fitrah and proper function"
tawatur_source = "5. Tawātur versus memetic propagation"
tawatur_pypdf = "5 5. T aw¯ atur versus memetic prop-\nagation"
tawatur_poppler = "5. Tawa\u0304tur versus memetic propagation"
athari_source = (
    "10. Theological / Atharī route and the created/uncreated distinction"
)
athari_pypdf = (
    "10 10. Theological / Athar ¯ ı route\n"
    "and the created/uncreated distinction"
)
athari_poppler = (
    "10. Theological / Atharı\u0304 route\n"
    "and the created/uncreated distinction"
)

eq(
    "heading normalization preserves the Fiṭrah base letters",
    heading_normalize(fitrah_source),
    "4fitrahandproperfunction",
)
eq(
    "heading normalization preserves the Tawātur base letters",
    heading_normalize(tawatur_source),
    "5tawaturversusmemeticpropagation",
)
ok(
    "Fiṭrah source key matches exact pypdf and Poppler extraction forms",
    heading_normalize(fitrah_source) == "4fitrahandproperfunction"
    and heading_normalize(fitrah_source)
    in (heading_normalize(fitrah_pypdf) or "")
    and heading_normalize(fitrah_source)
    in (heading_normalize(fitrah_poppler) or ""),
    repr(
        (
            heading_normalize(fitrah_source),
            heading_normalize(fitrah_pypdf),
            heading_normalize(fitrah_poppler),
        )
    ),
)
ok(
    "Tawātur source key matches exact pypdf and Poppler extraction forms",
    heading_normalize(tawatur_source)
    == "5tawaturversusmemeticpropagation"
    and heading_normalize(tawatur_source)
    in (heading_normalize(tawatur_pypdf) or "")
    and heading_normalize(tawatur_source)
    in (heading_normalize(tawatur_poppler) or ""),
    repr(
        (
            heading_normalize(tawatur_source),
            heading_normalize(tawatur_pypdf),
            heading_normalize(tawatur_poppler),
        )
    ),
)
eq(
    "precomposed and decomposed heading forms normalize identically",
    (
        heading_normalize("Fiṭrah Tawātur"),
        heading_normalize("Fit\u0323rah Tawa\u0304tur"),
    ),
    ("fitrahtawatur", "fitrahtawatur"),
)
eq(
    "heading normalization retains non-Latin letters and Unicode numbers",
    heading_normalize("章節 １２"),
    "章節12",
)
ok(
    "punctuation, spacing, and detached marks normalize to an empty key",
    hasattr(build_pdfs, "normalize_heading_text")
    and heading_normalize(" — … \u0304 ") == "",
    repr(heading_normalize(" — … \u0304 ")),
)
eq(
    "punctuation-only source headings are rejected instead of skipped",
    heading_sequence_issues("irrelevant", ["— …"]),
    ["heading normalizes to empty Unicode letter/number key: — …"],
)
eq(
    "duplicate section counters and wrapped hyphenation match in order",
    heading_sequence_issues(
        fitrah_pypdf + "\n" + tawatur_pypdf,
        [fitrah_source, tawatur_source],
    ),
    [],
)
eq(
    "Poppler decomposed extraction forms match in order",
    heading_sequence_issues(
        fitrah_poppler + "\n" + tawatur_poppler,
        [fitrah_source, tawatur_source],
    ),
    [],
)
eq(
    "Atharī source matches exact pypdf detached-macron extraction",
    heading_sequence_issues(athari_pypdf, [athari_source]),
    [],
)
eq(
    "Atharī source matches exact Poppler dotless-i extraction",
    heading_sequence_issues(athari_poppler, [athari_source]),
    [],
)
eq(
    "unmarked dotless i remains a retained Unicode letter",
    heading_normalize("ı"),
    "ı",
)
eq(
    "transliteration modifier letters are compatibility punctuation",
    heading_normalize("Qurʾān and ʿaql"),
    "quranandaql",
)
eq(
    "other Unicode modifier letters remain retained letters",
    heading_normalize("ʹ"),
    "ʹ",
)
eq(
    "H2 through H4 headings are extracted exactly in source order",
    markdown_headings(
        {
            "probe.md": (
                b"# excluded H1\n"
                b"## H2\n"
                b"### H3\n"
                b"#### H4\n"
                b"##### excluded H5\n"
                b"```\n### fenced\n```\n"
            )
        }
    ),
    ["H2", "H3", "H4"],
)
heading_sources = {}
for heading_path in [
    "manuscript/orthemma-ortheme-systems-revised-draft.md",
    "theory/orthemic-core-formalization.md",
    "theory/orthemic-multi-actor-conflict-note.md",
    "companion/orthability-and-the-ground-of-intelligibility.md",
    "companion/orthability-divine-attributes-and-speech-athari.md",
    "companion/dynamic-orthing-noetic-learning-and-orthability.md",
    "docs/notation-gallery.md",
]:
    with open(os.path.join(ROOT, heading_path), "rb") as heading_stream:
        heading_sources[heading_path] = heading_stream.read()
all_source_headings = markdown_headings(heading_sources)
eq(
    "authoritative H2 through H4 inventory has exact ordered 162-heading digest",
    (
        len(all_source_headings),
        hashlib.sha256("\n".join(all_source_headings).encode("utf-8")).hexdigest(),
    ),
    (
        162,
        "624cfd2a6d166ba73b432a54bbfc9179ede988fe24c9c3fde6f5ef830e655dd3",
    ),
)
eq(
    "missing H3 is rejected",
    heading_sequence_issues("H2\nH4", ["H2", "H3", "H4"]),
    ["heading missing from PDF text: H3"],
)
eq(
    "reordered H3 and H4 are rejected",
    heading_sequence_issues("H2\nH4\nH3", ["H2", "H3", "H4"]),
    ["heading appears out of order: H4"],
)
eq(
    "duplicated H4 source heading requires two ordered PDF occurrences",
    heading_sequence_issues("H2\nH4", ["H2", "H4", "H4"]),
    ["heading appears out of order: H4"],
)
eq(
    "Quranic modifier-letter source matches extraction without modifiers",
    heading_sequence_issues(
        "Quran-locus, type/token, and terminology-matching validators",
        ["Qurʾān-locus, type/token, and terminology-matching validators"],
    ),
    [],
)
ok(
    "test diagnostics are explicitly UTF-8",
    (getattr(sys.stdout, "encoding", "") or "").replace("-", "").lower()
    == "utf8"
    and (getattr(sys.stderr, "encoding", "") or "").replace("-", "").lower()
    == "utf8",
    repr((sys.stdout.encoding, sys.stderr.encoding)),
)

builder_source = open(
    os.path.join(ROOT, "scripts", "build_pdfs.py"), encoding="utf-8"
).read()
ok(
    "canonical builder has no hard-coded R5 status preamble",
    "Review state (R5)" not in builder_source and "STATUS_LINES" not in builder_source,
)
ok(
    "canonical builder no longer executes the historical Typst renderer",
    "typst.compile" not in builder_source and "typst_source" not in builder_source,
)

if hasattr(build_pdfs, "load_candidate_status"):
    candidate = build_pdfs.load_candidate_status(ROOT)
    ok(
        "candidate status is read from the explicit generated overlay",
        candidate["source"] == "docs/current-candidate-state.yaml"
        and candidate["status_claims"]["candidate_status"] == "proposed-candidate"
        and candidate["status_claims"]["merged"] is False,
        repr(candidate),
    )

if hasattr(build_pdfs, "load_toolchain_lock"):
    lock = build_pdfs.load_toolchain_lock(ROOT)
    ok(
        "toolchain lock pins digest, platform, and exact TeX versions",
        lock["container"]["image"]
        == (
            "texlive/texlive@sha256:"
            "ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51"
        )
        and lock["container"]["config_digest"]
        == "sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1"
        and lock["container"]["platform"] == "linux/amd64"
        and lock["tools"]
        == {
            "latexmk": "4.87",
            "pdftex": "1.40.28",
            "bibtex": "0.99d",
            "kpathsea": "6.4.1",
        },
        repr(lock),
    )
    ok(
        "toolchain lock declares the exact fvextra dependency closure",
        lock.get("tex_packages")
        == {
            "fvextra": {
                "tex_live_package": "fvextra",
                "revision": 78177,
                "version": "1.14.0",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "fvextra/fvextra.sty"
                ),
                "role": "compatibility-direct",
            },
            "fancyvrb": {
                "tex_live_package": "fancyvrb",
                "revision": 77677,
                "version": "4.6",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "fancyvrb/fancyvrb.sty"
                ),
                "role": "fvextra-required",
            },
            "etoolbox": {
                "tex_live_package": "etoolbox",
                "revision": 77677,
                "version": "2.5m",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "etoolbox/etoolbox.sty"
                ),
                "role": "fvextra-required",
            },
            "upquote": {
                "tex_live_package": "upquote",
                "revision": 77677,
                "version": "1.3",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "upquote/upquote.sty"
                ),
                "role": "fvextra-required",
            },
            "textcomp": {
                "tex_live_package": "latex",
                "revision": 76924,
                "version": "2.1b",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "base/textcomp.sty"
                ),
                "role": "fvextra-required",
            },
            "lineno": {
                "tex_live_package": "lineno",
                "revision": 77890,
                "version": "5.7",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "lineno/lineno.sty"
                ),
                "role": "fvextra-required",
            },
            "keyval": {
                "tex_live_package": "graphics",
                "revision": 75374,
                "version": "1.15",
                "path": (
                    "/usr/local/texlive/2025/texmf-dist/tex/latex/"
                    "graphics/keyval.sty"
                ),
                "role": "fancyvrb-required",
            },
        },
        repr(lock.get("tex_packages")),
    )
    if hasattr(build_pdfs, "latexmk_timeout_seconds") and hasattr(
        build_pdfs, "latex_page_guard_pages"
    ):
        ok(
            "latexmk execution and page output are bounded independently of latexmk pass limits",
            build_pdfs.latexmk_timeout_seconds(lock) == 120
            and build_pdfs.latex_page_guard_pages(lock) == 500
            and b"$max_repeat = 5" in (
                open(os.path.join(ROOT, "publication", "latexmkrc"), "rb").read()
            ),
            repr(lock.get("build")),
        )
    if hasattr(build_pdfs, "docker_build_command"):
        command = build_pdfs.docker_build_command(
            lock,
            host_package_root="C:/safe/package",
            artifact_id="example-artifact",
            source_date_epoch=1785132636,
        )
        ok(
            "Docker build is digest-pinned, linux/amd64, offline, fixed-locale, and no-shell-escape",
            command[0:2] == ["docker", "run"]
            and "--rm" in command
            and "--network=none" in command
            and "--platform=linux/amd64" in command
            and lock["container"]["image"] in command
            and "SOURCE_DATE_EPOCH=1785132636" in command
            and "LANG=C.UTF-8" in command
            and any(
                item.startswith(
                    "PATH=/usr/local/texlive/2025/bin/x86_64-linux:"
                )
                for item in command
            )
            and command[-2] == "-c"
            and command[-1].endswith("/latexmk main.tex"),
            repr(command),
        )

if hasattr(build_pdfs, "compatibility_input_bytes"):
    compatibility = build_pdfs.compatibility_input_bytes(ROOT)
    ok(
        "compatibility inputs map Unicode literals, preserve main job identity, and wrap verbatim without suppression",
        set(compatibility)
        == {"publication/latexmkrc", "publication/pdftex-unicode-compat.tex"}
        and b"DeclareUnicodeCharacter{2208}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"DeclareUnicodeCharacter{2262}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"RequirePackage{fvextra}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"DefineVerbatimEnvironment{verbatim}{Verbatim}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breaklines=true" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breakanywhere" not in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breakafter={/-.:}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breakbefore={|}" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breakautoindent=false" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"breakindent=0pt" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"orthemologyTaskThirteenPageGuard>500" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"orthemologyTaskThirteenOriginalTwoColumn" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"if@twocolumn" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"orthemologyTaskThirteenEmptyBibliography" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"thebibliography" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"-jobname=main" in compatibility["publication/latexmkrc"]
        and b"main.bibtex.rc" in compatibility["publication/latexmkrc"]
        and b"tabcolsep" in compatibility[
            "publication/pdftex-unicode-compat.tex"
        ]
        and b"hfuzz" not in compatibility["publication/pdftex-unicode-compat.tex"]
        and b"vfuzz" not in compatibility["publication/pdftex-unicode-compat.tex"]
        and b"sloppy" not in compatibility["publication/pdftex-unicode-compat.tex"],
        repr(compatibility),
    )

if hasattr(build_pdfs, "fls_issues"):
    ok(
        "pdflatex recorder requires main.tex and generated main.bbl, not BibTeX-only bib input",
        build_pdfs.fls_issues(
            "INPUT main.tex\nINPUT ./main.bbl\n",
            "example-artifact",
        )
        == [],
    )
    if hasattr(build_pdfs, "unicode_mapping_issues"):
        latex_inputs = {
            path.replace("\\", "/"): open(
                os.path.join(ROOT, path), "rb"
            ).read()
            for path in [
                "publication/latex/%s/main.tex" % artifact_id
                for artifact_id, _sources in build_pdfs.DOCS
            ]
        }
        unicode_issues = build_pdfs.unicode_mapping_issues(
            latex_inputs,
            compatibility["publication/pdftex-unicode-compat.tex"],
        )
        ok(
            "all 68 generated-LaTeX non-ASCII code points have declared mappings",
            unicode_issues == [],
            repr(unicode_issues),
        )
        missing_mapping = compatibility[
            "publication/pdftex-unicode-compat.tex"
        ].replace(
            b"\\DeclareUnicodeCharacter{2262}{\\ensuremath{\\not\\equiv}}\n",
            b"",
        )
        missing_issues = build_pdfs.unicode_mapping_issues(
            latex_inputs, missing_mapping
        )
        ok(
            "Unicode inventory rejects an unmapped generated-source code point",
            any("U+2262" in issue for issue in missing_issues),
            repr(missing_issues),
        )

if hasattr(build_pdfs, "artifact_specs"):
    specs = build_pdfs.artifact_specs(ROOT)
    ok(
        "profile maps the exact six artifact identities",
        [row["artifact_id"] for row in specs]
        == [
            "orthemma-ortheme-systems-draft",
            "orthemic-core-reference-draft",
            "orthability-ground-of-intelligibility-draft",
            "orthability-divine-speech-athari-draft",
            "dynamic-orthing-noetic-learning-orthability-draft",
            "notation-gallery",
        ],
        repr(specs),
    )

if hasattr(build_pdfs, "build_log_issues"):
    issues = build_pdfs.build_log_issues(
        "\n".join(
            [
                "LaTeX Warning: Reference `missing' on page 1 undefined.",
                "LaTeX Warning: Citation `absent' on page 2 undefined.",
                "Overfull \\hbox (6.25pt too wide) in paragraph",
            ]
        ),
        tolerance_pt=5,
    )
    ok(
        "build logs reject unresolved references, citations, and overfull boxes above tolerance",
        len(issues) == 3,
        repr(issues),
    )
    ok(
        "build logs allow overfull boxes at or below the declared tolerance",
        build_pdfs.build_log_issues(
            "Overfull \\hbox (5.0pt too wide) in paragraph",
            tolerance_pt=5,
        )
        == [],
    )
    utf8_break_issues = build_pdfs.build_log_issues(
        (
            "LaTeX Error: Invalid UTF-8 byte sequence "
            "(�\\FancyVerbBreakAnywhereBreak)."
        ),
        tolerance_pt=5,
    )
    ok(
        "build logs explicitly reject multibyte verbatim-break corruption",
        any("UTF-8 verbatim break corruption" in issue for issue in utf8_break_issues),
        repr(utf8_break_issues),
    )
    pass_limit_issues = build_pdfs.build_log_issues(
        "Maximum runs of pdflatex reached without getting stable files",
        tolerance_pt=5,
    )
    ok(
        "build logs explicitly reject a latexmk pass-limit failure",
        any("latexmk pass limit" in issue for issue in pass_limit_issues),
        repr(pass_limit_issues),
    )
    page_guard_issues = build_pdfs.build_log_issues(
        "Task 13 runaway page guard exceeded",
        tolerance_pt=5,
    )
    ok(
        "build logs explicitly reject a runaway page-guard failure",
        any("runaway page guard" in issue for issue in page_guard_issues),
        repr(page_guard_issues),
    )

if hasattr(build_pdfs, "build_sidecar_record"):
    sidecar = build_pdfs.build_sidecar_record(
        artifact_id="example-artifact",
        pdf_sha256="a" * 64,
        page_count=3,
        source_commit="b" * 40,
        source_tree="8" * 40,
        independently_reviewed_equivalent_source_commit="7" * 40,
        independently_reviewed_equivalent_source_tree="8" * 40,
        source_date_epoch=1,
        markdown_sha256={"source.md": "c" * 64},
        latex_sha256={
            "publication/latex/example-artifact/main.tex": "d" * 64
        },
        bibliography_sha256="e" * 64,
        profile_sha256="f" * 64,
        toolchain_lock_sha256="1" * 64,
        candidate_status={
            "source": "docs/current-candidate-state.yaml",
            "sha256": "2" * 64,
            "label": "candidate",
            "status_claims": {
                "candidate_status": "proposed-candidate",
                "merged": False,
                "independent_signoff": False,
                "ready_for_merge": False,
            },
        },
        source_package_sha256="3" * 64,
        source_manifest_sha256="4" * 64,
        tool_versions={
            "latexmk": "4.87",
            "pdftex": "1.40.28",
            "bibtex": "0.99d",
            "kpathsea": "6.4.1",
            "python": "3.11.9",
            "pypdf": "6.14.2",
            "poppler": "25.07.0",
        },
        bibliography_qa={
            "disposition": "EMPTY_BIBLIOGRAPHY_NO_CITATIONS",
            "bbl_sha256": "9" * 64,
            "blg_sha256": "0" * 64,
        },
    )
    ok(
        "sidecar binds all source, package, profile, lock, and tool provenance",
        sidecar["source_commit"] == "b" * 40
        and sidecar["source_tree"] == "8" * 40
        and sidecar["independently_reviewed_equivalent_source_commit"]
        == "7" * 40
        and sidecar["source_tree_equivalence"] == "verified-identical"
        and sidecar["source_hashes"]["markdown"]["source.md"] == "c" * 64
        and sidecar["source_hashes"]["latex"][
            "publication/latex/example-artifact/main.tex"
        ]
        == "d" * 64
        and sidecar["source_package"]["sha256"] == "3" * 64
        and sidecar["source_manifest"]["sha256"] == "4" * 64
        and sidecar["publication_profile"]["sha256"] == "f" * 64
        and sidecar["toolchain_lock"]["sha256"] == "1" * 64
        and sidecar["candidate_status"]["status_claims"]["merged"] is False
        and sidecar["bibliography_qa"]["disposition"]
        == "EMPTY_BIBLIOGRAPHY_NO_CITATIONS"
        and set(sidecar["tools"])
        == {
            "latexmk",
            "pdftex",
            "bibtex",
            "kpathsea",
            "python",
            "pypdf",
            "poppler",
        },
        repr(sidecar),
    )

ok(
    "PDF math validator exposes v2 artifact-id validation",
    hasattr(validate_pdf_math, "validate_pdf_records"),
)
if hasattr(validate_pdf_math, "validate_pdf_records"):
    issues = validate_pdf_math.validate_pdf_records(
        [
            {
                "artifact_id": "example-artifact",
                "glyph_defect_repaired": True,
                "full_math_source_migrated": True,
                "expected_notdef": 0,
            }
        ],
        {"example-artifact": "rendered text"},
    )
    ok("v2 artifact_id PDF record validates without legacy pdf key", issues == [], repr(issues))

if hasattr(build_pdfs, "prepare_render_directory"):
    with tempfile.TemporaryDirectory() as td:
        stale = os.path.join(td, "page-99.png")
        nested = os.path.join(td, "stale")
        os.makedirs(nested)
        open(stale, "wb").write(b"stale")
        open(os.path.join(nested, "old.png"), "wb").write(b"stale")
        build_pdfs.prepare_render_directory(td)
        ok(
            "committed-PDF rasterization clears every stale page first",
            os.path.isdir(td) and os.listdir(td) == [],
            repr(os.listdir(td)),
        )

print("TOTAL: %d failures" % len(FAILS))
sys.exit(1 if FAILS else 0)
