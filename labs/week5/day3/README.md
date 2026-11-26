# 5주차 3일차 실습 파일 — Terraform 기초

| 폴더 · 파일 | 쓰는 곳 | 내용 |
|---|---|---|
| `terraform/01-first/` | 2교시 | 첫 리소스 — S3 버킷 하나, init · plan · apply · destroy |
| `terraform/02-hcl/` | 3 · 4교시 | 변수 · locals · 데이터 소스 · for_each · 참조, 어긋남 · import |
| `terraform/03-backend/` | 5교시 | 원격 state 버킷 (S3 · 버전 관리 · 암호화) |
| `terraform/04-vpc/` | 5 · 6교시 | 1일차 VPC를 모듈로 + 보안 그룹, 원격 state |
| `terraform/05-github-oidc/` | 7교시 | GitHub Actions가 키 없이 맡을 plan 전용 역할 |
| `terraform/.gitignore` | 2교시 | state · tfvars는 Git에 넣지 않는다 |
| `workflows/terraform-plan.yml` | 7교시 | PR마다 fmt · validate · plan |

```bash
mkdir -p ~/devops-lab/aws/w5d3 && cp -r ~/course/labs/week5/day3/* ~/devops-lab/aws/w5d3/
```
