# PIoT Assignment 02 Car Share Scheme
Car Share Scheme is a website provide user with booking a pecific car on the specific period.

## Team members 
> Yi Zhang s3602956 <br>
> Shukun Lin s3587391<br>
> Shi Jiayin s3669495<br>
> Zhirui Liang S3554374<br>

## Environment and Deployment 
`pip3 install passlib`<br>
`pip3 install flask`<br>
`pip3 install mysqlclient`<br>
`pip3 install passlib`<br>
`pip3 install google-api-python-client google-auth-httplib2`<br> 
`google-auth-oauthlib oauth2client httplib2`<br>

# To run all unit tests in command line
`python -m unittest discover`<br>

## For mac 
`brew install sphinx-doc`<br>
`export PATH="/usr/local/opt/sphinx-doc/bin:$PATH"`<br>

## Breif Guide
### Master Pi (MP): 
UI website<br>
1. Home Page<br>
2. Register<br>
3. Login<br>
4. Booking -> Choose Specific Day -> Google Account Authentication -> Google Calerdar<br>

### MP server
Stand as a server listening on port 61180
1. Check login request from AP<br>
2. Check virtual Car ID from AP<br>
3. Check booking status for this Car within correct Date<br>
4. Reply to AP with relevant information in dict format<br>

### Agent Pi (AP): ###
Agent client<br>
1. Console based Login<br>
2. Unlock Car<br>
3. Return Car<br>
4. Facial recognition Login<br>

## Notice ##
Run mp/server.py in terminal first 
Then open a new termial to manually run client.py
