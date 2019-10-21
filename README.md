# Resources for Kubernetes

* A Kubernetes cluster consists of **Nodes** (simialr to servers)

* Nodes run **Pods**, which are collections of Docker containers. Containers in a Pod share the same network.

* The Kubernetes object responsible for launching and maintaining the desired number of pods is called a **Deployment**. 

* Kubernetes provides objects called a **Service** so thart Pods to communicate with other Pods. They are tied to Deployments through Selectors and Labels, and they can be exposed to external clients either by exposing a **NodePort** as a static port on each Kubernetes node or by creating a **LoadBalancer** object/

* Kubernetes provides the **Secret** object for managing sensitive information such as passwords, API keys, and other credentials.


-------------

## In this Repository

* [Spin up a node server example](https://github.com/bt3gl/Learning_Kubernetes/tree/master/node-server-example).
* [Use kustomize to organize and combine YAML templates of your services and deployments](https://github.com/bt3gl/Learning_Kubernetes/tree/master/kustomize-example).


--------------
## Tools

### Minikube

[Minikube](https://github.com/kubernetes/minikube) implements a local Kubernetes cluster on macOS, Linux, and Windows. You can install it following [this instructions](https://minikube.sigs.k8s.io/docs/start/).

### Kubectl

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


--------

## Learning 


* [Google's K8s 101](https://techdevguide.withgoogle.com/paths/cloud/sequence-2/kubernetes-101-pods-nodes-containers-and-clusters/#!).

