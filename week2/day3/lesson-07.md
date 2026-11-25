# 7교시 · 멀티 스테이지와 이미지 크기·보안

> [!NOTE]
> **이번 시간에 할 일**
>
> - 이미지 크기가 왜 중요한지 압니다.
> - 베이스 이미지(full, slim, alpine, scratch)의 차이를 압니다.
> - 멀티 스테이지 빌드로 "만드는 도구"와 "실행하는 결과물"을 분리해 이미지를 100분의 1로 줄입니다.
> - 이미지 보안 점검(실행 사용자, 취약점 검사)을 맛봅니다.

## 이미지 크기가 왜 중요할까

| 이미지가 크면 | 결과 |
|---|---|
| 다운로드가 느리다 | 새 서버가 뜰 때까지 오래 걸린다 → **확장(스케일 아웃)이 느려진다** (1주차 4일차) |
| 저장·전송 비용 | 레지스트리 저장 비용, 클라우드 데이터 전송 요금 (1주차 1일차 비용 함정) |
| 들어 있는 프로그램이 많다 | **공격받을 곳(공격 표면)**이 넓어지고, 취약점 검사 결과도 많아진다 |

## 베이스 이미지 고르기

| 베이스 | 대략의 크기 | 들어 있는 것 | 언제 |
|---|---|---|---|
| `python:3.14` | 약 1GB | Debian 전체 + 컴파일러 등 빌드 도구 | 빌드에 도구가 많이 필요할 때 (빌드 단계용) |
| **`python:3.14-slim`** | 수십~100MB대 | 꼭 필요한 것만 | **대부분의 Python 앱** (오늘 쓴 것) |
| `python:3.14-alpine` | 더 작음 | Alpine(musl libc) 기반 | 작지만 일부 라이브러리 설치가 까다롭다 |
| `scratch` | **0B** | **아무것도 없음** | 혼자서 실행되는 파일 하나(Go 등)만 넣을 때 |

## 멀티 스테이지 빌드 — 주방과 식탁을 나눈다

프로그램을 **만들 때** 필요한 것(컴파일러, 빌드 도구)과 **실행할 때** 필요한 것(완성된 실행 파일)은 다릅니다. 그런데 한 단계로 빌드하면 만드는 도구까지 전부 이미지에 남습니다. **멀티 스테이지 빌드**는 Dockerfile 하나 안에서 **빌드 단계**와 **실행 단계**를 나누고, 실행 단계에는 결과물만 복사합니다.

![멀티 스테이지 빌드 — 빌드 단계의 도구는 버리고, 결과물만 작은 실행 이미지로 옮긴다](../../assets/week2/day3/w2d3-multistage.png)

> **🧩 비유 — 주방과 식탁**
>
> 음식을 만들 때는 칼, 도마, 냄비, 가스레인지가 필요합니다. 하지만 손님 식탁에는 **완성된 요리만** 내갑니다. 냄비와 도마까지 식탁에 올리지 않지요. 멀티 스테이지에서 첫 단계는 **주방**, 마지막 단계는 **식탁**입니다.

## 실습 14 · 멀티 스테이지로 100분의 1

> **🧪 실습: 실습 목표**
>
> 아주 작은 Go 웹 서버를 한 단계 빌드와 멀티 스테이지 빌드로 각각 만들어 크기를 비교합니다. Go는 **혼자서 실행되는 파일 하나**를 만들어 주기 때문에 멀티 스테이지 효과가 가장 극적으로 보이는 언어입니다. Go 코드를 이해할 필요는 없습니다.

### 단계 1 — 파일 준비

```bash
mkdir -p ~/devops-lab/day3/hello-go
cd ~/devops-lab/day3/hello-go
code .
```

`main.go`:

```go
// 멀티 스테이지 빌드 맛보기용 아주 작은 웹 서버
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	host, _ := os.Hostname()
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "안녕하세요! Go 컨테이너 %s 입니다\n", host)
	})
	fmt.Println("listening on :8080")
	http.ListenAndServe(":8080", nil)
}
```

`go.mod`:

```text
module hello-go

go 1.22
```

### 단계 2 — 한 단계 빌드 (`Dockerfile.single`)

```dockerfile
# 한 단계(single-stage): 빌드 도구가 든 큰 이미지를 그대로 실행에 쓴다
FROM golang:1.27
WORKDIR /src
COPY go.mod main.go ./
RUN go build -o /hello .
EXPOSE 8080
CMD ["/hello"]
```

### 단계 3 — 멀티 스테이지 빌드 (`Dockerfile`)

```dockerfile
# 1단계: 빌드 전용 — Go 컴파일러가 든 큰 이미지
FROM golang:1.27 AS build
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 go build -o /hello .

# 2단계: 실행 전용 — 아무것도 없는 빈 이미지에 결과물(실행 파일)만 복사
FROM scratch
COPY --from=build /hello /hello
EXPOSE 8080
USER 10001
CMD ["/hello"]
```

| 새로 나온 것 | 뜻 |
|---|---|
| `FROM … AS build` | 이 단계에 `build`라는 이름을 붙인다 |
| `CGO_ENABLED=0` | 다른 라이브러리에 기대지 않는 **혼자 실행되는 파일**로 만든다 (scratch에서 돌기 위해) |
| `FROM scratch` | **완전히 빈** 이미지에서 다시 시작한다 |
| `COPY --from=build` | 내 폴더가 아니라 **앞 단계(build)**에서 파일을 가져온다 |
| `USER 10001` | scratch에는 사용자 목록 파일도 없으므로 **번호**로 지정 |

### 단계 4 — 둘 다 빌드하고 크기 비교

```bash
docker build -f Dockerfile.single -t hello-go:single .
docker build -t hello-go:multi .
docker images hello-go
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> IMAGE             ID             DISK USAGE   CONTENT SIZE   EXTRA
> hello-go:multi    5e1c…              11MB         …MB
> hello-go:single   9a7b…             997MB         …MB
> ```
> **약 1GB → 약 10MB**, 100분의 1입니다. (정확한 숫자는 Go 버전과 플랫폼에 따라 다릅니다.) 같은 프로그램인데 크기가 이만큼 차이 나는 것은 single 이미지에 **Go 컴파일러와 Debian 전체**가 들어 있기 때문입니다.

### 단계 5 — 작은 이미지도 똑같이 동작한다

```bash
docker run -d --name hello -p 8088:8080 hello-go:multi
curl http://localhost:8088
docker exec hello sh
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 안녕하세요! Go 컨테이너 608b8ad1d724 입니다
> OCI runtime exec failed: exec failed: unable to start container process: exec: "sh": executable file not found in $PATH
> ```
> 웹 서버는 잘 동작하는데, `sh`로 들어갈 수는 **없습니다.** scratch 이미지에는 셸조차 없기 때문입니다. 침입자가 이 컨테이너를 장악해도 **쓸 도구가 아무것도 없습니다.** 반대로 디버깅할 때 불편하다는 트레이드오프도 있습니다(1주차 4일차).

```bash
docker rm -f hello
docker image rm hello-go:single
```

> [!TIP]
> **Python 앱도 멀티 스테이지를 쓸까?**
>
> Python은 컴파일된 실행 파일 하나가 아니라 **인터프리터 + 라이브러리**가 필요하므로 scratch까지 줄일 수는 없습니다. 오늘 쓴 `python:3.14-slim`만으로도 충분히 작습니다. 다만 C 언어로 된 라이브러리를 **직접 컴파일해야** 할 때는, 빌드 단계(컴파일러가 든 `python:3.14`)에서 설치하고 실행 단계(`slim`)로 결과만 옮기는 멀티 스테이지를 씁니다. 강의 저장소 `labs/week2/devmart/catalog-api/`에서 예시를 볼 수 있습니다. **언어마다 효과가 다르다**는 것을 기억하세요.

## 실습 15 · 이미지 보안 점검 맛보기

> **🧪 실습: 실습 목표**
>
> 내 이미지가 누구로 실행되는지 확인하고, 취약점 검사를 맛봅니다.

### 단계 1 — 실행 사용자 확인

```bash
docker image inspect --format '사용자: {{.Config.User}}' devmart/catalog-api:1.0.1
docker image inspect --format '사용자: {{.Config.User}}' nginx:1.30-alpine
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 사용자: appuser
> 사용자:
> ```
> 우리 API는 **appuser**로 실행됩니다. nginx 공식 이미지는 빈칸(= **root**로 시작)입니다. nginx는 80번 포트를 열기 위해 root로 시작한 뒤 일하는 프로세스(worker)만 낮은 권한으로 내립니다(2일차 5교시 `docker top`에서 worker가 다른 사용자였던 이유). 운영 환경에서는 처음부터 root가 아닌 **`nginx-unprivileged`** 같은 변형 이미지를 쓰기도 합니다.

### 단계 2 — 취약점 검사 (Docker Desktop의 Docker Scout)

```bash
docker scout quickview devmart/catalog-api:1.0.1
```

> **🟢 확인: 이렇게 나오면 성공 (예시)**
>
> ```text
>   Target     │  devmart/catalog-api:1.0.1  │    0C     0H     2M    18L
>     digest   │  7d2e41c0a9f3               │
>   Base image │  python:3.14-slim           │    0C     0H     2M    18L
> ```
> C·H·M·L은 **심각(Critical)·높음(High)·중간(Medium)·낮음(Low)** 단계의 알려진 취약점 수입니다. 숫자는 검사하는 날에 따라 달라집니다(새 취약점이 계속 발견되므로). 대부분이 **베이스 이미지**에서 온다는 것에 주목하세요. 그래서 6교시 학술 노트처럼 **베이스를 최신으로 유지**하는 것이 가장 효과적인 보안 조치입니다. 처음 실행하면 로그인이나 동의를 물을 수 있고, 인터넷이 필요합니다.

| 점검 | 확인 | 오늘 상태 |
|---|---|---|
| root로 실행하지 않는가 | `Config.User` | appuser ✓ |
| 비밀값이 들어 있지 않은가 | `.dockerignore`, 4교시 | ✓ |
| 버전이 고정되어 있는가 | `FROM`, `requirements.txt` | ✓ |
| 필요 없는 것이 들어 있지 않은가 | slim / 멀티 스테이지 | ✓ |
| 알려진 취약점 | `docker scout` | 정기적으로 다시 빌드 |

> **🧹 정리: 오늘의 정리와 커밋**
>
> ```bash
> docker ps -a
> docker container prune
> cd ~/devops-lab
> git add day3/
> git commit -m "3일차: 멀티 스테이지 빌드 실습 (hello-go)"
> git push
> ```
> `devmart/catalog-api:1.0.0`, `1.0.1` 이미지는 **내일 쓰므로 남겨 둡니다.**

> **🎓 학술 노트 — 작을수록 안전하다: 공격 표면과 디스트로리스**
>
> 마이크로소프트의 마이클 하워드(Michael Howard)는 2000년대 초 **공격 표면(attack surface)**이라는 개념을 정리했습니다. 시스템에서 공격자가 건드릴 수 있는 지점(열린 포트, 설치된 프로그램, 권한 있는 계정)의 총합이며, 이것을 **줄이는 것 자체가 보안**이라는 생각입니다(Howard, Pincus & Wing, 2005). 1주차 3일차의 "필요한 포트만 연다", 1주차 2일차의 "최소 권한(Saltzer & Schroeder, 1975)"과 같은 원리를 **이미지 내용물**에 적용하면, "필요한 파일만 넣는다"가 됩니다.
>
> 구글은 이 생각을 밀어붙여 셸도 패키지 관리자도 없이 **앱과 그 실행에 꼭 필요한 파일만** 든 **디스트로리스(distroless)** 이미지를 공개했고, 오늘의 `scratch`는 그 극단입니다. 2일차 1교시 트렌드에서 본 **강화 이미지**들도 같은 흐름입니다. 다만 학술 노트마다 반복하듯이 **트레이드오프**가 있습니다. 셸이 없으면 침입자도 못 쓰지만 운영자도 디버깅하기 어렵습니다. 그래서 Kubernetes는 필요할 때만 디버깅용 컨테이너를 잠깐 붙이는 기능(`kubectl debug`)을 제공합니다(3주차).
>
> - Howard, M., Pincus, J., & Wing, J. M. (2005). Measuring relative attack surfaces. In *Computer Security in the 21st Century*. Springer.
> - Google. *Distroless container images*. github.com/GoogleContainerTools/distroless

> **📈 트렌드 — 취약점 0개를 목표로 하는 이미지**
>
> 취약점 검사를 처음 돌려 보면 수십~수백 개가 나와 놀라는 경우가 많습니다. 그중 상당수는 앱이 실제로 쓰지도 않는 베이스 이미지의 패키지에서 나옵니다. 그래서 최근에는 **취약점이 거의 없도록 매일 다시 빌드하는 최소 이미지**를 제공하는 회사들(Chainguard, Docker Hardened Images, Google distroless 등)이 늘었고, 기업들은 "심각(Critical) 취약점이 있는 이미지는 배포 금지" 같은 규칙을 파이프라인에 겁니다. 1주차 5일차 2교시 파이프라인의 **④ 보안 검사**가 이것이고, 3주차 CI에서 이미지 검사를 자동화하며, 4주차 Kyverno로 규칙을 클러스터에 강제합니다.

## 정리 — 오늘 만든 것

| 만든 것 | 핵심 |
|---|---|
| `devmart/catalog-api` 이미지 1.0.0, 1.0.1 | 파이썬 없이 파이썬 앱 실행, appuser, 0.0.0.0 |
| `.dockerignore` | 비밀값과 쓰레기를 빌드 컨텍스트에서 제외 |
| Docker Hub의 `내아이디/devmart-catalog-api:1.0.1` | 어디서든 같은 이미지 — 다이제스트로 정확히 |
| `hello-go:multi` | 멀티 스테이지로 약 1GB → 약 10MB |

> **✅ 확인 문제**
>
> 1. 이미지가 크면 생기는 문제 세 가지는?
> 2. 멀티 스테이지에서 `COPY --from=build`는 어디서 파일을 가져오나요?
> 3. scratch 이미지 컨테이너에 `docker exec … sh`가 안 되는 이유는?
> 4. 우리 API 이미지가 root로 실행되지 않는 것을 확인하는 명령은?
> 5. 취약점 검사 결과의 대부분은 보통 어디서 오나요?
>
> <details><summary>정답</summary>
>
> 1. 다운로드가 느려 확장이 느리다, 저장·전송 비용이 든다, 공격 표면이 넓다
> 2. 같은 Dockerfile의 앞 단계(`build`라는 이름의 단계)
> 3. scratch에는 셸을 포함해 아무 프로그램도 없기 때문
> 4. `docker image inspect --format '{{.Config.User}}' 이미지`
> 5. 베이스 이미지의 패키지
>
> </details>

> [!NOTE]
> **오늘의 배움일기**
>
> - 내 앱을 처음 이미지로 만든 소감, 그리고 "내 노트북에 파이썬이 없는데 파이썬 앱이 돈다"를 동료에게 설명해 보기
> - 빌드 캐시 규칙을 블록 탑 비유로 내 말로 다시 써 보기
> - `COPY . .` 실습에서 비밀번호가 보였을 때 든 생각
> - 내 Docker Hub 이미지 주소와 다이제스트 앞 12자리 적어 두기
> - 내일(볼륨·네트워크·환경 변수) 전에 궁금한 것: API와 DB는 어떻게 서로를 찾을까?

## 참고 문헌

- Docker Docs. *Multi-stage builds*. docs.docker.com/build/building/multi-stage
- Docker Docs. *Docker Scout quickview*. docs.docker.com/scout
- Docker Hub. *golang Docker Official Image*. hub.docker.com/_/golang
- Howard, M., Pincus, J., & Wing, J. M. (2005). Measuring relative attack surfaces. Springer.
- Google. *Distroless container images*. github.com/GoogleContainerTools/distroless
