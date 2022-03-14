# Imports
import boto3




# Main
if __name__ == '__main__':
    # AWS SDK client that allows us to interact with the AWS IAM service
    iam_client = boto3.client('iam')


    # Creating the IAM role for the AWS ECS task.
    # This role will allows our ECS TASK to call other AWS services on our behalf.
    # But since in this example our containerized Python application is not using any AWS services, we will just create this role and not attach any policy to it.
    role_name = 'ecs-basic-exec-role'
    ecr_task_role_response = iam_client.create_role(    Path='/',
                                                        RoleName=role_name,
                                                        AssumeRolePolicyDocument="""{
                                                            "Version": "2012-10-17", 
                                                            "Statement": [
                                                                {
                                                                    "Sid": "", 
                                                                    "Effect": "Allow", 
                                                                    "Principal": {
                                                                        "Service": "ecs-tasks.amazonaws.com"
                                                                    }, 
                                                                    "Action": "sts:AssumeRole"
                                                                }
                                                            ]
                                                        }""",
                                                        Description='Allows ECS tasks to call AWS services on your behalf.',
                                                        MaxSessionDuration=3600 )
    ecr_task_role_arn = ecr_task_role_response['Role']['Arn']
    print(f'ECS Task Role ARN: {ecr_task_role_arn}')


    # Creating an IAM role for the orchestration script.
    # This role will allow our orchestration script to setup & teardown the virtual network and to launch ECS task
    role_name = 'lambda-basic-exec-role'
    lambda_role_response = iam_client.create_role(    Path='/',
                                                        RoleName=role_name,
                                                        AssumeRolePolicyDocument="""{
                                                            "Version": "2012-10-17", 
                                                            "Statement": [
                                                                {
                                                                    "Effect": "Allow", 
                                                                    "Principal": {
                                                                        "Service": "lambda.amazonaws.com"
                                                                    }, 
                                                                    "Action": "sts:AssumeRole"
                                                                }
                                                            ]
                                                        }""",
                                                        Description='Allows Lambda functions to call AWS services on your behalf.',
                                                        MaxSessionDuration=3600 )
    lambda_role_arn = lambda_role_response['Role']['Arn']
    print(f'Orchestration (Lambda) Script Role ARN: {lambda_role_arn}')


    # Attaching an inline policy to the orchestration script.
    policy_name = 'lambda-basic-exec-role-policy'
    with open('lambda-basic-exec-role-policy.json') as pf:
        policy_doc = pf.read()
    lambda_role_policy_response = iam_client.create_policy( PolicyName=policy_name,
                                                            PolicyDocument=policy_doc   )
    lambda_role_policy_arn = lambda_role_policy_response['Policy']['Arn']
    iam_client.attach_role_policy(  RoleName=role_name,
                                    PolicyArn=lambda_role_policy_arn  )
    print(f'Orchestration (Lambda) Script Policy ARN: {lambda_role_policy_arn}')
