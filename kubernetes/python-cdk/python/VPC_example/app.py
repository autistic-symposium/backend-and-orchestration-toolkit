#!/usr/bin/env python3

from aws_cdk import core

from vpc_example.vpc_example_stack import VpcExampleStack


app = core.App()
VpcExampleStack(app, "vpc-example")

app.synth()
