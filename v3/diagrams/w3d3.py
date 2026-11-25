"""3주차 3일차 다이어그램. 실행: python3 diagrams/w3d3.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week3" / "day3"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def comp(name, sub, c, i, w=None, mono=True):
    ws = f"width:{w}px;" if w else ""
    nf = MONO if mono else ""
    return f'''<div class="card center grow" style="{ws}gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,48)}
<div style="font-size:19px;font-weight:900;color:var(--navy);{nf}">{name}</div><div style="font-size:15px;color:var(--slate);text-align:center">{sub}</div></div>'''


def pod(t, c="teal"):
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:15px;{MONO};border:1.5px solid var(--{c})">{t}</div>'


# 1. Compose 한 대 vs 클러스터
def host(name, pods, c="slate", dead=False):
    bg = "var(--red-l)" if dead else "#fff"
    bc = "var(--red)" if dead else f"var(--{c})"
    inner = "".join(pod(p, "red" if dead else "teal") for p in pods)
    lab = f'<span class="chip" style="font-size:13px;background:var(--red);color:#fff">꺼짐</span>' if dead else ""
    return f'<div class="card" style="gap:6px;padding:10px;border-color:{bc};background:{bg};width:200px"><div class="row c" style="gap:6px">{icon("Server",22,"red" if dead else c,2)}<b style="font-size:17px;{MONO};color:var(--navy)">{name}</b>{lab}</div>{inner}</div>'


R("w3d3-why-k8s", f'''<div class="row" style="gap:20px;align-items:stretch">
<div class="card" style="gap:10px;padding:16px;width:560px;border-color:var(--slate)"><div class="row c" style="gap:8px">{icon("Laptop",28,"slate",2)}<b style="font-size:21px;color:var(--navy)">Docker Compose — 컴퓨터 한 대</b></div>
<div class="row" style="gap:10px">{host("내 노트북", ["web", "order-api", "catalog-api", "order-worker", "redis · db"])}
<div class="col" style="gap:8px;flex:1;justify-content:center">
<div class="box" style="background:var(--slate-l);color:var(--navy);font-size:16px;text-align:left">한 대가 꺼지면 <b>전부</b> 멈춘다</div>
<div class="box" style="background:var(--slate-l);color:var(--navy);font-size:16px;text-align:left">한 대의 CPU · 메모리가 한계</div>
<div class="box" style="background:var(--slate-l);color:var(--navy);font-size:16px;text-align:left">어디에 놓을지는 <b>사람이</b> 정한다</div></div></div></div>
<div class="col center" style="justify-content:center">{arrow(size=36)}</div>
<div class="card" style="gap:10px;padding:16px;flex:1;border-color:var(--teal)"><div class="row c" style="gap:8px">{icon("Ship",28,"teal",2)}<b style="font-size:21px;color:var(--navy)">Kubernetes — 여러 대를 한 덩어리로</b></div>
<div class="row" style="gap:10px">{host("노드 1", ["web", "order-api"], "teal")}{host("노드 2", ["catalog-api", "order-api"], "teal", dead=True)}{host("노드 3", ["order-worker", "catalog-api ← 다시 띄움"], "teal")}</div>
<div class="box" style="background:var(--teal-l);color:var(--navy);font-size:16px">노드 하나가 꺼져도 <b>다른 노드에 다시 띄운다</b> · 어디에 놓을지는 <b>스케줄러가</b> 정한다</div></div></div>
<div class="row" style="gap:14px">{note("teal", "사람이 하던 일 — 배치 · 재시작 · 개수 맞추기 · 교체 — 을 <b style='color:var(--navy)'>클러스터가 대신</b>")}{note("orange", "대가: 배울 것과 움직이는 부품이 <b style='color:var(--navy)'>훨씬 많다</b>")}</div>''', w=1650)

# 2. 역사
hist = [("2003~", "Borg", "구글 내부 클러스터 관리", "slate"), ("2013", "Docker · Omega", "컨테이너 대중화", "slate"), ("2014.6", "Kubernetes 공개", "Borg 경험을 오픈소스로", "teal"),
        ("2015.7", "v1.0 · CNCF", "재단에 기증", "teal"), ("2018", "CNCF 졸업", "첫 졸업 프로젝트", "teal"), ("2022", "dockershim 제거", "v1.24 · containerd 직접", "orange"), ("2026.8", "v1.37", "1년 3번 릴리스", "orange")]
hc = []
for k, (y, t, d, c) in enumerate(hist):
    hc.append(f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:17px;font-weight:900;color:var(--{c});{MONO}">{y}</div><b style="font-size:18px;color:var(--navy);text-align:center">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{d}</span></div>')
    if k < len(hist) - 1:
        hc.append(arrow(size=18))
R("w3d3-history", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(hc)}</div>
<div class="row" style="gap:14px">{note("slate", "Borg 논문 (Verma 외 2015) · <b style='color:var(--navy)'>Borg, Omega, and Kubernetes</b> (Burns 외 2016)")}{note("teal", "2026년 1월 CNCF 조사: 컨테이너 사용자의 <b style='color:var(--navy)'>82%</b>가 운영 환경에서 Kubernetes")}</div>''', w=1650)

# 3. 아키텍처
cp = f'''<div style="border:3px solid var(--violet);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:10px;background:#FBFAFF">
<div class="row c" style="gap:8px">{icon("Building2",28,"violet",2)}<b style="font-size:21px;color:var(--navy)">컨트롤 플레인 — 본부</b><span style="font-size:16px;color:var(--slate);{MONO}">devmart-control-plane</span></div>
<div class="row" style="gap:10px">{comp("kube-apiserver", "유일한 창구<br>모든 요청은 여기로", "violet", "Router")}{comp("etcd", "클러스터의 장부<br>원하는 상태 저장", "violet", "Database")}{comp("kube-scheduler", "Pod를 놓을<br>노드 고르기", "violet", "Scale")}{comp("controller-manager", "원하는 상태로<br>맞추는 반복", "violet", "RefreshCw")}</div></div>'''


def node(n):
    return f'''<div class="card grow" style="gap:8px;padding:12px;border-color:var(--teal)"><div class="row c" style="gap:6px">{icon("Server",22,"teal",2)}<b style="font-size:18px;{MONO};color:var(--navy)">{n}</b></div>
<div class="row" style="gap:6px">{pod("kubelet","orange")}{pod("containerd","orange")}{pod("kube-proxy","orange")}</div>
<div class="row" style="gap:6px">{pod("Pod")}{pod("Pod")}</div></div>'''


R("w3d3-architecture", f'''<div class="row" style="gap:16px;align-items:center">
<div class="card center" style="width:190px;gap:6px;padding:14px;border-color:var(--navy)">{ic("Terminal","navy",54)}<b style="font-size:20px;{MONO};color:var(--navy)">kubectl</b><span style="font-size:15px;color:var(--slate);text-align:center">나<br>(~/.kube/config)</span></div>
<div class="col center" style="gap:2px">{arrow(size=30)}<span style="font-size:14px;{MONO};color:var(--slate)">HTTPS :6443</span></div>
<div style="flex:1">{cp}</div></div>
<div class="row c" style="gap:10px;justify-content:center">{icon("ArrowDown",28,"slate",2.5)}<span style="font-size:16px;color:var(--slate)">kubelet이 apiserver를 지켜보다가(watch) 자기 노드에 배정된 Pod를 띄운다</span>{icon("ArrowUp",28,"slate",2.5)}</div>
<div class="row" style="gap:12px">{node("devmart-worker")}{node("devmart-worker2")}</div>
<div class="row" style="gap:14px">{note("violet", "본부는 <b style='color:var(--navy)'>결정하고 기록</b>한다 — 컨테이너를 직접 띄우지 않는다")}{note("orange", "노드의 <b style='color:var(--navy)'>kubelet</b>이 현장 반장 — containerd에게 시켜서 띄운다")}</div>''', w=1650)

# 4. Pod 하나가 뜨기까지
steps = [("1", "kubectl", "원하는 상태를\n보낸다", "navy", "Terminal"), ("2", "apiserver", "검사 후\netcd에 저장", "violet", "Router"), ("3", "scheduler", "노드 고르기\nnodeName 기록", "violet", "Scale"),
         ("4", "kubelet", "내 노드 몫\n발견 (watch)", "orange", "Eye"), ("5", "containerd", "이미지 받고\n컨테이너 실행", "orange", "Container"), ("6", "kubelet", "상태 보고\nRunning", "teal", "Activity")]
sc = []
for k, (n, t, d, c, i) in enumerate(steps):
    sc.append(f'<div class="card center grow" style="gap:6px;padding:12px 6px;border-color:var(--{c})"><div style="font-size:16px;font-weight:900;color:var(--{c})">{n}</div>{ic(i,c,46)}<b style="font-size:18px;{MONO};color:var(--navy)">{t}</b><span style="font-size:14px;color:var(--slate);white-space:pre-line;text-align:center">{d}</span></div>')
    if k < len(steps) - 1:
        sc.append(arrow(size=18))
R("w3d3-pod-flow", f'''<div class="row flow" style="gap:4px;align-items:center">{"".join(sc)}</div>
<div class="row" style="gap:14px">{note("violet", "모두 <b style='color:var(--navy)'>apiserver를 통해서만</b> 말한다 — 서로 직접 부르지 않는다")}{note("teal", "kubectl은 '저장됐다'까지만 기다린다 — 실제 실행은 <b style='color:var(--navy)'>나중에, 비동기로</b>")}</div>''', w=1650)

# 5. 선언형 · reconcile
R("w3d3-reconcile", f'''<div class="row" style="gap:18px;align-items:center">
<div class="card center" style="width:300px;gap:8px;padding:16px;border-color:var(--violet)">{ic("FileText","violet",54)}<b style="font-size:21px;color:var(--navy)">원하는 상태 (spec)</b><span style="font-size:17px;{MONO};color:var(--slate)">replicas: 2</span><span style="font-size:15px;color:var(--slate)">etcd에 저장</span></div>
<div class="card center" style="flex:1;gap:10px;padding:16px;border-color:var(--orange);background:#FFFBF5">
<div class="row c" style="gap:8px">{icon("RefreshCw",32,"orange",2.2)}<b style="font-size:22px;color:var(--navy)">컨트롤러의 반복 (reconcile loop)</b></div>
<div class="row" style="gap:8px;align-items:center">
<div class="box grow" style="background:#fff;border:1.5px solid var(--orange);font-size:17px;color:var(--navy)"><b>1 관찰</b><br>지금 몇 개?</div>{arrow(size=18)}
<div class="box grow" style="background:#fff;border:1.5px solid var(--orange);font-size:17px;color:var(--navy)"><b>2 비교</b><br>원하는 것과 차이?</div>{arrow(size=18)}
<div class="box grow" style="background:#fff;border:1.5px solid var(--orange);font-size:17px;color:var(--navy)"><b>3 행동</b><br>모자라면 만들고<br>남으면 지운다</div></div>
<span style="font-size:15px;color:var(--slate)">차이가 0이 될 때까지 · 끝없이 반복</span></div>
<div class="card center" style="width:300px;gap:8px;padding:16px;border-color:var(--teal)">{ic("Activity","teal",54)}<b style="font-size:21px;color:var(--navy)">실제 상태 (status)</b><span style="font-size:17px;{MONO};color:var(--slate)">Running: 1 → 2</span><span style="font-size:15px;color:var(--slate)">kubelet이 보고</span></div></div>
<div class="row" style="gap:16px">
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--slate)"><b style="font-size:20px;color:var(--navy)">명령형 — "하나 더 띄워"</b><span style="font-size:18px">한 번 하고 끝 · 그 뒤에 죽으면 아무도 모른다</span><span style="font-size:15px;{MONO};color:var(--slate)">docker run · docker compose up</span></div>
<div class="card grow" style="gap:6px;padding:14px 18px;border-color:var(--teal)"><b style="font-size:20px;color:var(--teal)">선언형 — "늘 2개여야 해"</b><span style="font-size:18px">계속 지켜보다 어긋나면 고친다 — 같은 파일을 몇 번 적용해도 같은 결과</span><span style="font-size:15px;{MONO};color:var(--slate)">kubectl apply -f</span></div></div>
<div class="row" style="gap:14px">{note("orange", "비유: <b style='color:var(--navy)'>온도 조절기</b> — 24도로 맞춰 두면 알아서 켜고 끈다")}{note("violet", "학술: 되먹임 제어 (Hellerstein 외 2004) · CFEngine의 수렴 (Burgess 1998)")}</div>''', w=1650)

# 6. kind 구조
def knode(n, role, comps, c, port=""):
    inner = "".join(pod(x, "orange") for x in comps)
    p = f'<span class="chip" style="font-size:13px;background:var(--navy);color:#fff;{MONO}">{port}</span>' if port else ""
    return f'''<div class="card grow" style="gap:8px;padding:12px;border-color:var(--{c})"><div class="row c" style="gap:6px">{icon("Container",22,c,2)}<b style="font-size:17px;{MONO};color:var(--navy)">{n}</b></div>
<span style="font-size:14px;color:var(--slate)">{role}</span><div class="row" style="gap:6px;flex-wrap:wrap">{inner}</div>{p}</div>'''


R("w3d3-kind", f'''<div style="border:3px solid var(--navy);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:10px">
<div class="row c" style="gap:8px">{icon("Laptop",28,"navy",2)}<b style="font-size:21px;color:var(--navy)">내 노트북</b><span style="font-size:16px;color:var(--slate)">kubectl · kind 명령 · ~/.kube/config</span></div>
<div style="border:2.5px dashed var(--slate);border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:10px">
<div class="row c" style="gap:8px">{icon("Box",24,"slate",2)}<b style="font-size:19px;color:var(--navy)">Docker (Docker Desktop)</b><span style="font-size:15px;color:var(--slate)">노드 = 컨테이너 하나 · 이미지 kindest/node:v1.37.0</span></div>
<div class="row" style="gap:10px">{knode("devmart-control-plane", "컨트롤 플레인 + kubelet", ["apiserver", "etcd", "scheduler", "controller-mgr", "kubelet", "containerd"], "violet", "127.0.0.1:임의포트 → 6443 · 30080 → 30080")}
{knode("devmart-worker", "워커", ["kubelet", "containerd", "kube-proxy", "kindnet"], "teal")}{knode("devmart-worker2", "워커", ["kubelet", "containerd", "kube-proxy", "kindnet"], "teal")}</div>
<span style="font-size:15px;color:var(--slate)">컨테이너 안에 또 containerd가 있고, Pod는 그 안에서 뜬다 — <b style="color:var(--navy)">컨테이너 속의 컨테이너</b></span></div></div>
<div class="row" style="gap:14px">{note("teal", "kind = <b style='color:var(--navy)'>K</b>ubernetes <b style='color:var(--navy)'>IN</b> <b style='color:var(--navy)'>D</b>ocker — 원래 Kubernetes 자체를 시험하려고 만든 도구")}{note("orange", "진짜 서버 여러 대 대신 <b style='color:var(--navy)'>컨테이너 여러 개</b> — 지우면 흔적 없이 사라진다")}</div>''', w=1650)
