# 8교시: 구름 EXP 배움일기

![Week 3 Day 5 Lesson 8](./assets/lesson-08-kubernetes-voyage-log.png)

## 수업 목표
- Day5에서 확인한 Pod, Deployment, Service, rollout evidence를 정리한다.
- 장애 상태를 "느낌"이 아니라 명령 출력과 event/log로 설명한다.
- Week4의 Helm add-on 탐험으로 이어질 질문을 남긴다.

## 오늘 정리할 핵심
오늘은 Kubernetes object를 많이 외운 날이 아니다. 아래 흐름을 손으로 확인한 날이다.

```text
context 확인
  -> namespace 생성
  -> Pod 실행
  -> Pod 장애 읽기
  -> Deployment로 replica 유지
  -> Service로 내부 접근
  -> rollout 실패와 undo
```

## 배움일기 권장 구조
```markdown
# W3D5 Kubernetes 첫 앱 실행

## 1. 오늘 이해한 개념
- Pod:
- Deployment:
- Service:
- Rollout:

## 2. 오늘 남긴 evidence
- context:
- 첫 Pod 상태:
- ImagePullBackOff event:
- CrashLoopBackOff log:
- Deployment READY:
- Service endpoint:
- curlbox 응답:
- rollout undo 결과:

## 3. 헷갈렸던 지점
- Pod와 container:
- selector와 label:
- Service port와 targetPort:
- rollout과 rollback:

## 4. 다시 해볼 실습
- Pod 장애 재현:
- Service selector 장애:
- 실패 image rollout 후 undo:

## 5. Week4 질문
- Helm:
- metrics-server:
- ingress-nginx:
- Prometheus/Grafana:
- RBAC/Kyverno:
- Argo CD:
- Istio/Kiali:
```

## 오늘의 체크 질문
| 질문 | 스스로 답해보기 |
|---|---|
| `kubectl`은 어디에 요청을 보내는가? | API Server |
| Pod가 삭제되면 직접 Pod와 Deployment Pod는 어떻게 다른가? | controller 유무 |
| `ImagePullBackOff`에서 왜 logs가 없을 수 있는가? | container가 시작하지 못했기 때문 |
| Service endpoint가 비어 있으면 먼저 무엇을 보는가? | selector와 Pod label |
| rollout 실패 후 어떤 명령으로 되돌렸는가? | `kubectl rollout undo` |
| Week4에서 add-on 설치는 어떤 도구로 통일하는가? | Helm |

## Week4 예고
Week4는 오늘 만든 기본 object 위에 운영 도구를 하나씩 얹는다.

| Week4 주제 | Day5와의 연결 |
|---|---|
| Helm + metrics-server | Pod resource 사용량 보기 |
| ingress-nginx | Service를 외부 traffic에 연결 |
| kube-prometheus-stack | Pod/Deployment 상태를 dashboard로 관찰 |
| RBAC + Kyverno | 배포 권한과 policy deny 확인 |
| Argo CD | Git manifest와 cluster 상태 동기화 |
| Istio/Kiali | Service 간 traffic을 mesh로 시각화 |

## 마무리 기준
```text
오늘의 성공은 모든 명령을 외우는 것이 아니다.
실패했을 때 get -> describe -> logs/events -> 복구 순서로 움직일 수 있으면 성공이다.
```

## Evidence Note
```markdown
# W3D5S8 Learning Journal
- 오늘 가장 명확해진 개념:
- 아직 헷갈리는 개념:
- 가장 유용했던 명령:
- 다시 재현할 장애:
- Week4에서 기대하는 plugin/add-on:
```
