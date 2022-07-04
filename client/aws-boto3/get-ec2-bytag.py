#!/usr/bin/python3

import boto3
import sys

openshift_tag = sys.argv[1]
state = "running"
shutdown = True
ec2_to_shutdown = []

session =  boto3.Session(region_name="ap-southeast-1")

ec2 = session.resource('ec2', "ap-southeast-1")

instances = ec2.instances.filter(
          Filters=[
            {'Name': 'instance-state-name', 
             'Values': [state]},
            {'Name': openshift_tag,
             'Values': ['owned']}]
            )
print("Listing all running instances for %s tag..." % openshift_tag) 


for ec2 in instances:
  for tag in ec2.tags:
      if tag['Key'] == 'Name':
          print("Instance ID: %s, Name:%s, FQDN:%s, Placement:%s, Size:%s, PrivateIPv4:%s" 
                  % (ec2.id,tag['Value'],ec2.private_dns_name,ec2.placement,ec2.instance_type,ec2.private_ip_address))