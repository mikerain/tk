## Kubernetes 中的 Downward API 使用简介

### 一、什么是 Downward API？

Downward API 是 Kubernetes 提供的一种机制，它允许容器以 **环境变量（`env`）** 或 **挂载文件（`volumeMounts`）** 的方式访问关于 Pod 自身的信息，而不需要显式地通过外部服务发现或额外配置。

通过 Downward API，Pod 可以“向下”访问以下信息：

- Pod 的名称
- Pod 的命名空间
- Pod 的标签（Labels）
- Pod 的注解（Annotations）
- Pod 所在的节点名
- 容器资源限制（如 CPU/内存 requests/limits）
- 当前容器的启动时间戳等

### 二、用途与典型使用场景

#### 1. **日志和监控用途**

将 Pod 名称、命名空间、标签等写入日志，便于日志聚合工具（如 ELK/EFK、Loki）按 Pod 维度进行日志聚合和检索。

```
env:
- name: POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
- name: POD_NAMESPACE
  valueFrom:
    fieldRef:
      fieldPath: metadata.namespace
```

#### 2. **自动化配置与标识**

某些容器需要知道自身运行的上下文（如命名空间、所在节点、所属应用标签等）来决定服务行为、日志目录、配置文件路径等。

```
env:
- name: NODE_NAME
  valueFrom:
    fieldRef:
      fieldPath: spec.nodeName
```

#### 3. **性能和资源调优**

容器启动时通过环境变量读取自身分配的资源信息，从而根据资源限制动态调整线程池、连接数等。

```
env:
- name: CPU_LIMIT
  valueFrom:
    resourceFieldRef:
      resource: limits.cpu
```

#### 4. **控制文件挂载**

如果想将信息（如 labels/annotations）以文件方式提供给容器，也可以使用 Downward API 以 Volume 方式挂载。例如：

```
volumes:
- name: podinfo
  downwardAPI:
    items:
    - path: "labels"
      fieldRef:
        fieldPath: metadata.labels

volumeMounts:
- name: podinfo
  mountPath: /etc/podinfo
  readOnly: true
```

容器内即可通过读取 `/etc/podinfo/labels` 文件获得当前 Pod 的标签信息。

### 三、Downward API 的优点

- **去中心化**：不依赖于外部服务发现机制即可获取必要信息；
- **解耦设计**：让容器无需感知 Kubernetes API Server 的访问细节；
- **安全可控**：通过只暴露有限字段，避免信息泄露；
- **动态感知**：结合容器生命周期钩子可实现更智能的应用逻辑。