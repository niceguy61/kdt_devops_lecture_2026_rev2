[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [4일차](README.md)

# 6교시 · 클라우드에서 달라진 것

> [!NOTE]
> **이번 시간에 할 일**
>
> - Pod IP가 **VPC 주소**라는 것을 EC2 콘솔의 네트워크 인터페이스에서 확인합니다.
> - NLB가 어떻게 **Envoy Pod로 바로** 보내는지 대상 그룹에서 봅니다.
> - PVC가 **EBS 볼륨**이 되고, 그 볼륨이 **AZ 하나에 묶인** 것을 봅니다.
> - 노드를 늘려 보고, 콘솔의 EKS 화면을 둘러봅니다.

## 실습 9 · Pod IP = VPC IP

```bash
kubectl get pods -n devmart -o custom-columns=NAME:.metadata.name,IP:.status.podIP,NODE:.spec.nodeName
kubectl get nodes -o custom-columns=NAME:.metadata.name,IP:.status.addresses[0].address,ZONE:.metadata.labels.topology\\.kubernetes\\.io/zone
```

> **🟢 확인: 확인**
>
> ```text
> NAME                            IP             NODE
> catalog-api-7c9d8b6f4-m2k8q     10.0.137.201   ip-10-0-131-52…
> catalog-api-7c9d8b6f4-x4p7w     10.0.154.88    ip-10-0-150-17…
> db-6b7f8c9d5-q4w2e              10.0.140.33    ip-10-0-131-52…
> …
> NAME                IP            ZONE
> ip-10-0-131-52…     10.0.131.52   ap-northeast-2a
> ip-10-0-150-17…     10.0.150.17   ap-northeast-2c
> ```
> Pod IP가 kind의 `10.244.x.x`(클러스터 안에서만 의미 있는 주소)가 아니라 **VPC의 private 서브넷 주소**입니다. VPC CNI는 노드에 **네트워크 인터페이스(ENI)**를 더 붙이고, 그 보조 IP를 Pod에 나눠 줍니다.

EC2 콘솔 → **네트워크 인터페이스** → 필터 `10.0.137.201`(내 catalog-api Pod IP) → 그 ENI의 **보조 프라이빗 IPv4 주소**에 Pod IP가 있습니다. 쿠버네티스의 Pod가 AWS 네트워크에서 **일급 시민**으로 보이는 순간입니다.

| | kind (오버레이 네트워크) | EKS (VPC CNI) |
|---|---|---|
| Pod IP | 클러스터 안에서만 의미 | **VPC 안 어디서나** 닿는 주소 |
| 보안 그룹 · NLB가 Pod를 직접 | 불가 | **가능** (아래 NLB `ip` 대상) |
| 대가 | — | 노드 유형마다 Pod 수 상한(ENI × IP 수), 서브넷 IP 소모 |

> [!WARNING]
> **Pod 수 상한**
>
> t3.medium은 ENI 3개 × IP 6개라 노드당 **Pod 17개 남짓**이 한계입니다(`kubectl get node -o jsonpath='{.items[0].status.allocatable.pods}'`). 그 이상은 Pending입니다. 1일차 5교시에 서브넷을 /20으로 넉넉히 잡은 이유이고, 큰 클러스터는 **접두사 위임**(prefix delegation)으로 이 상한을 늘립니다.

## 실습 10 · NLB → Pod

EC2 → **로드 밸런서** → `k8s-envoygat-…` → **리스너** 탭 → 대상 그룹 → **대상** 탭

> **🟢 확인: 확인**
>
> 등록된 대상이 **노드 IP가 아니라 Envoy Pod IP**(`10.0.1xx.xx`)이고 상태 **Healthy**입니다. 4교시의 `nlb-target-type: ip`가 이것입니다. 2일차 ALB의 대상은 **인스턴스**였습니다 — 이제 대상이 **Pod**입니다.

```bash
kubectl scale deploy -n envoy-gateway-system -l gateway.envoyproxy.io/owning-gateway-name=devmart --replicas=2
sleep 60
aws elbv2 describe-target-health --target-group-arn $(aws elbv2 describe-target-groups --query "TargetGroups[?contains(TargetGroupName,'envoydev')].TargetGroupArn | [0]" --output text) \
  --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State]' --output text
```

> **🟢 확인: 확인**
>
> ```text
> 10.0.139.12   healthy
> 10.0.157.240  healthy
> ```
> Envoy Pod를 둘로 늘리자 LBC가 **대상 그룹에 자동으로** 더했습니다. 2일차에 Auto Scaling 그룹이 대상 그룹에 인스턴스를 등록하던 일을, 이제 Kubernetes 컨트롤러가 Pod 단위로 합니다.

## 실습 11 · PVC = EBS, 그리고 AZ

```bash
kubectl get pvc -n devmart
PV=$(kubectl get pvc db-data -n devmart -o jsonpath='{.spec.volumeName}')
kubectl get pv $PV -o jsonpath='{.spec.csi.volumeHandle}{"\n"}{.spec.nodeAffinity.required.nodeSelectorTerms[0].matchExpressions[0]}{"\n"}'
VOL=$(kubectl get pv $PV -o jsonpath='{.spec.csi.volumeHandle}')
aws ec2 describe-volumes --volume-ids $VOL --query 'Volumes[0].[VolumeType,Size,AvailabilityZone,State,Attachments[0].InstanceId,Encrypted]' --output text
```

> **🟢 확인: 확인**
>
> ```text
> NAME      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
> db-data   Bound    pvc-3f9a1c2e-…                             1Gi        RWO            gp3            30m
> vol-0a1b2c3d4e5f60718
> {"key":"topology.kubernetes.io/zone","operator":"In","values":["ap-northeast-2a"]}
> gp3  1  ap-northeast-2a  in-use  i-0c3d4e5f607182930  True
> ```
> - PVC 하나가 **EBS gp3 볼륨 하나**(`vol-…`)가 되었고, 암호화(True)되어 있습니다.
> - PV에 **nodeAffinity: ap-northeast-2a**가 붙었습니다 — 이 볼륨은 **2a의 노드에만** 붙을 수 있습니다. db Pod는 앞으로도 2a 노드에서만 뜰 수 있습니다.

> [!IMPORTANT]
> **EBS는 AZ에 묶인다**
>
> EBS 볼륨은 한 AZ 안의 블록 스토리지입니다. 2a의 노드가 모두 사라지면 db Pod는 2c 노드로 갈 수 **없어** Pending이 됩니다 — 데이터는 2a의 볼륨에 있으니까요. 내일 5교시 장애 훈련에서 직접 일으킵니다. 이것이 운영 DB를 Kubernetes Pod가 아니라 **RDS**(여러 AZ에 복제되는 관리형 DB)에 두는 큰 이유입니다.

## 실습 12 · 노드 늘리기 — 코드로

```bash
cd ~/devmart-infra/terraform/eks
terraform plan -var node_count=3 | grep -E "desired_size|Plan:"
```

> **🟢 확인: 확인**
>
> ```text
>       ~ desired_size = 2 -> 3
> Plan: 0 to add, 1 to change, 0 to destroy.
> ```
> apply하면 노드 그룹(= 2일차의 Auto Scaling 그룹)이 EC2를 하나 더 띄워 클러스터에 붙입니다(약 2~3분). 비용을 위해 오늘은 **plan만** 봅니다. 노드 수 같은 값은 `-var`가 아니라 코드(`variables.tf` 기본값)를 PR로 바꾸는 것이 원칙입니다(3일차 7교시).

## 콘솔 둘러보기

EKS 콘솔 → `devmart`:

| 탭 | 볼 것 |
|---|---|
| **개요** | 버전 1.36, 엔드포인트, 지원 기간(표준 · 연장) |
| **컴퓨팅** | 노드 그룹 `default`, 노드 둘 — EC2 콘솔의 인스턴스와 같은 것 |
| **리소스** | Pod · Deployment 목록 — Access Entry 덕분에 콘솔에서도 보인다 |
| **추가 기능** | 오늘 켠 애드온 여섯과 버전 |
| **액세스** | Access Entry — 나와 노드 그룹 역할 |
| **관찰성** | (오늘은 켜지 않은) 로그 · 지표 연결 |

```bash
kubectl top nodes
kubectl top pods -n devmart
```

> **🟢 확인: 확인**
>
> ```text
> NAME                CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
> ip-10-0-131-52…     118m         6%       1491Mi          44%
> ip-10-0-150-17…     96m          4%       1203Mi          35%
> …
> ```
> metrics-server 애드온 덕분입니다. 4주차 2일차의 Prometheus만큼은 아니지만, 노드가 얼마나 찼는지 바로 봅니다.

> **❓ 오해 — 클라우드 디스크는 어디서나 붙는다**
>
> S3(객체 저장소)는 리전 어디서나 읽히지만, **EBS(블록 저장소)는 AZ 하나**입니다. 여러 AZ에서 같은 파일을 쓰려면 EFS(네트워크 파일 시스템)를, 여러 AZ에 복제된 DB가 필요하면 RDS Multi-AZ를 씁니다. 저장소를 고르는 첫 질문은 "**어디서 붙여야 하나**"입니다.

> **🎓 학술 노트 — 플랫 네트워크의 비용**
>
> 'Pod마다 실제 네트워크 주소'는 Kubernetes 네트워크 모델의 원칙(모든 Pod가 NAT 없이 서로 닿는다)을 클라우드 네트워크에 **직접** 구현한 것입니다. 오버레이(VXLAN, 1일차 5교시)에 비해 캡슐화 비용이 없고 클라우드 장비(보안 그룹 · NLB)가 Pod를 직접 다룰 수 있지만, 주소 공간을 소모합니다. 이 트레이드오프는 Kubernetes 네트워킹 설계 문서와 AWS의 *Amazon VPC CNI* 설계 노트에 정리되어 있으며, IPv6 클러스터가 주소 부족의 근본 해법으로 제시됩니다.

> **📈 트렌드 2026 — 노드를 고르지 않는 클러스터**
>
> 오늘 `t3.medium × 2`를 **사람이** 골랐습니다. Karpenter · EKS Auto Mode는 대기 중인 Pod의 요구(CPU · 메모리 · AZ · 아키텍처)를 보고 **알맞은 EC2를 그때그때** 사고, 비면 돌려줍니다. 스팟 · Graviton을 섞어 비용을 크게 줄이는 것이 2026년 EKS 비용 최적화의 기본기입니다.

> **✅ 확인 문제**
>
> 1. EKS에서 Pod IP가 VPC 주소인 이유와, 그 장점 · 대가 하나씩은?
> 2. NLB의 대상이 인스턴스가 아니라 Pod IP인 것은 어떤 설정 덕분인가요?
> 3. db의 PV에 붙은 nodeAffinity의 뜻과, 그것이 장애 때 만드는 문제는?
> 4. 노드 수를 바꾸는 올바른 방법은?
>
> <details><summary>정답</summary>
>
> 1. VPC CNI가 ENI의 보조 IP를 Pod에 준다. 장점: NLB · 보안 그룹이 Pod를 직접 다룬다, 대가: 노드당 Pod 수 상한 · 서브넷 IP 소모
> 2. EnvoyProxy 주석 `aws-load-balancer-nlb-target-type: ip`
> 3. 그 볼륨이 ap-northeast-2a에만 있어 db Pod는 2a 노드에서만 뜰 수 있다 — 2a 노드가 없으면 Pending
> 4. Terraform 코드(variables.tf 기본값)를 PR로 바꾸고 apply
>
> </details>

## 참고 문헌

- AWS Docs. *Amazon VPC CNI*, *Maximum Pods per instance type*, *Prefix delegation*. docs.aws.amazon.com/eks
- AWS Docs. *Amazon EBS volumes — Availability Zone*, *Amazon EFS*, *Amazon RDS Multi-AZ*. docs.aws.amazon.com
- Kubernetes Docs. *Cluster Networking — The Kubernetes network model*. kubernetes.io/docs

---

⬅️ 이전: [5교시 · 같은 배포 저장소를 EKS에](lesson-05.md) &nbsp;|&nbsp; [⬆️ 4일차 목차](README.md) &nbsp;|&nbsp; 다음: [7교시 · 지우는 순서](lesson-07.md) ➡️
