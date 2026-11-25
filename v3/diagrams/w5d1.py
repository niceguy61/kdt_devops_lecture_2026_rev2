"""5주차 1일차 다이어그램. 실행: python3 diagrams/w5d1.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week5" / "day1"
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


# 1. 계정 · 루트 · IAM 사용자 · 역할
R("w5d1-identities", f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--red)"><div class="row c" style="gap:8px">{ic("Crown","red",40)}<b style="font-size:21px;color:var(--navy)">루트 사용자</b></div>
<span style="font-size:16px;color:var(--navy)">계정을 만든 이메일 · <b>모든 것</b>을 할 수 있다 (막을 수 없다)</span>{box("MFA 걸고 · 금고에 넣고 · 평소엔 쓰지 않는다", "red")}</div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--teal)"><div class="row c" style="gap:8px">{ic("User","teal",40)}<b style="font-size:21px;color:var(--navy)">IAM 사용자 (사람)</b></div>
<span style="font-size:16px;color:var(--navy)">오늘 만드는 <span style="{MONO}">devops-admin</span> · 그룹 <span style="{MONO}">admins</span>로 권한</span>{box("콘솔 비밀번호 + MFA · CLI는 aws login (키를 만들지 않는다)", "teal")}</div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--violet)"><div class="row c" style="gap:8px">{ic("IdCard","violet",40)}<b style="font-size:21px;color:var(--navy)">IAM 역할 (빌려 쓰는 신원)</b></div>
<span style="font-size:16px;color:var(--navy)">EC2 · EKS Pod · GitHub Actions가 <b>잠깐</b> 맡는다</span>{box("비밀 키 없음 · 짧게 사는 자격 증명 (STS)", "violet")}</div></div>
<div class="row" style="gap:12px">{box("정책(JSON): Effect · Action · Resource · Condition — 기본은 거절, 명시적 Deny가 이긴다", "orange", 17)}</div>
<div class="row" style="gap:14px">{note("teal", "4주차 RBAC: User · Group · <b style='color:var(--navy)'>ServiceAccount</b> ↔ AWS: IAM 사용자 · 그룹 · <b style='color:var(--navy)'>역할</b>")}{note("violet", "사람은 <b style='color:var(--navy)'>사용자</b>로, 프로그램은 <b style='color:var(--navy)'>역할</b>로")}</div>''', w=1750)

# 2. VPC 그림
def subnet(name, cidr, c, inner):
    return f'<div class="card" style="flex:1;gap:6px;padding:10px;border-color:var(--{c});background:var(--{c}-l)"><b style="font-size:16px;color:var(--navy)">{name}</b><span style="font-size:14px;{MONO};color:var(--slate)">{cidr}</span>{inner}</div>'


def az(n, pub, priv):
    return f'''<div class="card" style="flex:1;gap:8px;padding:10px;border-style:dashed;border-color:var(--slate)"><b style="font-size:17px;color:var(--slate)">가용 영역 ap-northeast-2{n}</b>
{subnet("public", pub, "teal", '<span style="font-size:14px;color:var(--navy)">ALB · NAT · 공개 EC2</span>')}
{subnet("private", priv, "violet", '<span style="font-size:14px;color:var(--navy)">EKS 노드 · DB — 밖에서 못 들어온다</span>')}</div>'''


R("w5d1-vpc", f'''<div class="row" style="gap:10px;align-items:stretch">
<div class="col center" style="gap:8px;width:200px">{card("인터넷", "", "slate", "Globe")}{arrow(size=22)}{card("IGW", "인터넷 게이트웨이<br>(VPC의 문)", "teal", "DoorOpen")}</div>
<div class="card" style="flex:1;gap:10px;padding:12px;border-color:var(--navy)"><div class="row c" style="gap:8px">{icon("Network",24,"navy",2)}<b style="font-size:20px;color:var(--navy)">VPC devmart-vpc</b><span style="font-size:16px;{MONO};color:var(--slate)">10.0.0.0/16 · 리전 ap-northeast-2 (서울)</span></div>
<div class="row" style="gap:10px">{az("a", "10.0.0.0/20", "10.0.128.0/20")}{az("c", "10.0.16.0/20", "10.0.144.0/20")}</div>
<div class="row" style="gap:10px">{box("public 라우팅 테이블: 0.0.0.0/0 → IGW", "teal")}{box("private 라우팅 테이블: 0.0.0.0/0 → NAT (오늘은 없음 = 밖으로 못 나감)", "violet")}</div></div></div>
<div class="row" style="gap:14px">{note("teal", "서브넷이 public인지는 <b style='color:var(--navy)'>라우팅 테이블</b>이 정한다 — 이름이 아니다")}{note("orange", "NAT 게이트웨이는 <b style='color:var(--navy)'>켜 두기만 해도</b> 시간당 요금 — 오늘은 만들지 않는다")}</div>''', w=1750)

# 3. 보안 그룹 vs NACL
R("w5d1-sg-nacl", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--teal)"><div class="row c" style="gap:8px">{ic("Shield","teal",40)}<b style="font-size:21px;color:var(--navy)">보안 그룹 (Security Group)</b></div>
{box("붙는 곳: 인스턴스 · ENI (ALB · EKS 노드 · RDS)", "teal")}{box("허가 규칙만 — 적지 않은 것은 거절", "teal")}{box("상태 저장 — 나간 요청의 응답은 자동 허가", "teal")}{box("출발지로 다른 보안 그룹을 지목할 수 있다", "teal")}</div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--orange)"><div class="row c" style="gap:8px">{ic("Fence","orange",40)}<b style="font-size:21px;color:var(--navy)">네트워크 ACL</b></div>
{box("붙는 곳: 서브넷", "orange")}{box("허가 + 거절 규칙, 번호 순서대로", "orange")}{box("상태 없음 — 응답 포트(1024-65535)도 따로 열어야", "orange")}{box("기본 NACL은 모두 허가 — 대개 그대로 둔다", "orange")}</div></div>
<div class="row" style="gap:14px">{note("teal", "보안 그룹 = 4주차 <b style='color:var(--navy)'>AuthorizationPolicy</b>처럼 '누가 이 문으로 올 수 있나'")}{note("orange", "1주차 3일차의 방화벽 · 상태 저장(stateful)이 여기서 실물이 된다")}</div>''', w=1700)
