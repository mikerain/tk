### 场景1 使用sidecar容器将日志输出到console

日志输出到文件的部署

```yaml
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



使用sidecar容器，输出日志到console

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'tailfile'
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
          volumeMounts:
            - name: log-volume
              mountPath: /var/log
        - name: log-container
          image:  quay.io/app-sre/ubi8-ubi-minimal
          command: ['tail','-f','/var/log/app.log']
          volumeMounts:
            - name: log-volume
              mountPath: /var/log 
      volumes:
        - name: log-volume
          emptyDir: {}          
```



### 场景2 使用sidecar容器中工具命令调试网络环境

主容器中缺少curl, ping此类命令

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: 'debuglogfile'
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
        - name: sidecar-container
          image: registry.redhat.io/rhel8/support-tools
          command: ['sleep','infinity']
```





### 场景3 使用sidecar容器中工具命令调试应用

主容器中缺少jstack, jmap 此类工具，sidecar容器中不能只是简单的包括这类工具，还需要和主容器共享应用进程。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: log-collection
spec:
  selector:
    matchLabels:
      app: log-collection
  replicas: 1
  template:
    metadata:
      labels:
        app: log-collection
    spec:
      containers:
        - name: log-collection
          image: quay.io/qxu/log-collection:jre
```



```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: debug-log-collection
spec:
  selector:
    matchLabels:
      app: log-collection
  replicas: 1
  template:
    metadata:
      labels:
        app: log-collection
    spec:
      shareProcessNamespace: true
      containers:
        - name: log-collection
          image: quay.io/qxu/log-collection:jre
          volumeMounts:
          - name: shared
            mountPath: /shared
        - name: debug-sidecar
          image: docker.io/library/openjdk:17.0-jdk-slim
          command: ["sleep", "infinity"]
          securityContext:
            capabilities:
              add: ["SYS_PTRACE"]
          volumeMounts:
          - name: shared
            mountPath: /shared
      volumes:
      - name: shared
        emptyDir: {}
```



OCP项目中需要添加对应的权限，共享进程

oc project test

oc adm policy add-scc-to-user anyuid -z default

oc adm policy add-scc-to-user privileged -z default

如果容器中没有ps命令，可使用以下方式查看java进程

```shell
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
  if grep -qa "java" /proc/$pid/cmdline 2>/dev/null; then
    echo "Java PID: $pid"
  fi
done


Found Java process with PID: 13
java -server -Xms256m -Xmx256m -Duser.timezone=Asia/Shanghai -Djava.security.egd=file:/dev/./urandom -jar /usr/local/log-collection-demo.jar 


jstack 13
2025-04-28 09:37:05
Full thread dump OpenJDK 64-Bit Server VM (11.0.16+8 mixed mode, sharing):

Threads class SMR info:
_java_thread_list=0x00007fd8240028f0, length=28, elements={
0x00007fd8500c8800, 0x00007fd8500ca800, 0x00007fd8500d2000, 0x00007fd8500d4000,
0x00007fd8500d6800, 0x00007fd8500d8800, 0x00007fd8500da800, 0x00007fd850122000
```

