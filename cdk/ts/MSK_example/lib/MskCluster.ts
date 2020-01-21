import cdk = require("@aws-cdk/core");
import ec2 = require("@aws-cdk/aws-ec2");
import msk = require("@aws-cdk/aws-msk");


interface MSKStackProps extends cdk.StackProps {
  vpc: ec2.IVpc;
}
export class MskClusterStack extends cdk.Stack {
  private vpc: ec2.IVpc;
  
  constructor(scope: cdk.Construct, id: string, props?: MSKStackProps) {
    super(scope, id, props);
    const current_env = this.node.tryGetContext("env.type");

    //****************************** Context variables **************************************//
    const clusterName = this.node.tryGetContext("msk.DevMskCluster");
    const clusterTag = this.node.tryGetContext("msk.mskClusterTag");
    const brokerNodeGroupBrokerAzDistribution = this.node.tryGetContext("msk.brokerNodeGroupBrokerAzDistribution");
    const brokerNodeGroupEBSVolumeSize = this.node.tryGetContext("msk.brokerNodeGroupEBSVolumeSize");
    const brokerNodeGroupInstanceType = this.node.tryGetContext("msk.brokerNodeGroupInstanceType");
    const brokerPort = this.node.tryGetContext("msk.brokerPort");
    const kafkaVersion = this.node.tryGetContext("msk.kafkaVersion");
    const numberOfBrokerNodes = this.node.tryGetContext("msk.numberOfBrokerNodes");
    const enhancedMonitoring = this.node.tryGetContext("msk.enhancedMonitoring");

    //****************************************  VPC 
    if (props)
      this.vpc = props.vpc;
    else
      this.vpc = ec2.Vpc.fromLookup(this, current_env+"Vpc", {
        vpcName: "VPCStack/"+current_env+"Vpc"
      });

    //****************************************  SG 
    const description = "Allow access to "+current_env+" MSK Cluster";
    const SecurityGroup = new ec2.SecurityGroup(
        this,
        current_env+"MskClusterSG",
        {
          vpc: this.vpc,
          securityGroupName: current_env+"MskClusterSG",
          description: description,
          allowAllOutbound: true
        }
    );
    SecurityGroup.addIngressRule(
        ec2.Peer.anyIpv4(),
        ec2.Port.tcp(brokerPort),
        description
    );

    //*******************************  MSK Cluster **************************//
    const cluster = new msk.CfnCluster(this, "MskCluster", {
        brokerNodeGroupInfo: {
          clientSubnets: this.vpc.privateSubnets.map(x => x.subnetId),
          instanceType: brokerNodeGroupInstanceType,
          brokerAzDistribution: brokerNodeGroupBrokerAzDistribution,
          storageInfo: {
            ebsStorageInfo: {
              volumeSize: brokerNodeGroupEBSVolumeSize
            }
          }
        },
        clusterName: clusterName,
        kafkaVersion: kafkaVersion,
        numberOfBrokerNodes: numberOfBrokerNodes,
        enhancedMonitoring: enhancedMonitoring,
        tags: {
          name: current_env+clusterTag,
        }
      });
    }
  }

