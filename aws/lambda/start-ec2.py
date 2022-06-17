import json
import boto3

openshift_tag = "tag:kubernetes.io/cluster/XXXXXXXX"
region = "ap-southeast-1"
state = "stopped"
bootup = True
ec2_to_bootup = []

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
          ec2_to_bootup.append(ec2inst.id)
    
    if bootup:
      print("Starting up these instances: %s)" % ec2_to_bootup)
      #for ec2ids in ec2_to_bootup:
      # ec2.instances.filter(InstanceIds = ec2ids).start()
      ec2.instances.filter(InstanceIds = ec2_to_bootup).start()
      return {
            'statusCode': 200,
            'body': json.dumps('%s started' % ec2_to_bootup)
        }
    else:
       print("Skipping starting, set 'bootup = True' in the script to execute the startup!")
       return {
        'statusCode': 200,
        'body': json.dumps('Bootup is false, skipped.')
       }
