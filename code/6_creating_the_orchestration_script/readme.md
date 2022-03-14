## Creating the orchestration script
<p>This directory contains the source code of the orchestration script that manages the setup, execution & teardown of all the AWS resources used in this solution. It contains the following files:
<ul>
<li>A script to manage the creation and deletetion of the AWS VPC.</li>
<li>A script to execute the ECS task in one of the subnets of the vpc.</li>
<li>A script to deploy the above two scripts as a Lambda function to AWS.</li>
</ul>
</p>
<hr>
<p>
<b>Orchestration script (lambda function) input:</b><br>
<pre>{
	"AWS_ACCOUNT_ID": {AWS-ACCOUNT-ID}, 
	"RUNTIME_ARGS": {
		"num": [10, 20, 30, 40], 
		"square": [100, 400, 900, 1600], 
		"cube": [1000, 8000, 27000, 64000]
	}
}</pre>
</p>
<hr>
<p>
<b>Orchestration script (lambda function) output:</b><br>
<pre>
START RequestId: ad89213b-472a-4235-a7a8-4fac6b4d566c Version: $LATEST
Setting up the VPC... ... ...
Checking to see if the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP exist
The demo-vpc VPC does not exist.
The demo-pub-snet-1 PUBLIC_SUBNET does not exist.
The demo-pvt-snet-1 PRIVATE_SUBNET_1 does not exist.
The demo-pvt-snet-2 PRIVATE_SUBNET_2 does not exist.
The demo-igw INTERNET_GATEWAY does not exist.
The demo-pub-rtbl PUBLIC_ROUTE_TABLE does not exist.
The demo-eip ELASTIC_IP does not exist.
The demo-natgw NAT_GATEWAY does not exist.
The demo-pvt-rtbl PRIVATE_ROUTE_TABLE does not exist.
Setting up the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP
The demo-vpc VPC has been created! The VPC ID is: vpc-00fb6171013570b98
The demo-pub-snet-1 Subnet has been created! The Subnet ID is: subnet-0b29642b47774951f
The demo-pvt-snet-1 Subnet has been created! The Subnet ID is: subnet-04cb22ddef65874b7
The demo-pvt-snet-2 Subnet has been created! The Subnet ID is: subnet-0945d69c87df8faf7
The demo-igw Internet Gateway has been created! The Internet Gateway ID is: igw-0fd62cb4f2734d74b
The demo-pub-rtbl public Route Table has been created! The Route Table ID is: rtb-01f358cc523cb1e83
The demo-eip Elastic IP has been created! The Allocation ID is: eipalloc-0373580aef171daec
Waiting for the NAT gateway to start...
Waiting for the NAT gateway to start...
The demo-natgw NAT Gateway has been created! The NAT Gateway ID is: nat-02a513bd5eb75e5a8
The demo-pvt-rtbl private Route Table has been created! The Route Table ID is: rtb-078b0008828e7e5c1
Running the containerized user application as a Fargate task on the ECS cluster... ... ...
Input Arguments: {"num": [1, 2, 3, 4], "square": [1, 4, 9, 16], "cube": [1, 8, 27, 64]}
Fargate Task ARN = arn:aws:ecs:us-east-1:{AWS-ACCOUNT-ID}:task/ecs-cluster/e4fd4bf000f240bda3c0ec6f28fa0696
Status: PENDING
Status: PENDING
Status: RUNNING
Status: STOPPED
AWS Fargate ECS task completed!!!
Tearing down the VPC... ... ...
Checking to see if the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP exist
The demo-vpc VPC exists.
The demo-pub-snet-1 PUBLIC_SUBNET exists.
The demo-pvt-snet-1 PRIVATE_SUBNET_1 exists.
The demo-pvt-snet-2 PRIVATE_SUBNET_2 exists.
The demo-igw INTERNET_GATEWAY exists.
The demo-pub-rtbl PUBLIC_ROUTE_TABLE exists.
The demo-eip ELASTIC_IP exists.
The demo-natgw NAT_GATEWAY exists.
The demo-pvt-rtbl PRIVATE_ROUTE_TABLE exists.
Deleting the NAT gateway...
The demo-natgw NAT Gateway (id: nat-0cf8e35b2ef7770d3) has been deleted
The demo-eip Elastic IP (id: eipalloc-0c75c6223463f3001) has been deleted
The demo-pub-snet-1 PUBLIC_SUBNET (id: subnet-018add387582e71cf) has been deleted
The demo-pvt-snet-1 PRIVATE_SUBNET_1 (id: subnet-068c468f477c700ea) has been deleted
The demo-pvt-snet-2 PRIVATE_SUBNET_2 (id: subnet-07202021bc797fa1d) has been deleted
The demo-pub-rtbl PUBLIC_ROUTE_TABLE (id: rtb-00fd2d21f0b42e0d2) has been deleted
The demo-pvt-rtbl PRIVATE_ROUTE_TABLE (id: rtb-040f2a94f49a0574d) has been deleted
The demo-igw Internet Gateway (id: igw-078d9370507a14edb) has been deleted
The demo-vpc VPC (id: vpc-07687d81d2d36d577) has been deleted
END RequestId: a945b939-0714-4327-9973-a9d0c985b7af
REPORT RequestId: a945b939-0714-4327-9973-a9d0c985b7af
Duration: 341965.22 ms
Billed Duration: 341966 ms
Memory Size: 128 MB
Max Memory Used: 81 MB
</pre>
</p>
<hr>
<p>
<b>AWS Fargate ECS Task output:</b><br>
<pre>
message
2022-03-14 09:45:32 INFO user-app: Logger setup successful!
2022-03-14 09:45:32 INFO user-app: The input arguments are: {'num': [10, 20, 30, 40], 'square': [100, 400, 900, 1600], 'cube': [1000, 8000, 27000, 64000]}
2022-03-14 09:45:32 INFO user-app: Waiting for 30 seconds... ... ...
2022-03-14 09:46:02 INFO user-app: Displaying the contents of the runtime arguments as a pandas dataframe:
   num  square   cube
0   10     100   1000
1   20     400   8000
2   30     900  27000
3   40    1600  64000
</pre>
</p>
<hr>
<p>
<i>Note: In the above script the AWS account id has been censored to prevent it disclosure. Kindly set an appropriate "aws_account_id" value before using this script._</i>
</p>