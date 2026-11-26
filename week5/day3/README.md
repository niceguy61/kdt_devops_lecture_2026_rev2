[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [3일차](README.md)

# 5주차 3일차 — Terraform 기초

📕 5주차 이북 PDF: [보기](../../downloads/pdf/week5.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week5.pdf) &nbsp;|&nbsp; 📊 3일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day3.pptx)

## 오늘의 목표

어제 배움일기의 마지막 질문은 "클릭 백 번을 **코드로 적어 두고**, 한 줄로 만들고 한 줄로 지울 수는 없을까? 그 코드가 실제 계정과 **어긋나면** 어떻게 알까?"였습니다. 오늘 그 답은 **Terraform**입니다. 3주차에 `kubectl run` 대신 YAML을 쓰기 시작한 것, 4주차에 Git을 원하는 상태로 삼은 것을 이번에는 **AWS 자원**에 합니다.

- **IaC**(코드로 인프라)와 Terraform의 작업 흐름 — init · plan · apply · destroy — 를 익힙니다.
- 변수 · locals · 데이터 소스 · `for_each` · 자원 사이의 **참조**로 코드를 씁니다.
- **state**가 무엇인지, 콘솔에서 손댄 **어긋남**을 plan이 어떻게 잡는지, 콘솔 자원을 **import**하는 법을 봅니다.
- state를 **S3에 두고 잠금**을 겁니다.
- **모듈**로 1일차의 VPC를 코드 몇십 줄로 다시 만들고, 콘솔 VPC는 지웁니다.
- GitHub Actions가 **키 없이(OIDC)** 역할을 맡아 PR마다 plan을 돌리게 합니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 2일차 요약 + 코드로 인프라 | 콘솔 · CLI · IaC 비교표 |
| 2교시 | 설치와 첫 리소스 | S3 버킷 하나를 만들고 지우기 |
| 3교시 | HCL — 변수 · 참조 · for_each | 버킷 둘 + 설정 + 파일, 의존 그래프 |
| 4교시 | state · 어긋남 · import | 콘솔 수정을 plan이 잡는다 |
| 5교시 | 원격 state와 잠금 | `devmart-tfstate-…` 버킷, 잠금 충돌 |
| 6교시 | 모듈로 VPC | `devmart-tf` VPC, 콘솔 VPC 정리 |
| 7교시 | GitHub Actions에서 plan (OIDC) | `devmart-infra` 저장소, PR의 plan 요약 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [2일차 요약 + 코드로 인프라](lesson-01.md)
2. [설치와 첫 리소스](lesson-02.md)
3. [HCL — 변수 · 참조 · for_each](lesson-03.md)
4. [state · 어긋남 · import](lesson-04.md)
5. [원격 state와 잠금](lesson-05.md)
6. [모듈로 VPC](lesson-06.md)
7. [GitHub Actions에서 plan (OIDC)](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - `aws login` → `aws sts get-caller-identity`가 `user/devops-admin`.
> - 어제 지운 것이 남지 않았는지: `~/devops-lab/aws/w5d1/check-account.sh | tail -4`.
> - 오늘 만드는 것은 S3 · VPC · IAM · 보안 그룹 — **모두 무료**(S3 사용량은 거의 0)입니다. 그래도 7교시에 정리합니다.
> - 실습 파일은 강의 저장소의 `labs/week5/day3/`입니다.

---

⬅️ 이전: [7교시 · 지우는 순서 + 비용 점검](../day2/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 2일차 요약 + 코드로 인프라](lesson-01.md) ➡️
