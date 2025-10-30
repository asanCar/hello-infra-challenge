# Infra-challenge

## Application

- The greeting application has been created using Python and FastAPI.
- In the current MVP, only an in-memory database has been implemented. In the future, the application code should be refactored to properly interact with an external DB (e.g. mysql, postgresql).
- For the sake of simplicity, the `routers/hello.py` file has been bloated not only with the FastAPI routers configuration but also with the app's business logic and the in-memory database implementation. In future iterations, this code should be refactored in order to properly separate concerns.

## Helm chart

- The Helm chart assumes the following `Gateway` resource will be already provisioned by the cluster administrator:
  
  ```yaml
  apiVersion: gateway.networking.k8s.io/v1
  kind: Gateway
  metadata:
    name: public-gateway
  spec:
    gatewayClassName: nginx
    listeners:
      - name: http
        protocol: HTTP
        port: 80
        hostname: "*.local"
        allowedRoutes:
          namespaces:
            from: All
  ```

- Resources `requests` and `limits` have been defined for the application's Pod memory. Only `requests` has been defined for the Pod's CPU to prevent CPU throttling from sudden traffic peaks.
