# Resources for Kubernetes

## What's K8s

A Kubernetes cluster consists of **Nodes**, which can be equated to servers, be they bare-metal or virtual machines running in a cloud. 

Nodes run **Pods**, which are collections of Docker containers. A Pod is the unit of deployment in Kubernetes. All containers in a Pod share the same network and can refer to each other as if they were running on the same host. There are many situations in which it is advantageous to run more than one container in a Pod. Typically, you will run your application container as the main one in the Pod, and if needed one or more so-called "sidecar" containers, for functionality such as logging or monitoring. One particular case of sidecar containers is an "init container" which is guaranteed to run first, and which can be used for housekeeping tasks, for example for running database migrations (12-factor principle: “Admin processes: Run admin/management tasks as one-off processes”)

An application will typically use more than one Pod for fault tolerance and performance purposes. The Kubernetes object responsible for launching and maintaining the desired number of pods is called a **Deployment**. 

For Pods to communicate with other Pods, Kubernetes provides another kind of object called a **Service**. Services are tied to Deployments through Selectors and Labels. Services are also exposed to external clients either by exposing a **NodePort** as a static port on each Kubernetes node or by creating a **LoadBalancer** object, corresponding to an actual load balancer if it is supported by the cloud provider running the Kubernetes cluster.

For managing sensitive information such as passwords, API keys, and other credentials, Kubernetes provides the **Secret** object.

For one-off tasks, Kubernetes provides the **Job** object. A Job can use the same ConfigMap and Secret objects already in place for regular Deployments and Pods. The Job will run a given Pod once, then stop.


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

### AWS Tools

* [AWS IAM authenticator](https://github.com/kubernetes-sigs/aws-iam-authenticator).


### Learning Examples


* [Spin up a node server example](https://github.com/bt3gl/Learning_Kubernetes/tree/master/node-server-example).
* [Use kustomize to organize and combine YAML templates of your services and deployments](https://github.com/bt3gl/Learning_Kubernetes/tree/master/kustomize-example).
