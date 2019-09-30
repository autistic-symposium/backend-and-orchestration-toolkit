# Resources and Examples to Learn Kubernetes


## Minikube

[Minikube](https://github.com/kubernetes/minikube) implements a local Kubernetes cluster on macOS, Linux, and Windows. You can install it following [this instructions](https://minikube.sigs.k8s.io/docs/start/).

## Kubectl

Kubectl is a command line interface for running commands against Kubernetes clusters. You can install it [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).


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


## Examples in this repo


* [Spin up a node server example](https://github.com/bt3gl/Learning_Kubernetes/tree/master/node-server-example).
* [Use kustomize to organize and combine YAML templates of your services and deployments](https://github.com/bt3gl/Learning_Kubernetes/tree/master/kustomize-example).