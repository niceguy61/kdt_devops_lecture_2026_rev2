"""4주차 3일차 다이어그램. 실행: python3 diagrams/w4d3.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week4" / "day3"
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
    return f'<div class="card center grow" style="gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,46)}<b style="font-size:18px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


def lane(title, c, cells):
    out = []
    for k, x in enumerate(cells):
        out.append(x)
        if k < len(cells) - 1:
            out.append(arrow(size=20))
    return f'''<div class="card" style="gap:8px;padding:12px;border-color:var(--{c})"><b style="font-size:20px;color:var(--navy)">{title}</b>
<div class="row" style="gap:6px;align-items:center">{"".join(out)}</div></div>'''


# 1. push vs pull
R("w4d3-push-pull", f'''<div class="col" style="gap:12px">
{lane("push — CI가 클러스터에 밀어 넣는다 (3주차까지 우리가 한 방식)", "orange", [
    card("git push", "개발자", "slate", "GitBranch"), card("CI", "빌드 · 테스트<br>+ kubectl apply", "orange", "Workflow"),
    card("클러스터", "CI가 관리자 열쇠를<br>들고 들어온다", "red", "KeyRound")])}
{lane("pull — 클러스터 안의 에이전트가 Git을 보고 맞춘다 (GitOps)", "teal", [
    card("git push", "개발자 · CI 봇", "slate", "GitBranch"), card("Git 저장소", "원하는 상태<br>(선언 · 버전 · 불변)", "violet", "FolderGit2"),
    card("Argo CD", "클러스터 안에서<br>당겨 와 비교 · 적용", "teal", "RefreshCw"), card("클러스터", "열쇠는 밖으로<br>나가지 않는다", "teal", "ShieldCheck")])}</div>
<div class="row" style="gap:14px">{note("orange", "push는 <b style='color:var(--navy)'>한 번 밀고 끝</b> — 누가 손으로 바꿔도 아무도 모른다")}{note("teal", "pull은 <b style='color:var(--navy)'>계속 비교한다</b> — 어긋남(drift)을 보고, 원하면 되돌린다")}</div>''', w=1650)

# 2. GitOps 루프와 두 저장소
R("w4d3-loop", f'''<div class="row" style="gap:10px;align-items:stretch">
<div class="col" style="gap:8px;width:300px"><div class="row c" style="gap:6px">{icon("Code",22,"slate",2)}<b style="font-size:18px;color:var(--navy)">devops-lab (코드)</b></div>
{box("devmart-msa/catalog-api/Dockerfile", "slate")}{box(".github/workflows/devmart-ci.yml", "slate")}
<span style="font-size:15px;color:var(--slate)">개발자가 PR → 리뷰 → main</span></div>
<div class="col center" style="gap:4px">{arrow(size=24)}<span style="font-size:13px;color:var(--slate)">CI<br>빌드 · push</span></div>
<div class="col" style="gap:8px;width:250px">{card("GHCR", "devmart-catalog-api<br>:sha-1a2b3c4", "orange", "Package", True)}</div>
<div class="col center" style="gap:4px">{arrow(size=24)}<span style="font-size:13px;color:var(--slate)">CI 봇<br>태그 커밋</span></div>
<div class="col" style="gap:8px;width:320px"><div class="row c" style="gap:6px">{icon("FolderGit2",22,"violet",2)}<b style="font-size:18px;color:var(--navy)">devmart-deploy (배포)</b></div>
{box("devmart/kustomization.yaml<br>images: newTag: sha-1a2b3c4", "violet")}{box("devmart/*.yaml · routes · rules", "violet")}
<span style="font-size:15px;color:var(--slate)">원하는 상태의 유일한 출처</span></div>
<div class="col center" style="gap:4px">{arrow(size=24)}<span style="font-size:13px;color:var(--slate)">60초마다<br>pull</span></div>
<div class="col" style="gap:8px;flex:1">{card("Argo CD", "Git ↔ 클러스터 비교<br>다르면 Sync", "teal", "RefreshCw")}{card("devmart 네임스페이스", "실제 상태", "teal", "Boxes")}</div></div>
<div class="row" style="gap:14px">{note("violet", "배포 = <b style='color:var(--navy)'>배포 저장소의 커밋</b> · 되돌리기 = <b style='color:var(--navy)'>git revert</b>")}{note("teal", "CI는 클러스터 열쇠가 없다 — 배포 저장소 <b style='color:var(--navy)'>하나만 쓸 수 있는 토큰</b>만 가진다")}</div>''', w=1750)

# 3. Argo CD 구조
R("w4d3-argocd", f'''<div class="row" style="gap:14px;align-items:stretch">
<div class="col" style="gap:8px;width:260px">{card("Git", "devmart-deploy", "violet", "FolderGit2")}{card("나", "웹 UI · argocd CLI<br>port-forward 8080", "slate", "User")}</div>
<div class="card" style="flex:1;gap:10px;padding:14px;border-color:var(--teal);background:#F7FDFC"><div class="row c" style="gap:8px">{icon("Ship",24,"teal",2)}<b style="font-size:20px;color:var(--navy);{MONO}">namespace: argocd</b></div>
<div class="row" style="gap:10px">{card("argocd-repo-server", "Git을 받아<br>kustomize build → YAML", "violet", "FileCode", True)}{card("argocd-application-controller", "원하는 상태 ↔ 실제 상태<br>비교 · Sync (reconcile)", "teal", "RefreshCw", True)}</div>
<div class="row" style="gap:10px">{card("argocd-server", "API · 웹 UI<br>로그인 · 권한", "orange", "Globe", True)}{card("argocd-redis", "계산 결과<br>캐시", "red", "Database", True)}{card("Application (CRD)", "어디서(source) →<br>어디로(destination)", "violet", "FileText", True)}</div></div>
<div class="col" style="gap:8px;width:240px">{card("Kubernetes API", "kubectl apply와<br>같은 길", "teal", "Server")}</div></div>
<div class="row" style="gap:14px">{note("teal", "application-controller는 3주차의 <b style='color:var(--navy)'>Deployment 컨트롤러와 같은 일</b>을 Git 단위로 한다")}{note("violet", "Application도 YAML — <b style='color:var(--navy)'>Argo CD 설정조차 Git에</b> 둘 수 있다 (app of apps)")}</div>''', w=1700)

# 4. Sync · Health 상태
def st(t, d, c, i):
    return f'<div class="card center grow" style="gap:6px;padding:10px 6px;border-color:var(--{c})">{ic(i,c,40)}<b style="font-size:18px;color:var(--navy);{MONO}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{d}</span></div>'


R("w4d3-status", f'''<div class="row" style="gap:16px;align-items:stretch">
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--violet)"><b style="font-size:21px;color:var(--navy)">Sync — Git과 같은가?</b>
<div class="row" style="gap:8px">{st("Synced", "Git = 클러스터", "teal", "CircleCheck")}{st("OutOfSync", "어긋났다<br>(새 커밋 · 손 수정)", "orange", "CircleAlert")}{st("Unknown", "비교 실패<br>(저장소 · 문법)", "slate", "CircleHelp")}</div></div>
<div class="card" style="flex:1;gap:8px;padding:14px;border-color:var(--teal)"><b style="font-size:21px;color:var(--navy)">Health — 잘 돌고 있나?</b>
<div class="row" style="gap:8px">{st("Healthy", "준비 끝<br>(readiness 통과)", "teal", "HeartPulse")}{st("Progressing", "롤아웃 중", "orange", "Loader")}{st("Degraded", "실패<br>(CrashLoop · 타임아웃)", "red", "HeartCrack")}{st("Missing", "Git엔 있고<br>클러스터엔 없다", "slate", "CircleDashed")}</div></div></div>
<div class="row" style="gap:14px">{note("violet", "<b style='color:var(--navy)'>Synced + Degraded</b> = Git대로 잘 배포했지만 <b style='color:var(--navy)'>Git이 틀렸다</b>")}{note("orange", "<b style='color:var(--navy)'>OutOfSync + Healthy</b> = 잘 돌지만 <b style='color:var(--navy)'>Git과 다르다</b> — 누가 손댔나?")}</div>''', w=1700)
