"""4주차 1일차 다이어그램. 실행: python3 diagrams/w4d1.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week4" / "day1"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def box(t, c, size=15):
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:{size}px;{MONO};border:1.5px solid var(--{c});text-align:left">{t}</div>'


def card(t, sub, c, i, w=None, mono=False):
    ws = f"width:{w}px;" if w else ""
    f = MONO if mono else ""
    return f'<div class="card center grow" style="{ws}gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,46)}<b style="font-size:19px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


# 1. Helm 개념
R("w4d1-helm", f'''<div class="row" style="gap:14px;align-items:center">
<div class="card" style="width:330px;gap:8px;padding:14px;border-color:var(--violet)"><div class="row c" style="gap:8px">{icon("Package",28,"violet",2)}<b style="font-size:21px;color:var(--navy)">차트 (chart)</b></div>
{box("Chart.yaml — 이름 · 버전", "violet")}{box("templates/ — 빈칸 뚫린 매니페스트<br>replicas: {{ .Values.replicaCount }}", "violet")}{box("values.yaml — 빈칸의 기본값", "violet")}
<span style="font-size:14px;color:var(--slate)">저장소: OCI 레지스트리(ghcr.io …) 또는 HTTP 저장소</span></div>
<div class="col center" style="gap:6px">{box("내 values.yaml<br>replicaCount: 2", "orange")}{icon("Plus",22,"slate",2)}</div>
<div class="card center" style="width:200px;gap:6px;padding:14px;border-color:var(--navy)">{ic("Terminal","navy",50)}<b style="font-size:20px;{MONO};color:var(--navy)">helm install</b><span style="font-size:14px;color:var(--slate);text-align:center">빈칸 채우기(렌더링)<br>→ apiserver로</span></div>
{arrow(size=28)}
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--teal)"><div class="row c" style="gap:8px">{icon("Layers",28,"teal",2)}<b style="font-size:21px;color:var(--navy)">릴리스 (release) <span style="{MONO}">podinfo</span></b></div>
<span style="font-size:15px;color:var(--slate)">클러스터에 설치된 차트 하나 — 버전 이력을 Secret에 남긴다</span>
<div class="row" style="gap:8px">{box("rev 1<br>install", "slate")}{box("rev 2<br>upgrade", "slate")}{box("rev 3<br>rollback → 1", "teal")}</div>
{box("Deployment · Service · HPA … (실제 리소스)", "teal")}</div></div>
<div class="row" style="gap:14px">{note("violet", "Kustomize는 <b style='color:var(--navy)'>완성된 YAML에 덧칠</b>, Helm은 <b style='color:var(--navy)'>빈칸을 채워 만든다</b>")}{note("teal", "남이 만든 add-on은 Helm으로 — <b style='color:var(--navy)'>values.yaml만 내 것</b>, 나머지는 차트를 믿는다")}</div>''', w=1650)

# 2. 외부 진입의 역사
hist = [("Service", "NodePort ·<br>LoadBalancer", "Service 하나 = 입구 하나", "slate", "DoorOpen"),
        ("2015 → 2020", "Ingress<br>(v1.19 정식)", "호스트 · 경로로 나누기<br>나머지는 어노테이션", "orange", "Signpost"),
        ("2023.10", "Gateway API v1.0", "역할별 리소스<br>표준 기능을 API에", "teal", "Network"),
        ("2025.11 발표", "ingress-nginx<br>은퇴 예고", "유지보수 인력 부족<br>보안 위험", "red", "TriangleAlert"),
        ("2026.3", "ingress-nginx<br>유지보수 종료", "패치 없음 —<br>그대로 쓰면 위험", "red", "Ban"),
        ("2026.6", "Gateway API v1.6", "TCP · UDP 라우팅도<br>표준으로", "teal", "Network")]
hc = []
for k, (y, t, d, c, i) in enumerate(hist):
    hc.append(f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c});{MONO}">{y}</div>{ic(i,c,42)}<b style="font-size:17px;color:var(--navy);text-align:center">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{d}</span></div>')
    if k < len(hist) - 1:
        hc.append(arrow(size=18))
R("w4d1-ingress-history", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(hc)}</div>
<div class="row" style="gap:14px">{note("orange", "Ingress의 한계: 표준이 너무 작아 기능마다 <b style='color:var(--navy)'>컨트롤러별 어노테이션</b> — 옮기기 어렵다")}{note("red", "은퇴한 것은 <b style='color:var(--navy)'>커뮤니티 ingress-nginx</b> — NGINX 자체도, Ingress API도 아니다")}</div>''', w=1700)


# 3. 역할별 리소스
def role(who, i, c, res, desc, ex):
    return f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="card center" style="width:230px;gap:4px;padding:10px;border-color:var(--{c})">{ic(i,c,42)}<b style="font-size:17px;color:var(--navy)">{who}</b></div>
<div class="col center">{arrow(size=22)}</div>
<div class="card" style="width:260px;gap:4px;padding:12px;border-color:var(--{c});background:var(--{c}-l)"><b style="font-size:20px;{MONO};color:var(--navy)">{res}</b><span style="font-size:15px;color:var(--slate)">{desc}</span></div>
<div class="box grow" style="background:#0F1E2E;color:#E2E8F0;font-size:15px;{MONO};text-align:left;white-space:pre">{ex}</div></div>'''


R("w4d1-gateway-roles", f'''<div class="col" style="gap:10px">
{role("인프라 제공자", "Building2", "violet", "GatewayClass", "어떤 구현으로? (Envoy Gateway)", "controllerName: gateway.envoyproxy.io/gatewayclass-controller")}
<div class="row c" style="gap:8px;padding-left:600px">{icon("ArrowDown",22,"slate",2)}<span style="font-size:14px;color:var(--slate)">gatewayClassName</span></div>
{role("클러스터 운영자", "ShieldCheck", "orange", "Gateway", "어느 포트로 · 누가 붙어도 되나", "listeners: [ { name: http, port: 80, protocol: HTTP } ]")}
<div class="row c" style="gap:8px;padding-left:600px">{icon("ArrowUp",22,"slate",2)}<span style="font-size:14px;color:var(--slate)">parentRefs — 라우트가 문에 '붙는다'</span></div>
{role("앱 개발자", "Code", "teal", "HTTPRoute", "어떤 경로를 · 어느 Service로", "rules: [ { path: /api/orders → order-api:8000 } ]")}</div>
<div class="row" style="gap:14px">{note("orange", "Ingress 하나에 섞여 있던 것을 <b style='color:var(--navy)'>세 사람 몫으로</b> 나눴다 — 권한(RBAC)도 따로 줄 수 있다")}{note("teal", "모든 리소스가 <b style='color:var(--navy)'>status.conditions</b>로 '받아들여졌나'를 말해 준다 — 장애 분석의 출발점")}</div>''', w=1650)

# 4. DevMart + Gateway
R("w4d1-devmart-gateway", f'''<div class="row" style="gap:12px;align-items:center">
<div class="card center" style="width:170px;gap:4px;padding:10px;border-color:var(--navy)">{ic("Laptop","navy",42)}<b style="font-size:15px;{MONO};color:var(--navy)">localhost:30080</b><span style="font-size:13px;color:var(--slate)">podinfo.localhost:30080</span></div>
{arrow(size=22)}
<div style="border:2.5px dashed var(--violet);border-radius:14px;padding:10px;display:flex;flex-direction:column;gap:8px;width:420px">
<div class="row c" style="gap:6px">{icon("Folder",22,"violet",2)}<b style="font-size:17px;color:var(--navy);{MONO}">envoy-gateway-system</b></div>
<div class="row" style="gap:8px">{card("envoy-gateway", "컨트롤러 — Gateway API를<br>읽어 Envoy를 설정(xDS)", "violet", "Cog", mono=True)}{card("Envoy", "실제 프록시<br>Service NodePort 30080", "orange", "Router", mono=True)}</div></div>
{arrow(size=22)}
<div style="border:2.5px dashed var(--teal);border-radius:14px;padding:10px;display:flex;flex-direction:column;gap:8px;flex:1">
<div class="row c" style="gap:6px">{icon("Folder",22,"teal",2)}<b style="font-size:17px;color:var(--navy);{MONO}">devmart</b><span style="font-size:14px;color:var(--slate)">Gateway devmart · HTTPRoute 셋</span></div>
<div class="col" style="gap:6px">{box("/api/orders → order-api:8000", "violet")}{box("/api/ → catalog-api:8000", "teal")}{box("/ → web:80 (정적 파일)", "orange")}{box("Host: podinfo.localhost → podinfo (default)", "slate")}</div></div></div>
<div class="row" style="gap:14px">{note("orange", "API 게이트웨이 역할이 nginx에서 <b style='color:var(--navy)'>Envoy로</b> — 요청 ID도 Envoy가 붙인다 (x-request-id)")}{note("violet", "<b style='color:var(--navy)'>컨트롤러와 프록시가 따로</b> — 3주차 컨트롤 플레인 · 데이터 플레인과 같은 모양")}</div>''', w=1700)

# 5. 상태 읽기
rows = [("parentRefs 이름 오타", "status 자체가 비어 있다", "아무 컨트롤러도 '내 것'이라 하지 않음", "404"),
        ("hostnames 불일치", "Accepted True", "붙긴 했지만 그 Host로 오는 요청이 없다", "404"),
        ("backendRefs Service 이름 오타", "ResolvedRefs False · BackendNotFound", "문은 열렸는데 보낼 곳이 없다", "500"),
        ("다른 네임스페이스 Service", "ResolvedRefs False · RefNotPermitted", "ReferenceGrant가 없다", "500"),
        ("Gateway가 준비 안 됨", "Gateway Programmed False", "프록시가 아직 없다 · 포트 충돌", "연결 거부")]
tr = "".join(f'''<div class="row" style="gap:8px;align-items:stretch">
<div class="box" style="width:330px;background:#fff;border:1.5px solid var(--line);color:var(--navy);font-size:16px;text-align:left">{a}</div>
<div class="box" style="width:420px;background:#0F1E2E;color:#E2E8F0;font-size:15px;{MONO};text-align:left">{b}</div>
<div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:16px;text-align:left">{c}</div>
<div class="box" style="width:120px;background:var(--red-l);border:1.5px solid var(--red);color:var(--red);font-size:17px;{MONO};font-weight:800">{d}</div></div>''' for a, b, c, d in rows)
R("w4d1-route-status", f'''<div class="row" style="gap:8px;font-size:16px;color:var(--slate);font-weight:800"><div style="width:330px">무엇이 틀렸나</div><div style="width:420px">kubectl describe httproute</div><div class="grow">뜻</div><div style="width:120px">curl</div></div>
<div class="col" style="gap:8px">{tr}</div>
<div class="row" style="gap:14px">{note("teal", "순서: <b style='color:var(--navy)'>Gateway Programmed → Route Accepted → ResolvedRefs</b> → EndpointSlice → Pod")}{note("red", "404는 '길이 없다', 500은 '길은 있는데 끝이 막혔다' — 숫자가 <b style='color:var(--navy)'>어느 층</b>인지 알려 준다")}</div>''', w=1700)
