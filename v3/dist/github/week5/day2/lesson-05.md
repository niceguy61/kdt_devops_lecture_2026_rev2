# 5교시 · 대상 그룹과 ALB

> [!NOTE]
> **이번 시간에 할 일**
>
> - ALB · 리스너 · 대상 그룹 · 상태 검사의 관계를 이해합니다.
> - **대상 그룹**과 **ALB**를 만들고, Auto Scaling 그룹에 붙입니다.
> - 주소 하나로 두 서버에 **번갈아** 닿는 것을 확인합니다.
> - 4주차 1일차의 Gateway API와 짝지어 둡니다.

## 네 부품

| 부품 | 하는 일 | 4주차 1일차에서 |
|---|---|---|
| **로드 밸런서 (ALB)** | 인터넷 주소 하나, public 서브넷 둘에 걸친다 | Gateway (입구) |
| **리스너** | "80번 포트로 오면" | Gateway의 listener |
| **규칙** | "경로가 /api면 저 대상 그룹으로" (오늘은 기본 하나) | HTTPRoute의 rules |
| **대상 그룹** | 보낼 서버 목록 + **상태 검사** | Service + readiness |

ALB는 L7(HTTP)을 봅니다 — Host · 경로 · 헤더로 나눌 수 있습니다. L4(TCP)만 보고 아주 빠르게 넘기는 것은 **NLB**입니다. 4일차 EKS에서는 Envoy Gateway 앞에 NLB를 둡니다.

## 실습 9 · 대상 그룹

EC2 → **대상 그룹** → **대상 그룹 생성**

| 칸 | 값 |
|---|---|
| 대상 유형 | **인스턴스** |
| 이름 | `devmart-tg` |
| 프로토콜 · 포트 | HTTP · **9898** |
| VPC | `devmart-vpc` |
| 상태 검사 경로 | `/healthz` (podinfo의 생존 검사 주소) |
| 고급 상태 검사 | 정상 임계값 **2**, 비정상 임계값 **2**, 간격 **10**초 |

다음 → **대상 등록은 하지 않고** → **대상 그룹 생성**. 등록은 Auto Scaling 그룹이 합니다.

## 실습 10 · ALB

EC2 → **로드 밸런서** → **로드 밸런서 생성** → **Application Load Balancer** 생성

| 칸 | 값 |
|---|---|
| 이름 | `devmart-alb` |
| 체계 | **인터넷 경계** (internet-facing) |
| IP 주소 유형 | IPv4 |
| VPC | `devmart-vpc` |
| 매핑 | `ap-northeast-2a` → `…public1…`, `ap-northeast-2c` → `…public2…` |
| 보안 그룹 | `default`를 **빼고** `devmart-web-sg` |
| 리스너 | HTTP : 80 → 기본 작업 **devmart-tg로 전달** |

**로드 밸런서 생성** — 상태가 **프로비저닝 중** → **활성**까지 2~3분.

## 실습 11 · 그룹에 붙이기

EC2 → Auto Scaling 그룹 → `devmart-asg` → **세부 정보** 탭 → **로드 밸런싱** 편집

1. **로드 밸런서 대상 그룹** → `devmart-tg` 선택 → 업데이트
2. 같은 탭의 **상태 확인** 편집 → **Elastic Load Balancing 상태 확인 켜기** 체크, 상태 확인 유예 기간 **60**초 → 업데이트

```bash
TG=$(aws elbv2 describe-target-groups --names devmart-tg --query 'TargetGroups[0].TargetGroupArn' --output text)
sleep 60
aws elbv2 describe-target-health --target-group-arn $TG --query 'TargetHealthDescriptions[].[Target.Id,TargetHealth.State]' --output text
DNS=$(aws elbv2 describe-load-balancers --names devmart-alb --query 'LoadBalancers[0].DNSName' --output text); echo $DNS
for i in $(seq 6); do curl -s http://$DNS/ | grep -o '"hostname": "[^"]*"'; done
```

> **🟢 확인: 확인**
>
> ```text
> i-0b2c3d4e5f6071829   healthy
> i-0c3d4e5f607182930   healthy
> devmart-alb-1234567890.ap-northeast-2.elb.amazonaws.com
> "hostname": "a1b2c3d4e5f6"
> "hostname": "f6e5d4c3b2a1"
> "hostname": "a1b2c3d4e5f6"
> …
> ```
> hostname이 **두 가지**로 번갈아 나옵니다 — 서로 다른 서버(의 컨테이너)가 답했습니다. 브라우저로 `http://<DNS>`를 열면 podinfo 화면에 "DevMart on EC2"가 보이고, 새로 고칠 때마다 hostname이 바뀝니다.

> [!IMPORTANT]
> **왜 이제는 닿나**
>
> 2교시에 내 노트북 → 서버 9898은 막혔습니다. 지금은 내 노트북 → **ALB**(web-sg: 80 허가) → 서버(app-sg: **web-sg에서 오는** 9898 허가)입니다. 서버는 여전히 인터넷에서 직접은 닿지 않고, **입구는 ALB 하나**입니다. 4주차 4일차에 "남북은 입구에서"라고 한 것이 AWS 네트워크에서도 같습니다.

## Gateway API와 나란히

| 4주차 1일차 (kind) | 오늘 (AWS 콘솔) |
|---|---|
| `Gateway` — listener :80 | ALB — 리스너 :80 |
| `HTTPRoute` — path → backendRef | 리스너 규칙 — 경로 → 대상 그룹 |
| `Service` + Endpoints | 대상 그룹 + 등록된 인스턴스 |
| readiness probe | 대상 그룹 상태 검사 `/healthz` |
| YAML 몇 줄 | 화면 셋 · 클릭 서른 번 |

4일차에 EKS에서는 다시 **YAML**(HTTPRoute)로 돌아갑니다. 그 HTTPRoute 앞에 AWS 로드 밸런서를 **Kubernetes가 대신 만들어** 줍니다.

> **❓ 오해 — 로드 밸런서는 트래픽을 나누기만 한다**
>
> ALB의 더 중요한 일은 **건강하지 않은 서버를 빼는 것**과 **입구를 하나로 만드는 것**입니다. 서버가 바뀌어도(6교시) 손님이 아는 주소는 그대로입니다. 그리고 TLS 인증서(HTTPS)를 ALB에서 끝내면 서버마다 인증서를 둘 필요가 없습니다 — 4주차 3일차 Argo CD의 `server.insecure` 설명과 같은 구조입니다.

> **🎓 학술 노트 — 부하 분산 알고리즘**
>
> ALB의 기본 알고리즘은 **라운드 로빈**이고, '처리 중인 요청이 가장 적은 곳'(least outstanding requests)도 고를 수 있습니다. Mitzenmacher의 *The Power of Two Choices in Randomized Load Balancing*(IEEE TPDS, 2001)은 무작위로 **둘만 골라 덜 바쁜 쪽**에 보내도 최대 부하가 지수적으로 줄어든다는 것을 보였고, Envoy · NGINX 등 많은 프록시가 이 방법을 씁니다. 4주차의 Envoy Gateway도 그 계열입니다.

> **📈 트렌드 2026 — 로드 밸런서도 Gateway API로**
>
> AWS Load Balancer Controller는 Kubernetes의 Gateway API 리소스(Gateway · HTTPRoute)를 읽어 **ALB · NLB를 직접 만드는** 기능을 정식으로 지원하기 시작했고, Amazon VPC Lattice도 Gateway API로 설정할 수 있습니다. 오늘 클릭한 화면 셋이 결국 4주차의 YAML로 표현되는 셈입니다.

> **✅ 확인 문제**
>
> 1. ALB의 네 부품과 각각 Gateway API의 무엇에 해당하나요?
> 2. 대상 그룹에 서버를 손으로 등록하지 않은 이유는?
> 3. 내 노트북에서 서버 9898로는 안 되고 ALB로는 되는 이유는?
> 4. ASG에 'ELB 상태 확인'을 켠 효과는? (6교시에 확인)
>
> <details><summary>정답</summary>
>
> 1. 로드 밸런서 = Gateway, 리스너 = listener, 규칙 = HTTPRoute rules, 대상 그룹 = Service(+readiness)
> 2. Auto Scaling 그룹이 만든 서버를 자동으로 등록 · 해제하게 하려고
> 3. app-sg가 9898을 web-sg(ALB)에서 오는 것만 허가하기 때문
> 4. 앱이 응답하지 않는 서버(EC2는 살아 있어도)를 그룹이 교체한다
>
> </details>

## 참고 문헌

- AWS Docs. *Application Load Balancers — listeners, target groups, health checks*. docs.aws.amazon.com/elasticloadbalancing
- AWS Docs. *Attach a load balancer to your Auto Scaling group*, *Health checks for instances in an Auto Scaling group*. docs.aws.amazon.com/autoscaling
- Mitzenmacher, M. (2001). *The Power of Two Choices in Randomized Load Balancing*. IEEE TPDS 12(10).
