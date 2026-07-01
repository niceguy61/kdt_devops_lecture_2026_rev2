# 4교시: Security Group 장애 분석

![Security Group failure drill](./assets/lesson-04-security-group-debug.png)

## 수업 목표
- Security Group rule 변경으로 의도적 접속 실패를 만들고 복구한다.
- SSH 22와 HTTP 80의 source CIDR 위험을 구분한다.
- wrong rule, wrong port, wrong source를 evidence로 분석한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Inbound rule | 외부에서 resource로 들어오는 traffic gate다 | app 장애로 오진한다 | SG inbound tab |
| Source CIDR | 누가 들어올 수 있는지 정한다 | SSH가 전체 공개된다 | 내 IP, `0.0.0.0/0` |
| Port mismatch | app listen port와 SG port가 맞아야 한다 | SG를 열어도 응답이 없다 | port 80/8080 |
| Recheck | rule 수정 후 같은 명령으로 다시 확인해야 한다 | 고쳤는지 증명하지 못한다 | curl/ssh retry |

## 장애 주입 1: HTTP 80 닫기
1. EC2 Security Group inbound rule에서 TCP 80을 제거한다.
2. 브라우저 또는 `curl`로 다시 접속한다.
3. timeout 또는 접속 실패를 기록한다.
4. TCP 80 rule을 복구한다.
5. 같은 `curl` 명령으로 다시 확인한다.

```bash
curl -m 5 -i http://<EC2_PUBLIC_IP>/
```

## 장애 주입 2: source 잘못 지정
HTTP 80 source를 현재 내 IP가 아닌 다른 CIDR로 제한하면 외부에서 접속이 실패한다. 이때 instance와 web server는 정상일 수 있다.

| 원인 | 증거 |
|---|---|
| app process down | EC2 접속 후 process/service 상태 불량 |
| SG 80 closed | TCP timeout, inbound rule 없음 |
| wrong source | rule은 있으나 source가 내 IP와 다름 |
| wrong port | app은 8080, SG는 80 또는 반대 |

## SSH 22 주의
SSH 22를 `0.0.0.0/0`으로 오래 열어두지 않는다. 교육장/개인 IP가 자주 바뀌는 경우에는 일시적으로 열 수 있지만, evidence에 사유와 종료 시각을 남긴다.

| Rule | 수업 판단 |
|---|---|
| TCP 22 from my IP | 권장 |
| TCP 22 from `0.0.0.0/0` | 임시 예외, 종료 전 삭제 |
| TCP 80 from `0.0.0.0/0` | public web 확인 목적 가능 |
| DB port from `0.0.0.0/0` | 금지에 가깝게 다룸 |


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | SG rule 구조 복기 | protocol/port/source |
| 10~20분 | HTTP 80 제거로 장애 주입 | curl timeout |
| 20~30분 | rule 복구와 recheck | curl success |
| 30~40분 | source CIDR 변경 실험 | my IP mismatch |
| 40~50분 | 위험 rule 정리 | SG audit note |

## 왜 일부러 고장내는가
운영자는 정상 화면만 보고 성장하지 않는다. 일부러 80을 닫고, source를 틀리고, port를 바꾸어 보면 증상이 어떻게 달라지는지 몸으로 익힌다. 이 경험이 있어야 실제 장애에서 app code와 cloud network 문제를 분리할 수 있다.

## SG 변경 시 주의
Security Group rule 변경은 즉시 반영될 수 있다. 같은 instance를 여러 학생이 공유하면 한 명의 rule 변경이 다른 사람 실습에 영향을 준다. 개인 계정/개인 SG를 쓰는 이유는 이 영향 범위를 줄이기 위해서다.

## Recheck 원칙
복구했다면 반드시 실패를 확인했던 같은 명령으로 다시 확인한다. 브라우저 새로고침만으로는 DNS/cache/redirect 때문에 판단이 흐릴 수 있다. `curl -m 5 -i` 같은 명령을 고정하면 전후 비교가 쉽다.

## 운영 판단 표
| 바꿀 rule | 수업 중 허용 | 종료 후 상태 |
|---|---|---|
| TCP 22 from my IP | 가능 | 필요 없으면 삭제 |
| TCP 22 from public | 피함 | 반드시 삭제 |
| TCP 80 from public | HTTP 실습 중 가능 | EC2/ALB 삭제 또는 rule 삭제 |
| DB port from public | 사용하지 않음 | 없어야 함 |

## 강사 보강 노트
이 교시는 `SG 장애 드릴`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| 브라우저 증상만 보고 판단함 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| source CIDR을 보지 않고 port만 봄 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| 복구 후 recheck를 생략함 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

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
| 화면 캡처 | before/after inbound rule | 성공 toast만 보이는 캡처 |
| 설정 기록 | curl 실패 출력 | "기본값 사용"이라고만 적음 |
| 운영 판단 | curl 복구 출력 | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D2S4 SG failure drill
- 실패 주입:
- 실패 증상:
- SG rule before:
- SG rule after:
- 같은 명령으로 recheck:
- 보안상 위험했던 rule:
```

## 혼자 다시 따라오기
- 최소 재현 경로: TCP 80 inbound rule을 제거하고 `curl -m 5` 실패를 확인한 뒤 복구한다.
- 공식 문서 키워드: `EC2 security groups`, `inbound rules`, `outbound rules`, `virtual firewall`.
- 스스로 확인할 화면: EC2 Security tab, Security Groups inbound rules.
- 흔한 실패 3개: outbound만 보고 inbound를 안 봄, source CIDR을 안 봄, rule 수정 후 같은 명령으로 재확인하지 않음.
- 다음 준비 상태: "timeout이면 app log보다 SG/route/public IP를 먼저 본다"는 판단을 설명할 수 있어야 한다.

## 한 줄 요약
```text
Security Group 장애 분석은 port, source, direction, recheck를 한 세트로 본다.
```
