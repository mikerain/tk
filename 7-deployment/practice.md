### 场景1 deployment基本结构示例

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
          image: quay.io/qxu/logfile
```

### 场景2 deployment的滚动升级示例

升级镜像为以下版本，在logfile:probe与logfile之间切换

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
          image: quay.io/qxu/logfile:probe
```

查看replicaset,回退到指定的replicaset

修改maxSurge,maxUnavailable,查看pod的同时删除和建立的数量



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'logfile'
spec:
  selector:
    matchLabels:
      app: logfile
  replicas: 10
  template:
    metadata:
      labels:
        app: logfile
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 50%
      maxSurge: 50%
```

### 场景3 修改deployment的默认升级方式



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'logfile'
spec:
  selector:
    matchLabels:
      app: logfile
  replicas: 3
  template:
    metadata:
      labels:
        app: logfile
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile
  strategy:
    type: Recreate

```



### 场景4 deployment的自动伸缩（需启用 HPA）

```
kind: HorizontalPodAutoscaler
apiVersion: autoscaling/v2
metadata:
  name: http-stress
spec:
  scaleTargetRef:
    kind: Deployment
    name: logfile
    apiVersion: apps/v1
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 10
```





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
        image: quay.io/qxu/logfile:hpa
        resources:
          limits:
            cpu: 10m
            memory: 4096Mi
```



```
apiVersion: v1
kind: Service
metadata:
  name: logfile
spec:
  selector:
    app: logfile
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000

```



```
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: logfile
spec:
  to:
    kind: Service
    name: logfile
    weight: 100
  port:
    targetPort: 5000
```



在route界面上使用300秒的压力测试，查看pod是否自扩容

查看deployment的整体的metric
