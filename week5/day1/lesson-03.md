# 3교시: Region/AZ와 장애 경계

![AWS Region and Availability Zone map](./assets/lesson-03-region-az.png)

## 수업 목표
- Region과 Availability Zone을 위치, 장애 경계, latency 관점으로 구분한다.
- 서울 리전 `ap-northeast-2`를 실습 기본값으로 고정한다.
- resource를 못 찾는 문제의 첫 확인 지점이 Region임을 이해한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Region | AWS resource가 생성되는 지리적/운영 경계다 | 다른 Region에서 resource를 찾으며 시간을 낭비한다 | Console Region selector |
| Availability Zone | Region 안의 격리된 location이다 | 단일 AZ 장애와 multi-AZ 구성을 구분하지 못한다 | subnet AZ, EC2 placement |
| Service availability | 모든 service와 feature가 모든 Region에서 같지 않을 수 있다 | 문서와 Console 화면이 달라 보인다 | service Region support |
| Cost and latency | 가까운 Region이 latency에 유리할 수 있지만 비용과 지원 기능도 봐야 한다 | 무조건 한 Region만 고집한다 | pricing, latency, compliance |

## Region
AWS Region은 독립된 지리적 영역이다. Console 오른쪽 위 Region selector에서 현재 작업 Region을 확인한다. EC2, VPC, ALB, RDS 같은 많은 resource는 Region 단위로 생성된다.

```text
ap-northeast-2 = Asia Pacific (Seoul)
```

오늘 수업에서는 혼선을 줄이기 위해 기본 Region을 `ap-northeast-2`로 둔다. 다른 Region을 써야 하는 경우 evidence note에 반드시 남긴다.

## Availability Zone
Availability Zone은 Region 안의 격리된 location이다. AWS 공식 문서 기준으로 AZ는 Region 내부의 isolated location이다. 고가용성 설계에서는 여러 AZ에 resource를 분산한다.

```mermaid
flowchart TB
  R["Region: ap-northeast-2"]
  R --> A["AZ A: subnet-a"]
  R --> B["AZ B: subnet-b"]
  R --> C["AZ C: subnet-c"]
  A --> EC2A["EC2"]
  B --> EC2B["EC2"]
  C --> RDS["RDS standby or subnet option"]
```

## Kubernetes와 연결
Kubernetes에서 Pod가 어느 node에 배치되는지가 중요했듯, AWS에서는 instance와 subnet이 어느 AZ에 있는지가 중요하다.

| Kubernetes | AWS |
|---|---|
| node | EC2 instance 또는 managed node |
| node zone label | Availability Zone |
| Service endpoint | ALB target 또는 service endpoint |
| PV/PVC zonal disk | EBS volume과 AZ 제약 |
| multi-replica | multi-AZ 배치 |

## Region을 잘못 보면 생기는 증상
| 증상 | 첫 확인 |
|---|---|
| 방금 만든 EC2가 안 보인다 | Console Region selector |
| S3 bucket 이름이 중복된다고 나온다 | S3 bucket name은 전역 unique |
| VPC가 다르게 보인다 | Region별 VPC list |
| ALB target이 등록되지 않는다 | target과 ALB의 VPC/Region |
| 비용은 있는데 resource를 못 찾는다 | Cost Explorer service/Region filter |


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | Region과 AZ 정의 | 공식 용어 note |
| 10~20분 | Console Region 변경 실험 | resource list 변화 |
| 20~30분 | subnet과 AZ 연결 | subnet AZ column |
| 30~40분 | failure boundary 시나리오 | 단일 AZ vs multi-AZ 표 |
| 40~50분 | 실습 Region 고정 | `ap-northeast-2` evidence |

## Region 선택 의사결정
| 기준 | 질문 | 예시 판단 |
|---|---|---|
| latency | 사용자가 어디에 있는가 | 국내 교육/서비스면 서울 Region 우선 |
| service availability | 필요한 service가 지원되는가 | 새 기능은 일부 Region만 지원 가능 |
| cost | 같은 resource라도 가격이 다른가 | 장기 운영 전 pricing 확인 |
| compliance | 데이터 위치 요구가 있는가 | 고객/기관 요구 확인 |
| failure design | 어느 범위 장애를 견딜 것인가 | multi-AZ 또는 multi-Region 판단 |

## 콘솔 실험
EC2 화면에서 서울 Region을 보고, 다른 Region으로 바꾼 뒤 instance list가 달라지는지 확인한다. 이때 resource가 삭제된 것이 아니라 조회 범위가 바뀐 것이다. 이 작은 실험은 AWS 초반에 매우 중요하다. 많은 학생이 "방금 만든 게 사라졌다"고 느끼지만 실제 원인은 Region mismatch다.

## 장애 분석 연결
| 장애 증상 | Region/AZ 관점 질문 |
|---|---|
| ALB target 등록 실패 | ALB와 target이 같은 VPC/Region인가 |
| RDS 연결 실패 | app subnet과 DB subnet/security group이 맞는가 |
| EBS volume attach 실패 | instance와 volume AZ가 같은가 |
| resource가 안 보임 | Console Region이 맞는가 |

## 캡처 가이드
Region selector, subnet list의 AZ column, VPC ID가 함께 보이도록 캡처한다. account email은 제외하고, resource ID 일부와 tag는 남겨도 된다.

## 강사 보강 노트
이 교시는 `Region/AZ 경계`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| 서울 Region에서 만들고 다른 Region을 보고 있음 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| AZ를 backup location처럼 이해함 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| global service와 regional service를 구분하지 못함 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

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
| 화면 캡처 | 현재 Region selector | 성공 toast만 보이는 캡처 |
| 설정 기록 | resource 생성 Region | "기본값 사용"이라고만 적음 |
| 운영 판단 | multi-AZ가 필요한 service 후보 | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D1S3 region az
- 오늘 실습 Region:
- 선택 이유:
- 확인한 AZ 이름:
- Region을 바꾸면 사라져 보일 resource:
- 비용 확인 시 Region filter가 필요한 이유:
```

## 혼자 다시 따라오기
- 최소 재현 경로: Console 오른쪽 위 Region을 확인하고, EC2/VPC/S3 화면에서 resource 범위가 어떻게 보이는지 비교한다.
- 공식 문서 키워드: `AWS Regions`, `Availability Zones`, `isolated locations`.
- 스스로 확인할 화면: Region selector, VPC subnet list, EC2 launch placement.
- 흔한 실패 3개: Region이 달라 resource를 못 찾음, AZ와 Region을 같은 말로 씀, S3 bucket의 global name 특성을 Region resource처럼 오해함.
- 다음 준비 상태: "서울 Region의 여러 AZ에 subnet이 나뉜다"는 문장을 설명할 수 있어야 한다.

## 한 줄 요약
```text
AWS에서 resource를 못 찾으면 먼저 이름보다 Region을 확인한다.
```
