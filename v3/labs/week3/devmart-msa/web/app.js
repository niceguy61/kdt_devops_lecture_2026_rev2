// 같은 주소의 /api/... 로 요청한다. nginx가 주소를 보고 알맞은 서비스로 넘겨 준다.
async function loadProducts() {
  const list = document.getElementById("products");
  const source = document.getElementById("source");
  try {
    const i = await (await fetch("/api/info")).json();
    document.getElementById("info").textContent = `catalog-api v${i.version} · ${i.env} · 컨테이너 ${i.hostname}`;
    const res = await fetch("/api/products");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || res.status);
    source.textContent = "상품 서비스 정상";
    list.innerHTML = data.items.map((p) =>
      `<li><b>${p.name}</b><span>${p.price.toLocaleString()}원 · 재고 ${p.stock}</span>
       <button onclick="order(${p.id})">주문하기</button></li>`).join("");
  } catch (e) {
    source.textContent = `상품을 불러오지 못했습니다: ${e.message}`;
    source.classList.add("error");
  }
}

async function order(productId) {
  const res = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 }),
  });
  const data = await res.json();
  if (!res.ok) alert(`주문 실패 (${res.status}): ${data.error}\n요청 ID: ${data.request_id}`);
  loadOrders();
}

async function loadOrders() {
  const body = document.querySelector("#orders tbody");
  try {
    const res = await fetch("/api/orders");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || res.status);
    body.innerHTML = data.items.map((o) =>
      `<tr><td>${o.id}</td><td>${o.product_name}</td><td>${o.quantity}</td>
       <td>${o.total_price.toLocaleString()}원</td><td class="st-${o.status}">${o.status}</td>
       <td><code>${(o.request_id || "").slice(0, 8)}</code></td></tr>`).join("");
  } catch (e) {
    body.innerHTML = `<tr><td colspan="6" class="error">주문 서비스에 연결할 수 없습니다: ${e.message}</td></tr>`;
  }
}

loadProducts();
loadOrders();
setInterval(loadOrders, 2000); // 2초마다 주문 상태를 다시 읽는다
