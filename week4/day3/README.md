[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [3일차](README.md)

# 4주차 3일차 — GitOps

📕 4주차 이북 PDF: [보기](../../downloads/pdf/week4.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week4.pdf) &nbsp;|&nbsp; 📊 3일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day3.pptx)

## 오늘의 목표

어제 배움일기의 마지막 질문은 "런북 · 대시보드 · 규칙을 모두 Git에 올렸다. 그렇다면 **클러스터 자체도** Git에 있는 대로 맞춰지게 할 수는 없을까?"였습니다. 3주차 5일차에 우리는 `kubectl apply -k`로 DevMart를 올렸고, 장애 훈련에서는 `kubectl set env`로 손을 댔습니다. 그 손질은 **어디에도 기록되지 않았습니다.** 오늘은 Git을 **원하는 상태의 유일한 출처**로 만들고, 클러스터가 스스로 그것을 따라가게 합니다.

- **push 배포**와 **pull 배포(GitOps)**의 차이와, GitOps의 네 원칙을 이해합니다.
- 코드 저장소(`devops-lab`)와 **배포 저장소**(`devmart-deploy`)를 나누고, 오늘까지 만든 매니페스트를 배포 저장소에 모읍니다.
- **Argo CD**를 Helm으로 설치하고 웹 UI · CLI로 로그인합니다.
- **Application**을 만들어 DevMart를 Argo CD가 관리하게 하고, 손으로 **Sync**합니다.
- 누가 클러스터를 손으로 바꾸면 Argo CD가 **어긋남(drift)**을 어떻게 보여 주는지 봅니다.
- **selfHeal · prune**으로 자동 동기화를 켜고, 손 수정이 되돌려지는 것을 봅니다.
- **코드 PR → CI → 배포 저장소 커밋 → Argo CD → 클러스터**의 전체 흐름을 한 번에 돌리고, `git revert`로 되돌립니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 2일차 요약 + GitOps | push vs pull 비교표 |
| 2교시 | CI와 CD 나누기 · 배포 저장소 | `devmart-deploy` 저장소 |
| 3교시 | Argo CD 설치 | 웹 UI 로그인, `argocd` CLI |
| 4교시 | Application과 Sync | Argo CD가 관리하는 DevMart |
| 5교시 | Sync와 어긋남 | `argocd app diff`로 손 수정 찾기 |
| 6교시 | selfHeal과 prune | 스스로 되돌리는 클러스터 |
| 7교시 | Actions → Argo CD 전체 파이프라인 | PR 하나로 v2.1.0 배포 · revert로 되돌리기 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [2일차 요약 + GitOps](lesson-01.md)
2. [CI와 CD 나누기 · 배포 저장소](lesson-02.md)
3. [Argo CD 설치](lesson-03.md)
4. [Application과 Sync](lesson-04.md)
5. [Sync와 어긋남](lesson-05.md)
6. [selfHeal과 prune](lesson-06.md)
7. [Actions → Argo CD 전체 파이프라인](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 어제의 모니터링 도구 위에 Argo CD가 **약 0.5~1GB** 더 씁니다. 빠듯하면 `helm uninstall podinfo-canary -n default`로 자리를 만듭니다.
> - DevMart가 살아 있어야 합니다: `curl -s -o /dev/null -w '%{http_code}\n' localhost:30080/api/products` → `200`.
> - `gh auth status`로 GitHub 로그인이 되어 있어야 합니다(2주차 1일차). 오늘 **새 저장소 하나**와 **토큰 하나**를 만듭니다.
> - 3주차 2일차의 CI(`devmart-ci`)가 `devops-lab`에서 초록이어야 하고, GHCR 패키지 셋이 **공개(Public)**여야 합니다.
> - 실습 파일은 강의 저장소의 `labs/week4/day3/`입니다.

---

⬅️ 이전: [7교시 · 관찰 런북과 SLO](../day2/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 2일차 요약 + GitOps](lesson-01.md) ➡️
