const statusBox = document.querySelector("#status");
const serviceList = document.querySelector("#service-list");

function setStatus(message, type) {
  statusBox.textContent = message;
  statusBox.className = `status ${type}`;
}

function renderServices(services) {
  serviceList.innerHTML = "";
  for (const service of services) {
    const item = document.createElement("li");
    item.textContent = `${service.name}: ${service.check}`;
    serviceList.appendChild(item);
  }
}

async function loadData() {
  try {
    const response = await fetch("./data.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    setStatus(data.message, "ok");
    renderServices(data.services);
  } catch (error) {
    setStatus(`데이터를 불러오지 못했습니다: ${error.message}`, "error");
    console.error("Sample app data load failed", error);
  }
}

loadData();
