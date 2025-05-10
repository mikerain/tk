## 一、什么是 Container Lifecycle Hooks？

Kubernetes 支持容器生命周期钩子（Lifecycle Hooks），即在容器启动和终止过程中执行自定义操作的机制。两种钩子事件包括：

| Hook 类型   | 触发时机                   | 作用                         |
| ----------- | -------------------------- | ---------------------------- |
| `postStart` | 容器创建成功后，立即执行   | 在容器启动后执行自定义初始化 |
| `preStop`   | 容器终止之前，优雅下线处理 | 在容器被杀死之前执行清理逻辑 |



这两个 Hook 由 Kubelet 在容器生命周期内调用，并在容器内部以命令或 HTTP 请求形式运行。

------

## 二、用途与意义

### ✳ `postStart` 用途

- 执行容器级别初始化逻辑
- 启动伴随进程（如 sidecar 的辅助守护程序）
- 注册容器信息到外部服务

### ✳ `preStop` 用途

- 实现容器的**优雅关闭**
- 完成连接清理、缓存刷新等
- 通知外部服务自己即将下线
- 停止守护进程、防止数据丢失

------

## 三、常见使用场景

| 场景                       | Hook 类型   | 示例操作                    |
| -------------------------- | ----------- | --------------------------- |
| 通知服务注册中心容器上线   | `postStart` | 注册自己到 Consul/ZooKeeper |
| 启动辅助监控或日志收集程序 | `postStart` | 启动 filebeat 等代理        |
| 通知负载均衡器容器即将下线 | `preStop`   | 调用 API 注销自身           |
| 等待一段时间给上游关闭连接 | `preStop`   | 执行 sleep 等待连接断开     |
| 上传缓存或 session 数据    | `preStop`   | 调用脚本将数据持久化        |



------

## 四、生命周期钩子的使用方式

生命周期钩子配置在 Pod 的 `containers.lifecycle` 字段下，可以选择 `exec` 或 `httpGet` 两种方式：

### ✅ 示例：使用 `exec` 执行命令

```
yamlCopyEditlifecycle:
  postStart:
    exec:
      command: ["sh", "-c", "echo Container started at $(date) >> /var/log/start.log"]
  preStop:
    exec:
      command: ["sh", "-c", "echo Container stopping at $(date) >> /var/log/stop.log"]
```

### ✅ 示例：使用 `httpGet` 发送 HTTP 请求

```
yamlCopyEditlifecycle:
  preStop:
    httpGet:
      path: /shutdown
      port: 8080
```

------

## 五、注意事项与限制

| 事项                                             | 描述                                |
| ------------------------------------------------ | ----------------------------------- |
| `postStart` 执行后即启动主容器进程               | 它不会阻止主进程运行，可能并发执行  |
| `preStop` 执行有**宽限期（gracePeriodSeconds）** | 默认 30 秒，可配置                  |
| Hook 执行失败不影响主容器状态                    | 即使失败也不会阻止容器启动/终止     |
| Hook 应尽量**快速完成**                          | 过长的执行时间可能导致 Pod 停止延迟 |
| `exec` 是容器内部命令                            | 必须是容器镜像中可用的命令          |



------

## 六、完整 Pod 示例

```
yamlCopyEditapiVersion: v1
kind: Pod
metadata:
  name: lifecycle-demo
spec:
  containers:
  - name: web
    image: nginx
    lifecycle:
      postStart:
        exec:
          command: ["sh", "-c", "echo The container has started > /usr/share/nginx/html/start.txt"]
      preStop:
        exec:
          command: ["sh", "-c", "sleep 10; echo Container shutting down"]
    ports:
    - containerPort: 80
  terminationGracePeriodSeconds: 30
```

------

## 七、与探针（Probe）的区别

| 对比项   | Lifecycle Hook         | Probe                              |
| -------- | ---------------------- | ---------------------------------- |
| 执行方式 | 执行一次               | 周期性执行                         |
| 时间点   | 容器启动/终止时        | 容器运行期间                       |
| 目的是   | 自定义初始化/清理逻辑  | 检测容器状态                       |
| 类型     | `postStart`、`preStop` | `liveness`、`readiness`、`startup` |



------

## 八、最佳实践建议

- ✅ 使用 `preStop + sleep` 来实现连接优雅断开
- ✅ 保证 `preStop` 的命令执行时间 < `terminationGracePeriodSeconds`
- ✅ 避免在 `postStart` 中进行复杂或阻塞的操作
- ✅ 用日志记录 Hook 执行，方便排查问题
- ✅ 配合探针使用，提升系统可靠性

------

## 九、总结

Container Lifecycle Hooks 是 Kubernetes 提供的重要扩展机制，适合在容器启动和终止前后执行控制逻辑，特别适合实现优雅启停、资源注册、外部通信等场景。

| Hook 类型   | 触发时间   | 应用示例                       |
| ----------- | ---------- | ------------------------------ |
| `postStart` | 容器启动后 | 注册服务、初始化任务           |
| `preStop`   | 容器终止前 | 通知下线、缓存持久化、延时关闭 |



------