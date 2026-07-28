#!/usr/bin/env python3
"""Provision and verify the exact PDF infrastructure used by validate.yml."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
POPPLER_LOCK = ROOT / "publication" / "poppler-linux-64.explicit.txt"
POPPLER_LOCK_SHA256 = (
    "bc1b26e6a386d853fd6e07225bb3b0b7a17a2a19b2ed51b5aaacedb3597ec6c3"
)
MICROMAMBA_URL = "https://github.com/mamba-org/micromamba-releases/releases/download/2.8.1-0/micromamba-linux-64"
MICROMAMBA_SHA256 = (
    "9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82"
)
TEX_IMAGE = "texlive/texlive@sha256:ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51"
TEX_MANIFEST_DIGEST = (
    "sha256:ccf0168bb3dc1e5ba18094131ebb57177f90eca37ab2727bc2d2afb54ad60a51"
)
TEX_CONFIG_DIGEST = (
    "sha256:58b5c7718b4fd239c651873cd267b6c7c82caa5d9a25fe22845d1b8720fff6b1"
)
TEX_PLATFORM = "linux/amd64"
POPPLER_VERSION = "25.07.0"
POPPLER_PACKAGE_URL = (
    "https://conda.anaconda.org/conda-forge/linux-64/"
    "poppler-25.07.0-h13eef12_1.conda"
)
POPPLER_PACKAGE_SHA256 = (
    "a45c9c35808c44d817209af859d2e9d90b89c72f8cd8fcea20163ee774583ed8"
)


class InfrastructureError(RuntimeError):
    """Raised when exact infrastructure cannot be established."""


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def explicit_lock_entries(text: str) -> list[tuple[str, str]]:
    rows = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not rows or rows[0] != "@EXPLICIT":
        raise InfrastructureError("Poppler lock must begin with @EXPLICIT")
    pattern = re.compile(
        r"^(https://conda\.anaconda\.org/conda-forge/"
        r"(?:linux-64|noarch)/[^#]+)#([0-9a-f]{64})$"
    )
    entries: list[tuple[str, str]] = []
    for row in rows[1:]:
        match = pattern.fullmatch(row)
        if not match:
            raise InfrastructureError(
                "Poppler lock row lacks an exact conda-forge URL and SHA-256"
            )
        entries.append((match.group(1), match.group(2)))
    if len(entries) != 61 or len(set(entries)) != 61:
        raise InfrastructureError("Poppler lock must contain 61 unique packages")
    if entries.count((POPPLER_PACKAGE_URL, POPPLER_PACKAGE_SHA256)) != 1:
        raise InfrastructureError(
            "Poppler lock must contain exactly poppler 25.07.0 h13eef12_1"
        )
    return entries


def verify_poppler_lock() -> None:
    observed_lock = sha256_file(POPPLER_LOCK)
    if observed_lock != POPPLER_LOCK_SHA256:
        raise InfrastructureError(
            "Poppler lock SHA-256 mismatch: expected %s, got %s"
            % (POPPLER_LOCK_SHA256, observed_lock)
        )
    explicit_lock_entries(POPPLER_LOCK.read_text(encoding="utf-8"))


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
        check=False,
    )
    if result.returncode:
        detail = (result.stdout or "") + (result.stderr or "")
        raise InfrastructureError(
            "command failed (%d): %s\n%s"
            % (result.returncode, " ".join(command), detail.strip())
        )
    return result


def provision_linux_poppler() -> pathlib.Path:
    verify_poppler_lock()
    runner_temp = pathlib.Path(
        os.environ.get("RUNNER_TEMP", tempfile.gettempdir())
    )
    micromamba = runner_temp / "orthemology-micromamba-2.8.1-0"
    download = micromamba.with_suffix(".download")
    prefix = runner_temp / "orthemology-poppler-25.07.0"
    if micromamba.exists() or download.exists() or prefix.exists():
        raise InfrastructureError(
            "fresh CI provisioning refuses a pre-existing micromamba or Poppler path"
        )
    urllib.request.urlretrieve(MICROMAMBA_URL, download)
    observed = sha256_file(download)
    if observed != MICROMAMBA_SHA256:
        raise InfrastructureError(
            "micromamba SHA-256 mismatch: expected %s, got %s"
            % (MICROMAMBA_SHA256, observed)
        )
    download.replace(micromamba)
    micromamba.chmod(
        micromamba.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )
    run(
        [
            str(micromamba),
            "create",
            "--yes",
            "--no-rc",
            "--prefix",
            str(prefix),
            "--file",
            str(POPPLER_LOCK),
        ]
    )
    binary_dir = prefix / "bin"
    github_path = os.environ.get("GITHUB_PATH")
    if not github_path:
        raise InfrastructureError("GITHUB_PATH is required during CI provisioning")
    with open(github_path, "a", encoding="utf-8", newline="\n") as stream:
        stream.write(str(binary_dir) + "\n")
    return binary_dir


def verify_poppler(binary_dir: pathlib.Path | None = None) -> dict[str, str]:
    versions: dict[str, str] = {}
    for tool in ("pdfinfo", "pdftoppm", "pdffonts"):
        executable = (
            str(binary_dir / tool)
            if binary_dir is not None
            else shutil.which(tool)
        )
        if not executable:
            raise InfrastructureError("%s is not available" % tool)
        result = run([executable, "-v"], capture=True)
        output = (result.stdout or "") + (result.stderr or "")
        match = re.search(r"\bversion\s+([0-9]+\.[0-9]+\.[0-9]+)\b", output)
        if not match or match.group(1) != POPPLER_VERSION:
            raise InfrastructureError(
                "%s version differs from %s: %s"
                % (tool, POPPLER_VERSION, output.strip())
            )
        versions[tool] = match.group(1)
    return versions


def verify_tex_image() -> dict[str, object]:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run(["docker", "pull", TEX_IMAGE])
    result = run(["docker", "image", "inspect", TEX_IMAGE], capture=True)
    records = json.loads(result.stdout)
    if len(records) != 1:
        raise InfrastructureError("TeX image inspection returned an invalid record")
    record = records[0]
    platform = "%s/%s" % (record.get("Os"), record.get("Architecture"))
    if platform != TEX_PLATFORM:
        raise InfrastructureError("TeX image platform differs from linux/amd64")
    repo_digests = record.get("RepoDigests") or []
    if not any(item.endswith("@" + TEX_MANIFEST_DIGEST) for item in repo_digests):
        raise InfrastructureError("TeX image manifest digest mismatch")
    manifest_result = run(
        ["docker", "manifest", "inspect", TEX_IMAGE],
        capture=True,
    )
    manifest = json.loads(manifest_result.stdout)
    config_digest = (manifest.get("config") or {}).get("digest")
    if config_digest != TEX_CONFIG_DIGEST:
        raise InfrastructureError("TeX image configuration digest mismatch")
    return {
        "config_digest": config_digest,
        "manifest_digest": TEX_MANIFEST_DIGEST,
        "platform": platform,
    }


def main() -> int:
    verify_poppler_lock()
    binary_dir = None
    if os.environ.get("GITHUB_ACTIONS") == "true":
        if sys.platform != "linux":
            raise InfrastructureError("CI infrastructure provisioning requires Linux")
        binary_dir = provision_linux_poppler()
    poppler = verify_poppler(binary_dir)
    tex = verify_tex_image()
    print(
        json.dumps(
            {
                "micromamba_sha256": MICROMAMBA_SHA256,
                "poppler": poppler,
                "poppler_lock_sha256": sha256_file(POPPLER_LOCK),
                "tex": tex,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InfrastructureError as error:
        print("[FAIL] %s" % error, file=sys.stderr)
        raise SystemExit(1)
