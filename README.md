# 🎨 A Quick Intro to K8s 🎨

In this guide, I show you how to spin a quick ```Node.js``` server in kubernetes and to grasp some of its main concepts.

### Install kubectl

First, you will need to install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in your machine.

Make sure you have all the auths right, for instance, I do the following:

1. Create an auth token and move to `~/.kube`
2. Create a config file and move to `~/.kube`


### Spinning up a Hello World node server in docker

Download [this code](https://github.com/bt3gl/intro_to_k8s/tree/master/node_server_example) and build the image:

```
$ make build:
```

Now, just run the container:

```
$ make run
```

Which is:
```
docker build -t node_app_test .
```

Check whether the server is up:
```
$ make curl
```

Voilà!

You can also check the status of your setup with:

```
$ make status
```


#### Other useful Docker commands

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



## Useful General Commands

Checking out pods:

```
$ kubectl get pods --namespace=<ns-name>
```

Checking deployments:

```
$ kubectl get deployments --namespace=<ns-name>
```

Checking services:

```
$ kubectl get services --namespace=<ns-name>
```

Get more information about a pod:

```
$ kubectl describe pod --namespace=<ns-name> <pod name>
```



## Some References:

* [Dockerfiles good practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#general-guidelines-and-recommendations).


----


## License

When making a reference to my work, please use my [website](http://bt3gl.github.io/index.html).

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

