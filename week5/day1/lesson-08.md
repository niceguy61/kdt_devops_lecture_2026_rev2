# 8교시: 구름 EXP 배움일기

## 수업 목표
- 오늘 배운 AWS 계정 안전장치와 운영 좌표계를 스스로 정리한다.
- 다음 수업 EC2/ALB 실습 전에 필요한 질문을 남긴다.
- 생성한 resource가 있다면 cleanup 상태를 확인한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| 계정 안전 checklist | AWS 실습의 시작 조건이다 | 비용/권한 사고가 먼저 난다 | MFA, Budget, IAM |
| Region 고정 | resource 위치와 비용 분석의 기준이다 | resource를 못 찾는다 | `ap-northeast-2` selector |
| AWS service map | 다음 4일 수업의 공통 지도다 | EC2/S3/VPC/IAM을 따로 외운다 | mapping table |
| Cleanup mindset | cloud resource는 잔여 비용을 남길 수 있다 | 수업 후 비용이 계속 발생한다 | resource list, Billing |

## 오늘 정리할 내용
구름 EXP 배움일기는 긴 블로그가 아니어도 된다. 다만 오늘은 AWS 첫날이므로 다음 항목은 꼭 남긴다.

```markdown
# W5D1 AWS account safety and operating map

## 1. 오늘 사용한 계정/Region
- Account ID:
- Region:
- 실습 identity:

## 2. 계정 안전장치
- root MFA:
- Budget/비용 알림:
- access key 생성 여부:
- 공통 tag:

## 3. Kubernetes에서 AWS로 연결된 개념
| Kubernetes | AWS에서 이어지는 질문 |
|---|---|
| Node |  |
| Service/Ingress |  |
| Secret |  |
| PV/PVC |  |
| logs/metrics/events |  |

## 4. 오늘 가장 헷갈린 AWS 용어 3개
- 
- 
- 

## 5. 다음 수업 전 질문
- 
- 
```

## Cleanup 확인
오늘 실제 resource를 만들었다면 다음을 확인한다.

| resource | 종료 전 상태 |
|---|---|
| EC2 instance | stopped 또는 terminated 여부, EBS 잔여 확인 |
| S3 bucket | object 삭제 여부, public access block 상태 |
| IAM access key | 새로 만들었다면 삭제 또는 비활성화 |
| Budget | 알림 이메일 확인 |
| Region | 다른 Region에 resource가 생기지 않았는지 확인 |

오늘 resource를 만들지 않았다면 "생성 없음"이라고 남긴다. cloud 수업에서는 아무것도 만들지 않은 것도 좋은 evidence가 될 수 있다. 중요한 것은 현재 상태를 설명할 수 있는가다.

## 다음 수업 준비
Day2는 EC2와 ALB를 더 구체적으로 다룬다. 다음 수업 전에 아래 질문을 답할 수 있으면 좋다.

| 질문 | 내 답 |
|---|---|
| EC2 접속은 SSH로 할 것인가, browser-based connect로 할 것인가 |  |
| 내 PC에서 `.pem` key file을 안전하게 보관할 수 있는가 |  |
| HTTP 80을 열 때 source를 어떻게 제한할 것인가 |  |
| 실습이 끝난 뒤 stop과 terminate 중 무엇을 할 것인가 |  |
| ALB가 비용을 만들 수 있다는 점을 알고 있는가 |  |

## 혼자 다시 따라오기
- 최소 재현 경로: lesson 02의 계정 안전 checklist와 lesson 03의 Region note를 먼저 채운다.
- 공식 문서 키워드: `root user best practices`, `AWS Budgets`, `Regions and Availability Zones`, `Security Groups`, `S3 Block Public Access`.
- 스스로 확인할 화면: IAM, Billing, VPC, EC2 launch preview, S3 bucket create preview.
- 흔한 실패 3개: 배움일기에 계정/Region을 안 남김, cleanup 상태를 추측으로 적음, 다음 수업 질문을 남기지 않음.
- 다음 준비 상태: Day2에서 EC2/ALB를 만들기 전에 비용과 삭제 기준을 말할 수 있어야 한다.

## 한 줄 요약
```text
오늘의 산출물은 AWS resource가 아니라 AWS resource를 안전하게 만들기 위한 운영 지도다.
```
