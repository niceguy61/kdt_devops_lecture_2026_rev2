# 1교시: 쿠팡 - 현대 애플리케이션 전체 구성 지도

## 수업 목표
- 커머스 서비스가 하나의 프로그램이 아니라 여러 시스템의 조합임을 설명한다.
- frontend, backend, data, cache, queue, network, config, observability, compute를 한 화면에서 구분한다.
- 비즈니스가 커질수록 어떤 운영 부담이 늘어나는지 연결한다.
- Docker가 필요한 첫 질문을 만든다: "모든 의존성을 각자 직접 설치하면 무엇이 고통스러울까?"

## 참고 자료
- Coupang Engineering Blog: https://medium.com/coupang-engineering
- Coupang Engineering microservice architecture challenge: https://medium.com/coupang-engineering/%ED%96%89%EB%B3%B5%EC%9D%84-%EC%B0%BE%EA%B8%B0-%EC%9C%84%ED%95%9C-%EC%9A%B0%EB%A6%AC%EC%9D%98-%EC%97%AC%EC%A0%95-a31fc2d5a572
- Coupang Engineering data platform growth: https://medium.com/coupang-engineering/data-platform-2022-global-expansion-in-petabytes-3dbbbf27f6fe

## 50분 운영
| 시간 | 활동 | 강사 초점 | 학생 산출 |
|---|---|---|---|
| 0-5분 | 취업 동기 hook | 익숙한 회사의 시스템을 해부한다고 안내한다. | motivation note |
| 5-15분 | 상품 페이지 분해 | 상품, 가격, 재고, 이미지, 배송, 리뷰, 추천을 나눈다. | component list |
| 15-25분 | 비즈니스 증가 요인 | 사용자, 상품, 판매자, 지역, 배송 약속 증가를 설명한다. | growth-pressure table |
| 25-35분 | 운영 challenge | 데이터 소유권, 지연시간, 피크 트래픽, 배포 조율 | challenge note |
| 35-45분 | 로컬 실행 조건으로 축소 | 작은 쇼핑 앱이면 무엇이 필요한지 적는다. | local condition map |
| 45-50분 | Docker 연결 | 수동 설치의 고통을 한 문장으로 만든다. | Docker 필요성 문장 |

## 핵심 설명
사용자에게 상품 페이지는 하나의 화면처럼 보인다. 하지만 뒤에서는 상품 카탈로그, 가격, 재고, 이미지 저장소, 배송 약속, 리뷰, 추천 같은 여러 책임이 만난다. 회사가 커질수록 상품 수와 사용자 수만 늘어나는 것이 아니라, 데이터 소유권, 읽기 속도, 캐시, 배포 조율, 장애 영향 범위가 함께 커진다.

Docker는 이 비즈니스 문제를 해결하는 도구가 아니다. 하지만 이런 서비스가 실행되기 위한 조건을 포장하고 재현하기 위한 첫 번째 도구가 된다.

## 시각 자료
![커머스 앱 구성요소](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-01-commerce-component-map.png)

![커머스 서비스 아키텍처 모델](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-01-commerce-architecture.png)

![커머스 최적화 포인트](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day4/assets/lesson-01-commerce-optimization.png)

## 서비스 특장점과 채용 동기 연결
- 쿠팡형 커머스 서비스의 강점은 사용자가 상품 탐색, 가격 확인, 재고 확인, 주문, 배송 기대를 한 화면에서 빠르게 끝낸다는 점이다.
- 학생 관점에서는 "대규모 트래픽을 버티는 백엔드", "상품/주문/배송 데이터 처리", "추천과 검색"을 모두 볼 수 있는 도메인이다.
- 비즈니스가 커질수록 빠른 화면보다 더 어려운 문제는 정확한 재고, 주문 정합성, 배송 약속, 장애 시 복구다.

## AI 엔지니어링 연결
- 커머스에서는 추천, 검색 랭킹, 리뷰 요약, 상품 이미지 검수, 수요 예측에 AI가 들어갈 수 있다.
- AI 기능이 붙으면 모델 서버, feature data, batch job, GPU/CPU 비용, 실험 추적이 추가 실행 조건이 된다.
- Docker 관점에서는 "추천 API를 어떤 runtime으로 띄우는가", "모델 파일은 어디에 두는가", "실험용 데이터를 어떻게 초기화하는가"가 Week2 이후 질문이 된다.

## 비즈니스 증가와 시스템 노력
| 비즈니스 증가 | 함께 늘어나는 시스템 노력 |
|---|---|
| 상품 수 증가 | catalog storage, image storage, search indexing |
| 사용자 수 증가 | API 처리량, cache hit rate, monitoring |
| 판매자 수 증가 | 데이터 소유권, 검증, 권한 규칙 |
| 주문 수 증가 | 재고 정합성, queue 처리, retry |
| 지역 증가 | network latency, 배송 로직, traffic routing |

## 로컬 매핑 실습
| 구성요소 | 작은 로컬 버전 | 실제 회사 버전 |
|---|---|---|
| Frontend | `index.html` 상품 화면 | web/mobile product page |
| Backend | 간단한 API process | 여러 domain service |
| Data | `products.json` | database, data platform |
| Cache | browser cache | distributed cache |
| Queue | 아직 없음 | order/event pipeline |
| Network | `localhost:8000` | CDN, load balancer, internal network |
| Config | `.env` 또는 hard-coded value | environment config, secret |

## 학생 산출물
```text
회사: 쿠팡
구성요소 초점:
비즈니스 증가:
운영 부담:
로컬 앱으로 줄이면:
Docker가 필요해지는 지점:
```

## 체크포인트
- 상품 페이지 뒤의 구성요소 5개 이상을 말할 수 있다.
- 비즈니스 증가 요인 1개와 운영 부담 1개를 연결한다.
- Docker 명령 없이 Docker가 필요한 이유를 한 문장으로 쓴다.

## 다음 연결
2교시는 전체 시스템에서 프론트엔드로 좁힌다. 질문은 "화면 하나 바꾸는 일이 왜 플랫폼 문제가 되는가?"이다.
