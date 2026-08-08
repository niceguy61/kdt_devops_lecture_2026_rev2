# Java 팀 셋업

1. 라이브러리: build.gradle.additions 내용 복붙
2. Filter 등록: @Component라 자동 등록, service.name은 application.yml에
service:
  name: your-team-api

3. Prometheus 엔드포인트 확인: http://localhost:8080/actuator/prometheus
4. MDC 설정: logback-spring.xml에 %X{traceId} 추가
<pattern>%d{yyyy-MM-dd HH:mm:ss} [%X{traceId}] [%thread] %-5level %logger{36} - %msg%n</pattern>

5. Loki 전송: logback에 Loki appender 추가 (선택, stdout이면 Promtail이 수집)
