### 场景1 `livenessProbe`失败时，不断重启容器的示例

不使用probe:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe
```



使用失败的probe, 观察pod会不断重启

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe
          livenessProbe:
            httpGet:
              path: /notready
              port: 5000
              scheme: HTTP
```

使用成功的probe, 观察pod会不会重启



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe
          livenessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
```



### 场景2  `readinessProbe`失败时，pod不提供服务的情况

先建立对应的service和route,

检查pod下是否ready, route是否可以正常访问

```
apiVersion: v1
kind: Service
metadata:
  name: liveprobe
spec:
  selector:
    app: liveprobe
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000

```



```
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: liveprobe
spec:
  to:
    kind: Service
    name: liveprobe
    weight: 100
  port:
    targetPort: 5000
```



添加一个失败的readniess probe

先直接在原有的deployment上修改，检查一下原有的pod是否会自动删除？否

检查pod下是否ready, 否

 route是否可以正常访问？是

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe
          readinessProbe:
            httpGet:
              path: /notready
              port: 5000
              scheme: HTTP
```

然后将deployment的replica数量修改为0，再修改为1，

检查pod下是否ready, route是否可以正常访问？否





### 场景3 配置liveness后，应用启动慢超时，引发的pod失败

些镜像用于模拟慢启动的ready接口，启动时间大约120s

使用默认的配置，检查pod会重启多少次后失败,大约在每5－6次会失败

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe2.0
          livenessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
```



添加超时配置,发现不再重启，但是pod处于ready状态，不是我们想要的结果：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe2.0
          livenessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
              failureThreshold: 20
              periodSeconds: 20  
  
```





添加readniess配置

检查pod是否ready?否，因为原有的代码有bug，在写ready检查接口时，不要简单的写time sleep,否则会使得检查超时

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe2.0
          livenessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
            failureThreshold: 30
            periodSeconds: 10   
          readinessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
            failureThreshold: 30
            periodSeconds: 10  
```



使用些配置，再检查pod是否能ready?是

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'liveprobe'
spec:
  selector:
    matchLabels:
      app: liveprobe
  replicas: 1
  template:
    metadata:
      labels:
        app: liveprobe
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:probe3.0
          livenessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
            timeoutSeconds: 1
            periodSeconds: 3
            successThreshold: 1
            failureThreshold: 30 
          readinessProbe:
            httpGet:
              path: /ready
              port: 5000
              scheme: HTTP
            timeoutSeconds: 1
            periodSeconds: 3
            successThreshold: 1
            failureThreshold: 30 
```

