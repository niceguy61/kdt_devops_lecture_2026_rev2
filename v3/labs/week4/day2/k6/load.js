// 5교시 · DevMart 부하 테스트 — 상품 보기 4번에 주문 1번 꼴로
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://host.docker.internal:30080';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // 30초 동안 사용자 0 → 10명
    { duration: '2m', target: 10 },    // 10명 유지
    { duration: '30s', target: 0 },    // 정리
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],            // 실패 1% 미만
    http_req_duration: ['p(95)<500'],          // 느린 쪽 5%도 0.5초 안에
  },
};

export default function () {
  const r = Math.random();
  if (r < 0.8) {
    const res = http.get(`${BASE}/api/products`, { tags: { name: 'products' } });
    check(res, { '상품 200': (x) => x.status === 200 });
  } else {
    const res = http.post(`${BASE}/api/orders`, JSON.stringify({ product_id: 1 + Math.floor(Math.random() * 5) }),
      { headers: { 'Content-Type': 'application/json' }, tags: { name: 'orders' } });
    check(res, { '주문 202': (x) => x.status === 202 });
  }
  sleep(0.5);
}
