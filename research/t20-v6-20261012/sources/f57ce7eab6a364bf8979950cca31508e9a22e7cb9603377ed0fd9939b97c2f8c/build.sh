#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v pdflatex >/dev/null || { echo 'Missing pdflatex and TeX Live packages.' >&2; exit 1; }
command -v pandoc >/dev/null || { echo 'Missing pandoc (assessment PDF).' >&2; exit 1; }
mkdir -p build
name=information-composition-and-self-revision-v5
for pass in 1 2; do
 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$name.tex" > "build/main-pass-$pass.stdout"
done
pandoc assessment/review-and-preservation.md --standalone --variable fontsize=11pt --variable papersize=a4 --variable geometry:margin=0.85in --include-in-header=assessment/header.tex --to=latex -o build/review-and-preservation.tex
for pass in 1 2; do
 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build build/review-and-preservation.tex > "build/assessment-pass-$pass.stdout"
done
if grep -E 'Overfull|undefined|multiply defined' "build/$name.log" build/review-and-preservation.log; then
 echo 'Unresolved layout/reference warning: inspect before delivery.' >&2; exit 1
fi
printf 'BUILD_PASS\n'
