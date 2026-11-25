"""2주차 4일차 다이어그램. 실행: python3 diagrams/w2d4.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week2" / "day4"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def ctr(name, sub, color="teal", icn="Box", w=None, extra=""):
    ws = f"width:{w}px;" if w else ""
    return f'''<div class="card center" style="{ws}gap:6px;border-color:var(--{color});padding:14px 12px">{ic(icn, color, 62)}
<div style="font-size:21px;font-weight:900;color:var(--navy);{MONO}">{name}</div><div style="font-size:16px;color:var(--slate)">{sub}</div>{extra}</div>'''


# 1. 컨테이너 데이터는 사라진다
def scene(title, col, body):
    return f'<div class="card grow" style="gap:10px;border-color:var(--{col})"><div class="tag" style="color:var(--{col})">{title}</div>{body}</div>'


wl = lambda t, bg: f'<div style="background:{bg};border-radius:8px;padding:9px 14px;font-size:18px;font-weight:700;color:var(--navy)">{t}</div>'
left = f'''<div class="row c" style="gap:12px">{ic("Box","slate",56)}<div style="font-size:21px;font-weight:800;color:var(--navy)">db-temp</div></div>
{wl("쓰기 가능한 층 — memo 표", "var(--orange-l)")}{wl("이미지 postgres:18 (읽기 전용)", "#E8EEF4")}
<div class="row c" style="gap:10px;justify-content:center">{icon("Trash2",28,"red",2.2)}<span style="font-size:19px;font-weight:800;color:var(--red);{MONO}">docker rm</span></div>
<div class="box" style="background:var(--red-l);color:var(--red);font-size:19px">새 컨테이너 = 빈 데이터 · memo 없음</div>'''
mid = f'''<div class="row c" style="gap:12px">{ic("Box","slate",56)}<div style="font-size:21px;font-weight:800;color:var(--navy)">-v 없음 + 이미지의 VOLUME</div></div>
<div class="row" style="gap:8px">{"".join(f'<div class="box grow" style="background:#fff;border:2px dashed var(--slate);color:var(--slate);font-size:16px;{MONO}">{x}…</div>' for x in ["1673955","5835936"])}</div>
<div style="font-size:18px;color:var(--slate);text-align:center">무작위 이름 볼륨이 매번 새로 생긴다</div>
<div class="box" style="background:var(--orange-l);color:var(--orange);font-size:19px">남아 있지만 찾을 수 없다 — 고아 볼륨</div>'''
right = f'''<div class="row c" style="gap:12px">{ic("Vault","green",56)}<div style="font-size:21px;font-weight:800;color:var(--navy);{MONO}">-v devmart-db:/var/lib/postgresql</div></div>
<div class="row c" style="gap:10px;justify-content:center">{ctr("db","1번째","slate","Box",150)}{arrow(size=26)}{ctr("db","2번째","slate","Box",150)}</div>
<div style="font-size:18px;color:var(--slate);text-align:center">컨테이너는 바뀌어도 같은 이름의 볼륨을 붙인다</div>
<div class="box" style="background:var(--green-l);color:var(--green);font-size:19px">데이터가 그대로 — 6 rows</div>'''
R("w2d4-ephemeral", f'''<div class="row" style="gap:16px;align-items:stretch">{scene("① 볼륨 없이 (쓰기 가능한 층)", "red", left)}{scene("② 이름 없는 볼륨", "orange", mid)}{scene("③ 이름 있는 볼륨 (2교시)", "green", right)}</div>
<div class="row" style="gap:14px">{note("slate", "<b style='color:var(--navy)'>호텔 방</b> = 컨테이너 · 체크아웃하면 비워진다")}{note("green", "<b style='color:var(--navy)'>개인 금고</b> = 볼륨 · 어느 방에 묵든 다시 꺼낸다")}</div>''', w=1500)

# 2. 마운트 종류
def mt(title, col, icn, syn, where, use, who):
    return f'''<div class="card grow" style="gap:10px;border-color:var(--{col})"><div class="row c" style="gap:12px">{ic(icn,col,60)}<h3 style="font-size:24px">{title}</h3></div>
<div style="background:#0F1E2E;color:#E2E8F0;border-radius:8px;padding:9px 12px;font-size:16px;{MONO}">{syn}</div>
<div style="font-size:18px"><b style="color:var(--navy)">저장</b> · {where}</div><div style="font-size:18px"><b style="color:var(--navy)">관리</b> · {who}</div>
<div class="box" style="background:var(--{col}-l);color:var(--navy);font-size:18px">{use}</div></div>'''


cbox = f'''<div style="border:3px solid var(--teal);border-radius:16px;padding:14px 20px;display:flex;align-items:center;gap:16px;background:#F4FAFB">{ic("Box","teal",64)}
<div class="col" style="gap:6px"><div style="font-size:22px;font-weight:900;color:var(--teal-d)">컨테이너</div><div style="font-size:17px;{MONO};color:var(--slate)">/var/lib/postgresql · /usr/share/nginx/html · /tmp</div></div>
<div class="grow"></div><div style="font-size:18px;color:var(--slate)">컨테이너 안에서는 셋 다 그냥 폴더로 보인다</div></div>'''
R("w2d4-mount-types", f'''{cbox}
<div class="row" style="gap:10px;justify-content:space-around">{icon("ArrowDown",34,"slate",2.5)}{icon("ArrowDown",34,"slate",2.5)}{icon("ArrowDown",34,"slate",2.5)}</div>
<div class="row" style="gap:16px;align-items:stretch">
{mt("이름 있는 볼륨", "green", "Vault", "-v devmart-db:/var/lib/postgresql", "Docker가 정한 곳", "DB 데이터 — 오래 남길 것", "docker volume …")}
{mt("바인드 마운트", "violet", "FolderOpen", '-v "$PWD/web":/usr/share/nginx/html:ro', "<b>내가 고른 폴더</b>", "코드 · 설정 — 고치면 즉시 반영", "나 (VS Code)")}
{mt("tmpfs", "orange", "MemoryStick", "--tmpfs /tmp", "메모리 — 끄면 사라짐", "임시 파일 · 디스크에 남기면 안 되는 것", "없음")}</div>''', w=1500)

# 3. bridge vs user-defined DNS
def net(title, col, ctrs, dns_ok):
    inner = "".join(ctr(n, ip, "slate" if not dns_ok else "teal", "Box", 200) for n, ip in ctrs)
    dns = (f'<div class="box" style="background:var(--green-l);color:var(--green);font-size:19px">{icon("BookOpen",24,"green",2)} 내장 DNS — "db" → 172.18.0.2</div>' if dns_ok
           else f'<div class="box" style="background:var(--red-l);color:var(--red);font-size:19px">{icon("X",24,"red",2.5)} 이름 찾기 없음 — IP를 외워야 한다</div>')
    q = (f'<div style="font-size:18px;{MONO};color:var(--navy)">getent hosts db → <b style="color:var(--green)">172.18.0.2</b></div>' if dns_ok
         else f'<div style="font-size:18px;{MONO};color:var(--navy)">getent hosts api-b → <b style="color:var(--red)">(없음, 코드 2)</b></div>')
    return f'''<div class="card grow" style="gap:12px;border-color:var(--{col});border-width:3px"><div class="row c" style="gap:10px">{icon("Network",32,col,2)}<h3 style="font-size:23px">{title}</h3></div>
<div class="row" style="gap:12px;justify-content:center">{inner}</div>{dns}{q}</div>'''


R("w2d4-bridge-dns", f'''<div class="row" style="gap:18px;align-items:stretch">
{net("기본 bridge (172.17.x.x)", "slate", [("api-a", "172.17.0.2"), ("api-b", "172.17.0.3 → .4")], False)}
{net("devmart-net (직접 만든 bridge)", "teal", [("db", "172.18.0.2"), ("catalog-api", "172.18.0.3")], True)}</div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>IP는 바뀐다</b> — 다시 띄우면 다른 번호")}{note("teal", "<b style='color:var(--navy)'>이름은 그대로</b> — DNS가 새 IP를 알려 준다")}{note("slate", "<b style='color:var(--navy)'>localhost</b> = 그 컨테이너 자신")}</div>''', w=1500)

# 4. API ↔ DB
R("w2d4-api-db", f'''<div class="row" style="gap:12px;align-items:center">
<div class="card center" style="width:220px;gap:8px">{ic("Laptop","navy",70)}<h3 style="font-size:22px">노트북</h3><div style="font-size:17px;{MONO};color:var(--slate)">curl localhost:8000</div></div>
<div class="col center" style="gap:4px">{arrow(size=34)}<div class="chip" style="font-size:15px;background:var(--orange);color:#fff">-p 8000:8000</div></div>
<div style="border:3px dashed var(--teal);border-radius:18px;padding:18px;display:flex;gap:14px;align-items:center;justify-content:space-around;flex:1;background:#F4FAFB;position:relative">
 <div style="position:absolute;top:-16px;left:20px;background:#fff;padding:0 10px;font-size:18px;font-weight:900;color:var(--teal-d)">devmart-net</div>
 {ctr("catalog-api", "DB_HOST=db", "violet", "Server", 230)}
 <div class="col center" style="gap:4px">{arrow(size=34)}<div style="font-size:16px;{MONO};color:var(--teal-d);font-weight:800">db:5432</div></div>
 {ctr("db", "-p 없음", "teal", "Database", 200)}
 <div class="col center" style="gap:4px">{icon("ArrowRight",30,"slate",2.5)}</div>
 <div class="card center" style="width:200px;gap:6px;border-color:var(--green)">{ic("Vault","green",62)}<div style="font-size:19px;font-weight:900;color:var(--navy);{MONO}">devmart-db</div><div style="font-size:16px;color:var(--slate)">볼륨 · 상품 5개</div></div>
</div></div>
<div class="row" style="gap:14px">{note("violet", "환경 변수 <b style='color:var(--navy)'>DB_HOST · DB_PASSWORD</b> — 코드는 그대로")}{note("teal", "이름으로 찾는다 — <b style='color:var(--navy)'>같은 네트워크</b>일 때만")}{note("green", "응답 <b style='color:var(--navy)'>\"source\":\"database\"</b>")}</div>''', w=1600)

# 5. 진단 순서
steps = [("Search", "이름", "failed to resolve host 'db'", "켜져 있나 · 같은 네트워크인가 · 오타", "red"),
         ("Plug", "연결", "Connection refused", "아직 시작 중인가 (pg_isready) · 포트", "orange"),
         ("KeyRound", "인증", "password authentication failed", "DB_PASSWORD · DB_USER", "violet"),
         ("Database", "DB", 'database "…" does not exist', "DB_NAME", "teal"),
         ("Table", "표", 'relation "products" does not exist', "초기화 SQL이 실행되었나", "green")]
rows = []
for k, (i, t, msg, chk, c) in enumerate(steps):
    rows.append(f'''<div class="row c" style="gap:14px"><div style="width:44px;height:44px;border-radius:22px;background:var(--{c});color:#fff;font-size:22px;font-weight:900;display:flex;align-items:center;justify-content:center">{k+1}</div>
<div class="row c" style="width:150px;gap:8px">{icon(i,28,c,2)}<span style="font-size:21px;font-weight:900;color:var(--navy)">{t}</span></div>
<div style="width:560px;background:#0F1E2E;color:#F5B5AE;border-radius:8px;padding:10px 14px;font-size:17px;{MONO}">{msg}</div>
<div class="grow" style="background:var(--{c}-l);border-radius:8px;padding:10px 14px;font-size:18px;color:var(--navy)">{chk}</div></div>''')
R("w2d4-debug-order", f'''<div class="row c" style="gap:12px">{icon("FileText",30,"navy",2)}<div style="font-size:22px;font-weight:800;color:var(--navy)">503 database unavailable → <span style="{MONO}">docker logs catalog-api</span>의 오류 문장으로 층을 좁힌다</div></div>
<div class="col" style="gap:10px">{"".join(rows)}</div>
<div class="row" style="gap:14px">{note("slate", "바깥 → 안 순서 · <b style='color:var(--navy)'>아래 단계 오류가 보이면 위 단계는 통과</b> — 예: 인증 실패면 네트워크는 정상")}</div>''', w=1500)

# 6. 설정과 비밀값
envs = [("개발 (노트북)", "APP_ENV=dev\nDB_HOST=(없음)", "slate"), ("오늘 (docker)", "APP_ENV=docker\nDB_HOST=db", "teal"), ("운영 (5주차)", "APP_ENV=prod\nDB_HOST=RDS 주소", "violet")]
ec = "".join(f'<div class="card grow" style="gap:6px;border-color:var(--{c});padding:12px"><div class="tag" style="color:var(--{c})">{t}</div><div style="font-size:16px;{MONO};white-space:pre-line;color:var(--navy)">{v}</div></div>' for t, v, c in envs)
leak = [("Terminal", "셸 기록", "~/.bash_history", "green", "Check", ".env + --env-file"), ("Eye", "docker inspect", "Config.Env", "orange", "Clock", "파일 비밀값 · Secret"), ("Box", "컨테이너 안 env", "자식 프로세스 · 로그", "orange", "Clock", "비밀 저장소")]
lc = "".join(f'<div class="card grow" style="gap:6px;padding:12px"><div class="row c" style="gap:8px">{icon(i,26,"red",2)}<b style="font-size:19px;color:var(--navy)">{t}</b></div><div style="font-size:16px;{MONO};color:var(--slate)">{s}</div><div class="row c" style="gap:6px">{icon(ii,22,c,2.5)}<span style="font-size:17px;color:var(--{c})">{fx}</span></div></div>' for i, t, s, c, ii, fx in leak)
R("w2d4-config", f'''<div class="row" style="gap:16px;align-items:center">
<div class="card center" style="width:280px;gap:8px;border-color:var(--teal)">{ic("Layers","teal",72)}<div style="font-size:19px;font-weight:900;{MONO};color:var(--navy)">catalog-api:1.0.1</div><div style="font-size:16px;color:var(--slate)">이미지는 하나 — 비밀값 없음</div></div>
{arrow(size=36)}<div class="row grow" style="gap:12px">{ec}</div></div>
<div class="row c" style="gap:12px"><div class="tag" style="color:var(--red)">-e DB_PASSWORD=… 가 남는 곳</div></div>
<div class="row" style="gap:12px">{lc}</div>
<div class="row" style="gap:14px">{note("violet", "<b style='color:var(--navy)'>.env.example</b> → Git (이름만) · <b style='color:var(--navy)'>.env</b> → .gitignore (진짜 값)")}{note("slate", "우선순위 <b style='color:var(--navy)'>-e &gt; --env-file &gt; Dockerfile ENV</b>")}</div>''', w=1500)

# 7. 3계층
R("w2d4-three-tier", f'''<div class="row" style="gap:12px;align-items:center">
<div class="card center" style="width:200px;gap:8px">{ic("Globe","navy",70)}<h3 style="font-size:22px">브라우저</h3><div style="font-size:16px;{MONO};color:var(--slate)">localhost:8080</div></div>
<div class="col center" style="gap:4px">{arrow(size=34)}<div class="chip" style="font-size:15px;background:var(--orange);color:#fff">-p 8080:80 (유일한 문)</div></div>
<div style="border:3px dashed var(--teal);border-radius:18px;padding:22px 16px 16px;display:flex;flex-direction:column;gap:14px;flex:1;background:#F4FAFB;position:relative">
 <div style="position:absolute;top:-16px;left:20px;background:#fff;padding:0 10px;font-size:18px;font-weight:900;color:var(--teal-d)">devmart-net</div>
 <div class="row" style="gap:10px;align-items:center;justify-content:space-around">
  {ctr("web", "nginx · /api/ → 프록시", "orange", "Globe", 230)}
  <div class="col center" style="gap:4px">{arrow(size=30)}<div style="font-size:15px;{MONO};color:var(--teal-d);font-weight:800">catalog-api:8000</div></div>
  {ctr("catalog-api", "--env-file .env", "violet", "Server", 230)}
  <div class="col center" style="gap:4px">{arrow(size=30)}<div style="font-size:15px;{MONO};color:var(--teal-d);font-weight:800">db:5432</div></div>
  {ctr("db", "postgres:18", "teal", "Database", 190)}
 </div>
 <div class="row" style="gap:10px">
  <div class="box grow" style="background:var(--violet-l);color:var(--navy);font-size:16px;{MONO}">바인드: web/ · nginx/default.conf (:ro)</div>
  <div class="box grow" style="background:var(--green-l);color:var(--navy);font-size:16px;{MONO}">볼륨: devmart-db → /var/lib/postgresql</div>
 </div>
</div></div>
<div class="row" style="gap:14px">{note("orange", "띄우는 순서 <b style='color:var(--navy)'>db → catalog-api → web</b> — 거꾸로면 nginx가 시작하지 않는다")}{note("slate", "명령 6개 · 옵션 20개 가까이 → 내일 <b style='color:var(--navy)'>compose.yaml</b> 하나로")}</div>''', w=1600)
