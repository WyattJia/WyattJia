## 常用命令

* pod 就是 container group ，捆绑管理网络。

  使用 `kubectl run` 命令创建一个 pod 。

* pod 创建完成后就是一个 *deployment* ，可以使用 deployment 创建和扩容 pod 

  * 使用 `kubectl get deployments` 查看 deployment 运行情况

  ```shell
  ➜  Desktop git:(master) kubectl get deployment
  NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
  hello-minikube   1         1         1            0           12d
  hello-node       1         1         1            0           3d
  ```

  * 使用 `kubectl get pods` 查看通过 deployments 创建的 pod 的运行情况

  ```shell
  ➜  Desktop git:(master) kubectl get pods
  NAME                              READY     STATUS              RESTARTS   AGE
  hello-minikube-7c77b68cff-t7xv2   0/1       ContainerCreating   0          12d
  hello-node-6b88b9bc77-fqg2w       0/1       ContainerCreating   0          3d
  ```

  * 查看 pod 日志

    ```shell
    kubectl logs <pod-name>
    ```
  
  * 查看集群元数据运行情况 

    ```shell
    kubectl cluster-info
    ```

  * 查看集群事件

    ```shell
    kubectl get events
    ```
    
---
---

## 基本概念 

### Container

Docker container， rkt container。镜像的运行时就是容器。

---

### Pod

用 Pod 管理容器，一个 Pod 包括一个或者多个容器。容器间共享 PID， IPC， Network,UTS Namespace, 是 Kubernetes 的基本调度单位。有点类似 docker-compose 的一个 stack 。

Kubernetes 中的所有对象都使用 manifest 来定义，如 json 或者 yaml 。一个 nginx 服务就可以定义为 nginx.yaml，其中包含一个 nginx 镜像的容器。

Pod 对象示例：

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: nginx
    labels:
        app: nginx
spec:
    containers:
    - name: nginx
      image: nginx
      ports:
      - containerPort: 80
```

---

### Node

Node（节点） 是 Pod 运行主体。为了方便管理，每个 Node 上面都会有 container runtime ，常见的 container runtime 是 docker 或者 rkt 。以及还需要有 `kubelet`（维护容器生命周期， volumn、 网络管理等等）、`kuber-proxy`（负载均衡，服务发现等） 等 node processes （节点共用工具）。 

---

### Namespace

一组资源和对象的抽象集合。

---

### Service

应用服务的抽象，通过 labels 提供负载均衡和服务发现。匹配 labels 的 Pod IP PORTS 组成的 endpoints ，由 kube-proxy 负责将 ip 负载均衡到这些 endpoints 上面。 

没有 service 都会分配一个 cluster ip 和 DNS ，仅 cluster 内部可以访问。集群内部的容器都通过该地址和 DNS 来访问服务。

example:

```yaml
apiVerson: v1
kind: Service
metadata:
  name: nginx
spec:
  port: 8078 # the port that this service should serve on
  name: http
  targetPort: 80
  protocol: TCP
selector:
  app: nginx

```

---

### Label

识别 Kubernetes 对象的标签，以键值对的方式附加到对象上，不唯一。label 定义好之后，其他对象可以使用 Label Selector 来选择一组相同label 的对象。

Label Selector example:
  * 等式 `app=nginx` `env!=production`
  * 集合 `env in (production, qa)`
  * 多个 label `and` 关系 `app=nginx, env=test`

---

### Annotations

Annotations 是 key/value 形式附加于对象的注解。不同于 Labels 用于标志和选择对象，Annotations 则是用来记录一些附加信息，用来辅助应用部署、安全策略以及调度策略等。比如 deployment 使用 annotations 来记录 rolling update 的状态。

---
---

## 核心组件

* etcd 
  分布式键值对存储，保存了整个集群的状态

* apiserver
  资源操作的唯一入口，提供认证、授权、访问、控制、API注册和服务发现等机制

* controller manager 
  负责维护集群状态，比如故障检测、自动扩展（auto scale）、滚动更新(roll update) 等功能

* scheduler 
  负责资源的调度，按照调度策略将 pod 调度到相应的机器上。

* kublet
  维护容器的生命周期，维护 Volume 和网络管理。

* container runtime
  镜像管理和 Pod 与容器的运行

* kube-proxy
  为 Service 提供 cluster 内部的服务发现和负载均衡。