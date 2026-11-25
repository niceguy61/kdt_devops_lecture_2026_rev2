"""5주차 4일차 다이어그램. 실행: python3 diagrams/w5d4.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week5" / "day4"
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


def az(n):
    return f'''<div class="card" style="flex:1;gap:8px;padding:10px;border-style:dashed;border-color:var(--slate)"><b style="font-size:16px;color:var(--slate)">AZ ap-northeast-2{n}</b>
<div class="card" style="gap:6px;padding:8px;border-color:var(--teal);background:var(--teal-l)"><b style="font-size:15px;color:var(--navy)">public</b><span style="font-size:13px;color:var(--navy)">NLB 노드{" · NAT" if n == "a" else ""}</span></div>
<div class="card" style="gap:6px;padding:8px;border-color:var(--violet);background:var(--violet-l)"><b style="font-size:15px;color:var(--navy)">private — 노드 (EC2 t3.medium)</b>
<div class="row" style="gap:4px">{box("Pod 10.0.13x.x", "violet", 13)}{box("Pod", "violet", 13)}{box("Pod", "violet", 13)}</div></div></div>'''


R("w5d4-eks", f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="card" style="width:330px;gap:8px;padding:12px;border-color:var(--orange);background:#FFFBF6"><div class="row c" style="gap:8px">{icon("Cloud",22,"orange",2)}<b style="font-size:18px;color:var(--navy)">AWS가 운영하는 곳</b></div>
{card("EKS 컨트롤 플레인", "apiserver · etcd · 스케줄러<br>AZ 여럿에 복제 · $0.10/h", "orange", "Server")}
{box("내가 보는 것: 엔드포인트 URL 하나", "orange", 14)}</div>
<div class="col center" style="gap:4px">{arrow(size=24)}<span style="font-size:13px;color:var(--slate)">노드가<br>붙는다</span></div>
<div class="card" style="flex:1;gap:8px;padding:12px;border-color:var(--navy)"><div class="row c" style="gap:8px">{icon("Network",22,"navy",2)}<b style="font-size:18px;color:var(--navy)">내 계정 — VPC devmart-vpc (Terraform)</b></div>
<div class="row" style="gap:10px">{az("a")}{az("c")}</div>
<div class="row" style="gap:8px">{box("관리형 노드 그룹 = Auto Scaling 그룹 (2일차) + EKS가 관리", "orange", 14)}{box("VPC CNI: Pod가 VPC IP를 받는다", "violet", 14)}</div></div></div>
<div class="row" style="gap:14px">{note("orange", "kind의 control-plane 컨테이너 → AWS가 대신 운영하는 <b style='color:var(--navy)'>엔드포인트 하나</b>")}{note("violet", "kind의 worker 컨테이너 → <b style='color:var(--navy)'>private 서브넷의 EC2</b> — 밖으로는 NAT로")}</div>''', w=1800)

R("w5d4-identity", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--teal)"><b style="font-size:21px;color:var(--navy)">사람 → 클러스터 (Access Entry)</b>
<div class="row" style="gap:6px;align-items:center">{box("IAM user/devops-admin", "teal")}{arrow(size=18)}{box("Access Entry", "teal")}{arrow(size=18)}{box("AmazonEKSClusterAdminPolicy", "teal")}</div>
<span style="font-size:16px;color:var(--navy)">kubectl → <span style="{MONO}">aws eks get-token</span>(IAM 신원) → apiserver가 Access Entry로 <b>Kubernetes 권한</b>을 정한다 — 4주차 5일차 RBAC의 '누가'가 IAM이 된다</span></div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--violet)"><b style="font-size:21px;color:var(--navy)">Pod → AWS (Pod Identity)</b>
<div class="row" style="gap:6px;align-items:center">{box("SA kube-system/aws-load-balancer-controller", "violet")}{arrow(size=18)}{box("IAM 역할 devmart-lbc", "violet")}</div>
<span style="font-size:16px;color:var(--navy)">Pod Identity Agent가 그 SA의 Pod에 <b>역할의 임시 자격 증명</b>을 준다 — 2일차 EC2 인스턴스 프로파일의 Pod판</span></div></div>
<div class="row" style="gap:14px">{note("teal", "방향이 반대다: <b style='color:var(--navy)'>IAM → Kubernetes</b>(Access Entry) · <b style='color:var(--navy)'>Kubernetes → IAM</b>(Pod Identity)")}{note("violet", "두 방향 모두 <b style='color:var(--navy)'>키 파일이 없다</b>")}</div>''', w=1750)

R("w5d4-path", f'''<div class="row" style="gap:6px;align-items:center">
{card("손님", "NLB DNS 주소", "slate", "Users")}{arrow(size=20)}
{card("NLB", "LBC가 만들었다<br>(EnvoyProxy의 주석)", "teal", "Split")}{arrow(size=20)}
{card("Envoy (Pod)", "4주차 Gateway<br>그대로", "teal", "DoorOpen")}{arrow(size=20)}
{card("HTTPRoute", "orders · catalog · web<br>배포 저장소 그대로", "violet", "Signpost")}{arrow(size=20)}
{card("catalog-api · order-api", "이미지 그대로 (GHCR)", "orange", "Boxes")}{arrow(size=20)}
{card("db Pod + PVC", "EBS gp3 볼륨<br>AZ 하나에 묶인다", "red", "HardDrive")}</div>
<div class="row" style="gap:14px">{note("violet", "바뀐 것: <b style='color:var(--navy)'>NodePort → NLB</b>, <b style='color:var(--navy)'>노드 디스크 → EBS</b> — 둘 다 '플랫폼'")}{note("orange", "그대로인 것: 이미지 · HTTPRoute · Deployment · Argo CD — '앱'")}</div>''', w=1800)
