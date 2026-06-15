# Week 2 Day 2 Academic And Professional Foundations

| 기준 | Day 2 연결 |
|---|---|
| Dockerfile reference | Dockerfile instruction의 공식 의미를 확인한다. |
| Docker build docs | build context, cache, layer, tag를 공식 명령과 연결한다. |
| Docker image docs | image, tag, digest, immutable image 개념을 설명한다. |
| Docker storage docs | image layer, container writable layer, bind mount, volume을 분리한다. |
| Docker Hub docs | registry push/pull과 credential 보호를 다룬다. |
| OCI Image Specification | image manifest, layer, digest가 content-addressed artifact로 다뤄지는 기준을 연결한다. |
| Operating systems filesystem model | mount, path, file permission, persistence를 OS abstraction으로 설명한다. |
| OWASP Secrets Management | secret을 image layer와 public registry에 포함하지 않는 기준이다. |
| DevOps handoff practice | README build/run/check/cleanup/troubleshoot가 인수인계 evidence가 된다. |

## Conceptual Rationale
Dockerfile은 단순 명령 모음이 아니라 build artifact를 만드는 source code에 가깝다. Dockerfile instruction의 순서, build context의 범위, cache 사용 여부, base image tag는 결과 image의 내용과 재현성에 영향을 준다. 학생은 `docker build` 성공 여부만 보지 않고, 어떤 파일이 context로 들어갔는지, 어떤 instruction이 layer를 만들었는지, image가 어떤 tag와 ID를 갖는지 확인해야 한다.

Storage 실습은 image build와 분리해서 다룬다. image layer는 배포 artifact의 일부이고, container writable layer는 container lifecycle에 묶인 임시 실행 상태다. 반면 bind mount와 named volume은 container filesystem 외부에 데이터를 두는 방식이다. 이 차이를 모르면 "컨테이너를 삭제했는데 데이터가 왜 남았는가" 또는 "컨테이너를 삭제하니 수정한 파일이 왜 사라졌는가" 같은 운영 사고가 생긴다.

## Standards Crosswalk
| 기준 | 학생 행동 |
|---|---|
| Bloom apply/analyze | Dockerfile을 작성하고 build output에서 layer/cache/path 문제를 분석한다. |
| ABET-style problem solving | 실패 메시지를 build context, path, cache, permission 문제로 분류한다. |
| Professional responsibility | secret이 image layer, build context, public registry에 들어가지 않게 확인한다. |
| SRE/DevOps evidence culture | build/run/check/logs/cleanup 결과를 README와 RCA note에 남긴다. |

## Official Links
- Dockerfile reference: https://docs.docker.com/reference/dockerfile/
- Docker build command: https://docs.docker.com/reference/cli/docker/buildx/build/
- Docker build context: https://docs.docker.com/build/building/context/
- Docker storage: https://docs.docker.com/engine/storage/
- Docker bind mounts: https://docs.docker.com/engine/storage/bind-mounts/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- Docker image tag: https://docs.docker.com/reference/cli/docker/image/tag/
- Docker image history: https://docs.docker.com/reference/cli/docker/image/history/
- Docker Hub quickstart: https://docs.docker.com/docker-hub/
- OCI Image Specification: https://specs.opencontainers.org/image-spec/
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
