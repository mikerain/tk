### podman 查看镜像原始命令

```
podman pull quay.io/qxu/sleep

podman inspect quay.io/qxu/sleep

"History": [
               {
                    "created": "2024-09-06T12:05:36Z",
                    "created_by": "ADD alpine-minirootfs-3.20.3-x86_64.tar.gz / # buildkit",
                    "comment": "buildkit.dockerfile.v0"
               },
               {
                    "created": "2024-09-06T12:05:36Z",
                    "created_by": "CMD [\"/bin/sh\"]",
                    "comment": "buildkit.dockerfile.v0",
                    "empty_layer": true
               },
               {
                    "created": "2025-04-27T02:15:05.590156839Z",
                    "created_by": "/bin/sh -c #(nop) ENTRYPOINT [\"sleep\"]",
                    "comment": "FROM docker.io/library/alpine:latest",
                    "empty_layer": true
               },
               {
                    "created": "2025-04-27T02:15:05.630485513Z",
                    "created_by": "/bin/sh -c #(nop) CMD [\"3600\"]",
                    "empty_layer": true
               }

```

### 场景1 pod使用args参数覆盖dockerfile原有的参数

示例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'sleep'
spec:
  selector:
    matchLabels:
      app: sleep
  replicas: 1
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



使用args

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'sleep'
spec:
  selector:
    matchLabels:
      app: sleep
  replicas: 1
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - name: container
          image: quay.io/qxu/sleep
          args: 
            - '30'
```



### 场景2 pod使用command覆盖dockerfile原有启动命令

使用command

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'sleep'
spec:
  selector:
    matchLabels:
      app: sleep
  replicas: 1
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - name: container
          image: quay.io/qxu/sleep
          command: ["sleep", 'infinity']
```



### pod使用command/args覆盖dockerfile原有启动命令

command and args:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'sleep'
spec:
  selector:
    matchLabels:
      app: sleep
  replicas: 1
  template:
    metadata:
      labels:
        app: sleep
    spec:
      containers:
        - name: container
          image: quay.io/qxu/sleep
          command: ["sleep"]
          args: ["infinity"]
```





### 场景4 使用command，进行调试出错的镜像

使用mysql镜像建立部署

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'mysql'
spec:
  selector:
    matchLabels:
      app: mysql
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: container
          image: quay.io/qxu/mysql
```



添加command,履盖原有的启动命令

```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'mysql'
spec:
  selector:
    matchLabels:
      app: mysql
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: container
          image: quay.io/qxu/mysql
          command: ["sleep", "infinity"]
```

检查镜像的默认启动命令

```
podman inspect quay.io/qxu/mysql
        {
                    "created": "2024-10-14T22:15:13Z",
                    "created_by": "ENTRYPOINT [\"docker-entrypoint.sh\"]",
                    "comment": "buildkit.dockerfile.v0",
                    "empty_layer": true
               },
```



进入容器内部执行启动命令，查看是否有报错信息：

```shell
sh-5.1$ ./docker-entrypoint.sh 
sh-5.1$ ./docker-entrypoint.sh  -x
2025-04-28 01:52:55+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.40-1.el9 started.
2025-04-28 01:52:56+00:00 [ERROR] [Entrypoint]: Database is uninitialized and password option is not specified
    You need to specify one of the following as an environment variable:
    - MYSQL_ROOT_PASSWORD
    - MYSQL_ALLOW_EMPTY_PASSWORD
    - MYSQL_RANDOM_ROOT_PASSWOR
```



添加变量，使用以下yaml，

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'mysql'
spec:
  selector:
    matchLabels:
      app: mysql
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: container
          image: quay.io/qxu/mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: '123456'
      
```

