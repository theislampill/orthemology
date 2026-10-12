#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p downloads receipts cache
if [ ! -x lean-4.19.0-linux/bin/lean ]; then
  curl --fail --location --retry 2 https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst -o downloads/lean-4.19.0-linux.tar.zst
  echo '6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe  downloads/lean-4.19.0-linux.tar.zst' | sha256sum -c -
  tar --zstd -xf downloads/lean-4.19.0-linux.tar.zst
fi
export PATH="$PWD/lean-4.19.0-linux/bin:$PATH"
export XDG_CACHE_HOME="$PWD/cache"
if [ ! -d mathlib4/.git ]; then
  git clone https://github.com/leanprover-community/mathlib4.git mathlib4
fi
git -C mathlib4 checkout --detach c44e0c8ee63ca166450922a373c7409c5d26b00b
lake update
./verify.sh
