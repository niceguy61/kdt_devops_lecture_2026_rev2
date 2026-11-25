"""5주차 3일차 다이어그램. 실행: python3 diagrams/w5d3.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week5" / "day3"
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


def chain(items, s=20):
    out = []
    for k, x in enumerate(items):
        out.append(x)
        if k < len(items) - 1:
            out.append(arrow(size=s))
    return f'<div class="row" style="gap:6px;align-items:center">{"".join(out)}</div>'


# 1. 작업 흐름
R("w5d3-workflow", f'''{chain([
  card("코드 (.tf)", "원하는 상태<br>resource · module", "violet", "FileCode", True),
  card("terraform init", "프로바이더 · 모듈 받기<br>backend 연결", "slate", "Download", True),
  card("terraform plan", "코드 ↔ state ↔ 실제<br>+ 만들 · ~ 바꿀 · - 지울", "orange", "GitCompare", True),
  card("terraform apply", "AWS API 호출<br>의존 순서대로", "teal", "Play", True),
  card("state", "내가 만든 것의 장부<br>ID · 속성", "red", "BookMarked", True)])}
<div class="row" style="gap:10px">{box("terraform destroy = 장부의 모든 것을 의존 역순으로 지운다 (2일차 7교시를 자동으로)", "teal", 16)}</div>
<div class="row" style="gap:14px">{note("orange", "plan은 <b style='color:var(--navy)'>아무것도 바꾸지 않는다</b> — 3일차 argocd app diff처럼 '무엇이 바뀔지'만")}{note("red", "state가 없으면 Terraform은 '내가 만든 것'을 모른다 — 4주차 추적 표시와 같은 역할")}</div>''', w=1750)

# 2. 원격 state와 잠금
R("w5d3-remote-state", f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="col" style="gap:8px;width:280px">{card("나", "terraform apply", "teal", "User")}{card("동료 · CI", "terraform plan", "orange", "Users")}</div>
<div class="col center" style="gap:4px">{arrow(size=26)}<span style="font-size:14px;color:var(--slate)">같은 장부</span></div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--red)"><div class="row c" style="gap:8px">{icon("Archive",24,"red",2)}<b style="font-size:20px;color:var(--navy);{MONO}">s3://devmart-tfstate-…</b><span style="font-size:15px;color:var(--slate)">버전 관리 · 암호화 · 퍼블릭 차단 · prevent_destroy</span></div>
{box("w5d3/vpc/terraform.tfstate          ← 장부", "red")}{box("w5d3/vpc/terraform.tfstate.tflock   ← 잠금: 누가 쓰는 중이면 있다 (use_lockfile)", "orange")}{box("w5d4/eks/terraform.tfstate          ← 내일", "red")}</div></div>
<div class="row" style="gap:14px">{note("red", "state에는 <b style='color:var(--navy)'>비밀 값</b>도 평문으로 들어갈 수 있다 — Git이 아니라 잠긴 버킷에")}{note("orange", "잠금이 없으면 두 사람의 apply가 장부를 <b style='color:var(--navy)'>덮어쓴다</b>")}</div>''', w=1700)

# 3. GitHub OIDC
R("w5d3-oidc", f'''{chain([
  card("PR 열기", "devmart-infra", "slate", "GitPullRequest"),
  card("GitHub Actions", "id-token: write<br>→ OIDC 토큰 (JWT)<br>sub: repo:…/devmart-infra:…", "violet", "Workflow"),
  card("AWS STS", "AssumeRoleWithWebIdentity<br>발급자 · aud · sub 확인", "orange", "BadgeCheck"),
  card("devmart-tf-plan 역할", "ReadOnly + state<br>1시간짜리 자격 증명", "teal", "IdCard"),
  card("terraform plan", "결과를 PR 요약에", "teal", "GitCompare")])}
<div class="row" style="gap:14px">{note("violet", "GitHub 시크릿에 <b style='color:var(--navy)'>AWS 키가 없다</b> — 4주차 3일차의 배포 토큰보다 한 걸음 더")}{note("orange", "신뢰 정책의 <b style='color:var(--navy)'>sub 조건</b>이 '어느 저장소의 워크플로만'을 정한다")}</div>''', w=1750)
