<sub>[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [3일차](README.md) › 8/8교시</sub>

# 8교시 · 이미지 취약점 스캔과 SBOM — Trivy

> [!NOTE]
> **이번 시간에 할 일**
>
> - 오픈소스 스캐너 **Trivy**를 설치 없이 **컨테이너로** 실행합니다.
> - 내 이미지의 취약점을 심각도별로 읽고, **어디서 왔는지**(베이스 이미지 · 내 라이브러리)를 구분합니다.
> - 종료 코드로 "심각한 취약점이 있으면 실패"하는 **검문소**를 만듭니다(3주차 CI에서 그대로 씀).
> - 이미지의 부품 목록 **SBOM**을 만들어 보고, 그것이 왜 1주차 5일차의 Log4Shell 같은 날에 필요한지 압니다.
> - Dockerfile의 설정 실수도 검사합니다.

> [!IMPORTANT]
> **7교시의 이어서**
>
> 7교시에 `docker scout quickview`로 숫자 네 개(C · H · M · L)를 봤습니다. 오늘은 **그 숫자가 무엇인지 한 줄씩 열어 보고**, 고치고, 기록으로 남깁니다. Trivy는 CNCF 생태계에서 가장 널리 쓰이는 공개 스캐너로, 로그인 없이 쓸 수 있고 3주차 GitHub Actions에 그대로 넣을 수 있습니다.

## 실습 16 · Trivy를 컨테이너로 실행하기

> **🧪 실습: 실습 목표**
>
> Trivy를 컨테이너로 실행할 수 있게 짧은 이름(alias)을 만들고, 버전을 확인합니다.

```bash
cd ~/devops-lab/devmart/catalog-api
TRIVY_IMAGE=aquasec/trivy:0.76.2      # 그날의 최신은 github.com/aquasecurity/trivy/releases
alias trivy='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivy-cache:/root/.cache/ -v "$PWD":/work -w /work '"$TRIVY_IMAGE"
trivy --version
```

| 부분 | 뜻 |
|---|---|
| `alias trivy='…'` | 긴 명령에 짧은 이름을 붙임. 이 터미널을 닫으면 사라진다 |
| `-v /var/run/docker.sock:…` | Trivy 컨테이너가 **내 Docker 엔진에 있는 이미지**를 읽을 수 있게 엔진의 문(소켓)을 연결 |
| `-v trivy-cache:/root/.cache/` | 취약점 데이터베이스를 **이름 있는 볼륨**에 보관 — 다음부터 빠르다 (4일차 미리 보기) |
| `-v "$PWD":/work -w /work` | 지금 폴더를 컨테이너 안 `/work`로 — 결과 파일을 여기 남긴다 |

> [!WARNING]
> **도커 소켓은 열쇠 꾸러미다**
>
> `docker.sock`을 연결한 컨테이너는 **내 Docker 엔진을 마음대로 조종**할 수 있습니다(새 컨테이너 실행 · 삭제). 오늘처럼 **이름과 버전을 고정한 믿을 만한 도구**에만 연결합니다. 모르는 이미지에 소켓을 넘기지 않습니다.

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> Version: 0.76.2
> ```
> 처음 실행하면 이미지를 받느라 시간이 조금 걸립니다.

## 실습 17 · 내 이미지 검사하기

### 단계 1 — 높음 · 심각만 보기

```bash
trivy image --severity HIGH,CRITICAL devmart/catalog-api:1.0.1
```

처음에는 취약점 데이터베이스를 내려받습니다(1분 안팎).

> **🟢 확인: 이렇게 보입니다 (예시 — 실제로는 표 테두리와 Title 칸이 더 있고, 숫자는 검사하는 날마다 다름)**
>
> ```text
> devmart/catalog-api:1.0.1 (debian 13.2)
> Total: 1 (HIGH: 1, CRITICAL: 0)
>
> Library    Vulnerability   Severity  Status  Installed  Fixed Version
> ─────────  ──────────────  ────────  ──────  ─────────  ───────────────
> libexpat1  CVE-2026-xxxxx  HIGH      fixed   2.7.1-2    2.7.1-2+deb13u1
>
> Python (python-pkg)
> Total: 0 (HIGH: 0, CRITICAL: 0)
> ```

| 칸 | 읽는 법 |
|---|---|
| 첫 줄 `(debian 13.2)` | **베이스 이미지의 OS 패키지** 검사 결과 |
| `Python (python-pkg)` | **내가 넣은 라이브러리**(`requirements.txt`) 검사 결과 |
| `Vulnerability` | **CVE** 번호 — 전 세계가 같은 취약점을 같은 이름으로 부르는 번호 |
| `Status` · `Fixed Version` | `fixed`면 **고친 버전이 이미 나왔다** = 다시 빌드하면 사라질 수 있다 |
| `will_not_fix` · `affected` | 아직 고친 버전이 없다 — 위험을 판단하고 기록해야 한다 |

### 단계 2 — 베이스 이미지 비교

같은 Python이라도 베이스에 따라 짐(패키지)의 양이 다릅니다.

```bash
trivy image -q --severity HIGH,CRITICAL python:3.14 2>/dev/null | grep "^Total"
trivy image -q --severity HIGH,CRITICAL python:3.14-slim 2>/dev/null | grep "^Total"
```

> **🟢 확인: 이렇게 보입니다 (예시)**
>
> ```text
> Total: 37 (HIGH: 33, CRITICAL: 4)
> Total: 1 (HIGH: 1, CRITICAL: 0)
> ```
> 컴파일러와 도구가 다 든 `python:3.14`는 **설치된 패키지가 많은 만큼 취약점도 많습니다.** 7교시의 "작을수록 안전하다"를 숫자로 확인했습니다. (`python:3.14`를 처음 받으면 1GB 가까이 내려받습니다. 시간이 없으면 이 단계는 강사 화면으로 봅니다.)

### 단계 3 — 고치기: 베이스를 새로 받아 다시 빌드

`Fixed Version`이 있는 취약점은 대부분 **베이스 이미지를 새로 받아 다시 빌드**하면 사라집니다.

```bash
docker build --pull -t devmart/catalog-api:1.0.2 .
trivy image -q --severity HIGH,CRITICAL devmart/catalog-api:1.0.2 | grep "^Total"
```

- `--pull` : 내 컴퓨터에 `python:3.14-slim`이 있어도 **레지스트리에서 최신을 다시 확인**해 받는다. 이게 없으면 몇 주 전에 받아 둔 낡은 베이스로 계속 빌드한다

> [!IMPORTANT]
> **취약점 대응의 대부분은 '다시 빌드'다**
>
> 코드는 한 줄도 안 바꿨는데 이미지가 안전해졌습니다. 그래서 운영 팀은 앱이 바뀌지 않아도 **정기적으로(예: 매주) 다시 빌드**합니다. 3주차 CI에서 이것을 자동으로 돌립니다.

## 실습 18 · 검문소 만들기 — 종료 코드

```bash
trivy image -q --exit-code 1 --severity CRITICAL devmart/catalog-api:1.0.2 > /dev/null
echo "CRITICAL 검문: $?"
trivy image -q --exit-code 1 --severity HIGH,CRITICAL python:3.14 > /dev/null
echo "python:3.14 검문: $?"
```

> **🟢 확인: 이렇게 나오면 성공 (예시)**
>
> ```text
> CRITICAL 검문: 0
> python:3.14 검문: 1
> ```
> `--exit-code 1` : 조건에 맞는 취약점이 **하나라도 있으면 종료 코드 1**. 1일차 8교시의 `$?` 그대로입니다. 3주차 2일차에 이 한 줄을 GitHub Actions에 넣으면, 심각한 취약점이 있는 이미지는 **레지스트리에 올라가기 전에 멈춥니다.**

> [!TIP]
> **당장 고칠 수 없는 취약점은 이유와 기한을 적어 넘긴다**
>
> 고친 버전이 없거나, 우리 앱이 그 기능을 쓰지 않아 위험이 없다고 판단한 취약점은 폴더에 `.trivyignore` 파일을 두고 적습니다.
> ```text
> # libfoo의 XML 외부 개체 기능 — catalog-api는 XML을 처리하지 않음. 2026-11 검토(김데브)
> CVE-2026-xxxxx exp:2027-02-28
> ```
> `exp:` 날짜가 지나면 다시 검사에 걸립니다. **무시한 이유와 사람과 기한**을 남기는 것이 핵심입니다 — 2일차의 `troubleshooting.md`처럼 기록이 곧 실력입니다.

## 실습 19 · SBOM — 이미지의 부품 목록

> **🧪 실습: 실습 목표**
>
> 이미지에 무엇이 들어 있는지 표준 형식(CycloneDX)의 목록으로 만들고, 그 목록만으로 다시 검사합니다.

### 단계 1 — 만들기

```bash
trivy image --format cyclonedx --output sbom-catalog-api-1.0.2.cdx.json devmart/catalog-api:1.0.2
ls -lh sbom-catalog-api-1.0.2.cdx.json
```

### 단계 2 — 읽기

```bash
jq '.components | length' sbom-catalog-api-1.0.2.cdx.json
jq -r '.components[] | select(.name=="flask" or .name=="gunicorn") | "\(.name) \(.version)"' sbom-catalog-api-1.0.2.cdx.json
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 143
> flask 3.1.3
> gunicorn 27.0.1
> ```
> 부품 수는 다를 수 있습니다. 내가 `requirements.txt`에 적은 것은 세 줄인데, 실제 이미지에는 **백 개가 넘는 부품**이 들어 있습니다. 대부분은 베이스 이미지와 라이브러리가 데려온 것입니다. `jq`가 없으면 `sudo apt install -y jq`(Mac은 `brew install jq`).

### 단계 3 — 목록만으로 다시 검사

```bash
trivy sbom -q --severity HIGH,CRITICAL sbom-catalog-api-1.0.2.cdx.json | grep "^Total"
```

이미지 없이 **목록 파일만으로** 검사됩니다. 1주차 5일차의 Log4Shell 같은 날, 회사의 이미지 수백 개를 다시 받지 않고 **보관해 둔 SBOM만 검사해** "우리는 영향받는가?"에 몇 분 안에 답할 수 있습니다.

## 실습 20 · Dockerfile 설정 검사

취약점은 부품에만 있지 않습니다. **설정 실수**도 검사합니다.

```bash
trivy config -q --severity HIGH,CRITICAL,MEDIUM,LOW .
```

> **🟢 확인: 이렇게 보입니다 (예시)**
>
> ```text
> Dockerfile (dockerfile)
> Tests: 27 (SUCCESSES: 26, FAILURES: 1)
> Failures: 1 (LOW: 1)
>
> LOW: Add HEALTHCHECK instruction in your Dockerfile
> ```
> `USER`가 없으면 `HIGH: Specify at least 1 USER command`가 나왔을 겁니다. 우리 Dockerfile에는 `USER appuser`가 있어서 통과했습니다. **HEALTHCHECK**는 5일차 Compose에서 다룹니다.

> **🧹 정리: 정리와 커밋**
>
> ```bash
> cd ~/devops-lab
> git add devmart/catalog-api/sbom-catalog-api-1.0.2.cdx.json
> git commit -m "3일차: catalog-api 1.0.2 SBOM"
> git push
> ```
> `trivy-cache` 볼륨은 남겨 둡니다(다음에 빨라짐). `python:3.14` 이미지는 비교용이었으니 지웁니다: `docker rmi python:3.14`

> **🎓 학술 노트 — 부품을 알아야 고칠 수 있다 (NTIA SBOM, 2021)**
>
> 미국 상무부 산하 **NTIA**는 2018년부터 업계와 함께 "소프트웨어에도 식품의 **성분표**가 필요하다"는 논의를 이끌었고, 2021년 대통령 행정명령 14028을 계기로 「SBOM의 최소 요소」를 발표했습니다. 최소 요소는 **공급자 · 부품 이름 · 버전 · 고유 식별자 · 의존 관계 · 작성자 · 작성 시각**입니다. 연구들은 오픈소스 의존성의 대부분이 개발자가 직접 고른 것이 아니라 **간접 의존성(의존성의 의존성)**이라는 점을 반복해서 보여 주었습니다. 오늘 `requirements.txt` 세 줄이 백 개 넘는 부품이 된 것이 그 모습입니다.
>
> - National Telecommunications and Information Administration (2021). *The Minimum Elements For a Software Bill of Materials (SBOM)*. U.S. Department of Commerce.
> - Executive Order 14028 (2021). *Improving the Nation's Cybersecurity*.

> **📈 트렌드 — 스캔에서 'VEX'로: 정말 위험한 것만**
>
> 이미지마다 수십 개씩 나오는 취약점을 모두 고칠 수는 없습니다. 그래서 **"이 취약점은 우리 제품에 실제로 영향이 있는가"**를 기계가 읽을 수 있게 적는 **VEX**(Vulnerability Exploitability eXchange) 형식이 퍼지고 있습니다. 공급자가 "이 CVE는 해당 기능을 쓰지 않아 영향 없음"을 VEX로 함께 배포하면, Trivy 같은 스캐너가 그것을 읽어 결과에서 빼 줍니다. 오늘의 `.trivyignore`를 표준 형식으로, 공급자가 직접 써 주는 방향입니다. 유럽 사이버 복원력법(1주차 5일차)도 제조사에게 SBOM 작성과 취약점 처리를 요구합니다.

## 정리

- Trivy는 **설치 없이 컨테이너로** 실행합니다. `docker.sock` 연결은 믿을 만한 도구에만.
- 결과는 **베이스 OS 패키지**와 **내 라이브러리**로 나뉩니다. `Fixed Version`이 있으면 **`--pull`로 다시 빌드**가 가장 큰 처방입니다.
- `--exit-code 1 --severity CRITICAL`이 **검문소**입니다 → 3주차 CI.
- **SBOM**은 이미지의 부품 목록입니다. 목록만으로 다시 검사할 수 있어 대형 취약점이 터진 날 빠르게 답합니다.
- 넘기는 취약점은 **이유 · 사람 · 기한**을 적습니다(`.trivyignore`, 표준은 VEX).

> **✅ 확인 문제**
>
> 1. Trivy 결과에서 `Status: fixed`, `Fixed Version`이 적힌 취약점을 없애는 가장 쉬운 방법은?
> 2. `docker build`에 `--pull`을 붙이는 이유는?
> 3. 심각한 취약점이 하나라도 있으면 CI를 멈추게 하는 Trivy 옵션 두 개는?
> 4. SBOM을 보관해 두면 새 대형 취약점이 발표된 날 무엇이 빨라지나요?
> 5. 모르는 이미지를 실행할 때 `-v /var/run/docker.sock:/var/run/docker.sock`을 붙이면 안 되는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 베이스 이미지를 새로 받아 다시 빌드합니다(`docker build --pull`).
> 2. 내 컴퓨터에 남은 낡은 베이스 대신 레지스트리의 최신 베이스(보안 패치 포함)로 빌드하려고.
> 3. `--exit-code 1`과 `--severity CRITICAL`(또는 `HIGH,CRITICAL`)
> 4. 이미지를 다시 받지 않고 목록만 검사해서 "우리가 그 부품을 쓰는가"에 바로 답할 수 있습니다.
> 5. 그 컨테이너가 내 Docker 엔진 전체를 조종할 수 있게 되기 때문입니다.
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - 내 앱을 처음 이미지로 만든 소감, 그리고 "내 노트북에 파이썬이 없는데 파이썬 앱이 돈다"를 동료에게 설명해 보기
> - 빌드 캐시 규칙을 블록 탑 비유로 내 말로 다시 써 보기
> - `COPY . .` 실습에서 비밀번호가 보였을 때 든 생각
> - 내 Docker Hub 이미지 주소와 다이제스트 앞 12자리 적어 두기
> - 내일(볼륨·네트워크·환경 변수) 전에 궁금한 것: API와 DB는 어떻게 서로를 찾을까?

## 참고 문헌

- Aqua Security. *Trivy Documentation* — Image scanning, SBOM, Misconfiguration, `.trivyignore`, VEX. trivy.dev
- National Telecommunications and Information Administration (2021). *The Minimum Elements For a Software Bill of Materials (SBOM)*.
- OWASP. *CycloneDX Specification* v1.6. cyclonedx.org
- CISA (2023). *Minimum Requirements for Vulnerability Exploitability eXchange (VEX)*.
- Docker Docs. *docker image build — --pull*; *Protect the Docker daemon socket*.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 멀티 스테이지와 이미지 크기·보안](lesson-07.md) | [⬆️ 3일차 목차](README.md) | [2주차 4일차 목차](../day4/README.md) ➡️ |
