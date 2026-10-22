1) Цыганов Артём Дмитриевич ФТ-301

Система:

У меня консоль fish поэтому иногда вывод странно выглядит.
---

  Static hostname: cachyos-x8664
        Icon name: computer-laptop
          Chassis: laptop 💻
Chassis Asset Tag: NO Asset Tag
 Operating System: CachyOS                      
           Kernel: Linux 7.2.9-2-cachyos
     Architecture: x86-64
  Hardware Vendor: Lenovo
   Hardware Model: XiaoXinPro 16c AHP10R
     Hardware SKU: LENOVO_MT_83QH_BU_idea_FM_XiaoXinPro 16c AHP10R
 Firmware Version: S8CN11WW
    Firmware Date: Wed 2025-04-30
     Firmware Age: 1y 5month 3w 2d

2) Приложение

Приложение - адаптировал свой старый python task под веб приложение.
Используя алгоритм фано архивирует и обратно текст отправленный в post запросе.

Переменные окружения:

APP_TOKEN - токен для задания
APP_MESSAGE - сообщение для задания
FLASK_HOST - на каком айпи хостим
FLASK_PORT - его порт (8000)

3) Команды сборки:

Весь ход выполнения в работы и команды находятся в `evidence/console_snaps.md`

Последней версии:
``` bash
docker build -t localhost:5001/tsiganov-homework:v2.0 .
docker push localhost:5001/tsiganov-homework:v2.0  
kubectl create -f k8s/namespace.yaml
kubectl config use-context kind-hosting-lab
kubectl config set-context kind-hosting-lab --namespace=homework-1
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/homework-1 --timeout=180s
kubectl exec deployment/homework-1 -- printenv
kubectl -n homework-1 port-forward deployment/homework-1 8082:8000  
```

``` 
The push refers to repository [localhost:5001/tsiganov-homework]
6aaf5b0aae75: Layer already exists 
7472f19c4477: Layer already exists 
a5883d972f3b: Layer already exists 
1562e5070c19: Already exists 
44136fa355b3: Already exists 
c406f2bf5caf: Layer already exists 
ecc510c1e359: Layer already exists 
bb8166eb34e6: Layer already exists 
4f7260c4a166: Layer already exists 
012a5861ae59: Layer already exists 
v2.0: digest: sha256:b18ae162116839f726fa8f974c47cb006a4003b030832cd241625b76db0f6fa8 size: 856
```
5) Эксперементы и список deployment

Всё в основном в `evidence/console_snaps.md` так как занимают много места

```

◄ 0s ◎ kubectl get deployments              
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
homework-1   2/2     2            2           71m
                                                                                                   
◄ 0s ◎ kubectl get replicaset 
NAME                    DESIRED   CURRENT   READY   AGE
homework-1-69c96fc9c7   2         2         2       34m

◄ 0s ◎ kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
homework-1-69c96fc9c7-g6jcx   1/1     Running   0          34m
homework-1-69c96fc9c7-wncc9   1/1     Running   0          34m
                                                                                                   
```


Объяснение эксперимент 1: ReplicaSet заменил удалённый под, так как под капотом Deployment управляет Подами через ReplicaSet. Изменившиеся имя и UID доказывают, что k8s создал абсолютно новый объект Пода с нуля.

Объяснение эксперимент 2: До перезапуска значения использовались из памяти, но после команды rollout restart поды пересоздались, заново подтянули данные из обновлённого ConfigMap


6)
labels - это метки-теги на объектах (например, app: myapp),
selector - фильтр, по которому Deployment или Service находит свои поды среди остальных.

requests - сколько ресурсов гарантом выделяется поду при старте
limits - максимум ресурсов для пода.

ConfigMap хранит обычные открытые настройки (конфиги, env-переменные), 
Secret хранит более конфиденциальные данные (пароли, ключи, токены).

Base64 - это метод кодирования, а не шифрования.


7) УДАЛЕНИЕ

``` bash
kubectl delete namespace homework-1
```

