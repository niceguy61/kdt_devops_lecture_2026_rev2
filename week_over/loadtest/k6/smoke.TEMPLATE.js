
import http from 'k6/http';
import { check } from 'k6';
const TARGET = __ENV.TARGET_URL || 'http://localhost:8080/api/health';
export const options = {
  vus: 1, duration: '30s',
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'] },
};
export default function(){
  const res = http.get(TARGET, { headers: { 'X-Trace-Id': `trc_${Date.now()}` }});
  check(res, { '200': r=>r.status===200 });
}
