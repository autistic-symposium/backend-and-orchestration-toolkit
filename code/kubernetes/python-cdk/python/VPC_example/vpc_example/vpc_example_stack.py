from aws_cdk import core, aws_ec2

class VpcExampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc(self, "MiaVPCTest", cidr="10.0.0.0/16", max_azs=3)
