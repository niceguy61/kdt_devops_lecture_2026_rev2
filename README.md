# Cloud Native DevOps 기초 과정 (5주 · 200시간)

서버와 클라우드의 기초부터 Docker, Kubernetes, GitOps, AWS · Terraform · EKS까지 — **작은 쇼핑몰 DevMart 하나**를 5주 동안 내 노트북에서 클라우드까지 옮기며 배웁니다.

## 시작하기

1. 아래 **과정 목차**에서 1주차 1일차부터 엽니다. 모든 페이지 맨 아래에 **⬅️ 이전 · 다음 ➡️** 링크가 있어 그대로 따라가면 순서대로 읽힙니다.
2. 도구 설치는 해당 교시에 나옵니다. OS별(Windows PowerShell · WSL · macOS) 설치 방법을 한곳에 모은 것은 [부록 A · 도구 설치 가이드](appendix/install.md)입니다.
3. 3주차부터는 실습 파일을 이 저장소에서 복사해 씁니다(3주차 1일차 4교시).

```bash
cd ~
git clone https://github.com/niceguy61/kdt_devops_lecture_2026_rev2.git course
ls ~/course/labs        # week2 … week5 실습 파일
```

## 내려받기

| 주차 | 이북 PDF | 슬라이드 PPTX (일차별) |
|---|---|---|
| [1주차 · 클라우드·컴퓨팅 기초 이론](week1/README.md) | [보기](downloads/pdf/week1.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week1.pdf) | [1일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week1-day1.pptx) · [2일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week1-day2.pptx) · [3일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week1-day3.pptx) · [4일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week1-day4.pptx) · [5일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week1-day5.pptx) |
| [2주차 · Docker + Git 첫 실습](week2/README.md) | [보기](downloads/pdf/week2.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week2.pdf) | [1일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day1.pptx) · [2일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day2.pptx) · [3일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day3.pptx) · [4일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day4.pptx) · [5일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day5.pptx) |
| [3주차 · MSA + Kubernetes 입문](week3/README.md) | [보기](downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) | [1일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day1.pptx) · [2일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day2.pptx) · [3일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day3.pptx) · [4일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day4.pptx) · [5일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day5.pptx) |
| [4주차 · Kubernetes 운영](week4/README.md) | [보기](downloads/pdf/week4.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week4.pdf) | [1일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day1.pptx) · [2일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day2.pptx) · [3일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day3.pptx) · [4일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day4.pptx) · [5일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day5.pptx) |
| [5주차 · AWS + Terraform + EKS](week5/README.md) | [보기](downloads/pdf/week5.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week5.pdf) | [1일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day1.pptx) · [2일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day2.pptx) · [3일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day3.pptx) · [4일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day4.pptx) · [5일차](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week5-day5.pptx) |
| [부록 A · 도구 설치 가이드](appendix/install.md) | [보기](downloads/pdf/appendix-install.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/appendix-install.pdf) | — |

PDF는 **보기**를 누르면 GitHub에서 바로 읽히고 **내려받기**는 파일로 저장합니다. PPTX는 누르면 내려받습니다.

## 과정 목차

### [1주차 · 클라우드·컴퓨팅 기초 이론](week1/README.md)

- **[1일차 · OT와 클라우드의 큰 그림](week1/day1/README.md)**  
  [1교시](week1/day1/lesson-01.md) · [2교시](week1/day1/lesson-02.md) · [3교시](week1/day1/lesson-03.md) · [4교시](week1/day1/lesson-04.md) · [5교시](week1/day1/lesson-05.md)
- **[2일차 · 컴퓨터와 운영체제, 가상화](week1/day2/README.md)**  
  [1교시](week1/day2/lesson-01.md) · [2교시](week1/day2/lesson-02.md) · [3교시](week1/day2/lesson-03.md) · [4교시](week1/day2/lesson-04.md) · [5교시](week1/day2/lesson-05.md) · [6교시](week1/day2/lesson-06.md) · [7교시](week1/day2/lesson-07.md)
- **[3일차 · 네트워크 기초](week1/day3/README.md)**  
  [1교시](week1/day3/lesson-01.md) · [2교시](week1/day3/lesson-02.md) · [3교시](week1/day3/lesson-03.md) · [4교시](week1/day3/lesson-04.md) · [5교시](week1/day3/lesson-05.md) · [6교시](week1/day3/lesson-06.md) · [7교시](week1/day3/lesson-07.md)
- **[4일차 · 현대 애플리케이션 구조](week1/day4/README.md)**  
  [1교시](week1/day4/lesson-01.md) · [2교시](week1/day4/lesson-02.md) · [3교시](week1/day4/lesson-03.md) · [4교시](week1/day4/lesson-04.md) · [5교시](week1/day4/lesson-05.md) · [6교시](week1/day4/lesson-06.md) · [7교시](week1/day4/lesson-07.md)
- **[5일차 · DevOps 문화와 협업](week1/day5/README.md)**  
  [1교시](week1/day5/lesson-01.md) · [2교시](week1/day5/lesson-02.md) · [3교시](week1/day5/lesson-03.md) · [4교시](week1/day5/lesson-04.md) · [5교시](week1/day5/lesson-05.md) · [6교시](week1/day5/lesson-06.md) · [7교시](week1/day5/lesson-07.md)

### [2주차 · Docker + Git 첫 실습](week2/README.md)

- **[1일차 · 개발 환경 세팅과 Git 첫걸음](week2/day1/README.md)**  
  [1교시](week2/day1/lesson-01.md) · [2교시](week2/day1/lesson-02.md) · [3교시](week2/day1/lesson-03.md) · [4교시](week2/day1/lesson-04.md) · [5교시](week2/day1/lesson-05.md) · [6교시](week2/day1/lesson-06.md) · [7교시](week2/day1/lesson-07.md)
- **[2일차 · Docker 기본](week2/day2/README.md)**  
  [1교시](week2/day2/lesson-01.md) · [2교시](week2/day2/lesson-02.md) · [3교시](week2/day2/lesson-03.md) · [4교시](week2/day2/lesson-04.md) · [5교시](week2/day2/lesson-05.md) · [6교시](week2/day2/lesson-06.md) · [7교시](week2/day2/lesson-07.md)
- **[3일차 · 이미지와 Dockerfile](week2/day3/README.md)**  
  [1교시](week2/day3/lesson-01.md) · [2교시](week2/day3/lesson-02.md) · [3교시](week2/day3/lesson-03.md) · [4교시](week2/day3/lesson-04.md) · [5교시](week2/day3/lesson-05.md) · [6교시](week2/day3/lesson-06.md) · [7교시](week2/day3/lesson-07.md)
- **[4일차 · 볼륨 · 네트워크 · 환경 변수](week2/day4/README.md)**  
  [1교시](week2/day4/lesson-01.md) · [2교시](week2/day4/lesson-02.md) · [3교시](week2/day4/lesson-03.md) · [4교시](week2/day4/lesson-04.md) · [5교시](week2/day4/lesson-05.md) · [6교시](week2/day4/lesson-06.md) · [7교시](week2/day4/lesson-07.md)
- **[5일차 · Docker Compose와 GitHub 협업](week2/day5/README.md)**  
  [1교시](week2/day5/lesson-01.md) · [2교시](week2/day5/lesson-02.md) · [3교시](week2/day5/lesson-03.md) · [4교시](week2/day5/lesson-04.md) · [5교시](week2/day5/lesson-05.md) · [6교시](week2/day5/lesson-06.md) · [7교시](week2/day5/lesson-07.md)

### [3주차 · MSA + Kubernetes 입문](week3/README.md)

- **[1일차 · MSA 개념과 실행](week3/day1/README.md)**  
  [1교시](week3/day1/lesson-01.md) · [2교시](week3/day1/lesson-02.md) · [3교시](week3/day1/lesson-03.md) · [4교시](week3/day1/lesson-04.md) · [5교시](week3/day1/lesson-05.md) · [6교시](week3/day1/lesson-06.md) · [7교시](week3/day1/lesson-07.md)
- **[2일차 · MSA 장애와 CI](week3/day2/README.md)**  
  [1교시](week3/day2/lesson-01.md) · [2교시](week3/day2/lesson-02.md) · [3교시](week3/day2/lesson-03.md) · [4교시](week3/day2/lesson-04.md) · [5교시](week3/day2/lesson-05.md) · [6교시](week3/day2/lesson-06.md) · [7교시](week3/day2/lesson-07.md)
- **[3일차 · Kubernetes 아키텍처](week3/day3/README.md)**  
  [1교시](week3/day3/lesson-01.md) · [2교시](week3/day3/lesson-02.md) · [3교시](week3/day3/lesson-03.md) · [4교시](week3/day3/lesson-04.md) · [5교시](week3/day3/lesson-05.md) · [6교시](week3/day3/lesson-06.md) · [7교시](week3/day3/lesson-07.md)
- **[4일차 · Pod · Deployment · Service](week3/day4/README.md)**  
  [1교시](week3/day4/lesson-01.md) · [2교시](week3/day4/lesson-02.md) · [3교시](week3/day4/lesson-03.md) · [4교시](week3/day4/lesson-04.md) · [5교시](week3/day4/lesson-05.md) · [6교시](week3/day4/lesson-06.md) · [7교시](week3/day4/lesson-07.md)
- **[5일차 · 운영 가능한 워크로드](week3/day5/README.md)**  
  [1교시](week3/day5/lesson-01.md) · [2교시](week3/day5/lesson-02.md) · [3교시](week3/day5/lesson-03.md) · [4교시](week3/day5/lesson-04.md) · [5교시](week3/day5/lesson-05.md) · [6교시](week3/day5/lesson-06.md) · [7교시](week3/day5/lesson-07.md)

### [4주차 · Kubernetes 운영](week4/README.md)

- **[1일차 · Helm + Gateway API](week4/day1/README.md)**  
  [1교시](week4/day1/lesson-01.md) · [2교시](week4/day1/lesson-02.md) · [3교시](week4/day1/lesson-03.md) · [4교시](week4/day1/lesson-04.md) · [5교시](week4/day1/lesson-05.md) · [6교시](week4/day1/lesson-06.md) · [7교시](week4/day1/lesson-07.md)
- **[2일차 · Observability](week4/day2/README.md)**  
  [1교시](week4/day2/lesson-01.md) · [2교시](week4/day2/lesson-02.md) · [3교시](week4/day2/lesson-03.md) · [4교시](week4/day2/lesson-04.md) · [5교시](week4/day2/lesson-05.md) · [6교시](week4/day2/lesson-06.md) · [7교시](week4/day2/lesson-07.md)
- **[3일차 · GitOps](week4/day3/README.md)**  
  [1교시](week4/day3/lesson-01.md) · [2교시](week4/day3/lesson-02.md) · [3교시](week4/day3/lesson-03.md) · [4교시](week4/day3/lesson-04.md) · [5교시](week4/day3/lesson-05.md) · [6교시](week4/day3/lesson-06.md) · [7교시](week4/day3/lesson-07.md)
- **[4일차 · Service Mesh](week4/day4/README.md)**  
  [1교시](week4/day4/lesson-01.md) · [2교시](week4/day4/lesson-02.md) · [3교시](week4/day4/lesson-03.md) · [4교시](week4/day4/lesson-04.md) · [5교시](week4/day4/lesson-05.md) · [6교시](week4/day4/lesson-06.md) · [7교시](week4/day4/lesson-07.md)
- **[5일차 · Kubernetes 보안](week4/day5/README.md)**  
  [1교시](week4/day5/lesson-01.md) · [2교시](week4/day5/lesson-02.md) · [3교시](week4/day5/lesson-03.md) · [4교시](week4/day5/lesson-04.md) · [5교시](week4/day5/lesson-05.md) · [6교시](week4/day5/lesson-06.md) · [7교시](week4/day5/lesson-07.md)

### [5주차 · AWS + Terraform + EKS](week5/README.md)

- **[1일차 · AWS 계정과 VPC](week5/day1/README.md)**  
  [1교시](week5/day1/lesson-01.md) · [2교시](week5/day1/lesson-02.md) · [3교시](week5/day1/lesson-03.md) · [4교시](week5/day1/lesson-04.md) · [5교시](week5/day1/lesson-05.md) · [6교시](week5/day1/lesson-06.md) · [7교시](week5/day1/lesson-07.md)
- **[2일차 · EC2 · ALB · Auto Scaling · S3](week5/day2/README.md)**  
  [1교시](week5/day2/lesson-01.md) · [2교시](week5/day2/lesson-02.md) · [3교시](week5/day2/lesson-03.md) · [4교시](week5/day2/lesson-04.md) · [5교시](week5/day2/lesson-05.md) · [6교시](week5/day2/lesson-06.md) · [7교시](week5/day2/lesson-07.md)
- **[3일차 · Terraform 기초](week5/day3/README.md)**  
  [1교시](week5/day3/lesson-01.md) · [2교시](week5/day3/lesson-02.md) · [3교시](week5/day3/lesson-03.md) · [4교시](week5/day3/lesson-04.md) · [5교시](week5/day3/lesson-05.md) · [6교시](week5/day3/lesson-06.md) · [7교시](week5/day3/lesson-07.md)
- **[4일차 · Terraform으로 EKS](week5/day4/README.md)**  
  [1교시](week5/day4/lesson-01.md) · [2교시](week5/day4/lesson-02.md) · [3교시](week5/day4/lesson-03.md) · [4교시](week5/day4/lesson-04.md) · [5교시](week5/day4/lesson-05.md) · [6교시](week5/day4/lesson-06.md) · [7교시](week5/day4/lesson-07.md)
- **[5일차 · 통합 · 장애 · 정리 · 회고](week5/day5/README.md)**  
  [1교시](week5/day5/lesson-01.md) · [2교시](week5/day5/lesson-02.md) · [3교시](week5/day5/lesson-03.md) · [4교시](week5/day5/lesson-04.md) · [5교시](week5/day5/lesson-05.md) · [6교시](week5/day5/lesson-06.md) · [7교시](week5/day5/lesson-07.md)

## 저장소 구성

```
README.md            ← 지금 이 페이지 (과정 목차)
week1/ … week5/      ← 교재 (주차 목차 → 일차 목차 → 교시)
appendix/            ← 부록 A · 도구 설치 가이드
downloads/pdf/       ← 주차별 이북 PDF
downloads/pptx/      ← 일차별 슬라이드
labs/                ← 실습 파일 (3주차부터 복사해서 사용)
v3/                  ← 원고와 빌드 도구 (강사용)
archive/rev2/        ← 이전 판 교재 (보관)
```
