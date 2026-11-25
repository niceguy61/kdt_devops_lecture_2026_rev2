"""3주차 2일차 다이어그램. 실행: python3 diagrams/w3d2.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week3" / "day2"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def svc(name, sub, c, i, w=200):
    return f'''<div class="card center" style="width:{w}px;gap:6px;padding:14px 10px;border-color:var(--{c})">{ic(i,c,56)}
<div style="font-size:20px;font-weight:900;color:var(--navy);{MONO}">{name}</div><div style="font-size:15px;color:var(--slate);text-align:center">{sub}</div></div>'''


def req(t, c, txt):
    return f'<div class="row c" style="gap:8px"><div style="width:16px;height:16px;border-radius:8px;background:var(--{c})"></div><span style="font-size:16px;{MONO};color:var(--navy)">{t}</span><span style="font-size:15px;color:var(--slate)">{txt}</span></div>'


# 1. 장애 전파
R("w3d2-cascade", f'''<div class="row" style="gap:14px;align-items:center">
<div class="card" style="width:330px;gap:10px;padding:16px"><div class="tag">줄 선 요청들</div>
{req("POST /api/orders","red","주문 1 — 일꾼이 기다리는 중")}
{req("POST /api/orders","orange","주문 2 — 줄 섬")}
{req("GET /api/orders","orange","주문 목록 — catalog와 상관없는데 줄 섬")}
{req("POST /api/orders","orange","주문 3 — 줄 섬")}</div>
{arrow(size=30)}
<div class="card center" style="width:280px;gap:10px;padding:16px;border-color:var(--violet)">{ic("ShoppingCart","violet",56)}<div style="font-size:21px;font-weight:900;{MONO};color:var(--navy)">order-api</div>
<div class="box" style="background:var(--red-l);color:var(--red);font-size:17px">{icon("Hourglass",22,"red",2)} 일꾼 1명 — 묶여 있음</div><div style="font-size:15px;color:var(--slate)">gunicorn 기본값</div></div>
<div class="col center" style="gap:6px">{icon("ArrowRight",34,"red",2.5)}<span style="font-size:16px;{MONO};color:var(--red);font-weight:800">기다리는 중…<br>timeout 2s / 30s</span></div>
<div class="card center" style="width:240px;gap:10px;padding:16px;border-color:var(--slate);background:var(--slate-l)">{ic("Snowflake","slate",56)}<div style="font-size:21px;font-weight:900;{MONO};color:var(--navy)">catalog-api</div><div class="chip" style="font-size:15px;background:var(--slate);color:#fff">Paused — 답 없음</div></div></div>
<div class="row" style="gap:14px">
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--orange)"><b style="font-size:20px;color:var(--navy)">타임아웃 2초</b><span style="font-size:18px">주문 2초 뒤 503 · 주문 목록 최대 2초 지연</span></div>
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--red)"><b style="font-size:20px;color:var(--red)">타임아웃 30초</b><span style="font-size:18px">주문 · <b>주문 목록까지</b> 60초 뒤 504 — 주문 서비스 전체 마비</span></div></div>
<div class="row" style="gap:14px">{note("slate", "기다리는 동안 <b style='color:var(--navy)'>부르는 쪽의 자원이 묶인다</b> — 콜센터 상담원 비유")}{note("teal", "처방: <b style='color:var(--navy)'>짧은 타임아웃</b> · 서킷 브레이커 · 벌크헤드 (4주차)")}</div>''', w=1600)

# 2. 메시지 유실
def stage(n, t, d, c, ok=True):
    return f'<div class="card center grow" style="gap:6px;padding:14px 8px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div><b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">{d}</span></div>'


flow = [stage("1", "DB에 저장", "orders: pending", "violet"), arrow(size=22), stage("2", "큐에 넣기", "LPUSH orders", "orange"), arrow(size=22),
        stage("3", "처리기가 꺼냄", "BRPOP → 큐에서 삭제", "orange"), arrow(size=22), stage("4", "처리", "WORK_SECONDS", "green"), arrow(size=22), stage("5", "완료 기록", "status = completed", "green")]
R("w3d2-message-loss", f'''<div class="row flow" style="gap:6px;align-items:center">{"".join(flow)}</div>
<div class="row" style="gap:16px;align-items:stretch">
<div class="card grow" style="gap:8px;border-color:var(--red);background:#FFF8F7"><div class="row c" style="gap:10px">{icon("Ghost",30,"red",2)}<b style="font-size:21px;color:var(--red)">유령 주문 (12번) — 1은 됐는데 2 실패</b></div>
<span style="font-size:18px">redis가 꺼져 큐에 못 넣음 → 사용자는 503, DB에는 pending</span><span style="font-size:16px;{MONO};color:var(--slate)">개선: 트랜잭셔널 아웃박스 (같은 트랜잭션에 '보낼 메시지' 저장)</span></div>
<div class="card grow" style="gap:8px;border-color:var(--red);background:#FFF8F7"><div class="row c" style="gap:10px">{icon("Skull",30,"red",2)}<b style="font-size:21px;color:var(--red)">유실 (13번) — 3 뒤 4 도중 죽음</b></div>
<span style="font-size:18px">이미 큐에서 지워짐 + 처리 안 됨 → 어디에도 없음</span><span style="font-size:16px;{MONO};color:var(--slate)">개선: 처리 중 목록으로 옮기고(LMOVE) 끝나면 확인(ack)</span></div></div>
<div class="row" style="gap:14px">{note("orange", "찾기: <b style='color:var(--navy)'>status = 'pending' AND created_at &lt; now() - 1분</b>")}{note("green", "복구: 큐에 다시 LPUSH — <b style='color:var(--navy)'>두 번 해도 괜찮은지(멱등)</b> 먼저 확인")}</div>''', w=1600)

# 3. CI 범위
pp = [("1", "커밋 · PR", "GitBranch", "teal", True), ("2", "빌드", "Hammer", "teal", True), ("3", "테스트", "FlaskConical", "teal", True),
      ("4", "보안 검사", "ShieldCheck", "slate", False), ("5", "이미지 저장", "Warehouse", "teal", True), ("6", "배포", "Rocket", "slate", False), ("7", "모니터링", "Activity", "slate", False)]
pc = []
for k, (n, t, i, c, today) in enumerate(pp):
    bg = "#fff" if today else "var(--slate-l)"
    tag = '<div class="chip" style="font-size:13px;background:var(--orange);color:#fff">오늘</div>' if today else '<div style="font-size:13px;color:var(--slate)">' + ("4주차" if n in "467" else "") + '</div>'
    pc.append(f'<div class="card center grow" style="gap:6px;padding:14px 6px;border-color:var(--{c});background:{bg}"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div>{ic(i,c,50)}<b style="font-size:18px;color:var(--navy)">{t}</b>{tag}</div>')
    if k < 6:
        pc.append(arrow(size=20))
R("w3d2-ci-scope", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(pc)}</div>
<div class="row" style="gap:14px">{note("teal", "<b style='color:var(--navy)'>CI</b> — 코드가 올라올 때마다 기계가 똑같이: PR엔 테스트 · 빌드, main엔 push까지")}{note("slate", "<b style='color:var(--navy)'>CD</b> — 창고의 이미지를 서버로 (4주차 ArgoCD)")}</div>''', w=1600)

# 4. Actions 해부
R("w3d2-actions-anatomy", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="col" style="gap:12px;width:250px">
<div class="card center" style="gap:6px;padding:14px;border-color:var(--orange)">{ic("Zap","orange",54)}<b style="font-size:20px;color:var(--navy)">이벤트</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">push · pull_request<br>workflow_dispatch · schedule</span></div>
<div class="card center" style="gap:6px;padding:14px;border-color:var(--red)">{ic("KeyRound","red",50)}<b style="font-size:19px;color:var(--navy)">시크릿</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">secrets.GITHUB_TOKEN<br>로그에 *** 로 가림</span></div></div>
<div class="col center" style="gap:4px;justify-content:center">{arrow(size=34)}<span style="font-size:15px;color:var(--slate)">깨운다</span></div>
<div style="border:3px solid var(--navy);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:12px;flex:1">
<div class="row c" style="gap:10px">{icon("FileCode",30,"navy",2)}<b style="font-size:21px;color:var(--navy);{MONO}">.github/workflows/devmart-ci.yml</b><span style="font-size:16px;color:var(--slate)">워크플로</span></div>
<div class="row" style="gap:12px">
{"".join(f'''<div class="card grow" style="gap:8px;padding:12px;border-color:var(--{c});background:var(--{c}-l)"><div class="row c" style="gap:8px">{icon("Server",22,c,2)}<b style="font-size:18px;{MONO};color:var(--navy)">{j}</b></div><span style="font-size:14px;color:var(--slate)">러너: ubuntu-latest (새 VM)</span>
{"".join(f'<div class="box" style="background:#fff;color:var(--navy);font-size:15px;{MONO};text-align:left">{s}</div>' for s in st)}</div>''' for j, c, st in [("test (×2)", "teal", ["checkout@v6", "setup-python@v6", "pip install", "pytest"]), ("compose-check", "violet", ["checkout@v6", "compose config"]), ("build (×3)", "orange", ["setup-buildx@v4", "login@v4", "metadata@v6", "build-push@v7"])])}
</div>
<div class="row c" style="gap:10px;justify-content:center"><span style="font-size:16px;color:var(--slate)">잡끼리는 동시에 · <b style="color:var(--navy)">needs:</b>로 순서 · 스텝은 차례로 · <b style="color:var(--navy)">uses:</b> = 남이 만든 액션</span></div>
</div></div>
<div class="row" style="gap:14px">{note("teal", "러너는 <b style='color:var(--navy)'>매번 새 컴퓨터</b> — 잡마다 checkout부터")}{note("red", "남의 액션은 남의 코드 — 검증된 제작자 · <b style='color:var(--navy)'>SHA 고정</b> · 최소 권한")}</div>''', w=1650)

# 5. build 잡
bs = [("ShieldCheck", "권한", "permissions:\npackages: write", "red"), ("LogIn", "로그인", "login-action@v4\nGITHUB_TOKEN", "violet"),
      ("Tags", "태그", "metadata-action@v6\nsha-7f3c2e1 · latest", "orange"), ("Hammer", "빌드 + 캐시", "build-push-action@v7\ncache type=gha", "teal"), ("Warehouse", "push", "ghcr.io/아이디/\ndevmart-서비스", "green")]
bc = []
for k, (i, t, d, c) in enumerate(bs):
    bc.append(f'<div class="card center grow" style="gap:6px;padding:14px 6px;border-color:var(--{c})">{ic(i,c,52)}<b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:14px;{MONO};color:var(--slate);white-space:pre-line;text-align:center">{d}</span></div>')
    if k < 4:
        bc.append(arrow(size=22))
R("w3d2-build-job", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(bc)}</div>
<div class="row" style="gap:16px">
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--slate)"><b style="font-size:20px;color:var(--navy)">pull_request</b><span style="font-size:18px">로그인 안 함 · <b>빌드만</b> — 검토 중인 코드는 창고에 넣지 않는다</span></div>
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--green)"><b style="font-size:20px;color:var(--green)">push (main)</b><span style="font-size:18px">로그인 · 빌드 · <b>push</b> — sha 태그 + latest</span></div></div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>sha-커밋</b> = 절대 안 바뀜 (배포 · 롤백) · <b style='color:var(--navy)'>latest</b> = 옮겨 붙음 (개발)")}{note("teal", "라벨 <b style='color:var(--navy)'>image.revision</b> = 커밋 SHA → 이 이미지는 어느 코드인가")}</div>''', w=1600)

# 6. CI 실패 읽기
fs = [("ListChecks", "1 어느 잡?", "gh pr checks", "red"), ("Footprints", "2 어느 스텝?", "gh run view --log-failed", "orange"),
      ("ArrowUpToLine", "3 마지막 에러 줄", "아래에서 위로 · ##[error] 위", "violet"), ("Laptop", "4 로컬 재현", "docker run … pytest", "teal")]
fc = []
for k, (i, t, d, c) in enumerate(fs):
    fc.append(f'<div class="card center grow" style="gap:6px;padding:14px 8px;border-color:var(--{c})">{ic(i,c,52)}<b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">{d}</span></div>')
    if k < 3:
        fc.append(arrow(size=24))
tb = [("코드 동작", "test (order-api)", "assert 500 == 200"), ("빌드 재료", "build (order-worker)", '"/wroker.py": not found'),
      ("설정 문법", "compose-check", "services.redis must be a mapping"), ("레지스트리 권한", "build (…)", "denied: permission_denied")]
tr = "".join(f'<div class="row" style="gap:10px"><div class="box" style="width:190px;background:var(--slate-l);color:var(--navy);font-size:17px">{a}</div><div class="box" style="width:260px;background:#fff;border:1.5px solid var(--line);color:var(--navy);font-size:16px;{MONO}">{b}</div><div class="box grow" style="background:#0F1E2E;color:#F5B5AE;font-size:16px;{MONO}">{c}</div></div>' for a, b, c in tb)
R("w3d2-ci-failure", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(fc)}</div>
<div class="col" style="gap:8px">{tr}</div>
<div class="row" style="gap:14px">{note("red", "맨 아래 <b style='color:var(--navy)'>exit code 1</b>은 '실패했다'는 사실뿐 — 원인은 몇 줄 위")}{note("teal", "main 보호: <b style='color:var(--navy)'>초록이어야 병합</b> — 토요타의 안돈 줄")}</div>''', w=1600)
