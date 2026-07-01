# 3교시: EC2 웹 서버 실행

![EC2 user data web server flow](./assets/lesson-03-ec2-user-data-web.png)

## 수업 목표
- user data로 EC2 bootstrap을 재현 가능한 형태로 만든다.
- browser와 `curl`로 HTTP 응답을 확인한다.
- user data 실패 시 system log와 instance 상태를 확인한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| User Data | 최초 부팅 시 설정을 자동 실행해 재현성을 높인다 | 서버마다 손작업이 달라진다 | Advanced details, system log |
| Listen port | app이 실제로 어느 port에서 응답하는지 알아야 한다 | SG는 열렸는데 응답이 없다 | HTTP 80, process |
| HTTP evidence | "됐다"는 말보다 status/body를 남겨야 한다 | 장애 재현과 비교가 안 된다 | browser, curl |

## User data 예시
AMI에 따라 package manager와 service name이 다르다. Amazon Linux 계열을 기준으로 단순 HTTP 응답을 만들 때는 다음 형태를 사용할 수 있다.

```bash
#!/bin/bash
dnf update -y
dnf install -y httpd
systemctl enable --now httpd
cat > /var/www/html/index.html <<'EOF'
<h1>paperclip w5d2 ec2 web</h1>
<p>hello from EC2 user data</p>
EOF
```

Ubuntu 계열을 선택했다면 `apt`와 `apache2` 기준으로 달라진다. 수업에서는 AMI와 명령을 맞추는 것을 중요하게 본다.

## 확인 순서
```text
EC2 state = running
Status checks = passed
Public IPv4 exists
Security Group allows TCP 80
Browser/curl returns HTTP response
```

```bash
curl -i http://<EC2_PUBLIC_IP>/
```

기대 결과는 `HTTP/1.1 200 OK` 또는 브라우저에서 index page가 보이는 것이다.

## 실패 증상별 첫 확인
| 증상 | 첫 확인 |
|---|---|
| timeout | public IP, route table, SG inbound 80 |
| connection refused | web server process/listen port |
| 403/404 | document root, index file |
| SSH는 되는데 HTTP 안 됨 | SG 80, web server |
| user data가 안 된 것 같음 | system log, cloud-init log |

## 직접 설치 경로
user data가 실패하면 SSH 또는 EC2 Instance Connect로 접속해 같은 작업을 직접 수행할 수 있다. 다만 직접 고친 내용은 재현성이 떨어진다. 수업 evidence에는 "user data 실패 -> system log 확인 -> 직접 설치로 임시 복구"처럼 경로를 남긴다.

## Evidence Note
```markdown
# W5D2S3 EC2 web
- EC2 public IP:
- User data 사용 여부:
- Web server package:
- SG inbound 80:
- curl result:
- 실패 시 첫 확인:
```

## 혼자 다시 따라오기
- 최소 재현 경로: EC2 public IP로 `curl -i`를 실행하고 status/body를 기록한다.
- 공식 문서 키워드: `EC2 user data`, `system log`, `EC2 status checks`.
- 스스로 확인할 화면: EC2 instance details, Connect tab, System log, Security tab.
- 흔한 실패 3개: AMI와 package manager가 다름, SG 80을 열지 않음, public IP를 확인하지 않음.
- 다음 준비 상태: EC2 직접 접속과 HTTP 응답 확인을 분리해서 설명할 수 있어야 한다.

## 한 줄 요약
```text
EC2 웹 서버 실습의 성공 증거는 instance running이 아니라 HTTP response다.
```
