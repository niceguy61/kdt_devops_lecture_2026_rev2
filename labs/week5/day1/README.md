# 5주차 1일차 실습 파일 — AWS 계정과 VPC

| 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `s3-read-only-policy.json` | 3교시 | IAM 정책 읽기 연습 (Allow · Deny · Resource) |
| `check-account.sh` | 4 · 7교시 | 내 계정 상태 — 신원 · MFA · 예산 · VPC · 돈이 나가는 것 |

```bash
mkdir -p ~/devops-lab/aws/w5d1 && cp -r ~/course/labs/week5/day1/* ~/devops-lab/aws/w5d1/
```

!!! warn "이번 주의 약속"
    클라우드 자원은 **켜 두는 시간만큼** 돈이 나갑니다. 매일 7교시에 `check-account.sh`로 남은 것을 확인하고, 그날 만든 것은 그날 지웁니다(VPC처럼 요금이 없는 것만 다음 날까지 둡니다).
