<h1>Lannister</h1>

<h2 style="margin-bottom: 0">Requirements</h2>
<hr style="margin-top: 0"/>
<dl>
  <li>Docker >= 20.10.10</li>
  <li>Node >= 14.16.0</li>
  <li>Serverless Framework >= 3.20.0</li>
  <li>dotenv-expand >= 8.0.3</li>
  <li>serverless-iam-roles-per-function >= 3.2.0</li>
</dl>
<h2 style="margin-bottom: 0">Deployment</h2>
<hr style="margin-top: 0"/>
Before launching application, you need to execute the following commands.<br/>
1. Before work you need to confire AWS credentials. Find file named <code>credentials</code>, in a folder 
named <code>.aws</code> in your home directory and add to the end of the file following lines:
<pre>
<code>[commonAccount]
aws_access_key_id=********************
aws_secret_access_key=****************************************</code>
</pre>
2. To deploy changes in project's root directory run following command:
<pre>
<code>serverless deploy</code>
</pre>
