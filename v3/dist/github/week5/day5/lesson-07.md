# 7교시 · 다음 걸음 + 마지막 배움일기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 이 과정에서 **소개만 하고 지나간 것**을 모아, 다음에 배울 지도를 그립니다.
> - 나의 **30일 계획**을 정합니다.
> - 마지막 배움일기를 씁니다.

## 소개만 하고 지나간 것

| 주제 | 어디서 만났나 | 다음 걸음 |
|---|---|---|
| **관리형 DB** (RDS · ElastiCache) | 오늘 4교시 | devmart-infra에 RDS 모듈 → db를 옮기고 AZ 훈련을 다시 |
| **비밀 값의 GitOps** | 4주차 3일차, 5주차 4일차 | External Secrets Operator + AWS Secrets Manager (Pod Identity로) |
| **EKS 위의 관찰** | 5주차 4일차(안 올림) | kube-prometheus-stack 또는 Amazon Managed Prometheus · Grafana, OpenTelemetry |
| **오토스케일링** | 2일차 6교시, 4주차 4일차 | HPA · KEDA(Pod), Karpenter(노드) |
| **TLS · 도메인** | 4주차 1일차, 2일차 5교시 | Route 53 + ACM 인증서 + Gateway HTTPS 리스너, ExternalDNS |
| **공급망 보안** | 4주차 5일차 | cosign 서명 · SLSA 증명 · Kyverno ImageValidatingPolicy |
| **플랫폼도 GitOps** | 4일차 4교시 | install.sh → Argo CD app of apps · ApplicationSet |
| **CI에서 apply** | 3일차 7교시 | main 브랜치 apply 역할(OIDC) · Atlantis |
| **멀티 환경 · 멀티 클러스터** | 오늘 3교시 | ApplicationSet · Kargo |

## 자격증과 학습 자료

| 목표 | 자격증 (2026 기준) | 이 과정에서 이미 한 것 |
|---|---|---|
| AWS 전반 | AWS Certified Solutions Architect – Associate | IAM · VPC · EC2 · ALB · S3 · EKS |
| Kubernetes 운영 | CKA (Certified Kubernetes Administrator) | 3 · 4주차 전체 |
| Kubernetes 앱 | CKAD | 3주차 · 4주차 1 · 5일차 |
| Kubernetes 보안 | CKS | 4주차 4 · 5일차 |
| IaC | HashiCorp Terraform Associate | 5주차 3 · 4일차 |

자격증은 **지도를 빈틈없이 채우게** 해 주는 도구입니다. 시험 범위를 이 과정의 목차와 나란히 놓고, 비어 있는 칸부터 공부합니다.

> [!TIP]
> **공부의 순서**
>
> ① 이 과정의 저장소를 **처음부터 혼자 다시** 만든다(교재를 덜 보며) → ② 위 표의 다음 걸음을 **하나씩 PR로** 더한다 → ③ 막히는 곳을 **글로 쓴다**(블로그 · README) → ④ 자격증으로 빈칸을 채운다. 읽는 것보다 **다시 만드는 것**이 훨씬 오래 남습니다.

## 실습 10 · 나의 30일 계획

```bash
cat >> ~/devops-lab/RETRO-COURSE.md <<'MD'

## 30일 계획
| 주 | 할 것 (한 번에 끝낼 수 있게) | 확인 방법 |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
MD
```

예:

| 주 | 할 것 | 확인 방법 |
|---|---|---|
| 1 | 5주차 4일차를 교재 없이 다시 — `up.sh`를 처음부터 내가 쓴다 | 30분 안에 DevMart가 NLB로 열린다 |
| 2 | devmart-infra에 RDS(PostgreSQL) 모듈, db를 RDS로 | 오늘 4교시 훈련 2에서 주문이 멈추지 않는다 |
| 3 | External Secrets + Secrets Manager로 `devmart-db` | 배포 저장소만으로 클러스터를 새로 세울 수 있다 (Secret 손작업 0) |
| 4 | CKA 또는 SAA 모의고사 두 번, 틀린 범위를 저장소에 PR로 | 점수 · PR 링크 |

> **🎓 학술 노트 — 의도적 연습**
>
> Ericsson 외의 *The Role of Deliberate Practice in the Acquisition of Expert Performance*(Psychological Review, 1993)는 전문성이 단순한 반복이 아니라 **목표가 분명하고, 피드백이 즉각적이고, 지금 실력보다 조금 어려운** 연습에서 자란다는 것을 보였습니다. 30일 계획의 '확인 방법' 칸이 그 피드백이고, '교재 없이 다시'가 그 조금 어려운 연습입니다.

> **📈 트렌드 2026 — AI와 함께 일하는 DevOps**
>
> AI 에이전트가 Terraform을 쓰고, 장애 채널에서 원인을 요약하고, PR을 리뷰하는 일이 일상이 되었습니다. 그럴수록 사람에게 남는 일은 이 과정에서 반복한 것들입니다 — **plan을 읽고 위험을 가려내기**(돈 · 권한 · 공개 · 삭제), **원하는 상태를 정확히 적기**, **장애에서 '누가 거절했나'를 묻기**, **비용과 책임을 판단하기**. 도구는 바뀌어도 이 판단은 여러분의 것입니다.

> [!NOTE]
> **마지막 배움일기**
>
> - 오늘 `up.sh`로 잰 시간과, 1주차의 나라면 같은 일을 얼마나 걸렸을지
> - 커밋 하나가 두 클러스터에 간 순간 — 무엇이 그것을 가능하게 했나 (세 가지)
> - 훈련 2에서 주문이 멈춘 이유를 친구에게 설명하듯 세 문장으로
> - 이번 주 AWS 비용과, 가장 큰 줄 · 줄이는 방법
> - 5주 동안 가장 오래 막혔던 순간과, 결국 무엇이 풀었나
> - 다섯 주를 꿰는 한 문장 — 내 말로
> - 30일 계획의 첫 주에 할 일 하나

## 마치며

1주차 1일차에 "클라우드는 남의 컴퓨터"라는 말로 시작했습니다. 다섯 주 뒤, 여러분은 그 남의 컴퓨터를 **코드로 빌리고, 그 위에 서비스를 올리고, 지켜보고, 고치고, 지키고, 남김없이 돌려주는** 일을 처음부터 끝까지 해 보았습니다. 이 과정의 저장소 셋은 그 증거입니다. 다음은 그것을 **여러분의 것으로** 다시 만드는 일입니다.

## 참고 문헌

- Ericsson, K. A., Krampe, R. T. & Tesch-Römer, C. (1993). *The Role of Deliberate Practice in the Acquisition of Expert Performance*. Psychological Review 100(3).
- AWS Training and Certification. *AWS Certified Solutions Architect – Associate*. aws.amazon.com/certification
- The Linux Foundation. *CKA · CKAD · CKS*. training.linuxfoundation.org
- HashiCorp. *Terraform Associate certification*. developer.hashicorp.com/certifications
