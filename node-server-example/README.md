# Deploying a Node.js K8s Cluster with Kubectl


Build the image:

```
make build:
```

Run the container:

```
make run
```

Check whether the server worked

```
make curl
```

Check container's status

```
$ make status
```


#### Other useful commands

Exec inside the container:

```
$ docker exec -i -t <container name from status> /bin/bash
```

Check images in disk:

```
$ docker images
```


### Pushing the Registry to Kubernetes

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

### Clean up

Removing the service and the deployment when you are done:

```
$ kubectl delete service node-app-test
$ kubectl delete deployment node-app-test
```


## Some References:

* [Dockerfiles good practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#general-guidelines-and-recommendations).