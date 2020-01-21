# Setting up a VPC with CDK in Python

[AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) is a very neat way to write infrastructure as code, enabling you to create and provision AWS infrastructure deployments predictably and repeatedly.

You choose your favorite language to code what resources (stacks) you want, and CDK synthetizes them to CloudFormation and helps you to deploy them to AWS.

In this example we see how to setup a VPC using CDK in Python. 

### Install AWS CDK

Follow [this instructions](https://github.com/aws/aws-cdk#at-a-glance).

### Create a virtual environment and install dependencies:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note: If you are starting from a blank project with `cdk init app --language=python` instead, you will we need to manually install resources, such as `pip install aws_cdk.aws_ec2`.

### Define You VPC 

Define how you want your VPC in the file `vpc_example/vpc_example_stack.py`:

```
class VpcExampleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc(self, "MiaVPCTest", cidr="10.0.0.0/16", max_azs=3)
```


### Create synthesized CloudFormation template

```
cdk synth
```

You can check what changes this introduces into your AWS account:
```
cdk diff --profile <AWS PROFILE>
```

### Deploy to AWS

If everything looks right, deploy:

```
cdk deploy --profile <AWS PROFILE>
```

These are the resources that will be created with this command:

![vpc](https://github.com/bt3gl/AWS_Resources/blob/master/CDK_examples/VPC_example/imgs/vpc.png)



To check all the stacks in the app:

```
cdk ls
```

### Clean up

To destroy/remove all the newly created resources, run:

```
cdk destroy --profile <AWS PROFILE>
```

