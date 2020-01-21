import cdk = require('@aws-cdk/core');
import ec2 = require("@aws-cdk/aws-ec2");

export class VPCStack extends cdk.Stack {
  readonly Vpc: ec2.IVpc;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    const current_env = this.node.tryGetContext("env.type");

    const vpc_cidr = this.node.tryGetContext("vpc.cidr");
    const vpc_maxAzs = this.node.tryGetContext("vpc.maxAzs");
    const vpc = new ec2.Vpc(this, current_env+"Vpc", {
      cidr: vpc_cidr,
      maxAzs: vpc_maxAzs
    });
    this.Vpc = vpc;
  }
}
