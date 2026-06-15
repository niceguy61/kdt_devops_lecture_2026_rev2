# Week 3 Glossary: MSA 운영 용어

## Architecture

### MSA
- 한 줄 뜻: 애플리케이션을 독립 서비스들의 조합으로 운영하는 아키텍처
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Monolith
- 한 줄 뜻: 하나의 배포 단위에 여러 기능이 함께 들어간 구조
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Service Boundary
- 한 줄 뜻: 서비스가 책임지는 기능, 데이터, 배포 경계
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Topology
- 한 줄 뜻: 서비스와 의존성의 연결 구조
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Blast Radius
- 한 줄 뜻: 장애가 퍼지는 영향 범위
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

## Network/API

### API
- 한 줄 뜻: 서비스가 외부 또는 다른 서비스에 제공하는 요청 계약
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Endpoint
- 한 줄 뜻: 요청을 받는 URL path와 method
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Service Discovery
- 한 줄 뜻: 서비스가 다른 서비스의 주소를 찾는 방식
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Internal Port
- 한 줄 뜻: 컨테이너나 서비스 내부에서 열리는 port
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### External Entry Point
- 한 줄 뜻: 사용자나 외부 시스템이 들어오는 공개 진입점
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

## Reliability

### Health Check
- 한 줄 뜻: 서비스 상태를 자동으로 확인하는 요청이나 명령
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Liveness
- 한 줄 뜻: 프로세스가 살아 있는지 보는 상태
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Readiness
- 한 줄 뜻: 요청을 받을 준비가 됐는지 보는 상태
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Timeout
- 한 줄 뜻: 무한 대기를 막는 최대 대기 시간
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Retry
- 한 줄 뜻: 실패한 요청을 다시 시도하는 정책
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Graceful Degradation
- 한 줄 뜻: 일부 기능이 실패해도 핵심 기능을 유지하는 방식
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

## Observability

### Distributed Logs
- 한 줄 뜻: 여러 서비스에 흩어진 로그
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Request ID
- 한 줄 뜻: 하나의 요청을 식별하는 ID
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Correlation ID
- 한 줄 뜻: 여러 서비스 로그를 같은 흐름으로 묶는 ID
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Trace
- 한 줄 뜻: 서비스 간 호출 경로와 시간을 이어서 보는 관찰 데이터
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Metric
- 한 줄 뜻: 시간에 따라 측정되는 수치 데이터
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

## Runtime

### Worker
- 한 줄 뜻: 사용자 요청과 분리된 작업을 처리하는 서비스
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Queue
- 한 줄 뜻: 작업을 잠시 저장하고 순서대로 처리하게 돕는 버퍼
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Dependency
- 한 줄 뜻: 서비스가 정상 동작하기 위해 필요한 다른 서비스나 자원
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Compose Service
- 한 줄 뜻: Compose 파일에서 정의된 실행 단위
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html

### Kubernetes Readiness
- 한 줄 뜻: MSA를 Kubernetes 리소스로 옮기기 전 필요한 준비 상태
- 왜 중요한가: 서비스가 늘어날수록 장애 원인과 책임 경계를 빠르게 찾기 위해 필요하다.
- 수업에서 다시 나오는 곳: Week 3 전반, Week 4 Kubernetes 연결
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html
