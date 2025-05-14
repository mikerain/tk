# Kubernetes ConfigMap 培训文档（第二部分）

## 👉 主题：挂载方式与动态更新机制

### 一、ConfigMap 的挂载用途

- 传递配置信息给容器使用，常见方式包括：
  - 环境变量（单个或批量）
  - Volume 文件挂载（整挂或拆分）
  - 指定 `subPath` 精确路径挂载

------

### 二、常用挂载方式示例

#### ✅ 1. 挂载为单个环境变量

```
env:
- name: ENV
  valueFrom:
    configMapKeyRef:
      name: config-kv
      key: ENV
```

#### ✅ 2. 批量导入为环境变量

```
envFrom:
- configMapRef:
    name: config-kv
```

#### ✅ 3. 整体挂载为 Volume（所有 key 成为文件）

```
volumes:
- name: config-vol
  configMap:
    name: config-kv

volumeMounts:
- name: config-vol
  mountPath: /etc/config
```

#### ✅ 4. 指定 key 挂载为特定文件（items）

```
volumes:
- name: config-vol
  configMap:
    name: config-kv
    items:
    - key: app.conf
      path: myapp.conf
```

#### ✅ 5. 使用 subPath 精确控制文件路径

```
volumeMounts:
- name: config-vol
  mountPath: /etc/app/config.yaml
  subPath: app.conf
```

------

### 三、只读挂载方式

```
volumeMounts:
- name: config-vol
  mountPath: /etc/config
  readOnly: true
```

- 推荐设置为只读，防止容器误修改

------

### 四、动态更新机制对比

| 挂载方式        | 是否动态更新 | 说明                 |
| --------------- | ------------ | -------------------- |
| 环境变量（env） | ❌ 不支持     | Pod 创建后值固定     |
| envFrom         | ❌ 不支持     | 同上                 |
| volume 挂载     | ✅ 延迟更新   | 默认每分钟检查更新   |
| subPath         | ❌ 不支持     | 是文件复制，不是绑定 |



------

### 五、如何让更新生效？

如果你的挂载方式不支持自动更新，可以使用以下命令手动滚动：

```
kubectl rollout restart deployment <deployment-name>
```