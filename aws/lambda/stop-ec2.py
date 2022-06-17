#!/usr/bin/python3

import boto3

openshift_tag = "tag:kubernetes.io/cluster/$cluster_id_here"
region = "ap-southeast-1"
state = "running"
shutdown = False
ec2_to_shutdown = []

session =  boto3.Session(region_name=region)

ec2 = session.resource('ec2', region)

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
          print("Instance ID: %s, Instance Name:%s" % (ec2.id,tag['Value']))
          ec2_to_shutdown.append(ec2.id)

if shutdown:
    print("Shutting down these instances: %s)" % ec2_to_shutdown)
    for ec2ids in ec2_to_shutdown:
      ec2.instances.filter(InstanceIds = ec2ids).stop()
else:
   print("Skipping shutdown, set 'shutdown = True' in the script to execute the shutdown!")