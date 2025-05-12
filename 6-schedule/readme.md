## 一、什么是调度（Scheduling）？

调度是 Kubernetes 控制器的重要功能之一，其核心职责是：

> **将 Pod 安排（Schedule）到合适的节点（Node）上运行。**

调度器会根据资源状况、策略约束、节点特性等因素，选择一个最优节点将 Pod 绑定（Bind）到它上面。

------

## 二、调度的用途

- **资源优化**：合理分配 CPU/内存，避免部分节点过载。
- **业务隔离**：将不同类型的工作负载安排到指定节点（如生产、测试环境分离）。
- **高可用性**：分布式部署，避免集中单点故障。
- **容错/弹性调度**：部分节点故障时，能将 Pod 自动调度到其它健康节点。

------

## 三、常见调度控制机制

------

### 1. **按节点名称调度**（NodeName）

最直接的方式 —— 强制指定 Pod 只能调度到某个具体节点。

```
spec:
  nodeName: worker-node-1
```

📌 使用场景：

- 调试、临时部署到指定节点。
- 预先知道运行节点，手动控制部署位置。

⚠️ 不具备自动调度能力，一般不推荐生产环境使用。

------

### 2. **按节点标签调度**（nodeSelector）

使用节点的标签（Label）控制 Pod 只能调度到特定类型的节点上。

```
spec:
  nodeSelector:
    disktype: ssd
```

📌 使用场景：

- GPU 节点、SSD 节点、地区节点分类部署。
- 业务与资源类型绑定。

------

### 3. **节点选择表达式（Node Affinity）**

更灵活的方式，支持 In、NotIn、Exists、Gt、Lt 等操作。

```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: zone
          operator: In
          values:
          - zone-a
```

📌 使用场景：

- 允许/限制 Pod 部署到多个匹配的区域节点。
- 比 `nodeSelector` 更强大、可组合逻辑。



一张表看清区别

| 特性           | `nodeSelector`       | `nodeAffinity`                                               |
| -------------- | -------------------- | ------------------------------------------------------------ |
| 基本功能       | 根据节点标签选择节点 | 根据节点标签选择节点                                         |
| 支持的操作符   | 只支持 `key=value`   | 支持 `In`、`NotIn`、`Exists`、`DoesNotExist`、`Gt`、`Lt` 等  |
| 表达式能力     | 简单键值对匹配       | 支持复杂的逻辑表达式                                         |
| 支持“尽量调度” | ❌ 不支持             | ✅ 支持 `preferredDuringSchedulingIgnoredDuringExecution`（尽量匹配） |
| 可读性         | 简单清晰，适合初学者 | 更灵活，适合复杂场景                                         |
| 推荐程度       | 一般用于简单场景     | ✅ 推荐使用（更现代、强大）                                   |



## 🛠 示例对比

### 🔹 `nodeSelector` 示例（只能做等值匹配）

```
nodeSelector:
  disktype: ssd
```

只能表达：“调度到标签为 `disktype=ssd` 的节点”。

------

### 🔸 `nodeAffinity` 示例（支持表达式）

```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
          - nvme
```

可以表达：“调度到 `disktype` 是 `ssd` 或 `nvme` 的节点”，甚至可以加多个表达式组合。

------

## ✅ 总结建议

> 如果只是简单地让 Pod 去一个带某个标签的节点，`nodeSelector` 就够用；
>  如果要更强的表达能力和兼容未来复杂调度策略，建议直接用 `nodeAffinity`。



------

### 4. **Pod 间亲和与反亲和（Pod Affinity / AntiAffinity）**

控制 Pod 相互靠近或分散调度（基于已有 Pod 的标签）。

```
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - nginx
      topologyKey: "kubernetes.io/hostname"
```

📌 使用场景：

- 让同一个服务的多个 Pod 分布到不同节点，避免单点。
- 让依赖组件靠近部署（如 Web Pod 靠近 Redis Pod）。



在 Kubernetes 中，`nodeAffinity` 和 `podAntiAffinity` 都有两种模式，分别对应**强制（required）\**和\**尽量（preferred）**，它们由字段的命名决定：

------

## ✅ 1. `nodeAffinity` 的两种模式

| 模式     | 字段名                                            | 含义                                                         |
| -------- | ------------------------------------------------- | ------------------------------------------------------------ |
| **强制** | `requiredDuringSchedulingIgnoredDuringExecution`  | Pod 只能被调度到满足条件的节点，否则调度失败（Pending 状态） |
| **尽量** | `preferredDuringSchedulingIgnoredDuringExecution` | 调度器会**优先**选择满足条件的节点，如果没有也可以调度到不满足的节点 |



### 示例：强制

```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
```

### 示例：尽量

```
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 1
      preference:
        matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
```

------

## ✅ 2. `podAntiAffinity` 的两种模式

| 模式     | 字段名                                            | 含义                                      |
| -------- | ------------------------------------------------- | ----------------------------------------- |
| **强制** | `requiredDuringSchedulingIgnoredDuringExecution`  | 如果没有符合条件的节点，调度失败          |
| **尽量** | `preferredDuringSchedulingIgnoredDuringExecution` | 调度器尽量将 Pod 分散调度，但不是硬性要求 |



### 示例：强制 AntiAffinity（互斥）

```
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: nginx
      topologyKey: "kubernetes.io/hostname"
```

### 示例：尽量 AntiAffinity（优雅分散）

```
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 1
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: nginx
        topologyKey: "kubernetes.io/hostname"
```

------

## ✅ 总结一句话：

> 如果使用的是 `required*` 字段，就是**强制条件**；如果是 `preferred*` 字段，就是**尽量满足**，调度器**可以不满足**。



#### weight

`affinity` 中的 `weight` 是在配置 **preferred（尽量匹配）** 类型的调度策略时使用的，用来告诉调度器：

> ⭐「**偏好强度（权重）**：你有多个备选策略时，哪个更重要？」

------

## 🧠 使用场景

当你使用 `preferredDuringSchedulingIgnoredDuringExecution`（用于 `nodeAffinity`、`podAffinity`、`podAntiAffinity`）时，可以给每条规则设置一个 `weight`（取值范围：**1 ~ 100**）。

调度器会为每个候选节点**打分**，然后选择得分最高的节点来调度 Pod。

------

## ✅ 示例：多个偏好节点

```
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 80
      preference:
        matchExpressions:
        - key: disktype
          operator: In
          values:
          - ssd
    - weight: 20
      preference:
        matchExpressions:
        - key: disktype
          operator: In
          values:
          - hdd
```

**含义**：

- 优先调度到有 `disktype=ssd` 的节点（权重高，分数更高）
- 如果没有，就考虑 `disktype=hdd` 的节点（虽然偏好较低，但比没有匹配还是好）

------



------

### 5. **污点与容忍（Taints & Tolerations）**

节点可以设置“污点”阻止普通 Pod 调度，只有具有“容忍”的 Pod 才能部署到这些节点上。

#### 节点添加污点：

```
kubectl taint nodes node1 key=value:NoSchedule
```

#### Pod 添加容忍：

```
tolerations:
- key: "key"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"
```

📌 使用场景：

- 管理节点隔离（只允许特定 DaemonSet 或系统组件部署）。
- 节点维护、升级前引导 Pod 自动迁移。

------

### 6. **互斥与独占控制（Pod Topology Spread Constraints）**

从 Kubernetes 1.18 开始，推荐使用此方式实现 Pod 均衡分布：

```
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: myapp
```

📌 使用场景：

- 保证副本在不同节点/区域中分布均匀。
- 防止多个副本调度到同一个节点。



在 Kubernetes 的 `topologySpreadConstraints` 中，`maxSkew` 是一个非常重要的字段，它表示：

> **Pod 在各个拓扑域（如节点、zone）之间允许的最大分布差异（倾斜程度）**。

------

## 🧠 通俗解释

你想让 Pod 尽量**平均分布**在多个拓扑域上，但允许一定的不均衡。
 这个“不均衡”的最大容忍程度就是 `maxSkew`。

------

## ✅ 举个例子：

你有 3 个节点（每个节点是一个拓扑域），你部署 5 个 Pod，配置如下：

```
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: myapp
```

这意味着：

- 每个节点上分布的 Pod 数量**相差不能超过 1**
- 合法的分布方案是：2、2、1 或 2、1、2（但不是 3、1、1）

------

## 📌 详细字段说明：

| 字段                | 含义                                                         |
| ------------------- | ------------------------------------------------------------ |
| `maxSkew`           | 不同拓扑域之间匹配 Pod 数量的最大差值                        |
| `topologyKey`       | 按什么维度划分拓扑域（如节点、zone）                         |
| `whenUnsatisfiable` | 如果无法满足 maxSkew，是否仍允许调度： `DoNotSchedule` = 不调度 `ScheduleAnyway` = 尽量调度 |
| `labelSelector`     | 哪些 Pod 需要被均匀分布控制                                  |



------

## ✅ 总结一句话：

> `maxSkew` 决定了你想让 Pod 在拓扑中**分布得多均匀**，数值越小，要求越严格。





`topologySpreadConstraints` 和 `podAntiAffinity` 在功能上确实**看起来类似**——都可以让 Pod 在集群中“分散”分布，但它们有**本质的区别**。

------

## 🧠 核心区别概览

| 特性                               | `podAntiAffinity`                          | `topologySpreadConstraints` |
| ---------------------------------- | ------------------------------------------ | --------------------------- |
| 是否明确控制**分布倾斜度（skew）** | ❌ 否                                       | ✅ 是                        |
| 是否需要已有 Pod 的标签来生效      | ✅ 是（基于现有 Pod 标签匹配）              | ✅ 是（基于 labelSelector）  |
| 控制粒度                           | 粗：只要不能在同一个拓扑域                 | 细：允许偏斜 `maxSkew`      |
| 是否可以实现**多副本强制均衡分布** | ❌ 不支持自动均衡                           | ✅ 支持，常用于副本均衡      |
| 编写复杂度                         | 相对复杂（需 labelSelector + topologyKey） | 更清晰（常用于 Deployment） |
| 常见用途                           | 避免某类 Pod 放在一起（互斥）              | 控制同类 Pod 均匀分布       |



------

## 🧪 示例对比

### 🔸 PodAntiAffinity：让 nginx 不和 nginx 放同一节点

```
podAntiAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
  - labelSelector:
      matchLabels:
        app: nginx
    topologyKey: kubernetes.io/hostname
```

- 含义：如果节点上已有 nginx，则调度器不会再把 nginx 调度上来
- **缺点：不能保证均匀，比如多个节点可能都是 0 个 nginx，而一个节点被允许放 1 个**

------

### 🔹 TopologySpreadConstraints：让 nginx 尽量均匀分布在节点上

```
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: kubernetes.io/hostname
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels:
      app: nginx
```

- 含义：nginx 副本在不同节点上数量差异不得超过 1
- 优点：**适合多副本服务**（如 3 副本分 3 个节点）

------

## ✅ 总结一句话：

> `podAntiAffinity` 更适合**控制 Pod 不要堆在一起**，而 `topologySpreadConstraints` 更适合**让多个副本均匀分布**。

------

如果你要做高可用服务副本分散部署，优先用 `topologySpreadConstraints`。
 如果你要防止同类 Pod 在一个节点上“拥挤”或冲突，则用 `podAntiAffinity`。



------

## 四、实战示例对比

| 机制               | 场景                            | 强度 | 推荐程度                 |
| ------------------ | ------------------------------- | ---- | ------------------------ |
| nodeName           | 临时调试、单节点部署            | 强   | ❌ 不推荐生产用           |
| nodeSelector       | 静态节点选择                    | 中   | ✅ 简单场景适用           |
| NodeAffinity       | 条件化节点选择                  | 强   | ✅ 推荐                   |
| PodAffinity        | 联动调度                        | 中   | ⚠️ 可用，但需注意调度性能 |
| Taints/Tolerations | 控制允许哪些 Pod 调度到特定节点 | 强   | ✅ 推荐                   |
| Spread Constraints | 分布控制（HA）                  | 强   | ✅ 强烈推荐               |



------

## 五、调度排查建议

当 Pod 长时间 Pending，可以通过以下命令分析调度失败原因：

```
kubectl describe pod <pod-name>
```

关注输出中的：

- **Events 中的调度错误原因**
- 是否满足：
  - 节点标签匹配
  - 容忍污点
  - 资源充足
  - 调度策略限制（亲和/互斥）

------

## 六、调度策略设计建议

- 🧩 **生产中尽量使用 Affinity + Taints/Tolerations 组合配置**。
- 🧠 **使用 Pod AntiAffinity 做服务副本隔离时，要选择合理的 topologyKey**（如 `hostname` 或 `zone`）。
- ⚖️ **资源调度策略 + 服务高可用分布应协同设计**。
- 🧪 在调度策略生效前，可以用 dry-run 或 `kubectl scheduler` 工具进行验证。