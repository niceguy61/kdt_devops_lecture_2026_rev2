# Week 3 Day1 Academic Foundations

## 수업 기준
Day 1은 Week 2 Compose 경험을 MSA 운영 토폴로지로 확장한다. 표준 `msa-demo` 앱을 기준으로 frontend, api, worker, db의 역할과 요청 흐름을 읽고 실제로 실행한다.

## 공식/현업 참고 자료
| 자료 | URL | 연결 포인트 |
|---|---|---|
| Microservices on AWS | https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html | 수업에서 확인할 키워드 |
| Docker Compose services | https://docs.docker.com/reference/compose-file/services/ | 수업에서 확인할 키워드 |
| Twelve-Factor App | https://12factor.net/ | 수업에서 확인할 키워드 |

## 수업 적용 원칙
- 공식 문서를 명령 암기 자료로 쓰지 않고, 어떤 상태를 확인하는 기준인지 읽는다.
- 정상/비정상 판단은 화면 인상보다 command output, log, event, health response로 남긴다.
- 보안 값과 token은 evidence에 그대로 남기지 않는다.
- 8교시 배움일기에는 그날 확인한 증거와 다음 수업 질문을 남긴다.
