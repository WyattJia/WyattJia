Minikube Features
  Minikube supports Kubernetes features such as:
    * DNS
    * NodePorts
    * ConfigMaps and Secrets
    * Dashboards
    * Container Runtime: Docker, rkt and CRI-O
    * Enabling CNI (Container Network Interface)
    * Ingress

Start minikube on macOS.

```shell
minikube start --bootstrapper=localkube --vm-driver hyperkit
```
