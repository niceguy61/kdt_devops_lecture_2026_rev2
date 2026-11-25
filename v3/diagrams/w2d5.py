"""2주차 5일차 다이어그램. 실행: python3 diagrams/w2d5.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week2" / "day5"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def code(txt, w=None, fs=17):
    ws = f"width:{w}px;" if w else ""
    return f'<div style="{ws}background:#0F1E2E;color:#E2E8F0;border-radius:10px;padding:12px 16px;font-size:{fs}px;{MONO};white-space:pre;line-height:1.45">{txt}</div>'


# 1. docker run → compose.yaml
pairs = [("violet", "--name db", "services:\n  db:"),
         ("teal", "-e POSTGRES_PASSWORD=\"$DB_PASSWORD\"", "environment:\n  POSTGRES_PASSWORD: ${DB_PASSWORD:?…}"),
         ("green", "-v devmart-db:/var/lib/postgresql", "volumes:\n  - db-data:/var/lib/postgresql"),
         ("orange", "until pg_isready …; do sleep 1; done", "healthcheck: + depends_on:\n  condition: service_healthy"),
         ("slate", "docker network create devmart-net\n--network devmart-net", "(적지 않는다)\n→ devmart_default 자동 생성")]
rows = "".join(f'''<div class="row c" style="gap:14px"><div style="width:10px;align-self:stretch;border-radius:5px;background:var(--{c})"></div>
{code(a.replace("<", "&lt;"), 560, 17)}{icon("ArrowRight",30,c,2.5)}{code(b, None, 17).replace('<div style="', '<div class="grow" style="', 1)}</div>''' for c, a, b in pairs)
R("w2d5-run-to-compose", f'''<div class="row c" style="gap:14px"><div style="width:10px"></div><div class="tag" style="width:560px">어제 — docker run 옵션 (명령형)</div><div style="width:30px"></div><div class="tag grow">오늘 — compose.yaml (선언형)</div></div>
<div class="col" style="gap:10px">{rows}</div>
<div class="row" style="gap:14px">{note("violet", "서비스 이름 = <b style='color:var(--navy)'>DNS 이름</b> · db, catalog-api, web")}{note("slate", "<b style='color:var(--navy)'>-p → ports</b> · API와 DB에는 적지 않는다")}{note("green", "순서는 <b style='color:var(--navy)'>depends_on</b>을 보고 Compose가 정한다")}</div>''', w=1500)

# 2. 변경 반영
ch = [("FileCode", "violet", "web/index.html", "바인드 마운트", "브라우저 새로 고침", "없음"),
      ("Settings", "teal", "compose.yaml 환경 변수", "컨테이너 설정", "docker compose up -d", "그 서비스만 다시 생성"),
      ("Package", "orange", "catalog-api/app.py", "이미지 안", "docker compose up -d --build", "다시 빌드 → 그 서비스만"),
      ("Database", "red", "db/init/01-schema.sql", "빈 볼륨일 때만 실행", "down -v → up -d", "데이터 처음부터")]
cr = "".join(f'''<div class="row c" style="gap:12px"><div class="card row c" style="width:400px;gap:12px;padding:12px 16px;border-color:var(--{c})">{ic(i,c,52)}<div class="col" style="gap:2px"><b style="font-size:19px;color:var(--navy);{MONO}">{f}</b><span style="font-size:16px;color:var(--slate)">{w}</span></div></div>
{arrow(size=30)}<div style="width:420px;background:#0F1E2E;color:#8FD6A8;border-radius:10px;padding:14px 16px;font-size:18px;{MONO}">{cmd}</div>{arrow(size=30)}
<div class="grow" style="background:var(--{c}-l);border-radius:10px;padding:14px 16px;font-size:18px;color:var(--navy);font-weight:700">{r}</div></div>''' for i, c, f, w, cmd, r in ch)
R("w2d5-change-flow", f'''<div class="row c" style="gap:12px"><div class="tag" style="width:400px">무엇을 고쳤나 · 어디에 있나</div><div style="width:30px"></div><div class="tag" style="width:420px">반영하는 명령</div><div style="width:30px"></div><div class="tag grow">Compose가 하는 일</div></div>
<div class="col" style="gap:12px">{cr}</div>
<div class="row" style="gap:14px">{note("orange", "코드를 고치고 <b style='color:var(--navy)'>--build</b>를 빠뜨리면 옛 이미지 그대로")}{note("slate", "API를 다시 만든 뒤 502 → <b style='color:var(--navy)'>docker compose restart web</b>")}</div>''', w=1600)


# helper for git graph (SVG)
def svg_graph(w, h, inner):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="font-family:Pretendard">{inner}</svg>'


def dot(x, y, c, label="", below=True, r=16):
    ty = y + 42 if below else y - 28
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="#fff" stroke-width="4"/>' + (f'<text x="{x}" y="{ty}" font-size="17" text-anchor="middle" fill="#334155">{label}</text>' if label else "")


NAVY, TEAL, ORANGE, VIOLET, GREEN, RED, SLATE = "#0F2A44", "#00808F", "#C8651B", "#6A4FB3", "#2E7D4F", "#B83227", "#64748B"

# 3. 브랜치
g = f'''<line x1="80" y1="90" x2="1260" y2="90" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>
<path d="M 380 90 C 440 90 440 230 500 230 L 820 230 C 880 230 880 90 940 90" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round"/>
{dot(140,90,NAVY,"",)}{dot(260,90,NAVY,"")}{dot(380,90,NAVY,"compose.yaml", False)}
{dot(560,230,TEAL,"웹: 바닥글 추가")}{dot(740,230,TEAL,"(리뷰 반영)")}
{dot(940,90,NAVY,"병합", False,20)}{dot(1100,90,NAVY,"")}
<rect x="1150" y="58" width="110" height="40" rx="8" fill="{NAVY}"/><text x="1205" y="85" font-size="20" font-weight="800" text-anchor="middle" fill="#fff">main</text>
<rect x="560" y="280" width="230" height="40" rx="8" fill="{TEAL}"/><text x="675" y="307" font-size="19" font-weight="800" text-anchor="middle" fill="#fff">feature/footer</text>
<text x="415" y="210" font-size="18" fill="{TEAL}" font-weight="700" text-anchor="end">git switch -c</text>
<text x="880" y="185" font-size="18" fill="{NAVY}" font-weight="700">git merge</text>'''
R("w2d5-branch", f'''<div class="card" style="padding:18px">{svg_graph(1300, 340, g)}</div>
<div class="row" style="gap:14px">{note("slate", "<b style='color:var(--navy)'>main</b> = 언제나 동작하는 원고")}{note("teal", "<b style='color:var(--navy)'>브랜치</b> = 마지막 커밋을 가리키는 이름표 · 연습장")}{note("orange", "<b style='color:var(--navy)'>짧게, 자주</b> — 하루~이틀 안에 합친다")}</div>''', w=1400)

# 4. PR 흐름
st = [("GitBranch", "teal", "브랜치", "switch -c"), ("GitCommitHorizontal", "teal", "커밋 · push", "push -u origin"),
      ("GitPullRequest", "violet", "PR 열기", "gh pr create"), ("MessageSquare", "orange", "리뷰", "코멘트 · 변경 요청"),
      ("PenLine", "orange", "수정 push", "같은 브랜치에"), ("CircleCheck", "green", "승인", "Approve"),
      ("GitMerge", "navy", "병합", "merge --squash"), ("Trash2", "slate", "브랜치 삭제", "--delete-branch")]
sc = []
for k, (i, c, t, d) in enumerate(st):
    sc.append(f'<div class="card center" style="width:150px;gap:6px;padding:14px 6px;border-color:var(--{c})">{ic(i,c,58)}<b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">{d}</span></div>')
    if k < len(st) - 1:
        sc.append(arrow(size=22))
R("w2d5-pr-flow", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(sc)}</div>
<div class="row c" style="gap:12px;justify-content:center"><div style="background:var(--orange-l);border:2px dashed var(--orange);border-radius:30px;padding:8px 22px;font-size:18px;color:var(--navy)">{icon("RefreshCw",22,"orange",2.2)} 리뷰 ↔ 수정은 승인될 때까지 반복 — PR은 자동 갱신</div></div>
<div class="row" style="gap:14px">{note("violet", "<b style='color:var(--navy)'>PR</b> = 결재 요청서 · 대화와 기록이 남는다")}{note("red", "내 PR은 <b style='color:var(--navy)'>내가 승인할 수 없다</b>")}{note("teal", "3주차: PR마다 <b style='color:var(--navy)'>CI</b>가 자동 테스트")}</div>''', w=1600)

# 5. 충돌
g2 = f'''<line x1="60" y1="70" x2="900" y2="70" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>
<path d="M 200 70 C 260 70 260 190 320 190 L 520 190" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round"/>
<path d="M 200 70 C 260 70 260 -40 320 -40" fill="none" stroke="none"/>
{dot(120,70,NAVY,"")}{dot(200,70,NAVY,"&lt;h1&gt;DevMart", False)}
{dot(420,70,NAVY,"PR 병합: DevMart 🛒", False, 18)}
{dot(420,190,ORANGE,"DevMart — 겨울 세일")}
<rect x="760" y="38" width="110" height="40" rx="8" fill="{NAVY}"/><text x="815" y="65" font-size="20" font-weight="800" text-anchor="middle" fill="#fff">main</text>
<rect x="540" y="170" width="220" height="40" rx="8" fill="{ORANGE}"/><text x="650" y="197" font-size="18" font-weight="800" text-anchor="middle" fill="#fff">feature/title-sale</text>
<path d="M 600 70 C 640 70 640 150 680 150" fill="none" stroke="{RED}" stroke-width="4" stroke-dasharray="8 6"/>
<text x="610" y="128" font-size="17" fill="{RED}" font-weight="800">git merge main</text>'''
mk = (f'<div style="background:#0F1E2E;border-radius:10px;padding:14px 16px;font-size:18px;{MONO};line-height:1.6">'
      f'<div style="color:#F5B5AE">&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</div><div style="color:#FFD8B0">    &lt;h1&gt;DevMart — 겨울 세일&lt;/h1&gt;</div>'
      f'<div style="color:#F5B5AE">=======</div><div style="color:#B9E3C9">    &lt;h1&gt;DevMart 🛒&lt;/h1&gt;</div><div style="color:#F5B5AE">&gt;&gt;&gt;&gt;&gt;&gt;&gt; main</div></div>')
R("w2d5-conflict", f'''<div class="row" style="gap:18px;align-items:stretch">
<div class="card" style="padding:14px;width:960px">{svg_graph(930, 260, g2)}</div>
<div class="col grow" style="gap:10px">{mk}<div class="row c" style="gap:8px;justify-content:center">{icon("ArrowDown",28,"slate",2.5)}<span style="font-size:17px;color:var(--slate)">양쪽 의도를 살려 고르고 표시 줄 삭제</span></div>
{code("    &lt;h1&gt;DevMart 🛒 — 겨울 세일&lt;/h1&gt;", None, 18)}</div></div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>HEAD</b> = 지금 내 브랜치 · <b style='color:var(--navy)'>main</b> = 들어오는 쪽")}{note("teal", "git add → git commit --no-edit → git push")}{note("slate", "처음부터 다시: <b style='color:var(--navy)'>git merge --abort</b>")}</div>''', w=1600)

# 6. 2주차 지도
days = [("1일차", "Laptop", "teal", "개발 환경", "WSL · Git · gh · Docker"), ("2일차", "Box", "violet", "컨테이너", "run · logs · exec · 실패 5종"),
        ("3일차", "Layers", "orange", "이미지", "Dockerfile · 캐시 · Hub"), ("4일차", "Network", "green", "볼륨·네트워크", "DB 연결 · .env · 3계층"),
        ("5일차", "GitPullRequest", "navy", "Compose·협업", "compose.yaml · PR · 충돌")]
dc = []
for k, (d, i, c, t, s) in enumerate(days):
    dc.append(f'<div class="card center grow" style="gap:6px;padding:16px 8px;border-color:var(--{c})"><div class="chip" style="font-size:15px;background:var(--{c});color:#fff">{d}</div>{ic(i,c,64)}<b style="font-size:21px;color:var(--navy)">{t}</b><span style="font-size:15px;color:var(--slate);text-align:center">{s}</span></div>')
    if k < 4:
        dc.append(arrow(size=24))
R("w2d5-week2-map", f'''<div class="row flow" style="gap:6px;align-items:center">{"".join(dc)}</div>
<div class="card" style="padding:16px 20px;gap:10px;border-color:var(--teal);background:#F4FAFB"><div class="row c" style="gap:12px">{icon("Rocket",30,"teal",2)}<b style="font-size:21px;color:var(--navy)">동료의 노트북에서도 같은 DevMart</b></div>
{code("git clone …/devops-lab.git  →  cp .env.example .env  →  docker compose up -d --build", None, 18)}</div>
<div class="row" style="gap:14px">{note("slate", "한계: <b style='color:var(--navy)'>한 대의 컴퓨터</b> · 죽으면 그대로 · 죽은 곳에도 보냄")}{note("violet", "3주차: <b style='color:var(--navy)'>Kubernetes</b> + <b style='color:var(--navy)'>GitHub Actions CI</b>")}</div>''', w=1600)
