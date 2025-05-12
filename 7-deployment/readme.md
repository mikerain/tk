# Kubernetes Deployment 培训文档

## 1️⃣ Deployment 是什么？

`Deployment` 是 Kubernetes 中用于**声明式管理应用副本**的核心控制器，负责：

- 管理 Pod 副本的生命周期
- 实现版本控制和滚动升级
- 自动修复异常实例
- 与 ReplicaSet 协同实现无缝部署

------

## 2️⃣ Deployment 的用途

| 功能         | 说明                         |
| ------------ | ---------------------------- |
| 应用部署     | 快速创建并运行一组相同的 Pod |
| 滚动升级     | 平滑地从旧版本迁移到新版本   |
| 自动重建     | 当 Pod 异常终止时自动恢复    |
| 版本控制     | 可回滚到历史版本             |
| 声明式扩缩容 | 可随时调整副本数（replicas） |



------

## 3️⃣ 常见使用场景

- **部署 Web 应用**：如 nginx、flask、springboot 等服务
- **持续集成交付**：与 GitOps/Jenkins 配合自动部署
- **高可用服务**：结合多副本与探针进行容错部署
- **灰度发布**：逐步替换 Pod 观察效果

------

## 4️⃣ Deployment 基本结构示例

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1
        ports:
        - containerPort: 80
```

------

## 5️⃣ 与 ReplicaSet 的关系

| Deployment                              | ReplicaSet                      |
| --------------------------------------- | ------------------------------- |
| 高层控制器，用户直接操作                | 被 Deployment 自动管理          |
| 提供升级、回滚等高级功能                | 只负责维持副本数一致            |
| 一个 Deployment 对应多个历史 ReplicaSet | 每次升级都会创建新的 ReplicaSet |



> ⚠️ 建议：**不要直接创建 ReplicaSet**，请通过 Deployment 管理。

------

## 6️⃣ Deployment 升级方式（策略）

Deployment 支持两种升级策略：

### ✅ 滚动升级（默认）

```
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 1
```

- `maxSurge`: 允许多创建的 Pod 数量（如 1 表示可额外增加 1 个）
- `maxUnavailable`: 升级过程中允许暂停的 Pod 数量

### ⛔ 替换式升级（Recreate）

```
strategy:
  type: Recreate
```

- 会先终止所有旧版本 Pod，再启动新版本
- 有停机风险，不推荐用于生产

------

## 7️⃣ Deployment 回滚操作

```
kubectl rollout undo deployment myapp
```

- 回滚到上一个版本
- 可指定版本：`--to-revision=n`

查看历史记录：

```
kubectl rollout history deployment myapp
```

------

## 8️⃣ 扩缩容方法

### 自动伸缩（需启用 HPA）

```
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=70
```

### 手动伸缩

```
kubectl scale deployment myapp --replicas=5
```

------

## 9️⃣ 实践技巧与建议

| 建议                             | 说明                      |
| -------------------------------- | ------------------------- |
| 配合 `readinessProbe`            | 防止未就绪 Pod 被流量命中 |
| 配合 `tolerations`/`affinity`    | 控制 Pod 具体调度位置     |
| 配合 `topologySpreadConstraints` | 实现高可用部署            |
| 配合 ConfigMap/Secret            | 实现配置与密钥解耦        |



------

## 🔚 总结一句话

> **Deployment 是面向无状态服务的最佳实践工具**，兼顾**可扩展性、稳定性与灵活性**，是 CI/CD 中的核心资源对象。