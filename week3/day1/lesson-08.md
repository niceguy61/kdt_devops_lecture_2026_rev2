<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [1일차](README.md) › 8/8교시</sub>

# 8교시 · 서비스 사이의 약속 — API 계약 · 버전 · 하위 호환

> [!NOTE]
> **이번 시간에 할 일**
>
> - 서비스 둘이 주고받는 응답의 모양이 **약속(계약)**이라는 것을 압니다.
> - 카탈로그 팀이 필드 이름 하나를 바꿨을 때 **주문이 어떻게 깨지는지** 직접 봅니다.
> - **안전한 변경**(추가)과 **깨는 변경**(이름 변경 · 삭제 · 타입 변경)을 구분합니다.
> - 이름을 바꿔야 할 때 쓰는 **늘렸다가 줄이기(expand → contract)** 순서를 압니다.
> - 상대 서비스가 지켜야 할 약속을 검사하는 작은 **계약 테스트**를 만듭니다.

> [!IMPORTANT]
> **MSA에서 가장 흔한 장애는 '배포'다**
>
> 7교시의 세 장애는 연결이 끊기거나 설정이 어긋난 경우였습니다. 실제 MSA 장애는 그보다 **서로 다른 팀이 각자 배포한 순간**에 더 자주 납니다. 내 서비스의 테스트는 다 통과했는데, 나를 부르는 **다른 서비스**가 깨지는 것입니다. 2교시에서 "서비스마다 따로 배포한다"를 장점으로 배웠다면, 오늘은 그 장점의 대가를 봅니다.

## 약속은 어디에 있나

DevMart에서 `order-api`는 `catalog-api`에게 상품을 물어보고, 응답의 두 필드를 꺼내 씁니다.

```python
# order-api/app.py (일부)
status, product = get_product(product_id, request_id)
total = product["price"] * quantity          # ← price가 숫자로 와야 한다
... product["name"] ...                      # ← name이 있어야 한다
```

`catalog-api`의 코드 어디에도 "`order-api`가 `price`와 `name`을 쓴다"는 말은 없습니다. 이 약속은 **두 서비스 사이의 빈 공간**에 있습니다. 그래서 깨지기 쉽습니다.

## 실습 5 · 이름 하나 바꿨을 뿐인데

> **🧪 실습: 실습 목표**
>
> 카탈로그 팀 입장에서 "가격이 원화라는 걸 분명히 하자"며 `price`를 `price_krw`로 바꿔 배포하고, 주문 서비스가 깨지는 것을 확인합니다.

### 단계 1 — 지금은 된다

```bash
cd ~/devops-lab/devmart-msa
docker compose up -d
curl -s -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 1, "quantity": 2}'; echo
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> {"order_id":7,"request_id":"…","status":"pending","total_price":118000}
> ```

### 단계 2 — 카탈로그 팀의 '작은' 변경

`catalog-api/app.py`의 상품 하나를 돌려주는 부분(맨 아래 `return`)을 고칩니다.

```python
    return jsonify(id=r[0], name=r[1], price_krw=r[2], stock=r[3])
```

카탈로그 팀은 자기 서비스만 다시 빌드해 배포합니다.

```bash
docker compose up -d --build catalog-api
curl -s http://localhost:8080/api/products/1; echo
```

> **🟢 확인: 카탈로그는 멀쩡하다**
>
> ```text
> {"id":1,"name":"러닝화","price_krw":59000,"stock":…}
> ```
> 카탈로그 팀이 보기에는 잘 배포됐습니다.

### 단계 3 — 그런데 주문이

```bash
curl -s -w '  (HTTP %{http_code})\n' -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 1, "quantity": 2}'
docker compose logs order-api --tail 8 | grep -E "KeyError|Error" | tail -2
```

> **🟢 확인: 깨졌습니다**
>
> ```text
> <!doctype html> … <title>500 Internal Server Error</title> …  (HTTP 500)
> order-api-1  | KeyError: 'price'
> ```
> **장애는 카탈로그가 아니라 주문에서** 났습니다. 주문 팀은 아무것도 바꾸지 않았는데 말입니다. 5교시처럼 요청 ID로 따라가면 원인은 "catalog-api 응답에 `price`가 없다"입니다.

### 단계 4 — 되돌리기

```bash
git restore catalog-api/app.py
docker compose up -d --build catalog-api
```

## 깨는 변경과 안전한 변경

| 변경 | 예 | 기존 소비자(order-api)는? |
|---|---|---|
| 필드 **추가** | `currency: "KRW"`를 더함 | ✓ 모르는 필드는 무시한다 |
| 선택 입력 추가 | 요청에 `coupon`(없어도 됨) | ✓ |
| 필드 **이름 변경** | `price` → `price_krw` | ✗ 오늘 본 것 |
| 필드 **삭제** | `stock`을 뺌 | ✗ 쓰는 곳이 있으면 |
| **타입 변경** | `59000` → `"59,000원"` | ✗ 곱셈이 깨진다 |
| **의미 변경** | 가격에 배송비를 포함 | ✗ **에러 없이** 틀린 값 — 7교시의 회색 장애 |
| 필수 입력 추가 | 요청에 `user_id` 필수 | ✗ 옛 요청이 모두 거절 |
| 주소 변경 | `/api/products/1` → `/api/items/1` | ✗ |

> [!TIP]
> **소비자 쪽의 방어 — 관대하게 읽기**
>
> `order-api`가 `product["price"]` 대신 필요한 필드가 있는지 먼저 확인하고, 없으면 **분명한 에러**(예: `502 catalog contract broken`)를 내면 500보다 훨씬 빨리 원인을 찾습니다. 모르는 필드는 무시하고, 필요한 것만 확인하는 것을 **관대한 독자(tolerant reader)** 패턴이라고 합니다.

## 이름을 꼭 바꿔야 한다면 — 늘렸다가 줄이기

한 번에 바꾸면 깨집니다. 그래서 **세 번에 나눠** 배포합니다.

| 단계 | 카탈로그 | 주문 | 그동안 |
|---|---|---|---|
| ① **늘리기**(expand) | `price`와 `price_krw`를 **둘 다** 보낸다 | 그대로 `price` 사용 | 아무도 깨지지 않음 |
| ② **옮기기**(migrate) | 둘 다 보냄 | `price_krw`를 읽도록 바꿔 배포 | 아무도 깨지지 않음 |
| ③ **줄이기**(contract) | 모든 소비자가 옮긴 걸 **확인한 뒤** `price` 삭제 | — | 아무도 깨지지 않음 |

①을 직접 해 봅니다.

```python
    return jsonify(id=r[0], name=r[1], price=r[2], price_krw=r[2], stock=r[3])
```

```bash
docker compose up -d --build catalog-api
curl -s -w '  (HTTP %{http_code})\n' -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' -d '{"product_id": 1, "quantity": 2}'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> {"order_id":8,…,"total_price":118000}  (HTTP 202)
> ```
> 새 필드를 **더했을 뿐**이므로 주문은 그대로 동작합니다. ③은 "모든 소비자가 옮겼다"는 것을 **어떻게 아느냐**가 어렵습니다. 그래서 다음 실습의 계약 테스트와, 4주차의 관찰(누가 어떤 필드를 호출하는지)이 필요합니다.

> **📘 통째로 바꿔야 할 때 — 버전**
>
> 응답 구조를 크게 바꿔야 하면 주소에 버전을 붙여 **옛 것과 새 것을 함께** 운영합니다: `/api/v1/products/1`(옛), `/api/v2/products/1`(새). 소비자가 모두 v2로 옮긴 뒤 v1을 내립니다. 1주차 4일차 8교시의 "버전을 주소에"가 이것입니다. 큐 메시지도 마찬가지로 `{"v": 1, "order_id": …}`처럼 **메시지 안에 버전**을 넣어 두면, 처리기가 두 형식을 함께 읽을 수 있습니다.

## 실습 6 · 계약 테스트 — 소비자가 약속을 적는다

> **🧪 실습: 실습 목표**
>
> `order-api`가 `catalog-api`에게 기대하는 것을 **실행 가능한 검사**로 적고, 약속이 깨지면 종료 코드 1이 나오게 합니다.

```bash
mkdir -p contract
code contract/catalog-for-order.sh
```

```bash
#!/usr/bin/env bash
# order-api가 catalog-api에게 기대하는 약속 (소비자: order-api)
set -uo pipefail
BASE="${CATALOG_BASE:-http://localhost:8080}"
fail=0

body=$(curl -sf "$BASE/api/products/1") || { echo "✗ 상품 1 조회 실패"; exit 1; }
echo "$body" | jq -e '.name  | type == "string"' >/dev/null && echo "✓ name은 문자열"  || { echo "✗ name"; fail=1; }
echo "$body" | jq -e '.price | type == "number"' >/dev/null && echo "✓ price는 숫자"   || { echo "✗ price"; fail=1; }

code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE/api/products/999999")
[ "$code" = "404" ] && echo "✓ 없는 상품은 404" || { echo "✗ 없는 상품: $code"; fail=1; }

exit $fail
```

- `jq -e` : 결과가 `false`나 `null`이면 **종료 코드 1** — 검사 도구로 쓰기 좋다
- 마지막 검사: `order-api`는 404를 "상품 없음(400)"으로 바꿔 답하므로, **404라는 약속**도 계약의 일부다

```bash
chmod +x contract/catalog-for-order.sh
./contract/catalog-for-order.sh; echo "종료 코드: $?"
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> ✓ name은 문자열
> ✓ price는 숫자
> ✓ 없는 상품은 404
> 종료 코드: 0
> ```

이번에는 깨는 변경(이름 변경)을 다시 넣고 계약 테스트를 돌려 봅니다.

```bash
sed -i 's/price=r\[2\], price_krw=r\[2\]/price_krw=r[2]/' catalog-api/app.py
docker compose up -d --build catalog-api
./contract/catalog-for-order.sh; echo "종료 코드: $?"
```

> **🟢 확인: 배포 전에 잡을 수 있었던 장애**
>
> ```text
> ✓ name은 문자열
> ✗ price
> ✓ 없는 상품은 404
> 종료 코드: 1
> ```
> 이 검사를 **카탈로그 팀의 CI**에서 돌리면, 카탈로그 팀은 배포하기 **전에** "주문 팀과의 약속을 깼다"는 것을 압니다. 내일 GitHub Actions를 배우면 바로 넣을 수 있습니다. (Mac은 `sed -i ''`)

> **🧹 정리: 정리와 커밋**
>
> ```bash
> git restore catalog-api/app.py
> docker compose up -d --build catalog-api
> cd ~/devops-lab
> git add devmart-msa/contract
> git commit -m "3주차 1일차: catalog-api 계약 테스트 (소비자 order-api)"
> git push
> cd ~/devops-lab/devmart-msa && docker compose down
> ```

> **🎓 학술 노트 — '보낼 때는 엄격하게, 받을 때는 너그럽게'와 그 반성**
>
> 인터넷 초기 프로토콜을 만든 **존 포스텔(Jon Postel)**은 TCP 명세(RFC 761, 1980)에 이런 원칙을 적었습니다. **"보낼 때는 보수적으로, 받을 때는 너그럽게(Be conservative in what you do, be liberal in what you accept from others)."** 서로 다른 구현이 섞인 인터넷이 그럭저럭 맞물려 돌아가게 한 이 **견고성 원칙**은 오늘의 "관대한 독자"의 뿌리입니다.
>
> 그런데 40여 년 뒤 IETF는 RFC 9413(2023)에서 이 원칙의 부작용을 정리했습니다. 받는 쪽이 이상한 입력까지 너그럽게 받아 주면, 보내는 쪽은 **틀린 줄 모르고** 계속 틀리게 보내고, 결국 그 이상한 형식이 **사실상의 약속**으로 굳어 아무도 고칠 수 없게 된다는 것입니다. 그래서 오늘날의 권고는 "모르는 **추가** 필드는 무시하되, **필요한 것이 없거나 틀리면 분명하게 실패하라**"입니다. 오늘 계약 테스트가 하는 일이 바로 그것입니다.
>
> - Postel, J. (Ed.). (1980). *RFC 761: DoD Standard Transmission Control Protocol*. §2.10 Robustness Principle.
> - Thomson, M., & Schinazi, D. (2023). *RFC 9413: Maintaining Robust Protocols*. IETF.

> **📈 트렌드 — 약속을 먼저 쓰고, 기계가 지키게**
>
> 큰 조직은 코드를 쓰기 **전에** API 모양을 **OpenAPI**(HTTP API) · **AsyncAPI**(메시지) 명세 파일로 먼저 정하고(API 우선 설계), 그 파일에서 문서 · 클라이언트 코드 · 검사를 자동으로 만듭니다. 명세 두 판을 비교해 **깨는 변경을 PR 단계에서 자동으로 막는** 도구도 흔해졌습니다. 소비자가 기대를 적어 공급자 CI에서 검사하는 방식은 **소비자 주도 계약 테스트**라고 하며, Pact가 대표 도구입니다. 오늘 만든 셸 스크립트가 그 원리를 가장 작게 줄인 모형입니다.

## 정리

- 서비스 사이의 응답 모양은 **계약**입니다. 계약은 어느 한쪽 코드에 있지 않고 **사이에** 있어서 깨지기 쉽습니다.
- **추가는 안전**, 이름 변경 · 삭제 · 타입 변경 · 의미 변경 · 필수 입력 추가는 **깨집니다**.
- 이름을 바꿀 때는 **늘리기 → 옮기기 → 줄이기** 세 번의 배포로. 크게 바꿀 때는 **버전**을 나란히.
- 소비자의 기대를 **계약 테스트**로 적어 공급자 CI에서 돌리면, 배포 전에 잡을 수 있습니다.

> **✅ 확인 문제**
>
> 1. 카탈로그가 응답에 `currency` 필드를 새로 더했습니다. `order-api`는 깨지나요?
> 2. 카탈로그가 `price`를 `"59,000원"`(문자열)으로 바꿨습니다. 무엇이 깨지나요?
> 3. `price` → `price_krw` 이름 변경을 깨지 않고 하는 세 단계는?
> 4. ③ 줄이기 단계가 가장 어려운 이유는?
> 5. 계약 테스트는 누가 쓰고, 어디서 돌리나요?
>
> <details><summary>정답</summary>
>
> 1. 깨지지 않습니다. 모르는 필드는 무시합니다.
> 2. `order-api`의 `price * quantity` 계산(타입이 달라 에러나 틀린 값)
> 3. ① 둘 다 보내기(늘리기) ② 소비자가 새 이름으로 옮기기 ③ 옛 이름 지우기(줄이기)
> 4. 옛 필드를 쓰는 소비자가 **하나도 없다는 것**을 확인하기 어렵기 때문입니다.
> 5. 소비자(여기서는 order-api 쪽)가 기대를 적고, 공급자(catalog-api)의 CI에서 배포 전에 돌립니다.
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - 모놀리식과 MSA를 '대형 식당과 푸드코트' 말고 **내 비유**로 설명해 보기
> - DevMart MSA 여섯 서비스의 역할을 한 줄씩, 그리고 주문 하나가 지나가는 길
> - 요청 ID로 로그를 이어 읽었을 때, 가장 오래 걸린 구간과 그 이유
> - 동기와 비동기 — 내가 아는 서비스(배달 앱, 은행 앱)에서 각각 어디에 쓰일지
> - 장애 3(조용한 장애)을 처음 봤을 때 무엇부터 의심했는지, 실제 원인은 무엇이었는지
> - 내일(장애 전파 + CI) 전에 궁금한 것: catalog-api가 **느려지면** order-api는 어떻게 될까?

## 참고 문헌

- Postel, J. (Ed.). (1980). *RFC 761: DoD Standard Transmission Control Protocol*.
- Thomson, M., & Schinazi, D. (2023). *RFC 9413: Maintaining Robust Protocols*. IETF.
- Fowler, M. (2011). *TolerantReader*; Sato, D. (2014). *ParallelChange*. martinfowler.com
- Newman, S. (2021). *Building Microservices* (2nd ed.). O'Reilly. — 7장 Testing (consumer-driven contracts)
- OpenAPI Initiative. *OpenAPI Specification*. spec.openapis.org; AsyncAPI Initiative. *AsyncAPI Specification*.
- Pact Foundation. *Pact Documentation — Consumer-driven contract testing*. docs.pact.io

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 장애 시나리오 1 — 연결이 끊겼다](lesson-07.md) | [⬆️ 1일차 목차](README.md) | [3주차 2일차 목차](../day2/README.md) ➡️ |
