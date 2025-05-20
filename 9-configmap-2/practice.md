

### 示例1 挂载configmap到变量

可对比以前直接变量方式部署 使用mysql的配置，有什么不同？



```
kind: ConfigMap
apiVersion: v1
metadata:
  name: config-kv
data:
  MYSQL_ROOT_PASSWORD: '123456'
  DBNAME: test
```

方式1

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'mysql2'
spec:
  selector:
    matchLabels:
      app: mysql2
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql2
    spec:
      containers:
        - name: container
          image: quay.io/qxu/mysql
          env:
          - name: MYSQL_ROOT_PASSWORD
            valueFrom:
              configMapKeyRef:
                name: config-kv
                key: MYSQL_ROOT_PASSWORD    
```



方式2

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'mysql2'
spec:
  selector:
    matchLabels:
      app: mysql2
  replicas: 1
  template:
    metadata:
      labels:
        app: mysql2
    spec:
      containers:
        - name: container
          image: quay.io/qxu/mysql
          envFrom:
          - configMapRef:
              name: config-kv
```

原来直接使用变量方式，修改变量，会引发应用重新部署，pod删除重建

现在使用configmap,引用到变量中，修改cm，pod不会自动更新，重建。需要删除pod，生效



### 示例2 挂载configmap中的内容到一个文件

访问应用的route,是否能查询数据成功

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: logfile-cm
data:
  config.ini: |
    [mysql]
    host = mysql
    port = 3306
    user = root
    password = 123456
    database = mysql

    
```





```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
```



```
apiVersion: v1
kind: Service
metadata:
  name: cmdemo
spec:
  selector:
    app: cmdemo
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000

kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: cmdemo
spec:
  to:
    kind: Service
    name: cmdemo
    weight: 100
  port:
    targetPort: 5000
```



挂载configmap, 访问应用的route,是否能查询数据成功

```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      volumes:
        - name: cm-volume
          configMap:
            name: logfile-cm
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
          volumeMounts:
            - name: cm-volume
              mountPath: /app/config
```





### 示例3 挂载configmap中的内容到多个文件

修改cm为以下内容

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: logfile-cm2
data:
  db.conf: |
    port=3306
    username=root
    password=secret
  redis.conf: |
    port=2379
    spring.datasource.username=root
    spring.datasource.password=secret
  config.ini: |
    [mysql]
    host = mysql
    port = 3306
    user = root
    password = 123456
    database = mysql

```

使用以上配置还可以成功吗？

```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      volumes:
        - name: cm-volume
          configMap:
            name: logfile-cm2
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
          volumeMounts:
            - name: cm-volume
              mountPath: /app/config
```

也加载可以，但是会加载所有的文件

如何加载不同文件，到不同目录?



```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      volumes:
        - name: cm-volume
          configMap:
            name: logfile-cm2
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
          volumeMounts:
            - name: cm-volume
              mountPath: /app/config/config.ini
              subPath: config.ini
            - name: cm-volume
              mountPath: /tmp/db.conf
              subPath: db.conf  
```



### 示例4挂载configmap中的内容的更新，自动变更

先在页面查询，确认可以成功查询

 先修改mysql的password,再查询，（f5,F10，disable network）,查询失败吗

再修改 cm中的password,再查询，（F5，f10disable network）,查询失败吗，查询pod中configmap的内容，更新了吗？

删除pod，再查询（F5，f10, disable network）

```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      volumes:
        - name: cm-volume
          configMap:
            name: logfile-cm2
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
          volumeMounts:
            - name: cm-volume
              mountPath: /app/config
```



### 示例5 挂载configmap中的内容的更新，pod不自动变更

subPath参数的加载，不会自动更新cm到pod中

```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: cmdemo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cmdemo
  template:
    metadata:
      labels:
        app: cmdemo
    spec:
      volumes:
        - name: cm-volume
          configMap:
            name: logfile-cm2
      containers:
        - name: cmdemo
          image: quay.io/qxu/logfile:cm
          volumeMounts:
            - name: cm-volume
              mountPath: /app/config/config.ini
              subPath: config.ini
            - name: cm-volume
              mountPath: /tmp/db.conf
              subPath: db.conf
```

