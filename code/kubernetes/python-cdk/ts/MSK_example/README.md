# CDK MSK Example



### Deploy VPC

[Amazon VPC](https://aws.amazon.com/vpc/) lets you provision a logically isolated section of the AWS Cloud where you can all the resources as in a virtual network.

These are the default values in `cdk.json`:

```
"vpc.cidr": "10.0.0.0/16",
"vpc.maxAzs": 3,
```

Deploy with:

```
cdk deploy VPCStack
```

### Deploy MSK

[Amazon MSK](https://aws.amazon.com/msk/) is a managed service that makes it easy for you to build and run applications that use Apache Kafka to process streaming data.

These are the default values in `cdk.json`:

```
"msk.DevMskCluster": "MskCluster",
"msk.ClusterTag": "MSK cluster",
"msk.brokerNodeGroupBrokerAzDistribution": "DEFAULT",
"msk.enhancedMonitoring": "PER_BROKER",
"msk.brokerNodeGroupEBSVolumeSize": 100,
"msk.brokerNodeGroupInstanceType": "kafka.m5.large",
"msk.brokerPort": 9092,
"msk.kafkaVersion": "2.2.1",
"msk.numberOfBrokerNodes": 3
```

Deploy with:

```
cdk deploy MskClusterStack
```

#### Kafka CLI 

Note that the CLI commands for MKS are given by the keyword `kafka`, for example:

```
aws kafka list-clusters
```

To retrieve `BootstrapBrokerStringTls`, run:

```
 aws kafka get-bootstrap-brokers --cluster-arn <cluster ARN>
 ```

However, access and development within the cluster (e.g. creating topics, accessing brokers) need to be done while connected to the VPN.

