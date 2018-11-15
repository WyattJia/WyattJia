### Istio 是啥

Istio 是 Google、IBM、Lyft 联合推出的 Service mesh 框架。是 Service mesh 概念的具体实现。

###Service Mesh 又是啥?

![架构演进](/Users/jiaweichuan/Documents/blog/assets/架构演进.png)

Service mesh是为了解决微服务体系下服务间通信复杂问题而产生，帮助治理微服务的的产物。其可以提供安全、快速、可靠的服务间通讯，相当无微服务间的 TCP/IP 传输层，负责服务间的调用，限流，熔断和监控等。 

### 为什么选择 Istio 

Istio 可以提供一种简单的方式来为已经部署的微服务架构建立服务间的网络通信。Istio 是非侵入式的，因此不需要对现有服务的代码做任何改动，只需要在部署环境中增加 Istio 的 sidecar 代理即可,通过这层 sidecar 。Istio 就接管了服务间的所有网络，因此就可以使用 Istio 控制平面来来配置和管理 Sidecar，管理服务间所有的网络通信，包括以下所列的功能:

  * HTTP, gRPC, WebSocket 和 TCP 流量的自动负载均衡
  * 通过 Istio 提供的路由规则，重试机制，故障转移和注入等功能，对流量行为进行更加细粒度的控制
  * 可插拔的策略层和配置 API，支持访问控制、速率控制，配额控制等
  * 对集群出入口的流量的自动度量指标、记录和跟踪日志
  * 自带强大的基于身份的验证和授权，在集群中实现安全的服务间通信
  * 可扩展性高

### 核心功能

  * 流量管理
    简化了熔断器，超时，重试的配置，并且可以轻松配置 A/B 测试、金丝雀部署，基于百分比的流量分割分阶段部署
  * 安全
    底层提供安全通信协议，默认情况下是安全地。默认情况下是安全的，几乎不需要应用程序层的更改。
  * 可观察性
    Istio 的 Mixer 组件负责策略控制和遥测手机。
  * 平台支持
    Istio 是基于现有集群平台的，目前 Istio 1.0 版本部署的环境有 :
    * Kubernetes 上部署的服务(这篇文章中会讲到的一种方式)
    * Consul + Nomad 上部署的服务
    * 虚拟机上部署的服务(待验证，官方文档上有提到)
  * 集成定制
  * 架构
    * 数据平台 
      由一组以 sidecar 方式部署的 Envoy 代理组成，这些代理可以调控微服务之间和 Mixer 之间的所有的网络通信。
    * 控制平台
      负责管理和配置代理来路由分发流量，并且用 Mixer 来实施策略和收集数据。
    * 架构图：
      ![istio_arch](/Users/jiaweichuan/Documents/blog/assets/istio_arch.png)

### 与 Envoy 的集成

Istio 使用了 Envoy 的扩展版本作为高性能代理，用于调控 Service mesh 中所有的出站流量和入站流量。Istio 沿用了 Envoy 中许多内置功能，如:

  * 动态服务发现
  * 负载均衡
  * TLS 终止
  * HTTP/2 & gRPC 代理
  * 熔断器
  * 健康检查、基于百分比流量拆分的灰度发布
  * 故障注入
  * 度量指标

Envoy 被部署为 sidecar ，和对应服务放置在同一个 Kubernetes Pod 中，而且 sidecar 的代理模型还可以支持 Istio 功能的热更新。



### Mixer

负责在 service mesh上执行访问控制和使用策略，并从 Envoy 代理和其他服务收集遥测数据。

### Pilot

为 Envoy sidecar 提供服务发现功能，为智能路由和弹性提供流量管理功能，可以将路由规则转换成 Envoy 配置，并分发给 sidecar 。

### Citadel

提供服务间和最终用户身份验证。

---

---

## Quickly start and requirements 

   * minikube
     可参考官方文档 [install-minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)。因为我是在 macOS 上运行的 minikube,所以我选择了 HyperKit 作为我的 Hypervisor 。

   * RBAC 

     k8s 1.8 版本之后，启动 Kubernetes apiserver 的时候需要带参数 `--authorization-mode=RBAC` 。

   * 启动 minikube:
     ```shell
     minikube start \\n    --extra-config=controller-manager.cluster-signing-cert-file="/var/lib/localkube/certs/ca.crt" \\n    --extra-config=controller-manager.cluster-signing-key-file="/var/lib/localkube/certs/ca.key" \\n    --extra-config=apiserver.admission-control="NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,DefaultTolerationSeconds,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota" \\n    --kubernetes-version=v1.10.0 --bootstrapper=localkube --alsologtostderr --vm-driver=hyperkit
     ```

   * 安装 Kuberctl

     使用 homebrew 安装：

     ```shell
     brew install kubernetes-cli
     ```

     其他方式参考[官方文档](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

   * 下载安装 istio 

     1. 直接下载官方 istio 仓库到本地

     ```shell
     curl -L https://git.io/getLatestIstio | sh -
     ```

     2. 解压安装文件，切换到文件所在目录。安装文件目录下包含：
       * install/ 目录下是 Kubernetes 使用的 .yaml 安装文件
       * samples/ 目录下是示例程序
       * istioctl 客户端二进制文件在 bin 目录下。istioctl 文件用户手动注入 Envoy sidecar 代理、创建路由和策略等
       * istio.VERSION 配置文件
     3. 添加 `istioctl` 到 PATH 中：
       ```shell
       $ cd istio-1.0.0
       $ export PATH=$PWD/bin:$PATH
       ```

   * 安装 Istio 核心部分

     官方支持五种安装方式，线上生产环境中官方推荐 Helm Chart 的方式来安装 Istio 。
     但我们选择用默认方式来安装：
     ```shell
     $ kubectl apply -f install/kubernetes/istio-demo-auth.yaml  # 默认会在 sidecar 之间进行双向 TLS 身份验证。
     ```

     其他几种种安装方式分别是：
     * 默认不启用 TLS 认证 `$ kubectl apply -f install/kubernetes/istio.yaml`
       能够与其他非 Istio kubernetes 服务通信。
     * 使用 Helm 渲染出 Kubernetes 配置清单然后使用 kubectl 部署
     * 使用 Helm 和 Tiller 管理 Istio 部署

   * 验证安装

     1. `kubectl get svc -n istio-system`

       确认下列 Kubernetes 服务已经部署：istio-pilot、 istio-ingressgateway、istio-policy、istio-telemetry、prometheus、sidecar-injector（可选）。
       *如果是 minikube 环境中运行的话，需要用 NodePort 来访问。*
     2. `kubectl get pods -n istio-system`
       确保所有相应的Kubernetes pod都已被部署且所有的容器都已启动并正在运行：istio-pilot-*、istio-ingressgateway-*、istio-egressgateway-*、istio-policy-*、istio-telemetry-*、istio-citadel-*、prometheus-*、istio-sidecar-injector-*（可选）


   * 尝试部署应用

     如果启用了 `Istio-Initializer`， 则直接使用 `kubectl create` 直接部署，它会自动向 Pod 中注入 Envoy sidecar。

     *否则的话需要手动注入 Envoy `$ kubectl create -f <(istioctl kube-inject -f <your-app-spec>.yaml)`*

### Bookinfo demo by Istio example

### Bookinfo 简介

  Bookinfo 是由微服务组成的一个异构应用，分别为:
   * productpage: productpage 微服务会调用 details 和 reviews 两个微服务，用来生成页面。
   * details ：这个微服务包含了书籍的信息。
   * reviews ：这个微服务包含了书籍相关的评论。它还会调用 ratings 微服务。
   * ratings ：ratings 微服务中包含了由书籍评价组成的评级信息。
reviews 应用分三个版本:
   * v1 版本不会调用 ratings 服务。
   * v2 版本会调用 ratings 服务，并使用 1 到 5 个黑色星形图标来显示评分信息。
   * v3 版本会调用 ratings 服务，并使用 1 到 5 个红色星形图标来显示评分信息。

    未引入 Istio 之前的 Bookinfo 架构:
    ![bookinfo_without_istio](/Users/jiaweichuan/Documents/blog/assets/bookinfo_without_istio.png)

### 在 K8S 中运行

  * 进入 Istio
    
    ```shell
    cd /path/to/istio-1.0.0
    ```

  * Sidecar 注入

    自动注入 sidecar:
    ```shell
    kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

    ```
    
    手动注入 sidecar:
    ```shell
    $ kubectl apply -f <(istioctl kube-inject -f samples/bookinfo/platform/kube/bookinfo.yaml)

    ```
    
  * 定义 Ingress Gateway

    ```shell
    $ kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
    ```

  * 确认启动
    ```shell
    $ kubectl get services
    NAME                       CLUSTER-IP   EXTERNAL-IP   PORT(S)              AGE
    details                    10.0.0.31    <none>        9080/TCP             6m
    kubernetes                 10.0.0.1     <none>        443/TCP              7d
    productpage                10.0.0.120   <none>        9080/TCP             6m
    ratings                    10.0.0.15    <none>        9080/TCP             6m
    reviews                    10.0.0.170   <none>        9080/TCP 
    ```

    ```shell
    $ kubectl get pods
    NAME                                        READY     STATUS    RESTARTS   AGE
    details-v1-1520924117-48z17                 2/2       Running   0          6m
    productpage-v1-560495357-jk1lz              2/2       Running   0          6m
    ratings-v1-734492171-rnr5l                  2/2       Running   0          6m
    reviews-v1-874083890-f0qf0                  2/2       Running   0          6m
    reviews-v2-1343845940-b34q5                 2/2       Running   0          6m
    reviews-v3-1813607990-8ch52  
    ```
   ```

  * 确定运行情况
   
   ```shell
   $ curl -o /dev/null -s -w "%{http_code}\n" http://127.0.0.1/productpage
   ```
   返回 `200` 即可。

   * 清除
     
     1. 删除路由规则，并终结应用的 Pod

        ```shell
        $ samples/bookinfo/platform/kube/cleanup.sh
        ```

     2. 确认应用已经关停
       
       ```shell
       $ istioctl get gateway           #-- 此处应该已经没有 Gateway
       $ istioctl get virtualservices   #-- 此处应该已经没有 VirtualService
       $ kubectl get pods               #-- Bookinfo 的所有 Pod 应该都已经被删除
       ```

---
---

### To be continued...

