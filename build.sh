#!/usr/bin/env bash
# Build LaTeX CVs and cover letters to PDF (Linux/macOS twin of build.ps1).
#
# Usage:
#   ./build.sh applications/Frontend_React        # build one folder
#   ./build.sh applications/Frontend_React/EN/cv_frontend_react_en.tex  # one file
#   ./build.sh --all                              # build all applications
#   ./build.sh --all --templates                  # all applications + templates
#   ./build.sh --clean                            # remove build artifacts everywhere
#   ./build.sh --clean applications/Frontend_React  # clean one folder
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTIFACTS=(aux log fls fdb_latexmk out synctex.gz synctex bbl blg toc lof lot nav snm vrb run.xml)

clean() {
  local target="$1" count=0
  for ext in "${ARTIFACTS[@]}"; do
    while IFS= read -r -d '' f; do rm -f "$f"; count=$((count+1)); done \
      < <(find "$target" -name "*.${ext}" -not -path "*/.git/*" -print0 2>/dev/null)
  done
  echo "Cleaned $count artifact file(s) from $target"
}

build_one() {
  local tex="$1"
  local dir name
  dir="$(dirname "$tex")"; name="$(basename "$tex")"
  echo "  Building: $name"
  if command -v latexmk >/dev/null 2>&1; then
    (cd "$dir" && latexmk -pdf -interaction=nonstopmode "$name" >/dev/null 2>&1)
  else
    (cd "$dir" && pdflatex -interaction=nonstopmode "$name" >/dev/null 2>&1 \
                && pdflatex -interaction=nonstopmode "$name" >/dev/null 2>&1)
  fi
  local pdf="${tex%.tex}.pdf"
  if [[ -f "$pdf" ]]; then echo "  OK: $(basename "$pdf")"; else echo "  FAILED: $name (no PDF produced)"; FAILED=$((FAILED+1)); fi
}

ALL=0; TEMPLATES=0; CLEAN=0; TARGET=""; FAILED=0
for arg in "$@"; do
  case "$arg" in
    --all) ALL=1 ;;
    --templates) TEMPLATES=1 ;;
    --clean) CLEAN=1 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) TARGET="$arg" ;;
  esac
done

if [[ $CLEAN -eq 1 ]]; then
  if [[ -n "$TARGET" ]]; then clean "$ROOT/$TARGET"; else clean "$ROOT/applications"; clean "$ROOT/templates"; fi
  exit 0
fi

FILES=()
if [[ -n "$TARGET" ]]; then
  path="$ROOT/$TARGET"
  [[ -e "$path" ]] || path="$TARGET"           # allow absolute paths too
  [[ -e "$path" ]] || { echo "Path not found: $TARGET" >&2; exit 1; }
  if [[ "$path" == *.tex ]]; then
    FILES+=("$path")
  else
    while IFS= read -r -d '' f; do FILES+=("$f"); done \
      < <(find "$path" -name '*.tex' -not -path "*/.git/*" -print0 | sort -z)
  fi
elif [[ $ALL -eq 1 ]]; then
  while IFS= read -r -d '' f; do FILES+=("$f"); done \
    < <(find "$ROOT/applications" -name '*.tex' -not -path "*/.git/*" -print0 | sort -z)
  if [[ $TEMPLATES -eq 1 ]]; then
    while IFS= read -r -d '' f; do FILES+=("$f"); done \
      < <(find "$ROOT/templates" -name '*.tex' -not -path "*/.git/*" -print0 | sort -z)
  fi
else
  grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0
fi

[[ ${#FILES[@]} -gt 0 ]] || { echo "No .tex files found."; exit 0; }
echo; echo "Building ${#FILES[@]} file(s)..."; echo
for f in "${FILES[@]}"; do build_one "$f"; done
echo; echo "Done. ($FAILED failure(s))"
[[ $FAILED -eq 0 ]]
