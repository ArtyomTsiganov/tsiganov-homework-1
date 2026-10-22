

## 1) Сначала, я написал небольшое фласк приложение и его сбилдил и проверил

``` bash
docker build -t localhost:5001/tsiganov-homework:v1.0 .
docker run --rm --name shannon-app -p 127.0.0.1:8082:8000 localhost:5001/tsiganov-homework:v1.0
docker push localhost:5001/tsiganov-homework:v1.0  
```

## 2) Создал `namespace.yaml` и создал сам namespace

``` bash
kubectl create -f k8s/namespace.yaml
kubectl config use-context kind-hosting-lab
kubectl config set-context kind-hosting-lab --namespace=homework-1

kubectl config get-contexts
```

## 3) Настроил yaml файлы и применил их
``` bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/homework-1 --timeout=180s
kubectl exec deployment/homework-1 -- printenv
```

Затем проверил работоспособность

В deployment повысил количество оперативки на pod, чтобы shannon-fano мог архивировать более большие файлы.

```bash
kubectl -n homework-1 port-forward deployment/homework-1 8082:8000  
```

Вот выводы команд:


``` bash
◄ 0s ◎ kubectl exec deployment/homework-1 -- printenv                                  □ Документы/tsiganov-homework-1 22:47

PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=homework-1-56b466cf9c-x26g5
PYTHON_VERSION=3.14.8
PYTHON_SHA256=c2215904f02b175596dc49351585104f4bc20341e1c47378b26a2c274360ce73
FLASK_HOST=0.0.0.0
FLASK_PORT=8000
APP_MESSAGE=Как работает алгоритм: https://habr.com/ru/articles/137766/
APP_TOKEN=Ur0yJ8TvhErcoqgGDJdK1FbyM0gq51pB
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_SERVICE_PORT=443
HOME=/root
               


◄ 1s ◎ kubectl describe deployment homework-1                                          □ Документы/tsiganov-homework-1 23:02

Name:                   homework-1
Namespace:              homework-1
CreationTimestamp:      Thu, 22 Oct 2026 23:01:59 +0500
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=homework-1
Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=homework-1
  Containers:
   homework-1:
    Image:      localhost:5001/tsiganov-homework:v1.0
    Port:       <none>
    Host Port:  <none>
    Limits:
      cpu:                500m
      ephemeral-storage:  256Mi
      memory:             1Gi
    Requests:
      cpu:                100m
      ephemeral-storage:  64Mi
      memory:             64Mi
    Environment Variables from:
      homework-1-config  ConfigMap  Optional: false
    Environment:
      APP_TOKEN:   <set to the key 'APP_TOKEN' in secret 'homework-1-credentials'>  Optional: false
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   homework-1-56b466cf9c (2/2 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  16s   deployment-controller  Scaled up replica set homework-1-56b466cf9c from 0 to 2
                                                                                                                            
◄ 0s ◎         

```

## 4) Собрал v2 версию, которая будет подгружать переменные окружения

``` bash
docker build -t localhost:5001/tsiganov-homework:v2.0 .
docker push localhost:5001/tsiganov-homework:v2.0  
```

Проверил

```bash
kubectl -n homework-1 port-forward deployment/homework-1 8082:8000  
```

После того как я развернул v2 вывод команды выше:


``` bash
0s ◎ curl -i http://localhost:8082/                                   □ Документы/tsiganov-homework-1 23:04
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 22 Oct 2026 18:14:21 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 442
Connection: close


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shannon Fano</title>
</head>
<body>
    <h2>Shannon Fano Decrypter</h2>
    <ul>
        <li><b>Author:</b> Artyom Tsiganov</li>
        <li><b>Project:</b> Shannon Fano decrypter</li>
        <li><b>Token Configured:</b> True</li>
        <li><b>App Message:</b> Как работает алгоритм: https://habr.com/ru/articles/137766/</li>
    </ul>
</body>
</html>⏎                                                                                             

```


## 5) Эксперимент 1:

Вот изначально работающие поды
```
◄ 0s ◎ kubectl -n homework-1 get pods -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount'
NAME                          UID                                    RESTARTS
homework-1-858ff695cd-99bn8   55706a3a-c1ca-4b7f-afd1-2e8822b975fb   0
homework-1-858ff695cd-hsklx   f6a423ec-2f51-495c-b21c-5a8cb606a2b6   0
             
```

Удалил первый под
``` bash
◄ 0s ◎ kubectl delete pod homework-1-858ff695cd-99bn8
pod "homework-1-858ff695cd-99bn8" deleted from homework-1 namespace
```

Поднялся новый под
``` bash
◄ 30s ◎ kubectl -n homework-1 get pods -o custom-columns='NAME:.metadata.name,UID:.metadata.uid,RESTARTS:.status.containerStatuses[0].restartCount'
NAME                          UID                                    RESTARTS
homework-1-858ff695cd-6cpjz   38d0ff89-b5b5-4e48-beb4-8fd7d0135b95   0
homework-1-858ff695cd-hsklx   f6a423ec-2f51-495c-b21c-5a8cb606a2b6   0
```
Объяснение: ReplicaSet заменил удалённый под, так как под капотом Deployment управляет Подами через ReplicaSet. Изменившиеся имя и UID доказывают, что k8s создал абсолютно новый объект Пода с нуля.

## 6) Эксперимент 2:

В `configmap.yaml` изменил APP_MESSAGE с "Как работает алгоритм: https://habr.com/ru/articles/137766/" на "тут может быть всё что угодно" 


```
◄ 0s ◎ kubectl apply -f k8s/configmap.yaml
configmap/homework-1-config configured
                                                                                                             
◄ 0s ◎ kubectl apply -f k8s/deployment.yaml   
deployment.apps/homework-1 configured
                                                                                                             
◄ 0s ◎ kubectl -n homework-1 port-forward deployment/homework-1 8082:8000
Forwarding from 127.0.0.1:8082 -> 8000
Forwarding from [::1]:8082 -> 8000
Handling connection for 8082

```
До перезапуска выдал:

``` bash
◄ 0s ◎ curl -i http://localhost:8082/                                   □ Документы/tsiganov-homework-1 23:14

HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 22 Oct 2026 18:35:29 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 442
Connection: close


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shannon Fano</title>
</head>
<body>
    <h2>Shannon Fano Decrypter</h2>
    <ul>
        <li><b>Author:</b> Artyom Tsiganov</li>
        <li><b>Project:</b> Shannon Fano decrypter</li>
        <li><b>Token Configured:</b> True</li>
        <li><b>App Message:</b> Как работает алгоритм: https://habr.com/ru/articles/137766/</li>
    </ul>
</body>
</html>⏎                                                                                             
```


Перезапустил

```
◄ 0s ◎ kubectl rollout restart deployment/homework-1                    □ Документы/tsiganov-homework-1 23:39
deployment.apps/homework-1 restarted
                                      

◄ 0s ◎ kubectl -n homework-1 port-forward deployment/homework-1 8082:8000
Forwarding from 127.0.0.1:8082 -> 8000
Forwarding from [::1]:8082 -> 8000
```


После перезапуска выдал такое:
```
◄ 0s ◎ curl -i http://localhost:8082/                                   □ Документы/tsiganov-homework-1 23:38
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Thu, 22 Oct 2026 18:40:28 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 417
Connection: close


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Shannon Fano</title>
</head>
<body>
    <h2>Shannon Fano Decrypter</h2>
    <ul>
        <li><b>Author:</b> Artyom Tsiganov</li>
        <li><b>Project:</b> Shannon Fano decrypter</li>
        <li><b>Token Configured:</b> True</li>
        <li><b>App Message:</b> тут может быть всё что угодно</li>
    </ul>
</body>
</html>⏎                                                                                             ```

Объяснение: До перезапуска значения использовались из памяти, но после команды rollout restart поды пересоздались, заново подтянули данные из обновлённого ConfigMap