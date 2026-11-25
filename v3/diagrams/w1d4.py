"""1주차 4일차 다이어그램. 실행: python3 diagrams/w1d4.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, aws, arrow  # noqa: E402

OUT = ROOT / "assets" / "week1" / "day4"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def rowcard(i, c, t, d, extra=""):
    return f'<div class="card" style="flex-direction:row;align-items:center;gap:14px;padding:14px 18px;border-color:var(--{c});{extra}">{ic(i,c,56)}<div><h3 style="font-size:23px">{t}</h3><p style="font-size:18px">{d}</p></div></div>'


# 1. 상품 페이지 분해
areas = [("Image", "orange", "상품 사진", "이미지 저장소 + CDN"), ("Tag", "teal", "이름 · 설명", "상품 카탈로그 DB"),
         ("BadgePercent", "teal", "가격 · 할인", "가격 서비스 (자주 바뀜)"), ("Truck", "violet", "재고 · 내일 도착", "재고 · 배송 서비스"),
         ("Star", "orange", "리뷰", "리뷰 서비스 + DB"), ("Sparkles", "violet", "추천 상품", "추천 시스템 (AI · GPU)")]
phone_items = "".join(f'<div style="background:var(--{c}-l);border:2px solid var(--{c});border-radius:10px;padding:{p}px 12px;font-size:19px;font-weight:800;color:var(--navy);display:flex;align-items:center;gap:8px">{icon(i,26,c,2)}{t}</div>'
                      for (i, c, t, _), p in zip(areas, [34, 10, 10, 10, 18, 18]))
right = "".join(rowcard(i, c, s, f"← {t}") for i, c, t, s in areas)
R("w1d4-product-page", f'''<div class="row" style="gap:30px;align-items:center">
<div style="width:330px;border:6px solid var(--navy);border-radius:36px;padding:26px 16px;display:flex;flex-direction:column;gap:10px;background:#fff">
 <div style="font-size:18px;font-weight:700;color:var(--slate);text-align:center">운동화 상품 페이지</div>{phone_items}</div>
<div class="col center" style="gap:6px">{arrow(size=44)}<div style="font-size:19px;font-weight:800;color:var(--slate)">뒤에서는</div></div>
<div class="col grow" style="gap:10px">{right}</div></div>
<div class="note">사용자에게는 페이지 하나 — 뒤에서는 책임이 다른 여러 시스템이 정보를 모아 온다</div>''')

# 2. 구성요소 지도
comp = [("MonitorSmartphone", "teal", "1 프론트엔드"), ("Server", "teal", "2 백엔드 API"), ("Database", "violet", "3 데이터베이스"),
        ("Zap", "orange", "4 캐시"), ("ListOrdered", "orange", "5 메시지 큐"), ("FolderArchive", "violet", "6 파일 저장소"),
        ("Network", "slate", "7 네트워크"), ("KeyRound", "red", "8 설정 · 비밀값"), ("Cpu", "slate", "9 컴퓨트"), ("Activity", "green", "10 관찰 가능성")]
cc = "".join(f'<div class="card center" style="gap:8px;padding:18px 10px;border-color:var(--{c})">{ic(i,c,70)}<div style="font-size:21px;font-weight:800;color:var(--navy)">{t}</div></div>' for i, c, t in comp)
R("w1d4-component-map", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card fill-teal center" style="width:250px;justify-content:center;gap:10px">{icon("Code",60,"teal",2)}<h3 style="font-size:28px">코드</h3><p style="font-size:19px">개발자가 만든 것<br>(1~2번)</p></div>
<div class="col center" style="justify-content:center;gap:4px"><div style="font-size:54px;font-weight:900;color:var(--slate)">+</div></div>
<div class="grid grow" style="grid-template-columns:repeat(5,1fr);gap:12px">{cc}</div></div>
<div class="row c" style="gap:14px;justify-content:center"><div class="box" style="background:var(--navy);color:#fff;font-size:24px;padding:16px 30px">애플리케이션 = 코드 + 실행 조건</div>
{arrow(size=36)}<div class="box" style="background:var(--orange-l);color:var(--navy);font-size:21px">2주차 Docker: 포장 · 3주차 K8s: 운영 · 5주차 Terraform: 인프라까지 코드로</div></div>''')

# 3. 3-tier
tiers = [("MonitorSmartphone", "teal", "표현 계층", "Presentation", "보여 주고 입력 받기", "홀 직원 · 메뉴판", "브라우저 · 모바일 앱"),
         ("Server", "orange", "애플리케이션 계층", "Logic", "규칙에 따라 처리", "주방", "API 서버"),
         ("Database", "violet", "데이터 계층", "Data", "저장하고 꺼내 주기", "식자재 창고", "PostgreSQL")]
tc = []
for k, (i, c, t, e, d, a, ex) in enumerate(tiers):
    tc.append(f'''<div class="card center grow" style="gap:10px;border-color:var(--{c})">{ic(i,c,92)}<h3 style="font-size:28px">{t}</h3><div class="tag">{e.upper()}</div>
<p style="font-size:21px;font-weight:700;color:var(--navy)">{d}</p><div class="box" style="background:var(--{c}-l);color:var(--slate);font-size:19px;width:100%">비유: {a}</div><div class="note" style="font-size:19px">예: {ex}</div></div>''')
    if k < 2:
        tc.append(arrow("both", 40))
R("w1d4-three-tier", f'''<div class="row flow" style="gap:12px">{"".join(tc)}</div>
<div class="card fill-slate" style="padding:16px 24px"><p style="font-size:21px">층을 나누면 <b style="color:var(--navy)">따로 바꾸고 따로 늘릴 수 있다</b> — 손님이 늘면 홀만, 요리가 밀리면 주방만 · 2주차 마지막 날 Compose 파일 하나로 세 층을 띄운다</p></div>''')

# 4. API 계약
R("w1d4-api-contract", f'''<div class="row flow" style="gap:16px">
<div class="card center" style="width:280px;gap:10px;justify-content:center">{ic("MonitorSmartphone","teal",92)}<h3 style="font-size:27px">프론트엔드</h3><p style="font-size:19px">손님<br>주방 안을 볼 수 없다</p></div>
<div class="col grow" style="gap:14px;justify-content:center">
 <div class="row c" style="gap:10px"><div style="flex:1;height:4px;background:var(--teal)"></div>{icon("ArrowRight",36,"teal",2.5)}</div>
 <div class="card fill-navy" style="padding:18px 22px;gap:10px"><div class="tag" style="color:#7FD3E0">API = 약속한 주문서</div>
  <div style="font-size:22px;{MONO};color:#fff">GET /api/products/123</div>
  <div style="font-size:20px;{MONO};color:#FBC99B">{{"id":123, "name":"운동화",<br>&nbsp;"price":59000, "stock":12}}</div></div>
 <div class="row c" style="gap:10px">{icon("ArrowLeft",36,"orange",2.5)}<div style="flex:1;height:4px;background:var(--orange)"></div></div>
</div>
<div class="card center" style="width:280px;gap:10px;justify-content:center">{ic("Server","orange",92)}<h3 style="font-size:27px">백엔드</h3><p style="font-size:19px">주방<br>조리법은 숨겨 둔다</p></div></div>
<div class="row" style="gap:14px"><div class="card fill-green grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">약속만 같으면</b> 주방이 요리사를 바꿔도 손님은 모른다 (정보 은닉)</p></div>
<div class="card fill-red grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">약속을 마음대로 바꾸면</b> 손님 쪽이 모두 고장 → 버전(/v2)과 공지</p></div></div>''')

# 5. 스케일 업 vs 아웃
def srv(size, col="teal"):
    return f'<div class="col center" style="gap:4px">{icon("Server",size,col,1.8)}</div>'


R("w1d4-scale", f'''<div class="row" style="gap:26px;align-items:stretch">
<div class="card grow center" style="gap:14px"><div class="tag">SCALE UP · 수직 확장</div>
 <div class="row c" style="gap:20px;justify-content:center;min-height:220px">{srv(70,"slate")}{arrow(size=40)}{srv(190,"orange")}</div>
 <h3 style="font-size:27px">더 큰 서버 하나로 교체</h3>
 <div class="row" style="gap:10px;width:100%"><div class="box grow" style="background:var(--green-l);color:var(--green);font-size:19px">코드 변경 거의 없음</div><div class="box grow" style="background:var(--red-l);color:var(--red);font-size:19px">한계 · 비쌈 · 교체 시 멈춤</div></div>
 <div class="note" style="font-size:19px">잘 맞는 곳: 데이터베이스</div></div>
<div class="card grow center" style="gap:14px"><div class="tag">SCALE OUT · 수평 확장</div>
 <div class="row c" style="gap:14px;justify-content:center;min-height:220px">
  <div class="col center" style="gap:6px">{icon("Split",60,"teal",2)}<div style="font-size:17px;font-weight:700;color:var(--slate)">로드밸런서</div></div>{arrow(size=34)}
  <div class="col" style="gap:8px">{"".join(f'<div class="row c" style="gap:6px">{srv(56)}</div>' for _ in range(3))}</div>
  <div class="col center" style="gap:4px;justify-content:center">{icon("Plus",40,"teal",2.5)}<div style="font-size:17px;color:var(--slate)">필요하면 더</div></div></div>
 <h3 style="font-size:27px">같은 서버를 여러 대로</h3>
 <div class="row" style="gap:10px;width:100%"><div class="box grow" style="background:var(--green-l);color:var(--green);font-size:19px">한계 없음 · 한 대 죽어도 OK</div><div class="box grow" style="background:var(--red-l);color:var(--red);font-size:19px">stateless 필요 · LB 필요</div></div>
 <div class="note" style="font-size:19px">잘 맞는 곳: 웹 · API 서버 → 클라우드의 기본</div></div></div>''')

# 6. SPOF
def chain(items, bad=None):
    out = []
    for k, (i, t) in enumerate(items):
        col = "red" if k == bad else "teal"
        out.append(f'<div class="col center" style="gap:6px;width:140px">{ic(i,col,70)}<div style="font-size:19px;font-weight:800;color:var(--navy)">{t}</div></div>')
        if k < len(items) - 1:
            out.append(arrow(size=32))
    return "".join(out)


def dup(i, t):
    return f'<div class="col center" style="gap:6px;width:150px"><div class="row" style="gap:6px">{ic(i,"teal",62)}{ic(i,"teal",62)}</div><div style="font-size:19px;font-weight:800;color:var(--navy)">{t} ×2</div></div>'


R("w1d4-spof", f'''<div class="card fill-red" style="gap:14px"><div class="row c" style="gap:12px">{icon("TriangleAlert",36,"red",2.2)}<h3 style="font-size:25px">SPOF가 있는 구조 — DB 한 대가 죽으면 전체가 멈춘다</h3></div>
<div class="row c" style="gap:10px;justify-content:center">{chain([("Users","사용자"),("Split","로드밸런서"),("Server","앱 서버 ×3"),("Database","DB 한 대")], bad=3)}</div></div>
<div class="card fill-green" style="gap:14px"><div class="row c" style="gap:12px">{icon("ShieldCheck",36,"green",2.2)}<h3 style="font-size:25px">이중화한 구조 — 가용 영역 두 곳에 나눠 둔다</h3></div>
<div class="row c" style="gap:10px;justify-content:center"><div class="col center" style="gap:6px;width:140px">{ic("Users","teal",70)}<div style="font-size:19px;font-weight:800;color:var(--navy)">사용자</div></div>{arrow(size=32)}{dup("Split","LB")}{arrow(size=32)}{dup("Server","앱 (AZ A·C)")}{arrow(size=32)}
<div class="col center" style="gap:6px;width:220px"><div class="row" style="gap:6px">{ic("Database","teal",62)}{icon("ArrowLeftRight",30,"slate",2)}{ic("Database","slate",62)}</div><div style="font-size:19px;font-weight:800;color:var(--navy)">DB 주 + 대기 (Multi-AZ)</div></div></div></div>
<div class="note">사람도 SPOF가 될 수 있다 — "그 사람만 아는 서버"는 문서와 런북으로 없앤다 (5일차)</div>''')

# 7. RDB
def table(name, cols, rows, col):
    head = "".join(f'<th style="padding:8px 12px;background:var(--{col});color:#fff;font-size:18px;text-align:left">{c}</th>' for c in cols)
    body = "".join("<tr>" + "".join(f'<td style="padding:7px 12px;border-top:1px solid var(--line);font-size:18px;{MONO};color:var(--navy);background:{"var(--orange-l)" if hl else "#fff"}">{v}</td>' for v in r) + "</tr>" for r, hl in rows)
    return f'<div class="col" style="gap:6px"><div style="font-size:21px;font-weight:800;color:var(--{col})">{name}</div><table style="border-collapse:collapse;border:2px solid var(--{col});border-radius:8px;overflow:hidden">{head and "<tr>"+head+"</tr>"}{body}</table></div>'


cust = table("customers (고객)", ["id", "name"], [(["7", "김하늘"], True), (["8", "이바다"], False)], "teal")
orders = table("orders (주문)", ["id", "customer_id", "product_id"], [(["501", "7", "123"], True), (["502", "8", "88"], False)], "violet")
prod = table("products (상품)", ["id", "name", "price"], [(["123", "운동화", "59000"], True), (["88", "양말", "3000"], False)], "orange")
R("w1d4-rdb", f'''<div class="row c" style="gap:18px;justify-content:center">{cust}<div class="col center" style="gap:4px">{icon("ArrowLeft",34,"teal",2.5)}<div style="font-size:16px;color:var(--slate)">customer_id</div></div>
{orders}<div class="col center" style="gap:4px">{icon("ArrowRight",34,"orange",2.5)}<div style="font-size:16px;color:var(--slate)">product_id</div></div>{prod}</div>
<div class="card fill-slate" style="padding:16px 24px;gap:8px"><div style="font-size:20px;{MONO};color:var(--navy)">SELECT c.name FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.product_id = 123;</div>
<p style="font-size:20px">→ <b style="color:var(--orange)">김하늘</b> · 표와 표를 <b style="color:var(--navy)">키(id)</b>로 연결하고, SQL로 조건에 맞는 줄을 골라 합친다</p></div>''')

# 8. 캐시
R("w1d4-cache", f'''<div class="row" style="gap:20px;align-items:center">
<div class="col center" style="width:220px;gap:8px">{ic("Server","navy",96)}<div style="font-size:24px;font-weight:800;color:var(--navy)">앱 서버</div></div>
<div class="col grow" style="gap:18px">
 <div class="card fill-green" style="gap:10px;padding:18px 22px"><div class="row c" style="gap:12px"><span class="chip" style="background:var(--green);color:#fff;font-size:20px">① 먼저 캐시에</span><h3 style="font-size:24px">있으면 — 캐시 적중 (hit)</h3></div>
  <div class="row c" style="gap:14px">{aws("Arch_Amazon-ElastiCache_48",56)}<p style="font-size:20px">Redis · Valkey (메모리) → <b style="color:var(--green)">1ms 안에</b> 바로 응답</p></div></div>
 <div class="card fill-orange" style="gap:10px;padding:18px 22px"><div class="row c" style="gap:12px"><span class="chip orange" style="font-size:20px">② 없으면 DB에서</span><h3 style="font-size:24px">없으면 — 캐시 실패 (miss)</h3></div>
  <div class="row c" style="gap:14px">{aws("Arch_Amazon-RDS_48",56)}<p style="font-size:20px">DB에서 가져오고(수~수십 ms) → <b style="color:var(--orange)">③ 캐시에 넣어 둔다</b> (TTL과 함께)</p></div></div>
</div></div>
<div class="card fill-slate" style="padding:14px 22px"><p style="font-size:20px"><b style="color:var(--navy)">어려운 점 = 캐시 무효화</b> — 가격을 바꿨는데 캐시에 옛 가격이 남아 있으면? (어제 DNS TTL과 같은 문제)</p></div>''')

# 9. 동기 vs 비동기
R("w1d4-sync-async", f'''<div class="card" style="gap:12px;border-color:var(--red)"><div class="row c" style="gap:12px"><span class="chip" style="background:var(--red);color:#fff;font-size:20px">동기</span><h3 style="font-size:24px">직접 부르고 응답을 기다린다 — 전화 주문</h3></div>
<div class="row c" style="gap:12px;justify-content:center">
 <div class="col center" style="gap:4px;width:150px">{ic("ShoppingCart","teal",64)}<div style="font-size:19px;font-weight:800">주문 서비스</div></div>
 <div class="col center" style="gap:2px">{arrow(size=34)}<div style="font-size:16px;color:var(--slate)">기다리는 중…</div></div>
 <div class="col center" style="gap:4px;width:150px">{ic("Bell","red",64)}<div style="font-size:19px;font-weight:800">알림 서비스</div><div style="font-size:16px;color:var(--red);font-weight:700">느려지거나 죽으면</div></div>
 {arrow(size=34)}<div class="box" style="background:var(--red-l);color:var(--red);font-size:20px">주문도 함께 실패 — 장애 전파</div></div></div>
<div class="card" style="gap:12px;border-color:var(--green)"><div class="row c" style="gap:12px"><span class="chip" style="background:var(--green);color:#fff;font-size:20px">비동기</span><h3 style="font-size:24px">큐에 맡기고 바로 돌아간다 — 주문서 꽂이</h3></div>
<div class="row c" style="gap:12px;justify-content:center">
 <div class="col center" style="gap:4px;width:150px">{ic("ShoppingCart","teal",64)}<div style="font-size:19px;font-weight:800">주문 서비스</div><div style="font-size:16px;color:var(--slate)">생산자</div></div>{arrow(size=34)}
 <div class="col center" style="gap:4px"><div class="row" style="gap:4px;border:3px solid var(--orange);border-radius:12px;padding:8px 10px;background:var(--orange-l)">{"".join(f'<div style="width:34px;height:44px;background:#fff;border:2px solid var(--orange);border-radius:5px"></div>' for _ in range(5))}</div><div style="font-size:19px;font-weight:800">토픽 / 큐</div></div>{arrow(size=34)}
 <div class="col" style="gap:8px">{"".join(f'<div class="row c" style="gap:8px">{ic(i,"violet",46)}<div style="font-size:18px;font-weight:800">{t}</div></div>' for i,t in [("Bell","알림"),("Truck","배송"),("ChartColumn","분석")])}</div>
 <div class="box" style="background:var(--green-l);color:var(--green);font-size:19px">알림이 잠시 죽어도<br>일은 큐에 남는다</div></div></div>''')

# 10. 선착순 쿠폰 흐름
steps = [("Users", "slate", "1만 명 동시 클릭", ""), ("Hourglass", "teal", "① 대기열 · 속도 제한", "초과 요청은 429"),
         ("Hash", "orange", "② 원자적 카운터", "Redis DECR — 정확히 100장"), ("ListOrdered", "violet", "③ 큐에 넣기", "당첨! 즉시 응답"),
         ("Database", "violet", "④ 작업자가 저장", "DB에 천천히 확실하게")]
sc = []
for k, (i, c, t, d) in enumerate(steps):
    sc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:20px 12px">{ic(i,c,78)}<h3 style="font-size:22px">{t}</h3><p style="font-size:18px">{d}</p></div>')
    if k < len(steps) - 1:
        sc.append(arrow(size=30))
R("w1d4-coupon-flow", f'''<div class="row flow" style="gap:8px">{"".join(sc)}</div>
<div class="row" style="gap:14px"><div class="card fill-orange grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">빠르게 판정할 일</b> → 메모리(Redis)</p></div>
<div class="card fill-violet grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">확실하게 기록할 일</b> → 큐(Kafka) → DB</p></div>
<div class="card fill-green grow" style="padding:14px 20px;flex-direction:row;align-items:center;gap:10px">{icon("ChartLine",34,"green",2)}<p style="font-size:20px"><b style="color:var(--navy)">⑤ 대시보드</b>로 수량·지연·에러 감시</p></div></div>''')

# 11. 모놀리식 vs MSA
mods = "".join(f'<div class="box" style="background:#fff;border:2px solid var(--line);color:var(--navy);font-size:20px">{m}</div>' for m in ["회원", "상품", "주문", "결제", "알림"])
svcs = "".join(f'<div class="col center" style="gap:6px"><div class="card center" style="padding:12px 10px;gap:6px;border-color:var(--{c});width:150px">{icon(i,40,c,2)}<div style="font-size:19px;font-weight:800;color:var(--navy)">{t}</div></div><div class="row" style="gap:4px">{icon("Database",26,"slate",2)}<span style="font-size:15px;color:var(--slate)">자기 DB</span></div></div>'
               for i, c, t in [("User", "teal", "회원"), ("Tag", "teal", "상품"), ("ShoppingCart", "orange", "주문"), ("CreditCard", "violet", "결제"), ("Bell", "green", "알림")])
R("w1d4-mono-vs-msa", f'''<div class="row" style="gap:26px;align-items:stretch">
<div class="card fill-slate center" style="width:360px;gap:12px"><div class="tag">MONOLITHIC</div><h3 style="font-size:27px">모놀리식</h3>
 <div class="card" style="width:100%;gap:8px;padding:16px;border-color:var(--navy);border-width:3px">{mods}</div>
 <div class="row c" style="gap:8px">{icon("Database",40,"navy",2)}<span style="font-size:19px;font-weight:700">DB 하나</span></div>
 <p style="font-size:19px">하나로 빌드 · 하나로 배포<br>작은 팀에 가장 효율적</p></div>
<div class="card grow center" style="gap:12px"><div class="tag">MICROSERVICES</div><h3 style="font-size:27px">마이크로서비스 (MSA)</h3>
 <div class="row" style="gap:10px;justify-content:center">{svcs}</div>
 <div class="box" style="background:var(--slate-l);color:var(--navy);font-size:19px;width:100%">서비스끼리 API · 이벤트(큐)로 대화 — 함수 호출이 <b>네트워크 호출</b>로 바뀐다</div>
 <div class="row" style="gap:10px;width:100%"><div class="box grow" style="background:var(--green-l);color:var(--green);font-size:18px">독립 배포 · 부분 확장 · 팀별 소유</div><div class="box grow" style="background:var(--red-l);color:var(--red);font-size:18px">지연 · 장애 전파 · 데이터 일관성 · 운영 복잡도</div></div></div></div>''')

# 12. 왜 Docker
conds = [("Code", "앱 코드"), ("Package", "런타임 · 버전"), ("Library", "라이브러리"), ("Settings", "설정 (환경 변수)"), ("Plug", "포트"), ("Terminal", "실행 명령")]
cb = "".join(f'<div class="row c" style="gap:10px;background:#fff;border-radius:10px;padding:10px 12px">{icon(i,30,"teal",2)}<span style="font-size:19px;font-weight:700;color:var(--navy)">{t}</span></div>' for i, t in conds)
targets = "".join(f'<div class="row c" style="gap:12px">{ic(i,c,58)}<div style="font-size:21px;font-weight:800;color:var(--navy)">{t}</div></div>' for i, c, t in [("Laptop", "teal", "내 노트북"), ("Users", "teal", "동료 컴퓨터"), ("FlaskConical", "orange", "테스트 서버"), ("Cloud", "violet", "AWS")])
R("w1d4-why-docker", f'''<div class="row flow" style="gap:18px">
<div class="card fill-teal" style="width:420px;gap:10px"><div class="row c" style="gap:12px">{icon("Container",44,"teal",2)}<h3 style="font-size:26px">컨테이너 이미지</h3></div>
 <div class="grid" style="grid-template-columns:1fr 1fr;gap:8px">{cb}</div><p style="font-size:18px">코드와 실행 조건을 한 상자에</p></div>
<div class="col center" style="gap:6px;justify-content:center">{arrow(size=44)}<div style="font-size:19px;font-weight:800;color:var(--slate)">어디서든</div></div>
<div class="card grow" style="gap:16px;justify-content:center">{targets}</div>
<div class="col center" style="gap:6px;justify-content:center">{arrow(size=44)}</div>
<div class="card fill-green center" style="width:250px;gap:10px;justify-content:center">{icon("CircleCheck",70,"green",2)}<h3 style="font-size:25px">똑같이 실행</h3><p style="font-size:18px">"제 컴퓨터에선<br>되는데요" 끝</p></div></div>
<div class="note">DB · 캐시 · 큐도 이미지로 — 2주차에 docker run 한 줄, Compose 파일 하나로 띄운다</div>''')


# 13. 폭주 트래픽 차트
def burst_chart():
    if only and "w1d4-burst" not in only:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    import math
    for f in (Path.home() / ".fonts").glob("Pretendard-*.otf"):
        fm.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Pretendard"
    xs = [i / 12 for i in range(0, 24 * 12 + 1)]
    base = [100 + 60 * math.sin((x - 8) / 24 * 2 * math.pi) for x in xs]
    burst = [b + (2600 if abs(x - 12) < 0.3 else 0) for x, b in zip(xs, base)]
    fig, ax = plt.subplots(figsize=(12, 4.6), dpi=220)
    ax.plot(xs, burst, color="#C8651B", lw=2.4)
    ax.fill_between(xs, burst, color="#C8651B", alpha=0.08)
    avg = sum(burst) / len(burst)
    ax.axhline(avg, color="#0089A0", lw=2, ls="--")
    ax.text(23.8, avg + 90, f"하루 평균 약 {avg:,.0f}건/초", ha="right", fontsize=14, color="#006A7C", fontweight="bold")
    ax.annotate("쿠폰 오픈 12:00\n피크 약 2,800건/초 — 평균의 수십 배", xy=(12, 2750), xytext=(14.2, 2300), fontsize=14, color="#C8651B", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#C8651B", lw=1.6))
    ax.set_xlim(0, 24); ax.set_ylim(0, 3100)
    ax.set_xticks(range(0, 25, 3)); ax.set_xticklabels([f"{h}시" for h in range(0, 25, 3)], fontsize=13, color="#475569")
    ax.set_yticks([0, 1000, 2000, 3000]); ax.set_yticklabels(["0", "1,000", "2,000", "3,000"], fontsize=12, color="#475569")
    ax.set_ylabel("초당 요청 수", fontsize=13, color="#475569")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"):
        ax.spines[s_].set_color("#CBD5E1")
    ax.grid(axis="y", color="#EEF2F6")
    fig.text(0.01, 0.01, "※ 이해를 돕기 위한 가상의 예시 데이터", fontsize=11, color="#94A3B8")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "w1d4-burst.png", facecolor="white"); plt.close(fig)
    print("ok w1d4-burst")


burst_chart()
