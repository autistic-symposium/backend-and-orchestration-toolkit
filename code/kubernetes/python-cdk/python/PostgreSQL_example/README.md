# Setting up a PostgreSQL RDS with CDK in Python

### Create a virtual environment and install dependencies:

```
virtualenv .env
source .env/bin/activate
pip3 install -r requirements.txt
```

### Define You RDS DB 

Add any constant variable in `cdk.json` and then define how you want your RDS instance in `postgre_sql_example/postgre_sql_example_stack.py`:

```
class PostgreSqlExampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Database Instance
        instance = rds.DatabaseInstance(self,
            'examplepostgresdbinstance', 
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
```

### Create synthesized CloudFormation templates

```
cdk synth
```

You can check what changes are introduced into your current AWS resources with:
```
cdk diff --profile <AWS PROFILE>
```


### Deploy to AWS

If everything looks OK, deploy with:

```
cdk deploy --profile <AWS PROFILE>
```

To check all the stacks in the app:

```
cdk ls
```

### Clean up

To destroy/remove all the newly created resources, run:

```
cdk destroy --profile <AWS PROFILE>
```
