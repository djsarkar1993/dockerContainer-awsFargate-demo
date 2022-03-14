# Approach to server-less execution of Docker containers on the Amazon cloud
<p>
This repository describes the procedure of running containerized applications on the Amazon cloud in a serverless manner. This will be achieved by erecting a general-purpose solution that can be easily adapted to suit a variety of real-world use-cases. Furthermore, all sensitive information (like access keys, account ids, etc.) used in the solution will be redacted to prevent their discloser.
</p>
<p>
The solution will be built using the AWS (Python) SDK in the AWS US East (N. Virginia) region, and all pricing information will be in-line with the same. The solution will use the following AWS services:
<ul>
<li>Elastic Container Repository (ECR)</li>
<li>Elastic Container Service (ECS)</li>
<li>Fargate</li>
<li>Virtual Private Cloud (VPC)</li>
<li>Identity and Access Management (IAM)</li>
<li>Lambda</li>
</ul>
Furthermore, the solution will also use the Docker desktop application to build a local container image.
</p>
<p>
At a high level, the solution will involve the creation of a simple Python application that accepts inputs at runtime and outputs them as a Pandas data frame. The application will then be containerized and hosted on AWS. Next, a virtual networking environment and a serverless compute engine will be created. The virtual network will manage the security of the compute engine, and the compute engine will provide the infrastructure for executing the containerized application. And finally, a (Python) script will be created to orchestrate the setup, execution & teardown of all the AWS resources used in this solution.
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/djsarkar1993/dockerContainer-awsFargate-demo/main/doc/fig1-HLD.png" width="400">
</p>