from pathlib import Path
import subprocess,json,platform,hashlib,time
out=Path('private-locator:0b3b275c067407d31400');out.mkdir(parents=True,exist_ok=True)
commands=[('local_tools',['bash','-lc','for t in lean lake elan docker podman; do command -v "$t" || true; done; uname -a; find private-locator:e80743debc9cc1395252 /opt /usr/local /mnt/data /usr/bin /var/cache -type f \\( -name lean -o -name lake -o -name "lean-4.19*" -o -name "*.olean" -o -name "elan*.deb" \\) 2>/dev/null | head -150']),('lean_release',['curl','-fIL','--connect-timeout','5','--max-time','12','https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst']),('official_release_redirect',['curl','-fIL','--connect-timeout','5','--max-time','12','https://releases.lean-lang.org/lean4/v4.19.0/lean-4.19.0-linux.tar.zst']),('mathlib_source',['curl','-fL','--connect-timeout','5','--max-time','12','https://raw.githubusercontent.com/leanprover-community/mathlib4/c44e0c8ee63ca166450922a373c7409c5d26b00b/lean-toolchain']),('source_bootstrap',['git','ls-remote','https://github.com/leanprover/lean4.git','refs/tags/v4.19.0']),('offline_cache',['bash','-lc','ls -ld ~/.elan/toolchains ~/.lake ~/.cache/mathlib private-locator:99992ba26e97a69e69ee private-locator:22a31bd0e117f015003e /var/cache/apt/archives /mnt/data/* 2>&1; find / -maxdepth 3 -type d \\( -name .elan -o -name .lake -o -name "lean-4.19*" \\) 2>/dev/null'])]
for label,cmd in commands:
 t=time.time()
 try:
  p=subprocess.run(cmd,capture_output=True,timeout=15); a,b,rc=p.stdout,p.stderr,p.returncode
 except subprocess.TimeoutExpired as e: a,b,rc=e.stdout or b'',e.stderr or b'',124
 (out/(label+'.stdout')).write_bytes(a);(out/(label+'.stderr')).write_bytes(b)
 (out/(label+'.json')).write_text(json.dumps({'command':cmd,'exit':rc,'seconds':time.time()-t,'stdout_sha256':hashlib.sha256(a).hexdigest(),'stderr_sha256':hashlib.sha256(b).hexdigest()},indent=2))
 print(label,rc,a.decode(errors='replace')[:500],b.decode(errors='replace')[-200:])
