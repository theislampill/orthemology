# Offline safe extraction and package verification

First compare the ZIP SHA-256 to the trusted external READ_FIRST/validation receipt. A replaced ZIP plus replaced hashes does not establish authenticity. These commands validate packaging and declared relationships only; they do not rerun science, source reading, Lean, or a metaphysical proof.

## Safe extraction into a new directory

Pass the archive filename, trusted SHA-256 from the external guide, and a NEW output directory:

```sh
python3 -B - ARCHIVE.zip TRUSTED_SHA256 NEW_DIRECTORY <<'PY'
import hashlib, pathlib, sys, tempfile, zipfile, subprocess
archive=pathlib.Path(sys.argv[1]); expected=sys.argv[2]; destination=pathlib.Path(sys.argv[3])
assert hashlib.sha256(archive.read_bytes()).hexdigest()==expected, 'ZIP digest mismatch'
name='T20_Sourcehood_Explanation_and_Redundancy_Intermediate_Checkpoint_20261009'
with zipfile.ZipFile(archive) as z:
    helper=z.read(name+'/PACKING/safe_extract.py')
with tempfile.TemporaryDirectory(prefix='t20-extractor-') as t:
    p=pathlib.Path(t)/'safe_extract.py'; p.write_bytes(helper)
    subprocess.run([sys.executable,'-B',str(p),str(archive),str(destination)],check=True)
PY
```

The helper rejects duplicate members, traversal/absolute/backslash paths, symlinks, multiple roots, wrong manifests, unexpected or missing files and altered payload bytes before creating the destination. It refuses to overwrite an existing destination. It does not execute archive research code.

## Verify the extracted packet

Replace `EXTRACTED_ROOT` with the single named directory beneath NEW_DIRECTORY:

```sh
python3 -B EXTRACTED_ROOT/PACKING/check_manifest.py
python3 -B EXTRACTED_ROOT/PACKING/integrity_controls.py ARCHIVE.zip
python3 -B EXTRACTED_ROOT/PACKING/binding_controls.py
python3 -B EXTRACTED_ROOT/PACKING/check_manifest.py
```

The first and last commands must print `status: PASS`. The two negative-control scripts must print PASS for expected rejections. They create and remove disposable temporary copies; their outputs are not new empirical/scientific evidence. External omitted source bodies and prior archives are not required to run these portable checks.

Existing component checksum/verification files record their original environments and earlier research claims. Their source bodies may be intentionally absent here and their historical revision relationships may differ from current paths. Use the normalized dependency registry rather than rewriting or blindly replaying those records. No scientific replay plan exists for this preservation-only increment.
