from flask import Flask, render_template, request,url_for, redirect, session, flash
from database import DatabaseUtils
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'asdasd12easd123rdada'

@app.route("/")
def home():

    return render_template("home.html")

#after login, redirect to about()
@app.route("/about", methods=['GET', 'POST'])
def about():
    if session.get('username') != None:
        #Data collected from login form, then passed to about.html
        var = "Hello"
        #username = request.form['username']
        #password = request.form['password']
        
        #Testing an array to be used in about.html
        data = ("one", "two", "three")
        return render_template("about.html", **locals())
    else:
        return login()

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
        return redirect(url_for('about'))
    elif request.method == 'POST':
        #clear session username, then assign new value
        session.pop('username', None)
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('about'))
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    session.pop('username', None)
    return home()

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