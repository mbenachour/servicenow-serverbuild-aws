import json
import datetime
import boto3
import sys
from dateutil import parser
from botocore.vendored import requests
from requests.auth import HTTPBasicAuth



def getAMI(os):
    os_search = ''
    if os == 'amazonlinux' :
        os_search = 'amzn-ami-hvm-*'

    client = boto3.client('ec2', region_name='us-east-1')
    filters = [ {
        'Name': 'name',
        'Values': [os_search]
    }]
    response = client.describe_images(Filters=filters)
    source_image = newest_image(response['Images'])
    #error check for NoneType to be implemented
    return source_image['ImageId']

def newest_image(list_of_images):
    latest = None

    for image in list_of_images:
        if not latest:
            latest = image
            continue

        if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
            latest = image

    return latest

def build(event, context):
    body = json.loads(event['body'])
    os = body['os']
    inst_size = body['inst_size']
    ami =  getAMI(os)
    vpcid = getVPC()
    subnet_id = getSubnet()
    EC2 = boto3.client('ec2', region_name='us-east-1')
    
    instance = EC2.run_instances(
        SubnetId=subnet_id,
        ImageId=ami,
        InstanceType=inst_size,
        MinCount=1, # required by boto, even though it's kinda obvious.
        MaxCount=1,
        InstanceInitiatedShutdownBehavior='terminate',
        TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'my_test_example'
                },
                
                   
                ],
            },
        ],
    )


    return {
        'statusCode': "200",
        'body': {
         "Server status":"in progress"
           
        }
    }

def getVPC():
    ec2 = boto3.resource('ec2')
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:Name', 'Values':['*VPC*']}]
    response = ec2client.describe_vpcs(Filters=filters)
    vpcid = ''
    #print(response)
    for vpc in response["Vpcs"]:
        vpcid = vpc["VpcId"]
    return vpcid



    

def getSubnet():
    ec2 = boto3.resource('ec2')
    ec2client = boto3.client('ec2')
    filters = [{'Name':'tag:Name', 'Values':['*Private*A*']}]
    response = ec2client.describe_subnets(Filters=filters)
    sub_id = ''
    #print(response)
    for sub in response["Subnets"]:
        sub_id = sub["SubnetId"]
    return sub_id


