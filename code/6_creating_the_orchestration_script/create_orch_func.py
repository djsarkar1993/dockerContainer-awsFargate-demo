# Imports
import boto3
import shutil




# Main
if __name__ == '__main__':
    # The AWS account id
    # Kindly note that the account id has been censored to prevent it disclosure. 
    # Kindly set an appropriate "aws_account_id" value before using these commands.
    aws_account_id = ''

    # AWS SDK client that allows us to interact with AWS Lambda
    lambda_client = boto3.client('lambda')

    # Function name
    func_name = 'run_app_container'

    # Archiving the the orchestration script
    shutil.make_archive(func_name, 'zip', func_name)
    with open(f'{func_name}.zip', 'rb') as zf:
        code_binary = zf.read()
    
    # Creating a lambda function which will run the orchestration script
    lambda_func_response = lambda_client.create_function(   FunctionName = func_name,
                                                            Runtime = 'python3.9',
                                                            Role = f'arn:aws:iam::{aws_account_id}:role/lambda-basic-exec-role',
                                                            Handler = 'main.lambda_handler',
                                                            Code = {'ZipFile': code_binary},
                                                            Timeout = 900,
                                                            PackageType = 'Zip',
                                                            Architectures = ['arm64']
                                                        )
    lambda_arn = lambda_func_response['FunctionArn']
    print(f'Lambda ARN = {lambda_arn}')