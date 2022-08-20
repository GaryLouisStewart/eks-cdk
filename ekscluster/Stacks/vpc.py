# aws-vpc default construct using aws cdk
# author: Gary Louis Stewart
# date: 11-08-2022

from constructs import Construct

from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)


class eks_vpc(Stack):
    
    def __init__(self, scope: Construct, 
                id: str, vpc_name: str,  
                cidr_range: str, 
                enable_dns_support: bool,
                enable_dns_hostnames: bool, 
                subnet_configuration: list,
                max_azs: int = 3,
                **kwargs):

        if max_azs < 2 or max_azs > 6:
            raise ValueError("max_azs must be greater than 2 and less than 6")
        
        if vpc_name is None:
            raise ValueError("vpc_name not specified or is an empty string, please choose a name for your vpc...")
        

        super().__init__(scope, id, **kwargs)
        
        self.vpc = ec2.Vpc(self, "VPC",
            vpc_name=vpc_name,
            max_azs=max_azs,
            cidr=cidr_range,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            subnet_configuration=subnet_configuration
        )
