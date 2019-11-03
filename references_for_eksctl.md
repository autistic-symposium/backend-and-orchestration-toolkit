# Creating EKS cluster using the eksctl CLI

    eksctl create cluster \
    --name staging \
    --version 1.14 \
    --nodegroup-name staging-workers \
    --node-type m5.xlarge \
    --nodes 3 \
    --nodes-min 1 \
    --nodes-max 10 \
    --node-ami auto

## Create RDS PostgreSQL instance

Create `hydra` database and `hydradbadmin` user/role in the database.

    hydra=> CREATE DATABASE hydra;
    CREATE DATABASE
    hydra=> \q
    hydra=> CREATE ROLE hydradbadmin;
    CREATE ROLE
    hydra=> ALTER ROLE hydradbadmin LOGIN;
    ALTER ROLE
    hydra=> ALTER USER hydradbadmin PASSWORD 'PASS';
    ALTER ROLE

DB connection string: `postgres://hydradbadmin:PASS@staging.cjwa4nveh3ws.us-west-2.rds.amazonaws.com:5432/hydra`

## Create MongoDB database and user in Atlas

    MONGO_OPLOG_URL: mongodb://domain:PASS@cluster0-shard-00-02-gk3cz.mongodb.net.:27017,[cluster0-shard-00-01-gk3cz.mongodb.net](http://cluster0-shard-00-01-gk3cz.mongodb.net/).:27017,[cluster0-shard-00-00-gk3cz.mongodb.net](http://cluster0-shard-00-00-gk3cz.mongodb.net/).:27017/local?authSource=admin&gssapiServiceName=mongodb&replicaSet=Cluster0-shard-0&ssl=true
   
    MONGO_URL: mongodb://domain:PASS@cluster0-shard-00-02-gk3cz.mongodb.net.:27017,[cluster0-shard-00-01-gk3cz.mongodb.net](http://cluster0-shard-00-01-gk3cz.mongodb.net/).:27017,[cluster0-shard-00-00-gk3cz.mongodb.net](http://cluster0-shard-00-00-gk3cz.mongodb.net/).:27017/rc-staging?authSource=admin&gssapiServiceName=mongodb&replicaSet=Cluster0-shard-0&ssl=true

## Generate kubeconfig files for administrator and developer roles

Save the above file somewhere, then 

    export KUBECONFIG=/path/to/file
    export AWS_PROFILE=profilename

This configuration uses the `aws-iam-authenticator` binary (needs to exist locally) 
and maps an IAM role to an internal Kubernetes RBAC role. 

This was created in the EKS cluster with:

    kind: Role
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: k8s-developer-role
      namespace: staging
    rules:
      - apiGroups:
          - ""
          - "apps"
          - "batch"
          - "extensions"
        resources:
          - "configmaps"
          - "cronjobs"
          - "deployments"
          - "events"
          - "ingresses"
          - "jobs"
          - "pods"
          - "pods/attach"
          - "pods/exec"
          - "pods/log"
          - "pods/portforward"
          - "secrets"
          - "services"
        verbs:
          - "create"
          - "delete"
          - "describe"
          - "get"
          - "list"
          - "patch"
          - "update"
    ---
    kind: RoleBinding
    apiVersion: rbac.authorization.k8s.io/v1beta1
    metadata:
      name: k8s-developer-rolebinding
      namespace: staging
    subjects:
    - kind: User
      name: k8s-developer-user
    roleRef:
      kind: Role
      name: k8s-developer-role
      apiGroup: rbac.authorization.k8s.io

## Install nginx ingress controller and create ALB in front of nginx ingress service

The `Service` type for the `ingress-nginx` service is `NodePort` and not `LoadBalancer` 
because we don't want AWS to create a new Load Balancer every time we recreate the ingress. 

    kind: Service
    apiVersion: v1
    metadata:
      name: ingress-nginx
      namespace: kube-ingress
      labels:
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
    spec:
      type: NodePort
      selector:
        app: ingress-nginx
      ports:
      - name: http
        port: 80
        nodePort: 30080
        targetPort: http
      - name: https
        port: 443
        nodePort: 30443
        targetPort: https

Instead, we provision an ALB and send both HTTP and HTTPS traffic to a Target Group that targets port 30080 on 
the EKS worker nodes (which is the `nodePort` in the manifest above for HTTP traffic).

**NOTE**: need to add rule in EKS worker SG to allow SG of ALB to access port 30080.

## Create Kubernetes Secret for DockerHub credentials (for pulling private images)

    apiVersion: v1
    type: kubernetes.io/dockerconfigjson
    kind: Secret
    metadata:
        name: reaction-docker-hub
    data:
        .dockerconfigjson: BASE64_OF_DOCKERHUB_AUTH_STRING

    DOCKERHUB_AUTH_STRING={"auths":{"https://index.docker.io/v1/":{"username":"rck8s","password":"PASS","auth":"OBTAINED_FROM_DOCKER_CONFIG.JSON"}}}

This Secret was created in several namespaces (`default`, `staging`, `monitoring`, `logging`, `flux-system`)

## Install and customize Flux for GitOps workflow

Flux is installed in its own `flux-system` namespace.

To install it, it we ran:

    kustomize build overlays/staging | kubectl apply -f -

The default `Deployment` for Flux is using the `weaveworks/flux` Docker image, which as of its last 
version contains an older binary for `kustomize`. 

Here is the `Dockerfile` for that image:

    FROM fluxcd/flux:1.15.0
    
    ARG REACTION_ENVIRONMENT
    ENV SOPS_VERSION 3.4.0
    ENV REACTION_ENVIRONMENT=${REACTION_ENVIRONMENT}
    
    RUN /sbin/apk add npm
    RUN wget https://github.com/mozilla/sops/releases/download/${SOPS_VERSION}/sops-${SOPS_VERSION}.linux \
        -O /usr/local/bin/sops; chmod +x /usr/local/bin/sops
    

For now, the script `build_and_push_image_staging.sh` sets this variable to `staging`:

    #!/bin/bash
    
    COMMIT_TAG=$(git rev-parse --short HEAD)
    docker build --build-arg REACTION_ENVIRONMENT=staging -t reaction-flux:staging .
    docker tag reaction-flux:staging reactioncommerce/reaction-flux:staging-${COMMIT_TAG}
    docker push reactioncommerce/reaction-flux:staging-${COMMIT_TAG}


Flux generates an ssh key upon startup. We need to obtain that key with `fluxctl` and add 
it as a deploy key to the `reaction-gitops` GitHub repo:

    fluxctl --k8s-fwd-ns=flux-system identity

The `manifest-generation=true` argument allows Flux to inspect and use a special configuration file called 
`.flux.yaml` in the root of the associated Git repo. The contents of this file are:

    version: 1
    commandUpdated:
      generators:
        - command: ./generate_kustomize_output.sh

Flux will `cd` into the `git-path` (set to `.` in our case in the args above), then will run the `command` 
specified in the `.flux.yaml` file. The output of the command needs to be valid YAML, which Flux will apply 
to the Kubernetes cluster via `kubectl apply -f -`.

We can run whatever commands we need, following whatever conventions we come up with, inside the `generate_kustomize_output.sh` script. Currently we do something along these lines:

    #!/bin/bash
    
    if [ -z $ENVIRONMENT ]; then
      echo Please set the ENVIRONMENT environment variable to a value such as staging before running this script.
      exit 1
    fi
    
    # this is necessary when running npm/npx inside a Docker container
    npm config set unsafe-perm true
    
    cd kustomize
    for SUBDIR in `ls`; do
      if [ "$1" ] && [ "${SUBDIR}" != "$1" ]; then
        continue
      fi
      OVERLAY_DIR=${SUBDIR}/overlays/${ENVIRONMENT}
      if [ ! -d "${OVERLAY_DIR}" ]; then
        continue
      fi
      if [ -d "${OVERLAY_DIR}/.sops" ]; then
        # decrypt sops-encrypted values and merge them into stub manifests for Secret objects
        npx --quiet --package @reactioncommerce/merge-sops-secrets@1.2.1 sops-to-secret ${OVERLAY_DIR}/secret-stub.yaml > ${OVERLAY_DIR}/secret.yaml
      fi
      # generate kustomize output
      kustomize build ${OVERLAY_DIR}
      echo "---"
      rm -rf ${OVERLAY_DIR}/secret.yaml
    done

Flux will do a `git pull` against the branch of the `reaction-gitops` repo specified in the 
command-line args (`master` in our case) every 5 minutes, and it will run the `generate_kustomize_output.sh` script, then will run `kubectl apply -f -` against the output of that script, applying any manifests that have changed.

The Flux `git pull` can also be forced with `fluxctl sync`:

    fluxctl sync --k8s-fwd-ns flux-system

To redeploy a Flux container for example when the underlying Docker image changes, do this in the 
`reaction-gitops` root directory:

    cd bootstrap/flux
    kustomize build overlays/staging | kubectl apply -f - 


## Management of Kubernetes secrets

We use sops to encrypt secret values for environment variables representing credentials, database connections, etc.

We create one file per secret in directories of the format `kustomize/SERVICE/overlays/ENVIRONMENT/.sops.`

We encrypt the files with a KMS key specified in `.sops.yaml` in the directory `kustomize/SERVICE/overlays/ENVIRONMENT`. 

Example:

    cd kustomize/hydra/overlays/staging
    echo -n "postgres://hydradbadmin:PASS@staging.cjwa4nveh3ws.us-west-2.rds.amazonaws.com:5432/hydra" > .sops/DATABASE_URL.enc
    sops -e -i .sops/DATABASE_URL.enc

We also create a `secret-stub.yaml` file in the directory `kustomize/SERVICE/overlays/ENVIRONMENT` similar to this:

    $ cat overlays/staging/secret-stub.yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: hydra
    type: Opaque
    data:
      DATABASE_URL: BASE64_OF_PLAIN_TEXT_SECRET
      OIDC_SUBJECT_TYPE_PAIRWISE_SALT: BASE64_OF_PLAIN_TEXT_SECRET
      SYSTEM_SECRET: BASE64_OF_PLAIN_TEXT_SECRET

The Flux container will call the `generate_kustomize_output.sh` script, which will decrypt the files via Pete's `@reactioncommerce/merge-sops-secrets@1.2.1 sops-to-secret` utility and will stitch their values inside `secret-stub.yaml`, saving the output in a `secret.yaml` file which will then be read by `kustomize`. 

Here is the relevant section from the `generate_kustomize_output.sh` script:

    npx --quiet \
         --package @reactioncommerce/merge-sops-secrets@1.2.1 \
         sops-to-secret ${OVERLAY_DIR}/secret-stub.yaml > ${OVERLAY_DIR}/secret.yaml

The Flux container needs to be able to use the KMS key for decryption, so we had to create an IAM policy allowing access to this KMS key, then attach the policy to the EKS worker node IAM role.

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "kms:GetKeyPolicy",
                    "kms:Decrypt",
                    "kms:DescribeKey",
                    "kms:GenerateDataKey*"
                ],
                "Resource": "arn:aws:kms:us-west-2:773713188930:key/a8d73206-e37a-4ddf-987e-dbfa6c2cd2f8"
            }
        ]
    }

## Kubernetes manifest generation with Kustomize

We use Kustomize to generate Kubernetes manifests in YAML format. 
There are several directories under the `kustomize` directory, one for each service to be deployed.

Example directory structure under `kustomize/reaction-storefront`:

    |____overlays
    | |____staging
    | | |____patch-deployment-imagepullsecret.yaml
    | | |____kustomization.yaml
    | | |____hpa.yaml
    | | |____secret-stub.yaml
    | | |____.sops
    | | | |____SESSION_SECRET.enc
    | | | |____OAUTH2_CLIENT_SECRET.enc
    | | |____configmap.yaml
    | | |____.sops.yaml
    |____base
    | |____deployment.yaml
    | |____ingress.yaml
    | |____kustomization.yaml
    | |____service.yaml

The manifests under the `base` directory define the various Kubernetes objects that will be created for `reaction-storefront` (similar to YAML manifests under the `templates` directory of a Helm chart, but with no templating). In this example we have a Deployment, a Service and an Ingress defined in their respective files.

The file `base/kustomization.yaml` specifies how these manifests files are collated and how other common information is appended:

    $ cat base/kustomization.yaml
    # Labels to add to all resources and selectors.
    commonLabels:
      app.kubernetes.io/component: frontend
      app.kubernetes.io/instance: reaction-storefront
      app.kubernetes.io/name: reaction-storefront
    
    # Value of this field is prepended to the
    # names of all resources
    #namePrefix: reaction-storefront
    
    configMapGenerator:
    - name: reaction-storefront
    
    # List of resource files that kustomize reads, modifies
    # and emits as a YAML string
    resources:
    - deployment.yaml
    - ingress.yaml
    - service.yaml

The  customization for a specific environment such as `staging` happens in files in the directory `overlays/staging`. Here is the `kustomization.yaml` file from that directory:

    $ cat overlays/staging/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization
    namePrefix: staging-
    namespace: staging
    images:
    - name: docker.io/reactioncommerce/reaction-next-starterkit
      newTag: 4e1c281ec5de541ec6b22c52c38e6e2e6e072a1c
    resources:
    - secret.yaml
    - ../../base
    patchesJson6902:
    - patch: |-
        - op: replace
          path: /spec/rules/0/host
          value: storefront.staging.reactioncommerce.io
      target:
        group: extensions
        kind: Ingress
        name: reaction-storefront
        version: v1beta1
    patchesStrategicMerge:
    - configmap.yaml
    - patch-deployment-imagepullsecret.yaml

Some things to note:

- You can customize the Docker image and tag used for a container inside a pod
- You can specify a prefix to be added to all object names, so a deployment declared in the `base/deployment.yaml` file with the name `reaction-storefront` will get `staging-` in front and will become `staging-reaction-storefront`
- You can apply patches to the files under `base` and specify values specific to this environment

Patches can be declared either inline in the `kustomization.yaml` file (such as the Ingress patch above), or in separate YAML files (such as the files in the `patchesStrategicMerge` section).

Here is an example of a separate patch file:

    $ cat overlays/staging/patch-deployment-imagepullsecret.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: reaction-storefront
    spec:
      template:
        spec:
          imagePullSecrets:
          - name: reaction-docker-hub

You need to specify enough information in the patch file for `kustomize` to identify the object to be patched. If you think of the YAML manifest as a graph with nodes specified by a succession of keys, then the patch needs to specify which node needs to be modified or added, and what is the new value for that key. In the example above, we add a new key at `spec->template->spec->imagePullSecrets->0 (item index)->name` and set its value to `reaction-docker-hub`.

**Environment variables** for a specific environment are set in the `configmap.yaml` file in the `overlays/ENVIRONMENT` directory. Example for `reaction-storefront`:

    $ cat overlays/staging/configmap.yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: reaction-storefront
    data:
      CANONICAL_URL: https://storefront.staging.reactioncommerce.io
      DEFAULT_CACHE_TTL: "3600"
      ELASTICSEARCH_URL: http://elasticsearch-client:9200
      EXTERNAL_GRAPHQL_URL: https://api.staging.reactioncommerce.io/graphql-beta
      HYDRA_ADMIN_URL: http://staging-hydra:4445
      INTERNAL_GRAPHQL_URL: http://staging-reaction-core/graphql-beta
      OAUTH2_ADMIN_PORT: "4445"
      OAUTH2_AUTH_URL: https://auth.staging.reactioncommerce.io/oauth2/auth
      OAUTH2_CLIENT_ID: staging-storefront
      OAUTH2_HOST: staging-hydra
      OAUTH2_IDP_HOST_URL: https://api.staging.reactioncommerce.io/
      OAUTH2_REDIRECT_URL: https://storefront.staging.reactioncommerce.io/callback
      OAUTH2_TOKEN_URL: http://staging-hydra:4444/oauth2/token
      PRINT_ERRORS: "false"
      SEARCH_ENABLED: "false"
      SESSION_MAX_AGE_MS: "2592000000"

Another example of a patch is adding `serviceMonitorNamespaceSelector` and `serviceMonitorSelector` sections to a Prometheus manifest file:

    $ cat bootstrap/prometheus-operator/overlays/staging/patch-prometheus-application-selectors.yaml
    apiVersion: monitoring.coreos.com/v1
    kind: Prometheus
    metadata:
      labels:
        prometheus: application
      name: application
      namespace: monitoring
    spec:
      serviceMonitorNamespaceSelector:
        matchExpressions:
        - key: name
          operator: In
          values:
          - staging
      serviceMonitorSelector:
        matchLabels:
          monitoring: application

**In short, the Kustomize patching mechanism is powerful, and it represents the main method for customizing manifests for a given environment while keeping intact the default manifests under the `base` directory.**

## Automated PR creation into reaction-gitops from example-storefront

We added a job to the CircleCI workflow for `reactioncommerce/example-storefront` (`master` branch) to create a PR automatically against `reactioncommerce/reaction-gitops`. 

The PR contains a single modification of the `reaction-storefront/overlays/staging/kustomize.yaml` file. It sets the Docker image tag to the CIRCLE_SHA1 of the current build by calling `kustomize edit set image [docker.io/${DOCKER_REPOSITORY}:${CIRCLE_SHA1}](http://docker.io/$%7BDOCKER_REPOSITORY%7D:$%7BCIRCLE_SHA1%7D)`.

Details here:

[https://github.com/reactioncommerce/example-storefront/blob/master/.circleci/config.yml#L101](https://github.com/reactioncommerce/example-storefront/blob/master/.circleci/config.yml#L101)

## Set up ElasticSearch and Fluentd for Kubernetes pod logging

Create IAM policy and add it to EKS worker node role:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams",
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "*",
                "Effect": "Allow"
            }
        ]
    }

Create ElasticSearch domain `staging-logs` and configure it to use Amazon Cognito for user authentication for Kibana.

Download `fluentd.yml` from [https://eksworkshop.com/logging/deploy.files/fluentd.yml](https://eksworkshop.com/logging/deploy.files/fluentd.yml) , kustomize it, then install `fluentd` manifests for staging:

    $ kustomize build bootstrap/fluentd/overlays/staging | kubectl create -f -
