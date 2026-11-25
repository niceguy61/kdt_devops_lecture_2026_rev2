"""2주차 1일차 다이어그램. 실행: python3 diagrams/w2d1.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, arrow  # noqa: E402

OUT = ROOT / "assets" / "week2" / "day1"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


# 1. 2주차 흐름
days = [("Wrench", "slate", "1일차", "개발 환경 + Git", "작업대 만들기"),
        ("Box", "teal", "2일차", "Docker 기본", "nginx로 연습"),
        ("FileCode", "orange", "3일차", "Dockerfile", "상품 API 포장"),
        ("Database", "violet", "4일차", "볼륨·네트워크·환경 변수", "API ↔ PostgreSQL"),
        ("Layers", "green", "5일차", "Compose + 협업", "웹+API+DB 한 번에")]
dc = []
for k, (i, c, d, t, n) in enumerate(days):
    dc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:18px 10px"><span class="chip" style="background:var(--{c});color:#fff;font-size:18px">{d}</span>{ic(i,c,72)}<h3 style="font-size:22px">{t}</h3><div class="box" style="background:var(--slate-l);color:var(--slate);font-size:17px;width:100%">{n}</div></div>')
    if k < 4:
        dc.append(arrow(size=28))
R("w2d1-week-flow", f'''<div class="row flow" style="gap:6px">{"".join(dc)}</div>
<div class="row c" style="gap:14px;justify-content:center"><div class="box" style="background:var(--navy);color:#fff;font-size:22px;padding:14px 26px;display:flex;align-items:center;gap:12px">{icon("ShoppingBag",32,"#7FD3E0",2)} 주인공: 쇼핑몰 DevMart — 3주차 MSA → 4주차 K8s → 5주차 AWS로 여행</div></div>''')

# 2. 작업 환경 지도
def env(title, ic_, col, shell, home, docker):
    return f'''<div class="card grow" style="gap:12px;border-color:var(--{col})"><div class="row c" style="gap:12px">{ic(ic_,col,62)}<h3 style="font-size:26px">{title}</h3></div>
<div class="box" style="background:var(--{col}-l);color:var(--navy);font-size:19px;text-align:left">명령: {shell}</div>
<div class="box" style="background:var(--slate-l);color:var(--navy);font-size:18px;text-align:left;{MONO}">{home}</div>
<div class="row c" style="gap:8px">{icon("Container",30,col,2)}<span style="font-size:19px;font-weight:700;color:var(--navy)">{docker}</span></div></div>'''


R("w2d1-workbench", f'''<div class="row" style="gap:18px">
{env("Windows 10/11","Monitor","teal","WSL2 안의 Ubuntu 24.04","~ = /home/내이름","Docker Desktop (WSL 연동)")}
{env("Mac","Laptop","violet","터미널 (zsh)","~ = /Users/내이름","Docker Desktop")}
{env("Linux","Terminal","orange","터미널 (bash)","~ = /home/내이름","Docker Engine")}</div>
<div class="row c" style="gap:12px;justify-content:center">{icon("ArrowDown",30,"slate",2.5)}</div>
<div class="row" style="gap:14px">
<div class="card fill-teal grow" style="padding:14px 20px;flex-direction:row;align-items:center;gap:12px">{icon("Code",34,"teal",2)}<p style="font-size:20px"><b style="color:var(--navy)">VS Code</b> — 위에서 편집, 아래 터미널에서 명령</p></div>
<div class="card fill-orange grow" style="padding:14px 20px;flex-direction:row;align-items:center;gap:12px">{icon("FolderGit2",34,"orange",2)}<p style="font-size:20px"><b style="color:var(--navy)">~/devops-lab</b> — 모든 실습을 담는 저장소</p></div>
<div class="card fill-violet grow" style="padding:14px 20px;flex-direction:row;align-items:center;gap:12px">{icon("CloudUpload",34,"violet",2)}<p style="font-size:20px"><b style="color:var(--navy)">GitHub</b> — gh로 로그인, push</p></div></div>''')

# 3. Git 한 바퀴
st = [("FilePen", "slate", "① 고친다", "VS Code에서 저장"), ("Search", "teal", "② 확인한다", "git status · git diff"),
      ("PackagePlus", "teal", "③ 담는다", "git add"), ("Stamp", "violet", "④ 기록한다", 'git commit -m "왜"'), ("CloudUpload", "orange", "⑤ 올린다", "git push")]
sc = []
for k, (i, c, t, d) in enumerate(st):
    sc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:20px 10px">{ic(i,c,74)}<h3 style="font-size:23px">{t}</h3><div style="font-size:18px;{MONO};color:var(--{c})">{d}</div></div>')
    if k < 4:
        sc.append(arrow(size=28))
R("w2d1-git-loop", f'''<div class="row flow" style="gap:6px">{"".join(sc)}</div>
<div class="row c" style="gap:12px;justify-content:center">{icon("RefreshCw",32,"teal",2.2)}<div class="box" style="background:var(--teal-l);color:var(--teal-d);font-size:21px">다시 ①로 — 5주 동안 수백 번 도는 바퀴 · 막히면 언제나 git status부터</div></div>''')

# 4. Docker 구조
R("w2d1-docker-arch", f'''<div class="row" style="gap:16px;align-items:center">
<div class="col center" style="width:220px;gap:10px">{ic("SquareTerminal","navy",96)}<h3 style="font-size:24px;color:var(--navy)">Docker CLI</h3><div class="box" style="background:var(--slate-l);color:var(--navy);font-size:18px;{MONO}">docker run …</div><div class="note" style="font-size:17px">주문서</div></div>
{arrow(size=40)}
<div class="grow" style="border:3px dashed var(--teal);border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:12px">
 <div class="tag" style="color:var(--teal-d)">DOCKER DESKTOP 안의 숨은 LINUX VM (Linux는 VM 없이 바로)</div>
 <div class="card fill-teal" style="gap:8px;padding:16px"><div class="row c" style="gap:10px">{icon("ChefHat",36,"teal",2)}<h3 style="font-size:23px">Docker Engine (dockerd)</h3><span class="note" style="font-size:17px">주방</span></div>
  <div class="row" style="gap:10px"><div class="box grow" style="background:#fff;color:var(--navy);font-size:18px">containerd</div><div class="box grow" style="background:#fff;color:var(--navy);font-size:18px">runc — 네임스페이스 · cgroups</div></div></div>
 <div class="row" style="gap:10px">{"".join(f'<div class="card center grow" style="padding:10px;gap:4px;border-color:var(--orange)">{icon("Box",34,"orange",2)}<div style="font-size:17px;font-weight:700">컨테이너 {n}</div></div>' for n in "ABC")}</div></div>
{arrow("both",40)}
<div class="col center" style="width:220px;gap:10px">{ic("Warehouse","violet",96)}<h3 style="font-size:24px;color:var(--navy)">레지스트리</h3><div class="box" style="background:var(--violet-l);color:var(--navy);font-size:18px">Docker Hub</div><div class="note" style="font-size:17px">이미지 창고</div></div></div>''')

# 5. hello-world 흐름
hs = [("SquareTerminal", "navy", "① CLI → 엔진", "docker run hello-world"), ("Download", "violet", "② 엔진 → 레지스트리", "이미지가 없으면 pull"),
      ("Box", "orange", "③ 컨테이너 생성 · 실행", "프로그램이 메시지 출력"), ("MonitorCheck", "green", "④ 출력 → 터미널", "Hello from Docker!")]
sc = []
for k, (i, c, t, d) in enumerate(hs):
    sc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:20px 10px">{ic(i,c,78)}<h3 style="font-size:22px">{t}</h3><p style="font-size:18px">{d}</p></div>')
    if k < 3:
        sc.append(arrow(size=30))
R("w2d1-hello-flow", f'''<div class="row flow" style="gap:8px">{"".join(sc)}</div>
<div class="row" style="gap:14px"><div class="card fill-violet grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">처음 실행</b> — Unable to find image locally → Pulling (에러 아님)</p></div>
<div class="card fill-green grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">두 번째 실행</b> — 이미 받은 이미지를 재사용, 바로 실행</p></div></div>''')
