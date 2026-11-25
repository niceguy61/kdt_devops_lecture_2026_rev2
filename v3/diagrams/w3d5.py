"""3주차 5일차 다이어그램. 실행: python3 diagrams/w3d5.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week3" / "day5"
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


# 1. 설정 주입
R("w3d5-config", f'''<div class="row" style="gap:16px;align-items:center">
<div class="col" style="gap:12px;width:430px">
<div class="card" style="gap:8px;padding:14px;border-color:var(--teal)"><div class="row c" style="gap:8px">{icon("FileText",26,"teal",2)}<b style="font-size:20px;color:var(--navy)">ConfigMap <span style="{MONO}">devmart-config</span></b></div>
{box("DB_HOST: db<br>REDIS_HOST: redis<br>CATALOG_URL: http://catalog-api:8000", "teal")}<span style="font-size:15px;color:var(--slate)">비밀이 아닌 설정 — Git에 올린다</span></div>
<div class="card" style="gap:8px;padding:14px;border-color:var(--red)"><div class="row c" style="gap:8px">{icon("KeyRound",26,"red",2)}<b style="font-size:20px;color:var(--navy)">Secret <span style="{MONO}">devmart-db</span></b></div>
{box("DB_PASSWORD: ZjNh…  (base64)", "red")}<span style="font-size:15px;color:var(--slate)">비밀 — <b>kubectl create secret</b>으로, Git 밖에서</span></div></div>
<div class="col center" style="gap:6px">{arrow(size=30)}<span style="font-size:14px;{MONO};color:var(--slate)">envFrom<br>secretKeyRef</span></div>
<div class="card" style="flex:1;gap:10px;padding:16px;border-color:var(--violet)"><div class="row c" style="gap:8px">{icon("Box",28,"violet",2)}<b style="font-size:21px;{MONO};color:var(--navy)">catalog-api Pod</b></div>
{box("DB_HOST=db  REDIS_HOST=redis  CATALOG_URL=…<br>DB_NAME=catalog   (매니페스트에 직접)<br>DB_PASSWORD=f3a…   (Secret에서)", "violet", 16)}
<span style="font-size:16px;color:var(--navy)">이미지는 그대로 — <b>설정만 바꿔</b> 개발 · 운영에 같은 이미지 (1주차 4일차 12-Factor의 설정 원칙)</span>
<span style="font-size:16px;color:var(--red)">ConfigMap을 고쳐도 <b>환경 변수는 Pod가 뜰 때 한 번</b> 읽힌다 → rollout restart</span></div></div>
<div class="row" style="gap:14px">{note("red", "base64는 <b style='color:var(--navy)'>암호가 아니다</b> — 누구나 되돌린다. 지키는 것은 RBAC와 저장 시 암호화")}{note("orange", "<b style='color:var(--navy)'>enableServiceLinks: false</b> — Service 'db'가 DB_PORT=tcp://…를 몰래 넣는 것을 막는다")}</div>''', w=1650)

# 2. probe
def pcard(name, q, fail, c, i, ex):
    return f'''<div class="card grow" style="gap:8px;padding:14px;border-color:var(--{c})"><div class="row c" style="gap:8px">{ic(i,c,44)}<b style="font-size:21px;{MONO};color:var(--navy)">{name}</b></div>
<span style="font-size:18px;color:var(--navy)"><b>묻는 것</b> — {q}</span><span style="font-size:18px;color:var(--{c})"><b>실패하면</b> — {fail}</span>{box(ex, c)}</div>'''


R("w3d5-probes", f'''<div class="row" style="gap:14px;align-items:stretch">
{pcard("startupProbe", "다 켜졌나? (느린 앱)", "아직 다른 probe를 시작하지 않는다", "slate", "Hourglass", "켜지는 데 1분 걸리는 앱용")}
{pcard("readinessProbe", "손님 받을 준비가 됐나?", "Service 목록(EndpointSlice)에서 <b>뺀다</b> — 죽이지 않는다", "teal", "DoorOpen", "order-api → /ready (DB · 큐)")}
{pcard("livenessProbe", "살아 있나? 멈추지 않았나?", "kubelet이 컨테이너를 <b>다시 시작</b>한다", "red", "HeartPulse", "order-api → /health (이 프로세스만)")}</div>
<div class="row" style="gap:14px">{note("teal", "2일차 2교시: <b style='color:var(--navy)'>/health = liveness, /ready = readiness</b> — 이제 Kubernetes가 직접 묻는다")}{note("red", "/ready를 liveness에 쓰면 → redis가 잠깐 죽을 때 <b style='color:var(--navy)'>모든 order-api가 재시작</b>되는 2차 사고")}</div>''', w=1650)

# 3. requests / limits
R("w3d5-resources", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:10px;padding:16px;border-color:var(--violet)"><div class="row c" style="gap:8px">{icon("Scale",28,"violet",2)}<b style="font-size:21px;color:var(--navy)">requests — 예약 (스케줄러가 본다)</b></div>
<span style="font-size:17px;color:var(--navy)">"최소 이만큼은 있어야 해" — 노드의 <b>남은 예약 가능량</b>과 비교해 놓을 곳을 정한다</span>
<div class="row" style="gap:6px;align-items:flex-end">
<div class="col" style="gap:4px;width:150px"><div style="height:60px;background:var(--violet-l);border:2px solid var(--violet);border-radius:6px;font-size:13px;{MONO};padding:4px">catalog 64Mi</div><div style="height:40px;background:var(--violet-l);border:2px solid var(--violet);border-radius:6px;font-size:13px;{MONO};padding:4px">redis 32Mi</div><div style="height:90px;background:var(--slate-l);border:2px dashed var(--slate);border-radius:6px;font-size:13px;padding:4px">남은 예약</div><span style="font-size:14px;color:var(--slate);text-align:center">워커 노드</span></div>
<div class="col" style="gap:6px;flex:1"><span style="font-size:16px;color:var(--slate)">실제로 덜 써도 예약은 예약</span><span style="font-size:16px;color:var(--slate)">예약이 꽉 차면 → 새 Pod <b style="{MONO}">Pending</b> (4일차 too-big)</span></div></div></div>
<div class="card" style="flex:1;gap:10px;padding:16px;border-color:var(--red)"><div class="row c" style="gap:8px">{icon("Gauge",28,"red",2)}<b style="font-size:21px;color:var(--navy)">limits — 상한 (커널이 지킨다)</b></div>
<div class="row" style="gap:10px"><div class="card grow" style="gap:6px;padding:12px;border-color:var(--orange)"><b style="font-size:18px;color:var(--orange)">CPU 넘으면</b><span style="font-size:16px">느려진다 (throttling) — 죽지 않는다</span></div>
<div class="card grow" style="gap:6px;padding:12px;border-color:var(--red)"><b style="font-size:18px;color:var(--red)">메모리 넘으면</b><span style="font-size:16px">죽는다 — <b style="{MONO}">OOMKilled · Exit 137</b></span></div></div>
<span style="font-size:16px;color:var(--slate)">메모리는 늘려 줄 수 없는 자원 — 넘는 순간 커널이 프로세스를 끝낸다</span></div></div>
<div class="row" style="gap:14px">{note("violet", "requests 없음 = 스케줄러가 <b style='color:var(--navy)'>0으로 친다</b> → 한 노드에 몰려 서로 굶긴다")}{note("orange", "오늘 기준: 메모리 requests · limits는 꼭, <b style='color:var(--navy)'>CPU는 requests만</b> (limits는 상황 따라)")}</div>''', w=1650)


# 4. DevMart on K8s
def svc(n, sub, c, i, w=210):
    return f'<div class="card center" style="width:{w}px;gap:4px;padding:10px 6px;border-color:var(--{c})">{ic(i,c,42)}<b style="font-size:17px;{MONO};color:var(--navy)">{n}</b><span style="font-size:13px;color:var(--slate);text-align:center">{sub}</span></div>'


R("w3d5-devmart-k8s", f'''<div style="border:3px solid var(--navy);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:12px">
<div class="row c" style="gap:8px">{icon("Folder",26,"navy",2)}<b style="font-size:20px;color:var(--navy)">네임스페이스 devmart</b><span style="font-size:15px;color:var(--slate)">kubectl apply -k devmart/</span></div>
<div class="row" style="gap:10px;align-items:center">
<div class="card center" style="width:170px;gap:4px;padding:10px;border-color:var(--navy)">{ic("Laptop","navy",42)}<b style="font-size:16px;{MONO};color:var(--navy)">localhost:30080</b></div>{arrow(size=22)}
{svc("web", "nginx · NodePort 30080<br>ConfigMap: html · conf", "orange", "Globe")}{arrow(size=22)}
<div class="col" style="gap:10px">{svc("catalog-api ×2", "/api/ · Service :8000", "teal", "Package")}{svc("order-api ×2", "/api/orders · readiness /ready", "violet", "ShoppingCart")}</div>{arrow(size=22)}
<div class="col" style="gap:10px">{svc("db", "postgres:18 · Recreate<br>PVC db-data 1Gi", "slate", "Database")}{svc("redis", "큐 orders", "red", "ListOrdered")}</div>
<div class="col center" style="gap:4px">{icon("ArrowLeft",24,"slate",2)}</div>
{svc("order-worker ×2", "Service 없음<br>BRPOP → completed", "green", "Cog")}</div>
<div class="row" style="gap:10px">{box("ConfigMap devmart-config — 공통 설정", "teal")}{box("Secret devmart-db — DB_PASSWORD (손으로 만듦)", "red")}{box("ConfigMap db-init — SQL 두 개", "slate")}</div></div>
<div class="row" style="gap:14px">{note("teal", "Service 이름 = Compose 서비스 이름, 포트도 8000 그대로 → <b style='color:var(--navy)'>nginx 설정 · CATALOG_URL을 안 고쳤다</b>")}{note("slate", "Pod는 바뀌어도 데이터는 <b style='color:var(--navy)'>PVC</b>에 — db Pod를 지워도 주문이 남는다")}</div>''', w=1700)

# 5. 장애 진단 흐름
st = [("1", "증상", "브라우저 · curl\n어느 기능이?", "navy", "Monitor"), ("2", "어느 Service", "get endpointslices\n비었나?", "orange", "Split"),
      ("3", "어느 Pod", "get pods\nREADY · STATUS · RESTARTS", "teal", "Box"), ("4", "클러스터의 말", "describe\nEvents · Readiness", "violet", "Search"),
      ("5", "앱의 말", "logs (--previous)\n마지막 에러 줄", "red", "ScrollText"), ("6", "고치기", "파일 고치고 apply\n→ 다시 1로", "green", "Wrench")]
sc = []
for k, (n, t, d, c, i) in enumerate(st):
    sc.append(f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div>{ic(i,c,44)}<b style="font-size:19px;color:var(--navy)">{t}</b><span style="font-size:14px;{MONO};color:var(--slate);white-space:pre-line;text-align:center">{d}</span></div>')
    if k < len(st) - 1:
        sc.append(arrow(size=18))
R("w3d5-diagnose", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(sc)}</div>
<div class="row" style="gap:14px">{note("orange", "<b style='color:var(--navy)'>바깥에서 안으로</b> — 사용자 증상 → Service → Pod → 컨테이너 → 앱")}{note("red", "증거가 없는 문장은 보고서에 쓰지 않는다 — <b style='color:var(--navy)'>명령과 출력 한 줄</b>이 근거 (2일차 3교시)")}</div>''', w=1650)
