# Kubernetes ConfigMap 培训文档（第一部分）

## 👉 主题：创建与修改 ConfigMap 的方法

### 一、ConfigMap 的用途简介

- 用于将**配置信息**以 key-value 的形式提供给容器
- 常见用途：
  - 存储环境变量
  - 配置文件（如 `.conf`、`.properties`）
  - 命令行参数
  - 模块化微服务配置

------

### 二、ConfigMap 的创建方法

#### ✅ 1. 使用 key/value 创建（命令行）

```
kubectl create configmap config-kv \
  --from-literal=ENV=prod \
  --from-literal=DEBUG=true
```

#### ✅ 2. 从单个文件创建

```
kubectl create configmap config-single \
  --from-file=app.properties
```

#### ✅ 3. 从多个文件创建

```
kubectl create configmap config-multi \
  --from-file=db.conf \
  --from-file=redis.conf
```

#### ✅ 4. 从 `.env` 文件创建

```
kubectl create configmap config-env \
  --from-env-file=config.env
```

#### ✅ 5. 加前缀创建（避免 key 冲突）

```
kubectl create configmap config-prefixed \
  --from-file=appconfig=config.env
```

生成的 key 形如：`appconfig.ENV`

#### ✅ 6. 使用 YAML 文件创建（适合版本管理）

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-yaml
data:
  ENV: production
  LOG_LEVEL: debug


kubectl apply -f config.yaml
```

------

### 三、ConfigMap 的修改方法

#### ✅ 1. 使用 `kubectl edit` 编辑 YAML

```

kubectl edit configmap <name>
```

#### ✅ 2. 使用 `kubectl patch` 修改单个字段

```
kubectl patch configmap <name> --type=merge \
  -p '{"data":{"ENV":"staging"}}'
```

#### ✅ 3. 使用 `create --dry-run` + `apply` 更新（覆盖式）

```
kubectl create configmap <name> \
  --from-file=config.conf \
  --dry-run=client -o yaml | kubectl apply -f -
```

#### ✅ 4. 使用 `replace` 替换整个 ConfigMap

```
kubectl get configmap <name> -o yaml > config.yaml
# 编辑文件后
kubectl replace -f config.yaml
```