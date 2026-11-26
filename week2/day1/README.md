[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [1일차](README.md)

# 2주차 1일차 — 개발 환경 세팅과 Git 첫걸음

📕 2주차 이북 PDF: [보기](../../downloads/pdf/week2.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week2.pdf) &nbsp;|&nbsp; 📊 1일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week2-day1.pptx)

## 오늘의 목표

드디어 첫 핸즈온입니다. 오늘은 앞으로 4주 동안 매일 쓸 **작업대**를 만듭니다. 목수가 작업 전에 작업대와 공구를 정리하듯, 우리도 터미널, 편집기, Git, GitHub, Docker를 한 번 제대로 설치해 두면 나머지 4주가 훨씬 편해집니다. 오늘이 끝나면 여러분 노트북에서 `docker run hello-world`가 성공하고, 내가 만든 첫 파일이 GitHub에 올라가 있어야 합니다.

- Windows는 WSL2 + Ubuntu, Mac은 터미널을 기본 작업 환경으로 준비합니다.
- VS Code로 Linux 안의 파일을 편집합니다.
- Git을 설치하고 이름과 이메일을 설정합니다.
- GitHub에 로그인해 첫 저장소를 만들고, 커밋하고, push합니다.
- Docker Desktop을 설치하고 `hello-world` 컨테이너를 실행합니다.
- 설치 점검표로 모든 도구가 준비되었는지 확인합니다.

## 실습 원칙 — 오늘부터 4주 동안

> [!IMPORTANT]
> **핸즈온을 대하는 다섯 가지 약속**
>
> 1. **한 단계씩.** 단계 하나를 실행하고, **확인 박스와 결과가 같은지** 본 다음에 넘어갑니다.
> 2. **에러는 정상입니다.** 막히면 그 단계의 **"막혔다면"** 표를 먼저 봅니다. 그래도 안 되면 1주차에 배운 **다섯 줄 질문**으로 물어봅니다.
> 3. **복사는 하되, 읽고 붙여 넣습니다.** 명령을 붙여 넣기 전에 무엇을 하는 명령인지 한 번 읽습니다.
> 4. **비밀번호와 토큰은 어디에도 붙여 넣지 않습니다.** 채팅, 스크린샷, 저장소, AI 도구 모두.
> 5. **끝나면 정리합니다.** 실습마다 있는 **정리** 박스를 따라 쓰지 않는 컨테이너를 지웁니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 1주차 요약 + 작업 환경 준비 (WSL2 / Mac 터미널) | Ubuntu 터미널 열기 |
| 2교시 | 터미널과 VS Code | `~/devops-lab` 폴더를 VS Code로 열기 |
| 3교시 | Git 설치와 설정 | `git config --list`에 내 이름 |
| 4교시 | GitHub 계정과 인증 | `gh auth status` 로그인 확인 |
| 5교시 | 첫 저장소 — commit과 push | GitHub에 README 올리기 |
| 6교시 | Docker Desktop 설치 | `docker version` 출력 |
| 7교시 | 설치 점검과 문제 해결 | `hello-world` 성공 + 점검표 push |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [1주차 요약과 작업 환경 준비](lesson-01.md)
2. [터미널과 VS Code](lesson-02.md)
3. [Git 설치와 설정](lesson-03.md)
4. [GitHub 계정과 인증](lesson-04.md)
5. [첫 저장소 — commit과 push](lesson-05.md)
6. [Docker Desktop 설치](lesson-06.md)
7. [설치 점검과 문제 해결](lesson-07.md)

---

⬅️ 이전: [7교시 · 손으로 맞추는 실행 환경 (강사 시연) + 2주차 준비](../../week1/day5/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 1주차 요약과 작업 환경 준비](lesson-01.md) ➡️
