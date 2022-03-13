# Imports
import boto3




# Main
if __name__ == '__main__':
    # Repository Name
    repo_name = 'user-app-repo'


    # AWS SDK client that allows us to interact with the Amazon Elastic Container Registry service
    ecr_client = boto3.client('ecr')


    # Checking to see it the repository exist
    repo_exists = None
    try:
        ecr_client.describe_repositories(repositoryNames=[repo_name])
        repo_exists = True
    except:
        repo_exists = False
    

    # Deleting the repository if it exists
    if repo_exists:
        print(f'An instance of the "{repo_name}" repository was found. Deleting the previous instance!')
        ecr_client.delete_repository(   repositoryName = repo_name, 
                                        force = True    )


    # Creating a new repository
    print(f'Creating the "{repo_name}" repository... ... ...')
    repo_create_response = ecr_client.create_repository(repositoryName = repo_name)
    repo_arn = repo_create_response['repository']['repositoryArn']
    print(f'Repository ARN = {repo_arn}')
