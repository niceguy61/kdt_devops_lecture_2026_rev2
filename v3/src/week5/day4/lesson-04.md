# 4교시 · 플랫폼 올리기

!!! goal "이번 시간에 할 일"
    - 기본 **StorageClass**를 EBS gp3로 정합니다.
    - **AWS Load Balancer Controller**를 설치합니다(Pod Identity로 권한).
    - 4주차의 **Envoy Gateway**를 같은 버전으로 올리되, 입구를 **NLB**로 바꿉니다.
    - **Argo CD**를 같은 values로 올립니다.

## 플랫폼 목록

| 순서 | 무엇 | 4주차 kind에서 | EKS에서 달라진 것 |
|---|---|---|---|
| 1 | StorageClass | `standard`(local-path) | **gp3**(EBS CSI) |
| 2 | Load Balancer Controller | (없음) | Service(LoadBalancer) → **NLB** |
| 3 | Envoy Gateway + Gateway | NodePort 30080 | **LoadBalancer** + 주석 셋 |
| 4 | Argo CD | 같은 values | 같다 |
| (안 올림) | kube-prometheus-stack · Istio · Kyverno | 있었다 | 노드 2대(4GB)에는 무겁다 — 5교시에 배포 저장소에서 뺀다 |

```bash
cd ~/devops-lab/aws/w5d4/platform
cat install.sh
```

스크립트를 한 단계씩 읽고, 실행은 한 번에 합니다.

## 1 · gp3 StorageClass

```yaml
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer   # Pod가 놓일 AZ가 정해진 뒤에 볼륨을 만든다
reclaimPolicy: Delete                     # PVC를 지우면 EBS도 지운다
parameters: { type: gp3, encrypted: "true" }
```

`WaitForFirstConsumer`가 중요합니다. EBS 볼륨은 **AZ 하나에 묶이므로**, Pod가 어느 AZ의 노드로 갈지 정해지기 전에 볼륨을 먼저 만들면 Pod가 다른 AZ로 갔을 때 붙일 수 없습니다(6교시 · 내일).

## 2 · AWS Load Balancer Controller

```bash
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system \
  --set clusterName=devmart --set region=ap-northeast-2 --set vpcId=$VPC_ID \
  --set serviceAccount.name=aws-load-balancer-controller
```

ServiceAccount 이름이 3교시 Pod Identity 연결의 이름과 **정확히 같아야** 권한을 받습니다.

## 3 · Envoy Gateway — NodePort에서 NLB로

```bash
diff ~/devops-lab/k8s/w4d1/gateway/envoyproxy.yaml envoyproxy-eks.yaml
```

```yaml
      envoyService:
        type: LoadBalancer
        annotations:
          service.beta.kubernetes.io/aws-load-balancer-type: external          # LBC가 맡는다
          service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing # public 서브넷에
          service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip     # Pod IP로 바로
```

바뀐 것은 **이 파일 하나**입니다. GatewayClass · Gateway · 차트 버전(v1.10.0)은 4주차 1일차 그대로입니다.

| 주석 | 뜻 |
|---|---|
| `type: external` | 이 Service의 로드 밸런서는 LBC가 만든다 (EKS 기본 컨트롤러가 아니라) |
| `scheme: internet-facing` | 2일차 ALB처럼 인터넷 경계 — 2교시에 태그한 **public 서브넷**에 |
| `nlb-target-type: ip` | NLB가 노드를 거치지 않고 **Envoy Pod IP로 바로** — VPC CNI 덕분에 Pod가 VPC IP를 가진다 |

## 4 · Argo CD

4주차 3일차의 `argocd-values.yaml` 그대로입니다. 차트 버전은 그날 적어 둔 `VERSIONS.txt`의 값을 씁니다.

## 실습 5 · 한 번에

```bash
export ARGOCD_CHART_VERSION=$(grep argo-cd ~/devops-lab/k8s/w4d3/VERSIONS.txt | tail -1 | awk '{print $NF}')
echo $ARGOCD_CHART_VERSION
./install.sh
```

!!! check "확인 (5~8분)"
    ```text
    == 1. 기본 StorageClass gp3
    storageclass.storage.k8s.io/gp3 created
    == 2. AWS Load Balancer Controller
    Release "aws-load-balancer-controller" does not exist. Installing it now.
    …
    == 3. Envoy Gateway (4주차 1일차와 같은 차트 · 버전)
    …
    gatewayclass.gateway.networking.k8s.io/eg created
    namespace/devmart created
    envoyproxy.gateway.envoyproxy.io/devmart-proxy created
    gateway.gateway.networking.k8s.io/devmart created
    == 4. Argo CD (4주차 3일차와 같은 values)
    …
    == 완료 — 다음: Secret devmart-db, Application
    ```

```bash
kubectl get storageclass
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-load-balancer-controller
kubectl get gateway -n devmart
kubectl get svc -n envoy-gateway-system -l gateway.envoyproxy.io/owning-gateway-name=devmart
```

!!! check "확인"
    ```text
    NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      …
    gp2             kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   …
    gp3 (default)   ebs.csi.aws.com         Delete          WaitForFirstConsumer   …
    aws-load-balancer-controller-7d9c8b6f5-k2m8p   1/1   Running
    aws-load-balancer-controller-7d9c8b6f5-x4q7w   1/1   Running
    NAME      CLASS   ADDRESS                                                                    PROGRAMMED   AGE
    devmart   eg      k8s-envoygat-envoydev-0a1b2c3d4e-0f1e2d3c4b5a6978.elb.ap-northeast-2.amazonaws.com   True   2m
    NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP                                         PORT(S)
    envoy-devmart-devmart-…    LoadBalancer   172.20.88.14    k8s-envoygat-envoydev-….elb.ap-northeast-2.amazonaws.com   80:31847/TCP
    ```
    Gateway의 ADDRESS가 **NLB의 DNS 이름**입니다. 4주차에는 이 칸이 비어 있었습니다(NodePort) — 이제 진짜 인터넷 주소가 생겼습니다. NLB가 '활성'이 되기까지 2~3분 걸립니다.

```bash
NLB=$(kubectl get gateway devmart -n devmart -o jsonpath='{.status.addresses[0].value}')
sleep 120; curl -s -o /dev/null -w '%{http_code}\n' http://$NLB/
```

!!! check "확인"
    `404` — **Envoy가 답했습니다.** 아직 HTTPRoute(앱)가 없어서 갈 곳이 없을 뿐입니다. 4주차 1일차에 Gateway만 만들었을 때와 같은 상태입니다.

!!! warn "이 NLB는 Terraform 장부에 없다"
    NLB는 **LBC가** 만들었으므로 `terraform state list`에 나오지 않습니다. 이것을 지우지 않고 `terraform destroy`하면, NLB가 public 서브넷을 붙잡고 있어 VPC 삭제가 **실패**하거나 NLB만 남아 계속 과금됩니다. 8교시에 **Kubernetes 쪽부터** 지우는 이유입니다.

!!! myth "오해 — Kubernetes Service 'LoadBalancer'면 어디서나 똑같다"
    `type: LoadBalancer`는 "**이 클러스터의 클라우드에게** 로드 밸런서를 만들어 달라"는 요청일 뿐입니다. kind에서는 아무도 받지 않아 영원히 `<pending>`이고, EKS에서는 LBC가 NLB를, GKE에서는 구글의 컨트롤러가 GCP 로드 밸런서를 만듭니다. 그래서 주석은 **클라우드마다** 다르고, 그것이 '플랫폼' 쪽에 있어야 합니다.

!!! academic "학술 노트 — 이식성의 층"
    Kubernetes가 클라우드 사이의 **이식성**을 준다는 주장은 '어느 층에서'를 따져야 합니다. Burns 외(2016)는 컨테이너 API가 앱을 인프라에서 떼어 낸다고 했지만, 스토리지 · 로드 밸런서 · 신원은 여전히 클라우드마다 다릅니다. Kubernetes는 이것을 **인터페이스**(CSI · Service LoadBalancer · Gateway API)와 **구현**(EBS CSI · LBC · Envoy Gateway)으로 나눠, 앱은 인터페이스에만 기대게 했습니다. 오늘 바뀐 것이 모두 구현 쪽이라는 것이 그 설계의 결과입니다.

!!! trend "트렌드 2026 — 플랫폼도 GitOps로"
    오늘 `install.sh`로 한 일을 실무에서는 Argo CD의 **app of apps**(4주차 3일차)나 ApplicationSet으로 둡니다 — 클러스터마다 "플랫폼 Application" 묶음을 Git에서 맞춥니다. EKS **Capabilities**(관리형 Argo CD · ACK)나 Auto Mode의 내장 로드 밸런서 · 스토리지를 쓰면 이 목록 자체가 줄어듭니다.

!!! quiz "확인 문제"
    1. gp3 StorageClass의 `WaitForFirstConsumer`가 필요한 이유는?
    2. EnvoyProxy에서 kind와 달라진 것과, 그대로인 것은?
    3. Gateway의 ADDRESS가 4주차와 달라진 이유는?
    4. NLB를 지우지 않고 terraform destroy하면 생기는 일은?

    ??? answer "정답"
        1. EBS는 AZ 하나에 묶여서, Pod가 갈 AZ가 정해진 뒤에 같은 AZ에 볼륨을 만들어야 붙일 수 있기 때문
        2. 달라진 것: envoyService type이 LoadBalancer + LBC 주석. 그대로: 차트 버전, GatewayClass, Gateway
        3. LBC가 Service(LoadBalancer)를 보고 NLB를 만들어 그 DNS 이름이 주소가 되었기 때문
        4. NLB가 Terraform 장부에 없어 남고(계속 과금), public 서브넷을 붙잡아 VPC 삭제가 실패할 수 있다

## 참고 문헌

- AWS Docs. *Route internet traffic with AWS Load Balancer Controller — Network Load Balancers*. docs.aws.amazon.com/eks
- AWS Docs. *Use Kubernetes volume storage with Amazon EBS (EBS CSI driver)*. docs.aws.amazon.com/eks
- Envoy Gateway Docs. *Customize EnvoyProxy — Service type and annotations*. gateway.envoyproxy.io
