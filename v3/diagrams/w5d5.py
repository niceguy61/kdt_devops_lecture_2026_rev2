"""5주차 5일차 다이어그램. 실행: python3 diagrams/w5d5.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week5" / "day5"
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


def layer(wk, title, items, c, i):
    chips = "".join(f'<div class="box" style="background:#fff;color:var(--navy);font-size:15px;border:1.5px solid var(--{c})">{x}</div>' for x in items)
    return f'''<div class="row" style="gap:10px;align-items:stretch"><div class="card center" style="width:210px;gap:4px;padding:10px;border-color:var(--{c});background:var(--{c}-l)">{ic(i,c,38)}<b style="font-size:17px;color:var(--navy)">{wk}</b><span style="font-size:14px;color:var(--slate)">{title}</span></div>
<div class="row" style="flex:1;gap:8px;flex-wrap:wrap;align-content:center">{chips}</div></div>'''


R("w5d5-course-map", f'''<div class="col" style="gap:8px">
{layer("5주차", "AWS + Terraform + EKS", ["IAM · aws login", "VPC · 보안 그룹", "EC2 · ALB · Auto Scaling · S3", "Terraform · 원격 state · 모듈", "OIDC", "EKS · Access Entry · Pod Identity", "LBC · NLB · EBS"], "orange", "Cloud")}
{layer("4주차", "Kubernetes 운영", ["Helm", "Gateway API", "Prometheus · Grafana · 알림", "Argo CD (GitOps)", "Istio ambient", "RBAC · Kyverno"], "violet", "Ship")}
{layer("3주차", "MSA + Kubernetes 입문", ["서비스 나누기", "GitHub Actions CI", "kind · Pod · Deployment · Service", "ConfigMap · Secret · probe", "장애 훈련"], "teal", "Boxes")}
{layer("2주차", "Docker + Git", ["Git · GitHub · PR", "Dockerfile · 이미지", "Compose", "레지스트리"], "red", "Container")}
{layer("1주차", "클라우드 · 컴퓨팅 기초", ["리눅스 · 셸", "네트워크 · DNS · HTTP", "클라우드 모델 · 비용", "DevOps · SRE"], "slate", "BookOpen")}</div>
<div class="row" style="gap:14px">{note("orange", "아래층이 위층을 받친다 — 장애는 대개 <b style='color:var(--navy)'>아래층</b>(네트워크 · 신원 · 설정)에서 온다")}{note("violet", "하나로 꿴 것: <b style='color:var(--navy)'>원하는 상태를 적어 두면 무언가가 맞춘다</b>")}</div>''', w=1700)

R("w5d5-two-clusters", f'''<div class="row" style="gap:10px;align-items:center">
{card("PR 합치기", "devops-lab<br>APP_VERSION 2.2.0", "slate", "GitMerge")}{arrow(size=22)}
{card("CI", "빌드 · GHCR<br>sha-…", "orange", "Workflow")}{arrow(size=22)}
<div class="col" style="gap:8px;width:330px">{card("devmart-deploy", "봇 커밋 하나<br>devmart/kustomization.yaml images:", "violet", "FolderGit2")}</div>
<div class="col" style="gap:8px">{arrow(size=22)}{arrow(size=22)}</div>
<div class="col" style="gap:10px;flex:1"><div class="row" style="gap:8px;align-items:center">{card("Argo CD @ kind", "path: devmart", "teal", "RefreshCw")}{arrow(size=18)}{card("내 노트북", "localhost:30080", "teal", "Laptop")}</div>
<div class="row" style="gap:8px;align-items:center">{card("Argo CD @ EKS", "path: eks (→ ../devmart)", "orange", "RefreshCw")}{arrow(size=18)}{card("인터넷", "NLB 주소", "orange", "Globe")}</div></div></div>
<div class="row" style="gap:14px">{note("violet", "커밋 <b style='color:var(--navy)'>하나</b>가 클러스터 <b style='color:var(--navy)'>둘</b>에 — 오버레이가 원본을 참조하기 때문")}{note("orange", "CI는 어느 클러스터도 모른다 — 4주차 3일차의 경계 그대로")}</div>''', w=1800)


def node(az, pods, c, dead=False):
    st = "opacity:.45;border-style:dashed" if dead else ""
    return f'<div class="card" style="flex:1;gap:6px;padding:10px;border-color:var(--{c});{st}"><b style="font-size:16px;color:var(--navy)">노드 · {az}</b><div class="row" style="gap:4px;flex-wrap:wrap">{pods}</div></div>'


R("w5d5-az", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:8px;padding:12px;border-color:var(--teal)"><b style="font-size:19px;color:var(--navy)">① 노드 하나 종료 — 같은 AZ에 새 노드</b>
<div class="row" style="gap:8px">{node("2a", box("db","red",13)+box("catalog","violet",13), "slate", True)}{node("2c", box("catalog","violet",13)+box("order","violet",13), "teal")}</div>
<div class="row" style="gap:8px">{node("2a (새 노드)", box("db ← EBS 다시 붙음","red",13), "teal")}</div>
<span style="font-size:15px;color:var(--navy)">노드 그룹이 AZ 균형을 맞춰 2a에 새 노드 → db가 <b>같은 볼륨</b>으로 돌아온다 (몇 분)</span></div>
<div class="card" style="flex:1;gap:8px;padding:12px;border-color:var(--red)"><b style="font-size:19px;color:var(--navy)">② 2a 전체를 못 쓰게 (cordon + drain)</b>
<div class="row" style="gap:8px">{node("2a — 못 씀", box("EBS vol-… (2a)","red",13), "red", True)}{node("2c", box("db — Pending","red",13)+box("catalog","violet",13), "slate")}</div>
<span style="font-size:15px;color:var(--navy)"><span style="{MONO}">volume node affinity conflict</span> — 데이터가 2a에 있어 2c에서 뜰 수 없다</span>{box("해법: RDS Multi-AZ · 복제하는 DB · 백업에서 복구", "red", 14)}</div></div>
<div class="row" style="gap:14px">{note("teal", "상태 없는 서비스는 <b style='color:var(--navy)'>어디서나</b> 다시 뜬다")}{note("red", "상태 있는 것은 <b style='color:var(--navy)'>데이터가 있는 곳</b>에서만 — 그래서 DB는 따로 설계한다")}</div>''', w=1750)
