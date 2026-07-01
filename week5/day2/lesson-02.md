# 2교시: EC2 Console 실습

![EC2 launch checklist](./assets/lesson-02-ec2-launch-checklist.png)

## 수업 목표
- EC2 launch 화면의 주요 설정을 운영 기준으로 읽는다.
- key pair, subnet, public IP, Security Group, storage, tag를 생성 전 확인한다.
- EC2 Instance Connect와 SSH client 접속 조건을 구분한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Launch checklist | EC2는 클릭 한 번이 아니라 여러 운영 선택의 묶음이다 | 잘못된 subnet/SG/type으로 비용과 접속 문제가 생긴다 | launch summary |
| Key pair | Linux instance 접속 identity material이다 | private key 분실 또는 노출 | key pair name, local file |
| Public IP | internet 직접 접속 조건이다 | instance running인데 외부 접속이 안 된다 | network settings |
| Tag | owner와 cleanup 추적 기준이다 | 실습 resource가 남는다 | Tags tab |

## EC2 launch 순서
Console에서 EC2를 만들 때는 다음 순서로 읽는다.

| 단계 | 확인 |
|---|---|
| Name and tags | `Course=paperclip`, `Week=5`, `Day=2`, `Owner=<id>` |
| AMI | 수업 OS와 명령이 맞는지 |
| Instance type | 비용 통제 가능한 작은 type |
| Key pair | 새로 만들면 안전하게 보관, 기존 key 재사용 시 소유 확인 |
| Network settings | VPC, public subnet, auto-assign public IP |
| Security Group | SSH/HTTP inbound 최소 허용 |
| Storage | root volume size와 delete on termination |
| Advanced details | user data 사용 여부 |

## 접속 방식
AWS 공식 문서 기준으로 EC2 key pair는 public/private key 기반 credential이다. Linux instance에서는 private key로 SSH 접속을 증명한다. EC2 Instance Connect를 사용할 수 있으면 browser 기반 접속도 가능하다.

| 방식 | 장점 | 확인할 것 |
|---|---|---|
| EC2 Instance Connect | browser에서 빠르게 접속 가능 | instance OS/Region/subnet/public IP/SG 조건 |
| SSH client | 현업 환경과 유사 | private key 권한, username, local network |
| Session Manager | 운영 친화적 | SSM agent, IAM role, VPC endpoint 또는 internet route |

Day2는 EC2 Instance Connect 또는 SSH 중 가능한 방식으로 접속한다. 둘 다 실패하면 먼저 Security Group과 public IP를 확인한다.

## Security Group 최소 예시
| 목적 | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | 내 IP 또는 교육장 CIDR |
| HTTP | TCP | 80 | 수업 중 임시 `0.0.0.0/0` 가능, 종료 전 삭제 |

`0.0.0.0/0`은 모든 IPv4 source를 뜻한다. SSH 22를 전체 공개로 오래 유지하지 않는다.


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | launch checklist 읽기 | AMI/type/key |
| 10~20분 | network settings 결정 | VPC/subnet/public IP |
| 20~30분 | SG 최소 rule 만들기 | 22/80 inbound |
| 30~40분 | tag/storage/user data 확인 | launch summary |
| 40~50분 | 생성 후 상태 확인 | instance state/status check |

## 생성 전 멈춤 지점
EC2 launch 화면의 마지막 버튼을 누르기 전에 반드시 summary를 읽는다. 실무에서도 배포 전 review 단계가 있는 이유와 같다. AMI, type, subnet, public IP, SG, storage, tag 중 하나라도 설명하지 못하면 아직 launch할 준비가 되지 않은 것이다.

## Key pair 운영 주의
private key는 다시 다운로드할 수 없다. 잃어버리면 해당 방식으로 접속하기 어렵고, 공개 repository에 올라가면 credential 사고가 된다. Windows/macOS/Linux별 파일 권한 처리도 다르므로, 수업에서는 key 파일 위치를 배움일기에 기록하되 파일 내용은 절대 붙이지 않는다.

## 접속 실패 판단
| 실패 지점 | 증상 | 확인 |
|---|---|---|
| key 문제 | permission denied | username/key pair |
| SG 22 닫힘 | SSH timeout | inbound 22 source |
| public IP 없음 | 외부 접속 불가 | instance networking |
| Instance Connect 불가 | Connect 버튼 실패 | supported OS, network |

## 비용 판단
Instance type은 성능 선택이면서 비용 선택이다. 수업에서는 성능보다 비용 통제를 우선한다. 큰 instance를 쓰면 실습은 빨라질 수 있지만 학생에게 잘못된 기본값을 심어줄 수 있다.

## 강사 보강 노트
이 교시는 `EC2 launch 판단`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| 프리티어만 보고 architecture를 안 봄 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| Key Pair를 잃어버려도 괜찮다고 생각함 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| SG를 default로 두고 넘어감 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

## 실습 중 멈춤 포인트
- 첫 번째 멈춤: 학생이 resource를 생성하기 전에 이름, Region, tag, 예상 비용 발생 지점을 말하게 한다.
- 두 번째 멈춤: 성공 화면이 나온 직후 resource ID와 상태값을 evidence note에 적게 한다.
- 세 번째 멈춤: 실패나 지연이 생기면 새로 클릭하기 전에 이전 단계의 화면과 명령을 다시 보게 한다.
- 네 번째 멈춤: 정리 단계에서 "삭제했다"가 아니라 "검색해도 남아 있지 않다"를 확인하게 한다.

## 확인 질문
1. 오늘 만든 resource가 어느 Region과 어느 계정 경계에 있는가?
2. 이 resource가 비용을 만들기 시작하는 시점은 언제인가?
3. 접속이 실패하면 app, network, permission 중 무엇을 먼저 확인할 것인가?
4. 수업이 끝난 뒤 남겨도 되는 resource와 지워야 하는 resource는 무엇인가?

## 제출 evidence 기준
| evidence | 좋은 예 | 부족한 예 |
|---|---|---|
| 화면 캡처 | AMI 이름 | 성공 toast만 보이는 캡처 |
| 설정 기록 | instance type | "기본값 사용"이라고만 적음 |
| 운영 판단 | key pair 사용 여부 | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D2S2 EC2 launch
- Instance name:
- AMI:
- Instance type:
- Key pair:
- VPC/subnet:
- Public IP auto-assign:
- Security Group inbound:
- Tags:
- Storage:
```

## 혼자 다시 따라오기
- 최소 재현 경로: EC2 launch 화면에서 summary까지 값을 채운 뒤, 실제 launch 전 모든 항목을 소리 내어 설명한다.
- 공식 문서 키워드: `EC2 key pairs`, `EC2 Instance Connect`, `launch instance`, `security groups`.
- 스스로 확인할 화면: EC2 launch summary, Instances list, Security tab.
- 흔한 실패 3개: key pair 파일을 잃음, public IP를 끔, default SG에 의존함.
- 다음 준비 상태: launch summary를 보고 비용/접속/cleanup 위험을 설명할 수 있어야 한다.

## 한 줄 요약
```text
EC2 launch는 AMI/type/key/network/SG/storage/tag를 한 번에 결정하는 운영 선택이다.
```
