# Week 2 Day 1 Academic And Professional Foundations

이 문서는 Day 1 강의안의 근거를 학생용 lesson보다 조금 더 명시적으로 정리한다.

| 기준 | Day 1 연결 |
|---|---|
| Docker Docs: Docker overview | image, container, registry, Docker Engine을 공식 용어로 설명한다. |
| Docker Desktop Docs | 설치, 실행, Desktop GUI, local development 환경을 확인한다. |
| Docker Desktop Mac install docs | 기본 실습 환경인 macOS에서 Apple silicon/Intel, system requirement, 실행 권한을 확인한다. |
| Docker Desktop Windows install docs | Windows 사용자가 있을 경우 WSL 2, 가상화, 권한, system requirement 이슈를 예외 경로 blocker evidence로 기록한다. |
| Google SRE incident culture | 설치 실패나 실행 실패를 blame이 아니라 관찰 가능한 evidence로 바꾼다. |
| Bloom's taxonomy | remember 명령 암기보다 understand/apply/analyze 수준의 실행, 관찰, 장애 분석을 요구한다. |
| ABET professional responsibility | secret, credential, device permission, software license 조건을 전문 책임으로 다룬다. |

## Evidence Standard
Day 1의 통과 기준은 "설치 성공" 하나가 아니다. 교육장 장비와 운영 정책에 따라 설치가 막힐 수 있으므로, 다음을 evidence로 인정한다.

| 상황 | 인정되는 evidence |
|---|---|
| 설치 성공 | Docker Desktop running 상태, `docker version`, `hello-world` output |
| 설치 실패 | OS, 설치 단계, error message, 시도한 공식 문서 URL, 도움 요청 대상 |
| macOS 권한/실행 문제 | Docker Desktop 실행 권한, 보안 설정, Client/Server 연결 error |
| Windows WSL/가상화 문제 | WSL 2 또는 virtualization 관련 error message, 관리자 권한 요청 여부 |
| 로그인 문제 | Docker Hub 로그인 상태 또는 로그인 없이 pull 가능한 이미지 실행 결과 |

## Official Links
- Docker overview: https://docs.docker.com/engine/docker-overview/
- Docker Desktop: https://docs.docker.com/desktop/
- Install Docker Desktop on Mac: https://docs.docker.com/desktop/setup/install/mac-install/
- Install Docker Desktop on Windows: https://docs.docker.com/desktop/setup/install/windows-install/
- Docker Desktop sign in: https://docs.docker.com/desktop/setup/sign-in/
- What is an image?: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/
