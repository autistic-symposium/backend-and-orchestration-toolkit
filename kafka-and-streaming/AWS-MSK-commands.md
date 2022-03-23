## AWS MSK Commands

### List clusters

Returns a list of all the MSK clusters in the current Region:

```
aws kafka list-clusters
```

### Describing the cluster

Returns a description of the MSK cluster whose (ARN) is specified in the request:

```
aws kafka describe-cluster --cluster-arn <arn>
```

### Listing nodes

Returns a list of the broker nodes in the cluste:

```
aws kafka list-nodes --cluster-arn <arn>
```

### Listing bootstrap brokers urls

A list of brokers that a client application can use to bootstrap:

```
aws kafka  get-bootstrap-brokers --cluster-arn <arn>
```

### List clusters operation

Returns a list of all the operations that have been performed on the specified MSK cluster:

```
aws kafka  list-cluster-operations --cluster-arn <arn>
```
