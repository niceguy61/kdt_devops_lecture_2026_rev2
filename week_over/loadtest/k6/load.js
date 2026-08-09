import http from 'k6/http';
import { check, sleep } from 'k6';

// Short run for checking the load-test procedure. Override for local execution.
const TARGET = __ENV.TARGET_URL || 'http://app:8080/api/order';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    checks: ['rate>0.95'],
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const headers = { 'X-Trace-Id': `trc_${__VU}_${__ITER}_${Date.now()}` };
  const res = http.get(TARGET, { headers, timeout: '5s' });
  check(res, {
    'HTTP status is 200': (r) => r.status === 200,
    'application response has orderId': (r) => r.status === 200 && r.json().orderId !== undefined,
  });
  sleep(0.5);
}
