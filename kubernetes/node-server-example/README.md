## deploying a node.js K8s cluster with kubectl

<br>


1. Build the image:

```
make build:
```
<br>

2. Run the container:

```
make run
```

<br>

3. Check whether the server worked

```
make curl
```
<br>

4. Check container's status

```
$ make status
```

<br>

---

### useful commands

<br>

Exec inside the container:

```
$ docker exec -i -t <container name from status> /bin/bash
```

Check images in disk:

```
$ docker images
```

<br>

----

### pushing the registry to kubernetes

<br>

In a real production system, we’ll want to build images in one place, then run these images in the Kubernetes cluster. 

The system that images for distribution is called a **container registry**.


Using a `yaml` Kubernetes files (for example, the one inside `node_server_example/`), you can now deploy the image with:

```
$ kubectl create -f  node_example_kube_config.yaml
```

After that, you are able to create the service with:

```
$  kubectl expose deployment node-app-test
```

Also, check out the service status with:

```
$ kubectl get services
```

<br>

---

### cleanning up

<br>

Removing the service and the deployment when you are done:

```
$ kubectl delete service node-app-test
$ kubectl delete deployment node-app-test
```

