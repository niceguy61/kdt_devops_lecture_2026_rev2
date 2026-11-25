"""1주차 1일차 다이어그램. 실행: python3 diagrams/w1d1.py"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, aws, arrow  # noqa: E402

OUT = ROOT / "assets" / "week1" / "day1"
only = set(sys.argv[1:])


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


# 1. 앱 하나의 여행 (5주 로드맵)
stops = [
    ("1주", "Laptop", "teal", "내 노트북", "컴퓨터·네트워크·<br>클라우드 개념", "★"),
    ("2주", "Container", "teal", "컨테이너", "Docker · Git<br>첫 실습", "★★"),
    ("3주", "Boxes", "violet", "MSA + K8s", "서비스 나누기<br>Kubernetes 입문", "★★★"),
    ("4주", "Gauge", "violet", "운영 도구", "Helm · 관찰<br>Argo CD · Istio", "★★★★"),
    ("5주", "Cloud", "orange", "AWS + IaC", "AWS 콘솔<br>Terraform", "★★★★★"),
    ("마지막 날", "Rocket", "orange", "EKS 배포", "클라우드 위<br>GitOps 완성", "🏁"),
]
cells = []
for i, (wk, ico, col, name, desc, star) in enumerate(stops):
    stars = star if star != "🏁" else "목표"
    cells.append(f'''<div class="card center grow" style="padding:26px 14px;gap:14px">
      <span class="chip {'teal' if col=='teal' else ('orange' if col=='orange' else 'navy')}">{wk}</span>
      {ic(ico, col, 96)}<h3 style="font-size:29px">{name}</h3>
      <p style="font-size:21px">{desc}</p>
      <div class="note t-orange" style="font-weight:800;letter-spacing:2px">{stars}</div></div>''')
    if i < len(stops) - 1:
        cells.append(arrow(size=36))
R("w1d1-journey", f'''<div class="hd">앱 하나의 여행 — 5주 로드맵</div>
<div class="sub">같은 애플리케이션이 노트북에서 출발해 클라우드의 Kubernetes까지 이동합니다</div>
<div class="row flow" style="gap:10px">{''.join(cells)}</div>''')

# 2. 직무 지도
roles = [
    ("Workflow", "teal", "DevOps 엔지니어", ["코드가 서비스가 되는 길을 자동화", "CI/CD 파이프라인, 배포 전략", "개발팀과 운영팀 연결"]),
    ("Cloud", "orange", "클라우드 엔지니어", ["AWS 같은 클라우드 인프라 설계·구축", "네트워크·권한·비용 관리", "Terraform으로 인프라를 코드화"]),
    ("Activity", "red", "SRE", ["서비스가 멈추지 않게 지키는 사람", "모니터링·알림·장애 대응", "안정성 목표(SLO) 관리"]),
    ("LayoutGrid", "violet", "플랫폼 엔지니어", ["개발자가 쓰는 내부 플랫폼 제작", "Kubernetes·셀프서비스 도구", "표준 템플릿과 가드레일"]),
]
rc = "".join(f'''<div class="card"><div class="row c" style="gap:18px">{ic(i, c, 80)}<h3>{t}</h3></div>
<ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div>''' for i, c, t, items in roles)
R("w1d1-roles", f'''<div class="hd">이 과정이 향하는 직무</div>
<div class="grid" style="grid-template-columns:1fr 1fr">{rc}</div>
<div class="card fill-navy" style="padding:18px 28px"><p style="font-size:24px;color:#fff"><b>공통 기본기</b> &nbsp; Linux · 네트워크 · 컨테이너 · 클라우드 · 코드로 관리하기 · <b style="color:#ffd7b0">소통과 문서화</b></p></div>''')

# 3. 하루 수업 리듬
blocks = [("1", "어제 10분 요약<br>+ 오늘 주제", "navy"), ("2", "개념", "teal"), ("3", "개념·그림", "teal"),
          ("4", "시연·실습", "teal"), ("점심", "", "lunch"), ("5", "시연·실습", "teal"), ("6", "확장·사례", "teal"),
          ("7", "장애·정리", "teal"), ("8", "배움일기", "orange")]
bc = []
for n, t, c in blocks:
    if c == "lunch":
        bc.append('<div class="box" style="background:#fff;border:2px dashed var(--line);color:var(--muted);flex:0.6;display:flex;align-items:center;justify-content:center">점심</div>')
        continue
    bg = {"navy": "var(--navy)", "teal": "var(--teal-l)", "orange": "var(--orange)"}[c]
    fg = "#fff" if c != "teal" else "var(--navy)"
    bc.append(f'<div class="box" style="background:{bg};color:{fg};flex:1;padding:22px 8px"><div style="font-size:38px;font-weight:900">{n}</div><div style="font-size:19px;font-weight:600;margin-top:8px">{t}교시</div></div>'
              .replace(f'{t}교시', (t + '<br><span style="opacity:.7">' + n + '교시</span>')))
R("w1d1-day-rhythm", f'''<div class="hd">하루 8교시의 리듬</div>
<div class="row" style="gap:12px;height:250px">{''.join(bc)}</div>
<div class="row" style="gap:24px">
 <div class="card fill-slate grow"><div class="row c">{ic('Timer','teal',64)}<h3>50분 수업 + 10분 휴식</h3></div><p>매 정시에 시작합니다. 쉬는 시간에는 화면에서 눈을 떼세요.</p></div>
 <div class="card fill-orange grow"><div class="row c">{ic('NotebookPen','orange',64)}<h3>8교시 배움일기</h3></div><p>이해한 것 · 막힌 것 · 다시 해볼 것 · 내일 질문 — 짧은 메모도 좋습니다.</p></div>
</div>''')

# 4. 좋은 질문 템플릿
qrows = [("Target", "하려던 것", "nginx 컨테이너를 8080 포트로 띄우려고 했습니다"),
         ("Terminal", "실행한 명령", "docker run -p 8080:80 nginx"),
         ("CircleAlert", "보인 결과", "에러 원문: port is already allocated"),
         ("Wrench", "시도한 것", "docker ps로 확인 → 다른 컨테이너가 8080 사용 중"),
         ("Monitor", "환경", "Windows 11 + WSL2, Docker Desktop 4.x")]
qr = "".join(f'<div class="row c" style="gap:16px">{ic(i,"teal",56)}<div style="width:150px;font-size:22px;font-weight:800;color:var(--navy)">{k}</div><div style="font-size:21px;color:var(--slate);font-family:Pretendard">{v}</div></div>' for i, k, v in qrows)
R("w1d1-good-question", f'''<div class="hd">질문을 "증거"로 바꾸기</div>
<div class="row" style="gap:28px">
 <div class="card fill-red center" style="flex:0.75;justify-content:center;gap:20px">{ic('MessageCircleX','red',110)}
   <div class="big t-red" style="font-size:60px">"안 돼요…"</div>
   <p>무엇이, 어디서, 왜 안 되는지<br>도와주는 사람이 알 수 없습니다</p></div>
 {arrow(size=56)}
 <div class="card fill-green" style="flex:1.6;gap:16px"><h3 style="margin-bottom:6px">도움받기 쉬운 질문 5줄</h3>{qr}</div>
</div>''')

# 5. 작은 앱 vs 운영 가능한 서비스 (빙산)
below = [("Cpu", "실행 환경"), ("ShieldCheck", "보안·권한"), ("Network", "인프라·네트워크"), ("Rocket", "배포·되돌리기"),
         ("Activity", "모니터링"), ("Wallet", "비용"), ("Siren", "장애 대응"), ("FileText", "문서·인수인계")]
bl = "".join(f'<div class="card center" style="background:rgba(255,255,255,.92);border-color:#b9dbe4;padding:20px 10px;gap:10px">{ic(i,"navy",64)}<div style="font-size:24px;font-weight:800;color:var(--navy)">{t}</div></div>' for i, t in below)
R("w1d1-app-vs-service", f'''
<div class="row c" style="justify-content:center;gap:24px">
  <div class="card fill-orange center" style="width:560px;padding:22px">{ic('Sparkles','orange',70)}<h3>화면 + 코드</h3><p>AI가 몇 분 만에 만들어 주는 부분</p></div>
  <div class="note" style="width:360px">물 위에 보이는 부분은 <b>작습니다</b>.<br>실제 서비스는 아래가 훨씬 큽니다.</div>
</div>
<div style="background:linear-gradient(180deg,#d6eef3,#a9d4df);border-radius:28px;padding:30px;position:relative">
  <div class="tag" style="color:var(--teal-d);margin-bottom:16px">운영 가능한 서비스가 되려면 필요한 것</div>
  <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:18px">{bl}</div>
</div>''')

# 6. AI 결과 검증 흐름
steps = [("Bot", "slate", "AI 제안", "코드·명령·설정"),
         ("ListChecks", "teal", "① 조건 확인", "무엇이 필요한가?<br>런타임·포트·데이터"),
         ("ShieldAlert", "orange", "② 안전 확인", "비밀값·비용·권한<br>삭제 명령은 없는가?"),
         ("Play", "teal", "③ 실행 검증", "직접 실행하고<br>로그·상태로 확인"),
         ("FileCheck", "green", "④ 기록", "README·runbook에<br>재현 방법 기록")]
sc = []
for i, (ico, col, t, d) in enumerate(steps):
    sc.append(f'<div class="card center grow" style="gap:14px">{ic(ico,col,96)}<h3>{t}</h3><p>{d}</p></div>')
    if i < len(steps) - 1:
        sc.append(arrow(size=40))
R("w1d1-ai-verify", f'''<div class="hd">AI 결과물은 "완료"가 아니라 "후보"입니다</div>
<div class="row flow" style="gap:12px">{''.join(sc)}</div>
<div class="card fill-slate" style="padding:18px 26px"><p style="font-size:23px"><b style="color:var(--navy)">기억할 것</b> — AI에게 좋은 답을 받는 사람은 프롬프트를 예쁘게 쓰는 사람이 아니라, <b style="color:var(--teal-d)">실행 조건과 검증 기준을 아는 사람</b>입니다.</p></div>''')

# 7. 서버의 역사 타임라인
tl = [("1990s", "Building", "navy", "회사 서버실", "직접 사고, 직접 설치"),
      ("2000s", "Warehouse", "navy", "IDC 입주", "공간·전력·회선을 빌림"),
      ("1999~", "Layers", "teal", "가상화", "서버 1대를 VM 여러 대로"),
      ("2006", "Cloud", "orange", "AWS S3·EC2", "API로 서버를 빌리는 시대"),
      ("2013~15", "Container", "violet", "Docker·K8s", "앱 단위로 포장·자동 운영")]
tc = []
for i, (yr, ico, col, t, d) in enumerate(tl):
    tc.append(f'''<div class="col center grow" style="gap:14px">
      <div style="font-size:30px;font-weight:900;color:var(--{'teal' if col=='teal' else col if col!='navy' else 'navy'})">{yr}</div>
      {ic(ico,col,104)}
      <div class="card center" style="padding:18px 12px;gap:6px;width:100%"><h3 style="font-size:27px">{t}</h3><p style="font-size:20px">{d}</p></div></div>''')
    if i < len(tl) - 1:
        tc.append(arrow(size=34))
R("w1d1-history", f'''<div class="hd">서버를 다루는 방식의 변화</div>
<div class="sub">점점 "물건"이 아니라 "필요할 때 요청하는 서비스"가 되어 왔습니다</div>
<div class="row c" style="gap:8px">{''.join(tc)}</div>''')

# 8. 데이터센터 해부도
dc = [("Server", "teal", "서버 랙", "수백~수천 대의 서버가<br>표준 크기 선반(랙)에"),
      ("Network", "teal", "네트워크", "스위치·라우터·방화벽<br>외부 인터넷 회선"),
      ("HardDrive", "teal", "스토리지", "디스크 장비, 백업 장치<br>데이터 복제"),
      ("Zap", "orange", "전력", "이중 전원, UPS,<br>비상 발전기"),
      ("Snowflake", "orange", "냉각", "항온항습기, 공조<br>서버 열 식히기"),
      ("Lock", "red", "물리 보안", "출입 통제, CCTV,<br>보안 인력")]
dcc = "".join(f'<div class="card" style="gap:10px"><div class="row c" style="gap:16px">{ic(i,c,72)}<h3>{t}</h3></div><p>{d}</p></div>' for i, c, t, d in dc)
R("w1d1-datacenter", f'''<div class="hd">데이터센터에는 서버만 있는 것이 아닙니다</div>
<div class="grid" style="grid-template-columns:repeat(3,1fr)">{dcc}</div>
<div class="card fill-navy" style="padding:18px 28px"><div class="row c" style="gap:18px">{ic('Users','white',58,'#1E3A5F')}<p style="font-size:23px;color:#fff">그리고 <b>24시간 운영 인력</b> — 고장 난 디스크 교체, 장비 증설, 장애 대응까지 모두 사람이 합니다</p></div></div>''')

# 9. 가상화 전/후
def srv(label, apps, util, col):
    a = "".join(f'<div class="box" style="background:var(--{col}-l);color:var(--navy);padding:10px;font-size:19px;width:100%">{x}</div>' for x in apps)
    return f'''<div class="card center" style="padding:16px;gap:10px;flex:1">{a}
      <div class="box" style="background:var(--slate-l);color:var(--slate);padding:8px;font-size:18px">{label}</div>
      <div style="width:100%;height:14px;background:var(--slate-l);border-radius:7px;overflow:hidden"><div style="width:{util}%;height:100%;background:var(--{ 'orange' if util<40 else 'teal'})"></div></div>
      <div class="note">사용률 약 {util}%</div></div>'''
before = "".join(srv("물리 서버", [f"앱 {x}", "OS"], u, "orange") for x, u in (("A", 15), ("B", 10), ("C", 20)))
vms = "".join(f'<div class="card center" style="padding:12px;gap:8px;flex:1;border-color:#9fd6df"><div class="tag">VM</div><div class="box" style="background:var(--teal-l);color:var(--navy);padding:10px;font-size:19px;width:100%">앱 {x}</div><div class="box" style="background:var(--teal-l);color:var(--navy);padding:10px;font-size:19px;width:100%">OS</div></div>' for x in "ABC")
R("w1d1-virtualization", f'''<div class="hd">가상화 — 물리 서버 1대를 여러 대처럼 쓰기</div>
<div class="row" style="gap:30px;align-items:center">
 <div class="col grow"><div class="tag">가상화 전 · 앱마다 서버 1대</div><div class="row" style="gap:14px">{before}</div></div>
 {arrow(size=56)}
 <div class="col grow"><div class="tag">가상화 후 · 서버 1대에 VM 3대</div>
   <div class="card" style="padding:16px;gap:10px"><div class="row" style="gap:12px">{vms}</div>
   <div class="box" style="background:var(--navy);color:#fff">하이퍼바이저 (가상화 소프트웨어)</div>
   <div class="box" style="background:var(--slate-l);color:var(--slate)">물리 서버 1대 (CPU · 메모리 · 디스크)</div>
   <div style="width:100%;height:14px;background:var(--slate-l);border-radius:7px;overflow:hidden"><div style="width:70%;height:100%;background:var(--teal)"></div></div>
   <div class="note center">사용률 약 70% · 남는 서버 2대 절약</div></div></div>
</div>
<div class="note">※ 사용률 수치는 이해를 돕기 위한 예시입니다</div>''')

# 10. NIST 5대 특성
nist = [("MousePointerClick", "주문형 셀프서비스", "담당자에게 전화하지 않고<br>웹 화면·API로 직접 생성"),
        ("Globe", "어디서나 네트워크 접근", "인터넷만 되면<br>노트북·휴대폰에서 접근"),
        ("Layers", "자원 풀링", "거대한 자원을 여러 고객이<br>나눠 씀 (위치는 몰라도 됨)"),
        ("Expand", "빠른 탄력성", "필요하면 몇 분 만에 늘리고<br>필요 없으면 바로 줄임"),
        ("Gauge", "측정되는 서비스", "쓴 만큼 측정되고<br>쓴 만큼 청구됨")]
nc = "".join(f'<div class="card center grow" style="gap:14px;padding:26px 14px"><div class="big t-teal" style="font-size:40px">{n}</div>{ic(i,"teal",88)}<h3 style="font-size:26px">{t}</h3><p style="font-size:20px">{d}</p></div>' for n, (i, t, d) in enumerate(nist, 1))
R("w1d1-nist5", f'''<div class="hd">클라우드의 5가지 특징</div>
<div class="sub">미국 표준기술연구소(NIST)의 정의 · 이 5가지가 있어야 "클라우드"라고 부릅니다</div>
<div class="row" style="gap:16px">{nc}</div>''')

# 11. 서비스 모델 책임 스택
layers = ["애플리케이션", "데이터", "런타임", "미들웨어", "운영체제(OS)", "가상화", "서버", "스토리지", "네트워크"]
own = {"온프레미스": 9, "IaaS": 5, "PaaS": 2, "SaaS": 0}
ex = {"온프레미스": "회사 서버실", "IaaS": "Amazon EC2", "PaaS": "AWS Elastic Beanstalk", "SaaS": "Gmail · Slack"}
cols = []
for m, k in own.items():
    cells_ = "".join(
        f'<div class="box" style="padding:9px 6px;font-size:19px;border-radius:10px;background:{"var(--teal)" if idx < k else "var(--slate-l)"};color:{"#fff" if idx < k else "var(--muted)"}">{l}</div>'
        for idx, l in enumerate(layers))
    cols.append(f'<div class="col grow" style="gap:6px"><div style="font-size:28px;font-weight:900;color:var(--navy);text-align:center">{m}</div>{cells_}<div class="note center" style="margin-top:6px">예) {ex[m]}</div></div>')
R("w1d1-service-models", f'''<div class="row" style="gap:20px;align-items:flex-end">
 <div class="hd grow">누가 어디까지 관리하는가</div>
 <div class="row c" style="gap:10px"><span class="box" style="background:var(--teal);color:#fff;padding:6px 14px;font-size:20px">내가 관리</span><span class="box" style="background:var(--slate-l);color:var(--muted);padding:6px 14px;font-size:20px">제공자가 관리</span></div></div>
<div class="row" style="gap:22px">{''.join(cols)}</div>''')

# 12. 피자 비유
pz = [("ChefHat", "teal", "집에서 직접", "온프레미스", "반죽·오븐·가스·식탁<br>모두 내가 준비"),
      ("ShoppingBag", "teal", "냉동 피자 사서 굽기", "IaaS", "피자는 사오고<br>오븐·굽기는 내가"),
      ("Bike", "orange", "배달 주문", "PaaS", "요리는 가게가<br>식탁·음료만 내가"),
      ("UtensilsCrossed", "orange", "식당에서 먹기", "SaaS", "가서 먹기만<br>나머지는 전부 식당이")]
pc = []
for i, (ico, col, t, m, d) in enumerate(pz):
    pc.append(f'<div class="card center grow" style="gap:12px">{ic(ico,col,100)}<span class="chip {"teal" if col=="teal" else "orange"}">{m}</span><h3 style="font-size:27px">{t}</h3><p>{d}</p></div>')
    if i < 3:
        pc.append(arrow(size=34))
R("w1d1-pizza", f'''<div class="hd">피자로 이해하는 서비스 모델</div>
<div class="sub">오른쪽으로 갈수록 내가 할 일은 줄고, 대신 고를 수 있는 자유도도 줄어듭니다</div>
<div class="row flow" style="gap:8px">{''.join(pc)}</div>''')

# 13. 공유 책임 모델
cust = ["고객 데이터", "IAM 사용자·권한", "OS 패치·보안 업데이트 (EC2)", "보안 그룹·방화벽 설정", "암호화 설정"]
awsr = ["데이터센터 물리 보안", "서버·스토리지·네트워크 하드웨어", "리전·가용 영역 인프라", "가상화 계층(하이퍼바이저)"]
cc = "".join(f'<div class="box" style="background:#fff;color:var(--navy);flex:1;font-size:20px;padding:14px 8px">{x}</div>' for x in cust)
ac = "".join(f'<div class="box" style="background:rgba(255,255,255,.12);color:#fff;flex:1;font-size:20px;padding:14px 8px">{x}</div>' for x in awsr)
R("w1d1-shared-responsibility", f'''<div class="hd">공유 책임 모델 — 책임을 나눠 갖는다</div>
<div class="card fill-orange" style="gap:14px"><div class="row c" style="gap:16px">{ic('User','orange',66)}<div><h3>고객 책임 — 클라우드 "안"의 보안</h3><p>내가 만든 것, 내가 설정한 것</p></div></div><div class="row" style="gap:12px">{cc}</div></div>
<div class="card fill-navy" style="gap:14px"><div class="row c" style="gap:16px">{aws('AWS-Cloud-logo_32',66)}<div><h3>AWS 책임 — 클라우드 "자체"의 보안</h3><p>클라우드를 돌리는 바닥 인프라</p></div></div><div class="row" style="gap:12px">{ac}</div></div>
<div class="note">※ 경계선은 서비스마다 다릅니다. EC2는 OS 패치가 고객 몫이지만, RDS·Lambda 같은 관리형 서비스는 AWS가 더 많이 맡습니다</div>''')

# 14. 리전 / AZ
def az(n):
    dcs = "".join(f'<div class="col center" style="gap:4px">{icon("Building2",54,"slate",1.8)}<div class="note" style="font-size:17px">데이터센터</div></div>' for _ in range(2))
    return f'''<div style="border:3px dashed var(--aws-az);border-radius:16px;padding:18px;flex:1;display:flex;flex-direction:column;gap:12px;align-items:center">
      <div style="font-size:24px;font-weight:800;color:var(--aws-az)">가용 영역 {n}</div><div class="row" style="gap:22px">{dcs}</div></div>'''
azs = "".join(az(x) for x in ("A", "B", "C"))
R("w1d1-region-az", f'''
 <div style="border:3px dashed var(--aws-region);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:16px">
   <div class="row c" style="gap:14px">{aws('Region_32',48)}<div style="font-size:30px;font-weight:900;color:var(--aws-region)">리전(Region) — 예: 서울 ap-northeast-2</div></div>
   <div class="row" style="gap:18px">{azs}</div>
   <div class="box" style="background:var(--teal-l);color:var(--teal-d)">가용 영역끼리는 전용 고속 네트워크로 연결 · 서로 수 km 이상 떨어져 있음</div>
 </div>
 <div class="row" style="gap:18px">
  <div class="card grow"><h3>리전</h3><p>지리적으로 떨어진 지역 단위. 서울, 도쿄, 버지니아 …</p></div>
  <div class="card grow"><h3>가용 영역(AZ)</h3><p>리전 안의 독립된 데이터센터 묶음. 전력·네트워크가 분리돼 있음</p></div>
  <div class="card fill-orange grow"><h3>왜 나눌까?</h3><p>AZ 하나가 멈춰도 다른 AZ에서 서비스를 이어가려고</p></div>
 </div>''')

# 15. 비용 함정
traps = [("Server", "켜두고 잊은 서버", "실습 끝나고 그대로 둔 EC2·DB는<br>쓰지 않아도 시간당 과금"),
         ("Router", "NAT Gateway", "켜져 있는 시간 + 지나간 데이터 양<br>둘 다 과금"),
         ("Globe", "퍼블릭 IPv4 주소", "2024년부터 퍼블릭 IPv4는<br>개당 시간당 $0.005"),
         ("Split", "로드밸런서", "트래픽이 없어도<br>켜져 있으면 시간당 과금"),
         ("Ship", "EKS 클러스터", "컨트롤 플레인만<br>시간당 $0.10 (월 약 $73)"),
         ("Archive", "쌓이는 로그·스냅샷", "작아 보여도 매달 쌓이면<br>계속 늘어나는 저장 비용")]
tcc = "".join(f'<div class="card" style="gap:10px"><div class="row c" style="gap:16px">{ic(i,"red",68)}<h3 style="font-size:27px">{t}</h3></div><p style="font-size:21px">{d}</p></div>' for i, t, d in traps)
R("w1d1-cost-traps", f'''<div class="hd">초보자가 가장 많이 당하는 비용 함정</div>
<div class="grid" style="grid-template-columns:repeat(3,1fr)">{tcc}</div>
<div class="card fill-green" style="padding:16px 26px"><div class="row c" style="gap:16px">{ic('BellRing','green',56)}<p style="font-size:23px"><b style="color:var(--green)">해결책</b> — 실습 첫날 Budget 알림 설정 · 매일 끝나기 전 "삭제 점검" · 태그 붙이기</p></div></div>
<div class="note">※ 요금은 2026년 11월 기준 AWS 공개 가격이며, 리전과 시점에 따라 달라질 수 있습니다</div>''')


# 16. CAPEX vs OPEX 누적 비용 (개념 차트, 예시 값)
def capex_chart():
    if only and "w1d1-capex-opex" not in only:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    for f in (Path.home() / ".fonts").glob("Pretendard-*.otf"):
        fm.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Pretendard"
    m = list(range(0, 37))
    onprem = [9000 + 150 * x for x in m]          # 초기 장비 9,000만 원 + 월 운영 150만 원
    cloud = [450 * x for x in m]                   # 초기 0 + 월 사용료 450만 원
    fig, ax = plt.subplots(figsize=(12, 5.4), dpi=220)
    ax.plot(m, onprem, color="#0089A0", lw=2.6, label="온프레미스 (CAPEX 중심)")
    ax.plot(m, cloud, color="#C8651B", lw=2.6, label="클라우드 (OPEX 중심)")
    ax.scatter([30], [13500], s=70, color="#1E293B", zorder=5)
    ax.annotate("약 30개월에 누적 비용 역전", xy=(30, 13500), xytext=(17.5, 15200), fontsize=14, color="#1E293B",
                arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=1.2))
    ax.annotate("첫 달에 장비 구매로\n큰돈이 한 번에 나감", xy=(0, 9000), xytext=(1.2, 10600), fontsize=13, color="#475569")
    ax.annotate("처음엔 0원,\n쓰는 만큼 매달 나감", xy=(4, 1800), xytext=(11, 900), fontsize=13, color="#475569")
    ax.text(36.4, onprem[-1], "온프레미스", color="#0089A0", fontsize=14, va="center", fontweight="bold")
    ax.text(36.4, cloud[-1], "클라우드", color="#C8651B", fontsize=14, va="center", fontweight="bold")
    ax.set_xlim(0, 40); ax.set_ylim(0, 17500)
    ax.set_xlabel("사용 개월 수", fontsize=13, color="#475569")
    ax.set_ylabel("누적 비용 (만 원)", fontsize=13, color="#475569")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    for s in ("left", "bottom"): ax.spines[s].set_color("#CBD5E1")
    ax.tick_params(colors="#64748B", labelsize=12)
    ax.grid(axis="y", color="#E2E8F0", lw=1)
    ax.legend(loc="upper left", frameon=False, fontsize=13)
    fig.text(0.01, 0.005, "※ 이해를 돕기 위한 예시 값입니다. 실제 비용은 규모·할인·운영 방식에 따라 크게 달라집니다.", fontsize=11, color="#94A3B8")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out = OUT / "w1d1-capex-opex.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    print("ok w1d1-capex-opex")


capex_chart()


# ───────── 확장: 학술·트렌드 다이어그램
# 17. 학습 과학 → 수업 설계
ls_ = [("Brain", "teal", "인지 부하 이론", "Sweller, 1988", "1주차는 실습 없이 개념에 집중"),
       ("ListOrdered", "teal", "예제 학습 효과", "Kalyuga 외, 2003", "실습을 101 단계로 잘게 쪼갬"),
       ("CircleHelp", "orange", "인출 연습", "Roediger & Karpicke, 2006", "매 교시 확인 문제"),
       ("CalendarClock", "orange", "간격 반복", "Ebbinghaus, 1885", "매일 1교시 어제 10분 요약"),
       ("NotebookPen", "violet", "메타인지", "아는 것과 모르는 것을 아는 힘", "8교시 배움일기"),
       ("Mountain", "violet", "바람직한 어려움", "Bjork, 1994", "3~5주차는 일부러 어렵게")]
lc = "".join(f"""<div class="card" style="gap:8px"><div class="row c" style="gap:14px">{ic(i,c,70)}<div><h3 style="font-size:27px">{t}</h3><div class="note" style="font-size:18px">{src}</div></div></div>
  <div class="row c" style="gap:10px;margin-top:6px">{icon('ArrowRight',26,'muted')}<p style="font-size:22px;color:var(--navy);font-weight:700">{d}</p></div></div>""" for i, c, t, src, d in ls_)
R("w1d1-learning-science", f"""<div class="grid" style="grid-template-columns:repeat(3,1fr)">{lc}</div>""")

# 18. DevOps 역사 타임라인
hist = [("2003", "navy", "SRE 탄생", "구글, 운영을<br>소프트웨어로"),
        ("2008", "teal", "Agile Infrastructure", "Debois & Shafer"),
        ("2009", "teal", "10+ Deploys/Day", "Flickr · 첫 DevOpsDays"),
        ("2013", "violet", "피닉스 프로젝트", "DevOps 대중화"),
        ("2016", "violet", "SRE 책 · 핸드북", "실천법 체계화"),
        ("2018", "orange", "Accelerate", "DORA 4대 지표"),
        ("2025", "orange", "AI = 증폭기", "DORA 2025 보고서"),
        ("2026", "red", "에이전트 시대", "PR 40%가 에이전트 시작<br>(Octoverse 2026)")]
hc = []
for k, (y, c, t, d) in enumerate(hist):
    hc.append(f"""<div class="col center grow" style="gap:10px"><div style="font-size:30px;font-weight:900;color:var(--{c})">{y}</div>
      <div style="width:22px;height:22px;border-radius:50%;background:var(--{c});box-shadow:0 0 0 6px #fff"></div>
      <div class="card center" style="padding:16px 10px;gap:6px;width:100%"><h3 style="font-size:23px">{t}</h3><p style="font-size:18px">{d}</p></div></div>""")
R("w1d1-devops-history", f"""<div style="position:relative"><div style="position:absolute;left:5%;right:5%;top:64px;height:4px;background:var(--line)"></div>
<div class="row" style="gap:12px;position:relative">{''.join(hc)}</div></div>""")

# 19. DORA 4대 지표
dk_ = [("속도", "teal", [("Rocket", "배포 빈도", "얼마나 자주 운영에 배포하나?"), ("Timer", "변경 리드 타임", "커밋에서 운영 반영까지 얼마나?")]),
       ("안정성", "orange", [("CircleX", "변경 실패율", "배포 중 몇 %가 장애·롤백으로?"), ("LifeBuoy", "복구 시간", "장애 후 얼마나 빨리 복구하나?")])]
cols = []
for title, c, items in dk_:
    it = "".join(f'<div class="card" style="gap:6px;padding:22px"><div class="row c" style="gap:14px">{ic(i,c,68)}<h3 style="font-size:28px">{t}</h3></div><p style="font-size:22px">{d}</p></div>' for i, t, d in items)
    cols.append(f'<div class="col grow" style="gap:16px"><div class="box" style="background:var(--{c});color:#fff;font-size:26px">{title}</div>{it}</div>')
R("w1d1-dora", f"""<div class="row" style="gap:26px">{''.join(cols)}</div>
<div class="card fill-navy" style="padding:18px 28px"><p style="font-size:23px;color:#fff"><b>DORA의 핵심 발견</b> — 상위 팀은 <b style="color:#7FD3E0">더 자주</b> 배포하면서도 <b style="color:#ffd7b0">더 안정적</b>이다. 속도와 안정성은 서로를 희생하지 않는다</p></div>""")

# 20. AI 숫자 타일
tiles = [("83%", "teal", "업무에 AI 도구를 쓰는 개발자<br>(안 쓴다 17.2%)", "Stack Overflow 2026"),
         ("6.6%", "orange", "중요한 결정을 AI에 맡기겠다는<br>개발자", "Stack Overflow 2026"),
         ("40%+", "violet", "AI 에이전트가 시작한<br>GitHub PR (2026년 9월)", "GitHub Octoverse 2026"),
         ("38%", "red", "보안 취약점이 생긴<br>AI 코드 생성 과제", "Veracode 2026년 10월"),
         ("+19%", "red", "숙련자가 AI 사용 시 늘어난 작업 시간<br>(본인 체감은 20% 단축)", "METR RCT 2025"),
         ("J-커브", "slate", "AI 도입 초기엔 생산성이<br>잠시 떨어졌다가 오른다", "DORA ROI 보고서 2026")]
tc_ = "".join(f"""<div class="card" style="gap:8px;padding:24px 26px"><div style="font-size:56px;font-weight:900;color:var(--{c if c!='slate' else 'slate'});letter-spacing:-1px">{n}</div>
  <p style="font-size:22px;color:var(--navy);font-weight:700;line-height:1.35">{d}</p><div class="note" style="font-size:17px">{src}</div></div>""" for n, c, d, src in tiles)
R("w1d1-ai-numbers", f"""<div class="grid" style="grid-template-columns:repeat(3,1fr)">{tc_}</div>
<div class="note">※ 각 수치의 조사 대상과 방법은 서로 다릅니다. 본문 표와 참고 문헌을 함께 보세요</div>""")

# 21. FinOps 순환
fs_ = [("Eye", "teal", "알리기", "Inform", "누가·어디에·얼마를<br>쓰는지 보이게"),
       ("Scissors", "orange", "최적화하기", "Optimize", "낭비를 줄이고<br>알맞은 크기로"),
       ("Settings2", "violet", "운영하기", "Operate", "규칙을 만들고<br>꾸준히 지키기")]
fc = []
for k, (i, c, t, en, d) in enumerate(fs_):
    fc.append(f'<div class="card center grow" style="gap:12px">{ic(i,c,100)}<h3 style="font-size:32px">{t}</h3><div class="tag">{en}</div><p style="font-size:22px">{d}</p></div>')
    fc.append(arrow(size=40))
fc.append(f'<div class="col center" style="gap:8px;flex:0.55;align-self:center">{ic("RefreshCw","navy",90)}<div style="font-size:21px;font-weight:800;color:var(--navy)">반복</div></div>')
R("w1d1-finops", f"""<div class="row flow" style="gap:12px">{''.join(fc)}</div>
<div class="card fill-slate" style="padding:16px 26px"><p style="font-size:22px"><b style="color:var(--navy)">FinOps = Finance + DevOps</b> — 엔지니어·재무·비즈니스 팀이 함께 클라우드 비용에 책임지는 문화 (FinOps Foundation)</p></div>""")


# 22. 클라우드 점유율 차트
def share_chart():
    if only and "w1d1-cloud-share" not in only:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    for f in (Path.home() / ".fonts").glob("Pretendard-*.otf"):
        fm.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Pretendard"
    names = ["AWS", "Microsoft", "Google", "기타 전체"]
    vals = [26, 19, 16, 39]
    cols = ["#0089A0", "#0089A0", "#0089A0", "#CBD5E1"]
    fig, ax = plt.subplots(figsize=(12, 4.2), dpi=220)
    y = list(range(len(names)))[::-1]
    ax.barh(y, vals, color=cols, height=0.56)
    for yy, v, n in zip(y, vals, names):
        ax.text(v + 0.6, yy, f"{v}%", va="center", fontsize=16, color="#1E293B", fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=15, color="#1E293B")
    ax.set_xlim(0, 45); ax.set_xticks([])
    for s_ in ("top", "right", "bottom"): ax.spines[s_].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.text(45, 3.45, "상위 3사 합계 61% · 분기 시장 규모 1,677억 달러 (전년 대비 +55%)", ha="right", fontsize=14, color="#475569")
    fig.text(0.01, 0.01, "출처: Synergy Research Group, 2026년 3분기 클라우드 인프라 서비스 시장 점유율", fontsize=11, color="#94A3B8")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(OUT / "w1d1-cloud-share.png", facecolor="white"); plt.close(fig)
    print("ok w1d1-cloud-share")


share_chart()
