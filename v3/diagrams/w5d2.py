"""5주차 2일차 다이어그램. 실행: python3 diagrams/w5d2.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week5" / "day2"
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


def card(t, sub, c, i, mono=False):
    f = MONO if mono else ""
    return f'<div class="card center grow" style="gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,44)}<b style="font-size:18px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


def ec2(n, az):
    return f'<div class="card center" style="gap:4px;padding:10px;border-color:var(--orange);flex:1">{ic("Server","orange",36)}<b style="font-size:16px;color:var(--navy);{MONO}">EC2 {n}</b><span style="font-size:13px;color:var(--slate)">{az} · podinfo :9898<br>app-sg</span></div>'


R("w5d2-arch", f'''<div class="row" style="gap:8px;align-items:center">
<div class="col" style="gap:8px;width:170px">{card("손님", "브라우저", "slate", "Users")}</div>{arrow(size=22)}
<div class="col" style="gap:8px;width:230px">{card("ALB", "devmart-alb<br>public 서브넷 둘 · web-sg<br>리스너 :80", "teal", "Split")}</div>{arrow(size=22)}
<div class="col" style="gap:8px;width:210px">{card("대상 그룹", "devmart-tg :9898<br>상태 검사 /healthz", "teal", "Crosshair")}</div>{arrow(size=22)}
<div class="card" style="flex:1;gap:8px;padding:12px;border-color:var(--orange);background:#FFFBF6"><div class="row c" style="gap:8px">{icon("Layers",22,"orange",2)}<b style="font-size:18px;color:var(--navy)">Auto Scaling 그룹 devmart-asg</b><span style="font-size:14px;color:var(--slate)">원하는 수 2 · 최소 1 · 최대 3 · 시작 템플릿 devmart-lt</span></div>
<div class="row" style="gap:8px">{ec2("a", "2a")}{ec2("c", "2c")}</div></div>
{arrow(size=22)}
<div class="col" style="gap:8px;width:220px">{card("S3", "devmart-assets-…<br>역할로 읽기 (키 없음)", "violet", "Archive")}</div></div>
<div class="row" style="gap:10px">{box("IAM 역할 devmart-ec2-role = SSM 접속 + S3 읽기 → 인스턴스 프로파일로 EC2에 붙는다", "violet", 16)}</div>
<div class="row" style="gap:14px">{note("teal", "손님은 ALB 주소 하나만 안다 — 뒤의 서버가 몇 대인지, 죽었는지 모른다")}{note("orange", "app-sg는 <b style='color:var(--navy)'>ALB(web-sg)에서만</b> 9898을 받는다 · SSH 포트는 없다")}</div>''', w=1800)


def pair(k, a, c):
    return f'<div class="row" style="gap:8px;align-items:stretch"><div class="col" style="width:640px">{box(k, "violet", 16)}</div><div class="col center">{arrow(size=18)}</div><div class="col" style="width:640px">{box(a, c, 16)}</div></div>'


R("w5d2-k8s-map", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="col" style="flex:1;gap:8px"><div class="row" style="gap:8px"><b style="font-size:20px;color:var(--navy);width:680px">3 · 4주차 Kubernetes</b><b style="font-size:20px;color:var(--navy);width:640px">오늘 AWS</b></div>
{pair("Pod 템플릿 (Deployment spec)", "시작 템플릿 (AMI · 타입 · user data)", "orange")}
{pair("Deployment · ReplicaSet (replicas: 2)", "Auto Scaling 그룹 (원하는 수 2)", "orange")}
{pair("readiness · liveness probe", "대상 그룹 상태 검사 + ASG ELB 상태 검사", "teal")}
{pair("Service · Gateway (입구 하나)", "ALB + 리스너 + 대상 그룹", "teal")}
{pair("ServiceAccount (Pod의 신원)", "IAM 역할 + 인스턴스 프로파일", "violet")}
{pair("kubectl exec", "Session Manager", "slate")}
{pair("노드 여럿에 흩어 놓기", "AZ 둘에 흩어 놓기", "slate")}</div></div>
<div class="row" style="gap:14px">{note("violet", "같은 생각 — '원하는 수를 적어 두면 무언가가 맞춰 준다' — 이 VM 크기로")}{note("orange", "다른 점: 서버 하나가 뜨는 데 <b style='color:var(--navy)'>수십 초~몇 분</b>, Pod는 몇 초")}</div>''', w=1600)
