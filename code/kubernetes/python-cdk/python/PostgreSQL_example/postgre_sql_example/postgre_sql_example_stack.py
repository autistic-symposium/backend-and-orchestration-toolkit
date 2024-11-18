import json
import sys
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core as core,
)

# Python CDK does not have get_context yet.
def _get_context():
    CONTEXT_FILE = 'cdk.json'
    try:
        with open(CONTEXT_FILE, 'r') as f:
            return json.load(f)['context']
    except IOError:
        print('Could not open context file {}. Exiting...'.format(CONTEXT_FILE))
        sys.exit(1)
    except KeyError as e:
        print('Context file {0} is misconfigured {1}. Exiting...'.format(CONTEXT_FILE, e))
        sys.exit(1)

class PostgreSqlExampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Grab variables from cdk.json
        context = _get_context()
        auto_minor_version_upgrade =  context["rds.auto_minor_version_upgrade"]
        availability_zone = context["rds.availability_zone"]
        backup_retention = core.Duration.days(context["rds.backup_retention"])
        database_name = context["rds.database_name"]
        enable_performance_insights = context["rds.enable_performance_insights"]
        master_username = context["rds.master_username"]
        monitoring_interval = core.Duration.seconds(context["rds.monitoring_interval"])
        multi_az = context["rds.multi_az"]
        storage_encrypted = context["rds.storage_encrypted"]
        cidr = context["vpc.cidr"]
        max_azs = context["vpc.max_azs"]

        # Set VPC
        self.vpc = ec2.Vpc(self, "VPCTest", cidr=cidr, max_azs=max_azs)

        # Database Instance
        instance = rds.DatabaseInstance(self,
            'storefrontrdspostgresdbinstance', 
            master_username=master_username,
            engine=rds.DatabaseInstanceEngine.POSTGRES, instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO), 
            vpc=self.vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            database_name=database_name,
            enable_performance_insights=enable_performance_insights,
            storage_encrypted=storage_encrypted,
            multi_az=multi_az,
            backup_retention=backup_retention,
            monitoring_interval=monitoring_interval,
         )

