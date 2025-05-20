## Kubernetes Secret 培训文档（第一部分）：创建与修改

### 一、Secret 简介

在 Kubernetes 中，Secret（秘密）是一种用于存储和管理敏感信息的资源对象，如密码、访问密钥、TLS 证书等。Secret 的主要目的是避免在 Pod 配置中硬编码这些敏感信息，并通过受控的方式进行访问。

Secret 与 ConfigMap 类似，都可用于将配置信息注入 Pod 中，但 Secret 专为敏感信息设计，具有更高的安全性和可控性。

### 二、Secret 与 ConfigMap 的异同

| 项目             | Secret                                          | ConfigMap                              |
| ---------------- | ----------------------------------------------- | -------------------------------------- |
| **用途**         | 存储敏感信息（如密码、密钥、证书等）            | 存储普通配置信息（如应用配置、参数）   |
| **数据编码**     | 必须使用 Base64 编码                            | 原始文本，YAML/JSON 中可直接写明文本值 |
| **资源类型**     | `Opaque`（默认），还支持 `kubernetes.io/tls` 等 | `ConfigMap`（固定类型）                |
| **安全性**       | 支持 RBAC 精细控制，可结合存储加密              | 安全性较低，内容明文存储               |
| **挂载方式**     | 环境变量、volume、API                           | 环境变量、volume、API                  |
| **自动更新机制** | 挂载为 volume 时支持自动更新（延迟几分钟）      | 同样在 volume 挂载方式下支持自动更新   |
| **默认加密存储** | 可配合 Kubernetes Encryption at Rest 启用加密   | 明文存储在 etcd 中（除非手动配置加密） |

### 三、Secret 类型与用途对比

| 类型                             | 用途说明                                           | 特点与适用场景                                     |
| -------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `Opaque`（默认 / generic）       | 通用的 key-value 类型 Secret，用于存储任意敏感数据 | 最常用类型，适用于数据库密码、API 密钥等自定义场景 |
| `kubernetes.io/dockerconfigjson` | 存储 Docker 镜像仓库认证信息                       | 用于 imagePullSecrets，拉取私有镜像时使用          |
| `kubernetes.io/tls`              | 存储 TLS 证书和私钥                                | 适用于 Ingress、Webhook、TLS 服务配置等场景        |

#### 1. `Opaque` 类型示例：

```
kubectl create secret generic my-secret \
  --from-literal=username=admin \
  --from-literal=password=s3cr3t
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=   # admin
  password: czNjcjN0   # s3cr3t
```

#### 2. `docker-registry` 类型示例：

```
kubectl create secret docker-registry my-docker-secret \
  --docker-server=your-registry.example.com \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myuser@example.com
```

用于 Pod：

```
apiVersion: v1
kind: Pod
metadata:
  name: private-reg
spec:
  containers:
    - name: app
      image: your-registry.example.com/myapp:latest
  imagePullSecrets:
    - name: my-docker-secret
```

#### 3. `tls` 类型示例：

```
kubectl create secret tls tls-secret \
  --cert=./tls.crt \
  --key=./tls.key
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64 encoded certificate>
  tls.key: <base64 encoded key>
```

用于 Ingress：

```
spec:
  tls:
    - hosts:
        - example.com
      secretName: tls-secret
```

### 四、创建 Secret 的方式

#### 1. 使用命令行创建

**从字面值创建：**

```
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=s3cr3t
```

**从文件创建：**

```
kubectl create secret generic app-cert \
  --from-file=tls.crt=./server.crt \
  --from-file=tls.key=./server.key
```

**从环境变量文件创建：**

```
cat > env.txt <<EOF
DB_USER=admin
DB_PASS=secret123
EOF
kubectl create secret generic db-env-secret --from-env-file=env.txt
```

#### 2. 使用 YAML 文件创建

```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: default
type: Opaque
data:
  username: YWRtaW4=     # base64 编码后的 'admin'
  password: czNjcjN0     # base64 编码后的 's3cr3t'
```

创建命令：

```
kubectl apply -f my-secret.yaml
```

**注意：**可以使用 `echo -n 'admin' | base64` 来生成编码，也可以用 `base64 -d` 解码。

### 五、修改 Secret 的方法

#### 1. 使用 `kubectl edit`

```
kubectl edit secret my-secret
```

这会打开默认编辑器（如 vim），编辑保存后直接更新 Secret 对象。

#### 2. 使用 `kubectl patch`

```
kubectl patch secret my-secret \
  -p '{"data": {"username": "bmV3dXNlcg=="}}'
```

此命令将 `username` 的值更新为 `newuser`（base64 编码后）。

#### 3. 使用 `kubectl apply` 覆盖更新

将更新后的 YAML 文件重新 apply：

```
kubectl apply -f my-secret.yaml
```

### 六、查看 Secret 内容

```
kubectl get secret my-secret -o yaml
```

注意：Secret 中的值以 base64 编码形式展示。

若想查看原始内容，可使用：

```
echo "YWRtaW4=" | base64 -d
```

### 七、小结

- Secret 是管理敏感信息的重要方式。

- 支持通过多种方式创建，推荐使用 YAML 管理。

- 修改 Secret 后是否生效，依赖于其挂载方式，下一部分将详细讲解挂载与更新机制。

  

## Kubernetes Secret 培训文档（第二部分）：挂载方式与自动更新机制

### 一、挂载 Secret 的方式

#### 1. 以环境变量方式挂载

在 Pod 的容器中通过 `env` 字段引用 Secret 内容：

```
apiVersion: v1
kind: Pod
metadata:
  name: env-secret-demo
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "echo $SECRET_USER && sleep 3600"]
      env:
        - name: SECRET_USER
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: username
```

**特点：**

- 读取方便，作为环境变量传入应用。
- **不能自动更新**：一旦 Pod 启动，环境变量的值固定不变。

#### 2. 以 Volume 的方式挂载

通过 `volumes` 和 `volumeMounts` 字段将 Secret 以文件形式挂载：

```
apiVersion: v1
kind: Pod
metadata:
  name: volume-secret-demo
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "cat /etc/secret-data/username && sleep 3600"]
      volumeMounts:
        - name: secret-volume
          mountPath: "/etc/secret-data"
  volumes:
    - name: secret-volume
      secret:
        secretName: my-secret
```

**特点：**

- Secret 的每个 key 会作为一个文件挂载在指定目录下。
- 应用可以从文件中读取 Secret 内容。

### 二、更新机制对比

| 挂载方式    | 是否自动更新 | 更新方式                           |
| ----------- | ------------ | ---------------------------------- |
| 环境变量    | 否           | 需重启 Pod 才能加载新值            |
| Volume 文件 | 是（延迟）   | 文件内容会被自动替换（inode 不变） |

#### 1. 环境变量方式说明

- 修改 Secret 后，Pod 中的环境变量不会发生变化。
- 建议在变更后重启相关 Pod：

```
kubectl rollout restart deployment <deployment-name>
```

#### 2. Volume 挂载方式说明

- Kubernetes Controller 会监测 Secret 内容变化，并将文件内容更新到 Pod 中对应挂载的路径中。
- 默认延迟几分钟（通常 1~2 分钟）更新。
- 文件 inode 不变，内容被替换，应用如果是通过 open 之后读取一次，不会看到更新；需应用逻辑支持动态 reload（如使用 inotify）。

### 三、推荐实践

- 尽量使用 Volume 挂载方式，以便 Secret 更新后可自动生效。
- 应用应设计为能动态读取文件或支持重载配置。
- 可结合 sidecar 或 init 容器机制实现配置刷新。
- 如需强制刷新 Secret，考虑使用自动重启机制（如通过 Kubernetes Operator、configmap-reload 工具等）。

### 四、小结

- Secret 支持两种主要挂载方式：环境变量和 Volume。
- 只有 Volume 挂载支持自动更新。
- 应结合业务场景选择挂载方式，确保 Secret 更改后能正确生效。