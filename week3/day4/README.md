<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [4일차](README.md)</sub>

<img src="../../v3/assets/readme/week3.png" alt="3주차 노선도" width="100%">

# 3주차 4일차 — Pod · Deployment · Service

📕 3주차 이북 PDF: [보기](../../downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) &nbsp;|&nbsp; 📊 4일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day4.pptx)

## 오늘의 목표

어제는 클러스터를 만들고 들여다보기만 했습니다. 오늘은 그 위에 **내 앱**을 올립니다. 2일차에 GitHub Actions가 GHCR에 올려 둔 `devmart-catalog-api` 이미지를, 어제 만든 `devmart` 클러스터가 받아 갑니다.

Kubernetes에서 앱을 돌리는 데 꼭 필요한 리소스는 세 가지입니다. 오늘 그 셋을 차례로 만들고, 일부러 망가뜨리고, 고칩니다.

- **kubectl 루프** — 쓰기(apply) → 보기(get) → 읽기(describe) → 듣기(logs) → 고치기 — 를 손에 붙입니다.
- **Pod**를 직접 만들고, 접속하고, 지워 봅니다. Pod 혼자서는 되살아나지 않는다는 것을 확인합니다.
- 망가진 Pod의 상태 — `Pending` · `ImagePullBackOff` · `CrashLoopBackOff` — 를 보고 **어디를 봐야 할지** 압니다.
- **Deployment**로 Pod를 3개 띄우고, ReplicaSet과의 관계를 라벨로 따라갑니다.
- Pod를 지우고 노드를 꺼서 **자가 치유**를 봅니다.
- **Service**로 바뀌지 않는 이름을 붙이고, 클러스터 안 DNS와 브라우저(`localhost:30080`)로 부릅니다.
- 새 버전으로 **무중단 교체**하고, 잘못된 배포를 **되돌립니다**.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 3일차 요약 + kubectl 루프 | 이미지 주소 확인, 실습 파일 준비 |
| 2교시 | 첫 Pod | catalog-api Pod + port-forward |
| 3교시 | Pod 장애 읽기 | 장애 3종 진단 기록 |
| 4교시 | Deployment | catalog-api × 3 |
| 5교시 | ReplicaSet과 자가 치유 | 지우기 · 라벨 떼기 · 노드 끄기 관찰 기록 |
| 6교시 | Service와 DNS | 클러스터 안 호출 + 브라우저 `localhost:30080` |
| 7교시 | 롤링 업데이트와 되돌리기 | 무중단 교체 · 실패한 배포 되돌리기 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [3일차 요약 + kubectl 루프](lesson-01.md)
2. [첫 Pod](lesson-02.md)
3. [Pod 장애 읽기](lesson-03.md)
4. [Deployment](lesson-04.md)
5. [ReplicaSet과 자가 치유](lesson-05.md)
6. [Service와 DNS](lesson-06.md)
7. [롤링 업데이트와 되돌리기](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 어제 만든 클러스터가 살아 있어야 합니다: `kubectl get nodes`에서 세 노드가 `Ready`. 아니면 3일차 7교시 마지막 절대로 다시 만듭니다.
> - 2일차에 GHCR의 세 패키지를 **Public**으로 바꿔 두었어야 합니다. 클러스터는 로그인 없이 이미지를 받습니다.
> - 오늘 처음 받는 이미지는 `busybox:1.37`(수 MB) 하나입니다. 클러스터 안에서 다른 Pod를 불러 볼 때 씁니다.
> - 실습 파일은 강의 저장소의 `labs/week3/day4/`입니다.

> [!WARNING]
> **오늘의 공통 주의 — 지금 어느 클러스터인가**
>
> 오늘부터 kubectl로 **상태를 바꾸는** 명령(apply · delete · scale)을 많이 칩니다. 회사에서 같은 명령을 운영 클러스터에 잘못 치면 사고입니다. 습관으로 만들기 위해, 바꾸는 명령 전에 프롬프트나 `kubectl config current-context`로 **`kind-devmart`인지** 확인합니다. 이 주의는 교시마다 반복하지 않습니다.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 첫 클러스터 — 둘러보고, 지우고, 끄기](../day3/lesson-07.md) | [⬆️ 3주차 목차](../README.md) | [1교시 · 3일차 요약 + kubectl 루프](lesson-01.md) ➡️ |
