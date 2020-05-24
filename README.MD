# PIoT Assignment 02 Car Share Scheme
Car Share Scheme is a website provide user with booking a pecific car on the specific period.

## Team members ##
> Yi Zhang s3602956 <br>
> Shukun Lin s3587391<br>
> Shi Jiayin s3669495<br>
> Zhirui Liang S3554374<br>

## Environment and Deployment ##
`pip3 install passlib`<br>
`pip3 install flask`<br>
`pip3 install mysqlclient`<br>
`pip3 install passlib`<br>
`pip3 install google-api-python-client google-auth-httplib2`<br> 
`google-auth-oauthlib oauth2client httplib2`<br>

## For mac ##
`brew install sphinx-doc`<br>
`export PATH="/usr/local/opt/sphinx-doc/bin:$PATH"`<br>

## Breif Guide ##
### mp: ###
UI website<br>
1. Home Page<br>
2. Register<br>
3. Login<br>
4. Booking -> Choose Specific Day -> Google Account Authentication -> Google Calerdar<br>

### Client server ###
Login by enter password and facial recognition <br>
1. Unlock Car<br>
2. Return Car<br>
3. quit<br>

### ap: ###
Agent server<br>
1. Check Login<br>
2. Set Unlock Car<br>
3. Set Return Car<br>
4. Connecting to Database<br>

## Notice ##
Run mp/server.py in terminal first 
Then open a new termial to manually run client.py
