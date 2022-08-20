# aws-vpc construct test suite
# author: Gary Louis Stewart
# date: 14-08-2022

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    assertions
)

from Stacks.vpc import eks_vpc
import pytest


# create a stack and vpc object to test against
stack = Stack()

vpc = eks_vpc(stack, "vpc",
        vpc_name="eks-test-vpc",
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
        max_azs=3,
    )
    
def test_vpc_is_created():
    template = assertions.Template.from_stack(vpc)
    template.resource_count_is("AWS::EC2::VPC", 1)

def test_vpc_cidr_range():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::VPC", {
        "CidrBlock" : "10.0.0.0/16"
    }
    )

def test_subnet_is_public():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::Subnet", {
        "MapPublicIpOnLaunch": True
    })


def test_subnet_is_private():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::Subnet", {
        "MapPublicIpOnLaunch": False
    })

def test_vpc_raises_max_az_error():
    stack = Stack()
    with pytest.raises(Exception):
        eks_vpc(stack, "vpc",
            vpc_name="eks-test-vpc",
            max_azs=1,
        )

def test_vpc_raises_name_error():
    stack = Stack()
    with pytest.raises(Exception):
        eks_vpc(stack, "vpc",
            max_azs=1,
        )

def test_vpc_dns_hostnames_is_true():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::VPC", {
        "EnableDnsHostnames": True
    })

def test_vpc_dns_support_is_true():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::VPC", {
        "EnableDnsSupport": True
    })

def test_instance_tenancy_is_default():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::VPC", {
        "InstanceTenancy": "default"
    })


def test_all_public_subnets_are_created():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::Subnet", {
        "MapPublicIpOnLaunch": True
    })
    template.resource_count_is("AWS::EC2::Subnet", 4)


def test_all_private_subnets_are_created():
    template = assertions.Template.from_stack(vpc)
    template.has_resource_properties("AWS::EC2::Subnet", {
        "MapPublicIpOnLaunch": False
    })
    template.resource_count_is("AWS::EC2::Subnet", 4)


def test_nat_gateways_are_created():
    template = assertions.Template.from_stack(vpc)
    template.resource_count_is("AWS::EC2::NatGateway", 2)
