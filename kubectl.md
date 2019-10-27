## Kubectl Commands


#### **Pods**

Get pods:

```
    kubectl get pods -n <namespace>
```

Debug pods:

```
    kubectl describe pod <podname>
```

Get pod's log:

```
    kubectl logs <podname>
```

#### **Services**

Get services:

```
    kubectl get services -n <namespace>
```

#### **Deployments**

Get deployments:

```
    kubectl get deployment -n <namespace>
```

#### **Secrets**

```
    kubectl get secret
```

#### **Namespaces**

```
    kubectl get namespaces
```

#### **Configmaps**

```
    kubectl get configmaps -n <namespace>
```

#### **Ingress**

```
    kubectl get ingress -n <namespace>
```
