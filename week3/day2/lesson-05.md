[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [2일차](README.md)

# 5교시 · PR마다 자동 테스트

> [!NOTE]
> **이번 시간에 할 일**
>
> - 오늘 받은 **단위 테스트**를 읽고, Docker로 내 노트북에서 먼저 돌려 봅니다.
> - CI 워크플로의 **테스트 부분**을 한 줄씩 읽습니다 (트리거 · 경로 필터 · 매트릭스 · 권한).
> - 브랜치 → PR을 열어 자동 테스트가 도는 것을 봅니다.
> - 테스트를 일부러 깨뜨려 **빨간 X**를 보고, 로그를 읽고 고칩니다.

## 테스트부터 읽기

CI가 할 일 중 가장 중요한 것은 **테스트**입니다. 테스트가 없으면 CI는 "빌드가 되는지"만 알려 줍니다. 오늘 받은 `order-api/tests/test_app.py`를 봅니다.

```python
"""order-api 단위 테스트 — DB · Redis · catalog-api 없이 돌아간다 (3주차 2일차 CI)."""
import app as order


def client():
    order.app.config["TESTING"] = True
    return order.app.test_client()


def test_health_ok():
    res = client().get("/health")
    assert res.status_code == 200


def test_ready_fails_without_dependencies(monkeypatch):
    # 의존 서비스가 없으면 /ready 는 503 — /health 와 다르다
    monkeypatch.delenv("DB_HOST", raising=False)
    monkeypatch.setattr(order, "REDIS_HOST", "127.0.0.1")
    res = client().get("/ready")
    assert res.status_code == 503
    assert res.get_json()["status"] == "not ready"


def test_order_returns_503_when_catalog_is_down(monkeypatch):
    # 상품 서비스가 응답하지 않으면 주문을 저장하지 않고 503을 돌려줘야 한다
    monkeypatch.setattr(order, "CATALOG_URL", "http://127.0.0.1:9")
    monkeypatch.setattr(order, "CATALOG_TIMEOUT", 0.5)
    res = client().post("/api/orders", json={"product_id": 1})
    assert res.status_code == 503
    assert res.get_json()["error"] == "catalog unavailable"
```

| 부분 | 뜻 |
|---|---|
| `def test_…():` | `pytest`는 `test_`로 시작하는 함수를 찾아 실행한다 |
| `app.test_client()` | 서버를 띄우지 않고 Flask 앱에 **가짜 요청**을 보낸다 |
| `assert 조건` | 조건이 거짓이면 그 테스트는 **실패** |
| `monkeypatch` | 테스트 동안만 환경 변수나 설정을 바꿔 둔다 (끝나면 원래대로) |

눈여겨볼 점은 **오늘 오전에 손으로 확인한 것**이 그대로 테스트가 되었다는 것입니다. "/health는 의존 서비스 없이도 ok", "/ready는 의존 서비스가 없으면 503", "catalog-api가 죽으면 503". 사람이 한 번 확인한 것을 **기계가 매번** 확인하게 만드는 것, 그것이 테스트입니다. 그리고 이 테스트들은 DB · Redis 없이도 돌기 때문에 CI 러너에서 빠르게 끝납니다.

## 실습 12 · 내 노트북에서 먼저 돌리기

CI에 올리기 **전에** 로컬에서 돌려 봅니다. 파이썬을 설치할 필요 없이, 2주차에 배운 Docker로 돌립니다.

```bash
cd ~/devops-lab/devmart-msa/order-api
docker run --rm -v "$PWD":/app -w /app python:3.14-slim \
  sh -c "pip install -q -r requirements-dev.txt && python -m pytest -v"
```

- `-v "$PWD":/app -w /app` : 지금 폴더를 컨테이너의 `/app`에 붙이고 거기서 실행 (2주차 4일차 바인드 마운트)
- `--rm` : 끝나면 컨테이너를 지운다

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> tests/test_app.py::test_health_ok PASSED                                  [ 33%]
> tests/test_app.py::test_ready_fails_without_dependencies PASSED           [ 66%]
> tests/test_app.py::test_order_returns_503_when_catalog_is_down PASSED     [100%]
> ============================== 3 passed in 5.81s ===============================
> ```
> `catalog-api` 폴더에서도 같은 명령으로 3개가 통과하는지 확인합니다.

> [!TIP]
> **로컬에서 먼저, CI는 확인용**
>
> CI에서 처음 실패를 발견하면, 고치고 push 하고 기다리기를 반복하느라 시간이 걸립니다. 같은 명령을 **로컬에서 먼저** 돌리는 습관을 들이면 CI는 "다른 사람 컴퓨터에서도 되는지" 확인하는 마지막 관문이 됩니다.

## CI 워크플로 읽기 — 테스트 부분

강의 저장소의 `labs/week3/day2/.github/workflows/devmart-ci.yml`은 잡이 셋입니다. 이번 교시는 앞의 두 잡(`test`, `compose-check`)을 읽고, 6교시에 `build`를 읽습니다.

```yaml
name: devmart-ci

on:
  pull_request:                       # PR을 열거나 새 커밋을 올릴 때
    paths:
      - "devmart-msa/**"
      - ".github/workflows/devmart-ci.yml"
  push:
    branches: [main]                  # main에 합쳐졌을 때
    paths:
      - "devmart-msa/**"
      - ".github/workflows/devmart-ci.yml"

permissions:
  contents: read                      # 기본은 읽기만 (최소 권한)

jobs:
  test:
    name: test (${{ matrix.service }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [catalog-api, order-api]
    defaults:
      run:
        working-directory: devmart-msa/${{ matrix.service }}
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.14"
          cache: pip
          cache-dependency-path: devmart-msa/${{ matrix.service }}/requirements*.txt
      - name: 의존성 설치
        run: pip install -r requirements-dev.txt
      - name: 단위 테스트
        run: python -m pytest -v

  compose-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: compose.yaml 문법 검사
        working-directory: devmart-msa
        env:
          DB_PASSWORD: ci-dummy-not-secret
        run: docker compose config --quiet
```

| 부분 | 뜻 | 왜 |
|---|---|---|
| `pull_request` + `push: branches: [main]` | PR에서 한 번, 합쳐진 뒤 main에서 한 번 | PR에서 미리 막고, main은 최종 확인 |
| `paths:` | `devmart-msa/` 아래가 바뀔 때만 | README만 고쳤는데 CI가 도는 낭비를 막는다 |
| `permissions: contents: read` | 이 워크플로의 토큰은 **읽기만** | 액션이 해킹돼도 저장소를 고칠 수 없게 (4교시) |
| `strategy.matrix.service` | 같은 잡을 값만 바꿔 **두 번 동시에** | 서비스가 늘어도 줄 하나만 추가 |
| `working-directory` | 명령을 그 폴더에서 실행 | 서비스 폴더마다 `requirements-dev.txt`가 있다 |
| `setup-python` + `cache: pip` | 파이썬 3.14 설치, 받은 패키지를 다음 실행에 재사용 | 두 번째부터 설치가 빨라진다 |
| `DB_PASSWORD: ci-dummy-not-secret` | `compose.yaml`의 `${DB_PASSWORD:?…}`를 통과시키는 가짜 값 | **문법만** 검사하므로 진짜 비밀번호가 필요 없다 |

> **📖 용어 — 매트릭스(matrix)**
>
> 같은 잡을 여러 값의 조합으로 펼쳐 실행하는 기능입니다. `service: [catalog-api, order-api]`면 잡이 2개, 여기에 `python: ["3.13", "3.14"]`를 더하면 2 × 2 = 4개가 동시에 돕니다. 화면에는 `test (catalog-api)`, `test (order-api)`처럼 따로 보입니다.

## 실습 13 · PR에서 자동 테스트 보기

> **🧪 실습: 실습 목표**
>
> 워크플로를 브랜치에 추가하고 PR을 열어, 체크가 자동으로 도는 것을 봅니다.

```bash
cd ~/devops-lab
git switch main && git pull
git switch -c ci/devmart-tests
cp ~/course/labs/week3/day2/.github/workflows/devmart-ci.yml .github/workflows/
git add .github/workflows/devmart-ci.yml
git commit -m "CI: DevMart 테스트 · compose 검사 · 이미지 빌드"
git push -u origin ci/devmart-tests
gh pr create --title "CI: DevMart 자동 테스트" --body "PR마다 테스트와 compose 검사, main에서 이미지 push"
gh pr checks --watch
```

- `gh pr checks --watch` : 이 PR의 자동 검사가 끝날 때까지 실시간으로 보여 준다

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> ✓  test (catalog-api)        18s
> ✓  test (order-api)          24s
> ✓  compose-check             9s
> ✓  build (catalog-api)       41s
> ✓  build (order-api)         43s
> ✓  build (order-worker)      38s
> ```
> PR 화면 아래쪽에도 **All checks have passed**와 초록 체크들이 보입니다. `build` 잡도 돌았는데, PR에서는 **빌드만 하고 올리지는 않습니다**(6교시).
>
> 잡이 `test` 2개 · `compose-check` 1개가 먼저 **동시에** 돌고, 셋이 모두 성공한 뒤에 `build` 3개가 돕니다. `build`에 적힌 `needs: [test, compose-check]` 때문입니다.

## 실습 14 · 테스트를 깨뜨려 보기

> **🧪 실습: 실습 목표**
>
> 누군가 실수로 `/health` 응답을 바꿨다고 가정하고, CI가 그것을 잡아내는지 봅니다.

`devmart-msa/order-api/app.py`의 `health()`를 고칩니다.

```python
@app.get("/health")
def health():
    return jsonify(status="ok"), 500       # 실수로 500을 돌려주게 됨
```

```bash
git commit -am "order-api: health 수정 (실수)"
git push
gh pr checks --watch
```

> **🟢 확인: 보이는 것 — 빨간 X**
>
> ```text
> ✓  test (catalog-api)        17s
> X  test (order-api)          22s
> ✓  compose-check             8s
> -  build (catalog-api)       (건너뜀)
> -  build (order-api)         (건너뜀)
> -  build (order-worker)      (건너뜀)
> ```
> `test (order-api)`만 실패했고, `build` 셋은 **실행조차 되지 않았습니다.** 테스트를 통과하지 못한 코드로는 이미지를 만들지 않습니다.

### 실패 로그 읽기

```bash
gh run view --log-failed | tail -15
```

- `--log-failed` : 실패한 스텝의 로그만 보여 준다

> **🟢 확인: 보이는 것**
>
> ```text
> test (order-api)  단위 테스트  FAILED tests/test_app.py::test_health_ok - assert 500 == 200
> test (order-api)  단위 테스트  ========================= 1 failed, 2 passed in 6.02s =========================
> test (order-api)  단위 테스트  ##[error]Process completed with exit code 1.
> ```
> 읽는 순서: **어느 잡**(`test (order-api)`) → **어느 스텝**(`단위 테스트`) → **어느 테스트**(`test_health_ok`) → **무엇이 달랐나**(`500 == 200`, 실제 500 · 기대 200). 원인이 정확히 한 줄로 나옵니다.

`500`을 지워 원래대로 되돌리고 다시 올립니다.

```bash
git commit -am "order-api: health 되돌리기"
git push
gh pr checks --watch
```

모두 초록이 되면 **아직 병합하지 않습니다.** 6교시에 병합하면서 이미지 push를 봅니다.

> **❓ 오해 — '테스트가 통과했으니 버그가 없다'**
>
> 테스트는 **적어 둔 것만** 확인합니다. 오늘 테스트는 "주문 금액 계산이 맞나", "큐 이름이 서로 맞나"를 확인하지 않습니다. 어제 장애 3(큐 이름 불일치)은 이 테스트를 모두 통과합니다. 그래서 장애를 겪을 때마다 **그 장애를 잡는 테스트나 검사를 하나씩 추가하는 것**이 좋은 습관입니다. 3교시 장애 보고서의 "재발 방지" 칸에 "CI에 검사 추가"가 자주 들어가는 이유입니다.

> **🎓 학술 노트 — 테스트 피라미드와 '빠른 되먹임'**
>
> 마이크 콘(Mike Cohn)은 『Succeeding with Agile』(2009)에서 **테스트 피라미드**를 제안했습니다. 맨 아래에 빠르고 많은 **단위 테스트**, 가운데에 서비스끼리 엮어 보는 **통합 테스트**, 맨 위에 화면까지 끝에서 끝으로 확인하는 **E2E 테스트**를 적게 두라는 것입니다. 위로 갈수록 느리고, 깨지기 쉽고, 비싸기 때문입니다.
>
> 이 피라미드의 핵심 가치는 **빠른 되먹임(fast feedback)**입니다. 1주차 1일차에 본 DORA 연구도 "개발자가 몇 분 안에 테스트 결과를 받는 것"을 고성과 팀의 특징으로 꼽았습니다. 오늘 단위 테스트는 DB 없이 몇 초에 끝납니다. 내일 이후 서비스가 Kubernetes에 올라가면, 실제 DB · Redis와 함께 띄워 확인하는 통합 테스트(2주차 4일차 트렌드의 Testcontainers)를 피라미드의 가운데에 추가할 수 있습니다.
>
> - Cohn, M. (2009). *Succeeding with Agile: Software Development Using Scrum*. Addison-Wesley.

> **📈 트렌드 — AI가 쓴 코드일수록 CI가 마지막 관문**
>
> 1주차 1일차에 본 Octoverse 2026에서 PR의 40% 이상을 AI 에이전트가 시작했습니다. 사람이 한 줄씩 쓰던 때보다 코드가 훨씬 빨리, 많이 들어옵니다. 그만큼 **사람의 리뷰만으로는** 모든 변경을 꼼꼼히 볼 수 없게 되었고, 자동 테스트와 검사가 **품질의 바닥**을 지키는 역할이 커졌습니다. 많은 팀이 "에이전트가 만든 PR은 CI가 초록이어야 사람 리뷰를 요청할 수 있다"는 규칙을 둡니다. 7교시에 만드는 main 보호 규칙이 그 장치입니다.

## 정리

- 테스트 = 사람이 한 번 확인한 것을 **기계가 매번** 확인. DB 없이 빨리 도는 단위 테스트부터.
- **로컬(Docker)에서 먼저**, CI는 마지막 관문.
- 워크플로: `pull_request` + `push main`, `paths:`로 필요할 때만, `permissions`는 최소, `matrix`로 서비스마다.
- `needs:` — 테스트를 통과해야 빌드한다.
- 실패 로그는 **잡 → 스텝 → 테스트 → 기대와 실제** 순서로 읽는다 (`gh run view --log-failed`).

> **✅ 확인 문제**
>
> 1. `test_ready_fails_without_dependencies`가 확인하는 것은?
> 2. `paths:`를 넣은 이유는?
> 3. 매트릭스 `service: [catalog-api, order-api]`는 잡을 몇 개 만드나요?
> 4. `test (order-api)`가 실패했을 때 `build` 잡들이 실행되지 않은 이유는?
> 5. `assert 500 == 200`에서 500과 200은 각각 무엇인가요?
>
> <details><summary>정답</summary>
>
> 1. 의존 서비스(DB · Redis)가 없으면 /ready가 503과 "not ready"를 돌려주는지
> 2. devmart-msa나 워크플로 파일이 바뀔 때만 CI를 돌려 시간과 비용을 아끼려고
> 3. 2개 (서비스마다 하나, 동시에)
> 4. build에 `needs: [test, compose-check]`가 있어 앞 잡이 모두 성공해야 시작하기 때문
> 5. 500은 실제로 받은 값, 200은 테스트가 기대한 값
>
> </details>

## 참고 문헌

- pytest Docs. *Getting started*, *monkeypatch*. docs.pytest.org
- Flask Docs. *Testing Flask Applications*. flask.palletsprojects.com
- GitHub Docs. *Workflow syntax — on.paths, jobs.<id>.strategy.matrix, jobs.<id>.needs, permissions*. docs.github.com/actions
- actions/setup-python. *Caching packages dependencies*. github.com/actions/setup-python
- Cohn, M. (2009). *Succeeding with Agile*. Addison-Wesley.

---

⬅️ 이전: [4교시 · GitHub Actions 개념과 첫 워크플로](lesson-04.md) &nbsp;|&nbsp; [⬆️ 2일차 목차](README.md) &nbsp;|&nbsp; 다음: [6교시 · 이미지 자동 빌드와 GHCR](lesson-06.md) ➡️
