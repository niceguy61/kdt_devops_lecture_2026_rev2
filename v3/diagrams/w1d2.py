"""1주차 2일차 다이어그램. 실행: python3 diagrams/w1d2.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, aws, arrow  # noqa: E402

OUT = ROOT / "assets" / "week1" / "day2"
only = set(sys.argv[1:])


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def flow(items, gap=12):
    """[(icon,color,title,desc)] → 화살표로 이어진 카드 행"""
    out = []
    for i, (ico, col, t, d) in enumerate(items):
        out.append(f'<div class="card center grow" style="gap:12px">{ic(ico,col,90)}<h3 style="font-size:27px">{t}</h3><p style="font-size:21px">{d}</p></div>')
        if i < len(items) - 1:
            out.append(arrow(size=36))
    return f'<div class="row flow" style="gap:{gap}px">{"".join(out)}</div>'


def layer(text, bg, fg="var(--navy)", size=24, pad=18, extra=""):
    return f'<div class="box" style="background:{bg};color:{fg};font-size:{size}px;padding:{pad}px;{extra}">{text}</div>'


# 1. 컴퓨터 부품 + 식당 비유
parts = [("Cpu", "teal", "CPU", "계산하고 실행", "요리사", "vCPU 개수"),
         ("MemoryStick", "violet", "메모리 (RAM)", "지금 쓰는 데이터<br>전원 끄면 사라짐", "조리대", "GiB 크기"),
         ("HardDrive", "orange", "디스크 (SSD)", "오래 보관<br>전원 꺼도 남음", "창고·냉장고", "EBS 볼륨"),
         ("Network", "green", "네트워크 카드", "다른 컴퓨터와<br>데이터 주고받기", "주문 창구", "Gbps 대역폭")]
pc = "".join(f'''<div class="card center grow" style="gap:10px">{ic(i,c,96)}<h3 style="font-size:28px">{t}</h3><p style="font-size:21px">{d}</p>
  <div class="box" style="background:var(--slate-l);color:var(--navy);font-size:20px;padding:10px;width:100%">비유: {a}</div>
  <div class="note" style="font-size:18px">클라우드에서 고르는 것: <b>{cl}</b></div></div>''' for i, c, t, d, a, cl in parts)
R("w1d2-computer-parts", f'<div class="row" style="gap:18px">{pc}</div>')

# 2. 메모리 계층 (가로 막대, 로그 스케일 느낌)
lv = [("CPU 캐시 (L1)", "약 1ns", "1초", 4, "teal"), ("메모리 (RAM)", "약 100ns", "약 1.5분", 14, "teal"),
      ("NVMe SSD", "약 10~100µs", "약 3시간~1일", 34, "violet"), ("데이터센터 내 왕복", "약 0.5ms", "약 6일", 48, "violet"),
      ("HDD 탐색", "약 5~10ms", "약 2~4개월", 66, "orange"), ("서울↔미국 서부 왕복", "약 150ms", "약 4~5년", 100, "red")]
rows = "".join(f'''<div class="row c" style="gap:18px"><div style="width:300px;font-size:24px;font-weight:800;color:var(--navy)">{n}</div>
  <div style="flex:1;background:var(--slate-l);border-radius:10px;height:46px;position:relative"><div style="width:{w}%;height:100%;border-radius:10px;background:var(--{c})"></div></div>
  <div style="width:170px;font-size:22px;font-weight:800;color:var(--{c})">{t}</div><div style="width:230px;font-size:21px;color:var(--slate)">{h}</div></div>''' for n, t, h, w, c in lv)
R("w1d2-memory-hierarchy", f'''<div class="row c" style="gap:18px"><div style="width:300px"></div><div style="flex:1" class="tag">멀수록 느리다 (막대 길이는 비교용 개념 척도)</div>
<div style="width:170px" class="tag">지연 시간</div><div style="width:230px" class="tag">1ns를 1초로 늘리면</div></div>
<div class="col" style="gap:14px">{rows}</div><div class="note">※ 하드웨어·측정 방법에 따라 달라지는 대략의 값</div>''')

# 3. OS 층
apps = "".join(f'<div class="box" style="background:#fff;border:2px solid #9fd6df;color:var(--navy);flex:1;font-size:22px">{a}</div>' for a in ["웹 브라우저", "nginx", "Python 앱", "셸 (bash)"])
kern = "".join(f'<div class="box" style="background:rgba(255,255,255,.12);color:#fff;flex:1;font-size:20px;padding:12px 6px">{a}</div>' for a in ["프로세스 관리", "메모리 관리", "파일시스템", "네트워크", "장치 드라이버"])
hw = "".join(f'<div class="col center" style="gap:6px;flex:1">{icon(i,48,"slate",1.8)}<div style="font-size:20px;font-weight:700;color:var(--slate)">{t}</div></div>' for i, t in [("Cpu", "CPU"), ("MemoryStick", "메모리"), ("HardDrive", "디스크"), ("Network", "NIC")])
R("w1d2-os-layers", f'''<div class="row" style="gap:24px;align-items:stretch">
<div class="col grow" style="gap:12px">
 <div class="card fill-teal" style="padding:18px;gap:10px"><div class="tag" style="color:var(--teal-d)">사용자 영역 · USER SPACE</div><div class="row" style="gap:12px">{apps}</div></div>
 <div class="row c" style="gap:12px;justify-content:center">{icon("ArrowDown",34,"orange",2.5)}<div style="font-size:24px;font-weight:800;color:var(--orange)">시스템 콜 — open · read · write · fork · socket</div>{icon("ArrowUp",34,"orange",2.5)}</div>
 <div class="card fill-navy" style="padding:18px;gap:10px"><div class="tag" style="color:#7FD3E0">커널 영역 · KERNEL SPACE (Linux 커널)</div><div class="row" style="gap:10px">{kern}</div></div>
 <div class="card fill-slate" style="padding:18px"><div class="row" style="gap:12px">{hw}</div></div>
</div>
<div class="col" style="width:330px;gap:14px;justify-content:center">
 <div class="card"><h3 style="font-size:25px">사용자 모드</h3><p style="font-size:20px">하드웨어를 직접 만질 수 없음. 버그가 나도 다른 프로그램은 안전</p></div>
 <div class="card fill-orange"><h3 style="font-size:25px">시스템 콜</h3><p style="font-size:20px">커널에 내는 공식 '신청서'. 권한을 확인받는다</p></div>
 <div class="card"><h3 style="font-size:25px">커널 모드</h3><p style="font-size:20px">하드웨어를 직접 다루는 유일한 영역</p></div>
</div></div>''')

# 4. 프로세스와 스레드
def proc(name, pid, threads, col):
    th = "".join(f'<div class="col center" style="gap:4px">{icon("Activity",40,col,2.2)}<div style="font-size:18px;color:var(--slate)">스레드 {k}</div></div>' for k in range(1, threads + 1))
    return f'''<div class="card grow" style="gap:12px;border-color:var(--{col})"><div class="row c" style="justify-content:space-between"><h3 style="font-size:26px">{name}</h3><span class="chip {"teal" if col=="teal" else "orange"}">PID {pid}</span></div>
      <div class="box" style="background:var(--{col}-l);color:var(--navy);font-size:20px">메모리 (코드 · 데이터 · 힙) — 스레드끼리 공유</div>
      <div class="row" style="gap:22px;justify-content:center">{th}</div></div>'''
R("w1d2-process-thread", f'''<div class="row" style="gap:28px;align-items:stretch">{proc("nginx", 1234, 3, "teal")}
 <div class="col center" style="gap:8px;justify-content:center">{icon("ShieldCheck",56,"red",2)}<div style="font-size:20px;font-weight:800;color:var(--red);text-align:center">메모리<br>분리</div></div>
 {proc("python app.py", 5678, 2, "orange")}</div>
<div class="card fill-slate" style="padding:16px 24px"><p style="font-size:22px"><b style="color:var(--navy)">프로세스끼리</b>는 메모리가 분리되어 하나가 죽어도 다른 하나는 무사 · <b style="color:var(--navy)">스레드끼리</b>는 메모리를 공유해 빠르지만 경쟁 상태에 주의</p></div>''')

# 5. 프로세스 생명주기
R("w1d2-process-lifecycle", flow([("Sparkles", "slate", "생성", "New<br>메모리에 올라감"), ("Clock", "violet", "준비", "Ready<br>CPU 차례 대기"),
                                    ("Play", "teal", "실행", "Running<br>CPU에서 실행"), ("Hourglass", "orange", "대기", "Waiting<br>디스크·네트워크 응답 대기"),
                                    ("Flag", "green", "종료", "Terminated<br>종료 코드 남김")]) +
  '<div class="row" style="gap:18px"><div class="card fill-teal grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">스케줄러</b> — 수 밀리초마다 실행할 프로세스를 바꿔(문맥 교환) 동시에 도는 것처럼 보이게 한다</p></div>'
  '<div class="card fill-orange grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">종료 코드</b> — 0 = 성공 · 1 = 실패 · 127 = 명령 없음 · 137 = 강제 종료(OOM 등)</p></div></div>')

# 6. 디렉터리 트리
dirs = [("/etc", "Settings", "orange", "설정 파일"), ("/var/log", "ScrollText", "red", "로그"), ("/home", "House", "teal", "사용자 폴더"),
        ("/usr/bin", "Terminal", "violet", "실행 프로그램"), ("/var/lib", "Database", "green", "프로그램 데이터"), ("/tmp", "Timer", "slate", "임시 파일"), ("/proc", "Activity", "navy", "프로세스 정보")]
dc = "".join(f'''<div class="col center" style="gap:8px;flex:1"><div style="width:4px;height:36px;background:var(--line)"></div>{ic(i,c,76)}
  <div style="font-size:25px;font-weight:900;color:var(--navy);font-family:monospace">{p}</div><div style="font-size:19px;color:var(--slate)">{d}</div></div>''' for p, i, c, d in dirs)
R("w1d2-fs-tree", f'''<div class="col center" style="gap:0"><div class="box" style="background:var(--navy);color:#fff;font-size:34px;font-family:monospace;padding:14px 60px">/ (루트)</div>
<div style="width:88%;height:4px;background:var(--line);margin-top:0"></div><div class="row" style="gap:8px;width:100%">{dc}</div></div>
<div class="row" style="gap:18px"><div class="card fill-orange grow" style="padding:16px 22px"><p style="font-size:22px"><b>"어떻게 설정됐나?"</b> → /etc</p></div><div class="card fill-red grow" style="padding:16px 22px"><p style="font-size:22px"><b>"무슨 일이 있었나?"</b> → /var/log</p></div></div>''')

# 7. 권한
perm = [("-", "slate", "종류", "- 파일 · d 폴더"), ("rwx", "teal", "소유자", "읽기·쓰기·실행<br>4+2+1 = 7"), ("r-x", "violet", "그룹", "읽기·실행<br>4+0+1 = 5"), ("r--", "orange", "그 외", "읽기만<br>4+0+0 = 4")]
pp = "".join(f'''<div class="col center" style="gap:10px;flex:{0.6 if s=="-" else 1}"><div class="box" style="background:var(--{c});color:#fff;font-size:52px;font-family:monospace;padding:12px 26px;letter-spacing:6px">{s}</div>
  <div style="font-size:25px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:20px;color:var(--slate);text-align:center">{d}</div></div>''' for s, c, t, d in perm)
ex = [("755", "실행 스크립트", "teal"), ("644", "일반 설정 파일", "teal"), ("600", "SSH 키 · 비밀 파일", "green"), ("777", "거의 쓰면 안 됨", "red")]
ec = "".join(f'<div class="card center grow" style="padding:16px;gap:4px;border-color:var(--{c})"><div style="font-size:40px;font-weight:900;color:var(--{c});font-family:monospace">{n}</div><p style="font-size:19px">{d}</p></div>' for n, d, c in ex)
R("w1d2-permissions", f'''<div class="row" style="gap:16px;align-items:flex-start">{pp}</div>
<div class="row c" style="gap:10px;justify-content:center"><span class="tag">숫자 표기:  r = 4 · w = 2 · x = 1 을 더한다  →  rwxr-xr-- = 754</span></div>
<div class="row" style="gap:16px">{ec}</div>''')

# 8. 스토리지 3종
st = [("Arch_Amazon-Elastic-Block-Store_64", "블록 스토리지", "EBS", "빈 하드디스크", ["서버 한 대에 연결", "빠름 · DB 디스크", "OS가 파일시스템 생성"], "teal"),
      ("Arch_Amazon-EFS_64", "파일 스토리지", "EFS", "공유 폴더 (NAS)", ["여러 서버가 동시 접근", "폴더·파일 구조", "공유 업로드 폴더"], "violet"),
      ("Arch_Amazon-Simple-Storage-Service_64", "객체 스토리지", "S3", "번호표 보관소", ["사실상 무한 용량", "HTTP 주소로 접근", "사진·백업·로그"], "orange")]
sc = "".join(f'''<div class="card grow" style="gap:12px;border-color:var(--{c})"><div class="row c" style="gap:16px">{aws(a,84)}<div><h3 style="font-size:28px">{t}</h3><div style="font-size:22px;font-weight:800;color:var(--{c})">Amazon {s}</div></div></div>
  <div class="box" style="background:var(--{c}-l);color:var(--navy);font-size:20px;padding:10px">비유: {an}</div>
  <ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>''' for a, t, s, an, li, c in st)
R("w1d2-storage-types", f'<div class="row" style="gap:20px">{sc}</div>')

# 9. 명령어 해부
R("w1d2-terminal-anatomy", f'''<div class="card fill-navy" style="padding:34px 40px;gap:26px">
<div style="font-family:monospace;font-size:38px;color:#E2E8F0;white-space:nowrap"><span style="color:#7FD3E0">student@devbox</span>:<span style="color:#ffd7b0">~/app</span>$ <span style="color:#fff;font-weight:700">ls</span> <span style="color:#C4B5FD">-l</span> <span style="color:#86EFAC">/var/log</span> <span style="color:#FCA5A5">| grep nginx</span></div>
</div>
<div class="row" style="gap:16px">
 <div class="card grow" style="gap:6px"><div style="font-size:24px;font-weight:900;color:var(--teal)">프롬프트</div><p style="font-size:20px">사용자@컴퓨터:현재위치<br><b>$</b> 일반 · <b>#</b> 관리자</p></div>
 <div class="card grow" style="gap:6px"><div style="font-size:24px;font-weight:900;color:var(--navy)">명령</div><p style="font-size:20px">무엇을 할까<br><code>ls</code> = 목록 보기</p></div>
 <div class="card grow" style="gap:6px"><div style="font-size:24px;font-weight:900;color:var(--violet)">옵션</div><p style="font-size:20px">어떻게 할까<br><code>-l</code> = 자세히</p></div>
 <div class="card grow" style="gap:6px"><div style="font-size:24px;font-weight:900;color:var(--green)">인자</div><p style="font-size:20px">무엇에 대해<br><code>/var/log</code></p></div>
 <div class="card grow" style="gap:6px"><div style="font-size:24px;font-weight:900;color:var(--red)">파이프</div><p style="font-size:20px">앞 출력을 뒤 입력으로<br><code>| grep</code> = 걸러내기</p></div>
</div>''')

# 10. 하이퍼바이저 Type1/2
def vmrow(n, col):
    return "".join(f'<div class="col grow" style="gap:6px"><div class="box" style="background:#fff;border:2px solid var(--{col});color:var(--navy);font-size:20px;padding:10px">앱</div><div class="box" style="background:var(--{col}-l);color:var(--navy);font-size:20px;padding:10px">게스트 OS</div></div>' for _ in range(n))
R("w1d2-hypervisor-types", f'''<div class="row" style="gap:34px;align-items:flex-end">
<div class="col grow" style="gap:10px"><div style="font-size:30px;font-weight:900;color:var(--teal);text-align:center">Type 1 · 베어메탈</div>
 <div class="row" style="gap:10px">{vmrow(3,"teal")}</div>
 {layer("하이퍼바이저 (KVM · ESXi · Hyper-V · Nitro)", "var(--teal)", "#fff")}
 {layer("하드웨어", "var(--slate-l)", "var(--slate)")}
 <div class="note center">데이터센터 · 클라우드 — 빠르다</div></div>
<div class="col grow" style="gap:10px"><div style="font-size:30px;font-weight:900;color:var(--orange);text-align:center">Type 2 · 호스티드</div>
 <div class="row" style="gap:10px">{vmrow(2,"orange")}</div>
 {layer("하이퍼바이저 앱 (VirtualBox · Parallels)", "var(--orange)", "#fff")}
 {layer("호스트 OS (Windows · macOS)", "var(--navy)", "#fff")}
 {layer("하드웨어", "var(--slate-l)", "var(--slate)")}
 <div class="note center">개인 PC 실험 — 중간 단계가 하나 더</div></div></div>''')

# 11. VM vs 컨테이너
def vmcol():
    vms = "".join(f'<div class="col grow" style="gap:6px;border:2px dashed var(--teal);border-radius:14px;padding:8px"><div class="box" style="background:#fff;border:2px solid var(--teal);color:var(--navy);font-size:19px;padding:9px">앱 {x}</div><div class="box" style="background:var(--slate-l);color:var(--slate);font-size:18px;padding:9px">라이브러리</div><div class="box" style="background:var(--teal-l);color:var(--navy);font-size:19px;padding:12px">게스트 OS<br>(수 GB)</div></div>' for x in "ABC")
    return f'<div class="row" style="gap:10px">{vms}</div>' + layer("하이퍼바이저", "var(--teal)", "#fff") + layer("하드웨어", "var(--slate-l)", "var(--slate)")
def ctcol():
    cs = "".join(f'<div class="col grow" style="gap:6px;border:2px dashed var(--orange);border-radius:14px;padding:8px"><div class="box" style="background:#fff;border:2px solid var(--orange);color:var(--navy);font-size:19px;padding:9px">앱 {x}</div><div class="box" style="background:var(--slate-l);color:var(--slate);font-size:18px;padding:9px">라이브러리</div></div>' for x in "ABCD")
    return f'<div class="row" style="gap:10px">{cs}</div>' + layer("컨테이너 런타임 (Docker · containerd)", "var(--orange)", "#fff") + layer("호스트 OS 커널 하나를 공유", "var(--navy)", "#fff") + layer("하드웨어 (또는 VM)", "var(--slate-l)", "var(--slate)")
R("w1d2-vm-vs-container", f'''<div class="row" style="gap:34px;align-items:flex-end">
<div class="col grow" style="gap:10px"><div style="font-size:30px;font-weight:900;color:var(--teal);text-align:center">가상 머신 (VM)</div>{vmcol()}<div class="note center">OS째 격리 · 강하지만 무겁다 · 수십 초</div></div>
<div class="col grow" style="gap:10px"><div style="font-size:30px;font-weight:900;color:var(--orange);text-align:center">컨테이너</div>{ctcol()}<div class="note center">프로세스 격리 · 가볍다 · 1초 안팎</div></div></div>''')

# 12. 네임스페이스 + cgroups
ns = [("Hash", "PID", "내 앱 = PID 1"), ("FolderTree", "Mount", "나만의 /"), ("Network", "Network", "나만의 IP·포트"), ("Tag", "UTS", "나만의 호스트 이름"), ("UserRound", "User", "안에선 root")]
nsc = "".join(f'<div class="col center grow" style="gap:6px">{ic(i,"teal",64)}<div style="font-size:22px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:18px;color:var(--slate)">{d}</div></div>' for i, t, d in ns)
cg = [("Cpu", "CPU", "최대 0.5코어"), ("MemoryStick", "메모리", "최대 512MiB"), ("HardDrive", "디스크 I/O", "초당 읽기 한도")]
cgc = "".join(f'<div class="col center grow" style="gap:6px">{ic(i,"orange",64)}<div style="font-size:22px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:18px;color:var(--slate)">{d}</div></div>' for i, t, d in cg)
R("w1d2-namespaces-cgroups", f'''<div class="row" style="gap:22px;align-items:stretch">
<div class="card fill-teal" style="flex:1.6;gap:14px"><div class="row c" style="gap:14px">{ic("EyeOff","teal",70,"#fff")}<div><h3>네임스페이스</h3><p style="font-size:21px">보이는 것을 제한한다</p></div></div><div class="row" style="gap:8px">{nsc}</div></div>
<div class="card fill-orange" style="flex:1;gap:14px"><div class="row c" style="gap:14px">{ic("Gauge","orange",70,"#fff")}<div><h3>cgroups</h3><p style="font-size:21px">쓰는 양을 제한한다</p></div></div><div class="row" style="gap:8px">{cgc}</div></div></div>
<div class="card fill-navy" style="padding:18px 28px"><p style="font-size:23px;color:#fff"><b>컨테이너 = 네임스페이스 + cgroups로 격리된 평범한 프로세스</b> &nbsp;·&nbsp; Kubernetes의 requests/limits는 결국 cgroups 설정이 된다</p></div>''')

# 13. 컨테이너 역사
hist = [("1979", "slate", "chroot", "Unix 루트 디렉터리 격리"), ("2000", "slate", "FreeBSD Jails", "파일·프로세스·네트워크 격리"),
        ("2002~", "violet", "Linux 네임스페이스", "커널에 격리 기능 추가"), ("2008", "violet", "cgroups · LXC", "Linux만으로 컨테이너"),
        ("2013", "teal", "Docker", "이미지·레지스트리로 대중화"), ("2014", "teal", "Kubernetes", "컨테이너 자동 운영"), ("2015", "orange", "OCI", "이미지·런타임 표준")]
hc = "".join(f'''<div class="col center grow" style="gap:10px"><div style="font-size:28px;font-weight:900;color:var(--{c})">{y}</div>
  <div style="width:22px;height:22px;border-radius:50%;background:var(--{c});box-shadow:0 0 0 6px #fff"></div>
  <div class="card center" style="padding:16px 8px;gap:6px;width:100%"><h3 style="font-size:23px">{t}</h3><p style="font-size:18px">{d}</p></div></div>''' for y, c, t, d in hist)
R("w1d2-container-history", f'''<div style="position:relative"><div style="position:absolute;left:5%;right:5%;top:58px;height:4px;background:var(--line)"></div>
<div class="row" style="gap:10px;position:relative">{hc}</div></div>
<div class="card fill-slate" style="padding:16px 24px"><p style="font-size:22px">격리 기술은 Docker 이전에 이미 있었다 — Docker는 그것을 <b style="color:var(--teal-d)">누구나 쓰기 쉽게 포장</b>해서 대중화했다</p></div>''')
