# Kubernetes 中 Pod 健康检查（Probe）使用方法培训文档

## 一、什么是 Probe？

在 Kubernetes 中，**Probe（探针）**用于判断容器的运行状态，帮助 Kubernetes 及时发现并处理容器异常。

Kubernetes 提供了三种探针类型：

| 类型             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| `livenessProbe`  | 判断容器是否还“活着”。失败时，Kubelet 会重启容器。           |
| `readinessProbe` | 判断容器是否“准备好”对外提供服务。失败时，容器从 Service 的 endpoints 中移除。 |
| `startupProbe`   | 专用于“启动过程缓慢”的容器。替代 `livenessProbe` 进行启动期间检查。 |



------

## 二、健康检查的作用

1. **提高系统稳定性**：异常容器能被及时发现和处理，避免影响整体系统。
2. **服务可用性保障**：`readinessProbe` 能防止未就绪的服务收到请求。
3. **自动化容器管理**：探针配合重启策略，实现自愈机制。
4. **滚动更新安全性**：确保新容器启动并准备好才加入服务。

------

## 三、使用场景举例

| 场景                         | 解决问题                 | 使用探针         |
| ---------------------------- | ------------------------ | ---------------- |
| 应用启动时间较长             | 避免应用被误判为“假死”   | `startupProbe`   |
| 应用可能因 bug 崩溃或卡死    | 自动检测并重启容器       | `livenessProbe`  |
| 应用需要等待数据库等外部服务 | 等待依赖准备好再接收请求 | `readinessProbe` |
| 后端负载均衡服务控制请求分发 | 保证只转发到健康实例     | `readinessProbe` |



------

## 四、三种探针的用法详解

### 1. `livenessProbe` – 容器“活性”检测

**用途**：判断容器是否需要重启。

**示例**（使用 HTTP 检查）：

```
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3
```

------

### 2. `readinessProbe` – 容器“就绪”检测

**用途**：是否可以接收请求（不影响容器生命周期）。

**示例**（使用 TCP 检查）：

```
readinessProbe:
  tcpSocket:
    port: 3306
  initialDelaySeconds: 5
  periodSeconds: 10
```

------

### 3. `startupProbe` – 容器“启动”检测

**用途**：给启动慢的容器更宽松的检测时间。

**示例**（使用 Exec 命令）：

```
startupProbe:
  exec:
    command:
    - cat
    - /tmp/app-ready
  failureThreshold: 30
  periodSeconds: 5
```

------

## 五、Probe 的几种探测方式

| 方式        | 用法示例                | 适用场景            |
| ----------- | ----------------------- | ------------------- |
| `httpGet`   | 检查 Web 接口是否正常   | Web 应用            |
| `tcpSocket` | 检查端口是否可连接      | 数据库/服务监听端口 |
| `exec`      | 执行命令返回 0 视为成功 | 应用自定义状态判断  |



------

## 六、常用配置字段解释

| 字段               | 含义                                                 |
| ------------------ | ---------------------------------------------------- |
|                    |                                                      |
| `periodSeconds`    | 探测的时间间隔                                       |
| `timeoutSeconds`   | 单次探测的超时时间                                   |
| `failureThreshold` | 连续失败多少次后认为失败                             |
| `successThreshold` | 连续成功多少次才认为成功（仅 `readinessProbe` 使用） |



------

## 七、最佳实践

- 对启动慢的容器，**配合使用 `startupProbe` 和 `livenessProbe`**，避免误判。
- 对于服务暴露的 Pod，**一定要使用 `readinessProbe`** 确保不会早接请求。
- `exec` 探针灵活但性能差，应谨慎使用。
- 不建议用探针来判断**外部依赖服务**（如 DB），建议通过应用逻辑判断自身状态。
- **保持探针频率合理**，避免对应用造成过多压力。

------

## 八、实际完整例子

```
apiVersion: v1
kind: Pod
metadata:
  name: probe-demo
spec:
  containers:
  - name: app
    image: myapp:latest
    ports:
    - containerPort: 8080
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      periodSeconds: 20
    startupProbe:
      httpGet:
        path: /startup
        port: 8080
      periodSeconds: 5
```

------

## 九、总结

| 探针类型         | 是否影响容器重启                      | 是否影响服务接收流量 |
| ---------------- | ------------------------------------- | -------------------- |
| `livenessProbe`  | ✅ 会重启容器                          | ❌ 不影响             |
| `readinessProbe` | ❌ 不重启容器                          | ✅ 不转发请求         |
| `startupProbe`   | ✅ 替代 `livenessProbe` 启动期重启控制 | ❌ 不影响             |



