"""1주차 5일차 다이어그램. 실행: python3 diagrams/w1d5.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, aws, arrow  # noqa: E402

OUT = ROOT / "assets" / "week1" / "day5"
only = set(sys.argv[1:])
MONO = "font-family:'D2Coding','Consolas',monospace"


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def flowcards(items, isize=78, h3=23, p=18):
    out = []
    for k, (i, c, t, d) in enumerate(items):
        out.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:20px 12px">{ic(i,c,isize)}<h3 style="font-size:{h3}px">{t}</h3><p style="font-size:{p}px">{d}</p></div>')
        if k < len(items) - 1:
            out.append(arrow(size=30))
    return f'<div class="row flow" style="gap:8px">{"".join(out)}</div>'


# 1. 혼란의 벽
R("w1d5-wall", f'''<div class="row" style="gap:0;align-items:stretch">
<div class="card fill-teal grow center" style="gap:12px;border-radius:20px 0 0 20px">{ic("Code","teal",100)}<h3 style="font-size:30px">개발팀 (Dev)</h3>
 <div class="box" style="background:#fff;color:var(--teal-d);font-size:24px">원하는 것: 변화</div><p style="font-size:20px">평가: 새 기능을 얼마나 빨리</p>
 <div class="box" style="background:var(--slate-l);color:var(--slate);font-size:19px;font-style:italic">"운영팀은 맨날 안 된다고만 해요"</div></div>
<div class="col center" style="width:170px;background:repeating-linear-gradient(0deg,#B83227 0 26px,#9e2a21 26px 30px);justify-content:center;gap:10px;padding:16px">
 <div style="font-size:24px;font-weight:900;color:#fff;text-align:center;line-height:1.3">혼란의<br>벽</div>{icon("ArrowRight",44,"#ffffff",2.5)}<div style="font-size:17px;color:#fde2df;text-align:center">코드를<br>벽 너머로<br>던진다</div></div>
<div class="card fill-orange grow center" style="gap:12px;border-radius:0 20px 20px 0">{ic("Server","orange",100)}<h3 style="font-size:30px">운영팀 (Ops)</h3>
 <div class="box" style="background:#fff;color:var(--orange);font-size:24px">원하는 것: 안정</div><p style="font-size:20px">평가: 서비스가 얼마나 안정적</p>
 <div class="box" style="background:var(--slate-l);color:var(--slate);font-size:19px;font-style:italic">"개발팀은 던져 놓고 가 버려요"</div></div></div>
<div class="row c" style="gap:14px;justify-content:center">{icon("ArrowDown",34,"green",2.5)}<div class="box" style="background:var(--green);color:#fff;font-size:23px;padding:14px 30px">DevOps — 벽을 허물고 같은 목표(사용자가 만족하는 서비스)를 본다</div></div>''')

# 2. CALMS
cl = [("C", "Culture", "문화", "같은 목표를 공유", "HeartHandshake", "teal"), ("A", "Automation", "자동화", "반복은 기계에게", "Bot", "orange"),
      ("L", "Lean", "린", "작게, 자주, 낭비 없이", "Feather", "green"), ("M", "Measurement", "측정", "감이 아니라 숫자로", "ChartColumn", "violet"),
      ("S", "Sharing", "공유", "지식과 실패를 나눈다", "Share2", "teal")]
cc = "".join(f'''<div class="card center grow" style="gap:10px;border-color:var(--{c});padding:22px 10px">
<div style="font-size:76px;font-weight:900;color:var(--{c});line-height:1">{L}</div><div class="tag">{e.upper()}</div>{icon(i,46,c,2)}
<h3 style="font-size:27px">{k}</h3><p style="font-size:19px">{d}</p></div>''' for L, e, k, d, i, c in cl)
R("w1d5-calms", f'''<div class="row" style="gap:14px">{cc}</div>
<div class="card fill-slate" style="padding:16px 24px"><p style="font-size:21px">도구(Automation)는 다섯 중 <b style="color:var(--navy)">하나</b>일 뿐 — Docker · K8s · Argo CD는 이 문화를 실천하기 위한 도구</p></div>''')

# 3. 폭포수 vs 애자일
wf = ["계획", "설계", "개발", "테스트", "배포"]
wsteps = "".join(f'<div class="box" style="background:var(--slate-l);color:var(--navy);font-size:21px;margin-left:{k*52}px;width:190px">{s}</div>' for k, s in enumerate(wf))
loop = "".join(f'<div class="col center" style="gap:4px"><div style="width:120px;height:120px;border-radius:50%;border:6px solid var(--teal);display:flex;align-items:center;justify-content:center;flex-direction:column">{icon("RefreshCw",36,"teal",2.2)}<div style="font-size:18px;font-weight:800;color:var(--teal-d)">{k}주기</div></div><div style="font-size:16px;color:var(--slate)">계획→개발→배포</div></div>' for k in range(1, 5))
R("w1d5-waterfall-agile", f'''<div class="row" style="gap:24px;align-items:stretch">
<div class="card grow" style="gap:12px"><div class="row c" style="gap:10px"><div class="tag">WATERFALL</div><h3 style="font-size:27px">폭포수 — 한 번에 크게</h3></div>
 <div class="col" style="gap:8px">{wsteps}</div>
 <div class="row c" style="gap:10px">{icon("PackageOpen",40,"orange",2)}<p style="font-size:19px">몇 달 뒤 마지막에 <b style="color:var(--orange)">한 번에 배포</b> — 문제도 마지막에 발견</p></div></div>
<div class="card grow" style="gap:12px"><div class="row c" style="gap:10px"><div class="tag">AGILE</div><h3 style="font-size:27px">애자일 — 작게 자주</h3></div>
 <div class="row c" style="gap:10px;justify-content:center;flex:1">{loop}</div>
 <div class="row c" style="gap:10px">{icon("Rocket",40,"teal",2)}<p style="font-size:19px">1~4주마다 <b style="color:var(--teal-d)">작게 배포</b>하고 피드백 — 변경을 환영</p></div></div></div>''')

# 4. CI/CD 파이프라인
st = [("GitCommitHorizontal", "slate", "① 커밋 · 푸시", "3교시 Git"), ("Hammer", "teal", "② 빌드", "docker build"),
      ("FlaskConical", "teal", "③ 테스트", "자동 테스트"), ("ShieldCheck", "red", "④ 보안 검사", "취약점 · 비밀값"),
      ("Archive", "violet", "⑤ 이미지 저장", "레지스트리"), ("Rocket", "orange", "⑥ 배포", "스테이징 → 운영")]
R("w1d5-cicd", f'''<div class="row" style="gap:10px"><div class="box grow" style="background:var(--teal-l);color:var(--teal-d);font-size:21px;flex:4">CI — 지속적 통합 (자주 합치고 매번 자동 검사)</div>
<div class="box grow" style="background:var(--orange-l);color:var(--orange);font-size:21px;flex:2">CD — 지속적 전달 · 배포</div></div>
{flowcards(st, 72, 21, 17)}
<div class="row c" style="gap:14px;justify-content:center"><div class="box" style="background:var(--navy);color:#fff;font-size:21px">각 단계 = 품질 관문 · 종료 코드 0이면 다음으로, 아니면 멈춤</div>
<div class="box" style="background:var(--red-l);color:var(--red);font-size:20px">문제가 생기면 → 되돌리기</div></div>''')

# 5. Git 세 영역
areas = [("FolderOpen", "slate", "작업 폴더", "지금 고치는 곳", "책상 위 물건"), ("PackagePlus", "teal", "스테이징 영역", "기록할 변경 고르기", "상자에 담기"),
         ("Database", "violet", "로컬 저장소", "이력이 기록된 곳", "송장 붙여 봉하기"), ("CloudUpload", "navy", "원격 저장소", "팀이 함께 (GitHub)", "택배 발송")]
cmds = ["git add", "git commit", "git push"]
out = []
for k, (i, c, t, d, a) in enumerate(areas):
    out.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c})">{ic(i,c,84)}<h3 style="font-size:24px">{t}</h3><p style="font-size:18px">{d}</p><div class="box" style="background:var(--slate-l);color:var(--slate);font-size:17px;width:100%">비유: {a}</div></div>')
    if k < 3:
        out.append(f'<div class="col center" style="gap:4px;align-self:center">{icon("ArrowRight",36,"orange",2.5)}<div style="font-size:18px;{MONO};font-weight:700;color:var(--orange);white-space:nowrap">{cmds[k]}</div></div>')
R("w1d5-git-areas", f'''<div class="row flow" style="gap:8px">{"".join(out)}</div>
<div class="row" style="gap:14px"><div class="card fill-teal grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">git status</b> — 지금 무엇이 바뀌었는지 (가장 자주 쓰는 명령)</p></div>
<div class="card fill-red grow" style="padding:14px 20px"><p style="font-size:20px"><b style="color:var(--navy)">비밀값은 절대 커밋 금지</b> — .env는 .gitignore에</p></div></div>''')

# 6. 브랜치와 PR (SVG 라인)
R("w1d5-branch-pr", f'''<div style="position:relative;height:330px">
<svg width="1240" height="330" style="position:absolute;left:0;top:0">
 <line x1="40" y1="250" x2="1200" y2="250" stroke="#0F2A44" stroke-width="8" stroke-linecap="round"/>
 <path d="M 220 250 C 300 250, 300 110, 380 110 L 860 110 C 940 110, 940 250, 1020 250" fill="none" stroke="#0089A0" stroke-width="8" stroke-linecap="round"/>
 {"".join(f'<circle cx="{x}" cy="250" r="16" fill="#0F2A44"/>' for x in (100, 220, 1020, 1140))}
 {"".join(f'<circle cx="{x}" cy="110" r="16" fill="#0089A0"/>' for x in (460, 560, 660))}
</svg>
<div style="position:absolute;left:20px;top:276px;font-size:22px;font-weight:900;color:var(--navy);{MONO}">main</div>
<div style="position:absolute;left:380px;top:50px;font-size:22px;font-weight:900;color:var(--teal-d);{MONO}">feature/login</div>
<div style="position:absolute;left:420px;top:140px;font-size:18px;color:var(--slate)">② 작은 커밋 여러 번</div>
<div style="position:absolute;left:150px;top:276px;font-size:18px;color:var(--slate)">① 브랜치 만들기</div>
<div style="position:absolute;left:720px;top:150px;display:flex;gap:10px;align-items:center"><span class="chip orange" style="font-size:19px">③ Pull Request</span></div>
<div style="position:absolute;left:960px;top:276px;font-size:18px;color:var(--green);font-weight:800">⑥ 병합 (merge)</div>
</div>
<div class="row" style="gap:14px">
<div class="card fill-orange grow" style="padding:14px 18px;flex-direction:row;align-items:center;gap:10px">{icon("GitPullRequest",38,"orange",2)}<p style="font-size:19px"><b style="color:var(--navy)">③ PR</b> "합쳐 주세요" + 무엇을 왜</p></div>
<div class="card fill-teal grow" style="padding:14px 18px;flex-direction:row;align-items:center;gap:10px">{icon("FlaskConical",38,"teal",2)}<p style="font-size:19px"><b style="color:var(--navy)">④ 자동 검사</b> CI 빌드 · 테스트</p></div>
<div class="card fill-violet grow" style="padding:14px 18px;flex-direction:row;align-items:center;gap:10px">{icon("MessageSquare",38,"violet",2)}<p style="font-size:19px"><b style="color:var(--navy)">⑤ 코드 리뷰</b> 감시가 아니라 학습</p></div></div>''')

# 7. 이해관계자 지도
peo = [("Code", "teal", "개발자", "빠르고 쉬운 배포"), ("CalendarCheck", "orange", "기획 · PM", "일정대로 출시"), ("FlaskConical", "violet", "QA", "운영과 같은 테스트 환경"),
       ("ShieldCheck", "red", "보안", "위험 최소화"), ("ChartColumn", "green", "데이터 팀", "데이터 접근"), ("Wallet", "orange", "재무 · 경영", "비용 통제"),
       ("Headset", "violet", "고객 지원", "장애 상황 파악")]
import math
cx, cy, rr = 640, 380, 300
nodes = []
for k, (i, c, t, d) in enumerate(peo):
    a = -math.pi / 2 + k * 2 * math.pi / len(peo)
    x, y = cx + rr * 1.45 * math.cos(a), cy + rr * math.sin(a)
    nodes.append(f'<div class="card center" style="position:absolute;left:{x-125:.0f}px;top:{y-72:.0f}px;width:250px;gap:4px;padding:12px;border-color:var(--{c})"><div class="row c" style="gap:8px;justify-content:center">{icon(i,32,c,2)}<h3 style="font-size:21px">{t}</h3></div><p style="font-size:17px">{d}</p></div>')
lines = "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + rr*1.45*math.cos(-math.pi/2 + k*2*math.pi/len(peo)):.0f}" y2="{cy + rr*math.sin(-math.pi/2 + k*2*math.pi/len(peo)):.0f}" stroke="#D5DEE6" stroke-width="3" stroke-dasharray="8 6"/>' for k in range(len(peo)))
R("w1d5-stakeholders", f'''<div style="position:relative;width:1280px;height:760px">
<svg width="1280" height="760" style="position:absolute;left:0;top:0">{lines}</svg>
<div class="card fill-navy center" style="position:absolute;left:{cx-130}px;top:{cy-80}px;width:260px;gap:6px;padding:18px">{icon("Workflow",50,"#7FD3E0",2)}<h3 style="font-size:25px">DevOps 엔지니어</h3><p style="font-size:17px">가장 많은 부서와 이야기하는 사람</p></div>
{"".join(nodes)}</div>''', w=1320)

# 8. 인시던트 흐름
inc = [("BellRing", "red", "① 감지", "알림 · 고객 신고<br>고객보다 먼저"), ("Megaphone", "orange", "② 선언", "인시던트 선언<br>채널 열기"),
       ("Undo2", "orange", "③ 완화", "피해부터 멈춘다<br>직전 배포 되돌리기"), ("HeartPulse", "teal", "④ 복구", "정상화<br>정기 상태 공유"),
       ("NotebookPen", "green", "⑤ 회고", "비난 없는<br>포스트모템")]
roles = "".join(f'<div class="card grow" style="flex-direction:row;align-items:center;gap:10px;padding:12px 16px">{icon(i,34,c,2)}<div><div style="font-size:20px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:16px;color:var(--slate)">{d}</div></div></div>'
                for i, c, t, d in [("Crown", "navy", "지휘자", "판단 · 결정, 직접 안 고침"), ("Wrench", "teal", "작업 담당", "조사와 조치"), ("MessagesSquare", "orange", "커뮤니케이션", "정기 공유"), ("PenLine", "violet", "기록 담당", "타임라인")])
R("w1d5-incident", f'''{flowcards(inc, 76, 23, 17)}<div class="tag">장애 중의 역할</div><div class="row" style="gap:12px">{roles}</div>''')

# 9. 장애 교훈
R("w1d5-outage-lessons", f'''<div class="row" style="gap:22px;align-items:stretch">
<div class="card grow" style="gap:12px;border-color:var(--red)"><div class="row c" style="gap:12px">{ic("MonitorX","red",66)}<div><div class="tag">2024.7.19</div><h3 style="font-size:26px">CrowdStrike 업데이트 장애</h3></div></div>
 <div class="row" style="gap:10px"><div class="box grow" style="background:var(--red-l);color:var(--red);font-size:30px;font-weight:900">850만 대</div><div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:19px">Windows PC가<br>부팅 직후 멈춤</div></div>
 <p style="font-size:19px">원인: 설정 파일 하나(Channel File 291) · UTC 04:09 배포 → 05:27 되돌림, 받은 PC는 손으로 복구</p>
 <div class="box" style="background:var(--orange-l);color:var(--navy);font-size:19px;text-align:left">교훈: 설정도 배포다 · 일부에게 먼저(점진적 배포) · 되돌릴 수 없는 곳은 더 신중히</div></div>
<div class="card grow" style="gap:12px;border-color:var(--orange)"><div class="row c" style="gap:12px">{ic("CloudOff","orange",66)}<div><div class="tag">2025.10</div><h3 style="font-size:26px">AWS us-east-1 장애</h3></div></div>
 <div class="row" style="gap:10px"><div class="box grow" style="background:var(--orange-l);color:var(--orange);font-size:30px;font-weight:900">약 15시간</div><div class="box grow" style="background:var(--slate-l);color:var(--navy);font-size:19px">빈 DNS 레코드에서<br>연쇄 장애</div></div>
 <p style="font-size:19px">원인: DynamoDB DNS 관리 자동화의 경쟁 상태 (3일차)</p>
 <div class="box" style="background:var(--green-l);color:var(--navy);font-size:19px;text-align:left">교훈: 원인을 사람이 아니라 시스템에서 · 사후 보고서를 공개 · 재발 방지도 시스템 수준으로</div></div></div>''')

# 10. 세 가지 문서
docs = [("BookOpen", "teal", "README", "이게 뭐고, 어떻게 실행하나?", "처음 볼 때", ["무엇인가", "실행에 필요한 것", "실행 방법", "설정 · 문제 해결"]),
        ("ListChecks", "orange", "런북 (Runbook)", "이 상황에서 무엇을 순서대로?", "장애 · 반복 작업 때", ["확인할 지표", "복사해 쓰는 명령", "판단 기준 숫자", "다음 단계 조건"]),
        ("Scale", "violet", "ADR", "왜 이렇게 결정했나?", "구조를 바꾸고 싶을 때", ["배경", "결정", "고려한 대안", "결과(트레이드오프)"])]
dc = "".join(f'''<div class="card grow" style="gap:10px;border-color:var(--{c})"><div class="row c" style="gap:12px">{ic(i,c,64)}<h3 style="font-size:26px">{t}</h3></div>
<div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:20px">{q}</div><div class="note" style="font-size:18px">읽는 때: {w}</div>
<ul>{"".join(f"<li style='font-size:19px'>{x}</li>" for x in items)}</ul></div>''' for i, c, t, q, w, items in docs)
R("w1d5-docs", f'''<div class="row" style="gap:18px">{dc}</div>
<div class="card fill-slate" style="padding:14px 22px;flex-direction:row;align-items:center;gap:12px">{icon("GitBranch",34,"navy",2)}<p style="font-size:20px"><b style="color:var(--navy)">Docs as Code</b> — 문서도 Git에 두고, 코드와 같은 PR에서 고치고 리뷰한다</p></div>''')

# 11. 설치 흔적
tr = [("FileCog", "teal", "실행 파일", "/usr/lib/postgresql/16/bin"), ("Power", "orange", "서비스 등록", "postgresql.service"), ("Plug", "red", "포트", ":5432"),
      ("Settings", "violet", "설정 파일", "/etc/postgresql/16/main/"), ("Database", "violet", "데이터", "/var/lib/postgresql/16/main"),
      ("UserRound", "slate", "계정", "OS 사용자 postgres"), ("ScrollText", "slate", "로그", "/var/log/postgresql/")]
tc = "".join(f'<div class="card" style="flex-direction:row;align-items:center;gap:12px;padding:12px 16px;border-color:var(--{c})">{ic(i,c,50)}<div><div style="font-size:20px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:17px;{MONO};color:var(--slate)">{p}</div></div></div>' for i, c, t, p in tr)
R("w1d5-install-traces", f'''<div class="row" style="gap:24px;align-items:center">
<div class="col center" style="width:300px;gap:12px">{ic("Download","navy",100)}<div class="box" style="background:var(--navy);color:#fff;font-size:20px;{MONO}">sudo apt install postgresql</div><p style="font-size:19px;color:var(--slate);text-align:center">명령 한 줄이 OS 곳곳에<br>흔적을 남긴다</p></div>
<div class="col center" style="gap:4px">{arrow(size=44)}</div>
<div class="grid grow" style="grid-template-columns:1fr 1fr;gap:12px">{tc}<div class="card fill-red" style="padding:12px 16px;justify-content:center"><p style="font-size:18px"><b style="color:var(--navy)">지워도 남는다</b> — 데이터 · 설정 · 로그</p></div></div></div>''')

# 12. 손 설치 vs Docker
pain = [("버전 충돌", "14와 16을 한 OS에", "postgres:14 · postgres:16 이미지"), ("포트 충돌", "둘 다 5432", "-p 5433:5432"),
        ("설정 차이", "내 .env만 다르다", "-e · .env · compose.yaml"), ("삭제 후 흔적", "지워도 남는 파일", "docker rm — 흔적 없이"),
        ("재현 불가", "새 컴퓨터에서 하루", "compose.yaml 한 파일로 한 줄")]
pr = "".join(f'''<div class="row c" style="gap:12px"><div class="box" style="width:200px;background:var(--navy);color:#fff;font-size:20px">{k}</div>
<div class="box grow" style="background:var(--red-l);color:var(--red);font-size:19px">{a}</div>{icon("ArrowRight",30,"slate",2.5)}
<div class="box grow" style="background:var(--green-l);color:var(--green);font-size:19px;{MONO}">{b}</div></div>''' for k, a, b in pain)
R("w1d5-manual-vs-docker", f'''<div class="row" style="gap:12px"><div style="width:200px"></div><div class="tag grow" style="text-align:center">손으로 설치하면</div><div style="width:30px"></div><div class="tag grow" style="text-align:center">Docker로 하면 (2주차)</div></div>
<div class="col" style="gap:10px">{pr}</div>
<div class="row" style="gap:12px;justify-content:center">{"".join(f'<span class="chip" style="font-size:21px;background:var(--{c});color:#fff">{v}</span>' for v,c in [("포장한다","teal"),("격리한다","violet"),("연결한다","orange"),("재현한다","green")])}</div>''')

# 13. 1주차 지도
days = [("Cloud", "teal", "1일차", "클라우드 · 가상화", "Docker도 남의 컴퓨터에서"), ("Cpu", "violet", "2일차", "OS · 프로세스 · 격리", "컨테이너 = 격리된 프로세스"),
        ("Network", "orange", "3일차", "네트워크", "-p 포트 연결 · 컨테이너 네트워크"), ("Layers", "teal", "4일차", "앱 구조", "볼륨 · Compose"),
        ("Users", "green", "5일차", "DevOps · 협업", "README · GitHub")]
dc = []
for k, (i, c, d, t, n) in enumerate(days):
    dc.append(f'<div class="card center grow" style="gap:8px;border-color:var(--{c});padding:18px 10px"><span class="chip" style="background:var(--{c});color:#fff;font-size:18px">{d}</span>{ic(i,c,70)}<h3 style="font-size:22px">{t}</h3><div class="box" style="background:var(--slate-l);color:var(--slate);font-size:16px;width:100%">→ {n}</div></div>')
    if k < 4:
        dc.append(arrow(size=28))
R("w1d5-week1-map", f'''<div class="row flow" style="gap:6px">{"".join(dc)}</div>
<div class="row c" style="gap:14px;justify-content:center">{icon("ArrowDown",34,"navy",2.5)}<div class="box" style="background:var(--navy);color:#fff;font-size:23px;padding:14px 30px;display:flex;align-items:center;gap:12px">{icon("Container",34,"#7FD3E0",2)} 2주차 — Docker: 실행 조건을 포장하고 재현한다</div></div>''')


# 14. 브룩스 차트
def brooks_chart():
    if only and "w1d5-brooks" not in only:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    for f in (Path.home() / ".fonts").glob("Pretendard-*.otf"):
        fm.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Pretendard"
    ns = [3, 5, 10, 20, 50]
    vs = [n * (n - 1) // 2 for n in ns]
    fig, ax = plt.subplots(figsize=(12, 4.4), dpi=220)
    xs = range(len(ns))
    cols = ["#0089A0"] * 4 + ["#C8651B"]
    bars = ax.bar(xs, vs, color=cols, width=0.56)
    for b, v in zip(bars, vs):
        ax.text(b.get_x() + b.get_width() / 2, v + 25, f"{v:,}개", ha="center", fontsize=16, fontweight="bold", color="#1E293B")
    ax.set_xticks(list(xs)); ax.set_xticklabels([f"{n}명" for n in ns], fontsize=15, color="#1E293B")
    ax.set_yticks([]); ax.set_ylim(0, 1400)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.text(0, 1150, "소통 경로 = n(n−1)/2\n사람은 10배, 경로는 약 100배", fontsize=15, color="#C8651B", fontweight="bold", va="top")
    fig.text(0.01, 0.01, "Brooks, F. P. (1975). The Mythical Man-Month — 소통 경로 수 계산", fontsize=11, color="#94A3B8")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "w1d5-brooks.png", facecolor="white"); plt.close(fig)
    print("ok w1d5-brooks")


brooks_chart()
