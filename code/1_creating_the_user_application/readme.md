## Creating the user application
<p>This directory contains the source code of a simple Python application that accepts inputs from the OS environment variables. It then displays the inputs as a Pandas data frame after 30 seconds.</p>
<hr>
<p>
<b>Input:</b><br>
<pre> 
$ export RUNTIME_ARGS="{\"num\": [1,2,3,4], \"square\": [1,4,9,16], \"cube\": [1,8,27,64]}"
$ python3 user_app.py
</pre>
</p>
<hr>
<p>
<b>Output:</b><br>
<pre>
2022-03-13 08:57:59 INFO user-app: Logger setup successful!
2022-03-13 08:57:59 INFO user-app: The input arguments are: {'num': [1, 2, 3, 4], 'square': [1, 4, 9, 16], 'cube': [1, 8, 27, 64]}
2022-03-13 08:57:59 INFO user-app: Waiting for 30 seconds... ... ...
2022-03-13 08:58:29 INFO user-app: Displaying the contents of the runtime arguments as a pandas dataframe:
|   | num | square | cube |
|---|-----|--------|------|
| 0 | 1   | 1      | 1    |
| 1 | 2   | 4      | 8    |
| 2 | 3   | 9      | 27   |
| 3 | 4   | 16     | 64   |
</pre>
</p>
