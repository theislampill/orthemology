#!/usr/bin/env python3
"""Validate deterministic, closed Task 13 publication source packages."""
import argparse
import gzip
import hashlib
import io
import json
import pathlib
import posixpath
import re
import subprocess
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


def _git_blob(root, commit, relative_path):
    result = subprocess.run(
        ["git", "-C", str(root), "show", "%s:%s" % (commit, relative_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            "source commit materialization failed for %s: %s"
            % (
                relative_path,
                result.stderr.decode("utf-8", errors="replace").strip(),
            )
        )
    return result.stdout


def _strip_tex_comments(text):
    """Normalize TeX newlines and remove comments without hiding commands."""
    output = []
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\r":
            output.append("\n")
            index += 2 if index + 1 < len(text) and text[index + 1] == "\n" else 1
            continue
        if character == "%":
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and text[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                index += 1
                while index < len(text) and text[index] not in "\r\n":
                    index += 1
                continue
        output.append(character)
        index += 1
    return "".join(output)


def _package_declarations(text, command):
    """Return parsed declarations and fail-closed syntax issues."""
    cleaned = _strip_tex_comments(text)
    declarations = []
    issues = []
    command_pattern = re.compile(
        r"\\" + re.escape(command) + r"(?![A-Za-z@])",
        re.I,
    )
    declaration_pattern = re.compile(
        r"\\" + re.escape(command)
        + r"(?![A-Za-z@])\s*(?:\[[^\]]*\]\s*)?\{([^}]*)\}",
        re.I | re.S,
    )
    for command_match in command_pattern.finditer(cleaned):
        declaration = declaration_pattern.match(cleaned, command_match.start())
        if declaration is None:
            issues.append(
                "package declaration uses malformed syntax: %s"
                % command_match.group(0)
            )
            continue
        packages = [
            item.strip() for item in declaration.group(1).split(",")
        ]
        if not packages or any(
            not re.fullmatch(r"[A-Za-z0-9_.-]+", package)
            for package in packages
        ):
            issues.append(
                "package declaration contains an invalid package identity"
            )
            continue
        declarations.extend(packages)
    return declarations, issues, cleaned


def _alternate_source_read_issues(cleaned):
    """Reject file-read control sequences outside the audited input grammar."""
    issues = []
    for match in re.finditer(r"\\([A-Za-z@]+)", cleaned):
        command = match.group(1)
        lowered = command.lower()
        if (
            ("input" in lowered or "include" in lowered)
            and lowered not in {"input", "include"}
        ) or lowered in {"openin", "read", "readline", "newread"}:
            issues.append(
                "prohibited alternate source-read command: \\%s" % command
            )
    if re.search(r"\\csname(?![A-Za-z@])", cleaned, re.I):
        issues.append(
            "prohibited dynamic source-read/control-sequence construction"
        )
    return issues


def _declared_input_issues(text, origin, contents, allowed_local_inputs):
    issues = []
    origin_dir = posixpath.dirname(origin)
    without_comments = _strip_tex_comments(text)
    issues.extend(_alternate_source_read_issues(without_comments))
    for match in re.finditer(
        r"\\(input|include)\b",
        without_comments,
        re.I,
    ):
        remainder = without_comments[match.end() :]
        argument = re.match(r"\s*\{([^}]*)\}", remainder, re.S)
        if argument is None:
            issues.append(
                "declared source dependency uses prohibited unbraced syntax: %s"
                % match.group(0)
            )
            continue
        target = argument.group(1)
        target = target.strip()
        if (
            not target
            or "\\" in target
            or target.startswith("/")
            or re.match(r"^[A-Za-z]:", target)
        ):
            issues.append(
                "declared source dependency is absolute or malformed: %s"
                % target
            )
            continue
        resolved = posixpath.normpath(posixpath.join(origin_dir, target))
        if not posixpath.splitext(resolved)[1]:
            resolved += ".tex"
        if resolved.startswith("../") or resolved not in contents:
            issues.append(
                "declared source dependency is absent or escapes package: %s"
                % target
            )
        elif resolved not in allowed_local_inputs:
            issues.append(
                "declared source dependency is not package-approved: %s"
                % resolved
            )
    return issues


def validate_source_package_bytes(
    archive_bytes,
    manifest,
    profile,
    *,
    root=ROOT,
    source_blobs=None,
):
    """Return deterministic issues for one archive, manifest, and profile."""
    root = pathlib.Path(root)
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
    expected_roles = {
        expected_rc: "build-driver",
        expected_main: "entry-point",
        expected_compat: "compatibility-input",
        expected_bib: "bibliography-owner",
    }
    expected_epoch = (
        manifest.get("source_date_epoch") if isinstance(manifest, dict) else None
    )
    canonical_header = (
        len(archive_bytes) >= 10
        and archive_bytes[0:4] == b"\x1f\x8b\x08\x00"
        and archive_bytes[8] == 2
        and archive_bytes[9] == 255
    )
    if not canonical_header:
        issues.append("archive gzip header metadata is not canonical")
    if (
        len(archive_bytes) < 8
        or not isinstance(expected_epoch, int)
        or int.from_bytes(archive_bytes[4:8], "little") != expected_epoch
    ):
        issues.append("archive gzip mtime differs from source epoch")
    if not canonical_header:
        return issues
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
                if member.mtime != expected_epoch:
                    issues.append(
                        "archive member mtime differs from source epoch: %s"
                        % member.name
                    )
            names = [member.name for member in members]
    except (EOFError, OSError, tarfile.TarError) as exc:
        return ["archive load failed: %s" % exc]

    if (
        isinstance(expected_epoch, int)
        and names == expected_names
        and all(name in contents for name in expected_names)
    ):
        canonical = io.BytesIO()
        with gzip.GzipFile(
            fileobj=canonical,
            mode="wb",
            filename="",
            mtime=expected_epoch,
        ) as compressed:
            with tarfile.open(
                fileobj=compressed,
                mode="w",
                format=tarfile.USTAR_FORMAT,
            ) as rebuilt:
                for name in expected_names:
                    payload = contents[name]
                    member = tarfile.TarInfo(name)
                    member.size = len(payload)
                    member.mode = 0o644
                    member.uid = 0
                    member.gid = 0
                    member.uname = ""
                    member.gname = ""
                    member.mtime = expected_epoch
                    rebuilt.addfile(member, io.BytesIO(payload))
        if archive_bytes != canonical.getvalue():
            issues.append(
                "archive is not the exact canonical USTAR byte encoding"
            )

    if names != expected_names:
        issues.append(
            "archive members must be exact and sorted: expected %r, got %r"
            % (expected_names, names)
        )
    expected_manifest_fields = {
        "schema",
        "artifact_id",
        "source_commit",
        "source_tree",
        "independently_reviewed_equivalent_source_commit",
        "independently_reviewed_equivalent_source_tree",
        "source_tree_equivalence",
        "source_date_epoch",
        "archive",
        "entry_point",
        "build_workdir",
        "publication_profile_sha256",
        "toolchain_lock_sha256",
        "tex_live_dependencies",
        "compatibility_inputs",
        "members",
    }
    if set(manifest) != expected_manifest_fields:
        issues.append("manifest schema fields are incomplete or unexpected")
    if manifest.get("schema") != "orthemology-source-manifest-v1":
        issues.append("manifest schema identity differs")
    expected_archive_record = {
        "path": "artifacts/%s.source.tar.gz" % artifact_id,
        "sha256": _sha(archive_bytes),
        "format": "tar-gzip-ustar",
    }
    if manifest.get("archive") != expected_archive_record:
        issues.append("archive path, hash, or format does not match manifest")
    if manifest.get("entry_point") != expected_main:
        issues.append("manifest entry point differs")
    if manifest.get("build_workdir") != "publication/latex/%s" % artifact_id:
        issues.append("manifest build workdir differs")
    profile_path = root / "docs" / "publication-profile.yaml"
    lock_path = root / TOOLCHAIN_LOCK_OWNER
    if manifest.get("publication_profile_sha256") != _sha(
        profile_path.read_bytes()
    ):
        issues.append("manifest publication profile hash differs from owner")
    if manifest.get("toolchain_lock_sha256") != _sha(lock_path.read_bytes()):
        issues.append("manifest toolchain lock hash differs from owner")
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
            "role": expected_roles[name],
        }
        for name in expected_names
        if name in contents
    ]
    if rows != expected_rows:
        issues.append("manifest member hashes or metadata do not match archive")

    owner_inputs = {
        expected_rc: root.joinpath(LATEXMKRC_OWNER).read_bytes(),
        expected_compat: root.joinpath(PDFTEX_COMPAT_OWNER).read_bytes(),
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
        root.joinpath(TOOLCHAIN_LOCK_OWNER).read_text(encoding="utf-8")
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

    main_declared, package_issues, main_without_comments = (
        _package_declarations(main, "usepackage")
    )
    issues.extend(package_issues)
    main_require_declared, main_require_issues, _ = _package_declarations(
        main,
        "RequirePackage",
    )
    issues.extend(main_require_issues)
    if main_require_declared:
        issues.append(
            "main package declarations must use the audited usepackage command"
        )
    compatibility_text = contents.get(expected_compat, b"").decode(
        "utf-8", errors="replace"
    )
    (
        compatibility_declared,
        compatibility_package_issues,
        _compatibility_without_comments,
    ) = _package_declarations(compatibility_text, "RequirePackage")
    issues.extend(compatibility_package_issues)
    compatibility_use_declared, compatibility_use_issues, _ = (
        _package_declarations(compatibility_text, "usepackage")
    )
    issues.extend(compatibility_use_issues)
    if compatibility_use_declared:
        issues.append(
            "compatibility package declarations must use RequirePackage"
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
        main_without_comments,
        re.I,
    ):
        issues.append("shell escape is prohibited")
    if re.search(
        r"\\(?:usepackage\{fontspec\}|setmainfont|setsansfont|setmonofont)",
        main_without_comments,
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

    if source_blobs is None:
        try:
            source_blobs = {
                expected_main: _git_blob(
                    root,
                    manifest.get("source_commit"),
                    expected_main,
                ),
                expected_bib: _git_blob(
                    root,
                    manifest.get("source_commit"),
                    expected_bib,
                ),
            }
        except (OSError, ValueError) as exc:
            issues.append(str(exc))
            source_blobs = {}
    for source_path in (expected_main, expected_bib):
        if contents.get(source_path) != source_blobs.get(source_path):
            issues.append(
                "package differs from source commit materialization: %s"
                % source_path
            )

    allowed_local_inputs = {expected_compat}
    issues.extend(
        _declared_input_issues(
            main,
            expected_main,
            contents,
            allowed_local_inputs,
        )
    )
    issues.extend(
        _declared_input_issues(
            compatibility_text,
            expected_compat,
            contents,
            allowed_local_inputs,
        )
    )
    rc_text = contents.get(expected_rc, b"").decode(
        "utf-8", errors="replace"
    )
    rc_inputs = re.findall(r"\\input\{([^}]+)\}", rc_text)
    if rc_inputs != ["pdftex-unicode-compat.tex"]:
        issues.append(
            "declared source dependency in .latexmkrc is not exact: %r"
            % rc_inputs
        )

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
            archive_path.read_bytes(),
            manifest,
            profile,
            root=root,
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
