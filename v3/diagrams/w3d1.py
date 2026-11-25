"""3주차 1일차 다이어그램. 실행: python3 diagrams/w3d1.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week3" / "day1"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def svc(name, sub, c, i, w=200, mono=True):
    f = MONO if mono else ""
    return f'''<div class="card center" style="width:{w}px;gap:6px;padding:14px 10px;border-color:var(--{c})">{ic(i,c,58)}
<div style="font-size:20px;font-weight:900;color:var(--navy);{f}">{name}</div><div style="font-size:15px;color:var(--slate);text-align:center">{sub}</div></div>'''


def dbx(name, c="teal", w=170):
    return f'<div class="card center" style="width:{w}px;gap:4px;padding:10px;border-color:var(--{c});background:var(--{c}-l)">{icon("Database",34,c,2)}<div style="font-size:17px;font-weight:800;{MONO};color:var(--navy)">{name}</div></div>'


# 1. 모놀리식 vs MSA
mods = ["상품", "주문", "결제", "회원", "배송"]
mono = f'''<div class="card grow" style="gap:12px;border-color:var(--slate)"><div class="tag">모놀리식 — 한 덩어리</div>
<div style="border:3px solid var(--slate);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:10px;background:var(--slate-l)">
<div class="row c" style="gap:10px">{icon("Box",30,"slate",2)}<b style="font-size:21px;color:var(--navy)">app (프로그램 하나 · 배포 하나)</b></div>
<div class="row" style="gap:8px;flex-wrap:wrap">{"".join(f'<div class="box" style="background:#fff;color:var(--navy);font-size:18px">{m}</div>' for m in mods)}</div>
<div class="row c" style="gap:8px;justify-content:center">{icon("ArrowDown",26,"slate",2.5)}<span style="font-size:16px;color:var(--slate)">함수 호출</span></div>
{dbx("DB 하나 · 표 전부","slate",460)}</div>
<div class="note" style="font-size:17px">하나 고쳐도 전체 배포 · 하나 죽으면 전체 위험</div></div>'''
ms = [("상품", "teal", "LayoutGrid"), ("주문", "violet", "ShoppingCart"), ("결제", "orange", "CreditCard")]
mcol = "".join(f'''<div class="col center" style="gap:8px"><div class="card center" style="width:150px;gap:4px;padding:12px;border-color:var(--{c})">{ic(i,c,48)}<b style="font-size:19px;color:var(--navy)">{n} 서비스</b></div>{icon("ArrowDown",22,"slate",2.5)}{dbx(n+" DB",c,150)}</div>''' for n, c, i in ms)
msa = f'''<div class="card grow" style="gap:12px;border-color:var(--teal)"><div class="tag" style="color:var(--teal-d)">MSA — 업무별 작은 서비스</div>
<div class="row" style="gap:12px;justify-content:center;position:relative">{mcol}</div>
<div class="row c" style="gap:8px;justify-content:center">{icon("ArrowLeftRight",26,"orange",2.5)}<span style="font-size:17px;color:var(--orange);font-weight:700">서비스 사이는 네트워크 호출 (HTTP · 큐)</span></div>
<div class="note" style="font-size:17px">따로 배포 · 장애를 가둘 수 있음 · 대신 운영할 것이 몇 배</div></div>'''
R("w3d1-mono-vs-msa", f'''<div class="row" style="gap:20px;align-items:stretch">{mono}{msa}</div>
<div class="row" style="gap:14px">{note("slate", "<b style='color:var(--navy)'>대형 식당</b> — 주방 하나에서 모든 메뉴")}{note("teal", "<b style='color:var(--navy)'>푸드코트</b> — 가게마다 자기 주방과 창고")}</div>''', w=1500)

# 2. 데이터 소유
R("w3d1-data-ownership", f'''<div class="row" style="gap:22px;align-items:stretch">
<div class="card grow" style="gap:12px;border-color:var(--red);background:#FFF8F7"><div class="tag" style="color:var(--red)">이렇게 하지 않는다 — 남의 DB를 직접 읽기</div>
<div class="row c" style="gap:16px;justify-content:center">{svc("order-api","주문 서비스","violet","ShoppingCart",180)}<div class="col center" style="gap:4px">{icon("ArrowRight",34,"red",2.5)}<span style="font-size:15px;{MONO};color:var(--red)">SELECT price<br>FROM products</span></div>{dbx("catalog DB","teal",170)}</div>
<div class="box" style="background:var(--red-l);color:var(--red);font-size:18px">상품 팀이 열 이름을 바꾸면 주문 서비스가 모르는 사이에 깨진다</div></div>
<div class="card grow" style="gap:12px;border-color:var(--green)"><div class="tag" style="color:var(--green)">이렇게 한다 — API로 묻기</div>
<div class="row c" style="gap:12px;justify-content:center">{svc("order-api","주문 서비스","violet","ShoppingCart",170)}<div class="col center" style="gap:4px">{icon("ArrowRight",30,"green",2.5)}<span style="font-size:14px;{MONO};color:var(--green)">GET /api/<br>products/3</span></div>{svc("catalog-api","상품 서비스","teal","LayoutGrid",170)}{icon("ArrowRight",26,"slate",2.5)}{dbx("catalog DB","teal",140)}</div>
<div class="row c" style="gap:12px;justify-content:center">{icon("ArrowDown",26,"violet",2.5)}{dbx("orders DB","violet",170)}<span style="font-size:16px;color:var(--slate)">product_name 복사 · FK 없음</span></div>
<div class="box" style="background:var(--green-l);color:var(--green);font-size:18px">API = 약속. 안쪽 표는 각 팀이 자유롭게</div></div></div>
<div class="row" style="gap:14px">{note("orange", "대가: 서비스를 넘는 <b style='color:var(--navy)'>JOIN · 외래 키 · 트랜잭션</b>을 쓸 수 없다")}{note("slate", "오늘 실습: PostgreSQL 서버 하나에 <b style='color:var(--navy)'>DB 둘</b> (catalog · orders) — 서로 접속하지 않는다")}</div>''', w=1600)

# 3. 토폴로지
R("w3d1-topology", f'''<div class="row" style="gap:12px;align-items:center">
<div class="card center" style="width:170px;gap:8px">{ic("Globe","navy",64)}<h3 style="font-size:21px">브라우저</h3><div style="font-size:15px;{MONO};color:var(--slate)">localhost:8080</div></div>
<div class="col center" style="gap:4px">{arrow(size=30)}<div class="chip" style="font-size:14px;background:var(--orange);color:#fff">8080 하나</div></div>
<div style="border:3px dashed var(--teal);border-radius:18px;padding:24px 16px 16px;flex:1;background:#F4FAFB;position:relative;display:flex;gap:14px;align-items:center">
 <div style="position:absolute;top:-16px;left:20px;background:#fff;padding:0 10px;font-size:18px;font-weight:900;color:var(--teal-d)">devmart-msa_default</div>
 {svc("web","nginx · API 게이트웨이<br>/api/orders → order-api<br>/api/ → catalog-api","orange","Globe",230)}
 <div class="col" style="gap:40px">{icon("ArrowRight",30,"slate",2.5)}{icon("ArrowRight",30,"slate",2.5)}</div>
 <div class="col" style="gap:16px;flex:1">
  <div class="row c" style="gap:12px">{svc("catalog-api","상품 · :8000","teal","LayoutGrid",200)}{icon("ArrowRight",26,"slate",2.5)}{dbx("catalog","teal",150)}</div>
  <div class="row c" style="gap:12px">{svc("order-api","주문 접수 · :8000<br>/health · /ready","violet","ShoppingCart",200)}
   <div class="col" style="gap:8px"><div class="row c" style="gap:6px">{icon("ArrowRight",22,"teal",2.5)}<span style="font-size:14px;{MONO};color:var(--teal-d)">① 가격 (동기)</span></div><div class="row c" style="gap:6px">{icon("ArrowRight",22,"violet",2.5)}<span style="font-size:14px;{MONO};color:var(--violet)">② 저장 → orders</span></div><div class="row c" style="gap:6px">{icon("ArrowRight",22,"orange",2.5)}<span style="font-size:14px;{MONO};color:var(--orange)">③ 큐 (비동기) → 아래 redis</span></div></div>
   {dbx("orders","violet",130)}</div>
  <div class="row c" style="gap:12px">{svc("redis","큐 orders","orange","Inbox",200)}{icon("ArrowRight",26,"orange",2.5)}{svc("order-worker","처리기 · 포트 없음","green","Cog",200)}{icon("ArrowRight",26,"slate",2.5)}{dbx("orders","violet",130)}</div>
 </div>
</div></div>
<div class="row" style="gap:14px">{note("teal", "db 컨테이너 하나 = <b style='color:var(--navy)'>catalog · orders 두 DB</b> (PostgreSQL 18, 볼륨 db-data)")}{note("orange", "바깥 공개는 web뿐 · 나머지는 <b style='color:var(--navy)'>서비스 이름</b>으로 서로 찾는다")}</div>''', w=1700)

# 4. 요청 추적
steps = [("web", "orange", "번호 붙이기", "X-Request-ID: ea22…", "19.200"),
         ("order-api", "violet", "order_received", "헤더로 받음", "19.202"),
         ("catalog-api", "teal", "get_product", "헤더로 전달", "19.216"),
         ("order-api", "violet", "order_saved · order_queued", "→ 202 응답", "19.228"),
         ("redis", "orange", "메시지 안에", '{"order_id":9,"request_id":"ea22…"}', "—"),
         ("order-worker", "green", "order_processing → completed", "메시지에서 꺼냄", "19.230 → 20.236")]
rows = "".join(f'''<div class="row c" style="gap:14px"><div style="width:120px;text-align:right;font-size:17px;{MONO};color:var(--slate)">{t}</div>
<div style="width:20px;height:20px;border-radius:10px;background:var(--{c});flex:none"></div>
<div style="width:190px;font-size:19px;font-weight:900;{MONO};color:var(--navy)">{s}</div>
<div class="grow" style="background:var(--{c}-l);border-radius:8px;padding:10px 14px;font-size:18px;color:var(--navy)"><b>{e}</b> · <span style="{MONO};font-size:16px">{d}</span></div></div>''' for s, c, e, d, t in steps)
R("w3d1-request-trace", f'''<div class="row c" style="gap:12px">{icon("Tag",30,"navy",2)}<div style="font-size:22px;font-weight:800;color:var(--navy)">요청 ID 하나 = 택배 송장 번호 — <span style="{MONO}">docker compose logs -t --no-log-prefix | grep $RID | sort</span></div></div>
<div class="col" style="gap:10px;position:relative">{rows}</div>
<div class="row" style="gap:14px">{note("violet", "HTTP 호출은 <b style='color:var(--navy)'>헤더</b>로 넘긴다")}{note("orange", "큐는 헤더가 없다 → <b style='color:var(--navy)'>메시지 안에</b> 넣는다")}{note("teal", "사용자 대기 <b style='color:var(--navy)'>약 26ms</b> · 처리 완료 약 1초 뒤")}</div>''', w=1600)

# 5. 동기 vs 비동기
R("w3d1-sync-async", f'''<div class="row" style="gap:22px;align-items:stretch">
<div class="card grow" style="gap:12px;border-color:var(--teal)"><div class="row c" style="gap:10px">{ic("Phone","teal",50)}<h3 style="font-size:24px">동기 — 전화</h3></div>
<div class="row c" style="gap:12px;justify-content:center">{svc("order-api","","violet","ShoppingCart",170)}<div class="col center" style="gap:6px"><div class="row c" style="gap:4px">{icon("ArrowRight",26,"teal",2.5)}<span style="font-size:15px;{MONO}">가격?</span></div><div class="row c" style="gap:4px">{icon("ArrowLeft",26,"teal",2.5)}<span style="font-size:15px;{MONO}">12000</span></div></div>{svc("catalog-api","","teal","LayoutGrid",170)}</div>
<div class="box" style="background:var(--teal-l);color:var(--navy);font-size:18px">답이 올 때까지 기다린다 · 상대가 느리면 나도 느림 → <b>타임아웃 2초</b></div></div>
<div class="card grow" style="gap:12px;border-color:var(--orange)"><div class="row c" style="gap:10px">{ic("Inbox","orange",50)}<h3 style="font-size:24px">비동기 — 주문서 함</h3></div>
<div class="row c" style="gap:10px;justify-content:center">{svc("order-api","202 Accepted","violet","ShoppingCart",160)}{icon("ArrowRight",26,"orange",2.5)}
<div class="card center" style="width:170px;gap:6px;padding:10px;border-color:var(--orange)"><div style="font-size:16px;font-weight:800;{MONO};color:var(--navy)">redis · orders</div><div class="row" style="gap:4px">{"".join('<div style="width:24px;height:30px;border-radius:4px;background:var(--orange)"></div>' for _ in range(5))}</div><div style="font-size:15px;{MONO};color:var(--orange)">LLEN = 5</div></div>
{icon("ArrowRight",26,"orange",2.5)}<div class="col" style="gap:6px">{"".join(f'<div class="box" style="background:var(--green-l);color:var(--green);font-size:15px;{MONO}">order-worker-{k}</div>' for k in (1,2,3))}</div></div>
<div class="box" style="background:var(--orange-l);color:var(--navy);font-size:18px">맡기고 바로 돌아간다 · 몰리면 쌓인다 → 처리기를 늘려 <b>나눠서</b> 비운다</div></div></div>
<div class="row" style="gap:14px">{note("slate", "리틀의 법칙 <b style='color:var(--navy)'>L = λ × W</b> — 도착률이 처리 능력보다 크면 큐는 끝없이 길어진다")}{note("red", "비동기는 장애를 없애지 않고 <b style='color:var(--navy)'>미룬다</b> → 큐 길이를 감시")}</div>''', w=1650)

# 6. 진단 순서
ds = [("Eye", "증상", "브라우저 · curl -i · 상태 코드", "red"), ("ScanSearch", "영향 범위", "무엇은 되고 무엇은 안 되나?", "orange"),
      ("ListChecks", "상태", "docker compose ps", "violet"), ("FileText", "로그", "docker compose logs 서비스", "teal"),
      ("Settings", "설정", "exec 서비스 env · compose.yaml", "navy"), ("Search", "안에서", "exec 서비스 getent hosts 이름", "green")]
dc = []
for k, (i, t, d, c) in enumerate(ds):
    dc.append(f'<div class="card center grow" style="gap:6px;padding:14px 8px;border-color:var(--{c})"><div style="font-size:15px;font-weight:900;color:var(--{c})">{k+1}</div>{ic(i,c,54)}<b style="font-size:20px;color:var(--navy)">{t}</b><span style="font-size:15px;{MONO};color:var(--slate);text-align:center">{d}</span></div>')
    if k < 5:
        dc.append(arrow(size=22))
tbl = [("1 주소 오타", "주문하기만 503", "Name or service not known"), ("2 DB 이름 오타", "주문 전부 503", 'database "order" does not exist'), ("3 큐 이름 불일치", "202인데 pending에서 멈춤", "에러 없음 → queue 값 · LLEN")]
tr = "".join(f'<div class="row" style="gap:10px"><div class="box" style="width:200px;background:var(--slate-l);color:var(--navy);font-size:17px">{a}</div><div class="box grow" style="background:#fff;border:1.5px solid var(--line);color:var(--navy);font-size:17px">{b}</div><div class="box" style="width:520px;background:#0F1E2E;color:#F5B5AE;font-size:16px;{MONO}">{c}</div></div>' for a, b, c in tbl)
R("w3d1-debug-order", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(dc)}</div>
<div class="col" style="gap:8px">{tr}</div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>② 영향 범위</b>가 가장 빨리 범위를 줄인다")}{note("red", "Up + 에러 없음 ≠ 정상 — <b style='color:var(--navy)'>회색 장애</b>")}</div>''', w=1650)
