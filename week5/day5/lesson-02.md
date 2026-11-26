<sub>[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [5일차](README.md) › 2/8교시</sub>

# 2교시 · 아침의 재현

> [!NOTE]
> **이번 시간에 할 일**
>
> - 어제 손으로 한 일을 **스크립트 하나**(`up.sh`)로 다시 합니다.
> - 단계마다 걸린 시간을 재고, 어디가 느린지 봅니다.
> - "코드로 만든 인프라는 **매일 다시 만들 수 있다**"를 직접 확인합니다.

## up.sh 읽기

```bash
cat ~/devops-lab/aws/w5d5/up.sh
```

| 단계 | 하는 일 | 어제의 어디 |
|---|---|---|
| 1 | `terraform apply` + kubeconfig | 4일차 2 · 3교시 |
| 2 | `platform/install.sh` — gp3 · LBC · Envoy Gateway · Argo CD | 4일차 4교시 |
| 3 | Secret · Application | 4일차 5교시 |
| 4 | NLB 주소가 생기고 `/api/products`가 200이 될 때까지 기다림 | 4일차 5교시 |

스크립트에 새로운 것은 없습니다. **어제 한 일의 순서를 적어 둔 것**입니다 — 런북(4주차 2일차)이 실행 가능해진 모양입니다.

## 실습 1 · 처음부터

```bash
aws sts get-caller-identity --query Arn --output text
~/devops-lab/aws/w5d5/up.sh
```

기다리는 동안(약 25~30분) 3교시를 위해 kind 클러스터를 확인해 둡니다.

```bash
kubectl --context kind-devmart get application -n argocd
kubectl --context kind-devmart get pods -n devmart | head -4
```

> **🟢 확인: 확인 — up.sh**
>
> ```text
> [0분 0초] 1. 클러스터 (Terraform)
> [16분 41초] 2. 플랫폼 (StorageClass · LBC · Envoy Gateway · Argo CD)
> [23분 12초] 3. Secret과 Application
> secret/devmart-db created
> application.argoproj.io/devmart created
> [23분 15초] 4. 손님이 들어올 수 있을 때까지
> [27분 48초] 완료 — http://k8s-envoygat-envoydev-….elb.ap-northeast-2.amazonaws.com/
> ```
> 어제 질문의 답 — **약 30분**. 사람이 한 일은 명령 **한 줄**입니다.

> **🟢 확인: 확인 — kind**
>
> ```text
> NAME      SYNC STATUS   HEALTH STATUS
> devmart   Synced        Healthy
> ```

| 단계 | 내 시간 | 가장 오래 걸린 것 |
|---|---|---|
| 1. 클러스터 | __분 | EKS 컨트롤 플레인 (~10분) |
| 2. 플랫폼 | __분 | Argo CD · LBC 준비 |
| 3~4. 앱 | __분 | NLB 활성화 · db 볼륨 |
| 합계 | __분 | |

> [!IMPORTANT]
> **어제와 오늘이 같은가**
>
> 어제 손으로 만든 결과와 오늘 스크립트의 결과가 **같은지**는 무엇으로 아나요? ① `terraform plan`이 `No changes`, ② Argo CD가 `Synced · Healthy`, ③ 손님 쪽 `curl`이 200. 세 층(인프라 · 앱 · 손님)이 각자의 '원하는 상태와 같다'를 보여 줍니다.
>
> ```bash
> terraform -chdir=$HOME/devmart-infra/terraform/eks plan -detailed-exitcode >/dev/null; echo "plan 종료 코드: $? (0 = 변경 없음)"
> kubectl --context eks-devmart get application devmart -n argocd -o jsonpath='{.status.sync.status} {.status.health.status}{"\n"}'
> ```

> [!TIP]
> **더 빠르게 하려면**
>
> 시간의 절반 이상이 EKS 컨트롤 플레인입니다. 실무에서 클러스터는 **오래 살리고**(업그레이드하며 몇 년), 그 위의 환경을 빠르게 만들었다 지웁니다(네임스페이스 · vCluster). 실습에서 매일 클러스터째 지우는 것은 **비용** 때문이고, 그 덕분에 '처음부터 다시 만들기'를 매일 시험하게 되었습니다.

> **❓ 오해 — 스크립트가 있으면 IaC다**
>
> `up.sh`는 **명령의 순서**(명령형)이지만, 그 안의 각 단계가 **선언적**(Terraform · Helm · Argo CD)이라 몇 번을 돌려도 같은 결과가 됩니다(멱등). 3일차 1교시의 "CLI 스크립트"와 다른 점입니다. 스크립트를 두 번 돌려 보면 확인할 수 있습니다 — 두 번째는 대부분 '변경 없음'으로 지나갑니다.

> **🎓 학술 노트 — 복구 시간의 측정**
>
> DORA의 네 지표(4주차 3일차) 중 **복구 시간**(time to restore)은 "장애에서 서비스를 되살리는 데 걸린 시간"입니다. 오늘 잰 30분은 '클러스터를 통째로 잃었을 때의 복구 시간'의 하한입니다(데이터 복구는 빠져 있다). Google SRE의 *Site Reliability Workbook* 9장은 재해 복구 계획을 **정기적으로 실제로 돌려 보지 않으면** 필요할 때 동작하지 않는다고 강조합니다 — 이번 주에 매일 지우고 다시 만든 것이 그 연습이었습니다.

> **📈 트렌드 2026 — 재현 가능한 환경의 표준**
>
> 개발 컨테이너(devcontainer) · Nix · 하루살이 환경이 흔해지면서 "**README의 명령 몇 줄로 누구나 같은 환경**"이 오픈소스와 회사 모두의 기대치가 되었습니다. 6교시에 포트폴리오 README에 `up.sh`를 적는 이유입니다 — 보는 사람이 직접 재현할 수 있는 것이 가장 강한 증거입니다.

> **✅ 확인 문제**
>
> 1. up.sh의 네 단계와 각각 어제의 몇 교시였나요?
> 2. "어제와 오늘이 같다"를 확인하는 세 층의 방법은?
> 3. 실무에서 클러스터를 매일 지우지 않는 이유와, 실습에서 매일 지운 이유는?
>
> <details><summary>정답</summary>
>
> 1. Terraform(2 · 3교시), 플랫폼(4교시), Secret · Application(5교시), 손님 확인(5교시)
> 2. terraform plan 변경 없음, Argo CD Synced · Healthy, curl 200
> 3. 실무: 컨트롤 플레인 생성이 오래 걸리고 클러스터는 오래 살려 업그레이드한다. 실습: 비용 — 덕분에 재현을 매일 시험했다
>
> </details>

## 참고 문헌

- Beyer, B. 외 (2018). *The Site Reliability Workbook*, Ch. 9 "Incident Response" · disaster recovery testing. O'Reilly.
- DORA. *DORA's software delivery metrics*. dora.dev

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [1교시 · 4일차 요약 + 5주 지도](lesson-01.md) | [⬆️ 5일차 목차](README.md) | [3교시 · 커밋 하나, 클러스터 둘](lesson-03.md) ➡️ |
