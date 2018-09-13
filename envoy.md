## 快速上手

在更深入了解 envoy 之前，我们首先在本地环境快速上手使用 envoy 以便做初步了解。了解一个开源软件，从官方实例入手再好不过了，下面的例子将会围绕官方仓库中的实例展开。`:w


### 前提条件

* Docker
* Docker Compose
* Git
* curl

我们将会使用 Docker 和 Docker Compose 来构建和运行几个 Envoy 示例服务，并用 curl 来检测服务是否在运行。

### 运行 Envoy

首先克隆 Envoy 官方仓库到本地,并定位到 `envoy/examples/front-proxy` 文件夹。

```shell
git clone https://github.com/envoyproxy/envoy
cd envoy/examples/front-proxy

```

`front-proxy` 文件夹中的服务是一个用 Flask 实现的服务，入口文件在 `service.py` 文件里面。Envoy 作为一个 sidecar 部件，将与 `service.py` 在同一个容器中运行，并由 `docker-compose,.yaml` 文件配置。
