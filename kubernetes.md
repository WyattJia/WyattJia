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
    
