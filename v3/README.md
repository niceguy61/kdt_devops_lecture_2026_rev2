# v3 — 강의 콘텐츠 원고와 빌드 파이프라인

하나의 원고에서 **PDF 이북**, **PPTX 슬라이드**, **GitHub용 Markdown**을 함께 만듭니다.
과정 기준표는 [CURRICULUM.md](CURRICULUM.md)를 보세요.

## 폴더 구조

```
v3/
├── CURRICULUM.md            5주 커리큘럼 기준표
├── src/weekN/dayM/          원고 (단일 원본)
│   ├── README.md            일차 개요 (front matter: title, subtitle)
│   ├── lesson-0X.md         교시별 본문 → 이북 · GitHub
│   └── slides.yaml          슬라이드 정의 → PPTX (발표자 노트 포함)
├── src/appendix/            부록 A · 도구 설치 가이드
├── diagrams/wNdM.py         다이어그램 코드 (HTML/CSS 레이아웃 → PNG)
├── assets/weekN/dayM/       생성된 그림 (+ _src/ 그림 원본 HTML)
├── build/                   빌드 도구
└── (결과물은 저장소 최상위로) ../weekN/ · ../appendix/ · ../README.md (GitHub md)
                             ../downloads/pdf/ · ../downloads/pptx/ (PDF · PPTX)
```

## 원고 작성 규칙

- 교시 제목: `# 1교시 · 제목`
- 박스: `!!! 종류 "제목"` 다음 줄부터 4칸 들여쓰기
  - `goal` 이번 시간에 할 일 · `key` 핵심 · `tip` 팁 · `example` 예시 · `analogy` 비유
  - `warn` 주의 · `myth` 오해 바로잡기 · `term` 용어 · `quiz` 확인 문제 · `diary` 배움일기
  - 퀴즈 정답은 `quiz` 박스 안에 `??? answer "정답"`
- 그림: `![캡션 — 부가 설명](../../../assets/week1/day1/파일.png)` (캡션의 `—` 앞부분이 그림 번호 옆에 표시됨)
- 슬라이드 타입: `cover` `agenda` `section` `image` `table` `cards` `statement` `compare` `steps` `quiz` `summary`

## 다이어그램 원칙

- 화살표를 좌표로 찍지 않습니다. 박스와 화살표를 같은 flex 줄 안에 배치해 레이아웃 엔진이 정렬합니다.
- 노드-엣지 그래프가 필요하면 `dk.gv()`(Graphviz 자동 레이아웃)를 씁니다.
- AWS 아이콘은 `reference/icons`의 공식 패키지를, 일반 아이콘은 Lucide를 씁니다.
- 렌더링 후 흰 여백을 자동으로 잘라 이북·슬라이드에서 빈 공간이 생기지 않게 합니다.

## 빌드

필요한 것: Python 3 (`weasyprint markdown pymdown-extensions pyyaml pillow matplotlib`), Node.js (`pptxgenjs react react-dom react-icons sharp`), Google Chrome, Pretendard 폰트

```bash
node build/icons.js                 # 아이콘 SVG 내보내기 (최초 1회)
bash build/build.sh week1 day1      # 다이어그램 → PDF → PPTX → GitHub
bash build/build.sh week1           # 1주차 전체
```

| 결과물 | 위치 |
|---|---|
| PDF 이북 (188×257mm) | `../downloads/pdf/week1.pdf` |
| 슬라이드 (16:9, 발표자 노트 포함) | `../downloads/pptx/week1-day1.pptx` |
| GitHub용 Markdown | `../week1/day1/` (저장소 최상위) |

PPTX 글꼴은 Windows·Office 기본 글꼴인 **맑은 고딕**을 씁니다. PDF는 Pretendard로 렌더링합니다.
