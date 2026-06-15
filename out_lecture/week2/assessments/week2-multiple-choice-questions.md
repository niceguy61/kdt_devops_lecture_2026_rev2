# Week 2 객관식 문제 세트

## 안내
- 범위: Week 2 Docker 기초, image/container, Dockerfile, lifecycle, port binding, environment variable, volume, Compose, logs/RCA, 보안/정리
- 문항 수: 10문항
- 형식: 4지선다

---

## 1. Image와 container 구분

### 문제 내용
Docker image와 container의 관계를 가장 적절하게 설명한 것은 무엇인가?

### 출제의도
Docker의 핵심 개념을 파일 묶음과 실행 중인 process 관점으로 구분하는지 확인한다.

### 선택지
1. image는 실행 중인 process이고 container는 Dockerfile이다.
2. image는 실행에 필요한 파일과 설정을 담은 불변에 가까운 묶음이고, container는 그 image를 기반으로 실행된 instance다.
3. image와 container는 같은 의미이며 구분할 필요가 없다.
4. container는 Docker Hub에만 존재하고 image는 로컬에만 존재한다.

### 정답
2

### 문제해설
image는 애플리케이션 실행에 필요한 파일, dependency, 기본 명령 등을 담은 실행 패키지에 가깝다. container는 그 image를 실행해 만들어진 실제 runtime instance다.

---

## 2. Dockerfile instruction 이해

### 문제 내용
다음 중 Dockerfile에서 `COPY` instruction을 사용할 때 가장 주의해야 할 점으로 적절한 것은 무엇인가?

### 출제의도
build context와 이미지에 포함되는 파일 범위를 이해하고, 불필요하거나 민감한 파일이 이미지에 들어가지 않도록 판단하는지 확인한다.

### 선택지
1. `COPY . .`는 항상 안전하므로 `.dockerignore`가 필요 없다.
2. 필요한 파일만 이미지에 포함되도록 경로와 `.dockerignore`를 함께 확인한다.
3. `COPY`는 container 실행 후에만 동작한다.
4. `COPY`는 port binding을 설정하는 instruction이다.

### 정답
2

### 문제해설
Docker build는 build context를 기준으로 파일을 이미지에 포함한다. 범위를 넓게 잡으면 `.env`, 임시 파일, 불필요한 자료가 들어갈 수 있으므로 `COPY` 범위와 `.dockerignore`를 함께 관리해야 한다.

---

## 3. Container lifecycle 확인

### 문제 내용
컨테이너가 실행 중인지 확인하고, 문제가 있을 때 로그를 보려는 상황이다. 가장 적절한 명령 조합은 무엇인가?

### 출제의도
컨테이너 lifecycle을 상태 확인과 로그 확인 명령으로 다룰 수 있는지 확인한다.

### 선택지
1. `docker ps`, `docker logs <container>`
2. `git status`, `git log`
3. `curl -I https://docker.com`, `python3 --version`
4. `docker build`, `docker pull`만 실행

### 정답
1

### 문제해설
`docker ps`는 실행 중인 컨테이너 상태를 확인하는 기본 명령이고, `docker logs`는 컨테이너 내부 process가 남긴 표준 출력/에러 로그를 확인하는 데 사용한다.

---

## 4. Port binding

### 문제 내용
nginx 컨테이너 내부의 80번 port를 호스트의 8080번 port로 접근하게 하려면 어떤 실행 방식이 적절한가?

### 출제의도
host port와 container port를 구분하고, 외부 접근 경로를 명령으로 표현할 수 있는지 확인한다.

### 선택지
1. `docker run -p 8080:80 nginx`
2. `docker run -p 80:8080 nginx`
3. `docker run nginx -p 8080`
4. `docker ps -p 8080:80 nginx`

### 정답
1

### 문제해설
`-p hostPort:containerPort` 형식으로 port를 바인딩한다. 호스트에서 `localhost:8080`으로 접근하면 컨테이너 내부 80번 port로 전달된다.

---

## 5. Environment variable 관리

### 문제 내용
컨테이너 실행 시 애플리케이션 설정값을 바꾸고 싶다. Week 2 기준으로 적절한 접근은 무엇인가?

### 출제의도
설정을 이미지에 고정하지 않고 실행 시점의 환경변수나 Compose 설정으로 분리하는지 확인한다.

### 선택지
1. 설정값을 소스 코드와 이미지에 직접 하드코딩한다.
2. `docker run -e` 또는 Compose `environment`로 설정 이름과 값을 주입하고, 민감정보 공개 여부를 점검한다.
3. 설정값은 README 제목에만 적는다.
4. 설정은 Docker에서 바꿀 수 없으므로 매번 새 컴퓨터를 사용한다.

### 정답
2

### 문제해설
환경변수는 실행 환경별로 달라질 수 있는 값을 이미지 밖에서 주입하는 방법이다. 다만 secret 값은 공개 repository나 스크린샷에 남기지 않아야 한다.

---

## 6. Volume과 데이터 보존

### 문제 내용
DB 컨테이너를 삭제했다가 다시 만들 때 데이터가 유지되어야 한다. 가장 적절한 선택은 무엇인가?

### 출제의도
컨테이너 filesystem과 volume의 차이를 이해하고, 데이터 보존 요구를 실행 구성에 반영할 수 있는지 확인한다.

### 선택지
1. 컨테이너 내부 임시 filesystem에만 데이터를 저장한다.
2. named volume 또는 필요한 bind mount를 사용하고, 삭제 전 위험을 README에 기록한다.
3. `docker logs`만 저장하면 DB 데이터가 유지된다.
4. image tag를 바꾸면 데이터가 자동 보존된다.

### 정답
2

### 문제해설
컨테이너를 삭제하면 컨테이너 내부 writable layer의 데이터는 사라질 수 있다. 데이터 보존이 필요하면 volume을 사용하고, `docker volume rm` 같은 정리 명령의 위험도 함께 기록해야 한다.

---

## 7. Compose service name과 network

### 문제 내용
Docker Compose로 `web`과 `db` service를 같은 compose project에서 실행한다. `web` 컨테이너가 DB에 접근할 때 일반적으로 기준이 되는 이름은 무엇인가?

### 출제의도
Compose가 multi-container 실행을 묶고, service name 기반 network discovery를 제공한다는 점을 이해하는지 확인한다.

### 선택지
1. 항상 `localhost`
2. Compose service name인 `db`
3. Docker Hub 계정 이름
4. image digest 전체 문자열

### 정답
2

### 문제해설
Compose는 같은 project의 service들을 기본 network에 연결하고 service name을 DNS 이름처럼 사용할 수 있게 한다. 따라서 `web`에서 DB service를 가리킬 때 `db` 같은 service name을 사용한다.

---

## 8. Docker 장애 분석

### 문제 내용
`docker run -p 8080:80 nginx`를 실행했는데 port가 이미 사용 중이라는 오류가 발생했다. 가장 적절한 기록과 대응은 무엇인가?

### 출제의도
Docker 실행 오류를 단순 실패로 끝내지 않고 증상, 원인 후보, 확인 명령, 수정, 재확인으로 정리하는지 확인한다.

### 선택지
1. 오류 메시지를 보지 않고 다른 image를 무작위로 실행한다.
2. port conflict 증상과 사용한 명령을 기록하고, 기존 process/container 확인 후 다른 host port로 재실행하고 HTTP 응답을 재확인한다.
3. Docker를 삭제한다.
4. README에는 성공한 명령만 남기고 실패는 숨긴다.

### 정답
2

### 문제해설
port conflict는 Docker 실습에서 자주 발생한다. 어떤 host port를 사용했는지, 무엇이 이미 점유했는지, 어떤 port로 바꿨는지, 변경 후 HTTP 확인이 되었는지를 남기면 좋은 RCA가 된다.

---

## 9. Registry와 tag

### 문제 내용
이미지를 다른 사람이 받을 수 있도록 registry에 올리려 한다. 다음 중 tag와 push 전 점검으로 가장 적절한 것은 무엇인가?

### 출제의도
image tag가 공유와 재현의 기준이 되며, registry 사용 전 민감정보와 불필요한 파일 포함 여부를 확인해야 함을 평가한다.

### 선택지
1. 아무 이름 없이 build한 뒤 password를 README에 적는다.
2. repository/image:version 형태로 tag를 붙이고, secret 포함 여부와 Docker Hub 인증 정보 노출 여부를 확인한다.
3. container name만 바꾸면 자동으로 registry에 올라간다.
4. `docker ps`를 실행하면 image push가 완료된다.

### 정답
2

### 문제해설
tag는 어떤 image를 공유하고 실행할지 식별하는 기준이다. push 전에는 이미지에 민감정보가 들어갔는지, README나 terminal 기록에 token/password가 노출되지 않았는지 확인해야 한다.

---

## 10. Week 2 학습 정리 제출물

### 문제 내용
Week 2 학습 정리 제출물에 포함하기 가장 적절한 내용 조합은 무엇인가?

### 출제의도
Docker 학습 결과를 발표식 문장보다 실행 증거, 문제 해결, 개선점, 다음 질문으로 정리할 수 있는지 확인한다.

### 선택지
1. Docker가 좋다는 감상과 참고 링크 목록만 작성한다.
2. build/run/compose 명령, HTTP/log/status evidence, 겪은 문제와 재확인, 보안/정리 note, hands-on 발전 내역, Week 3 질문을 포함한다.
3. Docker 공식 로고 이미지만 첨부한다.
4. 수업 시간표를 그대로 복사한다.

### 정답
2

### 문제해설
Week 2 제출물은 글의 화려함보다 재현 가능한 evidence와 판단 근거가 중요하다. 실행 명령, 확인 결과, 문제 해결 기록, 보안/정리 기준, 다음 주차로 이어지는 질문이 있으면 학습 상태를 확인하기 쉽다.
