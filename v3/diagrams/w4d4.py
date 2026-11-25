"""4주차 4일차 다이어그램. 실행: python3 diagrams/w4d4.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week4" / "day4"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def card(t, sub, c, i, mono=False, w=""):
    f = MONO if mono else ""
    ww = f"width:{w}px;" if w else ""
    return f'<div class="card center grow" style="{ww}gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,44)}<b style="font-size:18px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


def pod(t, c="teal"):
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:15px;{MONO};border:1.5px solid var(--{c})">{t}</div>'


# 1. 남북 vs 동서
R("w4d4-ns-ew", f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="col" style="gap:8px;width:220px">{card("손님", "브라우저 · k6", "slate", "Users")}</div>
<div class="col center" style="gap:4px">{arrow(size=24)}<span style="font-size:14px;color:var(--orange);font-weight:700">남북<br>north-south</span></div>
<div class="col" style="gap:8px;width:260px">{card("Envoy Gateway", "1일차 · 입구<br>Host · 경로 · 카나리", "orange", "DoorOpen")}</div>
<div class="col center" style="gap:4px">{arrow(size=24)}</div>
<div class="card" style="flex:1;gap:10px;padding:14px;border-color:var(--violet);background:#FBFAFF"><div class="row c" style="gap:8px">{icon("Network",24,"violet",2)}<b style="font-size:20px;color:var(--navy)">devmart 안 — 동서 (east-west) = 서비스 메시의 영역</b></div>
<div class="row" style="gap:10px;align-items:center">{pod("web")}{arrow(size=18)}{pod("order-api")}{arrow(size=18)}{pod("catalog-api")}{arrow(size=18)}{pod("db")}</div>
<div class="row" style="gap:10px;align-items:center">{pod("order-api")}{arrow(size=18)}{pod("redis")}{arrow(size=18)}{pod("order-worker")}</div>
<span style="font-size:16px;color:var(--slate)">지금은 평문 · 아무나 부를 수 있다 · 재시도는 코드에 (CATALOG_RETRIES) · 누가 누구를 부르는지 지도가 없다</span></div></div>
<div class="row" style="gap:14px">{note("orange", "입구(Gateway)는 <b style='color:var(--navy)'>밖에서 안으로</b> — 1일차")}{note("violet", "메시는 <b style='color:var(--navy)'>안에서 안으로</b> — 암호화 · 허가 · 재시도 · 지표를 <b style='color:var(--navy)'>코드 밖에서</b>")}</div>''', w=1750)

# 2. sidecar vs ambient
def node(title, inner, c):
    return f'<div class="card" style="flex:1;gap:8px;padding:12px;border-color:var(--{c})"><b style="font-size:17px;color:var(--navy)">{title}</b>{inner}</div>'


sc = node("노드 1", f'<div class="row" style="gap:6px">{pod("order-api<br>+ envoy", "orange")}{pod("catalog-api<br>+ envoy", "orange")}</div>', "orange")
sc2 = node("노드 2", f'<div class="row" style="gap:6px">{pod("catalog-api<br>+ envoy", "orange")}{pod("web<br>+ envoy", "orange")}</div>', "orange")
am = node("노드 1", f'<div class="row" style="gap:6px">{pod("order-api")}{pod("catalog-api")}</div>{pod("ztunnel (노드에 하나)", "violet")}', "teal")
am2 = node("노드 2", f'<div class="row" style="gap:6px">{pod("catalog-api")}{pod("waypoint (필요할 때)", "red")}</div>{pod("ztunnel (노드에 하나)", "violet")}', "teal")
R("w4d4-sidecar-ambient", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:10px;padding:14px;border-color:var(--orange)"><b style="font-size:22px;color:var(--navy)">sidecar 모드 — Pod마다 Envoy</b>
<div class="row" style="gap:10px">{sc}{sc2}</div>
<span style="font-size:16px;color:var(--navy)">· 모든 Pod에 프록시 컨테이너 주입 → <b>Pod 재시작</b>이 필요<br>· L4 · L7 기능을 늘 전부 — Pod마다 메모리 수십 MB<br>· 2017년부터, 가장 성숙</span></div>
<div class="card" style="flex:1;gap:10px;padding:14px;border-color:var(--teal)"><b style="font-size:22px;color:var(--navy)">ambient 모드 — 오늘 쓰는 것</b>
<div class="row" style="gap:10px">{am}{am2}</div>
<span style="font-size:16px;color:var(--navy)">· <b>ztunnel</b>(L4: mTLS · 신원 · L4 허가)은 노드마다 하나<br>· <b>waypoint</b>(L7: 경로 · 나누기 · 장애 주입)는 필요한 곳에만<br>· 네임스페이스 라벨 하나로 등록 — <b>Pod 재시작 없음</b></span></div></div>
<div class="row" style="gap:14px">{note("orange", "sidecar = 집집마다 경비원")}{note("teal", "ambient = 동네 경비 초소(ztunnel) + 필요한 건물에만 안내 데스크(waypoint)")}</div>''', w=1750)

# 3. ambient 흐름
R("w4d4-ambient-flow", f'''<div class="row" style="gap:6px;align-items:center">
{card("order-api", "평문으로 보낸다<br>(코드 그대로)", "slate", "Box", True)}{arrow(size=20)}
{card("ztunnel (노드 1)", "가로채서<br>mTLS로 감싼다", "violet", "Lock", True)}{arrow(size=20)}
{card("waypoint", "L7: 90/10 나누기<br>장애 주입 · 타임아웃<br>허가(AuthorizationPolicy)", "red", "Signpost", True)}{arrow(size=20)}
{card("ztunnel (노드 2)", "mTLS를 풀고<br>신원 확인", "violet", "LockOpen", True)}{arrow(size=20)}
{card("catalog-api", "평문으로 받는다", "slate", "Box", True)}</div>
<div class="row" style="gap:10px;align-items:stretch"><div class="card" style="flex:1;gap:6px;padding:12px;border-color:var(--teal)"><div class="row c" style="gap:8px">{icon("ShieldCheck",24,"teal",2)}<b style="font-size:19px;color:var(--navy);{MONO}">istiod</b><span style="font-size:16px;color:var(--slate)">— 설정을 나눠 주고(xDS), Pod마다 <b>신원 인증서</b>를 발급한다: <span style="{MONO}">spiffe://cluster.local/ns/devmart/sa/default</span></span></div></div></div>
<div class="row" style="gap:14px">{note("violet", "ztunnel 사이는 <b style='color:var(--navy)'>HBONE</b>(HTTP/2 CONNECT + mTLS, 포트 15008) 터널")}{note("red", "waypoint를 거치지 않는 길(Pod IP로 바로)은 <b style='color:var(--navy)'>L7 정책도 거치지 않는다</b>")}</div>''', w=1750)
