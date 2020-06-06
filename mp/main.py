from flask import Flask, render_template, request,url_for, redirect, session, flash
from werkzeug.utils import secure_filename
from database import DatabaseUtils
from passlib.hash import sha256_crypt
from datetime import datetime
from add_event import Calendar
from time import sleep
import random
import os
import cv2 

UPLOAD_FOLDER = 'mp/static/image'

app = Flask(__name__)
app.secret_key = 'asdasd12easd123rdada'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        
        with DatabaseUtils() as db:
            if(db.checkUsername(username)):
                if(db.insertPerson(username, sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
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

#Register for 3 type of admins
@app.route("/registerA", methods=['GET', 'POST'])
def registerA():
    if request.method == 'POST':
        #Data collected from register form
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        usertype = request.form['type']

        with DatabaseUtils() as db:
            if(usertype == "admin"):
                if(db.insertAdmin(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
                    print("{} inserted successfully.".format(username))
                    flash("Thank you for registering {}".format(firstname))
                    return redirect(url_for("home"))
                else:
                    print("{} failed to be inserted.".format(username))
                    flash("{} failed to be inserted.".format(username))
                    return redirect(url_for("registerA"))
            elif(usertype == "manager"):
                if(db.insertManager(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
                    print("{} inserted successfully.".format(username))
                    flash("Thank you for registering {}".format(firstname))
                    return redirect(url_for("home"))
                else:
                    print("{} failed to be inserted.".format(username))
                    flash("{} failed to be inserted.".format(username))
                    return redirect(url_for("registerA"))
            elif(usertype == "engineer"):
                if(db.insertEngineer(sha256_crypt.hash(username), sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
                    print("{} inserted successfully.".format(username))
                    flash("Thank you for registering {}".format(firstname))
                    return redirect(url_for("home"))
                else:
                    print("{} failed to be inserted.".format(username))
                    flash("{} failed to be inserted.".format(username))
                    return redirect(url_for("registerA"))
            else:
                print("{} failed to be inserted.".format(username))
                flash("{} failed to be inserted.".format(username))
                return redirect(url_for("registerA"))
    
    return render_template("registerA.html")

#Ask for 3 type of admins
@app.route("/askLogin", methods=['GET', 'POST'])
def askLogin():
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
    return render_template("loginAdmins.html", **locals())

# 3 type of admins login
@app.route("/processLoginAdmins", methods=['GET','POST'])
def processLoginAdmins():
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
                if(db.checkAdmin(username, password)):
                    session['manager'] = request.form['username']
                    print("Passed")
                    return redirect(url_for("askLogin"))
                else:
                    print("{}'s Password is wrong.".format(username))
                    flash("{}'s Password is wrong.".format(username))
                    return redirect(url_for("askLogin"))
        elif check == 'Engineer':
            with DatabaseUtils() as db:
                if(db.checkAdmin(username, password)):
                    session['engineer'] = request.form['username']
                    print("Passed")
                    return redirect(url_for("askLogin"))
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
    with DatabaseUtils() as db:
        booking = db.getAllBookings()
        return render_template("bookings.html", booking = booking)

# Get car rental history 
@app.route("/showAllUsers", methods=['GET','POST'])
def showAllUsers():
    with DatabaseUtils() as db:
        users = db.getAllUsers()
        return render_template("users.html", users = users)
    
# Get car rental history 
@app.route("/updateUser", methods=['POST'])
def updateUser():
    if request.method == 'POST':
        userid = request.form['userid']
        with DatabaseUtils() as db:
            user = db.getUser(userid)
            return render_template("updateUser.html", user = user)
    return render_template("updateUser.html")


@app.route("/updatingUser", methods=['POST'])
def updatingUser():
    if request.method == 'POST':
        userid = request.form['userid']
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        print(userid, username, password, firstname, lastname, phone, email, address)
        with DatabaseUtils() as db:
            if(db.updateUser(userid, username, password, firstname, lastname,phone,email,address)):
                print("{}'s profile is updated".format(username))
                flash("{}'s profile is updated".format(username))
                return redirect(url_for("showAllUsers"))
            else:
                print("Error while updating user profile")
                flash("Error while updating user profile")
                return redirect(url_for("showAllUsers"))

@app.route("/deleteUser", methods=['POST'])
def deleteUser():
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
    with DatabaseUtils() as db:
        cars = db.getAllCar()
    return render_template("adminCars.html", **locals())

# Routing update car
@app.route("/updateCar", methods=['POST'])
def updateCar():
    if request.method == 'POST':
        carid = request.form['carid']
        with DatabaseUtils() as db:
            car = db.getCar(carid)
        return render_template("updateCar.html", car = car)
    return render_template("updateCar.html")

# Updating individual car
@app.route("/updatingCar", methods=['POST'])
def updatingCar():
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
        print(carid, make, model, cartype, seats, color, location, cost, available)

        with DatabaseUtils() as db:
            if(db.updateCar(carid, make, model, cartype, seats, color, location, cost, available)):
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
    if request.method == 'POST':
        #Data collected from register form
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        
        with DatabaseUtils() as db:
            if(db.checkUsername(username)):
                if(db.insertPerson(username, sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
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

@app.route("/addCar", methods=['GET', 'POST'])
def addCar():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        cartype = request.form['type']
        seats = request.form['seats']
        color = request.form['color']
        location = request.form['location']
        cost = request.form['cost']
        available = request.form['status']
        with DatabaseUtils() as db:
            if(db.addCar(make, model, cartype, seats, color, location, cost, available)):
                print("{} {} is inserted successfully.".format(make,model))
                flash("{} {} is inserted successfully.".format(make,model))
                return redirect(url_for("addUser"))
            else:
                print("{} {} failed to be inserted.".format(make,model))
                flash("{} {} failed to be inserted.".format(make,model))
                return redirect(url_for("addUser"))
    return render_template("add.html") 

# Reporting cars with issue and update their availability status to "Faulty"
@app.route("/reportCar", methods=['POST'])
def reportCar():
    if request.method == 'POST':
        carid = request.form['carid']
        with DatabaseUtils() as db:
            if(db.reportCar(carid)):
                print("CarID: {} is reported successfully.".format(carid))
                flash("CarID: {} is reported successfully.".format(carid))
                return redirect(url_for("showAdminCars"))
            else:
                print("Error while reporting CarID: {} ".format(carid))
                flash("Error while reporting CarID: {} ".format(carid))
                return redirect(url_for("showAdminCars"))





################# Below are testing routes ##########################
@app.route("/chart", methods=['POST', 'GET'])
def chart():
    while True:
        x = random.randint(1,20)
        sleep(2)
        print(x)
        return render_template("chart.html", **locals())
    
    return render_template("chart.html", **locals())

@app.route("/gchart", methods=['POST', 'GET'])
def gchart():
    return render_template("gchart.html", **locals())

@app.route("/loginURL", methods=['GET', 'POST'])
def loginURL():
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