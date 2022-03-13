## Containerizing the user application
<p>This directory contains the source code for containerize the Python application using Docker. It contains the following files:
<ul>
<li>A requirements file containing the dependencies of the Python application.</li>
<li>A Docker file containing the commands required to assemble the container image.</li>
</ul>
</p>
<hr>
<p>
<b>Docker build command:</b><br>
<pre>
$ cd ..
$ docker build -f 2_containerizing_the_user_application/Dockerfile -t user-app-container-image:latest .
</pre>