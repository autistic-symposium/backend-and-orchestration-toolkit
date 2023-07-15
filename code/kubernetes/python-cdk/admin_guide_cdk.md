# GitOps, Flux, and Deploying services with CDK

An introduction to some concepts and tools we will be using. 

## What's **GitOps**

In general, there are two ways to deploy infrastructure changes:

- **Procedural way**: telling some tools what to do, e.g.: Ansible. This is also known as a push model.
- **Declarative way**: telling some tool what you want to have done, also known as infrastructure as code, e.g.: Terraform, Pulumi, CDK.

[GitOps](https://www.weave.works/technologies/gitops/) is a term created by WeWorks and works by using Git as a source of truth for declarative infrastructure and applications. Automated CI/CD pipelines roll out changes to your infrastructure after commits are pushed and approved in Git. 

The GitOps methodology consists in describing the desired state of the system using a **declarative** specification for each environment (e.g., our Kubernetes cluster for a specific environment):

- A Git repo is the single source of truth for the desired state of the system
- All changes to the desired state are Git commits
- All specified properties of the cluster are also observable in the cluster so that we can detect if the desired and observed states are the same (converged) or different (diverged)

In GitOps you only push code. The developer interacts with the source control, which triggers the CI/CD tool (CicleCI), and this pushes the docker image to the container register (e.g. docker hub). You see the Docker image as an artifact.

To deploy that Docker image, you have a different config repository which contains the Kubernetes manifests. CircleCI sends a pull request, and when it is merged, a pod in the Kubernetes cluster pulls the image to the cluster (similar to `kubectl apply`, or even `helm update`). Everything is controlled through pull requests. You push code, not containers.

The refereed pod runs a tool called [Flux](https://github.com/fluxcd/flux), which automatically ensures that the state of a cluster matches the config in Git. It uses an operator in the cluster to trigger deployments inside Kubernetes, which means you don't need a separated CircleCI. It monitors all relevant image repositories, detects new images, triggers deployments, and updates the desired running configuration based on that.

## Kubernetes

A Kubernetes cluster consists of a series of objects:

- **Nodes**, which can be equated to servers, be they bare-metal or virtual machines running in a cloud.
- Nodes run **Pods**, which are collections of Docker containers. A Pod is the unit of deployment in Kubernetes. All containers in a Pod share the same network and can refer to each other as if they were running on the same host. The Kubernetes object responsible for launching and maintaining the desired number of pods is called a **Deployment.**
- For Pods to communicate with other Pods, Kubernetes provides another kind of object called a **Service.**
- Services are tied to Deployments through **Selectors** and **Labels,** and are also exposed to external clients either by exposing a **NodePort** as a static port on each Kubernetes node or by creating a **LoadBalancer** object.

## Kustomize

Kustomize provides a **purely declarative approach** to configuration customization that adheres to and leverages the familiar and carefully designed Kubernetes API.

Kustomize lets you customize raw, template-free YAML files for multiple purposes, leaving the original YAML untouched and usable as is. Kustomize targets Kubernetes; it understands and can patch.

### How Kustomize works

For each service, there is two directories, where a `kustomization.yaml` file list all the `yaml` files inside them: 

- `base/` - usually immutable.
- `overlay/`- where you add customizations and new code.

---

# **Bootstrapping Services in an AWS EKS cluster**

## **Pre-requisites**

### **Install CLI tools**

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
- [sops](https://github.com/mozilla/sops).
- [Kustomize](https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md).
- [fluxctl](https://www.weave.works/blog/install-fluxctl-and-manage-your-deployments-easily).

### **Get access to our AWS Cluster**

We spin up clusters' resources using AWS CDK. This provisions a **developer EKS cluster** and **MSK cluster**, together with the following resources: a dedicated **VPC**, a **VPN**, **Elasticsearch cluster**, **Cloudwatch dashboards**, and an **RDS Postgres instance configured for Hydra.**

This staging and dev clusters are already available for you in our AWS staging account. For full access you need:

- AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)
- The VPN `.ovpn` file (can be downloaded from the dashboard) and VPN client private key.
- Kubeconfig file.

However, if you would like to bootstrap an entirely new cluster, follow the instructions below.


## **Bootstrapping Step-by-step**

### **Update Kubeconfig**

Edit `./bootstrap/kubeconfig/aws-auth-configmap.yaml` with your account's `rolearn`.

Set env variables:

    export REGION=<aws region>

Get kubectl config:

    ./get_kubeconfig.sh

Remember, you can always change your kubeconfig context with:

    kubectl config use-context <context>

You can also use [kubectx](https://github.com/ahmetb/kubectx) for this.

### **Create Nginx ingress controller in the EKS cluster**

Create Nginx ingress controller's namespaces, services, roless, deployments, etc. by running:

    kubectl apply -f ./bootstrap/nginx-ingress-alb/all-in-one.yaml

This is the output:

    namespace/kube-ingress created
    serviceaccount/nginx-ingress-controller created
    clusterrole.rbac.authorization.k8s.io/nginx-ingress-controller created
    role.rbac.authorization.k8s.io/nginx-ingress-controller created
    clusterrolebinding.rbac.authorization.k8s.io/nginx-ingress-controller created
    rolebinding.rbac.authorization.k8s.io/nginx-ingress-controller created
    service/nginx-default-backend created
    deployment.extensions/nginx-default-backend created
    configmap/ingress-nginx created
    service/ingress-nginx created
    deployment.extensions/ingress-nginx created
    priorityclass.scheduling.k8s.io/high-priority created

Check whether all the pods created:

    kubectl get pods --namespace kube-ingress

Should result:

    NAMESPACE      NAME                                    READY   STATUS    RESTARTS   AGE
    kube-ingress   ingress-nginx-55966f5cf8-bpvwj          1/1     Running   0          7m53s
    kube-ingress   ingress-nginx-55966f5cf8-vssfl          1/1     Running   0          7m53s
    kube-ingress   ingress-nginx-55966f5cf8-xtkv9          1/1     Running   0          7m53s
    kube-ingress   nginx-default-backend-c4bbbc8b7-j5cnh   1/1     Running   0          7m57s

Check all the services created:

    kubectl get services --namespace kube-ingress

Should result:

    NAMESPACE      NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
    kube-ingress   ingress-nginx           NodePort    172.20.203.36   <none>        80:30080/TCP,443:30443/TCP   6m32s
    kube-ingress   nginx-default-backend   ClusterIP   172.20.128.3    <none>        80/TCP                       6m35s

Note that the `Service` type for the `ingress-nginx` service is `NodePort` and not `LoadBalancer`. We don't want AWS to create a new Load Balancer every time we recreate the ingress. Instead, we provision an ALB and send both HTTP and HTTPS traffic to a `Target Group` that targets port `30080` on the EKS worker nodes (which is the `nodePort` in the manifest above for HTTP traffic).

### **Create a namespace in the EKS cluster**

This step is necessary in case you are creating an entirely new cluster namespace (i.e., if it's not `dev` nor `staging`).

To add a new namespace, just follow the current examples in `/bootstrap/namespaces/overlays/` and then apply the changes in the overlay:

    cd ./bootstrap/namespaces/overlays/
    kustomize build . |  kubectl apply -k <namespace>

You should see something like:

    namespace/<namespace> created
    namespace/logging created
    namespace/monitoring created
    namespace/observability created

Check whether it worked:

    kubectl get ns

### **Create secret for DockerHub credentials in EKS cluster**

All right, if you are working on an AWS account that is not staging, hold tight, because this step is a trip.

Currently, we use [sops](https://github.com/mozilla/sops) to manage secrets in Kubernetes.

You have a file named `./bootstrap/dockerhub-creds-secret/docker-hub.yaml` that possess the secret for DockerHub credentials and it's encrypted. So the first thing we need to do is decrypt it so we can use the secret for our cluster. The caveat is that you need to set your AWS creds to the account `773713188930` (staging) account (or it won't be able to grab the key to decrypt):

    sops -d  docker-hub.yaml > dec.yaml

Take a look at `dec.yaml`, you will see something like this:

    apiVersion: v1
    type: kubernetes.io/dockerconfigjson
    kind: Secret
    metadata:
        name: docker-hub
    data:
        .dockerconfigjson: <Base64 1337 password>

Now, the next step is either to go to the [AWS KMS dashboard](https://us-east-2.console.aws.amazon.com/kms/home?region=us-east-2#/kms/keys) or run `aws kms create-custom-key-store` to create a `Customer managed keys`.

KMS is a service that encrypts and decrypts data with AES_GCM, using keys that are never visible to users of the service. Each KMS master key has a set of role-based access controls, and individual roles are permitted to encrypt or decrypt using the master key. KMS helps solve the problem of distributing keys, by shifting it into an access control problem that can be solved using AWS's trust model.

Once you have this ready, grab its ARN.

Create a new encrypted file with your new KMS key:

    sops --kms="ARN" --encrypt  dec.yaml > docker-hub-<MY CLUSTER>.yaml


This Secret is created in several namespaces (default, monitoring, logging, flux-system).

### **Apply overlay config for fluentd, jaeger-operator and prometheus-operator**

Follow the same procedure for each of these services: `./bootstrap/fluentd`, `./bootstrap/jaeger-operator` and `./bootstrap/prometheus-operator`, copying an overlay subdirectory for your namespace, replacing your namespace string to anywhere where `staging` is, and running:

    cd ./bootstrap/<service>/overlays/<namespace>
    kustomize build . | kubectl apply -f -

### **Install and configure Flux in EKS cluster**

This part is a little longer. [Here](https://docs.fluxcd.io/en/latest/tutorials/get-started-kustomize.html) is the official Flux documentation with Kustomize.

Flux (and memcached) is bootstrapped by following the instructions inside `bootstrap/flux/`. That directory should have the following structure:

    ├── base
    │   ├── flux
    │   └── memcached
    ├── overlays

The first step is creating an `overlay/<namespace>` directory for your deployment, similar to `overlay/staging`.

### **How Flux works**

Flux runs by looking at `./.flux.yaml`. This calls `./generate_kustomize_output.sh` in a docker container and runs the following:

1. Set the environment (e.g. `staging`).
2. For each sub-directory in `kustomize/`, `cd` inside each `overlays/` for the environment and runs `kustomize build`.
3. If there are `sops` secrets inside these directories, decrypts the secret as well.

### **Setting up Flux Docker image**

The default `Deployment` for Flux is using `weaveworks/flux` Docker image.

You will need to push a docker image to DockerHub for your namespace. 

Once you have a [docker image in Docker Hub] grab its tag (e.g. `staging-af87bcc`).


### **Building and deploying**

Inside your overlay directory, run:

    cd bootstrap/flux/overlays/<namespace>
    kustomize build . | kubectl apply -f -

You should see the following:

    namespace/flux-system created
    serviceaccount/flux created
    podsecuritypolicy.policy/flux created
    role.rbac.authorization.k8s.io/flux created
    clusterrole.rbac.authorization.k8s.io/flux-psp created
    clusterrole.rbac.authorization.k8s.io/flux created
    clusterrole.rbac.authorization.k8s.io/flux-readonly created
    rolebinding.rbac.authorization.k8s.io/flux created
    clusterrolebinding.rbac.authorization.k8s.io/flux-psp created
    clusterrolebinding.rbac.authorization.k8s.io/flux created
    configmap/flux-kube-config-hmbbmcb469 created
    secret/flux-git-deploy created
    service/flux-memcached created
    deployment.apps/flux created
    deployment.apps/flux-memcached created

Wait for Flux and memcached to start:

    kubectl -n flux-system rollout status deployment.apps/flux

Check that the pods are up:

    kubectl get pods --namespace flux-system

You should see two pods, something like this:

    NAME                              READY   STATUS    RESTARTS   AGE
    flux-<some string>                1/1     Running   0          21m
    flux-memcached-<some string>      1/1     Running   0          60m

At any point you can debug your pod by running:

    kubectl describe pod  flux-<some string> -n flux-system

### **Adding key to Github**

Generate a deployment key:

    fluxctl --k8s-fwd-ns=flux-system identity


Later on, when you have everything set, you can force Flux `git pull` with

    fluxctl sync --k8s-fwd-ns flux-system


### **Create k8s-developer-role in multiple namespaces in EKS cluster**

Similarly to the previous step, create an overlay to your namespace (e.g. dev) in the [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) kustomize resources. You can do this by copying the files from `./bootstrap/rbac/overlays/staging`, and changing the namespace string from `staging` inside `k8s-developer-user.yaml`:

    ...
    metadata:
      name: k8s-developer-role
      namespace: <namespace>
    ...
    metadata:
      name: k8s-developer-rolebinding
      namespace: <namespace>

Apply the changes with:

    cd bootstrap/rbac/overlays/<namespace>
    kustomize build . | kubectl apply -f -

You should see the following:

    role.rbac.authorization.k8s.io/k8s-developer-role-default created
    role.rbac.authorization.k8s.io/k8s-developer-role created
    role.rbac.authorization.k8s.io/k8s-developer-role-monitoring created
    rolebinding.rbac.authorization.k8s.io/k8s-developer-rolebinding-default created
    rolebinding.rbac.authorization.k8s.io/k8s-developer-rolebinding created
    rolebinding.rbac.authorization.k8s.io/k8s-developer-rolebinding-monitoring created



---

# **Deploying Advanced services in an AWS EKS cluster**


## **Porting Hydra**

### **Customizing the overlay directory**

Inside `./kustomize/hydra`, create `overlay/` subdirectory for your environment.

Create a KMS key (the same way as in step *Create secret for DockerHub credentials in EKS cluster* in `./boostrap`). Grab its ARN and add it too `./kustomize/hydra/overlays/.sops.yaml`.

Replace the `staging` string (and the correct host URLS) for your namespace, inside `kustomization.yaml`, `configmap.yaml`.

### **Creating sops secrets for Hydra**

We use sops to encrypt secret values for environment variables representing credentials, database connections, etc. so that Flux can pick these secrets when it needs.

We place these files inside a `.sops/` directory inside the overlay environment directory.

Grab the RDS Postgres data and create secret string:

    echo -n "postgres://hydradbadmin:< hydra_passport>@<hydra_db_endpoint" > .sops/DATABASE_URL.enc
    sops -e -i .sops/DATABASE_URL.enc

Create password salt:

    echo -n "<random_string" > .sops/OIDC_SUBJECT_TYPE_PAIRWISE_SALT.enc
    sops -e -i .sops/OIDC_SUBJECT_TYPE_PAIRWISE_SALT.enc

Create system secret:

    echo -n "<random_string" > .sops/SYSTEM_SECRET.enc
    sops -e -i .sops/SYSTEM_SECRET.enc

Generate `secrets.yaml':

    npx --quiet --package @reactioncommerce/merge-sops-secrets@1.2.1 sops-to-secret secret-stub.yaml > secret.yaml

### **Building and applying**

Now, just run:

    cd ./kustomize/hydra/overlays/<namespace>
    kustomize build . | kubectl apply -f -


### **Create MongoDB database and user in Atlas**

So that you can have MongDB URL and MongDB OPLOG URL for the next step.

### **Creating sops secrets**

Create MongDB URL secret:

    echo -n "<atlas url>" .sops/MONGO_URL.enc
    sops -e -i .sops/MONGO_URL.enc

Create MongDB OPLOG URL secret:

    echo -n "<atlas ops url>" .sops/MONGO_OPLOG_URL.enc
    sops -e -i .sops/MONGO_OPLOG_URL.enc


Generate `secrets.yaml':

    npx --quiet --package @reactioncommerce/merge-sops-secrets@1.2.1 sops-to-secret secret-stub.yaml > secret.yaml

### **Building and applying**

Now, just run:

    cd ./kustomize/hydra/overlays/<namespace>
    kustomize build . | kubectl apply -f -


### **Testing pod**

    kubectl get pods -ntest

Exec to the pod:

    kubectl exec -it <cdc-toolbox-HASH> -ntest -- bash

## **Setting DNS Records**


### **Adding NS recorders**

First, add the nameserver records for `ENV.doman.io` in [Route53](https://console.aws.amazon.com/route53/home?region=us-east-2#hosted-zones:).

### **Adding Certificate**

You might have to add a net certificate `*.ENV.domain.io/` to [ACM](https://us-east-2.console.aws.amazon.com/acm/home?region=us-east-2#/), then add its record in Route53 (as CNAME), and associate it to the load balancer.

In the [load balancer dashboard](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LoadBalancers:sort=loadBalancerName), go to listeners and make sure `HTTPS : 443` uses that certificate. Make sure the load balancer has the correct security groups.

### **Add All aliases**

Then add all the URL aboves as IPv4 aliases pointing them to the load balancer.


