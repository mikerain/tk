### 场景1，使用initContainer检查依赖

暂时不成功的应用pod

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'myapp'
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 1
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile
      initContainers:
      - name: init-myservice
        image:  public.ecr.aws/docker/library/busybox
        command: ['sh', '-c', 'until nc -z mysql 3306; do echo waiting for db; sleep 2; done;']
```



检查日志，添回依赖的服务mysql

```
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  selector:
    app: mysql
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306

```



检查日志，添加service mysql 对应的部署

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



### 场景2，使用initContainer初始化环境，建立应用依赖的目录

部署后，应用会失败的例子

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'logfile'
spec:
  selector:
    matchLabels:
      app: logfile
  replicas: 1
  template:
    metadata:
      labels:
        app: logfile
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:2.0
```

查看应用的日志



添加initContainer容器后，运行成功的例子

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'logfile'
spec:
  selector:
    matchLabels:
      app: logfile
  replicas: 1
  template:
    metadata:
      labels:
        app: logfile
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:2.0
          volumeMounts:
          - mountPath: /var/log
            name: log-volume
      initContainers:
      - name: logs-init
        image: public.ecr.aws/docker/library/busybox
        command: ['sh', '-c', 'mkdir -p /var/log/flask && chmod 777 /var/log/flask']
        volumeMounts:
        - mountPath: /var/log
          name: log-volume
      volumes:
      - name: log-volume
        emptyDir: {}  
```



### 场景3，使用initContainer在NFS 上建立数据库目录，建立数据库

参见测试环境中mysql/redis的部署，此场景用于使用一个NFS共享，给多个不同实例的mysql/redis使用，每个实例使用不同目录。

目录名在helm模板中使用变量自动替换

```
ship-pre-t 项目
```



### 场景4，使用initContainer下载模型，然后运行应用

参见Openshift AI环境中的LLM模型



