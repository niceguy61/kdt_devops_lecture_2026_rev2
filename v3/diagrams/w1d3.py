"""1주차 3일차 다이어그램. 실행: python3 diagrams/w1d3.py [이름...]"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
from dk import render, ic, icon, aws, arrow  # noqa: E402

OUT = ROOT / "assets" / "week1" / "day3"
only = set(sys.argv[1:])


def R(name, body, **kw):
    if only and name not in only:
        return
    render(OUT / f"{name}.png", body, **kw)
    print("ok", name)


def box(text, bg, fg="var(--navy)", size=22, pad=14, extra=""):
    return f'<div class="box" style="background:{bg};color:{fg};font-size:{size}px;padding:{pad}px;{extra}">{text}</div>'


MONO = "font-family:'D2Coding','Consolas',monospace"

# 1. 택배로 이해하는 캡슐화 — 중첩 상자
R("w1d3-parcel", f'''<div class="row" style="gap:30px;align-items:center">
<div class="grow" style="border:4px solid var(--slate);border-radius:24px;padding:20px;background:var(--slate-l)">
 <div class="row c" style="gap:12px;margin-bottom:12px">{icon("Truck",44,"slate",2)}<div style="font-size:25px;font-weight:800;color:var(--slate)">트럭 · 네트워크 접근 계층 — MAC 주소</div></div>
 <div style="border:4px solid var(--violet);border-radius:20px;padding:18px;background:var(--violet-l)">
  <div class="row c" style="gap:12px;margin-bottom:12px">{icon("Package",42,"violet",2)}<div style="font-size:25px;font-weight:800;color:var(--violet)">상자 · 인터넷 계층 — IP 주소</div></div>
  <div style="border:4px solid var(--orange);border-radius:18px;padding:16px;background:var(--orange-l)">
   <div class="row c" style="gap:12px;margin-bottom:12px">{icon("Mail",40,"orange",2)}<div style="font-size:25px;font-weight:800;color:var(--orange)">봉투 · 전송 계층 — 포트 번호</div></div>
   <div style="border:4px solid var(--teal);border-radius:16px;padding:18px;background:#fff" class="row c">
    {icon("FileText",40,"teal",2)}<div style="font-size:25px;font-weight:800;color:var(--teal-d)">편지 · 응용 계층 — "상품 목록 주세요" (HTTP)</div>
   </div></div></div></div>
<div class="col" style="width:330px;gap:16px">
 <div class="card fill-teal" style="padding:20px"><h3 style="font-size:25px">보낼 때: 캡슐화</h3><p style="font-size:20px">안쪽부터 한 겹씩 포장을 덧씌운다</p></div>
 <div class="card fill-orange" style="padding:20px"><h3 style="font-size:25px">받을 때: 역캡슐화</h3><p style="font-size:20px">바깥부터 한 겹씩 벗긴다</p></div>
 <div class="card" style="padding:20px"><h3 style="font-size:25px">핵심</h3><p style="font-size:20px">각 층은 자기 포장만 본다 — 택배 기사는 편지 내용을 몰라도 된다</p></div>
</div></div>''')

# 2. TCP/IP 4계층 vs OSI 7계층
layers = [("응용", "teal", ["7 응용", "6 표현", "5 세션"], "도메인 · URL", "HTTP · DNS · SSH"),
          ("전송", "orange", ["4 전송"], "포트", "TCP · UDP"),
          ("인터넷", "violet", ["3 네트워크"], "IP 주소", "IP · ICMP"),
          ("네트워크 접근", "slate", ["2 데이터링크", "1 물리"], "MAC 주소", "이더넷 · 와이파이")]
rows = []
for name, c, osi, addr, tech in layers:
    o = "".join(f'<div class="box" style="background:#fff;border:2px solid var(--line);color:var(--slate);font-size:20px;padding:8px">{x}</div>' for x in osi)
    rows.append(f'''<div class="row" style="gap:16px">
 <div class="box" style="width:250px;background:var(--{c});color:#fff;font-size:26px;display:flex;align-items:center;justify-content:center">{name}</div>
 <div class="col" style="width:260px;gap:6px;justify-content:center">{o}</div>
 <div class="box grow" style="background:var(--{c}-l);color:var(--navy);font-size:23px;display:flex;align-items:center;justify-content:center">{addr}</div>
 <div class="box grow" style="background:var(--slate-l);color:var(--slate);font-size:22px;display:flex;align-items:center;justify-content:center">{tech}</div></div>''')
R("w1d3-tcpip-layers", f'''<div class="row" style="gap:16px"><div class="tag" style="width:250px;text-align:center">TCP/IP 4계층 (실제 구현)</div>
<div class="tag" style="width:260px;text-align:center">OSI 7계층 (참조 모델)</div><div class="tag grow" style="text-align:center">주소</div><div class="tag grow" style="text-align:center">대표 기술</div></div>
<div class="col" style="gap:12px">{"".join(rows)}</div>
<div class="row" style="gap:16px"><div class="card fill-orange grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">L4</b> = IP·포트까지 보고 판단 (AWS NLB)</p></div>
<div class="card fill-teal grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">L7</b> = HTTP 내용(경로·헤더)까지 보고 판단 (AWS ALB)</p></div></div>''')

# 3. IP 주소 구조와 CIDR
octs = [("10", "teal"), ("0", "teal"), ("1", "orange"), ("25", "orange")]
ob = '<div style="font-size:60px;font-weight:900;color:var(--slate)">.</div>'.join(
    f'<div class="col center" style="gap:6px"><div class="box" style="background:var(--{c}-l);border:3px solid var(--{c});color:var(--navy);font-size:58px;{MONO};width:170px;padding:12px">{v}</div><div style="font-size:19px;color:var(--slate)">8비트 · 0~255</div></div>'
    for v, c in octs)
cidr = [("/8", "10.x.x.x", "16,777,216", 18), ("/16", "10.0.x.x", "65,536", 48), ("/24", "10.0.1.x", "256", 78), ("/32", "10.0.1.25", "1", 100)]
cr = "".join(f'''<div class="row c" style="gap:16px"><div style="width:90px;font-size:30px;font-weight:900;color:var(--teal-d);{MONO}">{s}</div>
<div style="flex:1;height:38px;background:var(--slate-l);border-radius:10px"><div style="width:{w}%;height:100%;background:var(--teal);border-radius:10px"></div></div>
<div style="width:200px;font-size:22px;{MONO};color:var(--navy)">{r}</div><div style="width:200px;font-size:22px;font-weight:800;color:var(--navy);text-align:right">{n}개</div></div>''' for s, r, n, w in cidr)
R("w1d3-ip-anatomy", f'''<div class="row c" style="gap:10px;justify-content:center">{ob}<div style="font-size:60px;font-weight:900;color:var(--violet);{MONO}">/24</div></div>
<div class="row" style="gap:16px;justify-content:center"><span class="chip teal" style="font-size:21px">네트워크 부분 = 어느 동네</span><span class="chip orange" style="font-size:21px">호스트 부분 = 몇 번지</span>
<span class="chip" style="font-size:21px;background:var(--violet);color:#fff">/24 = 앞 24비트가 네트워크</span></div>
<div class="card" style="padding:22px 26px;gap:12px"><div class="row" style="gap:16px"><div class="tag" style="width:90px">CIDR</div><div class="tag grow">네트워크 부분이 길수록(숫자가 클수록) 동네가 작아진다</div><div class="tag" style="width:200px">범위</div><div class="tag" style="width:200px;text-align:right">주소 개수 2^(32−n)</div></div>{cr}</div>''')

# 4. NAT
devs = "".join(f'<div class="row c" style="gap:12px">{ic(i,"teal",64)}<div><div style="font-size:22px;font-weight:800;color:var(--navy)">{n}</div><div style="font-size:20px;{MONO};color:var(--slate)">{a}</div></div></div>'
               for i, n, a in [("Laptop", "노트북", "192.168.0.15"), ("Smartphone", "휴대폰", "192.168.0.23"), ("Tv", "스마트 TV", "192.168.0.31")])
R("w1d3-nat", f'''<div class="row flow" style="gap:14px">
<div class="card fill-teal" style="width:340px;gap:16px"><div class="tag" style="color:var(--teal-d)">집 안 · 사설 IP</div>{devs}</div>
{arrow(size=40)}
<div class="card center grow" style="gap:12px;justify-content:center">{ic("Router","orange",100)}<h3 style="font-size:28px">공유기 (NAT)</h3>
 <p style="font-size:20px">출발 주소를 공인 IP로 바꾸고<br>누가 보냈는지 표에 기록</p>
 <div class="box" style="background:var(--orange-l);color:var(--navy);font-size:20px;{MONO}">192.168.0.15:50122 ↔ 211.36.x.x:40001</div></div>
{arrow("both", 40)}
<div class="card center" style="width:300px;gap:12px;justify-content:center">{ic("Globe","violet",100)}<h3 style="font-size:28px">인터넷</h3>
 <p style="font-size:20px">상대방에게는<br><b style="color:var(--navy)">공인 IP 하나</b>만 보인다</p></div></div>
<div class="row" style="gap:16px"><div class="card fill-slate grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">비유</b> — 회사 대표 번호(공인 IP)와 내선 번호(사설 IP), 교환기(NAT)</p></div>
<div class="card fill-orange grow" style="padding:16px 22px"><p style="font-size:21px"><b style="color:var(--navy)">AWS</b> — 프라이빗 서브넷의 서버가 밖으로만 나가게 하는 <b>NAT Gateway</b></p></div></div>''')

# 5. VPC 서브넷 설계 (AWS 공식 그룹 스타일)
def subnet(kind, cidr, items):
    col = "#7AA116" if kind == "퍼블릭" else "#00A4A6"
    ico = "Public-subnet_32" if kind == "퍼블릭" else "Private-subnet_32"
    its = "".join(f'<div class="col center" style="gap:6px">{aws(a,58)}<div style="font-size:18px;font-weight:700;color:var(--navy)">{t}</div></div>' for a, t in items)
    return f'''<div style="border:2px solid {col};background:{"#F2F8E6" if kind=="퍼블릭" else "#E6F6F7"};border-radius:6px;padding:12px 14px;display:flex;flex-direction:column;gap:10px">
<div class="row c" style="gap:10px">{aws(ico,34)}<div style="font-size:20px;font-weight:800;color:{col}">{kind} 서브넷 · <span style="{MONO}">{cidr}</span></div></div>
<div class="row" style="gap:26px;justify-content:center">{its}</div></div>'''


def az(name, pub, pri):
    return f'''<div class="grow" style="border:2px dashed var(--aws-az);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:12px">
<div style="font-size:21px;font-weight:800;color:var(--aws-az)">가용 영역 {name}</div>
{subnet("퍼블릭", pub, [("Res_Elastic-Load-Balancing_Application-Load-Balancer_48", "ALB"), ("Res_Amazon-VPC_NAT-Gateway_48", "NAT Gateway")])}
{subnet("프라이빗", pri, [("Arch_Amazon-EC2_48", "앱 서버"), ("Arch_Amazon-RDS_48", "데이터베이스")])}</div>'''


R("w1d3-vpc-subnets", f'''<div class="row" style="gap:16px;align-items:center">
<div class="col center" style="gap:8px;width:150px">{ic("Users","navy",80)}<div style="font-size:21px;font-weight:800;color:var(--navy)">사용자</div></div>
{arrow(size=36)}
<div class="grow" style="border:2px solid #8C4FFF;border-radius:6px;padding:16px;display:flex;flex-direction:column;gap:14px">
 <div class="row c" style="gap:12px">{aws("Virtual-private-cloud-VPC_32",40) if False else aws("Arch_Amazon-Virtual-Private-Cloud_48",40)}<div style="font-size:23px;font-weight:900;color:#8C4FFF">VPC · <span style="{MONO}">10.0.0.0/16</span> (65,536개)</div>
 <div class="grow"></div>{aws("Res_Amazon-VPC_Internet-Gateway_48",44)}<div style="font-size:19px;font-weight:700;color:var(--navy)">인터넷 게이트웨이</div></div>
 <div class="row" style="gap:16px">{az("A", "10.0.1.0/24", "10.0.11.0/24")}{az("C", "10.0.2.0/24", "10.0.12.0/24")}</div>
</div></div>
<div class="note">5주차에 콘솔로 한 번, Terraform 코드로 한 번 직접 만든다 · 각 서브넷 /24 = 256개 (AWS가 5개를 예약해 실제 251개)</div>''')

# 6. IP와 포트 — 건물과 호실
rooms = [("22", "SSH", "Terminal", "slate"), ("80", "HTTP", "Globe", "teal"), ("443", "HTTPS", "Lock", "teal"), ("5432", "PostgreSQL", "Database", "violet"), ("6379", "Redis", "Zap", "orange")]
rm = "".join(f'''<div class="col center grow" style="gap:8px;background:#fff;border:2px solid var(--{c});border-radius:14px;padding:14px 8px">
<div style="font-size:30px;font-weight:900;color:var(--{c});{MONO}">:{p}</div>{icon(i,44,c,2)}<div style="font-size:20px;font-weight:800;color:var(--navy)">{n}</div></div>''' for p, n, i, c in rooms)
R("w1d3-ports", f'''<div class="row" style="gap:24px;align-items:center">
<div class="col center" style="gap:10px;width:230px">{ic("Laptop","navy",90)}<div style="font-size:22px;font-weight:800;color:var(--navy)">클라이언트</div>
 <div class="box" style="background:var(--slate-l);color:var(--navy);font-size:19px;{MONO}">13.125.10.20:443</div><div class="note" style="font-size:18px">주소 + 문 번호</div></div>
{arrow(size=40)}
<div class="grow" style="border:4px solid var(--navy);border-radius:22px;padding:20px;display:flex;flex-direction:column;gap:14px;background:var(--slate-l)">
 <div class="row c" style="gap:12px">{icon("Building2",44,"navy",2)}<div style="font-size:26px;font-weight:900;color:var(--navy)">서버 — IP <span style="{MONO}">13.125.10.20</span> = 건물 주소</div></div>
 <div class="row" style="gap:12px">{rm}</div>
 <div class="box" style="background:var(--navy);color:#fff;font-size:21px">운영체제(경비실)가 포트 번호(호실)를 보고 프로세스에 전달 · 한 포트에는 한 프로세스만</div>
</div></div>''')

# 7. TCP 3-way handshake (시퀀스 다이어그램)
def msg(label, sub, direction, col):
    a = icon("ArrowRight" if direction == "r" else "ArrowLeft", 40, col, 2.5)
    line = f'<div style="flex:1;height:4px;background:var(--{col})"></div>'
    inner = (line + a) if direction == "r" else (a + line)
    return f'''<div class="col" style="gap:6px"><div class="row c" style="gap:0">{inner}</div>
<div class="row c" style="justify-content:center;gap:12px"><span class="chip" style="background:var(--{col});color:#fff;font-size:22px;{MONO}">{label}</span><span style="font-size:21px;color:var(--slate)">{sub}</span></div></div>'''


R("w1d3-handshake", f'''<div class="row" style="gap:0;align-items:stretch">
<div class="col center" style="width:220px;gap:10px">{ic("Laptop","teal",90)}<div style="font-size:24px;font-weight:800;color:var(--navy)">클라이언트</div><div style="flex:1;width:4px;background:var(--line)"></div></div>
<div class="col grow" style="gap:30px;padding:40px 10px 10px">
 {msg("① SYN", "연결하고 싶어요", "r", "teal")}
 {msg("② SYN-ACK", "좋아요, 저도 준비됐어요", "l", "orange")}
 {msg("③ ACK", "확인했어요, 시작합시다", "r", "teal")}
 <div class="box" style="background:var(--green-l);color:var(--green);font-size:22px">연결 완료 → 이제 HTTP 요청 등 데이터 전송</div>
</div>
<div class="col center" style="width:220px;gap:10px">{ic("Server","orange",90)}<div style="font-size:24px;font-weight:800;color:var(--navy)">서버</div><div style="flex:1;width:4px;background:var(--line)"></div></div>
</div>
<div class="card fill-slate" style="padding:16px 24px"><p style="font-size:21px">데이터를 보내기 전에 <b style="color:var(--navy)">최소 왕복 1번</b> — 서울↔미국 서부라면 약 150ms. 그래서 연결을 재사용(keep-alive)한다</p></div>''')

# 8. DNS 조회 과정
servers = [("Server", "slate", "루트 네임서버", '".com은 저기"'), ("Server", "violet", "TLD 네임서버 (.com)", '"example.com은 저기"'), ("ServerCog", "orange", "권한 있는 네임서버", '"93.184.x.x 입니다"')]
sv = "".join(f'''<div class="row c" style="gap:14px"><div class="chip" style="background:var(--{c});color:#fff;font-size:22px">{k+3}</div>
<div class="card grow" style="gap:14px;padding:16px 20px;border-color:var(--{c});flex-direction:row;align-items:center">{ic(i,c,62)}<div><h3 style="font-size:24px">{n}</h3><p style="font-size:19px">{d}</p></div></div></div>''' for k, (i, c, n, d) in enumerate(servers))
R("w1d3-dns-resolution", f'''<div class="row" style="gap:20px;align-items:center">
<div class="col center" style="width:220px;gap:10px">{ic("Laptop","navy",96)}<div style="font-size:23px;font-weight:800;color:var(--navy)">내 컴퓨터</div>
 <div class="box" style="background:var(--slate-l);color:var(--navy);font-size:19px">① 캐시 확인<br><span style="{MONO}">www.example.com?</span></div></div>
<div class="col center" style="gap:4px">{arrow("both",40)}<div style="font-size:19px;font-weight:700;color:var(--slate)">② 질문 / ⑥ 답</div></div>
<div class="col center" style="width:270px;gap:10px">{ic("Search","teal",110)}<div style="font-size:25px;font-weight:800;color:var(--navy)">리졸버</div>
 <div class="note" style="font-size:18px">통신사 DNS 또는<br>8.8.8.8 · 1.1.1.1</div><div class="box" style="background:var(--teal-l);color:var(--teal-d);font-size:19px">답을 TTL 동안 캐시</div></div>
<div class="col center" style="gap:4px">{arrow("both",40)}<div style="font-size:19px;font-weight:700;color:var(--slate)">차례로 묻기</div></div>
<div class="col grow" style="gap:14px">{sv}</div></div>
<div class="note">처음 한 번만 여러 단계를 거치고, 이후에는 곳곳의 캐시에서 바로 답한다</div>''')

# 9. AWS 장애 연쇄
steps = [("Bug", "red", "경쟁 상태", "DNS 관리 자동화에<br>숨은 경쟁 상태"),
         ("FileX", "red", "빈 DNS 레코드", "dynamodb.us-east-1<br>이름 → IP 없음"),
         ("Unplug", "orange", "연결 실패", "서버는 정상이지만<br>찾아갈 수 없음"),
         ("Network", "orange", "연쇄 영향", "DynamoDB에 의존하는<br>내부 시스템까지"),
         ("Globe", "violet", "전 세계 서비스", "약 15시간 동안<br>여러 서비스 영향")]
sc = []
for k, (i, c, t, d) in enumerate(steps):
    sc.append(f'<div class="card center grow" style="gap:10px;border-color:var(--{c})">{ic(i,c,82)}<h3 style="font-size:24px">{t}</h3><p style="font-size:19px">{d}</p></div>')
    if k < len(steps) - 1:
        sc.append(arrow(size=32))
R("w1d3-aws-outage", f'''<div class="row flow" style="gap:8px">{"".join(sc)}</div>
<div class="row" style="gap:14px">
<div class="card fill-red grow" style="padding:16px 20px"><p style="font-size:20px"><b style="color:var(--navy)">It's always DNS</b><br>이름 해석 하나가 모든 것을 멈춘다</p></div>
<div class="card fill-orange grow" style="padding:16px 20px"><p style="font-size:20px"><b style="color:var(--navy)">자동화도 버그가 있다</b><br>테스트와 안전장치가 필요</p></div>
<div class="card fill-violet grow" style="padding:16px 20px"><p style="font-size:20px"><b style="color:var(--navy)">의존성은 보이지 않는다</b><br>단일 장애점(SPOF)</p></div>
<div class="card fill-green grow" style="padding:16px 20px"><p style="font-size:20px"><b style="color:var(--navy)">보고서를 공개한다</b><br>포스트모템 문화</p></div></div>
<div class="note">출처: AWS, Summary of the Amazon DynamoDB Service Disruption in the Northern Virginia (US-EAST-1) Region (2025년 10월)</div>''')

# 10. HTTP 요청·응답 구조
def part(lbl, col, lines):
    ln = "".join(f'<div>{x}</div>' for x in lines)
    return f'''<div class="row" style="gap:0;align-items:stretch"><div style="width:120px;background:var(--{col});color:#fff;font-size:19px;font-weight:800;display:flex;align-items:center;justify-content:center;border-radius:10px 0 0 10px;text-align:center;padding:6px">{lbl}</div>
<div style="flex:1;background:#fff;border:2px solid var(--{col});border-left:none;border-radius:0 10px 10px 0;padding:10px 16px;font-size:21px;{MONO};color:var(--navy);line-height:1.5">{ln}</div></div>'''


req = part("요청 줄", "teal", ["<b>GET</b> /products?category=shoes HTTP/1.1"]) + part("헤더", "violet", ["Host: shop.example.com", "Accept: application/json", "Authorization: Bearer eyJ…"]) + part("본문", "slate", ["(GET은 보통 없음)"])
res = part("상태 줄", "green", ["HTTP/1.1 <b>200 OK</b>"]) + part("헤더", "violet", ["Content-Type: application/json", "Cache-Control: max-age=60"]) + part("본문", "slate", ['[{"id":1,"name":"운동화"}]'])
R("w1d3-http-anatomy", f'''<div class="row flow" style="gap:16px">
<div class="card grow" style="gap:12px;padding:20px"><div class="row c" style="gap:10px">{ic("Laptop","teal",56)}<h3 style="font-size:27px">요청 (Request)</h3></div>{req}</div>
<div class="col center" style="gap:16px;justify-content:center">{arrow(size=40)}{arrow("left",40)}</div>
<div class="card grow" style="gap:12px;padding:20px"><div class="row c" style="gap:10px">{ic("Server","green",56)}<h3 style="font-size:27px">응답 (Response)</h3></div>{res}</div></div>
<div class="row" style="gap:12px;justify-content:center">
<span class="chip teal" style="font-size:20px">2xx 성공</span><span class="chip" style="font-size:20px;background:var(--violet);color:#fff">3xx 이동</span>
<span class="chip orange" style="font-size:20px">4xx 요청 쪽 문제</span><span class="chip" style="font-size:20px;background:var(--red);color:#fff">5xx 서버 쪽 문제</span></div>''')

# 11. TLS가 지키는 세 가지
tl = [("EyeOff", "teal", "기밀성", "내용을 남이 읽을 수 없다", "카페 와이파이에서<br>비밀번호 유출 방지"),
      ("ShieldCheck", "orange", "무결성", "중간에 내용을 바꿀 수 없다", "다운로드 파일에<br>악성코드 끼워 넣기 방지"),
      ("BadgeCheck", "violet", "인증", "대화 상대가 진짜 그 서버다", "가짜 은행 사이트로<br>유도 방지")]
tc = "".join(f'''<div class="card center grow" style="gap:10px;border-color:var(--{c})">{ic(i,c,96)}<h3 style="font-size:29px">{t}</h3><p style="font-size:21px;font-weight:700;color:var(--navy)">{d}</p>
<div class="box" style="background:var(--{c}-l);color:var(--slate);font-size:19px;width:100%">{e}</div></div>''' for i, c, t, d, e in tl)
R("w1d3-tls", f'''<div class="row c" style="gap:16px;justify-content:center">
 <div class="box" style="background:var(--slate-l);color:var(--slate);font-size:22px">HTTP = 내용이 보이는 엽서</div>{arrow(size=36)}
 <div class="box" style="background:var(--navy);color:#fff;font-size:22px">{icon("Lock",26,"orange",2.5)} HTTPS = HTTP + TLS 암호화 봉투</div></div>
<div class="row" style="gap:18px">{tc}</div>
<div class="card fill-slate" style="padding:16px 24px;gap:16px;flex-direction:row;align-items:center">{icon("IdCard",44,"navy",2)}<p style="font-size:21px"><b style="color:var(--navy)">인증서</b> = 인증기관(CA)이 서명한 서버의 디지털 신분증 · 만료되면 브라우저가 경고를 띄운다</p></div>''')

# 13. 요청의 여정 — 아키텍처
def node(a, t, sub, num, kind="aws"):
    img = aws(a, 70) if kind == "aws" else ic(a, "navy", 70)
    return f'''<div class="col center" style="gap:6px;width:150px"><div class="chip navy" style="font-size:18px">{num}</div>{img}<div style="font-size:20px;font-weight:800;color:var(--navy)">{t}</div><div style="font-size:16px;color:var(--slate)">{sub}</div></div>'''


R("w1d3-request-journey", f'''<div class="row c" style="gap:6px;justify-content:space-between">
{node("Smartphone","사용자","브라우저·앱","시작","lucide")}{arrow(size=30)}
{node("Arch_Amazon-Route-53_48","DNS","이름 → IP","①")}{arrow(size=30)}
<div class="col center" style="gap:4px"><div class="box" style="background:var(--slate-l);color:var(--navy);font-size:17px;padding:8px 10px">② TCP<br>③ TLS</div></div>{arrow(size=30)}
{node("Arch_Amazon-CloudFront_48","CDN","정적 파일","④")}{arrow(size=30)}
{node("Res_Elastic-Load-Balancing_Application-Load-Balancer_48","로드밸런서","건강한 서버 선택","⑤")}{arrow(size=30)}
{node("Arch_Amazon-EC2_48","앱 서버","로직 실행","⑥")}{arrow(size=30)}
<div class="col" style="gap:14px">{node("Arch_Amazon-ElastiCache_48","캐시","먼저 확인","⑦")}{node("Arch_Amazon-RDS_48","DB","없으면 조회","⑧")}</div>
</div>
<div class="box" style="background:var(--green-l);color:var(--green);font-size:21px">⑨ 응답은 같은 길을 거꾸로 — <span style="{MONO}">200 OK</span> + JSON</div>
<div class="row" style="gap:12px">
<div class="card fill-teal grow" style="padding:14px 18px"><p style="font-size:19px"><b style="color:var(--navy)">1주차 오늘</b> ①~③ 네트워크</p></div>
<div class="card fill-orange grow" style="padding:14px 18px"><p style="font-size:19px"><b style="color:var(--navy)">4일차·3주차</b> ⑥~⑧ 앱 구조·MSA</p></div>
<div class="card fill-violet grow" style="padding:14px 18px"><p style="font-size:19px"><b style="color:var(--navy)">4주차</b> ⑤ Gateway API</p></div>
<div class="card fill-slate grow" style="padding:14px 18px"><p style="font-size:19px"><b style="color:var(--navy)">5주차</b> 전체를 AWS로</p></div></div>''')

# 14. 네트워크 장비와 AWS/K8s 대응
dv = [("Route", "slate", "라우터", "다른 네트워크로 길 안내", "Res_Amazon-Route-53_Route-Table_48", "라우트 테이블·IGW", "CNI"),
      ("ShieldCheck", "red", "방화벽 (상태 있음)", "허용한 요청의 응답은 자동 통과", None, "보안 그룹", "NetworkPolicy"),
      ("ListChecks", "orange", "방화벽 (상태 없음)", "들어오고 나가는 것을 따로 검사", "Res_Amazon-VPC_Network-Access-Control-List_48", "네트워크 ACL", "—"),
      ("ArrowRightLeft", "violet", "NAT", "사설 IP → 공인 IP", "Res_Amazon-VPC_NAT-Gateway_48", "NAT Gateway", "—"),
      ("Split", "teal", "L7 로드밸런서·리버스 프록시", "경로·헤더 보고 나눠 주기", "Res_Elastic-Load-Balancing_Application-Load-Balancer_48", "ALB", "Gateway API")]
hdr = '<div class="row" style="gap:14px"><div class="tag" style="width:420px">일반 개념</div><div class="tag grow">하는 일</div><div class="tag" style="width:290px">AWS</div><div class="tag" style="width:200px">Kubernetes</div></div>'
dr = "".join(f'''<div class="row c" style="gap:14px;background:#fff;border:2px solid var(--line);border-radius:14px;padding:10px 14px">
<div class="row c" style="width:406px;gap:12px">{ic(i,c,54)}<div style="font-size:22px;font-weight:800;color:var(--navy)">{n}</div></div>
<div class="grow" style="font-size:20px;color:var(--slate)">{d}</div>
<div class="row c" style="width:290px;gap:10px">{aws(a,44) if a else icon("Shield",40,"red",2)}<div style="font-size:20px;font-weight:800;color:var(--orange)">{w}</div></div>
<div style="width:200px;font-size:20px;font-weight:800;color:var(--teal-d)">{k}</div></div>''' for i, c, n, d, a, w, k in dv)
R("w1d3-network-devices", f'''{hdr}<div class="col" style="gap:10px">{dr}</div>''')


# 12. 인증서 수명 차트
def cert_chart():
    if only and "w1d3-cert-lifetime" not in only:
        return
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    for f in (Path.home() / ".fonts").glob("Pretendard-*.otf"):
        fm.fontManager.addfont(str(f))
    plt.rcParams["font.family"] = "Pretendard"
    names = ["2026.3.15 이전", "2026.3.15~", "2027.3.15~", "2029.3.15~"]
    vals = [398, 200, 100, 47]
    cols = ["#CBD5E1", "#0089A0", "#0089A0", "#C8651B"]
    fig, ax = plt.subplots(figsize=(12, 4.4), dpi=220)
    x = range(len(names))
    bars = ax.bar(x, vals, color=cols, width=0.56)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 8, f"{v}일", ha="center", fontsize=17, fontweight="bold", color="#1E293B")
    ax.set_xticks(list(x)); ax.set_xticklabels(names, fontsize=15, color="#1E293B")
    ax.set_ylim(0, 450); ax.set_yticks([])
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color("#CBD5E1")
    ax.text(3.3, 330, "사람이 손으로 갱신하기엔\n너무 짧다 → 자동화 필수", ha="right", fontsize=15, color="#C8651B", fontweight="bold")
    fig.text(0.01, 0.01, "출처: CA/Browser Forum Ballot SC-081v3 (2025년 4월 통과) · 공개 TLS 인증서 최대 유효 기간", fontsize=11, color="#94A3B8")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "w1d3-cert-lifetime.png", facecolor="white"); plt.close(fig)
    print("ok w1d3-cert-lifetime")


cert_chart()
