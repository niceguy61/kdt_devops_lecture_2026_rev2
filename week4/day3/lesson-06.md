<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [3일차](README.md) › 6/8교시</sub>

# 6교시 · selfHeal과 prune

> [!NOTE]
> **이번 시간에 할 일**
>
> - **자동 동기화**를 켜고, 커밋이 사람 없이 반영되는 것을 봅니다.
> - **selfHeal** — 손 수정이 몇 초 만에 되돌려지는 것을 봅니다.
> - **prune** — Git에서 지운 리소스가 클러스터에서도 사라지는 것을 봅니다.
> - 자동화가 **방해가 되는 순간**(장애 대응, HPA)에 어떻게 하는지 익힙니다.

## 세 단계의 자동화

| 설정 | 새 커밋이 오면 | 누가 손으로 바꾸면 | Git에서 파일을 지우면 |
|---|---|---|---|
| (없음) — 4 · 5교시 | OutOfSync 표시만 | OutOfSync 표시만 | OutOfSync 표시만 |
| `automated: {}` | **자동 Sync** | 표시만 (다음 커밋 때 덮인다) | 클러스터에 **남는다** |
| `+ selfHeal: true` | 자동 Sync | **몇 초 안에 되돌린다** | 남는다 |
| `+ prune: true` | 자동 Sync | 되돌린다 | **클러스터에서도 지운다** |

```bash
cd ~/devops-lab/k8s/w4d3
diff argocd/devmart-app.yaml argocd/devmart-app-auto.yaml
```

> **🟢 확인: 확인**
>
> ```text
> 1c1
> < # 4교시 · 첫 Application — 손으로 Sync
> ---
> > # 6교시 · 자동 동기화 + 스스로 고치기 + 지운 것 정리
> …
> > syncPolicy:
> >   automated:
> >     prune: true        # Git에서 지운 리소스는 클러스터에서도 지운다
> >     selfHeal: true     # 누가 손으로 바꾸면 Git대로 되돌린다
> ```

> [!IMPORTANT]
> **prune이 기본으로 꺼져 있는 이유**
>
> Git에서 파일 하나를 실수로 지웠다고 운영 DB가 사라지면 안 됩니다. 그래서 Argo CD는 자동 동기화를 켜도 **지우는 일만은 따로 허락**받게 해 두었습니다. 켜기 전에 "Git에 없는 것은 클러스터에 있으면 안 된다"를 팀이 합의해야 합니다. 그 합의가 있으면 prune은 **쓰레기를 남기지 않는** 강력한 도구가 됩니다.

## 실습 13 · 자동 동기화 켜기

같은 이름(`devmart`)의 Application을 다시 apply하면 설정만 바뀝니다.

```bash
kubectl apply -f argocd/devmart-app-auto.yaml
argocd app get devmart | grep -E "Sync Policy|Sync Status|Health"
```

> **🟢 확인: 확인**
>
> ```text
> application.argoproj.io/devmart configured
> Sync Policy:        Automated (Prune)
> Sync Status:        Synced to main (2e6a8d3)
> Health Status:      Healthy
> ```

커밋 하나로 확인합니다. 이번에는 **Sync 명령을 치지 않습니다.**

```bash
cd ~/devmart-deploy
sed -i 's/replicas: 3/replicas: 2/' devmart/catalog-api.yaml      # Mac: sed -i ''
git commit -am "catalog-api 다시 2개로"
git push
kubectl get deploy catalog-api -n devmart -w
```

> **🟢 확인: 확인 (최대 1분)**
>
> ```text
> NAME          READY   UP-TO-DATE   AVAILABLE   AGE
> catalog-api   3/3     3            3           8d
> catalog-api   3/2     3            3           8d
> catalog-api   2/2     2            2           8d
> ```
> `Ctrl+C`로 멈춥니다. 사람이 한 일은 **커밋과 push뿐**입니다. 웹 UI의 **HISTORY AND ROLLBACK**에 방금 커밋이 한 줄 늘었습니다.

## 실습 14 · selfHeal — 손 수정이 되돌려진다

```bash
kubectl scale deploy/catalog-api -n devmart --replicas=5
kubectl get deploy catalog-api -n devmart -w
```

> **🟢 확인: 확인 (몇 초)**
>
> ```text
> deployment.apps/catalog-api scaled
> NAME          READY   UP-TO-DATE   AVAILABLE   AGE
> catalog-api   2/5     5            2           8d
> catalog-api   2/2     2            2           8d
> ```
> 5개로 늘었다가 Pod가 뜨기도 전에 **2개로 되돌아갑니다.** Argo CD는 리소스의 변화를 **지켜보고(watch)** 있다가, 바뀌자마자 Git과 비교해 되돌렸습니다. 60초 주기를 기다리지 않습니다.

더 과감하게 지워 봅니다.

```bash
kubectl delete deploy web -n devmart
sleep 10
kubectl get deploy web -n devmart
curl -s -o /dev/null -w '%{http_code}\n' localhost:30080/
```

> **🟢 확인: 확인**
>
> ```text
> deployment.apps "web" deleted
> NAME   READY   UP-TO-DATE   AVAILABLE   AGE
> web    1/1     1            1           8s
> 200
> ```
> AGE가 몇 초입니다 — **새로 만들어졌습니다.** 3주차 4일차에 Pod를 지우면 ReplicaSet이 다시 만들던 것과 같은 일이, 이제 **Deployment 단위**에서 일어납니다.

> [!WARNING]
> **selfHeal과 HPA가 싸운다**
>
> 3주차 5일차 7교시의 HPA(자동 늘리기)를 붙이면, HPA가 replicas를 5로 바꾸고 → selfHeal이 Git의 2로 되돌리고 → HPA가 다시 5로… 싸움이 납니다. 해결책은 둘입니다. ① Git의 Deployment에서 `replicas` 줄을 **지운다**(HPA에게 맡긴다), ② Application에 `ignoreDifferences`로 `/spec/replicas`를 **비교에서 뺀다.** 어느 필드를 **누가 소유하나**를 정하는 문제입니다(3교시 학술 노트).

## 실습 15 · prune — 지운 것은 사라진다

디버깅용 Pod를 Git으로 하나 넣었다가 Git에서 지워 봅니다.

```bash
cd ~/devmart-deploy
cat > devmart/debug.yaml <<'YAML'
# 잠깐 쓰는 디버깅 도구 — 다 쓰면 Git에서 지운다
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debug
spec:
  replicas: 1
  selector:
    matchLabels: { app: debug }
  template:
    metadata:
      labels: { app: debug }
    spec:
      containers:
        - name: curl
          image: curlimages/curl:8.17.0
          command: ["sleep", "infinity"]
          resources:
            requests: { cpu: 10m, memory: 16Mi }
            limits: { memory: 32Mi }
YAML
sed -i 's/^  - devmart-rules.yaml.*/&\n  - debug.yaml/' devmart/kustomization.yaml     # Mac: 편집기로 resources 끝에 한 줄
grep -A1 devmart-rules devmart/kustomization.yaml
git add . && git commit -m "디버깅용 curl 추가" && git push
sleep 60; kubectl get deploy debug -n devmart
kubectl exec -n devmart deploy/debug -- curl -s catalog-api:8000/api/products | head -c 80; echo
```

> **🟢 확인: 확인**
>
> ```text
>   - devmart-rules.yaml           # 4주차 2일차
>   - debug.yaml
> …
> NAME    READY   UP-TO-DATE   AVAILABLE   AGE
> debug   1/1     1            1           40s
> {"items":[{"id":1,"name":"러닝화","price":59000,"stock":12},{"id":2,"nam
> ```
> 클러스터 안에서 Service 이름(`catalog-api`)으로 부르는 3주차 4일차의 방법 그대로입니다.

이제 다 썼으니 **Git에서** 지웁니다.

```bash
git rm devmart/debug.yaml
sed -i '/  - debug.yaml/d' devmart/kustomization.yaml          # Mac: sed -i '' …
git commit -am "디버깅용 curl 제거"
git push
sleep 60; kubectl get deploy debug -n devmart
```

> **🟢 확인: 확인**
>
> ```text
> rm 'devmart/debug.yaml'
> …
> Error from server (NotFound): deployments.apps "debug" not found
> ```
> prune이 꺼져 있었다면 debug는 클러스터에 **계속 남고**, Argo CD 화면에 노란 휴지통 표시("requires pruning")만 떴을 것입니다. "잠깐 띄운 것"이 몇 달씩 남아 자원을 먹는 일이 운영에서 흔합니다.

### prune이 지우지 않는 것

```bash
kubectl get secret -n devmart
kubectl get gateway -n devmart
```

`devmart-db` Secret과 1일차의 `devmart` Gateway는 Git에 없는데도 **남아 있습니다.** 4교시에 본 **추적 표시**가 없기 때문입니다 — Argo CD는 "내가 만든 것"만 정리합니다. 반대로 말하면, 실수로 이것들을 배포 저장소에 넣었다가 지우면 **사라집니다.**

## 자동화를 잠시 끄는 법

장애 중에 원인을 찾으려고 일부러 손을 대야 할 때가 있습니다(3주차 5일차의 `kubectl set env`로 로그 수준 올리기 등). selfHeal이 켜져 있으면 몇 초 만에 되돌려집니다.

```bash
argocd app set devmart --sync-policy none          # 자동 동기화 끄기 (기록을 남긴다!)
# … 조사 …
kubectl apply -f ~/devops-lab/k8s/w4d3/argocd/devmart-app-auto.yaml   # 다시 켜기
```

> [!TIP]
> **런북에 적을 것**
>
> "자동 동기화를 껐다"는 사실 자체가 **장애 기록에 남아야** 합니다. 끈 채로 잊으면 그때부터 클러스터는 다시 push 시대로 돌아갑니다. 어제 만든 런북에 "끈 사람 · 시각 · 다시 켠 시각" 칸을 더해 둡니다. 또 자동 동기화가 켜진 Application은 `argocd app rollback`(이전 Sync로 되돌리기)이 **막혀 있습니다** — 되돌리기는 언제나 `git revert`입니다.

> **🎓 학술 노트 — 자율 컴퓨팅과 MAPE-K**
>
> 스스로 상태를 보고 고치는 시스템은 IBM이 2001년 제안한 **자율 컴퓨팅**(autonomic computing)의 목표였습니다. Kephart와 Chess의 *The Vision of Autonomic Computing*(IEEE Computer, 2003)은 이를 **MAPE-K 루프** — 감시(Monitor) · 분석(Analyze) · 계획(Plan) · 실행(Execute), 공유 지식(Knowledge) — 로 정리했습니다. selfHeal은 지식 = Git, 감시 = watch, 분석 = diff, 실행 = Sync인 가장 단순한 MAPE-K입니다. 같은 논문은 **자기 치유가 사람의 의도와 부딪칠 때**의 위험도 경고합니다 — 위의 HPA 싸움이 그 예입니다.

> **📈 트렌드 2026 — 정책으로 막는 GitOps**
>
> selfHeal은 "Git과 다르면 되돌린다"이지만, "Git에 **들어가면 안 되는 것**"은 막지 못합니다. 그래서 배포 저장소의 PR 단계에서 **정책 검사**(Kyverno CLI · Conftest)를 돌리고, 클러스터에서는 같은 정책을 **입장 제어**(admission)로 한 번 더 막는 이중 구조가 표준이 되었습니다. 5일차의 Kyverno에서 직접 해 봅니다.

> **✅ 확인 문제**
>
> 1. `automated`만 켜고 selfHeal을 끄면 손 수정은 어떻게 되나요?
> 2. prune이 기본으로 꺼져 있는 이유는?
> 3. selfHeal과 HPA의 싸움을 푸는 두 방법은?
> 4. Git에 없는 `devmart-db` Secret을 prune이 지우지 않는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 클러스터에 남아 OutOfSync로 표시되다가, 다음 커밋이 Sync될 때 덮인다
> 2. Git에서 실수로 파일을 지웠을 때 운영 리소스(데이터 포함)가 함께 사라지지 않게
> 3. Git의 Deployment에서 replicas를 지우거나, ignoreDifferences로 /spec/replicas를 비교에서 뺀다
> 4. Argo CD의 추적 표시가 없어 '내가 관리하는 것'이 아니기 때문
>
> </details>

## 참고 문헌

- Argo CD Docs. *Automated Sync Policy — Automatic Pruning, Automatic Self-Healing*. argo-cd.readthedocs.io
- Argo CD Docs. *Diffing Customization — ignoreDifferences*. argo-cd.readthedocs.io
- Kephart, J. O. & Chess, D. M. (2003). *The Vision of Autonomic Computing*. IEEE Computer 36(1).

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [5교시 · Sync와 어긋남](lesson-05.md) | [⬆️ 3일차 목차](README.md) | [7교시 · Actions → Argo CD 전체 파이프라인](lesson-07.md) ➡️ |
