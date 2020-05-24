# PIoT Assignment 02 Car Share Scheme
Car Share Scheme is a website provide user with booking a pecific car on the specific period.
## Environment and Deployment ##
pip3 install passlib
pip3 install flask
pip3 install mysqlclient
pip3 install passlib
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
#For mac 
#brew install sphinx-doc
#export PATH="/usr/local/opt/sphinx-doc/bin:$PATH"
## Breif Guide ##
mp:
UI website
client server
ap:
agent server
## Notice ##
run agent server in terminal then open a new termial to manually run client server.
## Code Structure ##
Folder PATH listing for volume Lenovo
Volume serial number is 1E1C-FB3C
D:.
�   .DS_Store
�   client_secret.json
�   list.txt
�   README.MD
�   test.py
�   test1.py
�   token.json
�   
����.idea
�   �   .gitignore
�   �   carshare.iml
�   �   misc.xml
�   �   modules.xml
�   �   vcs.xml
�   �   
�   ����inspectionProfiles
�           profiles_settings.xml
�           Project_Default.xml
�           
����.vscode
�       settings.json
�       
����ap
�   �   client.py
�   �   testAP.py
�   �   
�   ����__pycache__
�           client.cpython-38.pyc
�           
����doc
�   �   .DS_Store
�   �   make.bat
�   �   Makefile
�   �   
�   ����build
�   �   �   .DS_Store
�   �   �   
�   �   ����doctrees
�   �   �   �   environment.pickle
�   �   �   �   index.doctree
�   �   �   �   
�   �   �   ����ap
�   �   �   �       client.doctree
�   �   �   �       modules.doctree
�   �   �   �       
�   �   �   ����mp
�   �   �           add_event.doctree
�   �   �           database.doctree
�   �   �           main.doctree
�   �   �           menu.doctree
�   �   �           modules.doctree
�   �   �           server.doctree
�   �   �           
�   �   ����html
�   �       �   .buildinfo
�   �       �   .DS_Store
�   �       �   genindex.html
�   �       �   index.html
�   �       �   objects.inv
�   �       �   py-modindex.html
�   �       �   search.html
�   �       �   searchindex.js
�   �       �   
�   �       ����ap
�   �       �       client.html
�   �       �       modules.html
�   �       �       
�   �       ����mp
�   �       �       add_event.html
�   �       �       database.html
�   �       �       main.html
�   �       �       menu.html
�   �       �       modules.html
�   �       �       server.html
�   �       �       
�   �       ����_sources
�   �       �   �   index.rst.txt
�   �       �   �   
�   �       �   ����ap
�   �       �   �       client.rst.txt
�   �       �   �       modules.rst.txt
�   �       �   �       
�   �       �   ����mp
�   �       �           add_event.rst.txt
�   �       �           database.rst.txt
�   �       �           main.rst.txt
�   �       �           menu.rst.txt
�   �       �           modules.rst.txt
�   �       �           server.rst.txt
�   �       �           
�   �       ����_static
�   �               alabaster.css
�   �               basic.css
�   �               custom.css
�   �               doctools.js
�   �               documentation_options.js
�   �               file.png
�   �               jquery-3.4.1.js
�   �               jquery.js
�   �               language_data.js
�   �               minus.png
�   �               plus.png
�   �               pygments.css
�   �               searchtools.js
�   �               underscore-1.3.1.js
�   �               underscore.js
�   �               
�   ����source
�       �   .DS_Store
�       �   conf.py
�       �   index.rst
�       �   
�       ����ap
�       �       client.rst
�       �       modules.rst
�       �       
�       ����mp
�       �       add_event.rst
�       �       database.rst
�       �       main.rst
�       �       menu.rst
�       �       modules.rst
�       �       server.rst
�       �       
�       ����_templates
�               modules.rst
�               test.rst
�               
����mp
    �   add_event.py
    �   client_secret.json
    �   credentials.json
    �   database.py
    �   iotA2.sql
    �   main.py
    �   menu.py
    �   requirements.txt
    �   server.py
    �   testDb_Booking.py
    �   testDB_Car.py
    �   testDB_User.py
    �   testMP.py
    �   token.json
    �   __init__.py
    �   
    ����static
    �   ����css
    �   �       font.css
    �   �       searchicon.jpg
    �   �       
    �   ����image
    �   �       cars.jpg
    �   �       Cars_2006.jpg
    �   �       favicon.ico
    �   �       logo.png
    �   �       
    �   ����js
    �           app.js
    �           
    ����templates
    �       book.html
    �       cars.html
    �       home.html
    �       loggedin.html
    �       login.html
    �       loginURL.html
    �       myProfile.html
    �       register.html
    �       template.html
    �       testURL.html
    �       
    ����__pycache__
            add_event.cpython-38.pyc
            database.cpython-37.pyc
            database.cpython-38.pyc
            main.cpython-38.pyc
            menu.cpython-38.pyc
            server.cpython-38.pyc
            testDB_Booking.cpython-38.pyc
            testDB_Car.cpython-38.pyc
            testDB_User.cpython-38.pyc
            testMP.cpython-38.pyc
            __init__.cpython-38.pyc
            
## Team members ##
Yi Zhang s3602956 <br>
Shukun Lin s3587391<br>
Shi Jiayin s3669495<br>
Zhirui Liang S3554374<br>