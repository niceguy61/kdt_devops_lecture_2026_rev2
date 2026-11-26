#!/usr/bin/env bash
# 전체 빌드: ./build/build.sh week1 day1   (day 생략 시 해당 주 전체)
set -euo pipefail
cd "$(dirname "$0")/.."
WEEK=${1:-week1}; DAY=${2:-}
W=${WEEK#week}
if [[ "$WEEK" == appendix ]]; then python3 build/build_book.py appendix; python3 build/build_github.py appendix; exit 0; fi   # 부록: ./build/build.sh appendix
# 1) 다이어그램
for f in diagrams/w${W}d*.py; do
  d=$(basename "$f" .py); [[ -n "$DAY" && "$d" != "w${W}d${DAY#day}" ]] && continue
  python3 "$f"
done
# 2) PDF 이북
if [[ -n "$DAY" ]]; then python3 build/build_book.py "$WEEK" --days "$DAY"; else python3 build/build_book.py "$WEEK"; fi
# 3) PPTX (일차별) → 저장소/downloads/pptx
mkdir -p ../downloads/pptx ../downloads/pdf
for y in src/$WEEK/day*/slides.yaml; do
  d=$(basename "$(dirname "$y")"); [[ -n "$DAY" && "$d" != "$DAY" ]] && continue
  python3 -c "import yaml,json,sys; json.dump(yaml.safe_load(open('$y')),open('/tmp/_s.json','w'),ensure_ascii=False)"
  node build/build_slides.js /tmp/_s.json "../downloads/pptx/$WEEK-$d.pptx"
  zip -dq "../downloads/pptx/$WEEK-$d.pptx" "*/" 2>/dev/null || true   # 폴더 항목 제거 (클라우드 열기 오류 방지)
done
# 4) GitHub
python3 build/build_github.py "$WEEK"
