# 2교시: 토스 - 프론트엔드 플랫폼과 개발 생산성

## 수업 목표
- 프론트엔드를 단순 화면 그리기가 아니라 플랫폼으로 이해한다.
- UI 증가가 build tooling, shared component, test, preview 환경으로 이어지는 이유를 설명한다.
- Week2 Docker로 옮길 frontend 실행 조건을 찾는다.

## 참고 자료
- Toss Tech Engineering: https://toss.tech/category/engineering
- Toss Tech micro-frontend React: https://toss.tech/article/27436
- Toss Tech monorepo pipeline optimization: https://toss.tech/article/monorepo-pipeline

## 50분 운영
| 시간 | 활동 | 강사 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | 금융 앱 hook | 신뢰, 속도, 일관된 UI가 중요함을 설명한다. | context note |
| 5-15분 | 화면 이상의 프론트엔드 | route, state, package, build, preview를 나눈다. | frontend map |
| 15-25분 | 토스 사례 읽기 | 큰 프론트엔드 코드베이스에는 공통 인프라가 필요하다. | source note |
| 25-35분 | 비즈니스 압력 | 상품과 실험이 늘수록 화면과 배포가 복잡해진다. | pressure note |
| 35-45분 | 로컬 실행 조건 | Node version, package manager, build command, env var, port | execution table |
| 45-50분 | Docker 연결 | runtime과 package 상태가 다르면 onboarding이 실패한다. | readiness note |

## 핵심 설명
현대 프론트엔드는 HTML/CSS만이 아니다. routing, state, design system, build tool, package manager, test, preview, release pipeline이 함께 움직인다. 금융 서비스는 실험과 출시 속도가 중요하지만, 사용자 경험의 일관성과 신뢰도도 중요하다. 그래서 프론트엔드 자체가 개발 생산성 플랫폼이 된다.

## 시각 자료
![프론트엔드 플랫폼과 AI 보조 개발](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-02-frontend-ai-workflow.png)

![프론트엔드 플랫폼 아키텍처 모델](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-02-frontend-architecture.png)

![프론트엔드 최적화 포인트](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-02-frontend-optimization.png)

## 서비스 특장점과 채용 동기 연결
- 토스형 금융 서비스는 복잡한 금융 행동을 짧고 명확한 화면 흐름으로 바꾸는 것이 강점이다.
- 학생 입장에서는 프론트엔드가 단순 UI가 아니라 제품 실험, 접근성, 성능, 공통 컴포넌트, 배포 속도와 연결된다는 것을 볼 수 있다.
- 사용자 신뢰가 중요한 서비스에서는 작은 UI 오류도 비즈니스 리스크가 된다.

## AI 엔지니어링 연결
- 최근 프론트엔드 개발은 AI coding assistant, 자동 테스트 생성, 디자인-to-code, 접근성 점검, 에러 로그 요약과 연결된다.
- AI가 코드를 작성해도 build, test, preview, 공식 문서 확인, 보안 검토는 여전히 사람이 검증해야 한다.
- 그래서 AI 시대의 frontend platform은 "빠르게 만들기"보다 "빠르게 만들고 안전하게 검증하기"가 중요하다.

## 프론트엔드 구성요소
| 구성요소 | 역할 | 실패 증상 |
|---|---|---|
| UI component | 화면 요소 재사용 | 깨진 레이아웃, UX 불일치 |
| Router | 어떤 페이지를 열지 결정 | 잘못된 화면, blank page |
| State | 현재 화면 데이터 보관 | stale data, missing data |
| Build tool | source를 실행 가능한 asset으로 변환 | build failure |
| Package manager | 라이브러리 설치 | version conflict |
| Environment config | API endpoint와 flag 선택 | 잘못된 backend 연결 |

## 로컬 실행 조건 템플릿
```text
Runtime:
Package manager:
Install command:
Run command:
Port:
API endpoint:
Build output:
Known risk:
```

## 강사용 문장
"프론트엔드가 하나일 때는 설치가 대충 되어도 넘어갈 수 있습니다. 하지만 서비스와 팀이 늘어나면 화면 개발도 운영 문제가 됩니다. 핵심 질문은 '화면을 만들 수 있는가'가 아니라 '모든 개발자가 같은 조건으로 같은 화면을 실행할 수 있는가'입니다."

## 체크포인트
- frontend 실행 조건 4개 이상을 쓴다.
- build tooling이 팀 생산성 문제가 되는 이유를 설명한다.
- frontend 장애 1개를 빠진 실행 조건 1개와 연결한다.

## 다음 연결
3교시는 화면 뒤의 백엔드로 이동한다. 질문은 "언제 백엔드 코드가 서비스 경계를 필요로 하는가?"이다.
