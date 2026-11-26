<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [4일차](README.md) › 7/7교시</sub>

# 7교시 · 지우는 순서

> [!NOTE]
> **이번 시간에 할 일**
>
> - **Kubernetes가 만든 AWS 자원**(NLB · EBS)과 **Terraform이 만든 자원**을 구분합니다.
> - 의존 순서대로 — 앱 → 입구 → 클러스터 — 지웁니다.
> - 남은 것이 없는지 **AWS 쪽에서** 확인합니다.
> - 오늘을 배움일기로 정리합니다.

## 누가 무엇을 만들었나

| 자원 | 만든 것 | Terraform 장부에 | 지우는 방법 |
|---|---|---|---|
| NLB · 대상 그룹 · NLB 보안 그룹 | **LBC** (Service LoadBalancer를 보고) | ✗ | Service를 지운다 → LBC가 지운다 |
| EBS 볼륨 (db PVC) | **EBS CSI** (PVC를 보고) | ✗ | PVC를 지운다 → `reclaimPolicy: Delete` |
| VPC · NAT · EKS · 노드 그룹 · IAM 역할 | Terraform | ✓ | `terraform destroy` |

거꾸로 하면 — Terraform부터 지우면 — 클러스터가 먼저 사라져 LBC · EBS CSI가 **뒷정리를 못 합니다.** NLB와 EBS가 고아로 남아 과금되고, NLB가 public 서브넷을 붙잡아 VPC 삭제도 실패합니다(4교시 경고).

## 실습 13 · 지우기

```bash
cd ~/devops-lab/aws/w5d4
cat cleanup.sh
./cleanup.sh
```

> **🟢 확인: 확인**
>
> ```text
> == 1. 앱을 지운다 — PVC가 지워지면 EBS 볼륨도 지워진다 (reclaimPolicy: Delete)
> application.argoproj.io "devmart" deleted
> namespace "devmart" deleted
> == 2. Envoy Gateway를 지운다 — LoadBalancer Service가 사라지면 NLB도 지워진다
> release "eg" uninstalled
> namespace "envoy-gateway-system" deleted
> == 3. NLB가 정말 사라졌나 (빈 줄이 나올 때까지 기다린다)
> 남음: k8s-envoygat-envoydev-0a1b2c3d4e
> 없음
> == 4. 남은 EBS 볼륨 (kubernetes.io 태그)
> (빈 줄)
> == 이제: cd terraform/eks && terraform destroy
> ```

> [!WARNING]
> **Application을 지우면 Namespace까지**
>
> 4주차 3일차 4교시에서 `argocd app delete`는 Namespace까지 지운다고 경고했습니다. 오늘은 그것을 **일부러** 씁니다 — Namespace가 지워지면 그 안의 PVC → EBS, Secret까지 깨끗이 사라집니다.

```bash
cd ~/devmart-infra/terraform/eks
time terraform destroy
```

> **🟢 확인: 확인 (10~15분)**
>
> ```text
> Plan: 0 to add, 0 to change, 5○ to destroy.
> …
> module.eks.module.eks_managed_node_group["default"].aws_eks_node_group.this[0]: Destroying...
> …
> module.eks.aws_eks_cluster.this[0]: Destruction complete after 4m…
> module.vpc.aws_nat_gateway.this[0]: Destruction complete after 1m…
> module.vpc.aws_vpc.this[0]: Destruction complete after 1s
> Destroy complete! Resources: 5○ destroyed.
> real    1○m○s
> ```

## 실습 14 · AWS 쪽에서 확인

장부가 비었다고 끝이 아닙니다. **AWS가 실제로** 비었는지 봅니다.

```bash
~/devops-lab/aws/w5d1/check-account.sh | tail -5
aws eks list-clusters --query clusters --output text
aws ec2 describe-volumes --filters Name=status,Values=available,in-use --query 'Volumes[].[VolumeId,Size,AvailabilityZone]' --output text
aws ec2 describe-network-interfaces --query 'NetworkInterfaces[].[NetworkInterfaceId,Description]' --output text | head
kubectl config delete-context $(kubectl config get-contexts -o name | grep eks) 2>/dev/null; true
```

> **🟢 확인: 확인**
>
> 모든 줄이 **비어 있어야** 합니다(기본 VPC의 것은 없다). 남은 것이 있으면:
>
> | 남은 것 | 원인 | 지우기 |
> |---|---|---|
> | EBS 볼륨 `available` | PVC를 지우기 전에 클러스터가 사라졌다 | EC2 → 볼륨 → 삭제 |
> | NLB `k8s-…` | Service를 지우기 전에 LBC가 사라졌다 | EC2 → 로드 밸런서 → 삭제, 대상 그룹 · 보안 그룹도 |
> | 탄력적 IP | NAT용 EIP가 남았다 | VPC → 탄력적 IP → 릴리스 |
> | ENI `available` | 위의 것이 남아 있다 | 위를 지우면 함께 사라진다 |

**결제 및 비용 관리 → 청구서**에서 오늘 날짜의 EKS · EC2 · VPC(NAT · 공인 IP) · ELB 항목을 봅니다(몇 시간 늦게 반영). 대략 **$1.5~2**가 크레딧에서 나갔을 것입니다.

> [!TIP]
> **내일은 다시 만든다**
>
> 내일 아침 같은 코드로 다시 apply합니다. 오늘 16분 + 플랫폼 8분 + 앱 3분 — 약 **30분**이면 같은 상태로 돌아옵니다. 매일 지우고 다시 만드는 것이 비용을 아끼는 동시에 **코드가 진짜로 재현되는지**를 매일 시험하는 일입니다(2일차 학술 노트의 '버릴 수 있는 인프라').

> **❓ 오해 — terraform destroy가 끝나면 다 지워졌다**
>
> Terraform은 **자기 장부의 것**만 지웁니다(3일차 4교시). 클러스터 안의 컨트롤러(LBC · EBS CSI · 그리고 앞으로 쓸 Karpenter · ExternalDNS …)가 만든 AWS 자원은 장부에 없습니다. 그래서 순서는 언제나 **Kubernetes 쪽 먼저, 클러스터는 마지막**이고, 끝에는 **AWS 쪽에서** 확인합니다.

> **🎓 학술 노트 — 소유권의 경계**
>
> 누가 어떤 자원을 '소유'하고 수명을 책임지는가는 4주차의 Kubernetes(ownerReferences · Argo CD 추적 표시), 3일차의 Terraform(state)에서 계속 나온 주제입니다. 두 시스템이 같은 클라우드를 **각자의 장부로** 다루면, 장부 사이의 틈에서 고아 자원이 생깁니다. 이것은 분산 시스템의 **가비지 컬렉션** 문제와 같은 구조이며(Plainfossé & Shapiro, *A Survey of Distributed Garbage Collection Techniques*, IWMM 1995), 실무의 해법은 ① 만든 쪽이 지우게 순서를 지키기, ② 태그로 소유자를 적어 두고 주기적으로 훑기입니다.

> **📈 트렌드 2026 — 하루살이 환경**
>
> PR마다 클러스터 · 환경을 **만들었다가 합치면 지우는**(ephemeral environments) 방식이 흔해졌습니다. 그 전제가 오늘의 두 가지 — ① 코드로 30분 안에 재현, ② 지울 때 아무것도 남지 않음 — 입니다. 비용 도구들은 '태그 없는 자원', '주인 없는 볼륨'을 매일 찾아 알려 줍니다.

> **✅ 확인 문제**
>
> 1. NLB와 EBS 볼륨이 Terraform 장부에 없는 이유는?
> 2. terraform destroy를 먼저 하면 생기는 일 둘은?
> 3. Argo CD Application 삭제를 일부러 쓴 이유는?
> 4. destroy가 끝난 뒤에도 AWS 쪽에서 확인하는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 클러스터 안의 컨트롤러(LBC · EBS CSI)가 Kubernetes 리소스를 보고 만들었기 때문
> 2. NLB · EBS가 고아로 남아 계속 과금된다, NLB가 서브넷을 붙잡아 VPC 삭제가 실패한다
> 3. Namespace까지 지워져 PVC → EBS, Secret까지 깨끗이 사라지게 하려고
> 4. Terraform은 자기 장부의 것만 지우므로, 컨트롤러가 만든 자원이 남았을 수 있기 때문
>
> </details>

> [!NOTE]
> **오늘의 배움일기**
>
> - EKS에서 AWS가 운영하는 것과 내가 만든 것, kind와 짝지어 셋씩
> - 50개 plan에서 내가 실제로 확인한 것 넷 (돈 · 권한 · 공개 · 삭제)
> - 사람 → 클러스터, Pod → AWS — 두 방향의 신원을 각각 한 문장으로
> - DevMart를 EKS에 올리면서 바뀐 파일과 바뀌지 않은 파일
> - Pod IP · NLB 대상 · EBS의 AZ — 오늘 가장 '클라우드답다'고 느낀 것
> - 오늘 만들고 지운 시간: apply __분 · 플랫폼 __분 · destroy __분, 오늘의 비용 $__
> - 내일 전에 궁금한 것: 내일 다시 만들면 **정말로 30분 안에** 같아질까? 그리고 **노드 하나가 죽으면** db는 어떻게 될까?

## 참고 문헌

- AWS Docs. *Delete a cluster — delete Services and PVCs first*. docs.aws.amazon.com/eks
- AWS Load Balancer Controller Docs. *Deleting load balancers*. kubernetes-sigs.github.io/aws-load-balancer-controller
- Plainfossé, D. & Shapiro, M. (1995). *A Survey of Distributed Garbage Collection Techniques*. IWMM '95.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 클라우드에서 달라진 것](lesson-06.md) | [⬆️ 4일차 목차](README.md) | [5주차 5일차 목차](../day5/README.md) ➡️ |
