# PIoT Assignment 03 Car Share Scheme
Car Share Scheme is a website provide user with booking a pecific car on the specific period. In this step, User can view the history of booked car and avaiable car, they also can search the car book it and cancle the booking. Admin system provide the power to view car rental history, search users and cars and edit the information of them, they also can report the car issues to the engineer for asking for supporting. For Manager, there is a dashboard page for them to login and manage the business status. The Engineers should show their QR code to verify their identity and unlock the broken cars in GoogleMap by Bluetooth. This application will be continuously updated and developed in the future.

## Team members 
> Yi Zhang s3602956 <br>
> Shukun Lin s3587391<br>
> Shi Jiayin s3669495<br>
> Zhirui Liang S3554374<br>

## Username and password of 3 types of user 
> Username:__admin__ Password: ***abc123***<br>
> Username:__manager__ Password: ***abc123***<br>
> Username:__engineer__ Password: ***abc123***<br>

#### Report your repository usage in GitHub by attaching some screen shots in README.md
![image1](/screenshots/2.png)
For more please go to screenshots for check as images are too large !

#### Report your Trello board usage by attaching some screen shots in README.md

![image5](/screenshots/5.png)

#### Well organised file structure and also separate website and API code into two folders

#### Make surehaving one main method to run in main.py
> Run command __`python main.py`__

## Environment and Deployment 
`pip3 install passlib`<br>
`pip3 install flask`<br>
`pip3 install mysqlclient`<br>
`pip3 install passlib`<br>
`pip3 install google-api-python-client google-auth-httplib2`<br> 
`google-auth-oauthlib oauth2client httplib2`<br>
`pip3 install pushbullet.py`<br>
`sudo apt-get install libbluetooth-dev`<br>
`sudo pip3 install pybluez`<br>
`pip3 install qrcode pillow image zxing`<br>
`pip3 install SpeechRecognition`<br>
`sudo apt-get install portaudio19-dev python-all-dev python3-all-dev`<br>
`pip3 install pyaudio`<br>
`pip3 install google-api-python-client`<br>
`sudo apt-get install flac`<br>

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

## A3 Features
### MP:
web-based system<br>
1. Login Option
#### Admin
1. View the list of car rental history
2. Search and view users and car by properties
3. Edit information of car and user
4. Report cars with issues
5. Search the car by GoogleSpeech
#### Manager
1. View the number of users living in each area
2. View the user location
3. View the Frequent Booked Cars
4. View Most Profitable Car
#### Engineer
1. View the location of the broken car in Google Map
2. View the circle of the city


### AP:
object-detection console-based system<br>
1. Verify identity by QR code
2. Unlock the car by implementing an automatic identification system by Bluetooth



## Notice ##
Run mp/server.py in terminal first 
Then open a new termial to manually run client.py
