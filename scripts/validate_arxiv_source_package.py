#!/usr/bin/env python3
"""Validate deterministic, closed Task 13 publication source packages."""
import argparse
import hashlib
import io
import json
import pathlib
import posixpath
import re
import sys
import tarfile

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
LATEXMKRC_OWNER = pathlib.Path("publication/latexmkrc")
PDFTEX_COMPAT_OWNER = pathlib.Path("publication/pdftex-unicode-compat.tex")
TOOLCHAIN_LOCK_OWNER = pathlib.Path("publication/toolchain-lock.yaml")


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _safe_name(name):
    path = pathlib.PurePosixPath(name)
    return (
        bool(name)
        and "\\" not in name
        and not path.is_absolute()
        and ".." not in path.parts
        and not re.match(r"^[A-Za-z]:", name)
    )


def validate_source_package_bytes(archive_bytes, manifest, profile):
    """Return deterministic issues for one archive, manifest, and profile."""
    issues = []
    artifact_id = manifest.get("artifact_id") if isinstance(manifest, dict) else None
    expected_main = (
        "publication/latex/%s/main.tex" % artifact_id if artifact_id else None
    )
    expected_bib = "references/orthemology.bib"
    expected_rc = (
        "publication/latex/%s/.latexmkrc" % artifact_id if artifact_id else None
    )
    expected_compat = (
        "publication/latex/%s/pdftex-unicode-compat.tex" % artifact_id
        if artifact_id
        else None
    )
    expected_names = [expected_rc, expected_main, expected_compat, expected_bib]
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            contents = {}
            for member in members:
                if not _safe_name(member.name):
                    issues.append("unsafe archive path: %s" % member.name)
                if not member.isfile():
                    issues.append("archive member must be a regular file: %s" % member.name)
                    continue
                extracted = archive.extractfile(member)
                contents[member.name] = extracted.read() if extracted else b""
                if (
                    member.mode != 0o644
                    or member.uid != 0
                    or member.gid != 0
                    or member.uname
                    or member.gname
                ):
                    issues.append("archive metadata is not normalized: %s" % member.name)
            names = [member.name for member in members]
    except (OSError, tarfile.TarError) as exc:
        return ["archive load failed: %s" % exc]

    if names != expected_names:
        issues.append(
            "archive members must be exact and sorted: expected %r, got %r"
            % (expected_names, names)
        )
    if manifest.get("archive", {}).get("sha256") != _sha(archive_bytes):
        issues.append("archive hash does not match manifest")
    provenance = profile.get("source_provenance", {})
    for key in (
        "source_commit",
        "source_tree",
        "source_date_epoch",
        "independently_reviewed_equivalent_source_commit",
        "independently_reviewed_equivalent_source_tree",
        "source_tree_equivalence",
    ):
        if manifest.get(key) != provenance.get(key):
            issues.append("manifest source provenance differs: %s" % key)
    if (
        manifest.get("source_tree")
        != manifest.get("independently_reviewed_equivalent_source_tree")
        or manifest.get("source_tree_equivalence") != "verified-identical"
    ):
        issues.append("manifest source tree equivalence is not exact")
    rows = manifest.get("members", [])
    expected_rows = [
        {
            "path": name,
            "sha256": _sha(contents[name]),
            "bytes": len(contents[name]),
            "mode": "0644",
        }
        for name in expected_names
        if name in contents
    ]
    if rows != expected_rows:
        issues.append("manifest member hashes or metadata do not match archive")

    owner_inputs = {
        expected_rc: ROOT.joinpath(LATEXMKRC_OWNER).read_bytes(),
        expected_compat: ROOT.joinpath(PDFTEX_COMPAT_OWNER).read_bytes(),
    }
    for member_name, expected_bytes in owner_inputs.items():
        if contents.get(member_name) != expected_bytes:
            issues.append(
                "package compatibility input differs from declared owner: %s"
                % member_name
            )
    expected_compatibility = {
        LATEXMKRC_OWNER.as_posix(): _sha(owner_inputs[expected_rc]),
        PDFTEX_COMPAT_OWNER.as_posix(): _sha(owner_inputs[expected_compat]),
    }
    if manifest.get("compatibility_inputs") != expected_compatibility:
        issues.append("manifest compatibility-input hashes are incomplete")
    toolchain_lock = yaml.safe_load(
        ROOT.joinpath(TOOLCHAIN_LOCK_OWNER).read_text(encoding="utf-8")
    )
    expected_dependencies = toolchain_lock.get("tex_packages", {})
    if manifest.get("tex_live_dependencies") != expected_dependencies:
        issues.append("manifest TeX package identities are incomplete")
    profile_dependencies = profile.get("toolchain", {}).get(
        "tex_live_package_identities", []
    )
    if profile_dependencies != list(expected_dependencies):
        issues.append("profile TeX package identities differ from toolchain lock")

    main_bytes = contents.get(expected_main)
    if main_bytes is None:
        return issues + ["declared main.tex is missing"]
    try:
        main = main_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        return issues + ["main.tex is not UTF-8: %s" % exc]

    package_policy = profile.get("package_policy", {})
    direct_packages = package_policy.get("direct_packages")
    supported_packages = package_policy.get("supported_packages")
    expected_direct = [
        "amsmath",
        "amssymb",
        "booktabs",
        "geometry",
        "hyperref",
        "microtype",
        "natbib",
        "xcolor",
    ]
    expected_supported = expected_direct + ["fvextra"]
    if direct_packages != expected_direct:
        issues.append("package policy direct package list is not exact")
    if supported_packages != expected_supported:
        issues.append("package policy supported package list is not exact")
    if (
        isinstance(direct_packages, list)
        and isinstance(supported_packages, list)
        and (
            not set(direct_packages) < set(supported_packages)
            or set(supported_packages) - set(direct_packages) != {"fvextra"}
        )
    ):
        issues.append("package policy direct and compatibility sets are invalid")

    main_declared = []
    for match in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]+)\}", main):
        main_declared.extend(item.strip() for item in match.group(1).split(","))
    compatibility_text = contents.get(expected_compat, b"").decode(
        "utf-8", errors="replace"
    )
    compatibility_declared = []
    for match in re.finditer(
        r"\\RequirePackage(?:\[[^\]]*\])?\{([^}]+)\}",
        compatibility_text,
    ):
        compatibility_declared.extend(
            item.strip() for item in match.group(1).split(",")
        )
    if main_declared != expected_direct:
        issues.append(
            "main package declarations must equal direct package policy: %r"
            % main_declared
        )
    if compatibility_declared != ["fvextra"]:
        issues.append(
            "compatibility package declarations must equal ['fvextra']: %r"
            % compatibility_declared
        )
    if set(main_declared) & set(compatibility_declared):
        issues.append("main and compatibility package declarations overlap")
    if (
        set(main_declared) | set(compatibility_declared)
        != set(expected_supported)
    ):
        issues.append("main and compatibility package union is not supported policy")
    declared_codepoints = {
        int(value, 16)
        for value in re.findall(
            r"\\DeclareUnicodeCharacter\{([0-9A-Fa-f]{4,6})\}",
            compatibility_text,
        )
    }
    observed_codepoints = {ord(character) for character in main if ord(character) > 127}
    for codepoint in sorted(observed_codepoints - declared_codepoints):
        issues.append(
            "generated LaTeX contains unmapped Unicode point U+%04X" % codepoint
        )
    if re.search(
        r"\\(?:immediate\s*)?write18|\\ShellEscape|\\usepackage\{shellesc\}",
        main,
        re.I,
    ):
        issues.append("shell escape is prohibited")
    if re.search(
        r"\\(?:usepackage\{fontspec\}|setmainfont|setsansfont|setmonofont)",
        main,
        re.I,
    ):
        issues.append("undeclared or system font selection is prohibited")

    bib_matches = re.findall(r"\\bibliography\{([^}]+)\}", main)
    if bib_matches != ["../../../references/orthemology"]:
        issues.append("bibliography command must bind the declared package owner")
    else:
        workdir = "publication/latex/%s" % artifact_id
        target = posixpath.normpath(posixpath.join(workdir, bib_matches[0]))
        if not posixpath.splitext(target)[1]:
            target += ".bib"
        if target != expected_bib or target.startswith("../"):
            issues.append("bibliography path escapes or misses the archive root")
    if expected_bib not in contents:
        issues.append("declared bibliography is missing")

    artifact = next(
        (
            row
            for row in profile.get("artifacts", [])
            if row.get("artifact_id") == artifact_id
        ),
        None,
    )
    if artifact is None:
        issues.append("artifact is not declared by the publication profile")
    elif artifact.get("appendix_mode") == "single-column":
        appendix_heading = (
            r"\\section\*\{15\. Limitations and Honest-Evidence Appendix\}"
        )
        conclusion_heading = r"\\section\*\{16\. Conclusion\}"
        layout = re.search(
            r"\\onecolumn\s*"
            + appendix_heading
            + r".*?\\twocolumn\s*"
            + conclusion_heading,
            main,
            re.S,
        )
        if layout is None:
            issues.append(
                "source-owned single-column appendix layout is missing or misordered"
            )
        if re.search(r"\\appendix(?:\s|$)", main):
            issues.append(
                "literal appendix command is prohibited for source-owned headings"
            )
    return issues


def validate_repository_packages(root=ROOT):
    root = pathlib.Path(root)
    profile = yaml.safe_load(
        (root / "docs" / "publication-profile.yaml").read_text(encoding="utf-8")
    )
    issues = []
    for artifact in profile["artifacts"]:
        artifact_id = artifact["artifact_id"]
        archive_path = root / "artifacts" / (artifact_id + ".source.tar.gz")
        manifest_path = root / "artifacts" / (
            artifact_id + ".source-manifest.json"
        )
        if not archive_path.is_file() or not manifest_path.is_file():
            issues.append("%s source package and manifest are required" % artifact_id)
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for issue in validate_source_package_bytes(
            archive_path.read_bytes(), manifest, profile
        ):
            issues.append("%s: %s" % (artifact_id, issue))
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args(argv)
    issues = validate_repository_packages(args.root)
    for issue in issues:
        print("[FAIL] %s" % issue)
    if not issues:
        print("[PASS] six deterministic closed publication source packages")
    print("TOTAL: %d failures" % len(issues))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
