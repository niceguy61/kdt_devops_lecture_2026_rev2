import http from 'k6/http';
import { check, sleep } from 'k6';

const TARGET = __ENV.TARGET_URL || 'http://app:8080/api/health';

export const options = {
  vus: 1,
  duration: '30s',
  thresholds: {
    checks: ['rate>0.99'],
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500'],
  },
};

export default function () {
  const res = http.get(TARGET, { headers: { 'X-Trace-Id': `template_${__VU}_${__ITER}` }, timeout: '5s' });
  check(res, { 'health status is 200': (r) => r.status === 200 });
  sleep(1);
}
