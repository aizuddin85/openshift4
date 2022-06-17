import json
import boto3

openshift_tag = "tag:kubernetes.io/cluster/XXXXXXX"
region = "ap-southeast-1"
state = "running"
shutdown = True
ec2_to_shutdown = []

def lambda_handler(event, context):
    session = boto3.Session(region_name=region)
    
    ec2 = session.resource('ec2', region)
    
    instances = ec2.instances.filter(
          Filters=[
            {'Name': 'instance-state-name', 
             'Values': [state]},
            {'Name': openshift_tag,
             'Values': ['owned']}]
            )
    print("Listing all running instances for %s tag..." % openshift_tag)
    for ec2inst in instances:
      for tag in ec2inst.tags:
        if tag['Key'] == 'Name':
          print("Instance ID: %s, Instance Name:%s" % (ec2inst.id,tag['Value']))
          ec2_to_shutdown.append(ec2inst.id)
    
    if shutdown:
      print("Shutting down these instances: %s)" % ec2_to_shutdown)
      #for ec2ids in ec2_to_shutdown:
      ec2.instances.filter(InstanceIds = ec2_to_shutdown).stop()
      return {
            'statusCode': 200,
            'body': json.dumps('%s stopped' % ec2_to_shutdown)
        }
    else:
       print("Skipping shutdown, set 'shutdown = True' in the script to execute the shutdown!")
       return {
        'statusCode': 200,
        'body': json.dumps('Shutdown is false, skipped.')
       }
