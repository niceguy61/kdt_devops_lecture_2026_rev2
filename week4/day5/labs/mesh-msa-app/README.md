# Mesh MSA App

Istio/Kiali에서 service-to-service graph를 보기 위한 작은 MSA 샘플이다.

```text
frontend
  -> bff
      -> catalog
      -> inventory
      -> order
          -> inventory
          -> payment
```

`frontend`는 traffic generator 역할만 한다. 실제 사용자 화면을 제공하는 목적이 아니라 Kiali graph와 Envoy access log에서 통신 구조를 확인하기 위한 샘플이다.

## Apply
```bash
kubectl apply -f week4/day5/labs/mesh-msa-app/namespace.yaml
kubectl apply -f week4/day5/labs/mesh-msa-app/deployments.yaml
kubectl apply -f week4/day5/labs/mesh-msa-app/services.yaml
```

## Verify
```bash
kubectl -n mesh-msa-demo get pod,svc
kubectl -n mesh-msa-demo logs deploy/frontend -c traffic-generator --tail=20
kubectl -n mesh-msa-demo logs deploy/bff -c istio-proxy --tail=20
```

Kiali에서 `mesh-msa-demo` namespace를 선택하고 graph를 확인한다.

## If Kiali Graph Is Empty
The sample generates internal traffic automatically from the `frontend`
deployment. First prove that traffic exists:

```bash
kubectl -n mesh-msa-demo logs deploy/frontend -c traffic-generator --tail=20
kubectl -n mesh-msa-demo logs deploy/frontend -c istio-proxy --tail=20
kubectl -n mesh-msa-demo logs deploy/bff -c istio-proxy --tail=20
```

If the proxy logs show requests but Kiali still has no graph, Prometheus is
probably not scraping Istio sidecar metrics. Enable the scrape config:

```bash
bash week4/day5/labs/istio/enable-istio-prometheus-scrape.sh
```

Wait 30-60 seconds and verify that Istio metrics are present:

```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-prometheus 9090:9090
```

Open this Prometheus query:

```text
http://localhost:9090/api/v1/query?query=istio_requests_total
```

In Kiali, select namespace `mesh-msa-demo`, set the graph range to `Last 5m` or
`Last 10m`, and refresh.

## Fault Injection Preview
```bash
kubectl apply -f week4/day5/labs/mesh-msa-app/virtualservice-order-delay.yaml
kubectl -n mesh-msa-demo get virtualservice
```

## Cleanup
```bash
kubectl delete -f week4/day5/labs/mesh-msa-app/virtualservice-order-delay.yaml --ignore-not-found
kubectl delete namespace mesh-msa-demo --ignore-not-found
```
