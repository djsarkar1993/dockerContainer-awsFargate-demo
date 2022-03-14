# Imports
import boto3




# Functions
# This function creates & registers an ECS Task Definitions
def create_ecs_task_definition(ecs_client, cwLogs_client, task_definition_name, **configs):
    response = ecs_client.register_task_definition(
        family=task_definition_name,
        taskRoleArn=configs['task_definition_task_role_arn'],
        executionRoleArn=configs['task_definition_execution_role_arn'],
        networkMode=configs['task_definition_network_mode'],
        containerDefinitions=[{
            'name': configs['container_name'],
            'image': configs['container_image'],
            'essential': True,
            'logConfiguration': {
                'logDriver': configs['container_logDriver'],
                'options': {'awslogs-group': f"/ecs/{task_definition_name}", 'awslogs-region': 'us-east-1', 'awslogs-stream-prefix': 'ecs'}
            },
        }],
        requiresCompatibilities=['FARGATE'],
        cpu=str(configs['task_definition_cpu']),
        memory=str(configs['task_definition_memory'])
    )
    #print(f'ECS Register Task Response = {response}')
    result = response['taskDefinition']['taskDefinitionArn']

    log_group_name = f"/ecs/{task_definition_name}"
    response = cwLogs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
    #print(f'Describe Log Group Response = {response}')
    if len(response['logGroups']) == 0:
        response = cwLogs_client.create_log_group(
            logGroupName=log_group_name
        )
        #print(f'Create Log Group Response = {response}')
    
    return result




# Main
if __name__ == '__main__':
    # The AWS account id
    # Kindly note that the account id has been censored to prevent it disclosure. 
    # Kindly set an appropriate "aws_account_id" value before using these commands.
    aws_account_id = ''


    # AWS SDK client that allows us to interact with the AWS ECS service
    ecs_client = boto3.client('ecs')


    # AWS SDK client that allows us to interact with the AWS CloudWatch Logs service
    cwLogs_client = boto3.client('logs')


    # Creating an ECS cluster
    # ECS clusters provide the infrastructure on which container applications are run
    ecs_cluster_name = 'ecs-cluster'
    ecs_cluster_response = ecs_client.create_cluster(   clusterName=ecs_cluster_name,
                                                        capacityProviders=['FARGATE', 'FARGATE_SPOT'],
                                                        settings=[
                                                            {
                                                                'name': 'containerInsights',
                                                                'value': 'enabled'
                                                            }
                                                        ]
                                                    )
    ecs_cluster_arn = ecs_cluster_response['cluster']['clusterArn']
    print(f'ECS cluster ARN = {ecs_cluster_arn}')


    # Creating an AWS Fargate ECS task
    # AWS Fargate is a serverless compute engine that can be used with AWS ECS to run containers without having to manage servers or clusters of Amazon EC2 instances. 
    # With Fargate, we no longer have to provision, configure, or scale clusters of virtual machines to run containers.
    fargate_configs = {
        'task_definition_name': 'fargate-task',
        'task_definition_task_role_arn': f'arn:aws:iam::{aws_account_id}:role/ecs-basic-exec-role',
        'task_definition_execution_role_arn': f'arn:aws:iam::{aws_account_id}:role/ecsTaskExecutionRole',
        'task_definition_network_mode': 'awsvpc',
        'container_name': 'fargate-task-container',
        'container_image': f'{aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/user-app-repo:latest',
        'container_logDriver': 'awslogs',
        'task_definition_cpu': '256',
        'task_definition_memory': '512'
    }
    fargate_task_arn = create_ecs_task_definition(ecs_client, cwLogs_client, **fargate_configs)
    print(f'Fargate task ARN = {fargate_task_arn}')
