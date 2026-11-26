[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [3일차](README.md)

# 3주차 3일차 — Kubernetes 아키텍처

📕 3주차 이북 PDF: [보기](../../downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) &nbsp;|&nbsp; 📊 3일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day3.pptx)

## 오늘의 목표

어제 배움일기의 마지막 질문은 "처리기가 죽으면 **누가** 다시 띄워 줄까? 컴퓨터가 여러 대라면?"이었습니다. Compose의 `restart:`는 같은 컴퓨터 안에서 다시 띄우는 것까지만 합니다. 컴퓨터가 통째로 꺼지면, 여러 대 중 어디에 띄울지 정해야 하면, 개수를 늘렸다 줄였다 해야 하면 — 사람이 해야 합니다. 이 일을 대신하는 것이 **Kubernetes**입니다.

오늘은 Kubernetes를 **쓰기 전에 이해하는 날**입니다. 오전에는 구조와 동작 원리를, 오후에는 내 노트북에 클러스터를 직접 만들고 구석구석 들여다봅니다. 앱 배포(Pod · Deployment · Service)는 내일 합니다.

- Kubernetes가 왜 나왔는지, Compose와 무엇이 다른지 설명합니다.
- **컨트롤 플레인** 네 부품(apiserver · etcd · scheduler · controller-manager)의 역할을 구분합니다.
- **노드**의 kubelet · 컨테이너 런타임 · kube-proxy가 하는 일과 **Pod**의 뜻을 이해합니다.
- **선언형**과 **reconcile(조정) 반복**이 무엇인지, 왜 Kubernetes의 핵심인지 이해합니다.
- Kubernetes를 쓰지 말아야 할 때와 다른 선택지를 압니다.
- `kubectl`과 `kind`를 설치하고, 노드 세 대짜리 클러스터를 만듭니다.
- 클러스터의 부품을 눈으로 확인하고, 일부러 지우고 끄면서 **스스로 되돌아오는 것**을 봅니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 2일차 요약 + 왜 Kubernetes인가 | Compose로 안 되는 일 목록 |
| 2교시 | 컨트롤 플레인 — 결정하고 기록하는 본부 | 부품 네 개 역할 카드 |
| 3교시 | 노드와 Pod — 실제로 돌리는 현장 | Pod가 뜨기까지 6단계 |
| 4교시 | 선언형과 reconcile | 명령형 vs 선언형 비교 |
| 5교시 | 장단점과 선택지 | "우리 팀에 Kubernetes가 필요한가" 판단표 |
| 6교시 | kubectl과 kind 설치 | `kubectl version` · `kind version` |
| 7교시 | 첫 클러스터 — 둘러보고, 지우고, 끄기 | 노드 3대 클러스터 + 관찰 기록 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [왜 Kubernetes인가](lesson-01.md)
2. [컨트롤 플레인](lesson-02.md)
3. [노드와 Pod](lesson-03.md)
4. [선언형과 reconcile](lesson-04.md)
5. [장단점과 선택지](lesson-05.md)
6. [kubectl과 kind 설치](lesson-06.md)
7. [첫 클러스터](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - **Docker Desktop이 켜져 있어야** 합니다. 메모리는 **4GB 이상**을 권합니다(노드 세 대 + 내일 DevMart). Docker Desktop → Settings → Resources에서 확인합니다. WSL2 연동을 쓰는 Windows는 WSL이 쓰는 메모리 한도(기본: PC 메모리의 절반)가 적용됩니다.
> - 2일차 DevMart MSA를 내려 둡니다: `cd ~/devops-lab/devmart-msa && docker compose down`. 메모리를 비우고, 오후에 쓸 **30080 포트**와 겹치지 않게 합니다.
> - 오늘 처음 받는 이미지는 `kindest/node:v1.37.0` 하나입니다(압축 약 360MB, 풀면 1GB 안팎). 강의장 네트워크가 느리면 점심시간에 미리 받습니다: `docker pull kindest/node:v1.37.0`
> - 실습 파일은 강의 저장소의 `labs/week3/day3/`입니다.

> [!WARNING]
> **오늘의 공통 주의 — 클러스터는 지우지 않는다**
>
> 오늘 만드는 `devmart` 클러스터는 **내일과 모레 계속 씁니다**. 수업이 끝나도 지우지 않습니다. 노트북을 재부팅하면 Docker Desktop을 켠 뒤 `docker start devmart-control-plane devmart-worker devmart-worker2`로 노드를 다시 켭니다. 그래도 `kubectl get nodes`가 실패하면 지우고 새로 만드는 편이 빠릅니다(7교시 마지막 절).

---

⬅️ 이전: [7교시 · CI 실패 읽기와 main 보호](../day2/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 왜 Kubernetes인가](lesson-01.md) ➡️
