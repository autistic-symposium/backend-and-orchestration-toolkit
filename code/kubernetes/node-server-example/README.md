## deploying a node.js K8s cluster with kubectl

<br>


* build the image:

```
make build:
```

* run the container:

```
make run
```

* check whether the server worked:

```
make curl
```

* check container's status:

```
make status
```

<br>

---

### useful commands

<br>

* exec inside the container:

```
docker exec -i -t <container name from status> /bin/bash
```

* check images in disk:

```
docker images
```

<br>

----

### pushing the registry to kubernetes

<br>

* in a real production system, we’ll want to build images in one place, then run these images in the Kubernetes cluster
* the system that images for distribution is called a **container registry**
* using a `yaml` Kubernetes files (for example, the one inside `node_server_example/`), you can now deploy the image with:

```
kubectl create -f  node_example_kube_config.yaml
```

* after that, you are able to create the service with:

```
kubectl expose deployment node-app-test
```

* also, check out the service status with:

```
kubectl get services
```

<br>

---

### cleanning up

<br>

* removing the service and the deployment when you are done:

```
kubectl delete service node-app-test
kubectl delete deployment node-app-test
```

