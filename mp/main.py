from flask import Flask, render_template, request,url_for, redirect, session, flash
from werkzeug.utils import secure_filename
from database import DatabaseUtils
from passlib.hash import sha256_crypt
from datetime import datetime
from add_event import Calendar
from time import sleep

# Remove comment if your pushbullet is working
# from pushbullet import Pushbullet
import random
import requests
import json
import os
import cv2 

UPLOAD_FOLDER = 'mp/static/image'

app = Flask(__name__)
app.secret_key = 'asdasd12easd123rdada'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pushbullet API Token
ACCESS_TOKEN="o.DmzF65qvLy7Tbptcl0blbsRVQdWdOc0O"
# Remove this comment to use pushbullet library api instead
# pb = Pushbullet(ACCESS_TOKEN)

@app.route("/")
def home():
    """

    return to home.html

    """
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """

    Register function

    """
    if request.method == 'POST':
        #Data collected from register form
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']

        with DatabaseUtils() as db:
            if(db.checkUsername(username)):
                if(db.insertPerson(username, sha256_crypt.hash(password), firstname, lastname, phone, email, address, city)):
                    print("{} inserted successfully.".format(username))
                    flash("Thank you for registering {}".format(firstname))
                    return redirect(url_for("home"))
                else:
                    print("{} failed to be inserted.".format(username))
                    flash("{} failed to be inserted.".format(username))
                    return redirect(url_for("register"))
            else:
                print("{} already exist, try a different one.".format(username))
                flash("{} already exist, try a different one.".format(username))
                return redirect(url_for("register"))
    
    return render_template("register.html")

@app.route("/login",  methods=['GET', 'POST'])
def login():
    """

    Login function

    """
    #If session username exist, means already logged in
    if session.get('username') != None:
        return redirect(url_for('myprofile'))
    elif request.method == 'POST':
        #clear session username, then assign new value for later use
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        with DatabaseUtils() as db:
            if(db.checkUsername(username) == False):
                if(db.checkPerson(username, password)):
                    session['username'] = request.form['username']
                    session['userid'] = db.getPerson(username)[0]
                    #person = db.getPerson(username)
                    return redirect(url_for("myprofile"))
                else:
                    print("{} 's Password is wrong.".format(username))
                    flash("{} 's Password is wrong.".format(username))
                    return redirect(url_for("login"))

    return render_template("login.html")

#after login, redirect to myprofile page
@app.route("/myprofile", methods=['GET', 'POST'])
def myprofile():
    """

    Read database for login

    """
    if session.get('username') != None:
        with DatabaseUtils() as db:
            person = db.getPerson(session.get('username'))
            booking = db.showBooking(person[0])
            history = db.showHistory(person[0])
        return render_template("myProfile.html", person = person, booking = booking, history=history)
    else:
        return login()

# Upload image and encode it to database
@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    """

    Upload images to mp and encoded it into database

    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Images get stored in static/image/
            file.save(os.path.join('mp/static/image', filename))
            #Image file get enconded and sent to database
            img = cv2.imread('mp/static/image/' + filename,1)
            with DatabaseUtils() as db:
                db.insertImg(session.get('userid'), img)

    return redirect(url_for("myprofile"))

@app.context_processor
def utility_processor():
    """

    For booking

    """
    def car(bookingid):
        with DatabaseUtils() as db:
            car = db.getCar(bookingid)
            return car[1] + "-" + car[2]
    return dict(car=car)


@app.route("/logout")
def logout():
    """

    Logout an account

    """
    session.pop('username', None)
    session.pop('userid', None)
    session.pop('admin', None)
    session.pop('manager', None)
    session.pop('engineer', None)
    session.clear()
    flash("You have logged out!")
    return home()

@app.route("/cars", methods=['GET', 'POST'])
def cars():
    """

    Read available car for db

    """
    with DatabaseUtils() as db:
        cars = db.getAvailCar()

    return render_template("cars.html", **locals())

@app.route("/book", methods=['POST'])
def book():
    """

    Booking function and store data to db

    """
    if request.method == "POST":
        carid = request.form['carid']
        make = request.form['make']
        model = request.form['model']
        Type = request.form['type']
        seats = request.form['seats']
        color = request.form['color']
        location = request.form['location']
        price = request.form['price']
        return render_template("book.html", **locals())

    return render_template("book.html", **locals())

#Need to add more rules: Google calendar & check car's availability
@app.route("/processbook", methods=['POST'])
def processbook():
    """

    Function for process booking

    """
    if request.method == "POST":
        userid = request.form['userid']
        carid = request.form['carid']
        cost = request.form['price']
        startDate =  datetime.strptime(request.form['startDate'], '%Y-%m-%d').date()
        endDate = datetime.strptime(request.form['endDate'], '%Y-%m-%d').date()
        #For updating car's availability after booking
        avail = "False"
        #Check if input date is valid
        if(endDate < startDate):
            print("Error, minimum booking is 1 day")
            flash("Error, minimum booking is 1 day")
            return redirect(url_for("book"), code = 307)
        else:
            cal = Calendar()
            with DatabaseUtils() as db:
                #Check car availability
                if(db.checkCarAvail(carid)):
                    person = db.getPerson(session.get('username'))
                    carinfo = db.getCar(carid)
                    user = "{} {}".format(person[3], person[4])
                    car = "{} {}, {} Seats".format(carinfo[1], carinfo[2], carinfo[4])
                    location = carinfo[6]
                    status, eventID = cal.insert(car, location, user, startDate, endDate)
                    #Check if booking is confirmed for Google Calendar
                    if(status == "confirmed"):
                        #Check if booking record is inserted
                        if(db.insertBooking(userid, carid, int(cost), startDate, endDate, eventID)):
                            #If it is inserted, update car availability
                            if(db.updateCarAvail(carid, avail)):
                                print("Car ID: {} is booked from {} till {}".format(carid, startDate, endDate))
                                flash("Car ID: {} is booked from {} till {}".format(carid, startDate, endDate))
                                return redirect(url_for("home"))
                        else:
                            print("Error, booking failed, try again later.")
                            flash("Error, booking failed, try again later.")
                            return redirect(url_for("home"))
                    else:
                        print("Error, Google Calendar request is canceled, try again later.")
                        flash("Error, Google Calendar request is canceled, try again later.")
                        return redirect(url_for("book"), code = 307)
                else:
                    print("Error, Car ID: {} is not available, try a different car later".format(carid))
                    flash("Error, Car ID: {} is not available, try a different car later".format(carid))
                    return redirect(url_for("home"))

@app.route("/cancelbook", methods=['POST'])
def cancelbook():
    """

    Function for cancel booking

    """
    if request.method == "POST":
        carid = request.form['carid']
        bookid = request.form['bookid']
        avail = "True"
        with DatabaseUtils() as db:
            cal = Calendar()
            eventID = db.getBooking(bookid)[8]
            if(cal.delete(eventID)):
                if(db.cancelBooking(bookid) and db.updateCarAvail(carid, avail)):
                    print("Booking ID: {} is successfully canceled".format(bookid))
                    flash("Booking ID: {} is successfully canceled".format(bookid))
                else:
                    print("Error, please try cancel it again later.")
                    flash("Error, please try cancel it again later.")
            else:
                print("Error, Please use your primary google account.")
                flash("Error, Please use your primary google account.")
    return redirect(url_for("myprofile"))

########################### A3 Part ####################################

# Register for 3 type of admins, DISABLED!
# @app.route("/registerA", methods=['GET', 'POST'])
# def registerA():
#     if request.method == 'POST':
#         #Data collected from register form
#         username = request.form['username']
#         password = request.form['password']
#         firstname = request.form['firstname']
#         lastname = request.form['lastname']
#         phone = request.form['phone']
#         email = request.form['email']
#         address = request.form['address']
#         usertype = request.form['type']

#         with DatabaseUtils() as db:
#             if(usertype == "admin"):
#                 if(db.insertAdmin(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
#                     print("{} inserted successfully.".format(username))
#                     flash("Thank you for registering {}".format(firstname))
#                     return redirect(url_for("home"))
#                 else:
#                     print("{} failed to be inserted.".format(username))
#                     flash("{} failed to be inserted.".format(username))
#                     return redirect(url_for("registerA"))
#             elif(usertype == "manager"):
#                 if(db.insertManager(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
#                     print("{} inserted successfully.".format(username))
#                     flash("Thank you for registering {}".format(firstname))
#                     return redirect(url_for("home"))
#                 else:
#                     print("{} failed to be inserted.".format(username))
#                     flash("{} failed to be inserted.".format(username))
#                     return redirect(url_for("registerA"))
#             elif(usertype == "engineer"):
#                 if(db.insertEngineer(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
#                     print("{} inserted successfully.".format(username))
#                     flash("Thank you for registering {}".format(firstname))
#                     return redirect(url_for("home"))
#                 else:
#                     print("{} failed to be inserted.".format(username))
#                     flash("{} failed to be inserted.".format(username))
#                     return redirect(url_for("registerA"))
#             else:
#                 print("{} failed to be inserted.".format(username))
#                 flash("{} failed to be inserted.".format(username))
#                 return redirect(url_for("registerA"))
    
#     return render_template("registerA.html")

# Selection login system
@app.route("/askLogin", methods=['GET', 'POST'])
def askLogin():
    """

    Selection login system

    """
    if request.method == 'POST':
        usertype = request.form['user']
        if usertype == 'admin':
            print("Admin")
            return redirect(url_for('loginAdmins', usertype='Admin'))
        elif usertype == 'manager':
            print("Manager")
            return redirect(url_for('loginAdmins', usertype='Manager'))
        elif usertype == 'engineer':
            print("Engineer")
            return redirect(url_for('loginAdmins', usertype='Engineer'))

    return render_template("askLogin.html")

# 3 type of admins login
@app.route("/loginAdmins/<usertype>", methods=['GET', 'POST'])
def loginAdmins(usertype):
    """

    3 type of admins login
    :param usertype: string
    :return: string
    """
    return render_template("loginAdmins.html", **locals())

# 3 type of admins login
@app.route("/processLoginAdmins", methods=['GET','POST'])
def processLoginAdmins():
    """

    # 3 type of admins login

    """
    if request.method == 'POST':
        check = request.form['filter']
        username = request.form['username']
        password = request.form['password']
        # print(request.form)
        if check == 'Admin':
            with DatabaseUtils() as db:
                if(db.checkAdmin(username, password)):
                    session['admin'] = request.form['username']
                    print("Passed")
                    return redirect(url_for("showAllBookings"))
                else:
                    print("{}'s Password is wrong.".format(username))
                    flash("{}'s Password is wrong.".format(username))
                    return redirect(url_for("askLogin"))
        elif check == 'Manager':
            with DatabaseUtils() as db:
                if(db.checkManager(username, password)):
                    session['manager'] = request.form['username']
                    print("Passed")
                    return redirect(url_for("managerBoard1"))
                else:
                    print("{}'s Password is wrong.".format(username))
                    flash("{}'s Password is wrong.".format(username))
                    return redirect(url_for("askLogin"))
        elif check == 'Engineer':
            with DatabaseUtils() as db:
                if(db.checkEngineer(username, password)):
                    session['engineer'] = request.form['username']
                    print("Passed")
                    return redirect(url_for("engineer1"))
                else:
                    print("{}'s Password is wrong.".format(username))
                    flash("{}'s Password is wrong.".format(username))
                    return redirect(url_for("askLogin"))
    else:
        print("false")
    
    return render_template("admin.html")

# Get car rental history 
@app.route("/showAllBookings", methods=['GET','POST'])
def showAllBookings():
    """

    Get car rental history

    """
    #If session admin doesn't exist, redirect
    if session.get('admin') != None:
        with DatabaseUtils() as db:
            booking = db.getAllBookings()
            return render_template("bookings.html", booking = booking)
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))

# Get car rental history
@app.route("/showAllUsers", methods=['GET','POST'])
def showAllUsers():
    """

    Get car rental history

    """
    if session.get('admin') != None:
        with DatabaseUtils() as db:
            users = db.getAllUsers()
            return render_template("users.html", users = users)
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))
        
# Get car rental history 
@app.route("/updateUser", methods=['POST'])
def updateUser():
    """

    Get car rental history

    """
    if session.get('admin') != None:
        if request.method == 'POST':
            userid = request.form['userid']
            with DatabaseUtils() as db:
                user = db.getUser(userid)
                return render_template("updateUser.html", user = user)
        return render_template("updateUser.html")
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))


@app.route("/updatingUser", methods=['POST'])
def updatingUser():
    """

    Updating user data
    :return: string
    """
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        
        print(userid, username, password, firstname, lastname, phone, email, address, city)
        with DatabaseUtils() as db:
            if(db.updateUser(userid, username, password, firstname, lastname, phone, email, address, city)):
                print("{}'s profile is updated".format(username))
                flash("{}'s profile is updated".format(username))
                return redirect(url_for("showAllUsers"))
            else:
                print("Error while updating user profile")
                flash("Error while updating user profile")
                return redirect(url_for("showAllUsers"))

@app.route("/deleteUser", methods=['POST'])
def deleteUser()
    """
    
    Delete user
    :return: string
    """
    if request.method == 'POST':
        userid = request.form['userid']
        with DatabaseUtils() as db:
            if(db.deleteUser(userid)):
                print("UserID: {} 's profile is removed".format(userid))
                flash("UserID: {} 's profile is removed".format(userid))
                return redirect(url_for("showAllUsers"))
            else:
                print("Error while removing user profile")
                flash("Error while removing user profile")
                return redirect(url_for("showAllUsers"))

# List cars with editing function for Admins
@app.route("/showAdminCars", methods=['GET', 'POST'])
def showAdminCars():
    """

    List cars with editing function for Admins
    :return: string
    """
    if session.get('admin') != None:
        with DatabaseUtils() as db:
            cars = db.getAllCar()
        return render_template("adminCars.html", **locals())
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))

# Routing update car
@app.route("/updateCar", methods=['POST'])
def updateCar():
    """

    Routing update car
    :return: int
    """
    if request.method == 'POST':
        carid = request.form['carid']
        with DatabaseUtils() as db:
            car = db.getCar(carid)
        return render_template("updateCar.html", car = car)
    return render_template("updateCar.html")

# Updating individual car
@app.route("/updatingCar", methods=['POST'])
def updatingCar():
    """

    Updating individual car
    :return: string
    """
    if request.method == 'POST':
        carid = request.form['carid']
        make = request.form['make']
        model = request.form['model']
        cartype = request.form['type']
        seats = request.form['seats']
        color = request.form['color']
        location = request.form['location']
        cost = request.form['cost']
        available = request.form['status']
        lat = request.form['lat']
        lng = request.form['lng']
        print(carid, make, model, cartype, seats, color, location, cost, available, lat, lng)

        with DatabaseUtils() as db:
            if(db.updateCar(carid, make, model, cartype, seats, color, location, cost, available, lat, lng)):
                print("CarID : {} is updated".format(carid))
                flash("CarID : {} is updated".format(carid))
                return redirect(url_for("showAdminCars"))
            else:
                print("Error while updating car profile")
                flash("Error while updating car profile")
                return redirect(url_for("showAdminCars"))

# Updating individual car
@app.route("/deleteCar", methods=['POST'])
def deleteCar():
    """

    Updating individual car
    :return: int
    """
    if request.method == 'POST':
        carid = request.form['carid']
        with DatabaseUtils() as db:
            if(db.deleteCar(carid)):
                print("CarID : {} is removed".format(carid))
                flash("CarID : {} is removed".format(carid))
                return redirect(url_for("showAdminCars"))
            else:
                print("Error while removing car profile")
                flash("Error while removing car profile")
                return redirect(url_for("showAdminCars"))


@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
    """

    Add user to database
    :return: string
    """
    if session.get('admin') != None:
        if request.method == 'POST':
            #Data collected from register form
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            city = request.form['city']

            with DatabaseUtils() as db:
                if(db.checkUsername(username)):
                    if(db.insertPerson(username, sha256_crypt.hash(password), firstname, lastname,phone,email,address, city)):
                        print("{} is inserted successfully.".format(username))
                        flash("{} is inserted successfully.".format(username))
                        return redirect(url_for("addUser"))
                    else:
                        print("{} failed to be inserted.".format(username))
                        flash("{} failed to be inserted.".format(username))
                        return redirect(url_for("addUser"))
                else:
                    print("{} already exist, try a different username.".format(username))
                    flash("{} already exist, try a different username.".format(username))
                    return redirect(url_for("addUser"))
        
        return render_template("add.html")
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))

@app.route("/addCar", methods=['GET', 'POST'])
def addCar():
    """

    Add car to database
    :return: string
    """
    if session.get('admin') != None:
        if request.method == 'POST':
            make = request.form['make']
            model = request.form['model']
            cartype = request.form['type']
            seats = request.form['seats']
            color = request.form['color']
            location = request.form['location']
            cost = request.form['cost']
            lat = request.form['lat']
            lng = request.form['lng']
            available = request.form['status']
            with DatabaseUtils() as db:
                if(db.addCar(make, model, cartype, seats, color, location, cost, available, lat, lng)):
                    print("{} {} is inserted successfully.".format(make,model))
                    flash("{} {} is inserted successfully.".format(make,model))
                    return redirect(url_for("addUser"))
                else:
                    print("{} {} failed to be inserted.".format(make,model))
                    flash("{} {} failed to be inserted.".format(make,model))
                    return redirect(url_for("addUser"))
        return render_template("add.html") 
    else:
        print("You are not an authorized admin")
        flash("You are not an authorized admin")
        return redirect(url_for('home'))

# Reporting cars with issue and update their availability status to "Faulty"
@app.route("/reportCar", methods=['POST'])
def reportCar():
    """

    Reporting cars with issue and update their availability status to "Faulty"
    Remove this comment if pushbullet importing is working properly
    pb.push_note("Faulty Car Notification", body)
    :return: int
    """
    if request.method == 'POST':
        carid = request.form['carid']
        body = "CarID: {} is reported faulty by Admin".format(carid)
        with DatabaseUtils() as db:
            if(db.reportCar(carid)):
                send_notification_via_pushbullet("Faulty Car Notification", body)
                # Remove this comment if pushbullet importing is working properly
                # pb.push_note("Faulty Car Notification", body)
                print("CarID: {} is reported successfully.".format(carid))
                flash("CarID: {} is reported successfully.".format(carid))
                return redirect(url_for("showAdminCars"))
            else:
                print("Error while reporting CarID: {} ".format(carid))
                flash("Error while reporting CarID: {} ".format(carid))
                return redirect(url_for("showAdminCars"))

# Helper function for send notification to engineer
# Since my pushbullet didn't work on my windows, I used this HTTP Request method
def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error, Something is wrong')
    else:
        print('Faulty Car Message Sent')

# Displaying visual board chart #1
@app.route("/managerBoard1", methods=['GET', 'POST'])
def managerBoard1():
    """

    Displaying visual board chart #1
    :return: boolean
    """
    if session.get('manager') != None:
        return render_template("managerBoard1.html")
    else:
        print("You are not an authorized manager")
        flash("You are not an authorized manager")
        return redirect(url_for('home'))

# Displaying visual board chart #2
@app.route("/managerBoard2", methods=['GET', 'POST'])
def managerBoard2():
    """

    Displaying visual board chart #2
    :return: boolean
    """
    if session.get('manager') != None:
        return render_template("managerBoard2.html")
    else:
        print("You are not an authorized manager")
        flash("You are not an authorized manager")
        return redirect(url_for('home'))

# Displaying visual board chart #3
@app.route("/managerBoard3", methods=['GET', 'POST'])
def managerBoard3():
    """
     Displaying visual board chart #3
    :return:
    """
    if session.get('manager') != None:
        return render_template("managerBoard3.html")
    else:
        print("You are not an authorized manager")
        flash("You are not an authorized manager")
        return redirect(url_for('home'))

# Displaying maps with maker homepage for Engineer
@app.route("/engineer1", methods=['GET', 'POST'])
def engineer1():
    """

    Displaying maps with maker homepage for Engineer
    :return: string
    """
    with DatabaseUtils() as db:
        position = db.getFaultyCar()
    return render_template("engineer1.html",position=position)

# Displaying maps with circle area homepage for Engineer
@app.route("/engineer2", methods=['GET', 'POST'])
def engineer2():
    """

    Displaying maps with circle area homepage for Engineer
    :return: string
    """
    with DatabaseUtils() as db:
        position = db.getFaultyCar()
    return render_template("engineer2.html",position=position)



################# Below are testing routes ##########################
@app.route("/chart", methods=['POST', 'GET'])
def chart():
    """

    Testing function

    """
    while True:
        x = random.randint(1,20)
        sleep(2)
        print(x)
        return render_template("chart.html", **locals())
    
    return render_template("chart.html", **locals())

@app.route("/gchart", methods=['POST', 'GET'])
def gchart():
    """

    Testing function

    """
    return render_template("gchart.html", **locals())

@app.route("/loginURL", methods=['GET', 'POST'])
def loginURL():
    """

    Testing function

    """
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        print(request.form)
        return redirect(url_for('testURL', id=id,username=username,password=password), code=307)

    return render_template("loginURL.html")


@app.route("/testURL/<id>/<username>/<password>", methods=['POST'])
def testURL(id, username, password):
    """

    testing function
    
    LoginURL function

    """
    #return "The ID is " + str(id) + " Name is " + username + " Password is " + password
    return render_template("testURL.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)
