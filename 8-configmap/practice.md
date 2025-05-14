## 示例 1：一个configmap 对应单个文件

Spring Boot `application.properties` 内容

```
server.port=8080
spring.application.name=myapp
spring.datasource.url=jdbc:mysql://mysql:3306/mydb
spring.datasource.username=root
spring.datasource.password=secret
```

------

#### ✅ 使用 ConfigMap 方式创建（`application.properties`）

#### 方法 1：通过文件创建

1. **保存为文件** `application.properties`

```
cat <<EOF > application.properties
server.port=8080
spring.application.name=myapp
spring.datasource.url=jdbc:mysql://mysql:3306/mydb
spring.datasource.username=root
spring.datasource.password=secret
EOF
```

1. **创建 ConfigMap：**

```
kubectl create configmap springboot-config \
  --from-file=application.properties
```

------

#### 方法 2：用 YAML 显式定义

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: springboot-config
data:
  application.properties: |
    server.port=8080
    spring.application.name=myapp
    spring.datasource.url=jdbc:mysql://mysql:3306/mydb
    spring.datasource.username=root
    spring.datasource.password=secret
```



### 示例 2：一个configmap 对应多个文件

```
cat <<EOF > db.conf
port=3306
username=root
password=secret
EOF


cat <<EOF > redis.conf
port=2379
spring.datasource.username=root
spring.datasource.password=secret
EOF
```



```
kubectl create configmap config-multi \
  --from-file=db.conf \
  --from-file=redis.conf
```

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: config-multi
data:
  db.conf: |
    port=3306
    username=root
    password=secret
  redis.conf: |
    port=2379
    spring.datasource.username=root
    spring.datasource.password=secret
```



### 示例 3 使用 key/value 创建（命令行）

```
kubectl create configmap config-kv \
  --from-literal=app.name=prod \
  --from-literal=app.debug=true
```



```
kind: ConfigMap
apiVersion: v1
metadata:
  name: config-kv
data:
  app.name: 'true'
  app.debug: prod

```





### 示例 4 使用界面或命令行 修改  configmap

使用界面或命令行

```
kubectl edit cm springboot-config 
```



### 示例 4 使用文件修改  configmap

测试以下命令是否可以成功

```
kubectl create configmap springboot-config \
  --from-file=application.properties
    
```



使用drun-run方式,整体替换



```
kubectl create configmap springboot-config \
  --from-file=application.properties \
  --dry-run=client -o yaml
  

kubectl create configmap springboot-config \
  --from-file=application.properties \
  --dry-run=client -o yaml | kubectl apply -f -
```



使用yaml方式,整体替换

```
cat <<EOF >  temp.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: springboot-config
data:
  application.properties: |
    server.port=8080
    spring.application.name=myapp
    spring.datasource.url=jdbc:mysql://mysql:3306/mydb
    spring.datasource.username=root
    spring.datasource.password=secret
EOF


kubectl apply -f temp.yaml

```



使用 `kubectl patch` 修改部分字段（适合小修改）

```
kubectl patch configmap config-kv --type merge \
  -p '{"data":{"ENV":"staging"}}'
  
  kubectl patch configmap config-kv --type merge \
  -p '{"data":{"NAME":"test"}}'
 
```

