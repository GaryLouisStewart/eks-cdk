#!/usr/bin/env python3
import os
from re import subn

import aws_cdk as cdk

from aws_cdk import (
    aws_ec2 as ec2,
)

from Stacks.vpc import eks_vpc
from Stacks.eks import EksCluster



app = cdk.App()

vpc_stack = eks_vpc(
    app, 
    "VPC",
    vpc_name="eks-dev",
    cidr_range="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    subnet_configuration=[ec2.SubnetConfiguration(
        subnet_type=ec2.SubnetType.PUBLIC,
        name="eks-public",
        cidr_mask=24,
    ),
    ec2.SubnetConfiguration(
        subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
        name="eks-private",
        cidr_mask=24
    )],
    max_azs=3
)

# EksclusterStack(app, "EksclusterStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.

#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.

#     env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */

#     #env=cdk.Environment(account='123456789012', region='us-east-1'),

#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#     )

app.synth()
