from flask import Flask, render_template, request,url_for, redirect, session, flash
from database import DatabaseUtils
from passlib.hash import sha256_crypt

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
            if(db.insertPerson(username, sha256_crypt.hash(password), firstname, lastname,phone,email,address)):
                print("{} inserted successfully.".format(username))
                flash('Thank you for registering ' + firstname)
                return redirect(url_for("home"))
            else:
                print("{} failed to be inserted.".format(username))
                return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login",  methods=['GET', 'POST'])
def login():
    #If session username exist, means already logged in
    if session.get('username') != None:
        return redirect(url_for('myprofile'))
    elif request.method == 'POST':
        #clear session username, then assign new value
        session.pop('username', None)
        username = request.form['username']
        password = request.form['password']
        with DatabaseUtils() as db:
            if(db.checkPerson(username, password)):
                session['username'] = request.form['username']
                session['userid'] = db.getPerson(username)[0]
                person = db.getPerson(username)
                return redirect(url_for("myprofile", person = person))
            else:
                print("{} 's Password is wrong.".format(username))
                return redirect(url_for("register"))
        
    
    return render_template("login.html")

#after login, redirect to about()
@app.route("/myprofile", methods=['GET', 'POST'])
def myprofile():
    if session.get('username') != None:
        with DatabaseUtils() as db:
            person = db.getPerson(session.get('username'))
        return render_template("myprofile.html", person = person)
    else:
        return login()

@app.route("/logout")
def logout():
    session.clear()
    session.pop('username', None)
    return home()

@app.route("/cars", methods=['GET', 'POST'])
def cars():
    with DatabaseUtils() as db:
        cars = db.getAvailCar()
    return render_template("cars.html", **locals())

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
        #print(request.form)
        return redirect(url_for('testURL', id=id,username=username,password=password))

    return render_template("loginURL.html")


@app.route("/testURL/<id>/<username>/<password>", methods=["POST"])
def testURL(id, username, password):
    #return "The ID is " + str(id) + " Name is " + username + " Password is " + password
    return render_template("testURL.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)