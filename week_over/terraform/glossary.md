# Terraform 보강 과정 용어집

| 용어 | 의미 | 운영 확인 지점 |
|---|---|---|
| IaC | 인프라의 원하는 상태를 코드로 정의하고 변경하는 방식 | Git diff, review, plan |
| Terraform Core | 설정을 읽고 그래프와 실행 계획을 만드는 Terraform 본체 | `terraform version`, `terraform plan` |
| Provider | 외부 API와 Terraform Core를 연결하는 plugin | `required_providers`, lock file |
| Resource | Terraform이 생성·수정·삭제 수명주기를 관리하는 객체 | Resource 주소, State |
| Data Source | 기존 외부 정보를 읽는 객체 | `data.<type>.<name>` |
| Argument | 블록에 입력하는 설정값 | Provider Resource 문서의 argument reference |
| Attribute | 객체가 제공하며 다른 표현식에서 참조할 수 있는 값 | attribute reference, `terraform state show` |
| Expression | 값을 계산하거나 참조하는 Terraform Language 구문 | `terraform console` |
| Meta-argument | `for_each`, `count`, `depends_on`처럼 Resource 동작을 제어하는 언어 기능 | Resource 주소와 Plan |
| Module | 함께 관리하는 Resource를 입력·출력 인터페이스로 캡슐화한 구성 | module source/version, child address |
| State | Resource 주소와 실제 원격 객체 identity의 binding을 저장하는 데이터 | `terraform state list/show` |
| Backend | State 저장 위치와 관련 동작을 정의하는 구성 | backend block, init, locking |
| Drift | 실제 인프라가 Terraform 설정 또는 이전 State와 달라진 상태 | refresh 기반 Plan |
| Import | 기존 객체를 Terraform Resource 주소와 State에서 연결하는 작업 | import block, state, follow-up plan |
| Resource address | 구성과 State에서 Resource instance를 식별하는 주소 | `module.network.aws_subnet.public["a"]` |
| Plan | 적용 예정 변경과 의존성을 보여주는 실행 계획 | create/update/replace/destroy 수 |
| Lock file | 선택한 Provider 버전과 checksum을 기록하는 파일 | `.terraform.lock.hcl` |
