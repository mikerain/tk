### 1指定节点调度 (`nodeName`)



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      nodeName: xxxxxxx
      containers:
        - name: container
          image: quay.io/qxu/sleep


```



### 2 基于节点标签 (`nodeSelector`)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      nodeSelector:
        group: dev
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



### 3 节点亲和性 (`Node Affinity`)

可以把preferredDuringSchedulingIgnoredDuringExecution修改为requiredDuringSchedulingIgnoredDuringExecution，测试下效果

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            preference:
              matchExpressions:
              - key: group
                operator: In
                values:
                - test
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: group
                operator: In
                values:
                - test
      containers:
        - name: container
          image: quay.io/qxu/sleep
```

### 4 Pod 间反亲和（避免同类 Pod 同节点）

修改replicas的数量为4，或更多超过work的数量，检查pod在节点上的分布

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 2
  template:
    metadata:
      labels:
        app: busybox
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: busybox
            topologyKey: "kubernetes.io/hostname"
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



### 5 Taints & Tolerations（容忍节点污点）

部署无法调度的情况

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''
      containers:
        - name: container
          image: quay.io/qxu/sleep
```

添加容忍

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/master"
        operator: "Exists"
        effect: "NoSchedule"
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''
      containers:
        - name: container
          image: quay.io/qxu/sleep
```

使用万能容忍

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 1
  template:
    metadata:
      labels:
        app: busybox
    spec:
      tolerations:
      - operator: "Exists"
      nodeSelector:
        node-role.kubernetes.io/control-plane: ''
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



### 6 Pod 分布控制（Pod Topology Spread Constraints）



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'busybox'
spec:
  selector:
    matchLabels:
      app: busybox
  replicas: 2
  template:
    metadata:
      labels:
        app: busybox
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: busybox
      containers:
        - name: container
          image: quay.io/qxu/sleep
```



修改replicas的数量，超过work的数量，看能否部署成功？否

然后修改maxskew为3，看能否部署成功？是