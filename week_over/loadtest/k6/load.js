import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const headers = { 'X-Trace-Id': `trc_${Date.now()}` };
  const res = http.get('http://localhost:8080/api/order', { headers });
  check(res, { '200 and p95 ok': (r) => r.status === 200 });
}