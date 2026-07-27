#!/usr/bin/env python3
"""Task 13 source-package safety and determinism tests."""
import gzip
import importlib.util
import inspect
import io
import pathlib
import tarfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "scripts" / "build_pdfs.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_arxiv_source_package.py"


def load_module(name, path):
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILD = load_module("build_pdfs_task13", BUILD_PATH)
VALIDATOR = load_module("validate_arxiv_source_package", VALIDATOR_PATH)

ARTIFACT_ID = "orthemma-ortheme-systems-draft"
MAIN_PATH = "publication/latex/%s/main.tex" % ARTIFACT_ID
BIB_PATH = "references/orthemology.bib"
SOURCE_COMMIT = "1703a783d9b25a9cfa93370c4a1a0b568fa497d0"
SOURCE_TREE = "8edff88e8df79e8d0792d441c65227b9729403a9"
REVIEWED_SOURCE_COMMIT = "9dc0094cc6df908fbba1b965bb36d5f3f00979c0"
EPOCH = 1785161731
BASE_MAIN = r"""\documentclass[10pt,letterpaper,twocolumn]{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{microtype}
\usepackage{natbib}
\usepackage{xcolor}
\begin{document}
Body.
\onecolumn
\section*{15. Limitations and Honest-Evidence Appendix}
Appendix.
\twocolumn
\section*{16. Conclusion}
Conclusion.
\bibliographystyle{plainnat}
\bibliography{../../../references/orthemology}
\end{document}
"""
BASE_BIB = "@book{example, author={A}, title={T}, year={2026}}\n"
EMPTY_AUX = r"""\relax
\bibstyle{plainnat}
\bibdata{../../../references/orthemology}
"""
EMPTY_BBL = r"""\begin{thebibliography}{0}
\providecommand{\natexlab}[1]{#1}
\providecommand{\url}[1]{\texttt{#1}}
\expandafter\ifx\csname urlstyle\endcsname\relax
  \providecommand{\doi}[1]{doi: #1}\else
  \providecommand{\doi}{doi: \begingroup \urlstyle{rm}\Url}\fi

\end{thebibliography}
"""
EMPTY_BLG = r"""This is BibTeX, Version 0.99d (TeX Live 2025)
Capacity: max_strings=200000, hash_size=200000, hash_prime=170003
The top-level auxiliary file: main.aux
The style file: plainnat.bst
I found no \citation commands---while reading file main.aux
Database file #1: ../../../references/orthemology.bib
You've used 0 entries,
            2773 wiz_defined-function locations,
            592 strings with 4851 characters,
and the built_in function-call counts, 33 in all, are:
= -- 0
> -- 0
< -- 0
+ -- 0
- -- 0
* -- 2
:= -- 10
add.period$ -- 0
change.case$ -- 0
cite$ -- 0
empty$ -- 1
newline$ -- 8
(There was 1 error message)
"""
NONEMPTY_AUX = r"""\relax
\citation{example}
\bibstyle{plainnat}
\bibdata{../../../references/orthemology}
"""
NONEMPTY_BBL = r"""\begin{thebibliography}{1}
\bibitem[Author(2026)]{example}
Author. 2026. Example.
\end{thebibliography}
"""
NONEMPTY_BLG = r"""This is BibTeX, Version 0.99d (TeX Live 2025)
Capacity: max_strings=200000, hash_size=200000, hash_prime=170003
The top-level auxiliary file: main.aux
The style file: plainnat.bst
Database file #1: ../../../references/orthemology.bib
You've used 1 entry,
            2773 wiz_defined-function locations,
            592 strings with 4851 characters,
and the built_in function-call counts, 33 in all, are:
= -- 1
cite$ -- 1
"""
RECORDED_BBL_FLS = "INPUT main.tex\nINPUT ./main.bbl\n"


def locked_tex_packages():
    return yaml.safe_load(
        (ROOT / "publication" / "toolchain-lock.yaml").read_text(
            encoding="utf-8"
        )
    )["tex_packages"]


def unsafe_archive(entries):
    raw = io.BytesIO()
    with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=EPOCH) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.USTAR_FORMAT) as tf:
            for name, kind, data in entries:
                info = tarfile.TarInfo(name)
                info.mtime = EPOCH
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                info.mode = 0o644
                if kind == "file":
                    payload = data.encode("utf-8")
                    info.size = len(payload)
                    tf.addfile(info, io.BytesIO(payload))
                elif kind == "symlink":
                    info.type = tarfile.SYMTYPE
                    info.linkname = data
                    tf.addfile(info)
    return raw.getvalue()


class SourcePackageContractTests(unittest.TestCase):
    def api(self, module, name):
        self.assertIsNotNone(
            module,
            "Task 13 source-package validator must exist before this test can pass",
        )
        self.assertTrue(hasattr(module, name), name)
        return getattr(module, name)

    def create(self, main=BASE_MAIN, bib=BASE_BIB):
        create = self.api(BUILD, "create_source_package")
        parameters = inspect.signature(create).parameters
        self.assertTrue(
            {"latexmkrc", "pdftex_compat"}.issubset(parameters),
            parameters,
        )
        self.assertIn("tex_live_dependencies", parameters)
        return create(
            artifact_id=ARTIFACT_ID,
            main_tex=main.encode("utf-8"),
            bibliography=bib.encode("utf-8"),
            source_commit=SOURCE_COMMIT,
            source_tree=SOURCE_TREE,
            independently_reviewed_equivalent_source_commit=(
                REVIEWED_SOURCE_COMMIT
            ),
            independently_reviewed_equivalent_source_tree=SOURCE_TREE,
            source_date_epoch=EPOCH,
            profile_sha256="a" * 64,
            toolchain_lock_sha256="b" * 64,
            latexmkrc=(ROOT / "publication" / "latexmkrc").read_bytes(),
            pdftex_compat=(
                ROOT / "publication" / "pdftex-unicode-compat.tex"
            ).read_bytes(),
            tex_live_dependencies=locked_tex_packages(),
        )

    def validate(self, archive, manifest):
        validate = self.api(VALIDATOR, "validate_source_package_bytes")
        profile = yaml.safe_load(
            (ROOT / "docs" / "publication-profile.yaml").read_text(
                encoding="utf-8"
            )
        )
        profile["source_provenance"] = {
            "source_commit": SOURCE_COMMIT,
            "source_tree": SOURCE_TREE,
            "source_date_epoch": EPOCH,
            "independently_reviewed_equivalent_source_commit": (
                REVIEWED_SOURCE_COMMIT
            ),
            "independently_reviewed_equivalent_source_tree": SOURCE_TREE,
            "source_tree_equivalence": "verified-identical",
        }
        return validate(archive, manifest, profile)

    def validate_with_package_policy(self, archive, manifest, mutation):
        validate = self.api(VALIDATOR, "validate_source_package_bytes")
        profile = yaml.safe_load(
            (ROOT / "docs" / "publication-profile.yaml").read_text(
                encoding="utf-8"
            )
        )
        profile["source_provenance"] = {
            "source_commit": SOURCE_COMMIT,
            "source_tree": SOURCE_TREE,
            "source_date_epoch": EPOCH,
            "independently_reviewed_equivalent_source_commit": (
                REVIEWED_SOURCE_COMMIT
            ),
            "independently_reviewed_equivalent_source_tree": SOURCE_TREE,
            "source_tree_equivalence": "verified-identical",
        }
        profile["package_policy"]["direct_packages"] = [
            "amsmath",
            "amssymb",
            "booktabs",
            "geometry",
            "hyperref",
            "microtype",
            "natbib",
            "xcolor",
        ]
        profile["package_policy"]["supported_packages"] = (
            profile["package_policy"]["direct_packages"] + ["fvextra"]
        )
        mutation(profile["package_policy"])
        return validate(archive, manifest, profile)

    def test_deterministic_archive_has_closed_repository_relative_layout(self):
        archive_a, manifest_a = self.create()
        archive_b, manifest_b = self.create()
        self.assertEqual(archive_a, archive_b)
        self.assertEqual(manifest_a, manifest_b)
        self.assertEqual(self.validate(archive_a, manifest_a), [])
        self.assertEqual(
            manifest_a["tex_live_dependencies"],
            locked_tex_packages(),
        )
        self.assertEqual(manifest_a["source_commit"], SOURCE_COMMIT)
        self.assertEqual(manifest_a["source_tree"], SOURCE_TREE)
        self.assertEqual(
            manifest_a["independently_reviewed_equivalent_source_commit"],
            REVIEWED_SOURCE_COMMIT,
        )
        self.assertEqual(
            manifest_a["independently_reviewed_equivalent_source_tree"],
            SOURCE_TREE,
        )
        self.assertEqual(
            manifest_a["source_tree_equivalence"],
            "verified-identical",
        )

        with tarfile.open(fileobj=io.BytesIO(archive_a), mode="r:gz") as tf:
            members = tf.getmembers()
            self.assertEqual(
                [m.name for m in members],
                [
                    "publication/latex/%s/.latexmkrc" % ARTIFACT_ID,
                    MAIN_PATH,
                    "publication/latex/%s/pdftex-unicode-compat.tex"
                    % ARTIFACT_ID,
                    BIB_PATH,
                ],
            )
            self.assertTrue(all(m.isfile() for m in members))
            self.assertTrue(all(m.mode == 0o644 for m in members))
            self.assertTrue(all(m.uid == 0 and m.gid == 0 for m in members))
            self.assertTrue(all(m.uname == "" and m.gname == "" for m in members))
            self.assertTrue(all(m.mtime == EPOCH for m in members))

    def test_rejects_traversal_absolute_links_devices_and_stale_files(self):
        valid_archive, manifest = self.create()
        self.assertEqual(self.validate(valid_archive, manifest), [])
        attacks = {
            "traversal": [("../outside.tex", "file", BASE_MAIN)],
            "absolute": [("/outside.tex", "file", BASE_MAIN)],
            "link": [(MAIN_PATH, "symlink", "../../../outside")],
            "stale": [
                (MAIN_PATH, "file", BASE_MAIN),
                (BIB_PATH, "file", BASE_BIB),
                ("publication/latex/%s/main.aux" % ARTIFACT_ID, "file", "stale"),
            ],
        }
        for name, entries in attacks.items():
            with self.subTest(name=name):
                issues = self.validate(unsafe_archive(entries), manifest)
                self.assertTrue(issues, name)

    def test_rejects_shell_escape_unsupported_packages_fonts_and_external_paths(self):
        mutations = {
            "shell escape": BASE_MAIN.replace(
                "\\begin{document}", "\\immediate\\write18{echo bad}\n\\begin{document}"
            ),
            "unsupported package": BASE_MAIN.replace(
                "\\usepackage{amsmath}",
                "\\usepackage{amsmath}\n\\usepackage{todonotes}",
            ),
            "undeclared font": BASE_MAIN.replace(
                "\\usepackage{amsmath}",
                "\\usepackage{amsmath}\n\\usepackage{fontspec}",
            ),
            "outside bibliography": BASE_MAIN.replace(
                "../../../references/orthemology",
                "../../../../outside",
            ),
        }
        for name, main in mutations.items():
            with self.subTest(name=name):
                archive, manifest = self.create(main=main)
                issues = self.validate(archive, manifest)
                self.assertTrue(issues, name)

    def test_package_policy_separates_main_and_compatibility_declarations(self):
        valid_archive, manifest = self.create()
        self.assertEqual(self.validate(valid_archive, manifest), [])

        main_attacks = {
            "missing direct": (
                BASE_MAIN.replace("\\usepackage{xcolor}\n", ""),
                "main package",
            ),
            "overlapping compatibility direct": (
                BASE_MAIN.replace(
                    "\\usepackage{xcolor}",
                    "\\usepackage{xcolor}\n\\usepackage{fvextra}",
                ),
                "overlap",
            ),
        }
        for name, (main, fragment) in main_attacks.items():
            with self.subTest(name=name):
                archive, attacked_manifest = self.create(main=main)
                issues = self.validate(archive, attacked_manifest)
                self.assertTrue(
                    any(fragment in issue for issue in issues),
                    issues,
                )

        policy_attacks = {
            "missing direct policy": lambda policy: policy.pop(
                "direct_packages"
            ),
            "unsupported compatibility": lambda policy: policy[
                "supported_packages"
            ].append("tikz"),
            "missing compatibility": lambda policy: policy[
                "supported_packages"
            ].remove("fvextra"),
            "overlap": lambda policy: policy["direct_packages"].append(
                "fvextra"
            ),
        }
        for name, mutate in policy_attacks.items():
            with self.subTest(name=name):
                issues = self.validate_with_package_policy(
                    valid_archive,
                    manifest,
                    mutate,
                )
                self.assertTrue(
                    any("package policy" in issue for issue in issues),
                    issues,
                )

    def test_requires_source_owned_starred_appendix_layout(self):
        mutations = {
            "missing style": BASE_MAIN.replace("\\usepackage{booktabs}\n", ""),
            "missing bibliography command": BASE_MAIN.replace(
                "\\bibliography{../../../references/orthemology}\n", ""
            ),
            "missing appendix switch": BASE_MAIN.replace("\\onecolumn\n", ""),
            "one-column switch after appendix heading": BASE_MAIN.replace(
                "\\onecolumn\n\\section*{15. Limitations and Honest-Evidence Appendix}",
                "\\section*{15. Limitations and Honest-Evidence Appendix}\n"
                "\\onecolumn",
            ),
            "fabricated appendix command": BASE_MAIN.replace(
                "\\onecolumn\n",
                "\\onecolumn\n\\appendix\n",
            ),
            "unstarred appendix heading": BASE_MAIN.replace(
                "\\section*{15. Limitations and Honest-Evidence Appendix}",
                "\\section{15. Limitations and Honest-Evidence Appendix}",
            ),
            "wrong appendix number": BASE_MAIN.replace(
                "15. Limitations and Honest-Evidence Appendix",
                "14. Limitations and Honest-Evidence Appendix",
            ),
            "missing return to two columns": BASE_MAIN.replace(
                "\\twocolumn\n", ""
            ),
            "return before appendix": BASE_MAIN.replace(
                "\\onecolumn\n",
                "\\onecolumn\n\\twocolumn\n",
            ).replace("\\twocolumn\n\\section*{16. Conclusion}", "\\section*{16. Conclusion}"),
            "unstarred conclusion heading": BASE_MAIN.replace(
                "\\section*{16. Conclusion}", "\\section{16. Conclusion}"
            ),
            "wrong conclusion number": BASE_MAIN.replace(
                "16. Conclusion", "17. Conclusion"
            ),
        }
        for name, main in mutations.items():
            with self.subTest(name=name):
                archive, manifest = self.create(main=main)
                issues = self.validate(archive, manifest)
                self.assertTrue(issues, name)

    def test_accepts_layout_without_literal_appendix_command(self):
        archive, manifest = self.create()
        self.assertNotIn("\\appendix", BASE_MAIN)
        self.assertEqual(self.validate(archive, manifest), [])

    def test_rejects_incomplete_tex_live_dependency_identity_manifest(self):
        archive, manifest = self.create()
        manifest["tex_live_dependencies"].pop("fancyvrb")
        issues = self.validate(archive, manifest)
        self.assertTrue(
            any("TeX package identities" in issue for issue in issues),
            issues,
        )

    def bibliography_evidence(
        self,
        *,
        main=BASE_MAIN,
        aux=EMPTY_AUX,
        bbl=EMPTY_BBL,
        blg=EMPTY_BLG,
        bibtex_rc=2,
        fls=RECORDED_BBL_FLS,
        bibliography=BASE_BIB,
        expected_bibliography=None,
    ):
        classify = self.api(BUILD, "classify_bibliography_run")
        expected = bibliography if expected_bibliography is None else expected_bibliography
        return classify(
            main_tex=main.encode("utf-8"),
            aux_text=aux,
            bbl_bytes=bbl.encode("utf-8"),
            blg_text=blg,
            bibtex_rc=bibtex_rc,
            fls_text=fls,
            bibliography=bibliography.encode("utf-8"),
            expected_bibliography_sha256=BUILD.sha256_bytes(
                expected.encode("utf-8")
            ),
        )

    def test_typed_empty_bibliography_no_citations_evidence_is_exact(self):
        issues, record = self.bibliography_evidence()
        self.assertEqual(issues, [])
        self.assertEqual(
            record["disposition"],
            "EMPTY_BIBLIOGRAPHY_NO_CITATIONS",
        )
        self.assertEqual(record["bibtex_return_code"], 2)
        self.assertEqual(
            record["database_path"],
            "../../../references/orthemology.bib",
        )
        self.assertEqual(record["bibliography_style"], "plainnat")
        self.assertEqual(
            record["bbl_sha256"],
            BUILD.sha256_bytes(EMPTY_BBL.encode("utf-8")),
        )
        self.assertEqual(
            record["blg_sha256"],
            BUILD.sha256_bytes(EMPTY_BLG.encode("utf-8")),
        )
        self.assertEqual(record["citation_commands"], 0)

    def test_empty_bibliography_rejects_every_noncanonical_evidence_surface(self):
        attacks = {
            "source citation": {"main": BASE_MAIN.replace("Body.", r"Body \cite{example}.")},
            "aux citation": {"aux": EMPTY_AUX.replace(r"\bibstyle", "\\citation{example}\n\\bibstyle")},
            "wrong style": {"aux": EMPTY_AUX.replace("plainnat", "abbrvnat")},
            "wrong database": {
                "blg": EMPTY_BLG.replace(
                    "../../../references/orthemology.bib",
                    "../../../references/other.bib",
                )
            },
            "wrong BibTeX version": {
                "blg": EMPTY_BLG.replace("Version 0.99d", "Version 0.99c")
            },
            "wrong return code": {"bibtex_rc": 0},
            "additional warning": {"blg": EMPTY_BLG + "Warning--unexpected\n"},
            "additional error": {
                "blg": EMPTY_BLG.replace(
                    "(There was 1 error message)",
                    "I couldn't open database file extra.bib\n"
                    "(There were 2 error messages)",
                )
            },
            "noncanonical bbl": {"bbl": EMPTY_BBL + "% stale\n"},
            "entry in empty bbl": {
                "bbl": EMPTY_BBL.replace(
                    r"\end{thebibliography}",
                    "\\bibitem{example} Example.\n\\end{thebibliography}",
                )
            },
            "unrecorded bbl": {"fls": "INPUT main.tex\n"},
            "bibliography owner drift": {
                "expected_bibliography": BASE_BIB + "% changed\n"
            },
        }
        for name, changes in attacks.items():
            with self.subTest(name=name):
                issues, _record = self.bibliography_evidence(**changes)
                self.assertTrue(issues, name)

    def test_nonempty_bibliography_is_a_clean_positive_control(self):
        cited_main = BASE_MAIN.replace("Body.", r"Body \cite{example}.")
        issues, record = self.bibliography_evidence(
            main=cited_main,
            aux=NONEMPTY_AUX,
            bbl=NONEMPTY_BBL,
            blg=NONEMPTY_BLG,
            bibtex_rc=0,
        )
        self.assertEqual(issues, [])
        self.assertEqual(record["disposition"], "NONEMPTY_BIBLIOGRAPHY")
        self.assertEqual(record["bibtex_return_code"], 0)
        self.assertEqual(record["citation_commands"], 1)

        for name, changes in {
            "warning": {"blg": NONEMPTY_BLG + "Warning--bad entry\n"},
            "error return": {"bibtex_rc": 2},
            "empty output": {"bbl": EMPTY_BBL},
        }.items():
            with self.subTest(name=name):
                parameters = {
                    "main": cited_main,
                    "aux": NONEMPTY_AUX,
                    "bbl": NONEMPTY_BBL,
                    "blg": NONEMPTY_BLG,
                    "bibtex_rc": 0,
                }
                parameters.update(changes)
                issues, _record = self.bibliography_evidence(**parameters)
                self.assertTrue(issues, name)


if __name__ == "__main__":
    unittest.main()
