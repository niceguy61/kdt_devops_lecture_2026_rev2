# Week 1 Foundations Scorecard

## Purpose
이 평가표는 Week 1 산출물이 컴퓨팅 spine, 실행 증거, handoff, 학술/현업 기준을 충족하는지 확인한다.

## Critical Gates
| Condition | Verdict |
|---|---|
| secret, token, password, MFA code, payment information exposed | rebuild_required |
| paid API or cloud resource required for Week 1 deliverable | rebuild_required |
| mini app cannot run from README | repair_required |
| no command/status/log evidence | repair_required |
| Docker/AWS/Kubernetes/DORA/Well-Architected taught as standalone Week 1 topic | repair_required |
| no mapping to computing spine | repair_required |

## 0/1/2 Rubric
| Criterion | 0 | 1 | 2 | Evidence |
|---|---|---|---|---|
| computing_spine | terms missing | partial mapping | local evidence mapped to future platforms | mapping note |
| reproducibility | cannot run | runs with missing context | clean start/check/stop documented | README |
| observability | no evidence | screenshot only | command, status, log/RCA | log/status/RCA |
| professional_handoff | vague explanation | README only | README, risk, blocker, next action | handoff pack |
| security_cost_safety | unsafe exposure | principle only | no secret, no paid dependency | scan/note |
| academic_alignment | decorative links | some outcomes | observable action and scoring evidence | day academic files |

## Academic/Workforce Mapping
| Standard | Week 1 observable action | Artifact |
|---|---|---|
| ABET-style computing practice | Use computing tools and document evidence | repo, README, command output |
| ABET-style communication | Explain service execution to another operator | presentation card |
| CS2023 competency | Apply systems concepts to a running service | computing spine note |
| NIST NICE-style task/skill | Identify access, secret, and system-state risks | risk table |
| Bloom apply/analyze/evaluate | Run, inspect, diagnose, justify scope | RCA and mapping note |
