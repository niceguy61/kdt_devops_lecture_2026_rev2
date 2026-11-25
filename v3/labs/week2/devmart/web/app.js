// 같은 주소의 /api/... 로 요청한다. nginx가 catalog-api로 전달해 준다.
async function load() {
  const info = document.getElementById("info");
  const list = document.getElementById("products");
  const source = document.getElementById("source");
  try {
    const i = await (await fetch("/api/info")).json();
    info.textContent = `${i.service} v${i.version} · ${i.env} · 컨테이너 ${i.hostname}`;
  } catch (e) {
    info.textContent = "API에 연결할 수 없습니다 (catalog-api가 실행 중인지 확인하세요)";
  }
  try {
    const res = await fetch("/api/products");
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || res.status);
    source.textContent = data.source === "database" ? "데이터베이스에서 불러옴" : "샘플 데이터";
    list.innerHTML = data.items
      .map((p) => `<li><b>${p.name}</b><span>${p.price.toLocaleString()}원</span></li>`)
      .join("");
  } catch (e) {
    source.textContent = `상품을 불러오지 못했습니다: ${e.message}`;
    source.classList.add("error");
  }
}
load();
