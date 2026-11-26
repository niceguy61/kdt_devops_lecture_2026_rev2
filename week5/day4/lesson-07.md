<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [4일차](README.md) › 7/8교시</sub>

# 7교시 · EKS 버전 수명과 업그레이드 리허설 (plan만)

> [!NOTE]
> **이번 시간에 할 일**
>
> - Kubernetes와 EKS의 **버전 수명**을 알고, 업그레이드를 미루면 **돈이 든다**는 것을 숫자로 봅니다.
> - 업그레이드 전에 확인할 것 — **업그레이드 인사이트 · 사라지는 API · 애드온 호환** — 을 CLI로 점검합니다.
> - Terraform에서 버전 숫자 하나를 바꾼 `plan`을 읽고, **무엇이 어떤 순서로** 바뀌는지 봅니다(apply는 하지 않습니다).
> - 제자리 업그레이드와 **새 클러스터로 옮기기**(블루/그린) 중 무엇을 고를지 판단합니다.

> [!IMPORTANT]
> **클러스터는 '한 번 만들고 끝'이 아니다**
>
> Kubernetes는 **1년에 세 번** 새 마이너 버전(1.36 → 1.37 → …)을 내고, 각 버전은 약 14개월만 고쳐 줍니다. 오늘 만든 1.36 클러스터도 내년 이맘때면 **업그레이드하지 않으면 안 되는** 상태가 됩니다. 업그레이드는 사고가 아니라 **정기 일정**입니다. 그래서 운영 팀은 "한 번에 하나씩, 리허설을 거쳐, 되돌릴 계획과 함께"를 규칙으로 둡니다.

## 버전 수명 — 미루면 돈이 든다

| | 표준 지원 | 연장 지원 |
|---|---|---|
| 기간 | 버전 출시 후 약 **14개월** | 그 뒤 **12개월** 더 |
| EKS 요금 (클러스터당) | 시간당 **$0.10** | 시간당 **$0.60** — 여섯 배 |
| 연장 지원도 끝나면 | — | AWS가 **강제로** 다음 버전으로 올린다 |

클러스터 하나를 연장 지원에 1년 두면 $0.50 × 24 × 365 ≈ **$4,380**이 더 듭니다. 업그레이드를 미루는 것도 비용입니다.

## 실습 13 · 지금 버전과 다음 버전

```bash
cd ~/devmart-infra/terraform/eks
aws eks describe-cluster --name devmart --query 'cluster.[version, platformVersion]' --output text
aws eks describe-cluster-versions --query 'clusterVersions[].[clusterVersion, status, endOfStandardSupportDate]' \
  --output table | head -12
```

> **🟢 확인: 보이는 것 (예 — 날짜 · 버전은 조회하는 날 기준)**
>
> ```text
> 1.36    eks.3
> -------------------------------------------------------------
> |                  DescribeClusterVersions                  |
> +-------+-------------------+-----------------------------+
> |  1.37 |  STANDARD_SUPPORT |  2028-01-…                  |
> |  1.36 |  STANDARD_SUPPORT |  2027-08-…                  |
> |  1.35 |  STANDARD_SUPPORT |  2027-03-…                  |
> |  1.34 |  EXTENDED_SUPPORT |  2026-11-…                  |
> ```
> 오늘 클러스터(1.36)의 표준 지원이 **언제 끝나는지**, 그 위에 어떤 버전이 열려 있는지 봅니다. 아래에서 `NEXT`는 이 표의 **바로 위 버전**입니다. 표에 1.36보다 높은 버전이 없으면 아래 실습은 "1.36 → 1.36"으로 바꿀 것이 없다는 plan이 나옵니다 — 그때는 강사 화면으로 봅니다.

```bash
NEXT=1.37        # 위 표에서 1.36 바로 위 버전
```

## 실습 14 · 올리기 전에 확인할 세 가지

### 1 — EKS 업그레이드 인사이트

```bash
aws eks list-insights --cluster-name devmart \
  --query 'insights[].[category, name, insightStatus.status]' --output table
```

> **🟢 확인: 보이는 것 (예)**
>
> ```text
> | UPGRADE_READINESS |  Deprecated APIs removed in Kubernetes v1.37 |  PASSING |
> | UPGRADE_READINESS |  Kubelet version skew                         |  PASSING |
> | UPGRADE_READINESS |  EKS add-on version compatibility             |  PASSING |
> ```
> EKS가 클러스터의 **실제 사용 기록**을 보고 미리 점검해 둔 결과입니다. `ERROR` · `WARNING`이 있으면 `aws eks describe-insight --id …`로 **어느 리소스가** 문제인지 봅니다. 클러스터를 만든 지 얼마 안 됐으면 결과가 아직 없을 수 있습니다.

### 2 — 사라지는 API를 누가 부르나

```bash
kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis | head -5
```

Kubernetes는 오래된 API(예: 옛 `…/v1beta1`)를 **몇 버전 동안 경고만 하다가 지웁니다.** 이 지표에 줄이 있으면 **누군가 곧 사라질 API를 부르고 있다**는 뜻입니다. 3주차 1일차 8교시의 "늘렸다가 줄이기"를 Kubernetes가 스스로 하는 것입니다 — 우리는 '옮기기' 단계를 제때 해야 합니다. DevMart의 매니페스트는 모두 현재 API(`apps/v1` 등)를 쓰므로 비어 있는 게 정상입니다.

### 3 — 애드온은 다음 버전과 맞나

```bash
for a in vpc-cni coredns kube-proxy aws-ebs-csi-driver eks-pod-identity-agent metrics-server; do
  printf '%-24s 지금 %-22s %s용 기본 %s\n' $a \
    "$(aws eks describe-addon --cluster-name devmart --addon-name $a --query addon.addonVersion --output text)" \
    $NEXT \
    "$(aws eks describe-addon-versions --addon-name $a --kubernetes-version $NEXT \
        --query 'addons[0].addonVersions[?compatibilities[?defaultVersion==`true`]].addonVersion | [0]' --output text)"
done
```

> **🟢 확인: 보이는 것 (예)**
>
> ```text
> vpc-cni                  지금 v1.21.1-eksbuild.1   1.37용 기본 v1.21.1-eksbuild.1
> coredns                  지금 v1.12.4-eksbuild.1   1.37용 기본 v1.13.1-eksbuild.1
> kube-proxy               지금 v1.36.2-eksbuild.2   1.37용 기본 v1.37.0-eksbuild.1
> …
> ```
> `kube-proxy`처럼 **Kubernetes 버전에 묶인** 애드온은 반드시 함께 올라갑니다. 그 밖의 것은 같은 버전을 계속 써도 되는지 이 표로 확인합니다.

## 실습 15 · 숫자 하나 바꾼 plan 읽기

```bash
terraform plan -var kubernetes_version=$NEXT -no-color > upgrade.plan.txt
grep -E '^\s+# |version\s+=|release_version|Plan:' upgrade.plan.txt | head -30
```

> **🟢 확인: 보이는 것 (예 · 일부)**
>
> ```text
>   # module.eks.aws_eks_addon.this["coredns"] will be updated in-place
>       ~ addon_version = "v1.12.4-eksbuild.1" -> "v1.13.1-eksbuild.1"
>   # module.eks.aws_eks_addon.this["kube-proxy"] will be updated in-place
>       ~ addon_version = "v1.36.2-eksbuild.2" -> "v1.37.0-eksbuild.1"
>   # module.eks.aws_eks_cluster.this[0] will be updated in-place
>       ~ version = "1.36" -> "1.37"
>   # module.eks.module.eks_managed_node_group["default"].aws_eks_node_group.this[0] will be updated in-place
>       ~ version = "1.36" -> "1.37"
> Plan: 0 to add, 4 to change, 0 to destroy.
> ```

3일차 8교시의 다섯 질문으로 읽습니다.

| 질문 | 이 plan에서 |
|---|---|
| ① 지워지는 것? | 0 — 좋다 |
| ② `-/+` 교체? | 없다. **클러스터는 제자리**(in-place)로 올라간다 |
| ③ 변경 수? | 4 — 컨트롤 플레인 · 애드온 · 노드 그룹 |
| ④ 공개 · 보안? | 바뀌지 않음 |
| ⑤ 돈? | 업그레이드 동안 노드가 **잠깐 하나 더** 뜬다(새 노드를 먼저 띄우고 옛 노드를 비운다) |

> [!WARNING]
> **apply 순서는 Terraform이 아니라 규칙이 정한다**
>
> plan에는 넷이 나란히 있지만, 실제 업그레이드는 **컨트롤 플레인 → 애드온 → 노드** 순서여야 합니다. kubelet(노드)은 apiserver보다 **새 버전이면 안 되기** 때문입니다(버전 차이 규칙: 노드는 컨트롤 플레인보다 최대 세 단계 낮을 수 있고, 높을 수는 없다). 모듈은 내부 의존으로 이 순서를 지키지만, 그래도 운영에서는 **컨트롤 플레인만 먼저** 올리는 PR, 노드를 올리는 PR을 **나눠서** 냅니다. 그리고 **한 번에 한 단계씩만** — 1.36에서 1.38로 바로 갈 수 없습니다. **되돌릴(다운그레이드) 수도 없습니다.**

```bash
rm upgrade.plan.txt
```

## 제자리 업그레이드 vs 새 클러스터로 옮기기

| | 제자리 (in-place) | 블루/그린 (새 클러스터) |
|---|---|---|
| 방법 | 오늘 plan 그대로 apply | 새 버전 클러스터를 **하나 더** 만들고, 같은 배포 저장소로 띄운 뒤 손님을 옮긴다 |
| 되돌리기 | **불가** (컨트롤 플레인 다운그레이드 없음) | 손님을 옛 클러스터로 다시 보내면 끝 |
| 비용 | 낮다 | 옮기는 동안 클러스터 **두 개** 값 |
| 전제 | PodDisruptionBudget · 여러 노드 · 여러 복제본 | **모든 것이 코드**(Terraform + GitOps) — 내일 3교시의 "커밋 하나, 클러스터 둘" |

이 과정에서 만든 구조(Terraform으로 클러스터, Argo CD로 그 위)는 **블루/그린을 고를 수 있게** 해 줍니다. 클러스터를 다시 만드는 데 드는 것이 `up.sh` 하나(내일 2교시)이기 때문입니다.

> **🧹 정리: 정리**
>
> 오늘은 plan만 봤으므로 바뀐 것이 없습니다. 8교시에 모두 지웁니다.

> **🎓 학술 노트 — 소프트웨어 노화 (Parnas, 1994)**
>
> 데이비드 파나스(David Parnas)는 ICSE 1994의 초청 논문 「Software Aging」에서, 소프트웨어는 코드가 썩지 않아도 **주변 세상이 변하기 때문에 늙는다**고 했습니다. 운영체제 · 라이브러리 · 사용자의 기대가 바뀌는데 소프트웨어가 따라가지 않으면, 어느 순간 **고칠 수 없을 만큼 뒤처진다**는 것입니다. 그는 노화를 막을 수는 없고, **계속 갱신할 수 있게 설계하고 갱신을 일상으로** 만드는 것만이 처방이라고 했습니다. Kubernetes의 1년 세 번 출시와 14개월 지원은 이 노화를 **달력에 적어 둔** 것이고, 2주차 3일차의 "다시 빌드"와 3주차의 "늘렸다가 줄이기", 오늘의 업그레이드 리허설이 그 처방입니다.
>
> - Parnas, D. L. (1994). Software aging. *Proceedings of the 16th International Conference on Software Engineering (ICSE '94)*, 279–287.

> **📈 트렌드 — 업그레이드를 맡기거나, 길게 지원받거나**
>
> 노드 업그레이드의 수고를 줄이려고 **EKS Auto Mode**(2024)처럼 노드 · 핵심 애드온까지 AWS가 관리하고 업그레이드하는 방식이 나왔고, Karpenter는 노드의 **수명(expireAfter)**을 정해 오래된 노드를 자동으로 새 이미지로 바꿉니다. 반대편에서는 "업그레이드를 덜 하고 싶다"는 요구로 Kubernetes 커뮤니티에서 **장기 지원(LTS)** 논의가 이어지고, 클라우드들은 오늘 본 **유료 연장 지원**으로 답하고 있습니다. 어느 쪽이든 **"모든 것이 코드"인 클러스터만 쉽게 갈아탈 수 있다**는 것은 같습니다.

## 정리

- Kubernetes는 1년에 세 번, 각 버전 약 14개월 지원. EKS 연장 지원은 **여섯 배** 요금 — 미루는 것도 비용입니다.
- 올리기 전에: **업그레이드 인사이트 · 사라지는 API 지표 · 애드온 호환**.
- 버전 숫자 하나 바꾼 `plan`: 컨트롤 플레인 · 애드온 · 노드가 **제자리**로. 순서는 **컨트롤 플레인 → 애드온 → 노드**, **한 단계씩**, **되돌릴 수 없음**.
- 되돌릴 수 있어야 하면 **블루/그린** — 모든 것이 코드라서 가능한 선택입니다.

> **✅ 확인 문제**
>
> 1. 1.36 클러스터를 표준 지원이 끝난 뒤 1년 더 두면 EKS 요금은 대략 얼마 더 드나요?
> 2. `apiserver_requested_deprecated_apis` 지표에 줄이 있다는 것은 무슨 뜻인가요?
> 3. 노드를 컨트롤 플레인보다 먼저 올리면 안 되는 이유는?
> 4. 1.36에서 1.38로 한 번에 갈 수 있나요?
> 5. 업그레이드 뒤 문제가 생겨 되돌리고 싶습니다. 제자리 업그레이드와 블루/그린 중 무엇을 골랐어야 했나요?
>
> <details><summary>정답</summary>
>
> 1. ($0.60 − $0.10) × 24 × 365 ≈ $4,380
> 2. 누군가 곧 사라질(다음 버전들에서 지워질) API를 아직 부르고 있다 — 업그레이드 전에 그 매니페스트 · 도구를 고쳐야 한다
> 3. kubelet은 apiserver보다 새 버전이면 안 된다(버전 차이 규칙)
> 4. 없다 — 한 번에 한 마이너 버전씩
> 5. 블루/그린 — 컨트롤 플레인은 다운그레이드가 안 되지만, 새 클러스터로 옮겼다면 손님을 옛 클러스터로 돌리면 된다
>
> </details>

## 참고 문헌

- Parnas, D. L. (1994). Software aging. *ICSE '94*.
- Kubernetes Documentation. *Version Skew Policy*; *Release cycle*; *Deprecated API Migration Guide*.
- AWS Docs. *Understand the Kubernetes version lifecycle on EKS — standard and extended support*; *Prepare for Kubernetes version upgrades with cluster insights*; *Update existing cluster to new Kubernetes version*; *describe-cluster-versions*. docs.aws.amazon.com/eks
- AWS. *Amazon EKS pricing*. aws.amazon.com/eks/pricing
- terraform-aws-modules. *terraform-aws-eks v21 — Upgrade notes*. github.com/terraform-aws-modules/terraform-aws-eks

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 클라우드에서 달라진 것](lesson-06.md) | [⬆️ 4일차 목차](README.md) | [8교시 · 지우는 순서](lesson-08.md) ➡️ |
