# 5교시 · Sync와 어긋남

!!! goal "이번 시간에 할 일"
    - **Git이 바뀐 경우**: 커밋 → OutOfSync → diff → Sync의 흐름을 따라갑니다.
    - **클러스터가 바뀐 경우**: 손 수정이 어떻게 어긋남으로 보이는지 봅니다.
    - **Git이 틀린 경우**: Synced인데 Degraded가 되는 상황을 만들고 `git revert`로 되돌립니다.
    - 어긋남을 만났을 때 **어느 쪽이 맞는지** 정하는 기준을 세웁니다.

어긋남은 세 방향에서 옵니다. 하나씩 만들어 봅니다. 웹 UI의 devmart 화면을 옆에 띄워 둡니다.

| | 바뀐 곳 | Sync | Health | 실습 |
|---|---|---|---|---|
| A | Git (새 커밋) | OutOfSync | Healthy | 10 |
| B | 클러스터 (손 수정) | OutOfSync | Healthy | 11 |
| C | Git (틀린 커밋) | Synced | Progressing → Degraded | 12 |

## 실습 10 · Git이 바뀐 경우

catalog-api를 2개에서 3개로 늘립니다. **파일을 고치고, 커밋하고, push**합니다.

```bash
cd ~/devmart-deploy
grep -n "replicas" devmart/catalog-api.yaml
sed -i 's/replicas: 2/replicas: 3/' devmart/catalog-api.yaml      # Mac: sed -i ''
git diff
git commit -am "catalog-api 3개로 (부하 대비)"
git push
```

이제 Argo CD가 알아챌 때까지 기다립니다 — 최대 60초(3교시의 `timeout.reconciliation`). 기다리지 않으려면 **새로 고침**을 요청합니다.

```bash
argocd app get devmart --refresh | head -12
argocd app diff devmart
```

!!! check "확인"
    ```text
    Sync Status:        OutOfSync from main (9c3e1d7)
    Health Status:      Healthy
    …
    ===== apps/Deployment devmart/catalog-api ======
    163c163
    <   replicas: 2
    ---
    >   replicas: 3
    ```
    `<`가 지금 클러스터, `>`가 Git입니다. `from main (9c3e1d7)`의 해시는 방금 push한 커밋입니다 — `git log --oneline -1`과 같아야 합니다.

**아직 클러스터는 2개입니다.** syncPolicy가 없으니 Argo CD는 차이를 **보여 주기만** 합니다.

```bash
kubectl get deploy catalog-api -n devmart
argocd app sync devmart
kubectl get deploy catalog-api -n devmart
```

!!! check "확인"
    ```text
    NAME          READY   UP-TO-DATE   AVAILABLE   AGE
    catalog-api   2/2     2            2           8d
    …
    Phase:              Succeeded
    …
    NAME          READY   UP-TO-DATE   AVAILABLE   AGE
    catalog-api   3/3     3            3           8d
    ```

!!! key "운영 변경의 새 길"
    3주차에는 `kubectl scale`이었습니다. 이제는 **커밋 → (리뷰) → Sync**입니다. 느려 보이지만, 이 변경에는 **누가 · 언제 · 왜**("부하 대비")가 남습니다. `git log devmart/catalog-api.yaml`이 곧 catalog-api의 운영 이력입니다.

## 실습 11 · 클러스터가 바뀐 경우

3주차 5일차의 장애 훈련 3번을 다시 꺼냅니다 — 누군가 급하게 큐 이름을 바꿨습니다.

```bash
kubectl set env deploy/order-worker -n devmart QUEUE_NAME=order
kubectl rollout status deploy/order-worker -n devmart
argocd app get devmart --refresh | head -12
argocd app diff devmart
```

!!! check "확인"
    ```text
    deployment "order-worker" successfully rolled out
    Sync Status:        OutOfSync from main (9c3e1d7)
    Health Status:      Healthy
    …
    ===== apps/Deployment devmart/order-worker ======
    …
    <         - name: QUEUE_NAME
    <           value: order
    ```
    `<` 쪽에만 있습니다 — **클러스터에만 있고 Git에는 없는 값**입니다.

!!! warn "Healthy인데 고장 났다"
    order-worker는 떠 있고 준비도 되었으니 Argo CD는 **Healthy**라고 합니다. 하지만 엉뚱한 큐를 보고 있어서 주문이 처리되지 않습니다(3주차 5일차). Argo CD의 Health는 "**Kubernetes가 보기에** 잘 떠 있나"까지입니다. "**손님이 보기에** 잘 되나"는 어제의 대시보드와 알림이 답합니다 — 두 도구는 서로를 대신하지 않습니다.

이제 **어느 쪽이 맞나**를 정해야 합니다.

| 판단 | 행동 |
|---|---|
| Git이 맞다 (손 수정이 실수) | **Sync** — 클러스터를 Git대로 되돌린다 |
| 클러스터가 맞다 (급한 수정이 옳았다) | 같은 내용을 **Git에 PR**로 올린다 → 합쳐지면 다시 Synced |
| 모르겠다 | 손 수정한 사람에게 묻는다 — Git에는 기록이 없으니 사람이 기억해야 한다. 그래서 손 수정이 위험하다 |

이번에는 손 수정이 실수입니다. 웹 UI에서 **APP DIFF**를 눌러 같은 차이를 화면으로도 본 뒤, Sync합니다.

```bash
argocd app sync devmart
kubectl get deploy order-worker -n devmart -o jsonpath='{.spec.template.spec.containers[0].env[*].name}'; echo
```

!!! check "확인"
    `QUEUE_NAME`이 목록에 **없습니다.** 3주차에는 `fix.sh`가 하던 일(`set env QUEUE_NAME-`)을 Argo CD가 했습니다 — 무엇을 지워야 하는지를 **Git과 비교해서** 스스로 알아냈습니다.

## 실습 12 · Git이 틀린 경우

이번에는 Git에 **존재하지 않는 이미지 태그**를 넣습니다. catalog-api 한 줄만 바꿉니다.

```bash
cd ~/devmart-deploy
sed -i '/devmart-catalog-api/{n;s/newTag: .*/newTag: sha-0000000/;}' devmart/kustomization.yaml   # Mac: sed -i '' …
git diff
git commit -am "catalog-api 새 버전 (일부러 틀린 태그)"
git push
argocd app sync devmart --async
sleep 30
argocd app get devmart | head -12
kubectl get pods -n devmart -l app=catalog-api
```

!!! check "확인"
    ```text
    -    newTag: sha-7c1e9a2
    +    newTag: sha-0000000
    …
    Sync Status:        Synced to main (b81f0e4)
    Health Status:      Progressing
    …
    NAME                           READY   STATUS             RESTARTS   AGE
    catalog-api-5d8c7b9f6-2xkq4    1/1     Running            0          3h
    catalog-api-5d8c7b9f6-8wm3p    1/1     Running            0          3h
    catalog-api-5d8c7b9f6-r7t2n    1/1     Running            0          40m
    catalog-api-7f9b6c4d8-p5v9x    0/1     ImagePullBackOff   0          30s
    ```
    - **Synced** — Git대로 했습니다. Argo CD는 Git을 의심하지 않습니다.
    - **Progressing** — 새 Pod가 준비되지 않아 롤아웃이 끝나지 않았습니다. Deployment의 `progressDeadlineSeconds`(기본 600초)가 지나면 **Degraded**로 바뀝니다.
    - 옛 Pod 3개는 **그대로 손님을 받습니다** — 3주차 4일차의 롤링 업데이트가 새 Pod가 준비될 때까지 옛 것을 남겨 두기 때문입니다. `curl localhost:30080/api/products` → `200`.

### 되돌리기 — git revert

배포가 커밋이니, 되돌리기도 커밋입니다.

```bash
git log --oneline -3
git revert --no-edit HEAD
git push
argocd app sync devmart
argocd app get devmart | head -12
kubectl get pods -n devmart -l app=catalog-api
```

!!! check "확인"
    ```text
    b81f0e4 (HEAD -> main, origin/main) catalog-api 새 버전 (일부러 틀린 태그)
    9c3e1d7 catalog-api 3개로 (부하 대비)
    4f2a9c1 DevMart 매니페스트 첫 커밋 (…)
    [main 2e6a8d3] Revert "catalog-api 새 버전 (일부러 틀린 태그)"
    …
    Sync Status:        Synced to main (2e6a8d3)
    Health Status:      Healthy
    …
    catalog-api-5d8c7b9f6-2xkq4    1/1     Running   0          3h
    catalog-api-5d8c7b9f6-8wm3p    1/1     Running   0          3h
    catalog-api-5d8c7b9f6-r7t2n    1/1     Running   0          42m
    ```
    망가진 Pod는 사라지고 옛 Pod가 그대로 남았습니다. 이력에는 **틀린 배포와 그것을 되돌린 사실이 둘 다** 남습니다.

!!! key "왜 reset이 아니라 revert인가"
    `git reset --hard HEAD~1` 후 강제 push(`--force`)를 해도 클러스터는 돌아옵니다. 하지만 **이력이 지워집니다** — 장애 보고서(3주차 5일차)에 "몇 시에 무엇이 배포됐다"를 쓸 근거가 사라지고, 같은 커밋을 받아 둔 동료의 저장소와 어긋납니다. GitOps 원칙 2(**불변**)를 지키는 되돌리기는 revert입니다.

!!! myth "오해 — Argo CD가 망가진 배포를 막아 준다"
    Argo CD는 Git을 **충실히** 따를 뿐입니다. 틀린 태그를 막는 것은 그 앞 단계의 일입니다 — CI가 **실제로 올린 태그만** 커밋하게 하고(7교시), 배포 저장소에도 PR 리뷰를 두는 것. 새 버전을 조금씩 내보내다 이상하면 **자동으로 멈추는** 것은 Argo Rollouts 같은 도구의 몫입니다(아래 트렌드).

!!! academic "학술 노트 — 구성 표류의 비용"
    운영 사고의 원인을 조사한 연구들은 꾸준히 **설정 변경**을 큰 몫으로 꼽습니다. Oppenheimer 외의 *Why do Internet services fail, and what can be done about it?*(USITS 2003)는 대형 인터넷 서비스 장애에서 **운영자의 설정 실수**가 가장 큰 원인이었음을 보였고, Yin 외의 *An Empirical Study on Configuration Errors*(SOSP 2011)는 설정 오류의 상당수가 "**잘못된 값**"보다 "**환경 간 불일치**"에서 온다고 보고했습니다. 어긋남을 계속 보여 주는 도구는 이 불일치를 **사고가 되기 전에** 드러냅니다.

!!! trend "트렌드 2026 — 점진적 배포와 자동 중단"
    Argo 프로젝트의 **Argo Rollouts**는 Deployment 대신 Rollout 리소스를 써서 카나리(1일차의 80/20)를 **단계별로 자동 진행**하고, 각 단계에서 **Prometheus 쿼리**(어제의 오류율)를 확인해 기준을 넘으면 스스로 되돌립니다. "배포는 Git으로, 안전장치는 지표로"가 결합된 형태입니다. Flux 쪽에서는 Flagger가 같은 일을 합니다.

!!! quiz "확인 문제"
    1. `argocd app diff`에서 `<`와 `>`는 각각 무엇인가요?
    2. 손 수정이 옳았다면 어떻게 해야 하나요?
    3. 틀린 태그를 배포했는데 서비스가 끊기지 않은 이유는?
    4. 되돌리기에 `git reset --hard`와 강제 push를 쓰지 않는 이유는?

    ??? answer "정답"
        1. `<` — 지금 클러스터, `>` — Git (원하는 상태)
        2. 같은 내용을 Git에 PR로 올려 원하는 상태를 고친다
        3. 롤링 업데이트가 새 Pod가 준비될 때까지 옛 Pod를 남겨 두었기 때문
        4. 이력이 지워져 장애 기록의 근거가 사라지고, 다른 사람의 저장소와 어긋나기 때문 (불변 원칙)

## 참고 문헌

- Argo CD Docs. *Diffing*, *Sync Options*, *Automated Sync Policy*. argo-cd.readthedocs.io
- Oppenheimer, D., Ganapathi, A. & Patterson, D. (2003). *Why do Internet services fail, and what can be done about it?* USITS '03.
- Yin, Z. 외 (2011). *An Empirical Study on Configuration Errors in Commercial and Open Source Systems*. SOSP '11.
- Argo Rollouts Docs. *Analysis & Progressive Delivery*. argoproj.github.io/argo-rollouts
