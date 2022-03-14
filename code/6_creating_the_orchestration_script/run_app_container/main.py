# Imports
import boto3
import time
import json
from vpc_util import setup_vpc, teardown_vpc




# Constants
VPC_NAME_TAGS = {
    'VPC': 'demo-vpc',
    'PUBLIC_SUBNET': 'demo-pub-snet-1',
    'PRIVATE_SUBNET_1': 'demo-pvt-snet-1',
    'PRIVATE_SUBNET_2': 'demo-pvt-snet-2',
    'INTERNET_GATEWAY': 'demo-igw',
    'PUBLIC_ROUTE_TABLE': 'demo-pub-rtbl',
    'ELASTIC_IP': 'demo-eip',
    'NAT_GATEWAY': 'demo-natgw',
    'PRIVATE_ROUTE_TABLE': 'demo-pvt-rtbl'
}




# Functions
def lambda_handler(event, context):
    # The AWS account id
    aws_account_id = event['AWS_ACCOUNT_ID']

    # AWS SDK client that lets us create & teardown the VPC
    ec2_client = boto3.client('ec2', region_name = 'us-east-1')

    # AWS SDK client that lets us run ECS taks
    ecs_client = boto3.client('ecs')

    # VPC tags
    vpc_tags = {}

    # Setting up the VPC
    print('Setting up the VPC... ... ...')
    service_ids = setup_vpc(ec2_client, VPC_NAME_TAGS, **vpc_tags)
    
    # Running the AWS Fargate ECS task
    print('Running the containerized user application as a Fargate task on the ECS cluster... ... ...')
    ip_args = json.dumps(event['RUNTIME_ARGS'])
    print(f'Input Arguments: {ip_args}')
    ecs_task_response = ecs_client.run_task(    cluster = f'arn:aws:ecs:us-east-1:{aws_account_id}:cluster/ecs-cluster',
                                                launchType = 'FARGATE',
                                                taskDefinition = ecs_client.describe_task_definition(taskDefinition='fargate-task')['taskDefinition']['taskDefinitionArn'],
                                                count = 1,
                                                platformVersion = 'LATEST',
                                                networkConfiguration = {
                                                    'awsvpcConfiguration': {
                                                        'subnets': [
                                                            service_ids['PRIVATE_SUBNET_1'],      # replace with your public subnet or a private subnet (with NAT)
                                                            service_ids['PRIVATE_SUBNET_2']       # Second is optional, but good idea to have two
                                                        ],
                                                        'assignPublicIp': 'DISABLED'
                                                    }
                                                },
                                                overrides = {
                                                    'containerOverrides': [
                                                        {
                                                            'name': 'fargate-task-container',
                                                            'environment': [
                                                                {
                                                                    'name': 'RUNTIME_ARGS',
                                                                    'value': ip_args
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            )
    task_arn = ecs_task_response['tasks'][0]['taskArn']
    print(f"Fargate Task ARN = {task_arn}")
    while True:
        response = ecs_client.describe_tasks(   cluster = f'arn:aws:ecs:us-east-1:{aws_account_id}:cluster/ecs-cluster',
                                                tasks=[task_arn]    )
        status = response['tasks'][0]['containers'][0]['lastStatus']
        print(f'Status: {status}')
        if status == 'STOPPED':
            break
        else:
            time.sleep(30)
    print('AWS Fargate ECS task completed!!!')

    
    # Tearing down the VPC  
    print('Tearing down the VPC... ... ...')
    teardown_vpc(ec2_client, VPC_NAME_TAGS)




# Main
if __name__ == '__main__':
    # The AWS account id
    # Kindly note that the account id has been censored to prevent it disclosure. 
    # Kindly set an appropriate "aws_account_id" value before using these commands.
    aws_account_id = ''

    lambda_handler(  event={"AWS_ACCOUNT_ID": aws_account_id, "RUNTIME_ARGS": {"num": [1,2,3,4], "square": [1,4,9,16], "cube": [1,8,27,64]}}, 
                    context=None    ) 