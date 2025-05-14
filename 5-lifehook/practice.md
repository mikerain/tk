### 使用场景1 prestop 容器的优雅关闭

未使用prestop,删除pod，记录pod的terminating时间是多少？30s左右

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'prestop'
spec:
  selector:
    matchLabels:
      app: prestop
  replicas: 1
  template:
    metadata:
      labels:
        app: prestop
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook
```



使用prestop, 删除pod，记录pod的terminating时间是多少？60s左右(也可能是30s,取决于不同集群)

再修改sleep 90，删除pod，记录pod的terminating时间是多少？也是60s，这是因为没有修改terminationGracePeriodSeconds

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'prestop'
spec:
  selector:
    matchLabels:
      app: prestop
  replicas: 1
  template:
    metadata:
      labels:
        app: prestop
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook
          lifecycle:
            preStop:
              exec:
                command:
                - sleep
                - '60'
```



与terminationGracePeriodSeconds的比较，terminationGracePeriodSeconds无法主动执行业务相关的摘除流量动作。

 配置terminationGracePeriodSeconds: 120，删除pod,记录pod的terminating时间是多少？120s左右

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'prestop'
spec:
  selector:
    matchLabels:
      app: prestop
  replicas: 1
  template:
    metadata:
      labels:
        app: prestop
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook
      terminationGracePeriodSeconds: 120   
```



二者结合中使用：

prestop +terminationGracePeriodSeconds, 且terminationGracePeriodSeconds >prestop,大约60+90=150s左右

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'prestop'
spec:
  selector:
    matchLabels:
      app: prestop
  replicas: 1
  template:
    metadata:
      labels:
        app: prestop
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook
          lifecycle:
            preStop:
              exec:
                command:
                - sleep
                - '60'
      terminationGracePeriodSeconds: 90          
  
```



### 使用场景2 poststart 下载远程数据



未使用postart的页面显示效果

在页面上点击按钮，显示图片

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'poststart'
spec:
  selector:
    matchLabels:
      app: poststart
  replicas: 1
  template:
    metadata:
      labels:
        app: poststart
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook2.0
```



```
apiVersion: v1
kind: Service
metadata:
  name: poststart
spec:
  selector:
    app: poststart
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000

```

```
kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: poststart
spec:
  to:
    kind: Service
    name: poststart
    weight: 100
  port:
    targetPort: 5000
```





使用postart的页面显示效果（内部请使用jfrog.png的图处）

在页面上点击按钮，显示图片,

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'poststart'
spec:
  selector:
    matchLabels:
      app: poststart
  replicas: 1
  template:
    metadata:
      labels:
        app: poststart
    spec:
      containers:
        - name: container
          image: quay.io/qxu/logfile:hook2.0
          lifecycle:
            postStart:
              exec:
                command:
                  - python
                  - download.py
                  - 'https://pss.bdstatic.com/static/superman/img/topnav/newzhidao-da1cf444b0.png'
                  - static/sample.jpg
```



也可以修改command中的命令，让poststart命令出错，看一下pod的状态，poststart的命令出错会引发pod失败，而且不好调试。

查看event中的：PostStartHook failed相关事件