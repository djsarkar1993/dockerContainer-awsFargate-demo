## Creating the ECS task
<p>This directory contains the source code for creating the compute engine where the containerized application will run. It contains the following files:
<ul>
<li>
A script that creates:
<ul>
<li>An ECS cluster which provides the infrastructure for our containers to run.</li>
<li>An AWS Fargate task for the ECS cluster, which will run our container application (hosted on ECR)</li>
</ul>
</li>
</ul>
</p>