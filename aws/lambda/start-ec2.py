#!/usr/bin/python3

import boto3

openshift_tag = "tag:kubernetes.io/cluster/$cluster_id_here"
state = "stopped"
region = "ap-southeast=1"
bootup = False
ec2_to_bootup = []

session =  boto3.Session(region_name=region)

ec2 = session.resource('ec2', region)

instances = ec2.instances.filter(
          Filters=[
            {'Name': 'instance-state-name', 
             'Values': [state]},
            {'Name': openshift_tag,
             'Values': ['owned']}]
            )
print("Listing all stopped instances for %s tag..." % openshift_tag) 

for ec2 in instances:
  for tag in ec2.tags:
      if tag['Key'] == 'Name':
          print("Instance ID: %s, Instance Name:%s" % (ec2.id,tag['Value']))
          ec2_to_bootup.append(ec2.id)

if bootup:
    print("Booting up these instances: %s)" % ec2_to_bootup)
    for ec2ids in ec2_to_bootup:
      ec2.instances.filter(InstanceIds = ec2ids).start()
else:
   print("Skipping bootup, set 'bootup = True' in the script to execute the shutdown!")