import http from 'k6/http';
import { check } from 'k6';
export const options = {
  vus: 20,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<500'], // CI 게이트
    http_req_failed: ['rate<0.01'],
  },
};
export default function(){
  const res = http.get(__ENV.TARGET_URL || 'http://app:8080/api/order');
  check(res, {'status 200': r=>r.status===200});
}