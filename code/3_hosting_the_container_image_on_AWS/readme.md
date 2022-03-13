## Hosting the container image on AWS
<p>This directory contains the source code for hosting the container image of the Python application on AWS. It contains the following files:
<ul>
<li>A script to create a repository in the Amazon Elastic Container Registry (ECR) service.</li>
</ul>
</p>
<hr>
<p>
<b>Push commands:</b><br>
<ol>
<li>
Run the below command to authenticate the Docker client with the ECR repository:
<pre>aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {AWS-ACCOUNT-ID}.dkr.ecr.us-east-1.amazonaws.com</pre>
</li>
<li>
Run the below command to tag the image:
<pre>docker tag user-app-container-image:latest {AWS-ACCOUNT-ID}.dkr.ecr.us-east-1.amazonaws.com/user-app-repo:latest</pre>
</li>
<li>
Run the below command to push the image to the ECR repository:
<pre>docker push {AWS-ACCOUNT-ID}.dkr.ecr.us-east-1.amazonaws.com/user-app-repo:latest</pre>
</li>
</ol>
<br>
<i>Note: In the above commands the actual AWS account id was censored to prevent it disclosure. Kindly replace the "{AWS-ACCOUNT-ID}" keyword with an appropriate value before using these commands.</i>
</p>

