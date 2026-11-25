"""4주차 5일차 다이어그램. 실행: python3 diagrams/w4d5.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week4" / "day5"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def note(c, html):
    return f'<div class="card fill-{c} grow" style="padding:12px 18px"><p style="font-size:19px">{html}</p></div>'


def card(t, sub, c, i, mono=False):
    f = MONO if mono else ""
    return f'<div class="card center grow" style="gap:6px;padding:12px 8px;border-color:var(--{c})">{ic(i,c,44)}<b style="font-size:18px;color:var(--navy);{f}">{t}</b><span style="font-size:14px;color:var(--slate);text-align:center">{sub}</span></div>'


def box(t, c, size=15):
    return f'<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:{size}px;{MONO};border:1.5px solid var(--{c});text-align:left">{t}</div>'


def chain(items):
    out = []
    for k, x in enumerate(items):
        out.append(x)
        if k < len(items) - 1:
            out.append(arrow(size=20))
    return f'<div class="row" style="gap:6px;align-items:center">{"".join(out)}</div>'


# 1. apiserver 요청이 지나는 세 관문
R("w4d5-api-gates", f'''{chain([
  card("요청", "kubectl · Argo CD<br>· CI · Pod", "slate", "Send"),
  card("① 인증", "누구인가?<br>인증서 · 토큰 · OIDC", "teal", "IdCard"),
  card("② 인가 (RBAC)", "할 수 있나?<br>Role · RoleBinding", "orange", "KeyRound"),
  card("③ 입장 제어", "규칙에 맞나?<br>Kyverno · VAP", "violet", "ShieldCheck"),
  card("etcd에 저장", "→ 컨트롤러가<br>실제로 만든다", "navy", "Database")])}
<div class="row" style="gap:10px">{box("401 Unauthorized", "teal")}{box("403 Forbidden: User &quot;jane&quot; cannot list secrets", "orange")}{box("admission webhook … denied the request", "violet")}</div>
<div class="row" style="gap:14px">{note("orange", "RBAC는 <b style='color:var(--navy)'>누가 · 무엇에 · 어떤 동사</b>를 — 내용은 보지 않는다")}{note("violet", "입장 제어는 <b style='color:var(--navy)'>내용</b>을 본다 — 'latest 태그', 'limits 없음'")}</div>''', w=1750)

# 2. RBAC 모델
R("w4d5-rbac", f'''<div class="row" style="gap:12px;align-items:stretch">
<div class="col" style="gap:8px;width:330px"><b style="font-size:19px;color:var(--navy)">누가 (subjects)</b>
{box("User: minsu  (사람 · 인증서/OIDC)", "teal")}{box("Group: devmart-devs", "teal")}{box("ServiceAccount: devmart/pod-reader<br>(Pod 안의 프로그램)", "violet")}</div>
<div class="col center" style="gap:4px">{arrow(size=26)}<span style="font-size:14px;color:var(--slate)">이어 준다</span></div>
<div class="col" style="gap:8px;width:300px"><b style="font-size:19px;color:var(--navy)">RoleBinding</b>{box("devmart-developer<br>namespace: devmart", "orange")}
<span style="font-size:15px;color:var(--slate)">ClusterRoleBinding = 클러스터 전체</span></div>
<div class="col center" style="gap:4px">{arrow(size=26)}</div>
<div class="col" style="gap:8px;flex:1"><b style="font-size:19px;color:var(--navy)">Role — 무엇을 어떻게 (rules)</b>
{box("pods · pods/log · services · events → get · list · watch", "orange")}{box("deployments → get · list · watch", "orange")}{box("secrets · pods/exec · create · delete → 없음 (기본은 거절)", "red")}</div></div>
<div class="row" style="gap:14px">{note("teal", "RBAC에는 <b style='color:var(--navy)'>허가만</b> 있다 — 적지 않은 것은 모두 거절")}{note("orange", "GitOps에서 사람은 <b style='color:var(--navy)'>읽기만</b> — 쓰기는 Git → Argo CD의 몫")}</div>''', w=1750)

# 3. 거절의 지도
def who(t, msg, c, i):
    return f'<div class="card" style="gap:6px;padding:12px;border-color:var(--{c})"><div class="row c" style="gap:8px">{ic(i,c,38)}<b style="font-size:18px;color:var(--navy)">{t}</b></div>{box(msg, c, 14)}</div>'


R("w4d5-who-refused", f'''<div class="row" style="gap:10px;align-items:stretch">
<div class="col" style="gap:10px;flex:1"><b style="font-size:20px;color:var(--navy)">클러스터를 바꾸려 할 때 (kubectl · Argo CD)</b>
{who("apiserver RBAC", "Error from server (Forbidden): … cannot list resource &quot;secrets&quot;", "orange", "KeyRound")}
{who("Kyverno 입장 제어", "admission webhook &quot;…kyverno…&quot; denied the request", "violet", "ShieldCheck")}
{who("kubelet", "ImagePullBackOff · CreateContainerConfigError", "slate", "Server")}</div>
<div class="col" style="gap:10px;flex:1"><b style="font-size:20px;color:var(--navy)">요청이 오갈 때 (손님 · 서비스)</b>
{who("Envoy Gateway (입구)", "500 no healthy upstream · 404", "teal", "DoorOpen")}
{who("waypoint (L7)", "403 RBAC: access denied · 504 (UT)", "red", "Signpost")}
{who("ztunnel (L4)", "000 Connection reset by peer", "violet", "Lock")}</div></div>
<div class="row" style="gap:14px">{note("red", "메시지의 <b style='color:var(--navy)'>모양</b>이 거절한 주체를 알려 준다 — 그 주체의 설정을 본다")}{note("teal", "4주차에 층이 늘었다 = 거절할 수 있는 곳이 늘었다")}</div>''', w=1750)
