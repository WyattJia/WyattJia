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

---

### Pod

---

### Node

---

### Namespace

---

### Service

---

### Label

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