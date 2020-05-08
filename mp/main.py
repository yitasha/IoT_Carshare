from flask import Flask, render_template, request,url_for, redirect, session, flash
from database import DatabaseUtils
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'asdasd12easd123rdada'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
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
    if session.get('username') != None:
        with DatabaseUtils() as db:
            person = db.getPerson(session.get('username'))
            booking = db.showBooking(person[0])
            history = db.showHistory(person[0])

        return render_template("myprofile.html", person = person, booking = booking, history=history)
    else:
        return login()

@app.context_processor
def utility_processor():
    def car(bookingid):
        with DatabaseUtils() as db:
            car = db.getCar(bookingid)
            return car[1] + "-" + car[2]
    return dict(car=car)

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('userid', None)
    session.clear()
    flash("You have logged out!")
    return home()

@app.route("/cars", methods=['GET', 'POST'])
def cars():
    with DatabaseUtils() as db:
        cars = db.getAvailCar()

    return render_template("cars.html", **locals())

@app.route("/book", methods=['POST'])
def book():
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
    if request.method == "POST":
        userid = request.form['userid']
        carid = request.form['carid']
        cost = request.form['price']
        startDate =  datetime.strptime(request.form['startDate'], '%Y-%m-%d').date()
        endDate = datetime.strptime(request.form['endDate'], '%Y-%m-%d').date()
        #For updating car's availability after booking
        avail = "False"
        #Check if input date is valid
        if(endDate > startDate):
            with DatabaseUtils() as db:
                #Check car availability
                if(db.checkCarAvail(carid)):
                    #Check if record is inserted
                    if(db.insertBooking(userid, carid, int(cost), startDate, endDate)):
                        #If it is inserted, update car availability
                        if(db.updateCarAvail(carid, avail)):
                            print("Car ID: {} is booked from {} till {}".format(carid, startDate, endDate))
                            flash("Car ID: {} is booked from {} till {}".format(carid, startDate, endDate))
                            return redirect(url_for("home"))
                else:
                    print("Error, Car ID: {} is not booked, try again later".format(carid))
                    flash("Error, Car ID: {} is not booked, try again later".format(carid))
                    return redirect(url_for("home"))
        else:
            print("Error, minimum booking is 1 day")
            flash("Error, minimum booking is 1 day")
            return redirect(url_for("home"))
    
    return render_template("test.html", **locals())

@app.route("/cancelbook", methods=['POST'])
def cancelbook():
    if request.method == "POST":
        carid = request.form['carid']
        bookid = request.form['bookid']
        avail = "True"
        with DatabaseUtils() as db:
            if(db.cancelBooking(bookid) and db.updateCarAvail(carid, avail)):
                print("Booking ID: {} is successfully canceled".format(bookid))
                flash("Booking ID: {} is successfully canceled".format(bookid))
            else:
                print("Error, please try cancel it again later.")
                flash("Error, please try cancel it again later.")
    return redirect(url_for("myprofile"))


    
    

################# Below are testing routes 测试专用 ##########################
@app.route("/loggedin", methods=['POST'])
def loggedin():
    #Data collected from register form
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    
    #Username check
    if username != "Yi":
        return redirect(url_for('login'))

    return render_template("loggedin.html", **locals())

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

    #return "The ID is " + str(id) + " Name is " + username + " Password is " + password
    return render_template("testURL.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)