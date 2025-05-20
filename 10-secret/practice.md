### 创建以及修改示例

#### 示例1 创建 `Opaque` 类型示例：

```
kubectl create secret generic my-secret \
  --from-literal=username=root \
  --from-literal=password=123456

```

方式2，先加密字符串

```
echo -n root|base64 -w0
cm9vdA==
																																echo -n 123456|base64 -w0
MTIzNDU2			
```

再使用yaml生成

```
apiVersion: v1
data:
  password: MTIzNDU2
  username: cm9vdA==
kind: Secret
metadata:
  name: my-secret
  namespace: test
type: Opaque
```



不正确的用法：

如果不加-n, 

```
echo  root|base64 -w0
cm9vdAo=
```

如果不加-w0, 

```
echo  -n roottttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt|base64 
cm9vdHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0
dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0dHR0
dHR0dHR0dHR0dHR0dHR0dHR0dHQ=
```



#### 示例2. `docker-registry` 类型：

```
kubectl create secret docker-registry my-docker-secret \
  --docker-server=repos.taikangcloud.com \
  --docker-username=itw_xuqw01 \
  --docker-password=11111 
```



```
apiVersion: v1
data:
  .dockerconfigjson: eyJhdXRocyI6eyJyZXBvcy50YWlrYW5nY2xvdWQuY29tIjp7InVzZXJuYW1lIjoiaXR3X3h1cXcwMSIsInBhc3N3b3JkIjoiMTExMTEiLCJhdXRoIjoiYVhSM1gzaDFjWGN3TVRveE1URXhNUT09In19fQ==
kind: Secret
metadata:
  name: my-docker-secret
type: kubernetes.io/dockerconfigjson

```



 解密这个secret：

```
echo eyJhdXRocyI6eyJyZXBvcy50YWlrYW5nY2xvdWQuY29tIjp7InVzZXJuYW1lIjoiaXR3X3h1cXcwMSIsInBhc3N3b3JkIjoiMTExMTEiLCJhdXRoIjoiYVhSM1gzaDFjWGN3TVRveE1URXhNUT09In19fQ==|base64 -d
```





#### 示例 3. `tls` 类型：

```
kubectl create secret tls tls-secret \
  --cert=./mirror.crt \
  --key=./mirror.key
```



```
apiVersion: v1
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUYwVENDQTdtZ0F3SUJBZ0lVTzk1VXN2RWxhNHBPdzhtdGVXSHhuQTJNTHlJd0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FqRUxNQWtHQTFVRUJoTUNRMDR4RURBT0JnTlZCQWdNQjBKbGFXcHBibWN4RURBT0JnTlZCQWNNQjBKbAphV3BwYm1jeEREQUtCZ05WQkFvTUEweGhZakVQTUEwR0ExVUVDd3dHUkdWMlQzQnpNUmd3RmdZRFZRUUREQTl0CmFYSnliM0l1WTNKakxuUmxjM1F3SGhjTk1qTXdNVEU1TURFMU1qRXhXaGNOTXpNd01URTJNREUxTWpFeFdqQnEKTVFzd0NRWURWUVFHRXdKRFRqRVFNQTRHQTFVRUNBd0hRbVZwYW1sdVp6RVFNQTRHQTFVRUJ3d0hRbVZwYW1sdQpaekVNTUFvR0ExVUVDZ3dEVEdGaU1ROHdEUVlEVlFRTERBWkVaWFpQY0hNeEdEQVdCZ05WQkFNTUQyMXBjbkp2CmNpNWpjbU11ZEdWemREQ0NBaUl3RFFZSktvWklodmNOQVFFQkJRQURnZ0lQQURDQ0Fnb0NnZ0lCQUxlckdEMW4KeDVMbjNJWjZzR0tPRXVkV1g5dHVDRkJNQnk3N2duSnl6TFJ5dm5CUXhpZjExWThFK2htZUlZYjJGcGE0VzBMNwowaDlkUnJzaitwbnpuWHRCSEdFUXI1VGQreDlhc01wUGdsSm5ZdmIxQjJRVFZEbkhMWktEU25qYWNsZ0ticEc5ClRtV1o1YjYwMm1kMDNWK1d6K2VLWFJCUXBZdHkrbExRSEUxdWh3VjdEWVErQzNFWHl3SGQwOHEzL3JCSlg5Y2IKMGtqUlYxQXNvZmp5UGxaTlZvMksxZDFKbFh5SmQ1NFNwNGk1NUhkaTNuTk9MZ3kvTVBMZERGU0RWRkFxbVlPRQp3bkhiTlJDQ1p6a1dkMDQrbk9KR2xNSDJOZDVSeHJ4ZXlza1NzTFN5ZCtQRWNsWU9mUWFHcVFwWEE5YVMyeXVHCmhjMUpVZlplbmI0ZkpZRlRhQnQ3Tlp3OXFiT1g0Nm9QQkxjNlNWMGpxRGpvK0VGN0lKNjIrb3FvbEcyRXlvcEoKNDREM090SXFZZW5BTjlTVnRiK0M5U3daRUI5a0NTcFVTZ3M1RTRCcGFqN0E4N3pmV2JtazZlZXV6V2QxN0tmdQp4N1FiM21ZdTNRVjlFWmFlcVNRcmY3MFBMYXRoL0J0NEpxVmhSYXJEOU5Qd3pUcERPVjZMWFpzdGZMRWpGTDJGCmw3M0tmTHVybnI5VkNRdmgraVlMVTRWZkJiWm45TG95akl0aEYrNXdDWkNkc2dwQ2d3N1d2MDZnNUJHY2U3aUcKTk1rZUEvTmF2bzNZRm9UOWZZajE5Yi9uK3hqS2dtL1Y3cllsamRTVFk3aWFVK25nYXZnWm9EUzRIdnJIOW9nWQpvME04TFpWRFFnbmhzaWRITHBXdHR5VjlLRGlBU1RaMk90OHJBZ01CQUFHamJ6QnRNQjBHQTFVZERnUVdCQlN2Ck1wSnRsN1VTY2d5Ym84MFd1bkFUbE1QamtEQWZCZ05WSFNNRUdEQVdnQlN2TXBKdGw3VVNjZ3libzgwV3VuQVQKbE1QamtEQVBCZ05WSFJNQkFmOEVCVEFEQVFIL01Cb0dBMVVkRVFRVE1CR0NEMjFwY25KdmNpNWpjbU11ZEdWegpkREFOQmdrcWhraUc5dzBCQVFzRkFBT0NBZ0VBYk5NRmJiNndRYWRRaVh1Uk8rbTlFSkN4QUw5bUNjSzl3T2gyCkZIcTQ2ZDVROS9hVWFVOXZoM0lacVk4TThKdCtidTkvSmxuQkxIcHJwSkxnbmdNak02dXFaOTlnZWpJNm80VEEKU1ZhZFR2ZGFpbmhMMXprYkpnVkVNNmdNUStXM2s3dnNTUUUyNDRsNTJEbFBXZ1dpcGg4MFdYZ3gzcDdIamtsbQpRTE5Ld0JYZXZxVXhVZk9xMTZwTmd4WW1HMEhmd28wWUNmd2ZXRmdybkxXWWo2NlVSV1V4UGljM2s5Y21FOWh0CnpXMnFpQWtvRHVoTlZZeTdiSjA1M3BIdUNUVVFqWEtHRUoxNXF3enZpZEx1ZGdsVE9VMWhUUUNJc0dkL2JhOXAKK1ROcVloNkpHL2VONldkVFZzOExSd0phSVM1VnJTT1hFcmNyUWZyMThnYXp6b2diR0Z5clBIWlJOTXUweGZ3RwpXSGFpVnZDNG9zamRkaFpOaitiVmkyS3RZaGpOenRrUzZhQ1hpY0tyRkxLanptS1dlQ3lzTldHK3FuRVpnZzVpCkRTMUVlOFBna2VWL3ZhRzk1OUhDOHYwTXFhSnpmQlJnWWFIc3QvbHN6Yks2OFF5VG1PMnVERkhMQWhOWVFKSUgKbnY0Y0t5bTZyWEptNEZwdXFQVklyMUg1Ri9TMEdWUnNLWE9rUDJkNURnVi9PSExKeDlhZXQ5WlI4cVNMdWZydwpGQnM4T2NpYWpNRzlZdVlyZ0FLWjFVTTN2QnNMZlNibW1aMytqZ1AybnI5SVQ0bzI1b1FTd2N6L2tPbGdhcVllCno3MHZUa3BrWUhQUmVuZHk2NFVxUTB3Q2trYkhBb3ZleTd3QVRIMjFoNEdJQjFackh0K21JTlZQOW90Z3hzVVEKYVJLSGFSRT0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUpRd0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQ1Mwd2dna3BBZ0VBQW9JQ0FRQzNxeGc5WjhlUzU5eUcKZXJCaWpoTG5WbC9iYmdoUVRBY3UrNEp5Y3N5MGNyNXdVTVluOWRXUEJQb1puaUdHOWhhV3VGdEMrOUlmWFVhNwpJL3FaODUxN1FSeGhFSytVM2ZzZldyREtUNEpTWjJMMjlRZGtFMVE1eHkyU2cwcDQybkpZQ202UnZVNWxtZVcrCnROcG5kTjFmbHMvbmlsMFFVS1dMY3ZwUzBCeE5ib2NGZXcyRVBndHhGOHNCM2RQS3QvNndTVi9YRzlKSTBWZFEKTEtINDhqNVdUVmFOaXRYZFNaVjhpWGVlRXFlSXVlUjNZdDV6VGk0TXZ6RHkzUXhVZzFSUUtwbURoTUp4MnpVUQpnbWM1Rm5kT1BwemlScFRCOWpYZVVjYThYc3JKRXJDMHNuZmp4SEpXRG4wR2hxa0tWd1BXa3RzcmhvWE5TVkgyClhwMitIeVdCVTJnYmV6V2NQYW16bCtPcUR3UzNPa2xkSTZnNDZQaEJleUNldHZxS3FKUnRoTXFLU2VPQTl6clMKS21IcHdEZlVsYlcvZ3ZVc0dSQWZaQWtxVkVvTE9ST0FhV28rd1BPODMxbTVwT25ucnMxbmRleW43c2UwRzk1bQpMdDBGZlJHV25xa2tLMys5RHkycllmd2JlQ2FsWVVXcXcvVFQ4TTA2UXpsZWkxMmJMWHl4SXhTOWhaZTl5bnk3CnE1Ni9WUWtMNGZvbUMxT0ZYd1cyWi9TNk1veUxZUmZ1Y0FtUW5iSUtRb01PMXI5T29PUVJuSHU0aGpUSkhnUHoKV3I2TjJCYUUvWDJJOWZXLzUvc1l5b0p2MWU2MkpZM1VrMk80bWxQcDRHcjRHYUEwdUI3NngvYUlHS05EUEMyVgpRMElKNGJJblJ5NlZyYmNsZlNnNGdFazJkanJmS3dJREFRQUJBb0lDQUg4QjBtNU1BSWNHek1rMXVCayswN1dqClZnQUFFOEdyQVdDc3pXVGxHOGRBZlk1ZlhOZXZPTEdBcUkza2VwekFPWmlaL1luUloxa0hBRzFTa08yNnQ5RE8Ka3BoUW1Jb2lBcENJL3kyM1U1QTJMQXBJSUlkRWtuNnR6RWEvZ1ZVWEFmRDlyYjRjSVVWQzZjczVkcm9KNXpjOQpxNkVhWGdaMUxqVERHblQvc2tLZFJzTTBkNEZXQWtWL1JZT1I2TzRLMUJVRmVEL2cza1k2ZE4xZEw5aGRjMXZzCmVRakIwK2dGQlZrc0drcDE3ZUl2WWR4b3d4a0xHKzcybXh1bVhldG5NWHVLS2NQM254cHFra1JMV0tQeWRDZm8KUmtaMnRsRjJONFA0R3F5U0JEcU5NU0tUTXpLTzJ0M0ZnUkZ0TnlHT1VIb2w3V2NvekFmTVJ1Qk9SMWg4WTByaAo3NDUvSk92d3d4Y3MvNjU4VDBwbktvNVpkR3JUbFJhekp4OW5WVU5oMkFKSm5yWHlDV2owZ1d6Y2N6MFNmOUV2CnQvNnN3SjBGS0E2OEpGNXZyRjQ4bjhkeEYxZlcyakU3VUh4bVBBbENzYXpzY0grS1RNYUhxeG5oc1U1VEFOcHMKRjlFWmI3ZVAyejRQMGhvMXpscmF1c1RWelh3QXBMZVJ0a2hLVEpRa2REb1JzVzd0TS91Mk9OdkhjNEExQ1RRYgpyUXFvZm1LTEpwZjJFRGFMY3NIMDJtOHlDZkswZUNWRDF3QTZlWk5EbWQxZlA0QUxZT0I1Znp4cDg1ZTdiK1UyClRqT2xLK3RMbFlyQThtSkN3QVdvWTdkZWdhSSs3T2ZHclBhWURqTXIyNTl4cVBnM2ttL2dNZ2VYRUdBUkVqYVcKNXAyelBZNGp6SGdpZy9acVJlZ1JBb0lCQVFEZCtJYnA0YU0zbnBYUTQyN2poM0xrbUpINWNPTm5pYWo4c2IxNAp2akt6VXZOc1o2ZjNQc0RtZVFHVmRXM0wyeGNYQmlnOWZ1emJMaVFwUnhuMU9SQ0xYbFNONm9hZVp0ekhNSDJqCk1KaU9SUHdCclptZ1J6a0k0Um8vL3g1QXZxWm9DNzdyVGF1RVk0UThPSzZ2TjROZWc4dk1mMmZEWG5rM1FHdnQKenZTT05hdkN5TnJQK2wyUy83V09YOHFQSDhtUnVlU3NaOVh3dWZiWjI5MFdDUjJyaE1yVGZma2w0M21KaktDUgphSzVucngzNGVrQnVSQ3VyZ01MM2J4alpyS0tFV0JNSFhJVU0yR1RkaW5IOE5oNjdXcVZjVy9LZE9xYlo1VHJvCm9wZDNDSHU5R09icy84Q01kT2hTaEsrQzRVMWJnTk90cUdFL0hHUDJZVGcyMmlJREFvSUJBUURUMDFrSlJJQUYKZ0Q3VzY0OHNoTWdSb0w0SmRFUTV6S3VCcThFYXNIMjRUdVJuS00rTm1xdzZLVFdMVTJpcVM1U3ZRTzczSm55VQpCQkV1QjlkQzVCZ1FXbmVxWi9BaThnNlh3ajhNSWRsMmtpQnFCK091ZmF5YlBHdGFaYXhUNXJpVUF2QWtwRHpDCkdyQmY0aWVNS3BKcE45cnVIUnFlWk9ndDlsOHdTV1l3OXZadUJURkRxckRPd3Q4eEk3c0xaVEdpRkU0eVA5U0wKMzFvWkhUejJnQ2ZVWWFCdjM1ZG92Z1YzbnZVL1QrcWhDWnU0clBNTzZkcXNTODdwRUU0Qlc5ZjNHaGh4Q0dobgp5dTlRbWk0WXREN0ZWaGNLMUFETklMbkN5MU5jTXluK3NVakJaUC9LakY3THROQWRmdU1wQ0JaclNtY01pa21uCm9CV2tSN2FWd2htNUFvSUJBUUNGVGNISUo2ZmJ1VE9EMVhJODFwVmJUMzBxN203RE9WcnhGdFVROURpQ2xTaDMKUy9FRmZQeGY3UC9VZ0VkR0MvZGI3bWl3TmMrTStiTGh6ejk1azZHcDhTYWFhK1FZc1BHWjlqY2RrQXV1TlNPYQo1bVRDYXNPSDM1ZmlJeFpLRDdUaisxblcramd0TTQ2d2srSGtmRlE2cUsvMXlmWEkwSzIvVHNNQ2VDMUtVbFVxCmozRkpRYlI4bVhDeFpqbkJwbmRwT3RobjZad0VDOHFCbjVhd3F4elVhdFZjR2VWTXFjWE5vMVN5dnNrdW4yNUMKVVRqc2Y2Z3lRUXZWaVRURlZQWHN3Ty84bGNXWnAwTThBTzdmWnFraUh4ZjcxWVJvaEZhN3VQeWR4VGR0VnZ6bwozVkdodHg0dHUrL2h6cW1RMGptZzRFYy9uVVY1bjFVeEc4V2t1Mjk5QW9JQkFGY0hhSGRrUzJ6M0tkcEhZY1dhCnNGQjl5RlkrREtIcXN6Uk5pc01hYkN6RFRSZ05MbWt4ZVQxVUhRbW5OVU55Vmg1REFXdE54clZSam5WcEIwb1cKU01TL1JwY2VxUXpTZ3FoYlNHZ0ZxRUVNL0lCVHlYbXhiSzlDL2FCZ1VaTVBJaHE5c2toN3FmTGQ0RVVrdDdiZwo3dEtIL2swQ2JDTlR0Z2pjUm5PaVZIZ2RuMVhJa0ZzSzBDWEM3c3hUcjgrWXZmR25naEVuSkg1clA2czkxZ1E0CjF5UnREK3VtNDZCSElodnBsVDF6NmlSTHZFejkwY2I0MGIwa1VGaDFPSGRhY3JxMVlBRmd3UFNUN2dzaHJYcTgKNDJWVVg1YzFUemI0RVJvMVM0U0FDT3I1ajdqVmREcVZ2WVRZUHdFL1ZybE85MWNSZEpFMFo5cVU3UTlYMzI1YwpGeEVDZ2dFQkFNRnZpQ2xiQmhDcnFtN3N0NG44cndqSFpQY0FNU1NkZktvSDVVQ3FJdkYzb25ZakYwZ2RvVjFDCjVxajJUTDlsZXVzSjRlcHJYZGtlZFJoV253ZEs2OW1MWGxqZlNybjZPTmtYdlk3U2FEbUl0b00vMFF3WTNTb3AKdXU5MFhRSEdQZUJGV3VxRzVyRVBHaU5VWXpVUlljbFJFaDJONytXdm1RVXQxMUJCNGxmWHpqR3hyak93Z2tKUgpNd1ZUVUxFVU9jNEwwQmNNYWVMek9sdWVtWkhqQnRJVXljMVVRWkVGSzVxbXBRZVQvaUlGRHFieVIvQk5FMzZPCkYzdlNtVEpWZDFUbTEwdU4vMC9zV0FJbE9EOUQzQjRORFNwWklXOUhLaEZZK2YrWUNISC9MRUhZZEk5R0Y3RUEKVmRFRHFmMGFNRGxtSFdKdGhURC9ZdGVyNjgzbFcxUT0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQo=
kind: Secret
metadata:
  name: tls-secret

type: kubernetes.io/tls


```



### 修改示例,参考以下示例的格式

```
kubectl create secret generic my-secret \
  --from-literal=username=root \
  --from-literal=password=123456 --dry-run=client -o yaml |kubectl apply -f -
```





### secret 使用和挂载示例

secret加密的内容加载到文件后，会变为明文方式



#### 1 使用Opaque类型的secret到本地文件

Kubernetes Secret 默认每个 key 会挂载为一个独立的文件,

以下示例如建立两个文件在：/app/config/　下

```
apiVersion: v1
data:
  password: MTIzNDU2
  username: cm9vdA==
kind: Secret
metadata:
  name: my-secret
  namespace: test
type: Opaque
```



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secret-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secret-demo
  template:
    metadata:
      labels:
        app: secret-demo
    spec:
      containers:
        - name: demo-container
          image: quay.io/qxu/logfile
          volumeMounts:
            - name: secret-volume
              mountPath: /app/config
      volumes:
        - name: secret-volume
          secret:
            secretName: my-secret
```



如何使用单独文件挂载：

```
kubectl create secret generic my-secret-2 --from-file=db.conf=./db.conf

or
kubectl create secret generic my-secret-2 --from-file=./db.conf
```

或：

```
base64 -w0 db.conf 
dXNlcm5hbWU9cm9vdApwYXNzd29yZD0xMjM0NTYK

```



```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret-2
type: Opaque
data:
  db.conf: dXNlcm5hbWU9cm9vdApwYXNzd29yZD0xMjM0NTYK
```



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secret-demo2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: secret-demo2
  template:
    metadata:
      labels:
        app: secret-demo2
    spec:
      containers:
        - name: demo-container
          image: quay.io/qxu/logfile
          volumeMounts:
            - name: secret-volume
              mountPath: /app/config
      volumes:
        - name: secret-volume
          secret:
            secretName: my-secret-2
```



### 2 使用tls类型的secret到本地文件



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secret-demo3

spec:
  replicas: 1
  selector:
    matchLabels:
      app: secret-demo3
  template:
    metadata:
      labels:
        app: secret-demo3
    spec:
      containers:
        - name: app-container
          image: quay.io/qxu/logfile
          volumeMounts:
            - name: tls-secret-volume
              mountPath: /app/config/
              readOnly: true
      volumes:
        - name: tls-secret-volume
          secret:
            secretName: tls-secret

```



